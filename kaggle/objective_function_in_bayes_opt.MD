# Objective Function in Bayes Opt 

```python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skopt import gp_minimize
from skopt.space import Real
from skopt.utils import use_named_args

def objective_function(x):
    result = (x[0] - 2) ** 2 + (x[1] + 1) ** 2
    return result
space = [Real(-5, 5, name='x1'), Real(-5, 5, name='x2')]
@use_named_args(space)
def optimize(x1, x2):
    return objective_function([x1, x2])
step = 50
result = gp_minimize(optimize, space, n_calls=step)
x1_values = [x[0] for x in result.x_iters]
x2_values = [x[1] for x in result.x_iters]
y_values = result.func_vals
```

```python
for i in range(len(x1_values)):
    if i == 5: # Show only the first few steps
        break
    fig = plt.figure(figsize=(20, 5))
    ax1 = fig.add_subplot(121, projection='3d')
    x1 = np.linspace(-5, 5, 100)
    x2 = np.linspace(-5, 5, 100)
    X1, X2 = np.meshgrid(x1, x2)
    Y = objective_function([X1, X2])
    ax1.plot_surface(X1, X2, Y, cmap='YlOrBr', alpha=0.2)
    ax1.set_xlabel('x1')
    ax1.set_ylabel('x2')
    ax1.set_zlabel('Objective Value')
    ax1.set_title('Bayesian Optimization - Step {}'.format(i+1))
    ax1.plot(x1_values[:i+1], x2_values[:i+1], y_values[:i+1], c='b', linestyle='-', label='Optimization Path')
    scatter = ax1.scatter(x1_values[:i+1], x2_values[:i+1], y_values[:i+1], c=y_values[:i+1], cmap='cool', marker='o', label='Optimization Point')
    fig.colorbar(scatter, ax=ax1, label='Objective Value')
    for k in range(len(x1_values[:i+1])):
        ax1.text(x1_values[k], x2_values[k], y_values[k], round(y_values[k],1), color='b', fontsize=8)
    plt.tight_layout()
    plt.show()
```

```python
fig = plt.figure(figsize=(20, 5))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x1_values, x2_values, y_values, c='r', marker='o', label='Optimization Point')
ax.set_xlabel('x1')
ax.set_ylabel('x2')
ax.set_zlabel('Objective Value')
ax.set_title('Bayesian Optimization at Step {}'.format(step))
ax.legend()
plt.show()
```

![image](https://github.com/hughiephan/DPL/assets/16631121/093407ec-2170-4d40-8b7d-6c2216b23c39)
