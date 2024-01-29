# Denoising with SVD

Singular Value Decomposition (SVD) can be used for denoising due to its ability to describe the image's underlying concepts along unwanted noises. The key to denoising lies in the analysis of singular values in the Sigma matrix. Singular values in the Sigma matrix act as weights, indicating the contribution of each concept to the overall image. In denoising, the higher singular values are retained as they represent the predominant information, while the lower ones, associated with noise, are suppressed or discarded. 

![Untitled-2023-07-31-0913](https://github.com/hughiephan/DPL/assets/16631121/e4918e01-22e9-4527-b9ac-f066ba3e2fbd)

## Step 1: Import libraries
```python
import requests
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
```

## Step 2: Download noised image 

```python
img = np.array(Image.open(requests.get('https://i.imgur.com/MWMslYc.png', stream=True).raw))
```

![img](https://i.imgur.com/MWMslYc.png)

## Step 3: SVD

The image is flattened from 3D array into a 2D array using the `reshape(...,-1)` function. Then we apply SVD to the 2D image using the `np.linalg.svd` function, resulting in `U` and `V` are orthogonal matrices, and `S` is a diagonal matrix containing singular values. The parameter `full_matrices=False` indicates that only the essential parts of the decomposition are computed. Finally, any singular values in the S matrix that are less than `3000` are set to zero. This operation is a form of thresholding, where singular values below a certain threshold are effectively disregarded, removing the noise.

```python
img_2d = img.reshape(img.shape[0], -1)
U, S, V = np.linalg.svd(img_2d, full_matrices=False)
S[S < 3000] = 0
```

Output of `S` before we remove noise

![image](https://github.com/hughiephan/DPL/assets/16631121/7b999612-2a08-42ea-b0de-74d7b327d8ac)


## Step 4: Reconstruct image

The denoised image `denoised_img_2d` is reconstructed using the matrices obtained from the SVD: `U`, `S`, and `V`. This denoised image is then reshaped to the original image shape. To ensure pixel values remain within the valid range of 0 to 255, the `np.clip` function is applied, limiting values that fall outside this range. 

```python
denoised_img_2d = np.dot(U, np.dot(np.diag(S), V))
denoised_img = denoised_img_2d.reshape(img.shape)
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
- https://stackoverflow.com/questions/66768560/questions-about-svd-singular-value-decomposition
