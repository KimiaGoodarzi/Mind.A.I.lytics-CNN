import os
import shutil
from random import sample


def move_images(class_name, num_images=400):
    source_dir = '/Users/kimiagoodarzi/Downloads/archive (4)/test/{class_name}'
    target_dir = 'test/{class_name}'

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    all_files = os.listdir(source_dir)

    # Filter out non-image files if necessary (assuming .jpg)
    image_files = [file for file in all_files if file.lower().endswith('.jpg')]

    # Ensure there are enough images
    if len(image_files) < num_images:
        raise ValueError(f"Not enough image files in the directory for {class_name}.")

    # Randomly select a number of images
    selected_images = sample(image_files, num_images)

    # Move to the target directory
    for image in selected_images:
        shutil.move(os.path.join(source_dir, image), os.path.join(target_dir, image))

    print(f"Moved {len(selected_images)} images to {target_dir}")


# Call the function for each class
for class_name in ['neutral', 'surprise', 'happy']:
    move_images(class_name)
