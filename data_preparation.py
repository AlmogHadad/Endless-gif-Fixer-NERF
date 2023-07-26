import numpy as np
import matplotlib.pyplot as plt

def parse_images(images_file):
    image_data = {}
    with open(images_file, 'r') as f:
        for idx, line in enumerate(f):
            if line.startswith("#"):
                continue
            if idx % 2 == 0:
                # print(line)
                image_id, qw, qx, qy, qz, tx, ty, tz, camera_id, image_name = line.strip().split()
                image_data[image_id] = {'image_path': image_name, 'camera_id': camera_id,
                                    'pose': np.array([float(tx), float(ty), float(tz)])}
            else:
                image_points = line.strip().split()
    return image_data


def parse_cameras(cameras_file):
    camera_data = {}
    with open(cameras_file, 'r') as f:
        for line in f:
            if line.startswith("#"):
                continue
            camera_id, model, width, height, *params = line.strip().split()

            # Extract focal length and other relevant parameters based on your camera model format
            focal_length = float(params[0])  # Modify this line according to your camera model parameter index
            camera_data[camera_id] = {'focal_length': focal_length, 'principal_point': [0.0, 0.0]}  # Modify principal point if available
    return camera_data


def parse_points3D(points3D_file):
    with open(points3D_file, 'r') as f:
        lines = f.readlines()

    data = {}
    for line in lines:
        if not line.startswith('#'):
            elements = line.strip().split()
            point3D_id = int(elements[0])
            x, y, z = float(elements[1]), float(elements[2]), float(elements[3])
            r, g, b = int(elements[4]), int(elements[5]), int(elements[6])
            error = float(elements[7])
            track_data = [(int(elements[i]), int(elements[i+1])) for i in range(8, len(elements), 2)]
            data[point3D_id] = {'position': np.array([x, y, z]), 'color': np.array([r, g, b]), 'error': error, 'track': track_data}

    return data

# Set the paths to the COLMAP output files
images_file = 'images.txt'
points3D_file = 'points3D.txt'
cameras_file = 'cameras.txt'

# Parse the COLMAP output
image_data = parse_images(images_file)
camera_data = parse_cameras(cameras_file)
points = parse_points3D(points3D_file)
# Prepare the data for training TinyNERF
images = []
poses = []
focal_lengths = []

for image_id, image_info in image_data.items():
    image_path = image_info['image_path']
    camera_id = image_info['camera_id']
    pose = image_info['pose']
    focal_length = camera_data['camera_id']['focal_length']

    images.append(image_path)
    poses.append(pose)
    focal_lengths.append(focal_length)
