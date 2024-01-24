
## Step
```python
import numpy as np
import requests
import matplotlib.pyplot as plt
```

img = np.array(Image.open(requests.get('https://i.imgur.com/MWMslYc.png', stream=True).raw))

# Reshape the image into a 2D array
img_2d = img.reshape(img.shape[0], -1)
U, S, V = np.linalg.svd(img_2d, full_matrices=False)
S[S < 3000] = 0

# Reconstruct the denoised image
denoised_img_2d = np.dot(U, np.dot(np.diag(S), V))
denoised_img = denoised_img_2d.reshape(img_shape)
denoised_img = np.clip(denoised_img, 0, 255)
denoised_img = denoised_img.astype(np.uint8)

# Plot the original and denoised images side by side
plt.subplot(1, 2, 1)
plt.imshow(img)
plt.subplot(1, 2, 2)
plt.imshow(denoised_img)
plt.show()
