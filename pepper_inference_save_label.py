import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

# Define the file path for the trained model in HDF5 format
model_hdf5_file_path = "/home/leo/pynaoqi/EfficientNetB0/E50/E50.hdf5"

# Load the model
model = load_model(model_hdf5_file_path)

# Define the image size used during training
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 640

# Test image folder path
image_folder ="/home/leo/pynaoqi"

# Define the mapping of class indices to class labels (replace with your class labels)
class_labels = {0: 'anger', 1: 'disgust', 2: 'happy', 3: 'neutral', 4: 'sad', 5: 'surprise'}

def scan_and_read_images(folder_path):
    image_paths = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".png"):
            image_paths.append(os.path.join(folder_path, filename))
    return image_paths

def preprocess_image(image):
    # Resize the image
    image = cv2.resize(image, (IMAGE_WIDTH, IMAGE_HEIGHT))
    image = image / 255.0  # Normalize pixel values to [0, 1]
    return image

try:
    # Scan and read PNG images inside the folder
    image_paths = scan_and_read_images(image_folder)

    for image_path in image_paths:
        # Read the image
        test_image = cv2.imread(image_path)
        
        # Check if the image is read successfully
        if test_image is None:
            raise ValueError(f"Error reading the image: {image_path}")
        
        # Preprocess the image
        preprocessed_test_image = preprocess_image(test_image)
        preprocessed_test_image = np.expand_dims(preprocessed_test_image, axis=0)  # Add a batch dimension

        # Get predictions from the model
        predictions = model.predict(preprocessed_test_image)
        predicted_class_index = np.argmax(predictions[0])
        
        # Save the predicted_class_index to a .txt file
        base_filename = os.path.splitext(os.path.basename(image_path))[0]
        txt_filename = f"{base_filename}_predicted_class.txt"
        with open(txt_filename, 'w') as txt_file:
            txt_file.write(str(predicted_class_index))

except ValueError as e:
    print(e)