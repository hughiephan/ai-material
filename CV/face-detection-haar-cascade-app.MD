## Face Detection with Haar Cascade Application

![image](https://github.com/hughiephan/DPL/assets/16631121/b11d9e21-8cd7-4c2b-81e5-56fa00e3d7a7)

Haar features are just like our convolutional kernel. Each feature is a single value obtained by subtracting the sum of pixels under the white rectangle from the sum of pixels under the black rectangle. The first feature selected focuses on the property that the region of the eyes is often darker than the region of the nose and cheeks. The second feature selected relies on the property that the eyes are darker than the bridge of the nose. The main idea of Haar Cascade is to use Adaboost with Cascade of Classifiers but it will not be discussed in depth here. You can read more about it here https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html

## Step 1: Hugging Face Space

Access https://huggingface.co , then click on `New` and `Space` to create an interactive ML demo for our Face Detection

![image](https://github.com/hughiephan/DPL/assets/16631121/88579fdd-21a4-4d91-8637-ab9f8e49f8cd)

## Step 2: Create space

Add your space name: `Face Detection` or any other name you like. The owner will be your Hugging Face username, and leave the License field empty. After that, we will choose Gradio as the interface for our demo. We also set the Space Hardware to the FREE CPU basic and set it to the public so it can be accessed by everyone. If you don't want any to use your application, you can also set it to private.

![image](https://github.com/hughiephan/DPL/assets/16631121/6f2c2416-623c-43a8-be9e-076781071bd2)

## Step 3: How to create files

![image](https://github.com/hughiephan/DPL/assets/16631121/2243df05-1b9e-4655-be50-a807b233e579)

## Step 4: Create App.py

![image](https://github.com/hughiephan/DPL/assets/16631121/b0c69afa-9ba2-4f69-916a-14b50eeb2b26)

```python
import numpy as np
import cv2
import gradio as gr
from PIL import Image

def detect_faces(image):
    image_np = np.array(image)
    gray_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        cv2.rectangle(image_np, (x, y), (x+w, y+h), (0, 255, 0), 2)
    image_with_boxes = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
    return image_with_boxes

iface = gr.Interface(
    fn=detect_faces,
    inputs="image",
    outputs="image",
    title="Face Detection",
    description="Upload an image, and the model will detect faces and draw bounding boxes around them.",
)

iface.launch()
```

## Step 5: Create Requirements.txt

![image](https://github.com/hughiephan/DPL/assets/16631121/c1b357f2-8099-4d70-9ea9-cd41ed457301)

```
opencv-python
```

## Step 6: Folder structure

Make sure that our space's folder structure looks like this

![image](https://github.com/hughiephan/DPL/assets/16631121/5bb795e4-a863-4686-9ece-f17836b8797d)

## Step 7: Run demo

![image](https://github.com/hughiephan/DPL/assets/16631121/05280682-042a-4dd8-ad00-ecbc35edcd3e)

## Step 8: Get prediction

![image](https://github.com/hughiephan/DPL/assets/16631121/9c6f1ee2-b862-415c-b4a5-608d77bac72a)

## Reference
- https://becominghuman.ai/face-detection-using-opencv-with-haar-cascade-classifiers-941dbb25177
