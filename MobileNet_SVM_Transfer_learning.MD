```py
import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.applications.mobilenet import MobileNet
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet import preprocess_input
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.regularizers import l2
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import OneHotEncoder
from sklearn.utils import shuffle
from sklearn import svm
```

## Config
```py
classes = ["daisy", "dandelion", "rose", "sunflower", "tulip"]
path = "/kaggle/input/flowers-recognition/flowers"
```

## Import Model
```py
model = MobileNet(input_shape=(224,224,3), include_top=True)
model.summary()
```
![image](https://github.com/hughiephan/DPL/assets/16631121/69cb2019-a45f-4a36-aa85-dbaedcd01d08)

## Feature Extractor
```py
vector = model.get_layer("reshape_2").output
feature_extractor = tf.keras.Model(model.input, vector)
```

## Run Extract Feature
```py
X = []
Y = []
for f in range(5): # Flowers folder have 5 classes
    folder_path = os.path.join(path, classes[f])
    for file in os.listdir(folder_path):    
        file_path = os.path.join(folder_path, file)
        if not(file.endswith(".jpg")):
            continue
        img = image.load_img(file_path, target_size=(224,224))
        img_arr = image.img_to_array(img)
        img_arr_b = np.expand_dims(img_arr, axis=0) # add 1 more dimension
        input_img = preprocess_input(img_arr_b)
        feature_vec = feature_extractor.predict(input_img)
        X.append(feature_vec.ravel())
        Y.append(f)
```

## Make prediction with SVM
```py
train_X, test_X, train_Y, test_Y = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=42, shuffle=True)
svm_nlin = svm.SVC(C=1.0, kernel="rbf")
svm_nlin.fit(train_X, train_Y)
y_pred = svm_nlin.predict(test_X)
print(classification_report(test_Y, y_pred,target_names=classes))
```
