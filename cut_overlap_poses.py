import json
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.optimize import minimize

###
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import KMeans
###


import math


def find_middle_point(points):
    total_x = 0
    total_y = 0
    num_points = len(points)

    for x, y in points:
        total_x += x
        total_y += y

    middle_x = total_x / num_points
    middle_y = total_y / num_points

    return middle_x, middle_y


def line_equation(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - slope * x1
    return slope, intercept


def intersection_point(line1, line2):
    slope1, intercept1 = line1
    slope2, intercept2 = line2
    x = (intercept2 - intercept1) / (slope1 - slope2)
    y = slope1 * x + intercept1
    return x, y


def find_intersection_point(points):
    middle_point = find_middle_point(points)

    for i in range(int(len(points)/2), len(points)):
        if points[i] != middle_point:
            line1 = [(points[i][0], points[i][1]), (middle_point[0], middle_point[1])]

            for j in range(1, i-3):
                if j != i and j+1 != i:
                    line2 = [(points[j+1][0], points[j+1][1]), (points[j][0], points[j][1])]

                    if do_line_segments_intersect(line1, line2):
                        plt.plot([line1[0][0], line1[1][0]], [line1[0][1], line1[1][1]], color='blue')
                        plt.plot([line2[0][0], line2[1][0]], [line2[0][1], line2[1][1]], color='green')
                        plt.scatter(points[j][0], points[j][1], color='brown', s=50)
                        plt.scatter(points[j+1][0], points[j+1][1], color='yellow', s=50)
                        plt.scatter(points[i][0], points[i][1], color='grey', s=50)
                        plt.scatter(middle_point[0], middle_point[1], color='pink', s=50)
                        # plt.show()
                        return i, points[i], points[i-1]

    # If no intersection is found, return the point and its adjacent points
    return -1, points[-1], points[-2], None


def do_line_segments_intersect(segment1, segment2):
    x1, y1 = segment1[0]
    x2, y2 = segment1[1]
    x3, y3 = segment2[0]
    x4, y4 = segment2[1]

    # Check if the endpoints of one segment are on opposite sides of the other segment.
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # Collinear
        return 1 if val > 0 else 2  # Clockwise or counterclockwise

    o1 = orientation((x1, y1), (x2, y2), (x3, y3))
    o2 = orientation((x1, y1), (x2, y2), (x4, y4))
    o3 = orientation((x3, y3), (x4, y4), (x1, y1))
    o4 = orientation((x3, y3), (x4, y4), (x2, y2))

    # General case where segments intersect.
    if o1 != o2 and o3 != o4:
        return True

    # Special cases where segments are collinear and overlapping.
    if o1 == 0 and (min(x1, x2) <= x3 <= max(x1, x2)) and (min(y1, y2) <= y3 <= max(y1, y2)):
        return True
    if o2 == 0 and (min(x1, x2) <= x4 <= max(x1, x2)) and (min(y1, y2) <= y4 <= max(y1, y2)):
        return True
    if o3 == 0 and (min(x3, x4) <= x1 <= max(x3, x4)) and (min(y3, y4) <= y1 <= max(y3, y4)):
        return True
    if o4 == 0 and (min(x3, x4) <= x2 <= max(x3, x4)) and (min(y3, y4) <= y2 <= max(y3, y4)):
        return True

    return False


def calculate_angle_between_lines(points):
    if len(points) < 3:
        raise ValueError("The list of points should have at least three points.")

    # Extract the last two points
    # last_point = points[-1]
    # second_last_point = points[-2]
    middle_point = find_middle_point(points)
    # for i in points:
    #     if i[0]
    # Calculate the vector of the last line segment
    index_last_point, last_point, second_last_point = find_intersection_point(points)

    last_line_vector = (last_point[0] - second_last_point[0], last_point[1] - second_last_point[1])

    angles = []

    for i in range(int(len(points) / 2)):
        # Calculate the vector of the line segment between the last point and the current point
        current_point = points[i]
        current_line_vector = (last_point[0] - current_point[0],  last_point[1] - current_point[1])

        # Calculate the dot product and magnitudes
        dot_product = last_line_vector[0] * current_line_vector[0] + last_line_vector[1] * current_line_vector[1]
        magnitude_last = math.sqrt(last_line_vector[0] ** 2 + last_line_vector[1] ** 2)
        magnitude_current = math.sqrt(current_line_vector[0] ** 2 + current_line_vector[1] ** 2)

        # Calculate the angle in radians
        angle_radians = math.acos(dot_product / (magnitude_last * magnitude_current))

        # Convert the angle from radians to degrees
        angle_degrees = math.degrees(angle_radians)
        angles.append(angle_degrees)

    return angles, last_point, second_last_point, index_last_point

def plot_circle_and_points(points, x0, y0, z0, radius):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for idx, point in enumerate(points):
        x, y, z = point
        ax.scatter(x, y, z, color='blue', marker='o')

    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = radius * np.outer(np.cos(u), np.sin(v)) + x0
    y = radius * np.outer(np.sin(u), np.sin(v)) + y0
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + z0
    ax.plot_surface(x, y, z, color='r', alpha=0.2)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()


def distance_to_circle(x0, y0, z0, radius, x, y, z):
    return np.sqrt((x - x0) ** 2 + (y - y0) ** 2 + (z - z0) ** 2) - radius

def sum_of_distances_to_circle(params, points):
    x0, y0, z0, radius = params
    total_distance = 0
    for point in points:
        x, y, z = point
        total_distance += np.abs(distance_to_circle(x0, y0, z0, radius, x, y, z))
    return total_distance

def find_optimal_circle(points):
    initial_guess = [0, 0, 0, 1]  # Initial guess for (x0, y0, z0, radius)
    result = minimize(sum_of_distances_to_circle, initial_guess, args=(points,), method='L-BFGS-B')
    x0, y0, z0, radius = result.x
    # plot_circle_and_points(points, x0, y0, z0, radius)
    return sum_of_distances_to_circle([x0, y0, z0, radius], points) / len(points)

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

    # Plot the camera positions and orientation vectors in 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Extract camera positions and orientation vectors from each frame's transformation matrix
    pos = []
    ori = []
    for idx, frame in enumerate(data["frames"]):
        matrix = np.array(frame["transform_matrix"])
        camera_position, orientation_vector = extract_camera_position_and_orientation(matrix)
        pos.append(camera_position)
        ori.append(orientation_vector)
        camera_positions_x.append(camera_position[0])
        camera_positions_y.append(camera_position[1])
        camera_positions_z.append(camera_position[2])

    points = []
    for x, y in zip(camera_positions_x, camera_positions_y):
        points.append((x, y))
    angles, last_point, second_last_point, index_last_point = calculate_angle_between_lines(points)
    print(angles)
    # Find the index of the biggest angle
    index_of_biggest_angle = angles.index(max(angles))
    print(index_of_biggest_angle)

    # plt.plot([points[index_of_biggest_angle][0], last_point[0], second_last_point[0]], [points[index_of_biggest_angle][1], last_point[1], second_last_point[1]], 'ro-')

    ax.scatter(camera_positions_x, camera_positions_y, camera_positions_z, marker='o', s=10)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Camera Positions with Direction of View and Camera Frustums')
    plt.show()
    return index_of_biggest_angle, index_last_point

def shrinking_distances(data):

    camera_positions_x = []
    camera_positions_y = []
    camera_positions_z = []

    # Extract camera positions and orientation vectors from each frame's transformation matrix
    for frame in data["frames"]:
        matrix = np.array(frame["transform_matrix"])
        camera_position = matrix[:3, 3]
        camera_positions_x.append(camera_position[0])
        camera_positions_y.append(camera_position[1])
        camera_positions_z.append(camera_position[2])

    camera_positions = np.column_stack((camera_positions_x, camera_positions_y, camera_positions_z))
    length = len(camera_positions)
    # Calculate pairwise distances between camera positions
    dist_matrix = squareform(pdist(camera_positions))
    half_dist_matrix = dist_matrix.copy()
    for i in range(length):
        for j in range(length):
            half_dist_matrix[i,j] = float('inf') if abs(i-j)<length//2 else half_dist_matrix[i,j]

    min_index = np.argmin(half_dist_matrix)
    row_index, col_index = np.unravel_index(min_index, half_dist_matrix.shape)
    if row_index < col_index:
        # cut_positions = camera_positions[row_index:col_index]
        return row_index, col_index
    else:
        # cut_positions = camera_positions[col_index:row_index]
        return  col_index,row_index

    # return cut_positions

# Example usage:
# Assuming your JSON data is stored in a file called 'data.json'
with open('./data_example/transforms.json', 'r') as file:
    json_data = file.read()

angle_index, last_point = plot_camera_positions_with_direction(json_data)

# Remove the first 10 items from the 'frames' array
# Load JSON data
data = json.loads(json_data)

# dist_matrix = shrinking_distances(data)
start_idx,end_idx = shrinking_distances(data)

print(angle_index, last_point)
print(start_idx,end_idx)
# data['frames'] = data['frames'][angle_index:last_point]
data['frames'] = data['frames'][start_idx:end_idx]

# Write the modified JSON data back to the file
with open('./data_example/SandBox/transforms2.json', 'w') as file:
    json.dump(data, file, indent=2)
