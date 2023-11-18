# Vietnamese Celeb Classification using Roboflow for Image Preprocessing and Augmentation

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
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from roboflow import Roboflow
rf = Roboflow(api_key="ADD_YOUR_API_KEY")
project = rf.workspace("ADD_YOUR_WORKSPACE").project("ADD_YOUR_PROJECT")
dataset = project.version("ADD_PROJECT_VERSION").download("folder")
```

## Step 7: Set variables

The number `3` in Input Shape means we are handling colored images. If you want to set it to a Gray image, you can use `1`.

```python
image_size = (128, 128)
input_shape = (128, 128, 3)
batch_size = 32
num_classes = 10 
```

## Step 8: Load the Dataset

With `label_mode = 'int'`, our label will be encoded as integer numbers: 0,1,2...9 but `categorical` means that the labels are encoded as categorical vectors, for example: 000, 001, 010,...111

![image](https://github.com/hughiephan/DPL/assets/16631121/5c8bbc57-f8be-4de2-95b1-3936d590e359)

```python
train_data = tf.keras.preprocessing.image_dataset_from_directory(
    '/kaggle/working/ADD_YOUR_PROJECT_AND_PROJECT_VERSION/train',
    image_size=image_size,
    batch_size=batch_size,
    label_mode='categorical',
)

val_data = tf.keras.preprocessing.image_dataset_from_directory(
    '/kaggle/working/ADD_YOUR_PROJECT_AND_PROJECT_VERSION/valid',
    image_size=image_size,
    batch_size=batch_size,
    label_mode='categorical',
)

test_data = tf.keras.preprocessing.image_dataset_from_directory(
    '/kaggle/working/ADD_YOUR_PROJECT_AND_PROJECT_VERSION/test',
    image_size=image_size,
    batch_size=batch_size,
    label_mode='categorical',
)
```

## Step 9: Train our custom CNN model

![image](https://github.com/hughiephan/DPL/assets/16631121/1a4a894f-29f2-41c0-b313-b5eafa1dcc19)

```python
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
model.add(tf.keras.layers.MaxPooling2D((2, 2)))
model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
model.add(tf.keras.layers.MaxPooling2D((2, 2)))
model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dense(num_classes, activation='softmax'))
```

## Step 10: Training

```python
model.fit(train_data, epochs=10, validation_data=val_data)
```

## Step 11: Try a new version of the dataset with different Pre-processing and Augmentation 

You should test each pre-processing and augmentation method on this dataset to see what works best. Identifying the correct steps that can increase the model performance requires a firm understanding of the problem, data collected, and production environment. What may work well in one situation is not appropriate in others. Then update your Notebook with the new version and train everything again to see if the new set of pre-processing and augmentation methods increases the accuracy or not.

![image](https://github.com/hughiephan/DPL/assets/16631121/6361218b-f8e0-4917-aeea-7ca716b982a1)

![image](https://github.com/hughiephan/DPL/assets/16631121/0e2ebbf3-429c-485f-ae14-e0b2d913485e)

![image](https://github.com/hughiephan/DPL/assets/16631121/29deb0fa-201f-4992-83f6-b0f0ebdfbdb2)

## Step 12: Evaluate with Test Set
```python
loss, accuracy = model.evaluate(test_data)
print("Test Loss:", loss)
print("Test Accuracy:", accuracy)
```

![image](https://github.com/hughiephan/DPL/assets/16631121/82577557-b27f-47dc-9fc2-a031dfd70f51)

## Step 13: Make a prediction
```python
test_images, test_classes = next(iter(test_data))
random_index = np.random.randint(0, len(test_images))
random_image = test_images[random_index]
plt.imshow(random_image.numpy().astype("uint8"))
input_image = np.expand_dims(random_image, axis=0)
predictions = model.predict(input_image)
predicted_class_index = np.argmax(predictions[0])
predicted_class = test_data.class_names[predicted_class_index]
print("Predicted Class:", predicted_class)
```

![image](https://github.com/hughiephan/DPL/assets/16631121/a0b30a0c-4a59-42e3-81f1-65e6441f34d2)

## References
- https://blog.roboflow.com/why-preprocess-augment/
