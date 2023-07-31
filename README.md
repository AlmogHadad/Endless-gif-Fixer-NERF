# Endless-gif-Fixer-NERF

instant-ngp (NERF) repo (submodule in our project): https://github.com/NVlabs/instant-ngp

## projrct steps:
1. split the git into images
2. perform COLMAP and get camera poses for each of the images
3. Process the data output of the COLMAP to the nerf network
4. train and run NERF
5. retrive the missing posses from the last frame to the first one
6. creating fixed gif

## solution ways

### perform linear interpolation - between last and first point

![image](https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/076309ff-59bf-437d-9c9e-974320f50295)
![image](https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/ad4999ad-fd0e-46d3-9a59-e86509a87f1d)
