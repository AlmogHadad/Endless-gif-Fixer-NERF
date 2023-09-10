import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
import json
import os
from random import random

GAP_EDGE = 10


def circle_data():
    # Parameters of the circle
    radius = 1.0
    num_points = 100

    # Generate points on the circle using spherical coordinates
    theta = np.linspace(0, 2 * np.pi, num_points)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z = np.random.uniform(-0.2, 0.2, num_points)  # Random z values in the range [-0.1, 0.1]

    circle = np.column_stack([x, y, z])
    circle = circle[2 * GAP_EDGE:]
    return circle

# Generate synthetic data for demonstration
def generate_data():
    data = circle_data()
    data = torch.tensor(data, dtype=torch.float32)
    x_data = data[:, 0].unsqueeze(0).T
    y_data = data[:, 1].unsqueeze(0).T
    z_data = data[:, 2].unsqueeze(0).T
    return x_data, y_data, z_data


def frame_rate_function(points_matrix):
    total_distance = 0
    num_pairs = len(points_matrix) - 1

    for i in range(num_pairs):
        distance = np.linalg.norm(points_matrix[i + 1] - points_matrix[i])
        total_distance += distance

    average_distance = total_distance / num_pairs
    gap_distance = np.linalg.norm(points_matrix[0] - points_matrix[-1])
    return int(np.ceil(gap_distance / average_distance))


def plot_camera_positions_with_direction(json_data):
    # Load JSON data
    data = json.loads(json_data)

    # Function to extract camera positions and orientation vectors from the transformation matrix
    def extract_camera_position_and_orientation(matrix):
        position = matrix[:3, 3]
        matrix[0:3, 2] *= -1
        orientation = matrix[:3, :3]  # Assuming the camera is looking in the +Z direction
        return position, orientation

    # Initialize lists to store camera positions and orientation vectors
    camera_positions_x = []
    camera_positions_y = []
    camera_positions_z = []

    # Extract camera positions and orientation vectors from each frame's transformation matrix
    for frame in data["frames"]:
        matrix = np.array(frame["transform_matrix"])
        camera_position, orientation_vector = extract_camera_position_and_orientation(matrix)
        camera_positions_x.append(camera_position[0])
        camera_positions_y.append(camera_position[1])
        camera_positions_z.append(camera_position[2])

    # Extract the transformation matrices for the first and last frames
    transform_matrix_first_frame = np.array(data['frames'][0]['transform_matrix'])
    transform_matrix_last_frame = np.array(data['frames'][-1]['transform_matrix'])

    return np.column_stack((camera_positions_x, camera_positions_y,
                            camera_positions_z)), transform_matrix_first_frame, transform_matrix_last_frame


def filter_points_between(p1, p2, points):
    v1 = p2 - p1
    v2 = points - p1
    dot_product = np.sum(v1 * v2, axis=1)
    projection = dot_product / np.sum(v1 ** 2)
    filtered_points = points[(projection >= 0) & (projection <= 1)]
    return filtered_points

def noise_immitation(num_of_frames,x_new,y_new,z_new):
    axis_std = []
    for i in range(0, len(data), ):
        partial_std = np.std(data[i:i + num_of_frames], axis=0)
        axis_std.append(partial_std)
    axis_std = np.mean(axis_std, axis=0)
    # Set the mean and standard deviation of the normal distribution
    mean = 0
    std_deviation = 1
    # Generate a single random number with a normal distribution
    for i in range(len(x_new)):
        random_number = np.random.normal(mean, std_deviation, 3)
        x_new[i] = x_new[i] + random_number[0] * axis_std[0] * .7
        y_new[i] = y_new[i] + random_number[1] * axis_std[1] * .7
        z_new[i] = z_new[i] + random_number[2] * axis_std[2] * .7

    return x_new, y_new, z_new

PATH = r'data_example\SandBox\transforms2.json'
with open(PATH, 'r') as file:
    # Initialize an empty list to store the rows of data
    mat = file.read()
    data, transform_matrix_first_frame, transform_matrix_last_frame = plot_camera_positions_with_direction(mat)

# data = circle_data()

num_intermediate_frames = frame_rate_function(data)

start_p = data[0]
end_p = data[-1]
points_left = data[:GAP_EDGE]
points_right = data[-GAP_EDGE:]


