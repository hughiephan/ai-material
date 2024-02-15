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

## Step 3: Pre-process image
```
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (11, 11), 0)
```

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

## Step 5: Number of coins
```
print("Number of coins detected:", len(circles[0]))
circles = np.round(circles[0, :]).astype("int")
for (x, y, r) in circles:
    cv2.circle(image, (x, y), r, (0, 255, 0), 4)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
```
