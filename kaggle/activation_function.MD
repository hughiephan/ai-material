# Activation Function

```python
import numpy as np
x = np.array([-3, -2, -1, 1, 2, 3])
print("Sigmoid ", 1 / (1 + np.exp(-x)))
print("Tanh ", np.tanh(x))
print("ReLU ", np.maximum(x,0))
```
