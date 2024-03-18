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

## Step 5: Thresholding

![image](https://github.com/hughiephan/DPL/assets/16631121/5b4d32a7-01f6-4bfb-bce7-292dead3ee8c)

Compute a binary thresholded image from the input difference image. The thresholding operation converts pixel values above a certain threshold `30.0` to a maximum value `255` and the rest to zero, resulting in a binary image where pixels are either white `255` or black `0`. 

```python
_, img = cv2.threshold(imgDiff,30.0,255.0,cv2.THRESH_BINARY)
```

## Step 5: Morphological operations

In the dilation process, the value of the output pixel is the `maximum` value of all the pixels that fall within the structuring element's size and shape. For example, in a binary image, if any of the input image's pixels falling within the kernel's range is set to the value 1, the corresponding pixel of the output image will be set to 1 as well.

![image](https://github.com/hughiephan/DPL/assets/16631121/f79edc19-3296-4735-9d63-1e3e766959c6)

In the erosion process, the value of the output pixel is the `minimum` value of all the pixels that fall within the structuring element's size and shape.

![image](https://github.com/hughiephan/DPL/assets/16631121/08cb46d6-aa4f-43c3-bada-66817afd27fc)

Erosion removes white noises, but it also shrinks our objects, so we dilate them and since the noise is gone, they won’t come back, but our object area increases.

![image](https://github.com/hughiephan/DPL/assets/16631121/bdc7e70a-0bcb-466c-a3e8-a821a08e73e6)

We will create a 5x5 rectangular structuring element to define the neighborhood for morphological operations. Then, a loop iterates twice, performing dilation followed by erosion on the thresholded image using the structuring element. Dilation expands the white regions in the image, while erosion shrinks them. This sequence of dilation and erosion operations helps smooth and refine the binary image, eliminating noise and fine details while preserving the significant features. 

```python
kernel = np.ones((5, 5), dtype=np.uint8)
for i in range(2):
    img = cv2.dilate(img, kernel, iterations=2)
    img = cv2.erode(img, kernel, iterations=1)
```

![image](https://github.com/hughiephan/DPL/assets/16631121/d4ff7e74-2e73-4093-9642-ac9b14266907)

## Step 6: Contour

Detects contours in the thresholded image using the `cv2.findContours()` function, specifying parameters for contour retrieval and approximation. Finally, the contours detected are drawn onto the new image using `cv2.drawContours()`, resulting in a visualization of the contours overlaid on a black background.

```python
contours, _ = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
```

![image](https://github.com/hughiephan/DPL/assets/16631121/466476c2-c4a3-4c57-abd8-a3fe9e606494)

## Step 7: Convex hull

![image](https://github.com/hughiephan/DPL/assets/16631121/334ab918-8ad3-41ed-bb00-eecc4e75e04a)

Convex hull represents a simplified approximation of the shape formed by the contour. It is computed by identifying the outermost points of the contour and connecting them to form a convex polygon.

```python
hulls = list(contours)
for i in range(len(contours)):
    hulls[i] = cv2.convexHull(contours[i])
image = np.zeros((720,1280,3), np.uint8)
image = cv2.drawContours(image, hulls,-1,(255, 255, 255),-1)
plt.imshow(image)
print("Number of moving objects: ", len(hulls))
```

![image](https://github.com/hughiephan/DPL/assets/16631121/6d0ce0f4-094a-49d5-a674-5e65d9d66694)

## Optional command
```python
# Visualize original image
plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))

# Visualize threshold image, and after dilation and erosion
_, img = cv2.threshold(imgDiff, 30.0, 255.0, cv2.THRESH_BINARY)
plt.figure(figsize=(15, 4))
plt.subplot(1, 3, 1)
plt.title('Before')
plt.axis('off')
plt.imshow(img, cmap='gray')
strucEle5x5 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
img_dilated = cv2.dilate(img, strucEle5x5, iterations=2)
plt.subplot(1, 3, 2)
plt.title('After Dilation')
plt.axis('off')
plt.imshow(img_dilated, cmap='gray')
img_eroded = cv2.erode(img_dilated, strucEle5x5, iterations=1)
plt.subplot(1, 3, 3)
plt.imshow(img_eroded, cmap='gray')
plt.title('After Erosion')
plt.axis('off')
plt.show()

# Visualize contour
contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
image = np.zeros((720,1280,3), np.uint8)
image = cv2.drawContours(image, contours,-1,(255, 255, 255),-1)
```

## Reference
- https://www.kaggle.com/code/gauravduttakiit/pre-processing-for-video-data
- https://omes-va.com/adicion-sustraccion-de-imagenes
- https://www.tutorialspoint.com/how-to-find-and-draw-convex-hull-of-an-image-contour-in-opencv-python
- https://docs.opencv.org/4.x/dd/dd7/tutorial_morph_lines_detection.html
