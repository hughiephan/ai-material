# Batch, Stochastic, Mini-batch Gradient Descent

```python
import numpy as np
import matplotlib.pyplot as plt

def cost_function(theta0, theta1):
    return np.mean((y - (theta0 + theta1 * X)) ** 2)

def gradient(theta0, theta1, X, y):
    grad_theta0 = -2 * np.mean(y - (theta0 + theta1 * X))
    grad_theta1 = -2 * np.mean((y - (theta0 + theta1 * X)) * X)
    return grad_theta0, grad_theta1

# Generate Data
np.random.seed(42)
samples = 10
X = np.linspace(0, 10, samples)
y = 2 * X + np.random.normal(0, 1, size=samples)
eta = 0.01  # Learning rate
max_iterations = 5
```

```python
def batch_gradient_descent(eta, max_iterations):
    theta0 = 0.0  # Initial intercept
    theta1 = 0.0  # Initial slope
    cost_values = []
    for iteration in range(max_iterations):
        # Computing Gradient
        grad_theta0, grad_theta1 = gradient(theta0, theta1, X, y)
        theta0 -= eta * grad_theta0
        theta1 -= eta * grad_theta1
        cost_values.append(cost_function(theta0, theta1))
        plt.figure(figsize=(10, 4))
        # Feature vs Target
        plt.subplot(121)
        plt.scatter(X, y, label='Data Points')
        plt.plot(X, theta0 + theta1 * X, color='red', label=f'Iteration {iteration+1}')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Finding the best line with \n Batch Gradient Descent')
        plt.grid(True)
        plt.legend()
        # Cost vs Iteration
        plt.subplot(122)
        plt.scatter(np.arange(0, len(cost_values), dtype=int), cost_values, color='orange')
        for i, v in enumerate(cost_values):
            plt.text(i, v, np.round(v, 3))
        plt.plot(cost_values, color='orange')
        plt.xlabel('Iteration')
        plt.ylabel('Cost')
        plt.title('Cost of current line')
        plt.show()
    return cost_values

cost_bgd = batch_gradient_descent(eta, max_iterations)
```

```python
def stochastic_gradient_descent(eta, max_iterations):
    theta0 = 0.0  # Initial intercept
    theta1 = 0.0  # Initial slope
    cost_values = []
    for iteration in range(max_iterations):
        idx = np.random.randint(0, samples)  
        x_i = X[idx]
        y_i = y[idx]
        grad_theta0, grad_theta1 = gradient(theta0, theta1, x_i, y_i)
        theta0 -= eta * grad_theta0
        theta1 -= eta * grad_theta1
        cost_values.append(cost_function(theta0, theta1))
        plt.figure(figsize=(10, 4))
        # Feature vs Target
        plt.subplot(121)
        plt.scatter(X, y, label='Data Points')
        plt.scatter(x_i, y_i, label='Randomly Picked Data')
        plt.plot(X, theta0 + theta1 * X, color='red', label=f'Iteration {iteration+1}')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Finding the best line with \n Stochastic Gradient Descent')
        plt.grid(True)
        plt.legend()
        # Cost vs Iteration
        plt.subplot(122)
        plt.scatter(np.arange(0, len(cost_values), dtype=int), cost_values, color='green')
        for i, v in enumerate(cost_values):
            plt.text(i, v, np.round(v, 3))
        plt.plot(cost_values, color='green')
        plt.xlabel('Iteration')
        plt.ylabel('Cost')
        plt.title('Cost of current line')
        plt.show()
    return cost_values

cost_sgd = stochastic_gradient_descent(eta, max_iterations)
```

```python
def minibatch_gradient_descent(eta, max_iterations):
    theta0 = 0.0  # Initial intercept
    theta1 = 0.0  # Initial slope
    batch_size = 5 # If you set Batch_Size = Numer_of_samples, this will become Gradient Descent
    num_batches = samples // batch_size
    cost_values = []
    cost_values_of_batch = []
    for iteration in range(max_iterations):
        # Computing Gradient
        permutation = np.random.permutation(samples)
        X_shuffled = X[permutation]
        y_shuffled = y[permutation]
        for batch in range(num_batches):
            start = batch * batch_size
            end = start + batch_size
            X_batch = X_shuffled[start:end]
            y_batch = y_shuffled[start:end]
            grad_theta0, grad_theta1 = gradient(theta0, theta1, X_batch, y_batch)
            theta0 -= eta * grad_theta0
            theta1 -= eta * grad_theta1
            cost_values_of_batch.append(cost_function(theta0, theta1))
            plt.figure(figsize=(10, 4))
            # Feature vs Target
            plt.subplot(121)
            plt.scatter(X, y, label='Data Points')
            plt.scatter(X_batch, y_batch, label='Randomly Picked Data')
            plt.plot(X, theta0 + theta1 * X, color='red', label=f'Iteration {iteration+1}, Batch {batch+1}')
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.title('Finding the best line with \n Mini-batch Gradient Descent')
            plt.grid(True)
            plt.legend()
            # Cost vs Iteration
            plt.subplot(122)
            plt.scatter(np.arange(0, len(cost_values_of_batch), dtype=int), cost_values_of_batch, color='purple')
            for i, v in enumerate(cost_values_of_batch):
                plt.text(i, v, np.round(v, 3))
            plt.plot(cost_values_of_batch, color='purple')
            plt.xlabel('Iteration with Batch')
            plt.ylabel('Cost')
            plt.title('Cost of current line')
            plt.show()
        cost_values.append(cost_values_of_batch.pop()) # Get the cost in the final batch of that iteration
    return cost_values

cost_mbgd = minibatch_gradient_descent(eta, max_iterations)
```

```python
plt.figure(figsize=(10, 4))
plt.plot(cost_bgd, color='orange', label="Batch Gradient Descent")
plt.plot(cost_sgd, color='green', label='Stochastic Gradient Descent')
plt.plot(cost_mbgd, color='purple', label='Mini-batch Gradient Descent')
plt.legend(loc="upper left")
plt.xlabel('Iteration')
plt.ylabel('Cost')
plt.title('Cost Comparison')
plt.show()
```

![image](https://github.com/hughiephan/DPL/assets/16631121/5e1db926-dd86-403e-a736-52fd71109b21)
