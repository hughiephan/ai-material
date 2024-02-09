# Linear Discriminant Analysis 

![image](https://github.com/hughiephan/DPL/assets/16631121/f2360acb-3f2a-45d2-a328-4c69bbcc42af)

## Step 1: Import libraries
```python
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import classification_report
```

## Step 2: Dataset
```python
mnist = fetch_openml('mnist_784')
X, y = mnist['data'], mnist['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

## Step 3: Model
```python
lda = LinearDiscriminantAnalysis(n_components=2)
X_train_lda = lda.fit_transform(X_train, y_train)
X_test_lda = lda.transform(X_test)
```

## Step 4: Predict
```python
y_pred = lda.predict(X_test)
accuracy = sum(y_pred == y_test) / len(y_test)
print("Test set accuracy: ", accuracy)
```

## Step 5: Report
```python
print(classification_report(y_test, y_pred))
```

## Reference
- https://levelup.gitconnected.com/exploring-the-mnist-dataset-using-linear-discriminant-analysis-lda-7f0d025f4ce4
