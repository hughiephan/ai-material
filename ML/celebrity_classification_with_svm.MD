# Celebrity Classification with Roboflow and SVM

## Prerequisites
- Register a free account at https://app.roboflow.com/
- Download Dataset from https://www.kaggle.com/datasets/thala321/famous-vietnamese-celeb-mini

## Step 1: Create a new Project

Our task is Face Detection (one face at a time), which is the equivalent of Single-Label Classification. If there are many people in one image, we need to use the Multi-Label Classification.

![image](https://github.com/hughiephan/DPL/assets/16631121/307eb057-1af4-429c-be8d-52e52b9cdcc0)

![image](https://github.com/hughiephan/DPL/assets/16631121/9435c558-3e58-414e-bfe5-e71f0226fa4b)

## Step 2: Upload Dataset to Roboflow

First, we download the Celebrity Dataset from https://www.kaggle.com/datasets/thala321/famous-vietnamese-celeb-mini . Then there will be an option in Roboflow, prompting you to upload your dataset, so we just need to point it to our downloaded Dataset (remember to unzip it).

![image](https://github.com/hughiephan/DPL/assets/16631121/6e3ff2b0-f070-40ba-8055-b3da360e0a25)

![image](https://github.com/hughiephan/DPL/assets/16631121/aed2565d-f16e-4e8c-ba73-93eb7cebe37e)

Our dataset is quite small, so 70-20-10 should be a good enough split. But you can try out different split ratios and see how your model performs.

![image](https://github.com/hughiephan/DPL/assets/16631121/7bc25a67-2a36-4422-8ecf-22819c1d2f38)

## Step 3: Generate a new version of the Dataset

Image augmentation manipulations are forms of image preprocessing, but there is a critical difference: while image preprocessing steps are applied to training and test sets, image augmentation is only applied to the training data. By augmenting your images, you can increase the sample size of your training data and add in new cases that might be hard to find in the real-world. This is particularly important when collected datasets may be small

![image](https://github.com/hughiephan/DPL/assets/16631121/b73d1127-b7f0-4f22-a0ee-85ed46f7f0ba)

## Step 4: Export the Dataset

![image](https://github.com/hughiephan/DPL/assets/16631121/e1c7e138-edd7-458a-a956-7ed621445bbe)

![image](https://github.com/hughiephan/DPL/assets/16631121/36d69c15-9c9f-4644-ab95-cb4336daa0b7)

## Step 5: Copy the API Download code

![image](https://github.com/hughiephan/DPL/assets/16631121/0eaef9df-3095-4e69-a1b1-000df6daec75)

## Step 6: Import library and API Download code

Create a new Notebook (Kaggle, Jupyter, or Google Colab), and import the library with the API Download code

```python
!pip install roboflow
import numpy as np
import matplotlib.pyplot as plt
import cv2
import numpy as np
import os
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from roboflow import Roboflow
rf = Roboflow(api_key="ADD_YOUR_API_KEY")
project = rf.workspace("ADD_YOUR_WORKSPACE").project("ADD_YOUR_PROJECT")
dataset = project.version("ADD_PROJECT_VERSION").download("folder")
```

## Step 7: Load the Dataset

With `label_mode = 'int'`, our label will be encoded as integer numbers: 0,1,2...9 but `categorical` means that the labels are encoded as categorical vectors, for example: 000, 001, 010,...111

![image](https://github.com/hughiephan/DPL/assets/16631121/5c8bbc57-f8be-4de2-95b1-3936d590e359)

```python
def load_dataset(directory):
    images = []
    labels = []
    classes = os.listdir(directory)
    for idx, label in enumerate(classes):
        label_dir = os.path.join(directory, label)
        for image_name in os.listdir(label_dir):
            image_path = os.path.join(label_dir, image_name)
            img = cv2.imread(image_path)
            img = cv2.resize(img, (128, 128))  # Resize images to the desired shape
            images.append(img)
            labels.append(label)
    images = np.array(images)
    labels = np.array(labels)
    return images, labels

# Load and preprocess train, validation, and test datasets
train_images, train_labels = load_dataset(train_dir)
valid_images, valid_labels = load_dataset(valid_dir)
test_images, test_labels = load_dataset(test_dir)

# Flatten images and convert labels to numeric values
train_images = np.array([image.flatten() for image in train_images])
valid_images = np.array([image.flatten() for image in valid_images])
test_images = np.array([image.flatten() for image in test_images])

# Encode labels to numeric values
label_encoder = LabelEncoder()
train_labels = label_encoder.fit_transform(train_labels)
valid_labels = label_encoder.transform(valid_labels)
test_labels = label_encoder.transform(test_labels)
```

## Step 8: Train our SVC Model

```python
svm = SVC(kernel='linear')
svm.fit(train_images, train_labels)
```

## Step 9: Evaluate on Validation Set
```python
valid_predictions = svm.predict(valid_images)
accuracy = accuracy_score(valid_labels, valid_predictions)
print(f"Validation accuracy: {accuracy}")
```

## Step 10: Evaluate on Test Set
```python
test_predictions = svm.predict(test_images)
test_accuracy = accuracy_score(test_labels, test_predictions)
print(f"Test accuracy: {test_accuracy}")
```

## Step 11: Try a new version of the dataset with different Pre-processing and Augmentation 

You should test each pre-processing and augmentation method on this dataset to see what works best. Identifying the correct steps that can increase the model performance requires a firm understanding of the problem, data collected, and production environment. What may work well in one situation is not appropriate in others.

![image](https://github.com/hughiephan/DPL/assets/16631121/6361218b-f8e0-4917-aeea-7ca716b982a1)

 Then update your Notebook with the new version and train everything again to see if the new set of pre-processing and augmentation methods increases the accuracy or not.

![image](https://github.com/hughiephan/DPL/assets/16631121/0e2ebbf3-429c-485f-ae14-e0b2d913485e)

## Step 12: Make a prediction

```python
def load_random_image(directory):
    classes = os.listdir(directory)
    label = np.random.choice(classes)
    label_dir = os.path.join(directory, label)
    image_name = np.random.choice(os.listdir(label_dir))
    image_path = os.path.join(label_dir, image_name)
    img = cv2.imread(image_path)
    img = cv2.resize(img, (128, 128))  # Resize image to the desired shape
    return img, label

# Load a random image from the test set
random_image, actual_label = load_random_image(test_dir)

# Preprocess the random image for prediction
random_image_processed = np.array([random_image.flatten()])

# Make a prediction using the trained SVM model
predicted_label = svm.predict(random_image_processed)[0]

# Print information about the prediction
print(f"Actual Label: {actual_label}")
print(f"Predicted Label: {label_encoder.inverse_transform([predicted_label])[0]}")
```

![image](https://github.com/hughiephan/DPL/assets/16631121/3909593e-03ce-4b7f-b54b-ec774af1dd25)

## References
- https://blog.roboflow.com/why-preprocess-augment
