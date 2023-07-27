# ChatBot for Review IMDB Comments

Take a sequence of characters as input and the immediate next character as the target. As long as it can predict what is the next character given what are preceding, we can run the model in a loop to generate a long piece of text

## Step: Import Neural Network and necessary librarires
```py
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
```