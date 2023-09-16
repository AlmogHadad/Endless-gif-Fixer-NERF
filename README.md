# Endless-gif-Fixer-NERF
Authors:
  - Yaad
  - Almog Hadad

Given a GIF that endlessly repeats, but with detectable end and start points, the Endless-GIF-Fixer-NERF corrects the GIF by adding or removing new camera poses and smoothing the route through the construction of a 3D image using NERF networks and retrieving the necessary poses.

using instant-ngp (NERF) repo (submodule in our project): https://github.com/NVlabs/instant-ngp

## projrct steps:
1. split the git into images

2. perform COLMAP and get camera poses for each of the images

3. Process the data output of the COLMAP to the nerf network

4. train and run NERF

5. retrive the missing posses from the last frame to the first one
   - cut overlap poses (if exists)
   - perform interpolation using a fully connected neural network

6. extract the missing poses from the NERF
 
7. creating fixed gif

<div style="display: flex; justify-content: center;">
  <img src="https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/5424123a-45a1-402b-ad4d-7e61d98926d5" width="400">
  <img src="https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/0584eb48-0fed-4b0f-9c42-cfb5a9abcac6" width="400">
</div>

## solution ways - gap between the end and start point

### try 1 - perform linear interpolation - between last and first point

<img src="https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/076309ff-59bf-437d-9c9e-974320f50295" width=250>

<img src="https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/ad4999ad-fd0e-46d3-9a59-e86509a87f1d" width=250>

### try 2 - perform Polynomial interpolation
<img src="https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/076309ff-59bf-437d-9c9e-974320f50295" width=250>
<img src="https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/0747ecb3-0051-4995-83ae-56263fca4ab2" width=250>

### try 3 - interpolation with nueral network:
<img src="https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/bd3f4575-a80e-4c42-a544-1b387b48fc3f" width=250>
<img src="https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/e3bb9cc5-a83a-48d0-91a2-8cc2e7fc8864" width=250>
<img src="https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/d33a49db-097d-47be-aaea-37032b522a6c" width=250>



## solution ways - overlap video, needed to cut poses

### sulotion 1 - try 1 - widest angle of 2 last points
choosing the point that creates the most obtuse angle (less than 180 degrees) with the last two points, and deleting all the points from the beginning of the gif to it. then, rebuilding by using polynimial interpolation

<img src="https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/4b6370d5-0161-47a1-afbd-62b6b0000365" width=500><br>

<img src="https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/2ea152d9-d587-46ee-af1f-6dbe95a82b2a" width=250>
<img src="https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/68db6948-051a-40d7-b644-0016dbfa843b" width=250><br>

### sulotion 1 - try 2 - better fitted to nerf with widest angle
instead of taling the 2 last point, we find the first point that over lap and we start to cut images. the reason is that in this section, there are more images so the images that created by the network, will be in better shape.
It is important to mention that the cut is both the positions at the beginning and at the end.

<img src="https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/014c1262-e520-431e-8618-74c123f7259d" width=500><br>

<img src="https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/409b9f06-7ed9-4d73-93ef-c4c1fffb8f0f" width=250>
<img src="https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/efd3c78a-c1be-46c1-a607-622b49cfe80a" width=250>




### sulotion 2 - the smallest sum of distances
Start with the first three points and create a circle that will result in the smallest sum of distances between the points and the arc of the circle. At each step, the next point is added and the sum of the distances is updated. At the point where the sum of the distances increases, cut off the end of the video and rebuild it by polynomial interpolation.

<img src="https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/fa81e5e4-4394-4ff6-ae13-c624ed353e7d">

<img src="https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/f744ebc6-a86e-4be7-8644-96014e36cda4">

## Installation
To get started with the Endless-GIF-Fixer-NERF, follow these steps:

Clone the project repository:

`git clone https://github.com/AlmogHadad/Endless-gif-Fixer-NERF.git`

Initialize and update the submodule:

`cd Endless-gif-Fixer-NERF
git submodule init
git submodule update`

Navigate to the instant-ngp directory:

`cd instant-ngp`

Setup instant-ngp following the instructions provided in the repository at: https://github.com/NVlabs/instant-ngp#building-instant-ngp-windows--linux

Install the required Python dependencies:

`pip install -r requirements.txt`

With the installation completed, you should now have all the necessary components and dependencies ready to run the Endless-GIF-Fixer-NERF project.

## image from nerf (from train set)
### guess the fake image:
<img src="https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/89c2bc60-f62f-49be-a3ff-10afd64141c9" width=500>
<img src="https://github.com/AlmogHadad/Endless-gif-Fixer-NERF/assets/77130590/791ee1ad-3be5-464a-9406-edcc8fe1417b" width=500>

## Additional Notes
The Endless-GIF-Fixer-NERF project utilizes the instant-ngp (NERF) repository as a submodule. Make sure to check the linked repository for more details on NERF implementation.

Please follow the project steps carefully and ensure that all dependencies are correctly installed before running the solution.

## Acknowledgments
This project is inspired by the amazing work in the field of neural rendering, and it builds upon the advancements made by the instant-ngp (NERF) repository.

## License
This project is licensed under the MIT License. Feel free to use, modify, and distribute it according to the terms of the license.
