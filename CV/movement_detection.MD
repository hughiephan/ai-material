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
cap = cv2.VideoCapture('/kaggle/input/video-analysis/AundhBridge.mp4')
ret, img1 = cap.read()
ret, img2 = cap.read()
```

![image](https://github.com/hughiephan/DPL/assets/16631121/9a4eaf6e-c5d9-4bbc-86e5-fe06ef1fd357)

## Step 3: Gray and Blur
```python
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
img1 = cv2.GaussianBlur(img1,(5,5),0)
img2 = cv2.GaussianBlur(img2,(5,5),0)
```


## Step 4:

![image](https://github.com/hughiephan/DPL/assets/16631121/88e54921-503e-4ed0-b996-3c7501b6a76f)

```python
imgDiff = cv2.absdiff(img1, img2) 
```

## Step 5: Dilate structure
```python
ret,imgThresh = cv2.threshold(imgDiff,30.0,255.0,cv2.THRESH_BINARY)
ht = np.size(imgThresh,0)
wd = np.size(imgThresh,1)
strucEle5x5= cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
for i in range(2):
    imgThresh = cv2.dilate(imgThresh,strucEle5x5,iterations = 2)
    imgThresh = cv2.erode(imgThresh,strucEle5x5,iterations = 1)
```

## Step 6: Contour
```python
contours, hierarchy = cv2.findContours(imgThresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
im2 = np.zeros((ht,wd,3), np.uint8)
im2 = cv2.drawContours(im2,contours,-1,(255, 255, 255),-1)
```

![image](https://github.com/hughiephan/DPL/assets/16631121/466476c2-c4a3-4c57-abd8-a3fe9e606494)


## Step 7: Hull
```python
hulls = list(contours)
for i in range(len(contours)):
    hulls[i] = cv2.convexHull(contours[i])
im3 = np.zeros((ht,wd,3), np.uint8)
im3 = cv2.drawContours(im2,hulls,-1,(255, 255, 255),-1)
```

![image](https://github.com/hughiephan/DPL/assets/16631121/42599119-6dcd-4c98-9370-c34a1ff7effc)

## Optional command
```python
plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
```

## Reference
- https://www.kaggle.com/code/gauravduttakiit/pre-processing-for-video-data
