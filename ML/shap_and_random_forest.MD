
## Step 1: Import libraries
```python
import numpy as np
import pandas as pd
import shap
import graphviz
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
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
feature_names = [i for i in data.columns if data[i].dtype in [np.int64]]
X = data[feature_names]
train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)
```

## Step 4: Training with Random Forest
```python
model = DecisionTreeClassifier(random_state=0, max_depth=6, min_samples_split=2).fit(train_X, train_y)
```

## Step 5:

![image](https://github.com/hughiephan/DPL/assets/16631121/5b01aeee-8271-4504-85cc-675bf2a51a94)

```python
tree_graph = tree.export_graphviz(model, out_file=None, feature_names=feature_names)
graphviz.Source(tree_graph)
```

## Step 5:

Create object that can calculate shap values
```python
explainer = shap.TreeExplainer(model)
```

## Step 6:

Calculate shap_values for all of val_X rather than a single row, to have more data for plot.  Index of [1] is explained in text below.

![image](https://github.com/hughiephan/DPL/assets/16631121/37f0b077-1a53-4b71-83e2-c1fa00191511)

```python
shap_values = explainer.shap_values(val_X)
shap.summary_plot(shap_values[1], val_X)
```

## Step 7:

![image](https://github.com/hughiephan/DPL/assets/16631121/9bb09887-d09a-4ebd-8340-431868532142)

```python
shap_values = explainer.shap_values(X)
shap.dependence_plot('Ball Possession %', shap_values[1], X, interaction_index="Goal Scored")
```

## Reference
- https://www.kaggle.com/code/dansbecker/advanced-uses-of-shap-values/tutorial
- https://www.kaggle.com/code/dansbecker/partial-plots
