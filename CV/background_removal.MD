## Step 1: Import libraries

```python
import requests
import numpy as np
import cv2
import matplotlib.pyplot as plt
from io import BytesIO
```

## Step 2: Download image
```python
url = 'https://i.imgur.com/RE1xBRe.png'
response = requests.get(url)
image_bytes = BytesIO(response.content)
image = np.array(Image.open(image_bytes))
```

![image](https://github.com/hughiephan/DPL/assets/16631121/357b2e56-8eb2-4b86-8e0c-28d811128afd)

## Step 3: 
```python
gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
smoothed_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
```
![image](https://github.com/hughiephan/DPL/assets/16631121/ae2f90cc-2f81-4d8e-8c78-2197d5a6ad4c)

## Step 4: Mask
```python
threshold_value = 50
edges = cv2.Sobel(smoothed_image, cv2.CV_64F, 1, 1, ksize=5)
_, binary_mask = cv2.threshold(np.uint8(np.absolute(edges)), threshold_value, 255, cv2.THRESH_BINARY)
```
![image](https://github.com/hughiephan/DPL/assets/16631121/9d5e5f5b-fd6f-4f3a-bd2c-8b4707e80e5d)

## Step 5: Result
```python
foreground = cv2.bitwise_and(image, image, mask=binary_mask)
```

![image](https://github.com/hughiephan/DPL/assets/16631121/a6a29d17-b3ac-40eb-8b02-3b812d3275bc)
