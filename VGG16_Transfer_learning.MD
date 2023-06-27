Import Libraries
```py
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Input, Lambda, Dense, Flatten
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
```

Download Dataset
```py
!kaggle datasets download -d ashishjangra27/face-mask-12k-images-dataset
```

Unzip the dataset
```py
!unzip -q /content/face-mask-12k-images-dataset.zip
```

Pre-process data
```py
INPUT_SIZE = [128,128]
BATCH = 32
training_datagen = ImageDataGenerator(rescale=1./255, 
                                      zoom_range=0.1,
                                      rotation_range=20,
                                      width_shift_range=0.1,
                                      height_shift_range=0.1,
                                      horizontal_flip=True,
                                      brightness_range=[0.2,1.5],
                                      fill_mode="nearest")
training_data = training_datagen.flow_from_directory('/content/Face Mask Dataset/Train',
                                                     target_size = INPUT_SIZE,
                                                     batch_size=BATCH,
                                                     class_mode = 'binary')
test_datagen = ImageDataGenerator(rescale=1./255)
test_data = training_datagen.flow_from_directory('/content/Face Mask Dataset/Test',
                                                     target_size = INPUT_SIZE,
                                                     batch_size=BATCH,
                                                     class_mode = 'binary')
```

vgg16 = VGG16(input_shape=INPUT_SIZE + [3], weights='imagenet', include_top=False)



