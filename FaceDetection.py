import dlib
from skimage import transform as trans
import numpy as np
import cv2
import os

# to center and align faces in engaged dataset, and resize them to 48x48 pixels

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(
    '/Users/kimiagoodarzi/Downloads/shape_predictor_68_face_landmarks.dat')  # You need to download this model

# resize
output_size = (48, 48)
reference = np.array([
    (30.2946 / 96 * output_size[0], 51.6963 / 112 * output_size[1]),
    (65.5318 / 96 * output_size[0], 51.5014 / 112 * output_size[1]),
    (48.0252 / 96 * output_size[0], 71.7366 / 112 * output_size[1]),
], dtype=np.float32)


def align_face(img, landmarks):
    tform = trans.SimilarityTransform()
    tform.estimate(landmarks, reference)
    M = tform.params[0:2, :]
    warped = cv2.warpAffine(img, M, (output_size[0], output_size[1]), borderMode=cv2.BORDER_REPLICATE)
    return warped


def process_images(directory):
    for img_name in os.listdir(directory):
        if not img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        img_path = os.path.join(directory, img_name)
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = detector(gray, 1)
        for face in faces:
            landmarks = np.array([[p.x, p.y] for p in predictor(gray, face).parts()])

            eye_nose_landmarks = landmarks[[36, 45, 30]]

            aligned_face = align_face(gray, eye_nose_landmarks)

            cv2.imwrite(img_path, aligned_face)


process_images('train/engaged')
process_images('test/engaged')
