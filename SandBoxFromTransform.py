import json
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_camera_positions(json_data):
    # Load JSON data
    data = json.loads(json_data)

    # Function to extract camera positions from the transformation matrix
    def extract_camera_position(matrix):
        return matrix[:3, 3]

    # Initialize lists to store camera positions
    camera_positions_x = []
    camera_positions_y = []
    camera_positions_z = []

    # Extract camera positions from each frame's transformation matrix
    for frame in data["frames"]:
        matrix = np.array(frame["transform_matrix"])
        camera_position = extract_camera_position(matrix)
        camera_positions_x.append(camera_position[0])
        camera_positions_y.append(camera_position[1])
        camera_positions_z.append(camera_position[2])

    # Plot the camera positions in 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(camera_positions_x, camera_positions_y, camera_positions_z, marker='o', s=100)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Camera Positions')

    plt.show()

# Example usage:
# Assuming your JSON data is stored in a file called 'data.json'
with open(os.path.dirname(__file__) + r'\data_example\transforms.json', 'r') as file:
    json_data = file.read()

plot_camera_positions(json_data)
