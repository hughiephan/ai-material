# Lab: Hyperparameter Tuning

## Question
Implement a hyperparameter tuner for a Neural Network

## Requirement
Use ONE Tuner from this list: Random Search, Keras Tuner, Bayesian Optimisation, Evolutionary Algorithms, Gradient-Based Optimisation, Population-based Optimisation, ParamILS

Using at least THREE Hyperparameters of your choice: Learning Rate, Loss Function, Layer Size, Layer Params, Weight Initialization, Weight of Regularization, Model Depth, Optimizer, Optimizer Params, Batch Size...

You can train it on any Neural Network and Dataset of your choice

## Scoring Criteria
You will be graded based on:

Originality of your implementation: Did you implement anything new in the model or just re-use it? How much work did you put into implementing your model? Can your model work well on complex dataset and problem?

Result of your implementation: Accuracy, Loss, Cross-validation

Q/A to test your understanding: How well do you understand your code? How well do you understand Neural Network concepts?

Note: DO NOT add comments in your code

## Example Submission
```python
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import load_iris # Read more about IRIS Dataset here https://www.kaggle.com/code/kostasmar/exploring-the-iris-data-set-scikit-learn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.wrappers.scikit_learn import KerasClassifier
import pandas as pd
iris = load_iris() 
X = iris.data
y = iris.target
label_binarizer = LabelBinarizer()
y = label_binarizer.fit_transform(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
def create_model(optimizer, hidden_units, dropout_rate):
    model = Sequential()
    model.add(Dense(hidden_units, input_dim=4, activation='relu'))
    model.add(Dropout(dropout_rate))
    model.add(Dense(3, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    return model
model = KerasClassifier(build_fn=create_model, verbose=0)
param_grid = {
    'optimizer': ['adam', 'rmsprop'],
    'hidden_units': [8, 16, 32],
    'dropout_rate': [0.0, 0.1, 0.2],
}
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3)
grid_search.fit(X_train, y_train)
results = pd.DataFrame(grid_search.cv_results_)
mean_test_scores = results.pivot_table(values='mean_test_score',
                                       index='param_hidden_units',
                                       columns=['param_optimizer', 'param_dropout_rate'])
plt.figure(figsize=(12, 6))
sns.heatmap(mean_test_scores, annot=True, cmap='YlGnBu')
plt.title("Grid Search Results")
plt.xlabel("Optimizer, Dropout Rate")
plt.ylabel("Hidden Units")
plt.show()
```

![image](https://github.com/hughiephan/DPL/assets/16631121/c3f9ee82-38a4-4798-b4c0-be50cbef63df)
