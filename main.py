import subprocess
import gif_handler

gif_input = "example.gif"
output_prefix = "frame"

# step 1 - from GIF input, make set of images
gif_handler.create_images_from_gif(gif_input, output_prefix)

# step 2 - from the set of images, run COLMAP and process the data to input it to the NERF network
subprocess.run(['python', './scripts/colmap2nerf.py --colmap_matcher exhaustive --run_colmap --aabb_scale 32'])

# step 4 - train NERF network (instant-ngp)
subprocess.run(['python', './scripts/run.py /outputs'])

# step 5 - find the missing posses
subprocess.run(['python', './cut_overlap_poses.py'])
subprocess.run(['python', './find_missing_posses.py'])

# step 6 - extract missing posses from the NERF
subprocess.run(['python', './extract_posses.py'])

# step 7 - create gif from the set of images + new frames
gif_handler.create_gif_from_images(gif_input, output_prefix)
