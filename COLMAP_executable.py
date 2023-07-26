import subprocess
import os
# Set the path to the COLMAP BAT script
colmap_script_path = 'C:/Users/almog/Downloads/COLMAP-3.8-windows-cuda/COLMAP-3.8-windows-cuda/COLMAP.bat'

# Set the paths to the images and output directory
# Select the folder containing the images
folder_path = 'C:/Users/almog/Downloads/south-building/south-building/images' #C:/Users/almog/Documents/loop gif/frames'

# Get the list of image files in the folder
image_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.JPG')]

output_directory = 'C:/Users/almog/Documents/'

# Prepare the command-line arguments for the COLMAP script
command = f'"{colmap_script_path}" start_reconstructor --image_path "{folder_path}" --workspace_path "{output_directory}"'

# Execute the command using subprocess
subprocess.call(command, shell=True)
