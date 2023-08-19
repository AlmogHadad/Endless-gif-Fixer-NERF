import numpy as np
import json
import os

# Load the JSON data
with open('data_example/horse_gap_old/transforms.json') as json_file:
    data = json.load(json_file)

# Extract the transformation matrices for the first and last frames
transform_matrix_first_frame = np.array(data['frames'][0]['transform_matrix'])
transform_matrix_last_frame = np.array(data['frames'][-1]['transform_matrix'])

# Number of intermediate frames to generate (excluding the first and last frames)
num_intermediate_frames = 5

# Perform interpolation between the first and last transformation matrices
interpolated_frames = []
for t in np.linspace(0, 1, num_intermediate_frames + 2)[1:-1]:  # Exclude the endpoints (0 and 1)
    # Interpolate rotation matrix
    rotation_matrix_interpolated = (1 - t) * transform_matrix_first_frame[:3, :3] + t * transform_matrix_last_frame[:3, :3]

    # Interpolate translation vector
    translation_vector_interpolated = (1 - t) * transform_matrix_first_frame[:3, 3] + t * transform_matrix_last_frame[:3, 3]

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
with open('./data_example/horse_gap_old/transforms3.json', 'w') as json_file:
    json.dump(data, json_file, indent=2)

# print("New data with interpolated frames has been created and saved as 'updated_data.json'.")
