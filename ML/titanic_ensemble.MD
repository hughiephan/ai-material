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
from keras.layers import Dense
```

## Step 2: Data

Download dataset from `https://www.kaggle.com/competitions/titanic/data`

```python
train_df = pd.read_csv("/kaggle/input/titanic/train.csv")
X = train_df.drop(['Survived'], axis=1)
Y = train_df['Survived']
```

![image](https://github.com/hughiephan/DPL/assets/16631121/6f4c6fcb-5cce-4740-9556-573678446770)

## Step 3: Fill missing values

`inplace=True` parameter ensures that the changes are made directly instead of this `X['...'] = X['...'].fillna(...)`

```python
X['Embarked'].fillna('C', inplace=True)
X['Age'].fillna(X['Age'].mean(), inplace=True)
X['Fare'].interpolate(inplace=True)
```

![image](https://github.com/hughiephan/DPL/assets/16631121/87a8e44e-ac1d-4236-bc6d-b064ab686ee7)

## Step 4: Encoding
```python
X['Sex'] = X['Sex'].map({'male': 0, 'female': 1})
X['Embarked'] = X['Embarked'].map({'S': 0, 'C': 1, 'Q': 2})
```

![image](https://github.com/hughiephan/DPL/assets/16631121/c12e7039-4341-4454-ae64-53bedf75e57c)

## Step 5: Scaling and split
```python
sc = StandardScaler()
X = X.drop(['Name', 'Ticket', 'Cabin'], axis=1)
X = pd.DataFrame(sc.fit_transform(X.values), index=X.index, columns=X.columns)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
```

## Step 6: Neural network
```python
def build_ann():
    ann = Sequential()
    ann.add(Dense(units=32, activation='relu', input_shape=(8,)))
    ann.add(Dense(units=64, activation='relu'))
    ann.add(Dense(units=1, activation='sigmoid'))
    ann.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return ann
```

## Step 6: Ensemble classifier

![image](https://github.com/hughiephan/DPL/assets/16631121/2819e4a8-3ca7-4f5f-bbe6-420035a38099)

`(pred_ann > 0.5)*1` compares each element in the prediction array with 0.5. If the values are greater than 0.5 are classified as `1` (Survived), and values less than or equal to 0.5 are classified as `0` (Dead). If the combination of both `ann`, `rf`, and `svm` is larger than 2, it means that atleast 2 classfiers agree that the passenger survive, otherwise classify them as dead.

```python
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

Train our EnsembleClassifier by using `model.fit` and call `model.predict` to get the prediction on the test set. Finally, compare the prediction of our classifier on the test set and actual label `Y_test` to get the accuracy.

```python
model = EnsembleClassifier()
model.fit(X, Y)
prediction = model.predict(X_test)
score = metrics.accuracy_score(Y_test, prediction)
print("Accuracy:", score)
```

![image](https://github.com/hughiephan/DPL/assets/16631121/020abd22-fcf7-43cc-bc5f-02ed1d6015af)
