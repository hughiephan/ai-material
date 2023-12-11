# PCA

```python
import numpy as np
import matplotlib.pyplot as plt

matrix = np.array([[0, 2], [3, 0], [4, 1], [5,4]]) # create a numpy array that stores the data matrix
covariance_matrix = np.cov(matrix, rowvar=False) # calculate the covariance matrix
eigen_values, eigen_vectors = np.linalg.eig(covariance_matrix) # compute eigenvalues and eigenvectors

sorted_indices = np.argsort(eigen_values)[::-1]
eigen_values = eigen_values[sorted_indices]
eigen_vectors = eigen_vectors[:, sorted_indices]
first_pc = eigen_vectors[:, 0] # take the first principal component direction
projections = np.dot(matrix, first_pc) # project data points onto the first principal component line
projected_points = np.outer(projections, first_pc) # calculate coordinates of projected points on the first principal component line

print(projected_points)

plt.scatter(matrix[:, 0], matrix[:, 1], label='Original Data Points') # plot original data points
plt.scatter(projected_points[:, 0], projected_points[:, 1], label='Projections', marker='x')
plt.plot([0, first_pc[0]], [0, first_pc[1]], color='red', label='First Principal Component')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.show()
```

![image](https://github.com/hughiephan/DPL/assets/16631121/4e5a7436-addd-4b69-b580-b111b4a7cb47)
