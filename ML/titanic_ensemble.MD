# Titanic Disaster with Ensemble Learning



## Step 1: Import libraries
```python
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import keras
import sklearn
from sklearn import metrics
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout
```

## Step 2: Data

Download dataset from `https://www.kaggle.com/competitions/titanic/data`

```python
train_df = pd.read_csv("/kaggle/input/titanic/train.csv")
X = train_df.drop(['Survived'], axis=1)
Y = train_df['Survived']
```

## Step 3: Fill missing values
```python
X['Embarked'].fillna('C', inplace=True)
X['Age'] = X.groupby(['Pclass','Sex','Parch','SibSp'])['Age'].transform(lambda x: x.fillna(x.mean()))
X['Age'] = X.groupby(['Pclass','Sex','Parch'])['Age'].transform(lambda x: x.fillna(x.mean()))
X['Age'] = X.groupby(['Pclass','Sex'])['Age'].transform(lambda x: x.fillna(x.mean()))
X['Cabin'].fillna('U', inplace=True)
X['Fare'] = X['Fare'].interpolate()
```

## Step 4: Map
```python
X['Sex'] = X['Sex'].map({'male': 0, 'female': 1})
X['Embarked'] = X['Embarked'].map({'S': 0, 'C': 1, 'Q': 2})
```

## Step 5: Scaling and split
```python
sc = StandardScaler()
X = X.drop(['Name', 'Ticket', 'Cabin'], axis=1)
X = pd.DataFrame(sc.fit_transform(X.values), index=X.index, columns=X.columns)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
```

## Step 6: Model
```python
def build_ann():
    ann = Sequential()
    ann.add(Dense(units=32, activation='relu', input_shape=(8,)))
    ann.add(Dense(units=64, activation='relu'))
    ann.add(Dense(units=1, activation='sigmoid'))
    ann.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return ann

class EnsembleClassifier:
    def __init__(self, verbose=True):
        self.ann = build_ann()
        self.rf = RandomForestClassifier(n_estimators=30, max_depth=10, random_state=42)
        self.svm = SVC(random_state=42)
    def fit(self, X, y):
        self.ann.fit(X, y, epochs=2, batch_size=16, verbose=0)
        self.rf.fit(X, y)
        self.svm.fit(X, y)
    def predict(self, X):
        """
        If more than 2 classifiers make the same prediction, then trust that prediction. With: 0 is survived, 1 is dead
        Example:
             1 1 1: all classifiers say survived => survived
             1 0 1: two classfiers say survived => survived
             0 1 1: two classfiers say survived => survived
             1 0 0: two classfiers say dead => dead
             0 0 0: all classfiers say dead => dead
        """
        predictions = list()
        pred_ann = self.ann.predict(X)
        pred_ann = (pred_ann > 0.5)*1
        pred_rf = self.rf.predict(X)
        pred_svm = self.svm.predict(X)
        for n in range(len(pred_ann)):
            combined = pred_ann[n] + pred_rf[n] + pred_svm[n] 
            if combined >= 2: 
                p = 1
            else:
                p = 0
            predictions.append(p)
        return predictions
```

## Step 6: Training
```python
model = EnsembleClassifier()
model.fit(X, Y)
prediction = model.predict(X_test)
score = metrics.accuracy_score(Y_test, prediction)
print("Accuracy:", score)
```
