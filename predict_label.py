import os
import numpy as np
import urllib.request
import pickle
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image


def load_model():
    """
    Loads the pre-trained MobileNetV2 model from TensorFlow Hub.

    Returns:
    classifier: A TensorFlow Keras sequential model.
    """
    classifier_url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/4"
    IMAGE_SHAPE = (224, 224)
    classifier = tf.keras.Sequential([
        hub.KerasLayer(classifier_url, input_shape=IMAGE_SHAPE + (3,))
    ])
    return classifier


def preprocess_image(image_path):
    """
    Preprocesses an image from the given path for feeding to the model.

    Args:
    image_path: A string representing the path to the image file.

    Returns:
    A numpy array representing the preprocessed image.
    """
    image = Image.open(image_path)
    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    return np.expand_dims(image, axis=0)


def predict_label(image_path, classifier):
    """
    Predicts the label of an image using the given model.

    Args:
    image_path: A string representing the path to the image file.
    classifier: A TensorFlow Keras sequential model.

    Returns:
    predicted_label: A string representing the predicted label of the image.
    """
    image_data = preprocess_image(image_path)
    predictions = classifier.predict(image_data)

    labels_url = "https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt"
    with urllib.request.urlopen(labels_url) as response:
        labels = np.array(response.read().decode('utf-8').splitlines())

    predicted_label = labels[np.argmax(predictions)]
    return predicted_label.lower()


def generate_dict(dataset_folder):
    """
    Generates a dictionary of labels and image paths for a given dataset folder.

    Args:
    dataset_folder: A string representing the path to the folder containing the dataset.

    Returns:
    None.
    """
    label_dict = {}

    classifier = load_model()
    for filename in os.listdir(dataset_folder):
        if filename.endswith(".jpg"):
            image_path = os.path.join(dataset_folder, filename)
            predicted_label = predict_label(image_path, classifier)

            # create a dictionary of label and lists of image paths
            if predicted_label in label_dict:
                label_dict[predicted_label].append(image_path)
            else:
                label_dict[predicted_label] = [image_path]

    # Dump the dictionary to a binary pickle file
    with open("label.pickle", "wb") as f:
        pickle.dump(label_dict, f)


if __name__ == "__main__":
    dataset_folder = "static/album"
    generate_dict(dataset_folder)
