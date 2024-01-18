# Lab: Image Processing in Deep Learning

Train a CNN-based or Transformer-based model for a Computer Vision task

## Requirements

- `Requirement 1`: Choose ONE CNN model a custom CNN (Convolutional Layer, Fully-connected Layer), LeNet-5 (1998), AlexNet (2012), R-CNN (2013), GoogLeNet / Inception (2014), VGGNet (2014), ResNet (2015), U-NET (2015), SSD (2015), DenseNet (2016), Xception (2016), YOLO (2016), MobileNet (2017), EfficientNet (2019),... or any Vision-transformer based model.
- `Requirement 2`: Choose ONE Computer Vision task Image Classification, Object Detection, Semantic Segmentation, Instance Segmentation,...
- `Requirement 3`: Choose ONE Dataset of your choice: ImageNet, COCO, CIFAR-10 and CIFAR-100, PASCAL VOC, Open Images...
- `Requirement 4`: Given an input image, make a prediction using your Deep Learning model

## Example
Yolo V8 can detect upto 80 classes (person, bike,...) but it cannot detect fire. So I choose: CNN Network `YOLO`, Computer Vision Task `Object Detection`, Dataset `Fire and Smoke Dataset` from https://www.v7labs.com/open-datasets/fire-and-smoke-dataset

## Scoring Criteria
You will be graded based on Originality of your implementation: Did you implement anything new in the model or just re-use it? How much work did you put into implementing your model? Result of your implementation: Accuracy, Loss, Cross-validation Q/A to test your understanding: How well do you understand your code? How well do you understand Neural Network concepts? 

## Note
DO NOT add comments in your code. You can use any deep learning technique: Transfer learning, Pre-train, Finetune, Ensemble learning, Hyperparameter tuning, Pre-process image, Data augmentation, Build from scratch...

## Example Submission
```python
import warnings
warnings.filterwarnings('ignore')
import numpy as np 
import pandas as pd 
import tensorflow as tf
from keras.applications.vgg16 import VGG16
from sklearn.model_selection import train_test_split
from keras.models import Model
from keras.applications.vgg16 import VGG16
from keras.utils import load_img
from keras.layers import Dense, Dropout, Input, Flatten
from keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_dir='/kaggle/input/siim-isic-melanoma-classification/jpeg/train/'
test_dir='/kaggle/input/siim-isic-melanoma-classification/jpeg/test/'
train=pd.read_csv('/kaggle/input/siim-isic-melanoma-classification/train.csv')
test=pd.read_csv('/kaggle/input/siim-isic-melanoma-classification/test.csv')
labels=[]
data=[]
test_data=[]

df_0=train[train['target']==0].sample(2000)
df_1=train[train['target']==1]
train=pd.concat([df_0,df_1])
train=train.reset_index()
for i in range(train.shape[0]):
    data.append(train_dir + train['image_name'].iloc[i]+'.jpg')
    labels.append(train['target'].iloc[i])
df=pd.DataFrame(data)
df.columns=['images']
df['target']=labels
for i in range(test.shape[0]):
    test_data.append(test_dir + test['image_name'].iloc[i]+'.jpg')
df_test=pd.DataFrame(test_data)
df_test.columns=['images']
X_train, X_val, y_train, y_val = train_test_split(df['images'],df['target'], test_size=0.2, random_state=42)
train=pd.DataFrame(X_train)
train.columns=['images']
train['target']=y_train
validation=pd.DataFrame(X_val)
validation.columns=['images']
validation['target']=y_val
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True
)
val_datagen=ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_dataframe(
    train,
    x_col='images',
    y_col='target',
    target_size=(224, 224),
    batch_size=8,
    shuffle=True,
    class_mode='raw'
)
validation_generator = val_datagen.flow_from_dataframe(
    validation,
    x_col='images',
    y_col='target',
    target_size=(224, 224),
    shuffle=False,
    batch_size=8,
    class_mode='raw'
)

model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
x=Flatten()(model.output)
output=Dense(1,activation='sigmoid')(x) 
model=Model(model.input,output)
opt = Adam(learning_rate=1e-5)
model.compile(loss="binary_focal_crossentropy", metrics=[tf.keras.metrics.AUC()],optimizer=opt)
nb_epochs = 1
batch_size=8
nb_train_steps = train.shape[0]//batch_size
nb_val_steps = validation.shape[0]//batch_size
model.fit(
    train_generator,
    steps_per_epoch=nb_train_steps,
    epochs=nb_epochs,
    validation_data=validation_generator,
    validation_steps=nb_val_steps)
```
