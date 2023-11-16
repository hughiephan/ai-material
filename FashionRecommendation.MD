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
output = []
for dirname, _, filenames in os.walk('/kaggle/input/h-and-m-personalized-fashion-recommendations/images'):
    for filename in filenames:
        fullpath = os.path.join(dirname, filename)
        output.append(fullpath)
output = output[:10000]
```

```python
model = Xception(weights='imagenet',include_top=False)
for layer in model.layers:
    layer.trainable=False
```

```python
features=[]
for img_path in output[:999]: # Limiting the data for training
    # Preprocess Image
    image_data=cv2.imread(img_path)
    image_data=cv2.resize(image_data,(225,225),interpolation=cv2.INTER_NEAREST)  
    image_data=np.expand_dims(image_data,axis=0)
    image_data=preprocess_input(image_data)
    # Feature Extraction
    extracted_feature=model.predict(image_data)
    extracted_feature=np.array(extracted_feature).flatten()
    features.append(extracted_feature)
```

```python
feature_vec = np.array(features)
nbrs = NearestNeighbors(n_neighbors=12, metric="cosine").fit(feature_vec)
```

```python
image_data=cv2.imread((output[1000])) # Get the 1000th image for testing
image_data=cv2.resize(image_data,(225,225),interpolation=cv2.INTER_NEAREST)  
image_data=np.expand_dims(image_data,axis=0)
image_data=preprocess_input(image_data)
feature = model.predict(image_data)
feature = np.array(feature)
feature = feature.flatten()
distances, result = nbrs.kneighbors([feature])
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
