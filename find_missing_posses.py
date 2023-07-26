import numpy as np
import cv2
import os
import json


def load_data_from_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


def find_camera_poses(images_data):
    camera_poses = [np.eye(4)]  # Start with identity matrix for the first image
    for i in range(1, len(images_data)):
        # Extract transformation matrix from data
        pose = np.array(images_data[i]["transform_matrix"])
        # Accumulate the camera poses
        prev_pose = camera_poses[-1]
        new_pose = np.dot(prev_pose, pose)
        camera_poses.append(new_pose)

    return camera_poses


def interpolate_camera_poses(camera_poses, num_poses):
    if len(camera_poses) < 2:
        raise ValueError("At least two camera poses are required for interpolation.")

    # Calculate the interpolation step for the poses
    interpolation_step = 1.0 / (num_poses + 1)

    # Get the first and last camera poses
    first_pose = camera_poses[0]
    last_pose = camera_poses[-1]

    interpolated_poses = []
    for i in range(1, num_poses + 1):
        # Interpolate the camera poses using linear interpolation
        t = interpolation_step * i
        interpolated_pose = np.linalg.inv(first_pose) @ last_pose
        interpolated_pose[:3, 3] = t * interpolated_pose[:3, 3]
        interpolated_poses.append(interpolated_pose)

    return interpolated_poses


if __name__ == "__main__":
    # Get the current script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the filename of the JSON file
    json_filename = "fox/transforms.json"

    # Get the full path to the JSON file
    json_path = os.path.join(script_dir, json_filename)

    # Load the data from the JSON file
    data = load_data_from_json(json_path)

    # Now 'data' contains the content of the JSON file, and you can access the required information as follows:
    camera_angle_x = data["camera_angle_x"]
    camera_angle_y = data["camera_angle_y"]
    fl_x = data["fl_x"]
    fl_y = data["fl_y"]
    k1 = data["k1"]
    k2 = data["k2"]
    # ... and so on

    # Accessing the frames' information:
    frames_data = data["frames"]
    for frame in frames_data:
        file_path = frame["file_path"]
        sharpness = frame["sharpness"]
        transform_matrix = frame["transform_matrix"]


    # Step 1 & 2: Extract and match features (not provided in data)

    # Step 3 & 4: Camera Pose Estimation
    camera_poses = find_camera_poses(data["frames"])

    # Step 5: Interpolation
    num_poses_between = 5
    intrinsic_params = [data["fl_x"], data["fl_y"], data["cx"], data["cy"]]
    interpolated_poses = interpolate_camera_poses(camera_poses, num_poses_between)

    # Your interpolated camera poses and intrinsic parameters are now stored in the 'interpolated_poses' list
