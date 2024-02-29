# Transfer Learning with MobileNet and SVM 

![image](https://github.com/hughiephan/DPL/assets/16631121/7a8e7915-d77d-4b59-aef8-f6830dab245b)

Using MobileNet's convolutional base, we extract high-dimensional feature vectors from input images, capturing crucial visual information. These features learned during MobileNet's training on datasets like ImageNet, provide rich representations of the images. Then, employing SVM, a robust classification algorithm, we learn to classify these feature vectors into multiple classes accurately. This approach combines MobileNet's efficiency in feature extraction with SVM's effectiveness in classification, offering a powerful solution for image classification tasks in resource-constrained environments.

## Step 1: Import libraries
```python
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet import MobileNet, preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn import svm
```

## Step 2: Import Model
MobileNet is an efficient and portable CNN architecture. Because of the small size of the model, these models are considered very useful to be implemented on mobile and embedded devices. While a VGG16 model can take up to 500 MB of disk space, MobileNet only needs 16–18MB. This makes it ideal to be loaded on mobile devices. Having `include_top=True` means that a fully-connected layer will be added at the end of the model

```python
model = MobileNet(input_shape=(224,224,3), include_top=True)
model.summary()
```
![image](https://github.com/hughiephan/DPL/assets/16631121/69cb2019-a45f-4a36-aa85-dbaedcd01d08)

## Step 3: Define Feature Extractor
The output of `reshape_2` layer is a 1000 elements vector. MobileNet predictions layer takes this vector as input. We use this vector as our feature and try to do classification. A new model `feature_extractor` is created.

```python
output = model.get_layer("reshape_2").output
feature_extractor = tf.keras.Model(model.input, output)
```

## Step 4: Run Feature Extractor

![image](https://github.com/hughiephan/DPL/assets/16631121/d80667e4-4aa5-4ad9-90fc-4fa6db7a2e38)

Flowers Recognition dataset https://www.kaggle.com/datasets/alxmamaev/flowers-recognition will be used. In this dataset, there are 5 classes: daisy, dandelion, rose, sunflower, and tulip. Images belonging to a specific class are collected in the corresponding folder name. Next, ImageDataGenerator from Keras is created with the preprocessing function, making sure every image will be processed as the original MobileNet was trained on. We use `flow_from_directory` to specify the directory containing the image data, the target size of images (224x224 pixels), batch size (32), the classes. We will put the extracted features into X and the target label in Y. `class_mode` is set to sparse meaning that ["daisy", "dandelion", "rose", "sunflower", "tulip"] will be transformed into [0, 1, 2, 3, 4]

```python
classes = ["daisy", "dandelion", "rose", "sunflower", "tulip"]
datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
data_generator = datagen.flow_from_directory(
    "/kaggle/input/flowers-recognition/flowers",
    target_size=(224, 224),
    batch_size=32,
    classes=classes,
    class_mode='sparse'
)

X = []
y = []
for i in range(len(data_generator)):
    images, labels = data_generator[i]
    features = feature_extractor.predict(images)
    X.extend(features)
    y.extend(labels)
X = np.array(X)
y = np.array(y)
```
![image](https://github.com/hughiephan/DPL/assets/16631121/94cbceba-2e7a-4f98-a072-90f5c2008a01)

Looking at the first layer of `model.summary()` you can see it's expecting data in this format `[(None, 224, 224, 3)]` so we need to add 1 more dimension by `np.expand_dims(img_arr, axis=0)`, after that the image will transform from `(224, 224, 3)` into `(1, 224, 224, 3)`.

![image](https://github.com/hughiephan/DPL/assets/16631121/ef2c9233-602b-4c73-a57f-43c869d771cf)

## Step 5: Train Test Split
`X` and y` Lists are converted to numpy arrays. Then further split them into train and test sets using `train_test_split`.
```python
train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.2)
```
![image](https://github.com/hughiephan/DPL/assets/16631121/ae440bdc-2be2-4b9d-b992-2117ee82a170)

## Step 6: Make predictions with SVM
```python
svm_model = svm.SVC(C=1.0)
svm_model.fit(train_X, train_y)
y_pred = svm_model.predict(test_X)
print(classification_report(test_y, y_pred,target_names=classes))
```
![image](https://github.com/hughiephan/DPL/assets/16631121/adaa6b93-7a3b-428e-8167-ce224e2938e3)
