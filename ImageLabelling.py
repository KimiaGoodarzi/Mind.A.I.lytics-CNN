import os
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt


# Sort files alphanumerically
def sorted_alphanumeric(data):
    import re
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


data_folder = "COMP472Data"
output_folder = "labeled_data"
label_map_gender = {1: "Male", 2: "Female", 3: "Other/Non-binary"}
label_map_age = {1: "Young", 2: "Middle-aged", 3: "Senior"}

os.makedirs(output_folder, exist_ok=True)


def label_images(folder):
    path = os.path.join(data_folder, folder)
    csv_file_path = os.path.join(output_folder, f"{folder}_labels.csv")

    # Load existing data
    if os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)
    else:
        df = pd.DataFrame(columns=['Image', 'Gender', 'Age'])

    labeled_images = set(df['Image'])

    # Sort images before labeling
    images = sorted_alphanumeric([img for img in os.listdir(path) if
                                  (img.endswith('.png') or img.endswith('.jpg')) and
                                  img not in labeled_images])

    for idx, image in enumerate(images):
        img_path = os.path.join(path, image)
        img = Image.open(img_path).resize((100, 100)).convert('L')

        plt.imshow(img, cmap='gray')
        plt.axis('off')
        plt.show()

        label = input("Gender: 1- Male / 2-Female / 3-Other/Non-binary\n"
                      "Age:  1- Young / 2- Middle-aged / 3- Senior\n"
                      "Enter labels (GenderAge, e.g., 23 for Female Senior), or type 'quit' to exit:: ")
        if label.lower() == 'quit':
            df.to_csv(csv_file_path, index=False)
            print("Progress saved. Exiting now.")
            exit(0)

        while len(label) != 2 or not label.isdigit() or int(label[0]) not in label_map_gender or int(
                label[1]) not in label_map_age:
            print(
                "Invalid input. Please enter two numbers: the first for gender (1-3),"
                " the second for age (1-3), or 'quit' to exit.")
            label = input("Enter labels (GenderAge): ")
            if label.lower() == 'quit':
                df.to_csv(csv_file_path, index=False)
                print("Progress saved. Exiting now.")
                exit(0)

        new_row = pd.DataFrame([[image, label_map_gender[int(label[0])], label_map_age[int(label[1])]]],
                               columns=['Image', 'Gender', 'Age'])
        df = pd.concat([df, new_row], ignore_index=True)

        # Save progress after every labeled image
        df.to_csv(csv_file_path, index=False)
        print("Progress saved after labeling image: " + image)

    print(f"All labels for folder {folder} saved to {csv_file_path}")


# Process each subfolder in sorted order
subfolders = sorted_alphanumeric(['engaged', 'happy', 'surprise', 'neutral'])
for folder in subfolders:
    print(f"Processing images in folder: {folder}")
    label_images(folder)

print("All images have been labeled and saved.")
