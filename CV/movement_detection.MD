# Movement Detection with Absolute Difference

![image](https://github.com/hughiephan/DPL/assets/16631121/a9dedefd-9126-4d61-88b7-9e60522048f4)

## Step 1: Import libraries

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt
```

##  Step 2: Read video
Download dataset from `https://www.kaggle.com/datasets/gauravduttakiit/video-analysis` . We will read two frames from the video by using `cv2.VideoCapture`. The first value from `read` is a boolean indicating whether the frame was successfully read or not, and `img1`, which is the actual image data in the form of a NumPy array of the frame. We then read the next frame from the video capture object cap and store it in the variable `img2`. Now `img2` contains the image data of the second frame of the video.

```python
cap = cv2.VideoCapture('/kaggle/input/video-analysis/AundhBridge.mp4')
_, img1 = cap.read()
_, img2 = cap.read()
```

![image](https://github.com/hughiephan/DPL/assets/16631121/9a4eaf6e-c5d9-4bbc-86e5-fe06ef1fd357)

## Step 3: Gray and blur

Takes our two images `img1` and `img2`, and converts them from the BGR color space to grayscale. Using grayscale conversion simplifies the image to a single channel, representing the intensity of each pixel. Following the conversion, a Gaussian blur is applied to both images to reduce noise and detail in images by averaging the pixel values in a local neighborhood. In this code, a Gaussian kernel of size `(5,5)` and with a standard deviation of 0 is applied to both `img1` and `img2`.

```python
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
img1 = cv2.GaussianBlur(img1,(5,5),0)
img2 = cv2.GaussianBlur(img2,(5,5),0)
```

## Step 4: Absdiff

![image](https://github.com/hughiephan/DPL/assets/16631121/88e54921-503e-4ed0-b996-3c7501b6a76f)

Compute the absolute difference between two images `img1` and `img2`. This operation calculates the absolute pixel-wise difference between corresponding pixels in the two input images. The resulting image highlights regions where significant changes have occurred between the two input images. This can be useful in motion detection, where changes in consecutive frames of a video stream are analyzed to identify moving objects or detect changes in a scene. 

```python
imgDiff = cv2.absdiff(img1, img2) 
```

## Step 5: Dilate and erode structure

We then compute a binary thresholded image from the input difference image. The thresholding operation converts pixel values above a certain threshold `30.0` to a maximum value `255` and the rest to zero, resulting in a binary image where pixels are either white `255` or black `0`. Then, the height and width of the thresholded image are obtained. A 5x5 rectangular structuring element `strucEle5x5` is created using `cv2.getStructuringElement()` to define the neighborhood for morphological operations. Then, a loop iterates twice, performing dilation followed by erosion on the thresholded image using the structuring element. Dilation expands the white regions in the image, while erosion shrinks them. This sequence of dilation and erosion operations helps in smoothing and refining the binary image, eliminating noise and fine details while preserving the significant features

![image](https://github.com/hughiephan/DPL/assets/16631121/d4ff7e74-2e73-4093-9642-ac9b14266907)

```python
_, imgThresh = cv2.threshold(imgDiff,30.0,255.0,cv2.THRESH_BINARY)
strucEle5x5= cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
for i in range(2):
    imgThresh = cv2.dilate(imgThresh,strucEle5x5,iterations = 2)
    imgThresh = cv2.erode(imgThresh,strucEle5x5,iterations = 1)
```

## Step 6: Contour

Detects contours in the thresholded image using the `cv2.findContours()` function, specifying parameters for contour retrieval and approximation. Finally, the contours detected are drawn onto the new image using `cv2.drawContours()`, resulting in a visualization of the contours overlaid on a black background.

```python
contours, hierarchy = cv2.findContours(imgThresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
im2 = np.zeros((720,1280,3), np.uint8)
im2 = cv2.drawContours(im2,contours,-1,(255, 255, 255),-1)
```

![image](https://github.com/hughiephan/DPL/assets/16631121/466476c2-c4a3-4c57-abd8-a3fe9e606494)


## Step 7: Hull
```python
hulls = list(contours)
for i in range(len(contours)):
    hulls[i] = cv2.convexHull(contours[i])
im3 = np.zeros((720,1280,3), np.uint8)
im3 = cv2.drawContours(im2,hulls,-1,(255, 255, 255),-1)
```

![image](https://github.com/hughiephan/DPL/assets/16631121/42599119-6dcd-4c98-9370-c34a1ff7effc)

## Optional command
```python
# Visualize original image
plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))

# Visualize threshold image, and after dilation and erosion
_, imgThresh = cv2.threshold(imgDiff, 30.0, 255.0, cv2.THRESH_BINARY)
plt.figure(figsize=(15, 4))
plt.subplot(1, 3, 1)
plt.title('Before')
plt.axis('off')
plt.imshow(imgThresh, cmap='gray')
strucEle5x5 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
imgThresh_dilated = cv2.dilate(imgThresh, strucEle5x5, iterations=2)
plt.subplot(1, 3, 2)
plt.title('After Dilation')
plt.axis('off')
plt.imshow(imgThresh_dilated, cmap='gray')
imgThresh_eroded = cv2.erode(imgThresh_dilated, strucEle5x5, iterations=1)
plt.subplot(1, 3, 3)
plt.imshow(imgThresh_eroded, cmap='gray')
plt.title('After Erosion')
plt.axis('off')
plt.show()
```

## Reference
- https://www.kaggle.com/code/gauravduttakiit/pre-processing-for-video-data
- https://omes-va.com/adicion-sustraccion-de-imagenes
