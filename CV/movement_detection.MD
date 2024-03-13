## Step 1: Import libraries

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline 
```

##  Step 2: Read video
```python
cap = cv2.VideoCapture('../input/video-analysis/AundhBridge.mp4')
ret, fFrame  = cap.read()
ret, fFrame1 = cap.read()
ret, fFrame2 = cap.read()
img1 = fFrame1.copy()
img2 = fFrame2.copy()
```

## Step 3: Gray and Blur
```python
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
img1 = cv2.GaussianBlur(img1,(5,5),0)
img2 = cv2.GaussianBlur(img2,(5,5),0)
imgDiff = cv2.absdiff(img1, img2) 
```


## Reference
- https://www.kaggle.com/code/gauravduttakiit/pre-processing-for-video-data
