
## Step 1: Import libraries
```python
import numpy as np
import pandas as pd
import shap
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
```

## Step 2:

Create object that can calculate shap values
```python
explainer = shap.TreeExplainer(my_model)
```

## Step 3:

Calculate shap_values for all of val_X rather than a single row, to have more data for plot.  Index of [1] is explained in text below.

```python
shap_values = explainer.shap_values(val_X)
shap.summary_plot(shap_values[1], val_X)
```

## Step 4:
```python
shap_values = explainer.shap_values(X)
shap.dependence_plot('Ball Possession %', shap_values[1], X, interaction_index="Goal Scored")
```
