# Endless-gif-Fixer-NERF

instant-ngp (NERF) repo: https://github.com/NVlabs/instant-ngp

step:
1. split the git into images
2. perform COLMAP and get camera poses for each of the images
3. Process the data output of the COLMAP to the nerf network
4. train and run NERF
5. retrive the missing posses from the last frame to the first one
6. creating fixed gif
