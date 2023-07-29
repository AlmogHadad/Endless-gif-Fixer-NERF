import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Define the 3D points
data = []
# Open the text file
with open('D:\GitHub\Reposetories\Endless-gif-Fixer-NERF\data_example\colmap_text\points3D.txt', 'r') as file:
    # Initialize an empty list to store the rows of data


    # Read each line in the file
    for line in file:
        # Split the line into individual elements using whitespace as the delimiter
        row = line.split()

        # Convert each element from string to integer and add it to the data list
        data.append([s for s in row])


XYZ = []
for i,row in enumerate(data[3:]):
    temp=[]
    if i==500:
        break
    for point in row[4:7]:
        temp.append(point)
    XYZ.append((temp[0], temp[1], temp[2]))
# Create a 3D figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Extract x, y, and z coordinates for each point
x_coords = [p[0] for p in XYZ]
y_coords = [p[1] for p in XYZ]
z_coords = [p[2] for p in XYZ]

# Convert the data to NumPy arrays with float data type
x_coords = np.array(x_coords, dtype=float)
y_coords = np.array(y_coords, dtype=float)
z_coords = np.array(z_coords, dtype=float)

# Plot the points as a scatter plot
ax.scatter(x_coords, y_coords, z_coords, color='red', marker='o', s=10)

# Set axis labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Show the plot
plt.show()
