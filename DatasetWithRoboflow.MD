# Image Dataset with Roboflow

Step 1: Create new Project

![image](https://github.com/hughiephan/DPL/assets/16631121/307eb057-1af4-429c-be8d-52e52b9cdcc0)

![image](https://github.com/hughiephan/DPL/assets/16631121/9435c558-3e58-414e-bfe5-e71f0226fa4b)

Step 2: Upload Dataset

![image](https://github.com/hughiephan/DPL/assets/16631121/6e3ff2b0-f070-40ba-8055-b3da360e0a25)

![image](https://github.com/hughiephan/DPL/assets/16631121/aed2565d-f16e-4e8c-ba73-93eb7cebe37e)

![image](https://github.com/hughiephan/DPL/assets/16631121/7bc25a67-2a36-4422-8ecf-22819c1d2f38)

Step 3: Generate new version for the dataset with minimum Pre-processing and Augmentation

![image](https://github.com/hughiephan/DPL/assets/16631121/b73d1127-b7f0-4f22-a0ee-85ed46f7f0ba)

Step 4: Export the Dataset

![image](https://github.com/hughiephan/DPL/assets/16631121/e1c7e138-edd7-458a-a956-7ed621445bbe)

![image](https://github.com/hughiephan/DPL/assets/16631121/36d69c15-9c9f-4644-ab95-cb4336daa0b7)


Step 5: Copy the code

![image](https://github.com/hughiephan/DPL/assets/16631121/2bf43b3d-e083-454a-8c97-2d400bdb4af0)

Step 6: Create new Notebook
```py
!pip install roboflow
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from torchvision import transforms
from roboflow import Roboflow
rf = Roboflow(api_key="ADD_YOUR_API_KEY")
project = rf.workspace("ADD_YOUR_WORKSPACE").project("ADD_YOUR_PROJECT")
dataset = project.version("ADD_PROJECT_VERSION").download("folder")
```