class NonlinearApproximator(nn.Module):
    def __init__(self):
        super(NonlinearApproximator, self).__init__()
        self.hidden_layers = [18, 24]
        self.fc1 = nn.Linear(1, self.hidden_layers[0])  # Input dimension is 1 (time)
        self.fc2 = nn.Linear(self.hidden_layers[0], self.hidden_layers[1])
        self.fc3 = nn.Linear(self.hidden_layers[1], 3)  # Output has 3 dimensions for x, y, z

    def forward(self, x):
        x = self.fc1(x)
        x = torch.sigmoid(x)
        x = self.fc2(x)
        x = torch.sigmoid(x)
        output = self.fc3(x)
        return output


# Create the model, loss function, and optimizer
model = NonlinearApproximator()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# time_data, target_data = generate_data()
target_data = np.concatenate((points_right, points_left))
time_data = [i for i in range(1, GAP_EDGE + 1)] + [j + num_intermediate_frames for j in range(GAP_EDGE, 2 * GAP_EDGE)]
time_data = torch.tensor(time_data, dtype=torch.float32).unsqueeze(1)  # Convert to 2D tensor
target_data = torch.tensor(target_data, dtype=torch.float32)

# Training loop
num_epochs = 2000
for epoch in range(num_epochs):
    optimizer.zero_grad()
    outputs = model(time_data)
    loss = criterion(outputs, target_data)
    loss.backward()
    optimizer.step()
    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

# Test the model
with torch.no_grad():
    predicted_xyz = model(time_data)
    x_fit, y_fit, z_fit = predicted_xyz[:, 0], predicted_xyz[:, 1], predicted_xyz[:, 2]

with torch.no_grad():
    new_time_data = [i + GAP_EDGE for i in range(num_intermediate_frames)]
    new_time_data = torch.tensor(new_time_data, dtype=torch.float32).unsqueeze(1)  # Convert to 2D tensor
    predicted_xyz = model(new_time_data)
    x_new, y_new, z_new = predicted_xyz[:, 0], predicted_xyz[:, 1], predicted_xyz[:, 2]

x_new, y_new, z_new = noise_immitation(num_intermediate_frames,x_new,y_new,z_new)


# Plot the original data points and the predicted points
plt.plot(time_data, target_data[:, 0], label='True X')
plt.plot(time_data, target_data[:, 1], label='True Y')
plt.plot(time_data, target_data[:, 2], label='True Z')
plt.plot(time_data, x_fit, label='Predicted X')
plt.plot(time_data, y_fit, label='Predicted Y')
plt.plot(time_data, z_fit, label='Predicted Z')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Time-to-3D-Point Prediction')
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
data = data[1:-1]
ax.scatter(data[:, 0], data[:, 1], data[:, 2], c='blue', marker='o')
# ax.scatter(x_fit, y_fit, z_fit, color='red')
ax.scatter(x_new, y_new, z_new, color='green')
# ax.scatter(px, py, pz, color='orange',s=50)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Polynomial Regression')
plt.show()

with open('./data_example/SandBox/transforms2.json', 'r') as file:
    json_data = file.read()

data = json.loads(json_data)
transform_matrix_first_frame = np.array(data['frames'][0]['transform_matrix'])
transform_matrix_last_frame = np.array(data['frames'][-1]['transform_matrix'])

# Number of intermediate frames to generate (excluding the first and last frames)
num_intermediate_frames = len(new_time_data)
counter = 0
interpolated_frames = []
# Append the intermediate frame with its transformation matrix to the new data
for t in np.linspace(0, 1, num_intermediate_frames + 2)[1:-1]:  # Exclude the endpoints (0 and 1)
    # Interpolate rotation matrix
    rotation_matrix_interpolated = (1 - t) * transform_matrix_first_frame[:3, :3] + t * transform_matrix_last_frame[:3,
                                                                                        :3]

    # Interpolate translation vector
    translation_vector_interpolate = (1 - t) * transform_matrix_first_frame[:3, 3] + t * transform_matrix_last_frame[:3,
                                                                                         3]

    # Combine rotation and translation into a single transformation matrix
    intermediate_pose_matrix = np.eye(4)
    intermediate_pose_matrix[:3, :3] = rotation_matrix_interpolated
    intermediate_pose_matrix[:3, 3] = [x_new[counter], y_new[counter], z_new[counter]]
    counter += 1
    new_frame = {
        "file_path": f"./images/interpolated_frame_{t:.2f}.jpg",
        "sharpness": 0,  # Set the sharpness value as per your requirement
        "transform_matrix": intermediate_pose_matrix.tolist()
    }
    interpolated_frames.append(new_frame)

data['frames'].extend(interpolated_frames)

# Write the modified JSON data back to the file
with open('./data_example/SandBox/transforms3.json', 'w') as file:
    json.dump(data, file, indent=2)
