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

## Step 2: Import dataset
Our dataset is from the Quora Kaggle competition, where we have to develop models that identify and flag insincere questions https://www.kaggle.com/competitions/quora-insincere-questions-classification
```python
train = pd.read_csv("/kaggle/input/quora-insincere-questions-classification/train.csv")
train = train[0:100]
```

## Step 3: Pre-process
```python
eng_stopwords = set(stopwords.words("english"))
def pre_process(text):
    text = " ".join(word_tokenize(str(text))) # Tokenize
    text = text.translate(str.maketrans('', '', string.punctuation)) # Remove punctuation
    text = " ".join([w for w in str(text).lower().split() if not w in eng_stopwords]) # Remove stopwords in the text
    return text

train['question_text'] = train['question_text'].apply(pre_process)
all_words = set(word.lower() for i, row in train.iterrows() for word in word_tokenize(row['question_text']))
feature_set = [({word: (word in word_tokenize(row['question_text'])) for word in all_words}, row['target']) for i, row in train.iterrows()]
```

## Step 4: Train
```python
classifier = NaiveBayesClassifier.train(feature_set)
nltk.classify.accuracy(classifier, feature_set)
```

## Step 5: Make a prediction
```python
def predict(text):
    feature = {word: (word in word_tokenize(pre_process(text))) for word in all_words}
    return 'Sincere Question' if classifier.classify(feature) == '0' else 'Insincere Question'
    
predict("How did Quebec nationalists see their province as a nation in the 1960s?")
```

## Step 6: Build a demo
```python
demo = gr.Interface(
    fn=predict,
    inputs=["text"],
    outputs=["text"],
    title="Check question sincere or insincere?",
)

demo.queue().launch(share=True)
```

## References
- Kaggle Notebook from SHUBH24 (Wordnet Similarity Matrix)
