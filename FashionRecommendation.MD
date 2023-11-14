```python
import os
import cv2
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from sklearn.preprocessing import LabelBinarizer
from keras.applications.xception import Xception,preprocess_input
from keras.preprocessing import image
from keras.layers import Input
from keras.backend import reshape
from sklearn.neighbors import NearestNeighbors
```

```python
def getImagePaths(path):
    image_names = []
    for dirname, _, filenames in os.walk(path):
        for filename in filenames:
            fullpath = os.path.join(dirname, filename)
            image_names.append(fullpath)
    return image_names

features=[]
output = getImagePaths("../input/h-and-m-personalized-fashion-recommendations/images")[:10000]
model = Xception(weights='imagenet',include_top=False)
for layer in model.layers:
    layer.trainable=False
```

```python
def feature_extraction(image_data,model):
    features=model.predict(image_data)
    features=np.array(features)
    features=features.flatten()
    return features

for img_path in output[:999]: # Limiting the data for training
    # Preprocess Image
    new_image=cv2.imread(img_path)
    new_image=cv2.resize(new_image,(225,225),interpolation=cv2.INTER_NEAREST)  
    new_image=np.expand_dims(new_image,axis=0)
    new_image=preprocess_input(new_image)
    
    # Feature Extraction
    features.append(feature_extraction(new_image,model))
    
feature_vec = np.array(features)
new_feature = model.predict(preprocess_img(output[1000]))
new_feature = np.array(new_feature)
new_feature = new_feature.flatten()
nbrs = NearestNeighbors(n_neighbors=12, metric="cosine").fit(feature_vec)
distances, result = nbrs.kneighbors([new_feature])
```

```python
plt.title("Query Image")
plt.imshow(cv2.imread(output[1000]))
fig = plt.figure(figsize=(12,8))
for i in range(0,12):
    index_result=result[0][i]
    plt.subplot(3,4,i+1)
    plt.imshow(cv2.imread(output[index_result]))
plt.show()
```

## Todo: 

Publish on group

## Reference
- https://www.kaggle.com/code/hamditarek/similar-image-cnn-cosine-similarity
