# Feedback Baseline - Riken Dataset (JAIST)

## Dataset
Private / Feedback Dataset

## Pre-process
```python
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os 
import re

# for data cleaning
import string

# for calculating Polarity and Subjectivity
from textblob import TextBlob

# import all the necessary libraries
import warnings

#for Tokenization
import nltk

#for Wordscloud
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import sent_tokenize, word_tokenize

#Ignoring unnecessory warnings
warnings.filterwarnings("ignore")                   

# for stopwords Removal
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# for removing accented and special chracters
import plotly.express as px
import unicodedata
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier              #for data manipulation and analysis 
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler , LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix , accuracy_score , f1_score , classification_report , roc_curve , auc , roc_auc_score , zero_one_loss
from sklearn.linear_model import LinearRegression

# Read multiple input files
file_list = []
def getTrainData(dir_path):
    f_l = []
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            f_l.append(dir_path + '/' + path)
    return f_l
file_list = getTrainData("../input/readability/Y14")
file_list.extend(getTrainData("../input/readability/Y15"))
             
# Read multiple JSON inputs
dfs = []
for file in file_list:
    data = pd.read_json(file)
    dfs.append(data) 
train = pd.concat(dfs, ignore_index=True) 

# Read test data
test = pd.read_json('../input/readability/Y15_2-3_2_4-test.json')
train['length'] = train['mecab'].apply(len)
```

## Bag of words
```python
# Creating bag of words
import lightgbm as lgb
import xgboost as xgb
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

cv = CountVectorizer(max_features=30000)

X = cv.fit_transform(train['mecab']).toarray()
y = train.score

# Feature Scaling
sc = StandardScaler()
X = sc.fit_transform(X)

# Splitting the dataset into the Training set and Test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

dic_models = {'RandomForestRegressor' : RandomForestRegressor(criterion='mse'), 'LightGBM' : lgb.LGBMRegressor(), 'XGradientBoosting' : xgb.XGBRegressor()}
    
for i in dic_models:
    print('Training with ' + i + ' model. \n')
    
    model = dic_models[i].fit(X_train , y_train)
    
    #Predicting
    print('Predicting with ' + i + ' model. \n')
    pred = model.predict(X_test)
    
    # Using Accuracy Score for predicting models
    print("Accuracy of " + i + " Model is ", model.score(X_test , y_test))
    print("RMSE of " + i + " Model is ", np.sqrt(mean_squared_error(y_test , pred)))    
    print("------------------------------------------------------------------")
    print()

#Fitting Linear Regression to the data set
lin_reg = LinearRegression()
lin_reg.fit(X_train,y_train)

#Calculating Details
print('LogisticRegressionModel Train Score is : ' , lin_reg .score(X_train, y_train))
print('LogisticRegressionModel Test Score is : ' , lin_reg .score(X_test, y_test))
```

## TFIDF
```python
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_vectorizer = TfidfVectorizer()

# TF-IDF feature matrix
tfidf = tfidf_vectorizer.fit_transform(train['mecab'] )
matrix = pd.DataFrame(tfidf.toarray())
X = tfidf
y = train.score
X_train_tfidf, X_test_tfidf, y_train, y_test = train_test_split(X, y,random_state=42, test_size=0.25)

print("Training split input- ", X_train_tfidf.shape)
print("Testing split input- ", X_test_tfidf.shape)

print("\n\nY : Training split input- ", y_train.shape)
print("Y : Testing split input- ", y_test.shape)

models_2 = { 'GradientBoosting' : GradientBoostingRegressor() ,    
              'LightGBM' : lgb.LGBMRegressor(),
              'XGradientBoosting' : xgb.XGBRegressor()        
            }

for i in models_2:
    print('Training with ' + i + ' model. \n')
    
    model = models_2[i].fit(X_train_tfidf , y_train)
    
    #Predicting
    print('Predicting with ' + i + ' model. \n')
    pred = model.predict(X_test_tfidf)
    
    # Using Accuracy Score for predicting models
    print("R2 score of " + i + " Model is ", model.score(X_test_tfidf , y_test))
    print("RMSE of " + i + " Model is ", np.sqrt(mean_squared_error(y_test , pred)))    
    print("------------------------------------------------------------------")
    print()

#Fitting Linear Regression to the data set
lin_reg = LinearRegression()
lin_reg.fit(X_train_tfidf,y_train)

pred = lin_reg.predict(X_test_tfidf)

#Calculating Details
print('LogisticRegressionModel Train Score is : ' , lin_reg .score(X_train_tfidf, y_train))
print('LogisticRegressionModel Test Score is : ' , lin_reg .score(X_test_tfidf, y_test))
print("RMSE of LOGREGModel is ", np.sqrt(mean_squared_error(y_test , pred)))
```

