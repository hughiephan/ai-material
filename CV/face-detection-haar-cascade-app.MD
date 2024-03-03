## Face Detection with Haar Cascade Application

![image](https://github.com/hughiephan/DPL/assets/16631121/5bb795e4-a863-4686-9ece-f17836b8797d)

## App.py
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

## Requirements.txt
```
opencv-python
```

![image](https://github.com/hughiephan/DPL/assets/16631121/9c6f1ee2-b862-415c-b4a5-608d77bac72a)

