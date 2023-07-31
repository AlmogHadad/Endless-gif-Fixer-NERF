import numpy as np
import json
import os


def circle_center(x, y, z):
    center_x = np.mean(x)
    center_y = np.mean(y)
    center_z = np.mean(z)
    return center_x, center_y, center_z


def calculate_radius(points, center):
    # Calculate the distance between each point and the center
    distances = np.linalg.norm(points - center, axis=1)

    # Calculate the average distance, which represents the radius of the circle
    radius = np.mean(distances)

    return radius


def extract_camera_position_and_orientation(matrixx):
    position = matrixx[:3, 3]
    matrixx[0:3, 2] *= -1
    orientation = matrixx[:3, :3]  # Assuming the camera is looking in the +Z direction
    return position, orientation


# Initialize lists to store camera positions and orientation vectors

camera_positions_x = []
camera_positions_y = []
camera_positions_z = []

# Load the JSON data
with open(os.path.dirname(__file__) + r'\data_example\transforms.json') as json_file:
    data = json.load(json_file)

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

# Number of intermediate frames to generate (excluding the first and last frames)
num_intermediate_frames = 5
center_x,center_y,center_z = circle_center(camera_positions_x, camera_positions_y, camera_positions_z)
center_point = [center_x,center_y,center_z]
points_3d = np.column_stack((camera_positions_x, camera_positions_y, camera_positions_z))
target_distance = 1.2*calculate_radius(points_3d, center_point)

# Perform interpolation between the first and last transformation matrices
interpolated_frames = []
for t in np.linspace(0, 1, num_intermediate_frames + 2)[1:-1]:  # Exclude the endpoints (0 and 1)
    # Interpolate rotation matrix
    rotation_matrix_interpolated = (1 - t) * transform_matrix_first_frame[:3, :3] + t * transform_matrix_last_frame[:3,
                                                                                        :3]

    # Interpolate translation vector
    translation_vector_interpolated = (1 - t) * transform_matrix_first_frame[:3, 3] + t * transform_matrix_last_frame[
                                                                                          :3, 3]

    # Scale the translation vector to maintain the target distance from the center point
    current_distance = np.linalg.norm(translation_vector_interpolated - center_point)
    scaling_factor = target_distance / current_distance
    translation_vector_interpolated = center_point + scaling_factor * (translation_vector_interpolated - center_point)

    # Combine rotation and translation into a single transformation matrix
    intermediate_pose_matrix = np.eye(4)
    intermediate_pose_matrix[:3, :3] = rotation_matrix_interpolated
    intermediate_pose_matrix[:3, 3] = translation_vector_interpolated

    # Append the intermediate frame with its transformation matrix to the new data
    new_frame = {
        "file_path": f"./images/interpolated_frame_{t:.2f}.jpg",
        "sharpness": 0,  # Set the sharpness value as per your requirement
        "transform_matrix": intermediate_pose_matrix.tolist()
    }
    interpolated_frames.append(new_frame)

# Append the new frames to the existing frames
data['frames'].extend(interpolated_frames)

# Save the updated data to a new JSON file
with open('data_example/updated_data_2.json', 'w') as json_file:
    json.dump(data, json_file, indent=2)

print("New data with interpolated frames has been created and saved as 'updated_data_2.json'.")
