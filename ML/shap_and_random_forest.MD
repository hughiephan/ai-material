
## Step 1: Import libraries
```python
import numpy as np
import pandas as pd
import shap
import graphviz
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
```

## Step 2:

Download the dataset from: https://www.kaggle.com/datasets/mathan/fifa-2018-match-statistics

```python
data = pd.read_csv('/kaggle/input/fifa-2018-match-statistics/FIFA 2018 Statistics.csv')
```

## Step 3: Pre-process data
```python
y = (data['Man of the Match'] == "Yes")  # Convert from string "Yes"/"No" to binary
feature_names = [i for i in data.columns if data[i].dtype in [np.int64, np.int64]]
X = data[feature_names]
train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)
```

## Step 4: Training with Random Forest
```python
my_model = RandomForestClassifier(random_state=0).fit(train_X, train_y)
```

## Step 5:
```python
tree_graph = tree.export_graphviz(my_model, out_file=None, feature_names=feature_names)
graphviz.Source(tree_graph)
```

## Step 5:

Create object that can calculate shap values
```python
explainer = shap.TreeExplainer(my_model)
```

## Step 6:

Calculate shap_values for all of val_X rather than a single row, to have more data for plot.  Index of [1] is explained in text below.

```python
shap_values = explainer.shap_values(val_X)
shap.summary_plot(shap_values[1], val_X)
```

## Step 7:
```python
shap_values = explainer.shap_values(X)
shap.dependence_plot('Ball Possession %', shap_values[1], X, interaction_index="Goal Scored")
```

## Reference
- https://www.kaggle.com/code/dansbecker/advanced-uses-of-shap-values/tutorial
