# ANN on Fashion MNIST

```python
import tensorflow as tf
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from tensorflow import keras
fashion_mnist = keras.datasets.fashion_mnist
(X_train_full, y_train_full), (X_test, y_test) = fashion_mnist.load_data()
# Scale the pixel intensities down to the 0-1 range by dividing them by 255.0
X_valid, X_train = X_train_full[:5000] / 255., X_train_full[5000:] / 255. 
y_valid, y_train = y_train_full[:5000], y_train_full[5000:]
X_test = X_test / 255.
```

```python
model = keras.models.Sequential([
    keras.layers.Flatten(input_shape=[28, 28]),
    keras.layers.Dense(300, activation="relu"),
    keras.layers.Dense(100, activation="relu"),
    keras.layers.Dense(10, activation="softmax")
])
model.compile(loss="sparse_categorical_crossentropy", optimizer="sgd", metrics=["accuracy"])
print(model.summary())
history = model.fit(X_train, y_train, epochs=10, validation_data=(X_valid, y_valid))
model.evaluate(X_test, y_test) 
```

```python
image = X_test[0]  # Let's visualize the first image in the test set
input_data = image.reshape(1, 28, 28) / 255.0  # Reshape and normalize the image
flatten_layer = model.get_layer('flatten')
visualization_model = keras.models.Model(model.input, flatten_layer.output)
output_data = visualization_model.predict(input_data) # Get the output of the Flatten layer for the input image
print("Original Image")
plt.imshow(image, cmap="gray")
plt.show()
print("After flatten")
plt.figure(figsize=(100, 50)) 
plt.imshow(output_data, cmap='gray')
plt.axis('off')
plt.show()
```

![image](https://github.com/hughiephan/DPL/assets/16631121/0c580bb8-5dcc-41ce-aad0-772b5478a7d1)
