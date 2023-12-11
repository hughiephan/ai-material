# Bayes Optimization

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
def objective_function(x): # Blackbox Function
    return np.sin(3 * x) + 0.1 * x ** 2
def ucb(x, gp_model, kappa): # Acquisition function (using Upper Confidence Bound)
    mean, std = gp_model.predict(x.reshape(-1, 1), return_std=True)
    return mean + kappa * std
x = np.linspace(-5, 5, 400)
np.random.seed(0)
x_samples = np.random.uniform(-5, 5, size=5)
y_samples = objective_function(x_samples)
kappa = 2.0  # UCB exploration parameter
num_iterations = 2
for i in range(num_iterations):
    gp_model = GaussianProcessRegressor().fit(x_samples.reshape(-1, 1), y_samples) # Fit a GP model to the available data
    acquisition_values = ucb(x, gp_model, kappa) # Calculate the UCB acquisition values for the search space
    next_x = x[np.argmax(acquisition_values)] # Select the next point to evaluate based on the maximum acquisition value
    next_y = objective_function(next_x) # Evaluate the objective function at the selected point
    # Update the samples with the new evaluation
    x_samples = np.append(x_samples, next_x)
    y_samples = np.append(y_samples, next_y)
plt.figure(figsize=(10, 6))
plt.plot(x, objective_function(x), color= 'orange', label='Objective Function')
plt.scatter(x_samples, y_samples, color='red', marker='o', label='Data Points')
plt.plot(x, ucb(x, gp_model, kappa), color='green', label='Surrogate Function')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Fitting Surrogate Function \n into Objective Function')
plt.legend()
plt.grid(True)
plt.show()
```

```python
x_scatter = np.array([0, 0.5, 2.0, 1.0])
y_scatter = np.sin(x_scatter * np.pi)
x = np.linspace(0, 2, 100)
kernel = RBF(length_scale=0.1)
gpr = GaussianProcessRegressor(kernel=kernel)
gpr.fit(x_scatter.reshape(-1, 1), y_scatter)
y_mean, y_std = gpr.predict(x.reshape(-1, 1), return_std=True)
n_functions = 5
functions = gpr.sample_y(x.reshape(-1, 1), n_samples=n_functions)
plt.fill_between(x, y_mean - 2*y_std, y_mean + 2*y_std, color='lightblue', alpha=0.3, label='±2 Standard Deviation')
plt.scatter(x_scatter, y_scatter, color='red', label='Data Points')
for i in range(n_functions):
    plt.plot(x, functions[:, i], alpha=0.4, label='Line {}'.format(i))
plt.xlabel('x')
plt.ylabel('y')
plt.title('Gaussian Process Regression')
plt.legend()
plt.show()

plt.fill_between(x, y_mean - 2*y_std, y_mean + 2*y_std, color='lightblue', alpha=0.3, label='±2 Standard Deviation')
plt.scatter(x_scatter, y_scatter, color='red', label='Data Points')
plt.plot(x, functions[:, i], alpha=0.4, label='Mean line')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Gaussian Process Regression')
plt.legend()
plt.show()
```

![image](https://github.com/hughiephan/DPL/assets/16631121/8a19561c-64f7-45c6-9064-7d52f93f898a)
