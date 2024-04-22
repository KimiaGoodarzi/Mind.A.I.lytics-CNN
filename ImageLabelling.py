import os
import csv
from PIL import Image


# Sort files alphanumerically
def sorted_alphanumeric(data):
    import re
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


# Label mapping dictionaries
gender_map = {
    "1": "Male",
    "2": "Female",
    "3": "Other/Non-binary"
}

age_map = {
    "1": "Young",
    "2": "Middle-aged",
    "3": "Senior"
}


# Get input for labeling
def get_label():
    gender = input("Enter gender label (1 for Male, 2 for Female, 3 for Other/Non-binary): ")
    age = input("Enter age label (1 for Young, 2 for Middle-aged, 3 for Senior): ")
    return gender_map[gender], age_map[age]


# Save labels to CSV
def save_labels_to_csv(labels, filename):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(labels)


# Read labeled images from CSV to avoid relabeling
def get_labeled_images(filename):
    if os.path.exists(filename):
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            labeled_images = {rows[0] for rows in reader}
            return labeled_images
    return set()


# Process images in a folder
def process_folder(folder_path, emotion, output_folder):
    image_files = os.listdir(folder_path)
    image_files = sorted_alphanumeric(image_files)
    labels_file = os.path.join(output_folder, f"{emotion}_labels.csv")

    labeled_images = get_labeled_images(labels_file)

    if not os.path.exists(labels_file):
        with open(labels_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Image", "Gender", "Age"])

    for image_file in image_files:
        if image_file in labeled_images:
            continue  # Skip labeled images
        image_path = os.path.join(folder_path, image_file)
        img = Image.open(image_path)
        img = img.resize((100, 100))
        img.show()
        gender, age = get_label()
        labels = [image_file, gender, age]
        save_labels_to_csv(labels, labels_file)
        print(f"Labeled: {image_file}, Gender: {gender}, Age: {age}")


def main():
    data_folder = "COMP472Data"
    output_folder = "labelled_images"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    emotions = ["engaged", "happy", "surprise", "neutral"]
    emotions = sorted_alphanumeric(emotions)

    for emotion in emotions:
        folder_path = os.path.join(data_folder, emotion)
        print(f"Processing folder: {emotion}")
        process_folder(folder_path, emotion, output_folder)


if __name__ == "__main__":
    main()
