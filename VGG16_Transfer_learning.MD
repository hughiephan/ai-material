Import Libraries
```py
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Input, Lambda, Dense, Flatten, Dropout
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
```

Face Mask Dataset
```py
https://www.kaggle.com/datasets/ashishjangra27/face-mask-12k-images-dataset
```
![image](https://github.com/hughiephan/DPL/assets/16631121/71604595-7981-4808-890e-e5d57a224c81)

![image](https://github.com/hughiephan/DPL/assets/16631121/15f8cff9-cd23-4d5e-ad79-3e63e1e437eb)

Config
```py
input_size = (128,128)
input_shape = (128, 128, 3)
base_dir = '../input/face-mask-12k-images-dataset/Face Mask Dataset/'
```

Import generator

I use the ImageDataGenerator function from Keras to create an image generator that can apply these augmentations to the training images. The parameters for the different augmentations are set as follows:
- Rotation: Up to 30 degrees
- Height Shift: Up to 10% of the image height
- Width Shift: Up to 10% of the image width
- Zoom: Up to 10%
- Horizontal Flip: Enabled

```py
train_gen = ImageDataGenerator(
    rescale=1./255, 
    zoom_range=0.1,
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
    brightness_range=[0.2,1.5],
    fill_mode="nearest"
)
val_gen = ImageDataGenerator(rescale=1./255)
test_gen = ImageDataGenerator(rescale=1./255)
```

Pre-process the data
```py
train_data = train_gen.flow_from_directory(base_dir + 'Train',target_size=input_size,seed=42)
val_data = val_gen.flow_from_directory(base_dir + 'Validation',target_size=input_size,seed=42)
test_ds = test_gen.flow_from_directory(base_dir + 'Test',target_size=input_size,seed=42)
```
![image](https://github.com/hughiephan/DPL/assets/16631121/3dc60840-7919-49fa-a626-45678cc4d1e9)


Transfer learning
```py
vgg16 = VGG16(input_shape=input_shape, weights='imagenet', include_top=False)
for layer in vgg16.layers:
    layer.trainable = False
vgg16.summary()
```
![image](https://github.com/hughiephan/DPL/assets/16631121/3d0043ac-22ac-497e-ae3f-3813378c79c5)

```py
output = Flatten()(vgg16.output)
output = Dense(500, activation='relu')(output)
output = Dense(100, activation='relu')(output)
output = Dropout(0.5)(output)
output = Dense(2, activation='sigmoid')(output)
model = Model(inputs=vgg16.input, outputs=output)
model.compile(
  loss='binary_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)
model.summary()
```
![image](https://github.com/hughiephan/DPL/assets/16631121/807ef1fb-0805-496f-aaef-0aba55627094)

Train the model
```py
history = model.fit(train_data,
                    batch_size=32,
                    epochs=10,
                    validation_data=val_data)
```
