# Denoising with SVD

## Step 1: Import libraries
```python
import numpy as np
import requests
import matplotlib.pyplot as plt
```

## Step 2: Download image
```python
img = np.array(Image.open(requests.get('https://i.imgur.com/MWMslYc.png', stream=True).raw))
```

## Step 3: 
```python
img_2d = img.reshape(img.shape[0], -1)
U, S, V = np.linalg.svd(img_2d, full_matrices=False)
S[S < 3000] = 0
```

## Step 4: Reconstruct image
```python
denoised_img_2d = np.dot(U, np.dot(np.diag(S), V))
denoised_img = denoised_img_2d.reshape(img_shape)
denoised_img = np.clip(denoised_img, 0, 255)
denoised_img = denoised_img.astype(np.uint8)
```

## Step 5: Plot images
```python
plt.subplot(1, 2, 1)
plt.imshow(img)
plt.subplot(1, 2, 2)
plt.imshow(denoised_img)
plt.show()
```

![image](https://github.com/hughiephan/DPL/assets/16631121/7f702758-0dd4-46ad-b29c-fbb653836f67)

## Reference
- https://www.researchgate.net/figure/a-Original-Image-lena-b-Noisy-image-noise-density-08-c-Bilateral-filter_fig4_317421347
- https://medium.com/@maydos/image-processing-with-singular-value-decomposition-ce8db3f78ce0