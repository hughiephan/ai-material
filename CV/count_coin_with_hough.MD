# Coins counting with Hough 

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
url = 'https://i.imgur.com/KkctjzS.jpeg'
response = requests.get(url)
image_bytes = BytesIO(response.content)
image = np.array(Image.open(image_bytes))
```

![image](https://github.com/hughiephan/DPL/assets/16631121/77cd8149-3bce-433e-ac00-c13057a6dcec)

## Step 3: Pre-process image
```
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (11, 11), 0)
```

![image](https://github.com/hughiephan/DPL/assets/16631121/c05eceec-462c-4a27-98cd-58da555a6204)

## Step 4: Detect circles
```python
circles = cv2.HoughCircles(
    blurred,
    cv2.HOUGH_GRADIENT,
    dp=1.5,
    minDist=50,
    param1=200,
    param2=30,
    minRadius=20,
    maxRadius=100
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

![image](https://github.com/hughiephan/DPL/assets/16631121/8a8f2add-f0a5-43e2-86c5-18c650691697)

## Optional commands
```python
plt.imshow(image)
plt.imshow(blurred, cmap='gray')
print(circles)
