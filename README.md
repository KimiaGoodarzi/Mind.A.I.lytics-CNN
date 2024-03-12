# Dataset Overview for Education Mind.A.I.lytics Project

## DAiSEE: Dataset for Affective States in E-Environments

- **Source:** [DAiSEE dataset](https://people.iiith.ac.in/vineethnb/resources/daisee/index.html)
- **Reference Works:**
  - Gupta et al., "DAiSEE: Towards User Engagement Recognition in the Wild", [arXiv preprint arXiv:1609.01885](https://arxiv.org/abs/1609.01885)
  - Kamath et al., "A Crowdsourced Approach to Student Engagement Recognition in e-Learning Environments", presented at IEEE Winter Conference on Applications of Computer Vision (WACV'16).
- **Description:** DAiSEE features short video clips filmed in frontal face shots, simulating participation in a Zoom meeting. The dataset is categorized into validation, testing, and training subsets, showcasing emotions such as confusion, boredom, engagement, and frustration. For this project, we focus exclusively on the engaged/focused facial expressions, with 2,742 images utilized.

## FER-2013

- **Source:** [FER-2013 dataset by Manas Sambare](https://www.kaggle.com/datasets/msambare/fer2013)
- **Description:** The dataset includes 48x48 pixel grayscale images of faces, centered and uniform across all samples. The emotions covered are anger, disgust, fear, happiness, sadness, surprise, and neutrality. In this project, we use the data representing angry, happy, surprised, and neutral expressions.
- **Image Count by Expression:**
  - Angry: 4,953 (Train: 3,995; Test: 958)
  - Neutral: 6,198 (Train: 4,965; Test: 1,233)
  - Happy: 8,989 (Train: 7,215; Test: 1,774)
  - Surprise: 4,002 (Train: 3,171; Test: 831)

## Justification for Dataset Choices

The DAiSEE dataset was chosen for its unique inclusion of the engaged/focused expression, presenting two main challenges:
- The initial download size was 15 GB, posing storage concerns.
- We needed to extract frames representing engagement from the videos, necessitating script automation in Google Colab to handle data extraction and organization.

The FER-2013 dataset complements DAiSEE with a broad range of expressions, containing most of the images required for the project's scope. The existing image uniformity of 48x48 pixels in FER-2013 greatly benefitted the project, as convolutional neural networks thrive on fixed-size inputs, enhancing efficiency.

## Incorporating the Engaged Class

Challenges included inconsistent centering and alignment from the extracted video frames, which were essential for the model's performance. We addressed these issues using the `shape_predictor_68_face_landmarks.dat` model from the dlib library to detect facial landmarks and align the features across all images.

## Resizing and Grayscaling for Dataset Uniformity

To ensure consistency, the 'engaged' class images were converted to grayscale to match the single-channel format of the other classes. This uniformity across the dataset enables bias-free class treatment and computational efficiency. The images were also resized to the standard 48x48 pixels, in line with the FER-2013 dataset.

## Labeling

The 'engaged' class benefited from the videos being pre-labeled, streamlining the categorization of extracted frames into the dataset. This clear labeling facilitated the representation of a wide engagement spectrum.

## Visual Illustration of Preprocessing Impact

Below are before-and-after images demonstrating the preprocessing impact on the 'engaged' class images.

<img width="637" alt="Screenshot 2024-03-11 at 9 06 04 PM" src="https://github.com/KimiaGoodarzi/COMP472-GroupAK_14/assets/116121794/2f66e375-7bf8-4161-ae4d-6f4ebde686dd">

These examples validate the preprocessing techniques' effectiveness in achieving dataset uniformity.

## `PickImages.py` Script

The `PickImages.py` script automates the process of selecting and organizing images for the 'engaged' class from a consolidated directory of extracted frames.

### Script Functions

- **Image Selection**: Randomly selects 400 `.jpg` image files from the source directory to ensure a diverse and unbiased subset of images for the training model.

- **Directory Management**: Checks if the target directory (`train/engaged`) exists and creates it if necessary, providing a designated storage location for the selected images.

- **Image Transfer**: Moves the selected images from the source directory to the target training directory, organizing the dataset for model training.





## `MoveImagesFER+.py` Script

The `MoveImagesFER+.py` script streamlines the task of transferring a specific number of images from the FER+ dataset for each specified class to the designated test directory, aligning with the structure of our project's datasets.

### Script Functions

- **Customizable Image Transfer**: Allows for specifying the number of images to transfer per class, with a default set to 400 images.

- **Directory Management**: Verifies the existence of the target directory (`test/{class_name}`), creating it if it does not exist, ensuring proper organization of images by class.

- **Image Selection and Movement**: Randomly selects the specified number of `.jpg` images from the source directory and moves them to the target directory, automating the organization process for model evaluation.

## `FaceDetection.py` Script

The `FaceDetection.py` script leverages the dlib library's facial detection capabilities to center and align faces within the 'engaged' class images and resize them to a 48x48 pixel format.

### Script Functions

- **Face Detection**: Utilizes dlib's detector to identify faces in grayscale images.

- **Landmark Detection**: Employs the shape predictor to pinpoint facial landmarks.

- **Face Alignment**: Adjusts the face orientation based on eye and nose landmarks through a similarity transformation.

- **Image Processing**: Processes each image in the given directory, aligning the face and resizing it to the required dimensions.
