# Movement Detection with Absolute Difference

## Step 1: Import libraries

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline 
```

##  Step 2: Read video
Download dataset from `https://www.kaggle.com/datasets/gauravduttakiit/video-analysis`

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
```


## Step 4:
```python
imgDiff = cv2.absdiff(img1, img2) 
ret,imgThresh = cv2.threshold(imgDiff,30.0,255.0,cv2.THRESH_BINARY)
ht = np.size(imgThresh,0)
wd = np.size(imgThresh,1)

strucEle3x3 = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
strucEle5x5 = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
strucEle7x7 = cv2.getStructuringElement(cv2.MORPH_RECT,(7,7))        
strucEle15x15 = cv2.getStructuringElement(cv2.MORPH_RECT,(15,15))
for i in range(2):
    imgThresh = cv2.dilate(imgThresh,strucEle5x5,iterations = 2)
    imgThresh = cv2.erode(imgThresh,strucEle5x5,iterations = 1)
    imgThreshCopy = imgThresh.copy()
```

## Step 5: Contour
```python
contours, hierarchy = cv2.findContours(imgThreshCopy,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
im2 = np.zeros((ht,wd,3), np.uint8)
im2 = cv2.drawContours(im2,contours,-1,(255, 255, 255),-1)
```

## Step 6: Hull
```python
hulls = list(contours)
for i in range(len(contours)):
    hulls[i] = cv2.convexHull(contours[i])
im3 = np.zeros((ht,wd,3), np.uint8)
im3 = cv2.drawContours(im2,hulls,-1,(255, 255, 255),-1)
```

## Reference
- https://www.kaggle.com/code/gauravduttakiit/pre-processing-for-video-data
