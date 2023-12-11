# Weights and Biases

![image](https://github.com/hughiephan/DPL/assets/16631121/c7737b71-bb42-423b-989b-9522eedb60ee)

```python
import numpy as np
import math
import matplotlib.pyplot as plt

def activationFunc(x):
    return np.log(1 + np.exp(x))

def linearFunc(x, w, b):
    return x*w + b

x = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6 ,0.7, 0.8, 0.9, 1])
y = np.array([0, 0 , 0, 0, 1, 1, 1, 0 ,0, 0, 0])
bFinal = -0.58
```




```python
w1 = -34.4
b1 = 2.14
w3 = -1.3

fig, axis = plt.subplots(2,2, figsize=(15, 15))

# Show Data Points
for i in x:
    axis[0,0].scatter(x, y, marker='o', color='turquoise')
    axis[0,0].set_title("Step 1: Show Data Points")

# Step 1
axis[0,1].plot(x, linearFunc(x, w1, b1))
for i in x:
    axis[0,1].scatter(x, y, marker='o', color='turquoise')
    axis[0,1].plot(x, linearFunc(x, w1, b1), marker='o', markersize=3, color='cornflowerblue')
    axis[0,1].set_title("Step 1: Calculate Linear Function")

# Step 2
axis[1,0].plot(x, activationFunc(linearFunc(x, w1, b1))) 
for i in x:
    axis[1,0].scatter(x, y, marker='o', color='turquoise')
    axis[1,0].plot(x, activationFunc(linearFunc(x, w1, b1)), marker='o', markersize=3, color='cornflowerblue')
    axis[1,0].set_title("Step 2: Calculate Activation Function with Linear Function")

# Step 3.1
axis[1,1].plot(x, activationFunc(linearFunc(x, w1, b1)) * w3)
for i in x:
    axis[1,1].scatter(x, y, marker='o', color='turquoise')
    axis[1,1].plot(x, activationFunc(linearFunc(x, w1, b1)) * w3, marker='o', markersize=3, color='cornflowerblue') 
    axis[1,1].set_title("Step 3.1: Calculate Linear Function (Weight part only) ")
```

```python
w2 = -2.52
b2 = 1.29
w4 = 2.28
fig, axis = plt.subplots(2,2, figsize=(15, 15))

# Show Data Points
for i in x:
    axis[0,0].scatter(x, y, marker='o', color='turquoise')
    axis[0,0].set_title("Step 1: Show Data Points")

# Step 1
axis[0,1].plot(x, linearFunc(x, w2, b2))
for i in x:
    axis[0,1].scatter(x, y, marker='o', color='turquoise')
    axis[0,1].plot(x, linearFunc(x, w2, b2), marker='o', markersize=3, color='orange')
    axis[0,1].set_title("Step 1: Calculate the Linear Function")

# Step 2
axis[1,0].plot(x, activationFunc(linearFunc(x, w2, b2))) 
for i in x:
    axis[1,0].scatter(x, y, marker='o', color='turquoise')
    axis[1,0].plot(x, activationFunc(linearFunc(x, w2, b2)), marker='o', markersize=3, color='orange')
    axis[1,0].set_title("Step 2: Calculate Activation Function with Linear Function")

# Step 3.1
axis[1,1].plot(x, activationFunc(linearFunc(x, w2, b2)) * w4)
for i in x:
    axis[1,1].scatter(x, y, marker='o', color='turquoise')
    axis[1,1].plot(x, activationFunc(linearFunc(x, w2, b2)) * w4, marker='o', markersize=3, color='orange') 
    axis[1,1].set_title("Step 3.1: Calculate Activation Function with Linear Function (Weight part only)")
```

```python
fig, axis = plt.subplots(2, figsize=(10, 10))

# Step 4
for i in x:
    axis[0].scatter(x, y, marker='o', color='turquoise')
    axis[0].plot(x, activationFunc(linearFunc(x, w1, b1)) * w3, marker='o', markersize=3, color='cornflowerblue') 
    axis[0].plot(x, activationFunc(linearFunc(x, w2, b2)) * w4, marker='o', markersize=3, color='orange')
    axis[0].plot(x, (activationFunc(linearFunc(x, w1, b1)) * w3) + (activationFunc(linearFunc(x, w2, b2)) * w4 ) + bFinal,marker='o', markersize=3, color='lightgreen')  
    axis[0].set_title("Step 3.2: Combine with two functions from previous steps and plus the final bias")
    
# Make Prediction
for i in x:
    axis[1].scatter(x, y, marker='o', color='turquoise')
    axis[1].plot(x, (activationFunc(linearFunc(x, w1, b1)) * w3) + (activationFunc(linearFunc(x, w2, b2)) * w4 ) + bFinal,marker='o', markersize=3, color='lightgreen')  
    axis[1].set_title("Use the Final Function to make prediction")
```

![image](https://github.com/hughiephan/DPL/assets/16631121/9a90ae64-4c9c-4485-963c-82bf0acd7a74)
