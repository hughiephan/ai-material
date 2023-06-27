Import Libraries
```py
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Input, Lambda, Dense, Flatten, Dropout
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
```

Download Dataset
```py
https://www.kaggle.com/datasets/ashishjangra27/face-mask-12k-images-dataset
```

Config
```py
input_size = (128,128)
input_shape = (128, 128, 3)
base_dir = '../input/face-mask-12k-images-dataset/Face Mask Dataset/'
```

Import generator
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

Transfer learning
```py
vgg16 = VGG16(input_shape=input_shape, weights='imagenet', include_top=False)
for layer in vgg16.layers:
    layer.trainable = False
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
```

Train the model
```py
history = model.fit(train_data,
                    batch_size=32,
                    epochs=1,
                    validation_data=val_data)
```
