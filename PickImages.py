
import os
import shutil
from random import sample


source_dir = '/Users/kimiagoodarzi/Downloads/Consolidated_Extracted_Images 2'
target_dir = 'train/engaged'


if not os.path.exists(target_dir):
    os.makedirs(target_dir)


all_files = os.listdir(source_dir)

image_files = [file for file in all_files if file.lower().endswith('.jpg')]


if len(image_files) < 400:
    raise ValueError("Not enough image files in the source.")


selected_images = sample(image_files, 400)


for image in selected_images:
    shutil.move(os.path.join(source_dir, image), os.path.join(target_dir, image))

print(f"Moved {len(selected_images)} images to {target_dir}")
