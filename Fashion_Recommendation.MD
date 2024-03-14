# Fashion Recommendation with Xception and KD Tree Nearest Neighbors

![image](https://github.com/hughiephan/DPL/assets/16631121/ebeabf55-c495-4fb0-b793-7d27d6ecbf90)

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
Download the Fashion Recommendation dataset from: `https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/data` . A dirname contains a list of filenames (many images). We will join the dirnames and filenames together to create our dataset. Even though there are a total of 105100 images, for our tutorial we focus on the first 10000 images.

```python
dataset = []
for dirname, _, filenameList in os.walk('/kaggle/input/h-and-m-personalized-fashion-recommendations/images'):
    for filename in filenameList:
        dataset.append(os.path.join(dirname, filename))
dataset = dataset[:10000]
```

![image](https://github.com/hughiephan/DPL/assets/16631121/6fdf8065-63a8-441d-aa48-658bfd8c5f0f)

## Step 3: Add Xception model

![image](https://github.com/hughiephan/DPL/assets/16631121/625bda7a-5b44-47ad-b801-1f60f6251830)

Xception stands for “extreme inception”, it takes the principles of Inception to an extreme. XCeption architecture relies on Depthwise Separable Convolution, and Shortcuts between Convolution blocks as in ResNet. You can read more about Xception here `https://maelfabien.github.io/deeplearning/xception` . For this tutorial, we will use Xception model which was already trained on 14.000.000 images of the Imagenet dataset. We use `include_top=False` to remove the Fully-connected Layer as this Layer is not useful for our task at hand. We set all the layers to False in the Xception layer with `layer.trainable=False` to stop it from updating the weights.

```python
model = Xception(weights='imagenet', include_top=False)
for layer in model.layers:
    layer.trainable=False
```

## Step 4: Pre-process and extract features

Image files vary in size so we need to resize them all into the same width and height using `cv2.resize`. Because we are shrinking the image, we will use `INTER_AREA` interpolation but if the image needs to be enlarged, then we would use `INTER_LINEAR` or `INTER_CUBIC` interpolation. If. And Xception input must be 4-dimensional so we need to expand our image dimension with `expand_dims`. Lastly, the pre-process step uses `xception.preprocess_input` to normalize the input pixels between -1 and 1. 

![image](https://github.com/hughiephan/DPL/assets/16631121/05c87d19-8a50-4f0f-b4ae-ee2a95b40725)

```python
features=[]
for img_path in dataset:
    # Preprocess Image
    image_data = cv2.imread(img_path)
    image_data = cv2.resize(image_data, (225,225), interpolation=cv2.INTER_AREA)  
    image_data = np.expand_dims(image_data, axis=0)
    image_data = preprocess_input(image_data)
    # Feature Extraction
    extracted_feature = model.predict(image_data)
    extracted_feature = np.array(extracted_feature).flatten()
    features.append(extracted_feature)
```

## Step 5: Training with KD Tree Nearest Neighbors

KD Tree is an improvement over KNN. It is useful for representing data efficiently. Our features have the shape of `(1000, 100352)`, meaning it has 1000 images, and each image is a 100352-dimension vector. So our K = 100352, and the model will create a 100352-D Tree. Calling `fit` will start training our model with KD Train based on our list of features.

```python
nNeighbors = 4
nbrs = NearestNeighbors(n_neighbors = nNeighbors, algorithm = 'kd_tree').fit(features)
```

To easily explain how KD Tree works, let's say that our image features are just 2-D Vector [(2, 8), (7, 5), (1, 6), (6, 4), (9,6)], not the 100352-D Vector. In this illustration, our variation of the KD Tree picks the first value to compare instead of choosing a mean for simplicity, for a precise approach of KD Tree please refer to here `https://yasenh.github.io/post/kd-tree`

![image](https://github.com/hughiephan/DPL/assets/16631121/90baacad-2103-44ab-bcf4-19c820702776)

## Step 6: Predict

![image](https://github.com/hughiephan/DPL/assets/16631121/be6ffdf0-a5a6-4ec5-8716-64758c9e4378)

Given a query image, our model will predict by finding nearest neighbors as similar images. In our code `distances` is the distance to the 4 closest neighbors. And `result` is the index of that 4 neighbors.

```python
queryImagePath = dataset[999]
queryImage = cv2.imread(queryImagePath) 
queryImage = cv2.resize(queryImage, (225,225), interpolation=cv2.INTER_AREA)  
queryImage = np.expand_dims(queryImage, axis=0)
queryImage = preprocess_input(queryImage)
queryFeature = model.predict(queryImage)
distances, result = nbrs.kneighbors([queryFeature.flatten()])
```

## Step 7: Visualize predictions

Our predictions are the 4 similar images ranking by the most similarities from left to right. Note that the first image is the query image itself, as the similarity score of the query image to itself is always the highest.

```python
plt.title("Query")
plt.imshow(cv2.imread(queryImagePath))
fig = plt.figure(figsize=(12,8))
fig.suptitle('Nearest Neighbors')
for i in range(0, nNeighbors):
    index_result=result[0][i]
    plt.subplot(3, 4, i+1)
    plt.imshow(cv2.imread(dataset[index_result]))
plt.show()
```

![image](https://github.com/hughiephan/DPL/assets/16631121/112c37dd-f849-4711-a435-59e0b77ee537)

## Reference
- https://www.kaggle.com/code/hamditarek/similar-image-cnn-cosine-similarity
- https://maelfabien.github.io/deeplearning/xception/#what-does-it-look-like
- https://scikit-learn.org/stable/modules/metrics.html#cosine-similarity
- https://www.geeksforgeeks.org/search-and-insertion-in-k-dimensional-tree
- https://www.geeksforgeeks.org/introductory-guide-to-information-retrieval-using-knn-and-kdtree
- https://stackoverflow.com/questions/23853632/which-kind-of-interpolation-best-for-resizing-image
