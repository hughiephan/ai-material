# Image Caption

## Step: Import libraries
```python
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import os
import tensorflow as tf
import matplotlib.pyplot as plt
from tqdm import tqdm
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import Sequence, to_categorical
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D, Activation, Dropout, Flatten, Dense, Input, Layer, Embedding, LSTM, add, Concatenate, Reshape, concatenate, Bidirectional
from tensorflow.keras.applications import VGG16, ResNet50, DenseNet201
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from textwrap import wrap
```

Format text data and and startseq and endseq to sentence

## Step:
```python
image_path = '../input/flickr8k/Images'
data = pd.read_csv("../input/flickr8k/captions.txt")

def readImage(path,img_size=224):
    img = load_img(path,color_mode='rgb',target_size=(img_size,img_size))
    img = img_to_array(img)
    img = img/255.
    return img

def text_preprocessing(data):
    data['caption'] = data['caption'].apply(lambda x: x.lower())
    data['caption'] = data['caption'].apply(lambda x: x.replace("[^A-Za-z]",""))
    data['caption'] = data['caption'].apply(lambda x: x.replace("\s+"," "))
    data['caption'] = data['caption'].apply(lambda x: " ".join([word for word in x.split() if len(word)>1]))
    data['caption'] = "startseq "+data['caption']+" endseq"
    return data

data = text_preprocessing(data)
captions = data['caption'].tolist()
tokenizer = Tokenizer()
tokenizer.fit_on_texts(captions)
vocab_size = len(tokenizer.word_index) + 1
max_length = max(len(caption.split()) for caption in captions)
images = data['image'].unique().tolist()
nimages= len(images)
split_index = round(0.85*nimages)
train_images = images[:split_index]
val_images = images[split_index:]
train = data[data['image'].isin(train_images)]
test = data[data['image'].isin(val_images)]
train.reset_index(inplace=True,drop=True)
test.reset_index(inplace=True,drop=True)
```

data['caption']

![image](https://github.com/hughiephan/DPL/assets/16631121/c8ce2e92-6781-4417-bc8b-0cf1e0408df7)

## Step:
```python

```

## Step:
```python

```

## Step:
```python

```
