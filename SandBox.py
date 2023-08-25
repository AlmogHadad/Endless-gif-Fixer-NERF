import numpy as np
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt



# Calculate pairwise distances between camera positions
dist_matrix = squareform(pdist(camera_positions))

# Define distance threshold for overlap
overlap_threshold = 0.5  # Adjust based on your scenario

# Find overlapping pairs
overlap_pairs = np.argwhere(dist_matrix < overlap_threshold)

# Perform k-means clustering on camera positions
num_clusters = 3  # Adjust based on your scenario
kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(camera_positions)
clusters = kmeans.labels_

# Create a 3D scatter plot to visualize camera positions
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot camera positions with different colors for clusters
for i in range(num_clusters):
    cluster_mask = clusters == i
    ax.scatter(camera_positions[cluster_mask, 0],
               camera_positions[cluster_mask, 1],
               camera_positions[cluster_mask, 2],
               label=f'Cluster {i + 1}')

# Highlight overlapping camera positions
for pair in overlap_pairs:
    ax.plot(camera_positions[pair, 0], camera_positions[pair, 1], camera_positions[pair, 2], color='red')

# Set labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Camera Positions and Overlap Detection')
ax.legend()

# Show the plot
plt.show()
