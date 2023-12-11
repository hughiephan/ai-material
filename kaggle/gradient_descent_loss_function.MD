```python
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42) # Generate random but repoducible scatter data points 
num_points = 10
x = np.random.rand(num_points)
y = np.random.rand(num_points)
a = np.random.rand()
b = np.random.rand()
f = lambda x: a * x + b # Generate a random function (linear equation)
residuals = y - f(x)
sum_squared_residuals = np.sum(residuals**2) # Calculate the sum of squared residuals
vertical_distances = np.abs(residuals) # Calculate the vertical distance between the function and each data point
r_function = (a,b, sum_squared_residuals, vertical_distances)
functions = []
functions.append((a, b, sum_squared_residuals, vertical_distances)) # Combine the Random linear functions and with the previous function above 

# Visualize the scatter data points and the function
plt.scatter(x, y, color='green', label='Data Points')
plt.title('Data Points')
plt.show()

# Visualize the scatter data points and the function
plt.scatter(x, y, color='green', label='Data Points')
plt.plot(x, f(x), color='red', label='Random Function')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Loss Function')
plt.legend()
text = f'Sum of Squared Residuals \n (Loss Value): {sum_squared_residuals:.2f}' # Annotate the sum of squared residuals
plt.annotate(text, xy=(0.05, 0.65), xycoords='axes fraction', fontsize=10, ha='left', va='top')
for i, v in enumerate(y): # Plot vlines to show the distance between each data point and the function
    label = f'{residuals[i]**2:.2f}'
    if (y[i] < f(x[i])):
        plt.vlines(x[i], y[i], y[i] + vertical_distances[i], colors='black')
        plt.text(x[i] + 0.04, y[i] + vertical_distances[i]/2, label , ha='center', va='bottom', fontsize=8)
    if (y[i] > f(x[i])):
        plt.vlines(x[i], y[i], y[i] - vertical_distances[i], colors='black')
        plt.text(x[i] + 0.04, y[i] - vertical_distances[i]/2, label, ha='center', va='top', fontsize=8)
plt.show()

num_functions = 9 # Also generate 9 random linear functions and combine with the 1 function above
for _ in range(num_functions):
    a = np.random.rand() # Random slope
    b = np.random.rand() # Random y-intercept
    f = lambda x: a * x + b  # Linear function
    residuals = y - f(x)
    sum_squared_residuals = np.sum(residuals**2)
    vertical_distances = np.abs(residuals)
    functions.append((a, b, sum_squared_residuals, vertical_distances))
```

![image](https://github.com/hughiephan/DPL/assets/16631121/eb1d0449-ac71-4bb5-af99-282ea5039034)

```python
# Plot the Random linear functions
colors = ['red', 'green', 'blue', 'orange', 'purple', 'cyan', 'magenta', 'pink', 'brown', 'gray']
plt.figure(figsize=(10, 6))
for i, (a,b,s, v) in enumerate(functions):
    color = colors[i % len(colors)]
    plt.plot(x, a * x + b, linewidth=1, alpha=0.8, color = color)
plt.scatter(x, y, color='green', label='Data Points')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Random Linear Functions')
plt.show()

# Plot the Random linear functions and their Loss Value
for i, (a,b,s, v) in enumerate(functions):
    color = colors[i % len(colors)]
    plt.scatter(i, s, marker='o', color= color)
    plt.text(i, s, f'{s:.2f}', ha='center', va='bottom')

plt.xlabel('Index of the Random Linear Function')
plt.ylabel('Loss Function Value')
plt.title('Loss Function Value of Random Linear Functions')
plt.show()
```

![image](https://github.com/hughiephan/DPL/assets/16631121/d4510811-3eb4-4d27-9914-cf97ef052722)


```python
def gradient_descent(x, y, learning_rate, num_iterations):
    # Initialize the parameters
    a = 0
    b = 0
    n = len(x)
    # Store the parameter values for plotting
    a_values = [a]
    b_values = [b]
    loss_values = []
    for iteration in range(num_iterations):  # Perform gradient descent
        y_pred = a * x + b # Calculate the predicted values
        residuals = y_pred - y
        sum_squared_residuals = np.sum(residuals**2)
        # Calculate the gradients
        gradient_a = (2/n) * np.sum((y_pred - y) * x)
        gradient_b = (2/n) * np.sum(y_pred - y)
        # Update the parameters
        a -= learning_rate * gradient_a
        b -= learning_rate * gradient_b
        # Store the parameter values
        a_values.append(a)
        b_values.append(b)
        loss_values.append(sum_squared_residuals)
    return a, b, a_values, b_values, loss_values

learning_rate = 0.1 # Set hyperpameter learning rate
num_iterations = 5
a_optimal, b_optimal, a_values, b_values, loss_values = gradient_descent(x, y, learning_rate, num_iterations) # Perform gradient descent

for i, v in enumerate(a_values):
    plt.title('Training at step ' + str(i))
    plt.scatter(x, y, color='green', label='Data Points')
    plt.plot(x, a_values[i] * x + b_values[i], linewidth=1, alpha=0.8)
    plt.show()
    
residuals = y - a_optimal * x + b_optimal
sum_squared_residuals = np.sum(residuals**2)
```

```python
plt.title('Loss Value after training ' + str(num_iterations) + ' times')
plt.scatter(list(range(num_iterations)), loss_values, linewidth=1, alpha=1)
plt.plot(loss_values)
print("Optimal Linear Function: y = " + str(a_optimal) + "*x + " + str(b_optimal))
print("Loss Value of the Optimal Linear Function ", sum_squared_residuals)
```

![image](https://github.com/hughiephan/DPL/assets/16631121/bacc1e28-861b-410c-8770-eeb448649698)
