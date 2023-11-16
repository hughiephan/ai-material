# Fashion Recommendation with Xception and Nearest Neighbors

![image](https://github.com/hughiephan/DPL/assets/16631121/41645366-fed7-4162-aea8-a92ea935c4ac)

We will use Xception Feature Exaction layer, plugging in with the `sklearn.neighbors` method to find similiar images. 

## Step 1: Import libraries
```python
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from keras.applications.xception import Xception,preprocess_input
from sklearn.neighbors import NearestNeighbors
```

## Step 2: Prepare dataset
Download the Fasion Recommendation dataset from: https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/data . A dirname contains a list of filename (many images). We will join the dirnames and filenames together to create our dataset. Even though there are total of 105100 images, for our tutorial we focus on the first 10000 images.

```python
dataset = []
for dirname, _, filenameList in os.walk('/kaggle/input/h-and-m-personalized-fashion-recommendations/images'):
    for filename in filenameList:
        dataset.append(os.path.join(dirname, filename))
dataset = dataset[:10000]
```

![image](https://github.com/hughiephan/DPL/assets/16631121/6fdf8065-63a8-441d-aa48-658bfd8c5f0f)

## Step 3: Add Xception Model

![image](https://github.com/hughiephan/DPL/assets/16631121/85623bf0-3af3-40a1-8252-fab6bf7d8e5b)

Xception stands for “extreme inception”, it takes the principles of Inception to an extreme. XCeption architecture relies on Depthwise Separable Convolution, and Shortcuts between Convolution blocks as in ResNet. You can read more about Xception here: https://maelfabien.github.io/deeplearning/xception . For this tutorial, we will use Xception model which were already trained on 14.000.000 images of Imagenet dataset. We use `include_top=False` to remove the Fully-connected Layer as this Layer is not useful for our task at-hand. We set all the layers to False in Xception layer with `layer.trainable=False` to stop it from updating the weights.

```python
model = Xception(weights='imagenet',include_top=False)
for layer in model.layers:
    layer.trainable=False
```

## Step 4: Pre-process and extract features
`xception.preprocess_input` will scale input pixels between -1 and 1. 

```python
features=[]
for img_path in dataset[:999]: # Limiting the data for training
    # Preprocess Image
    image_data=cv2.imread(img_path)
    image_data=cv2.resize(image_data,(225,225),interpolation=cv2.INTER_NEAREST)  
    image_data=np.expand_dims(image_data,axis=0)
    image_data=preprocess_input(image_data)
    # Feature Extraction
    extracted_feature=model.predict(image_data)
    extracted_feature=np.array(extracted_feature).flatten()
    features.append(extracted_feature)
feature_vec = np.array(features)
```

## Step 5: Training with Nearest Neighbors
```python
nbrs = NearestNeighbors(n_neighbors=12, algorithm='ball_tree', metric="cosine").fit(feature_vec)
```

## Step 6: Predict
```python
image_data=cv2.imread((dataset[1000])) # Get the 1000th image for testing
image_data=cv2.resize(image_data,(225,225),interpolation=cv2.INTER_NEAREST)  
image_data=np.expand_dims(image_data,axis=0)
image_data=preprocess_input(image_data)
feature = model.predict(image_data)
feature = np.array(feature)
feature = feature.flatten()
distances, result = nbrs.kneighbors([feature])
```

## Step 7: Visualize predictions
```python
plt.title("Query Image")
plt.imshow(cv2.imread(dataset[1000]))
fig = plt.figure(figsize=(12,8))
fig.suptitle('Similar Images', fontsize=16)
for i in range(0,12):
    index_result=result[0][i]
    plt.subplot(3,4,i+1)
    plt.imshow(cv2.imread(dataset[index_result]))
plt.show()
```

![image](https://github.com/hughiephan/DPL/assets/16631121/db6c2f5d-71f2-4842-b28d-12ffe1dc8a62)

## Todo: 

Publish on group

## Reference
- https://www.kaggle.com/code/hamditarek/similar-image-cnn-cosine-similarity
- https://maelfabien.github.io/deeplearning/xception/#what-does-it-look-like
- https://scikit-learn.org/stable/modules/metrics.html#cosine-similarity
