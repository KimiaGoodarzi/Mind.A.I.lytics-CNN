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

## Visualization

Data visualization plays a pivotal role in understanding the nuances of our dataset. Here's an overview of the visualization techniques we applied:

### Grayscale Image Loading
Images were loaded in grayscale into a PyTorch `ImageFolder` object. This approach converts the images into a tuple comprising a PyTorch tensor of shape `[1x48x48]`—representing pixel intensity values—and an integer indicating the class label inferred from the directory name.

### Class Distribution Plotting
We utilized the `targets` attribute from `ImageFolder`, which contains all labels, to analyze the class distribution. By extracting unique values and their counts, we could plot the distribution of classes to ensure balanced representation in our model training.

### Image Grid Visualization
Using the `image_grid()` function, we randomly selected 25 samples from the 2000 images to display a diverse range of expressions. These were plotted using `matplotlib` subplots to create an informative image grid.

### Pixel Intensity Histograms
For pixel intensity analysis, we flattened an image from a `[1x48x48]` tensor to a `[1x2304]` tensor. The pixel values were then distributed across 256 bins and visualized using the `matplotlib hist()` function to assess the distribution of pixel intensities.

### Combined Image and Histogram Grids
The `image_hist_grids()` function was developed to concurrently exhibit a 5x5 grid of images alongside their respective histograms. Although it incorporates the functionality of the aforementioned `image_grid()` and `pixel_intensity()` functions, it does not call them directly due to the complexity of returning plots within `matplotlib` subplots.

<img width="569" alt="Screenshot 2024-03-11 at 10 33 00 PM" src="https://github.com/KimiaGoodarzi/COMP472-GroupAK_14/assets/116121794/55fc26c4-2267-419e-9e02-b1b4d3319cd6">


### Observations on Pixel Intensity
The pixel intensity distribution for 'engaged' images is approximately normal, with a mild peak towards the lower intensity spectrum—consistent with the conditions under which they were captured and converted to grayscale. In contrast, the FER2013 images exhibit varied pixel intensity distributions, with some showing signs of overexposure or underexposure. This variance is attributed to the diverse sources from which these images were collected, including instances of solid backgrounds leading to sharp intensity peaks.




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

## `COMP472ClassVisualization` Script

The `COMP472ClassVisualization` script, developed in a Jupyter Notebook on Google Colab, is designed to provide insightful visualizations of our dataset. This script aids in understanding the data's distribution and characteristics, essential for the subsequent stages of model training and evaluation.

### Script Features

- **Class Distribution Plotting**: Utilizes `plot_bar` function to display a bar graph, illustrating the number of images per class within the dataset. This visualization helps identify if any class is disproportionately represented.

- **Sample Images Grid**: The `image_grid` function randomly selects 25 images and arranges them in a 5x5 grid. This grid offers a glimpse into the dataset's diversity and helps spot any noticeable anomalies or potential mislabeling within the classes.

- **Pixel Intensity Histogram**: For the randomly chosen images, the `pixel_intensity` function plots histograms to display the distribution of pixel intensities. For color images, it would overlay the intensity distributions of the Red, Green, and Blue channels.

- **Image and Histogram Grids**: The `image_hist_grids` function combines functionalities to display both a 5x5 grid of images and their corresponding pixel intensity histograms, providing a comprehensive view of the visual and statistical properties of the samples.


