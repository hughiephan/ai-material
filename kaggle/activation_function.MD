# Activation Function

## Introduction
This notebook demonstrates how different activation functions—sigmoid, tanh, and ReLU—operate on an array of numbers, showcasing their respective output transformations. Activation functions in deep learning are mathematical equations applied to the output of each neuron in a neural network. They introduce non-linearities to the network, allowing it to model complex relationships in data. The primary purpose of an activation function is to determine the output of a neural network node or neuron, typically transforming the input into the desired output, usually by introducing non-linear properties. This transformation is crucial for the network to learn complex patterns in data that linear functions alone can't capture.

If you're interested in exploring similar data analysis or learning more about AI applications, then checkout my personal website https://hughiephan.co . Don't forget to upvote if you found the notebook insightful or helpful. Your feedback is valuable and can help others discover useful content.

## Initialize
Initialize a NumPy array named 'x' containing the elements -3, -2, -1, 1, 2, and 3. The NumPy library is used to create this array, allowing for efficient numerical operations and array handling in Python.

```python
import numpy as np
x = np.array([-3, -2, -1, 1, 2, 3])
```

## Sigmoid Function

Calculates the sigmoid values for each element in the array 'x' using the formula and outputs the sigmoid values for the given elements.

$$\text{Sigmoid}(x) = \frac{1}{1 + e^{-x}}$$

```python
print("Sigmoid ", 1 / (1 + np.exp(-x)))
```

## Tanh Function

Hyperbolic Tangent (Tanh) Function: Computes the hyperbolic tangent values for each element in the array 'x' using np.tanh(x). It returns the hyperbolic tangent values of the provided elements.

$$\text{Tanh}(x) = \tanh(x)$$

```python
print("Tanh ", np.tanh(x))
```

## Relu Function

Utilizes the ReLU activation function (np.maximum(x, 0)) on the array 'x', generating output by replacing negative values with zero and retaining positive values.

$$\text{ReLU}(x) = \max(0, x)$$

```python
print("ReLU ", np.maximum(x,0))
```
