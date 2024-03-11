import cv2
import os


# Converting images in engaged dataset to grayscale
def process_images_in_place(directory, img_size=(48, 48)):
    all_files = os.listdir(directory)

    image_files = [file for file in all_files if file.lower().endswith('.jpg')]

    for image_name in image_files:
        image_path = os.path.join(directory, image_name)
        image = cv2.imread(image_path)

        # Convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Resize the image
        resized_image = cv2.resize(gray_image, img_size, interpolation=cv2.INTER_AREA)

        # Overwrite the original image with the processed image
        cv2.imwrite(image_path, resized_image)


# Paths to your 'train' and 'test' directories for the 'engaged' class
train_engaged_dir = 'train/engaged'
test_engaged_dir = 'test/engaged'

# Process the images in 'train/engaged'
process_images_in_place(train_engaged_dir)

# Process the images in 'test/engaged'
process_images_in_place(test_engaged_dir)
