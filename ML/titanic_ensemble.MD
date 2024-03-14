# Titanic Disaster with Ensemble Learning



## Step 1: Import libraries
```python
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import sklearn
import keras
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
train_df = pd.read_csv("../input/titanic-disaster/train.csv")
X = train_df.drop(['Survived'], 1)
Y = train_df['Survived']
```

## Step 3: Feature engineering
```python
X['Embarked'].fillna('C', inplace=True)

# We replace missing ages by the mean age of passengers who belong to the same group of class/sex/family
X['Age'] = X.groupby(['Pclass','Sex','Parch','SibSp'])['Age'].transform(lambda x: x.fillna(x.mean()))
X['Age'] = X.groupby(['Pclass','Sex','Parch'])['Age'].transform(lambda x: x.fillna(x.mean()))
X['Age'] = X.groupby(['Pclass','Sex'])['Age'].transform(lambda x: x.fillna(x.mean()))

# We replace the only missing fare value for test dataset and the missing values of the cabin column
X['Fare'] = X['Fare'].interpolate()
X['Cabin'].fillna('U', inplace=True)

# Create a Title column from name column
X['Title'] = pd.Series((name.split('.')[0].split(',')[1].strip() for name in X['Name']), index=X.index)
X['Title'] = X['Title'].replace(['Lady', 'the Countess','Countess','Capt', 'Col','Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
X['Title'] = X['Title'].replace(['Mlle', 'Ms'], 'Miss')
X['Title'] = X['Title'].replace('Mme', 'Mrs')
X['Title'] = X['Title'].map({"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Rare": 5})

# Filling Age missing values with mean age of passengers who have the same title
X['Age'] = X.groupby(['Title'])['Age'].transform(lambda x: x.fillna(x.mean()))

# Transform categorical variables to numeric variables
X['Sex'] = X['Sex'].map({'male': 0, 'female': 1})
X['Embarked'] = X['Embarked'].map({'S': 0, 'C': 1, 'Q': 2})

# Create a Family Size, Is Alone, Child and Mother columns
X['FamillySize'] = X['SibSp'] + X['Parch'] + 1
X['FamillySize'][X['FamillySize'].between(1, 5, inclusive=False)] = 2
X['FamillySize'][X['FamillySize']>5] = 3
X['IsAlone'] = np.where(X['FamillySize']!=1, 0, 1)
X['IsChild'] = X['Age'] < 18
X['IsChild'] = X['IsChild'].astype(int)

# Modification of cabin column to keep only the letter contained corresponding to the deck of the boat
X['Cabin'] = X['Cabin'].str[:1]
X['Cabin'] = X['Cabin'].map({cabin: p for p, cabin in enumerate(set(cab for cab in X['Cabin']))})

# Create a ticket survivor column which is set to 1 if an other passenger with the same ticket survived and 0 else
X['TicketSurvivor'] = pd.Series(0, index=X.index)
tickets = X['Ticket'].value_counts().to_dict()
for t, occ in tickets.items():
    if occ != 1:
        table = X['Survived'][X['Ticket'] == t]
        if sum(table) != 0:
            X['TicketSurvivor'][X['Ticket'] == t] = 1

# These two columns are not useful anymore
X = X.drop(['Name', 'Ticket', 'PassengerId'], 1)
```

## Step 4: Scaling and split
```python
sc = StandardScaler()
X = pd.DataFrame(sc.fit_transform(X.values), index=X.index, columns=X.columns)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
```

## Step 5: Model
```python
def build_ann():
    ann = Sequential()
    ann.add(Dense(units=32, activation='relu', input_shape=(13,)))
    ann.add(Dense(units=64, activation='relu'))
    ann.add(Dropout(rate=0.5))
    ann.add(Dense(units=64, activation='relu'))
    ann.add(Dropout(rate=0.5))
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
