
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
```
