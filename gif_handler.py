from PIL import Image
import os
from natsort import natsorted

def delete_files_in_folder(folder_path):
    try:
        # Get a list of all files in the folder
        file_list = os.listdir(folder_path)

        # Iterate over each file in the folder
        for file_name in file_list:
            # Create the file path
            file_path = os.path.join(folder_path, file_name)

            # Check if the path is a file (not a directory)
            if os.path.isfile(file_path):
                # Delete the file
                os.remove(file_path)

    except Exception as e:
        print(f"An error occurred: {e}")


def create_gif_from_images(folder_path, output_path, duration=100, loop=0):
    try:
        # Get a list of all files in the folder
        file_list = os.listdir(folder_path)

        # Filter out non-image files
        image_files = [file_name for file_name in file_list if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

        # Sort the image files alphabetically
        image_files = natsorted(image_files)

        # Create a list to hold the image frames
        frames = []

        # Iterate over each image file
        for image_file in image_files:
            # Create the image path
            image_path = os.path.join(folder_path, image_file)

            # Open the image file
            image = Image.open(image_path)

            # Convert the image to RGB mode
            image = image.convert("RGB")

            # Append the image to the frames list
            frames.append(image)

        # Save the frames as a GIF file
        frames[0].save(output_path, format='GIF', append_images=frames[1:], save_all=True, duration=duration, loop=loop)

        print("GIF created successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")


def create_images_from_gif(input_path, output_path):
    try:
        # Open the GIF file
        gif = Image.open(input_path)

        # Get the duration of each frame in milliseconds
        frame_durations = gif.info.get("duration")

        delete_files_in_folder('./frames')

        # Iterate over each frame in the GIF
        for frame_index in range(gif.n_frames):
            # Go to the current frame
            gif.seek(frame_index)

            # Convert the frame to RGB mode
            frame = gif.convert("RGB")

            # Save the frame as a separate image file
            frame.save(f"frames/{frame_index}.JPG", "JPEG")

        print("GIF split into individual frames successfully!")

        return frame_durations

    except Exception as e:
        print(f"An error occurred: {e}")
