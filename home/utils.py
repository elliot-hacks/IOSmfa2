# utils.py

import cv2
import numpy as np
from skimage.feature import blob_dog, blob_log, blob_doh

def extract_features(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    features = blob_dog(image, max_sigma=30, threshold=.1)
    return features
