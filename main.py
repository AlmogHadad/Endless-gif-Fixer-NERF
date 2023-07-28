import subprocess
import gif_handler

gif_input = "example.gif"
output_prefix = "frame"

# step 1 - from GIF input, make set of images
gif_handler.create_images_from_gif(gif_input, output_prefix)

# step 2 - from the set of images, play COLMAP
subprocess.run(['python', './COLMAP_executable.py'])

# step 3 - from COLMAP output, process the data to input it to the NERF network
subprocess.run(['python', './colmap2nerf.py'])

# step 4 - train NERF network (instant-ngp)
# - to import the instant-ngp as subprocess

# step 5 - find the missing posses
subprocess.run(['python', './find_missing_posses.py'])

# step 6 - extract missing posses from the NERF
subprocess.run(['python', './extract_posses.py'])

# step 7 - create gif from the set of images + new frames
gif_handler.create_gif_from_images(gif_input, output_prefix)
