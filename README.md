# Endless-gif-Fixer-NERF

instant-ngp (NERF) repo (submodule in our project): https://github.com/NVlabs/instant-ngp

## projrct steps:
1. split the git into images                                         - completed
2. perform COLMAP and get camera poses for each of the images        - completed 
3. Process the data output of the COLMAP to the nerf network         - completed
4. train and run NERF                                                - completed
5. retrive the missing posses from the last frame to the first one   - in progress (see bellow)
6. creating fixed gif                                                - completed

## solution ways - gap between the end and start point

### perform linear interpolation - between last and first point

<img src="https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/076309ff-59bf-437d-9c9e-974320f50295" width=250>

<img src="https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/ad4999ad-fd0e-46d3-9a59-e86509a87f1d" width=250>

### perforn Polynomial interpolation

<img src="https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/076309ff-59bf-437d-9c9e-974320f50295" width=250>
<img src="https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/0747ecb3-0051-4995-83ae-56263fca4ab2" width=250>

## solution ways - overlap video, needed to cut poses

### sulotion 1 - widest angle of 2 last point
choosing the point that creates the most obtuse angle (less than 180 degrees) with the last two points, and deleting all the points from the beginning of the gif to it and rebuilding by using polynimial interpolation

<img src="https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/4b6370d5-0161-47a1-afbd-62b6b0000365" width=500>


### sulotion 2 - the smallest sum of distances
Start with the first three points and create a circle that will result in the smallest sum of distances between the points and the arc of the circle. At each step, the next point is added and the sum of the distances is updated. At the point where the sum of the distances increases, cut off the end of the video and rebuild it by polynomial interpolation.

<img src="https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/fa81e5e4-4394-4ff6-ae13-c624ed353e7d">

<img src="https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/f744ebc6-a86e-4be7-8644-96014e36cda4">
