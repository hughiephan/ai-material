# Classifying Insincere Questions with NLTK

## Step 1: Import libraries
```python
import numpy as np 
import pandas as pd 
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import word_tokenize 
```

## Step 2: Import Dataset
Our dataset is from the Quora Kaggle competition, where we have to develop models that identify and flag insincere questions https://www.kaggle.com/competitions/quora-insincere-questions-classification
```python
train = pd.read_csv("/kaggle/input/quora-insincere-questions-classification/train.csv")
train = train[0:100]
```

## Step 3: Pre-process
```python
eng_stopwords = set(stopwords.words("english"))
def pre_process(train):
    train['question_text'] = train["question_text"].apply(lambda x: " ".join(word_tokenize(str(x)))) # Tokenize
    train['question_text'] = train["question_text"].apply(lambda x: x.translate(str.maketrans('','',string.punctuation))) # Remove punctuation
    train["question_text"] = train["question_text"].apply(lambda x: " ".join([w for w in str(x).lower().split() if not w in eng_stopwords])) # Remove stopwords in the text
    return train
```

## Step 4: Train
```python
all_words = set(word.lower() for passage in train for word in word_tokenize(passage[0]))
tr = [({word: (word in word_tokenize(x[0])) for word in all_words}, x[1]) for x in train]
classifier = NaiveBayesClassifier.train(tr)
nltk.classify.accuracy(classifier, tr)
```

## Step 5: Make a prediction
```python
classifier.classify(xtest)
```

## References
- Kaggle Notebook from SHUBH24 (Wordnet Similarity Matrix)
