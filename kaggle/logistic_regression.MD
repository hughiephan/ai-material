# Logistic Regression

## Import libraries and prepare data

Sklearn provides us with a Logistic Regression model out of the box

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
data = {'Hours': [0.5, 0.75, 1, 1.25, 1.5, 1.75, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 4, 4.25, 4.5, 4.75, 5, 5.5],
        'Pass': [0, 0, 0, 0 ,0, 0, 1, 0, 1, 0, 1,0, 1,0, 1,1,1,1,1,1]}
df = pd.DataFrame(data)
```

## Make Prediction
Run model.fit to make prediction based on df[['Hours']] data. Logistic Regression will try to predict the df[['Pass']] without us providing any hint.

```python
model = LogisticRegression()
model.fit(df[['Hours']], df['Pass'])
binary_predictions = model.predict(df[['Hours']])
print("Pass prediction based on Hours: ", binary_predictions)
```

## Metrics
The prediction accuracy is 80%, with 5 missed prediction data points. We use np.where to find the indices where the Pass Prediction and the Pass Actual Data is different. The incorrect predictions are at: 6,8,11,13

```python
accuracy = accuracy_score(df['Pass'], binary_predictions)
incorrect_indices = np.where(df['Pass'] != binary_predictions)
print("Incorrect predictions:")
print(df.iloc[incorrect_indices])
print("Accuracy ", accuracy)
```

## Plot
To plot the logistic regression line and the data scatter points, we can use the sns seaborn library. In order to plot the incorrect prediction 6,8,11,13, we need to first combine the predictions and the original dataframe, then use the Prediction column as the hue.

```python
prediction_df = pd.DataFrame({'Prediction': binary_predictions})
result = pd.concat([df, prediction_df], axis=1)
print("Combination of orignal and prediction dataframe \n", result)
palette = {0: 'red', 1: 'blue'}
graph = sns.lmplot(x='Hours', y='Pass', hue='Prediction', data=result, fit_reg=False, palette=palette)
sns.regplot(x='Hours', y='Pass', data=result, scatter=False, ax=graph.axes[0, 0], logistic=True)
```
