## Face Detection with Haar Cascade Application

![image](https://github.com/hughiephan/DPL/assets/16631121/b11d9e21-8cd7-4c2b-81e5-56fa00e3d7a7)

Haar features are just like our convolutional kernel. Each feature is a single value obtained by subtracting the sum of pixels under the white rectangle from the sum of pixels under the black rectangle. For example, in the right image, the first feature selected focuses on the property that the region of the eyes is often darker than the region of the nose and cheeks. The second feature selected relies on the property that the eyes are darker than the bridge of the nose. The main idea of Haar Cascade is to use Adaboost with Cascade of Classifiers but it will not be discussed in depth here. You can read more about it here `https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html`

## Prerequisites:
- Create a new account at `https://huggingface.co/join`. You can watch this tutorial on how to create a new Hugging Face account: `https://www.youtube.com/watch?v=Hgqi28ffeBY`

## Step 1: Hugging Face Space

Access `https://huggingface.co`, then click on `New` and `Space` to create an interactive ML demo for our Face Detection

![image](https://github.com/hughiephan/DPL/assets/16631121/88579fdd-21a4-4d91-8637-ab9f8e49f8cd)

## Step 2: Create space

Add your space name: `Face Detection` or any other name you like. The owner will be your Hugging Face username, and leave the License field empty. After that, we will choose Gradio as the interface for our demo. We also set the Space Hardware to the FREE CPU basic and set it to the public so it can be accessed by everyone. If you don't want any to use your application, you can also set it to private.

![image](https://github.com/hughiephan/DPL/assets/16631121/6f2c2416-623c-43a8-be9e-076781071bd2)

## Step 3: How to create files

After you click on the `Files`, it will take you to your Space codebase. You can see it is similar to Github as they are both using Git for version control of the codebase. The default files are `.gitattributes` and `README.md`. The way you can add the Haar Cascade code or any other Deep Learning model is by clicking on `Add file`, then `Create a new file`

![image](https://github.com/hughiephan/DPL/assets/16631121/2243df05-1b9e-4655-be50-a807b233e579)

## Step 4: Create app.py

Name the file `app.py` and copy the below Haar Cascade code into it. Finally, press on `Commit new file to main` to save the file. 

![image](https://github.com/hughiephan/DPL/assets/16631121/5ae9de89-5ada-4479-bbab-03bbdcd932ef)

CV2 has a built-in Haar Cascade which is ready to be used. `numpy` and `Pil` are two libraries to help us process the image. `Gradio` is used to create an interface for our demo.

```python
import numpy as np
import cv2
import gradio as gr
from PIL import Image
```

Converts the input image to a NumPy array. This conversion allows us to process the image using OpenCV functions, which typically expect image data in NumPy array format. We convert the input image in RGB format to grayscale to simplify face detection since the Haar Cascade classifier works better with grayscale images. Loads the pre-trained Haar Cascade classifier for frontal face detection with `haarcascade_frontalface_default.xml`. The `detectMultiScale` accepts  A smaller parameters like  `scaleFactor`, `minNeighbors`, and `minSize` . `scaleFactor` increases the chance of detecting smaller faces but also increases the computational time. A typical value is around 1.1, meaning the image size is reduced by 10% at each scale. `minNeighbors` specifies how many neighbors each candidate rectangle should have to retain. Higher values result in fewer detections but with higher quality. Lower values will sometimes detect multiple overlapping faces but might include more false positives. `minSize` specifies the minimum size of the detected face. After all that, the `detectMultiScale` will return a list of  `bounding boxes` representing the detected faces for (x, y, w, h) in all the faces. We need to iterate over each detected face `(0, 255, 0)` tuple specifies the color of the rectangle, and `2` specifies the thickness of the rectangle outline.

```python
def detect_faces(image):
    image_np = np.array(image)
    gray_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        cv2.rectangle(image_np, (x, y), (x+w, y+h), (0, 255, 0), 2)
    return image_np
```

Using the `gr.Interface` from the gradio library to create a web-based interface for our Haar Cascade Face Detection. Upon instantiation, the interface is configured with parameters specifying that the `detect_faces` function will process input images and produce output images. Upon launching the interface, users are presented with a web page where they can upload an image and receive the identified faces with bounding boxes outlining them. 

```python
interface = gr.Interface(
    fn=detect_faces,
    inputs="image",
    outputs="image",
    title="Face Detection with Haar Cascade",
    description="Upload an image, and the model will detect faces and draw bounding boxes around them.",
)
interface.launch()
```

## Step 5: Create requirements.txt

Create a new file and name it `requirements.txt`. As our code is using `cv2`, we need to install the `opencv-python` library.

![image](https://github.com/hughiephan/DPL/assets/16631121/c1b357f2-8099-4d70-9ea9-cd41ed457301)

Copy the below line into `requirements.txt`

```python
opencv-python
```

## Step 6: Folder structure

Make sure that our space's folder structure looks like this

![image](https://github.com/hughiephan/DPL/assets/16631121/5bb795e4-a863-4686-9ece-f17836b8797d)

## Step 7: Run demo

![image](https://github.com/hughiephan/DPL/assets/16631121/05280682-042a-4dd8-ad00-ecbc35edcd3e)

## Step 8: Get prediction

![image](https://github.com/hughiephan/DPL/assets/16631121/27618bfd-515f-4d97-a641-9797e58f79f1)

## Optional: Notebook

You can run the following code on any Notebook to test 

```python
import requests
import numpy as np
import cv2
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
url = 'https://neurohive.io/wp-content/uploads/2023/08/ai-photo-enhancing-scaled.jpeg'
response = requests.get(url)
image = np.array(Image.open(BytesIO(response.content)))
gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
plt.imshow(image)
```

## Reference
- https://becominghuman.ai/face-detection-using-opencv-with-haar-cascade-classifiers-941dbb25177
