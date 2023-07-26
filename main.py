import subprocess
# import gif_handler
# import wget
import numpy as np
import os

# gif_input = "example.gif"
# output_prefix = "frame"
#
# frame_durations = gif_handler.create_images_from_gif(gif_input, output_prefix)
#
# # Example usage
# folder_path = "./frames"
# output_path = "output.gif"
# duration = frame_durations  # Duration in milliseconds per frame
# loop = 0  # 0 means loop indefinitely, any other number represents the number of loops
#
# gif_handler.create_gif_from_images(folder_path, output_path, duration, loop)
print("hi")
subprocess.run(['python', './colmap2nerf.py'])
# subprocess.run(['python', './data_preparation.py'])
# subprocess.run(['python', './find_missing_posses.py'])
