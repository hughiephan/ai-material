# Counting coins with Hough Transform

The circle Hough Transform is a basic feature extraction technique for detecting circles in images. The circle candidates are produced by voting in the Hough parameter space and then selecting local maxima points.

![CHT](https://github.com/hughiephan/DPL/assets/16631121/3335891a-323e-4498-8cb4-bbd423034be0)

An example with local maxima points

![image](https://github.com/hughiephan/DPL/assets/16631121/5e621a46-19ec-4238-b33b-fdd03283bc7e)

## Step 1: Import libraries

```python
import cv2
import numpy as np
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
```

## Step 2: Download image

First, we download the desired image from Imgur using the HTTP requests. The image's content is downloaded as bytes and then stored in a `BytesIO` object. Then we use `Image.open()` from the Python Imaging Library (PIL) to read the image data as numpy array.

```python
url = 'https://github.com/hughiephan/DPL/assets/16631121/77cd8149-3bce-433e-ac00-c13057a6dcec'
response = requests.get(url)
image_bytes = BytesIO(response.content)
image = np.array(Image.open(image_bytes))
```

![image](https://github.com/hughiephan/DPL/assets/16631121/77cd8149-3bce-433e-ac00-c13057a6dcec)

## Step 3: Gray and Blur
```python
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (11, 11), 0)
```

![image](https://github.com/hughiephan/DPL/assets/16631121/c05eceec-462c-4a27-98cd-58da555a6204)

## Step 4: Detect circles

`minDist` is the minimum distance between the centers of the detected circles which helps in eliminating multiple detections of the same circle. `minRadius` is the minimum radius of the circles to be detected where circles with a smaller radius than this value will not be detected. `maxRadius` is the maximum radius of the circles to be detected where circles with a larger radius than this value will not be detected.

![image](https://github.com/hughiephan/DPL/assets/16631121/d986e57d-8053-4394-bd30-1e48ebe61050)
 
`cv2.HoughCircles` already has canny edge detection implemented so we can modify its parameter `param1` to set the higher threshold to determine which edges are strong and which are weak. `param2` represents the accumulator threshold for the circle centers at the detection stage with a smaller value means that more false circles may be detected, while a larger value means that fewer circles will be detected. `dp` controls the size of the accumulator array where a smaller value will result in a larger accumulator array, which means higher resolution in the detection, but also more computational cost

![image](https://github.com/hughiephan/DPL/assets/16631121/0963d052-4992-4d64-b4cb-6b8249279b13)

```python
circles = cv2.HoughCircles(
    blurred,
    cv2.HOUGH_GRADIENT,
    minDist=50,
    minRadius=20,
    maxRadius=100,
    param1=150,
    param2=30,
    dp=1.5
)
```

![image](https://github.com/hughiephan/DPL/assets/16631121/80800481-3f6e-4a02-a2ad-8abe5271af61)

## Step 5: Number of coins
```python
print("Number of coins detected:", len(circles[0]))
circles = np.round(circles[0, :]).astype("int")
for (x, y, r) in circles:
    cv2.circle(image, (x, y), r, (0, 255, 0), 4)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
```

![image](https://github.com/hughiephan/DPL/assets/16631121/dd9ead59-5aa0-42e0-aee7-1c73ee25f890)

## Optional commands
```python
plt.imshow(image)
plt.imshow(blurred, cmap='gray')
print(circles)
edges = cv2.Canny(blurred, 50, 150)
plt.imshow(edges, cmap='gray')
```
