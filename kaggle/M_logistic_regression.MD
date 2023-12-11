# Logistic Regression

## Introduction
This notebook explores logistic regression to predict student pass/fail outcomes based on study hours. We start with preparing the data and training the logistic regression model to make predictions solely from the hours studied. Then evaluates the model's accuracy and identifies points where predictions differ from actual outcomes. Additionally, we will visualize the regression line and scatter points using seaborn, distinguishing correct and incorrect predictions.

If you're interested in exploring similar data analysis or learning more about AI applications, then checkout my personal website https://hughiephan.co . Don't forget to upvote if you found the notebook insightful or helpful. Your feedback is valuable and can help others discover useful content.

## Import libraries

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
```

## Load data
Create a Pandas DataFrame using study hours and pass/fail data for students, setting the stage to explore the potential relationship between study hours and exam outcomes using logistic regression.

```python
data = {'Hours': [0.5, 0.75, 1, 1.25, 1.5, 1.75, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 4, 4.25, 4.5, 4.75, 5, 5.5],
        'Pass': [0, 0, 0, 0 ,0, 0, 1, 0, 1, 0, 1,0, 1,0, 1,1,1,1,1,1]}
df = pd.DataFrame(data)
```python

## Model
Builds a logistic regression model using the 'Hours' column from the DataFrame to predict 'Pass' outcomes. Then generates predictions based on study hours and displays these predictions indicating pass or fail for each corresponding hour value.

```python
model = LogisticRegression()
model.fit(df[['Hours']], df['Pass'])
binary_predictions = model.predict(df[['Hours']])
print("Pass prediction based on Hours: ", binary_predictions)
```

## Evaluate
Evaluates the accuracy of the logistic regression model by comparing the predicted 'Pass' outcomes with the actual 'Pass' values in the DataFrame. Then calculatee the accuracy score and identifies incorrect predictions, displaying the corresponding rows and the overall accuracy of the model.

```python
accuracy = accuracy_score(df['Pass'], binary_predictions)
incorrect_indices = np.where(df['Pass'] != binary_predictions)
print("Incorrect predictions:")
print(df.iloc[incorrect_indices])
print("Accuracy ", accuracy)
```
