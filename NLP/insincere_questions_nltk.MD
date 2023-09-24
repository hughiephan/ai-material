# Classifying Insincere Questions with NLTK

![image](https://github.com/hughiephan/DPL/assets/16631121/9e311b08-1e5e-47dd-bc76-ec471c36d6c8)

## Step 1: Import libraries
```python
!pip install gradio
import numpy as np 
import pandas as pd 
import nltk
import string
import gradio as gr
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from nltk.classify import NaiveBayesClassifier
```

## Step 2: Import dataset
Our dataset is from the Quora Kaggle competition, where we have to develop models that identify and flag insincere questions https://www.kaggle.com/competitions/quora-insincere-questions-classification . We limit to 100 first rows to make our Notebook run faster.
```python
train = pd.read_csv("/kaggle/input/quora-insincere-questions-classification/train.csv")
train = train[0:100]
```

## Step 3: Pre-process
Define the pre-process with 3 functions: Lower Text, Remove Punctuation, Remove Stopwords, and then run `apply(pre_process)` to apply pre-processing to all our data rows. 

```python
eng_stopwords = set(stopwords.words("english"))
def pre_process(text):
    text = " ".join(i for i in text.lower().split()) # Lower Text
    text = text.translate(str.maketrans('', '', string.punctuation)) # Remove punctuation
    text = " ".join([w for w in str(text).lower().split() if not w in eng_stopwords]) # Remove stopwords
    return text

train['question_text'] = train['question_text'].apply(pre_process)
```

Here is what happen in our pre-proceing steps:
```
How did Quebec nationalists see their province as a nation in the 1960s? # Original Text
how did quebec nationalists see their province as a nation in the 1960s? # Lowered text
how did quebec nationalists see their province as a nation in the 1960s # Removed punctuation
quebec nationalists see province nation 1960s # Removed English stopwords
```

## Step 4: Train
NaiveBayesClassifier does not accept raw text `quebec nationalists see province nation 1960s` as input. So we need to convert all question_text into this form: `[({'nationalists': True, 'people': False, 'quebec': True, 'province': True, 'see': True, '1960s': True, 'nation': True}, 0)]`. `True` flag is for words that exist in question_text, and `False` is for words that are not. `0` is for Sincere Question, and `1` is for Insincere Question. 

`all_words` is our dictionary that contains all the words from the training dataset. So to achieve our desired `feature_set`, we just need to check which word in question_text row exists in the dictionary and set that to True.

```python
all_words = set(word.lower() for i, row in train.iterrows() for word in word_tokenize(row['question_text']))
feature_set = [({word: (word in word_tokenize(row['question_text'])) for word in all_words}, row['target']) for i, row in train.iterrows()]

classifier = NaiveBayesClassifier.train(feature_set)
nltk.classify.accuracy(classifier, feature_set)
```

## Step 5: Make a prediction
```python
def predict(text):
    feature = {word: (word in word_tokenize(pre_process(text))) for word in all_words}
    return 'Sincere question' if classifier.classify(feature) == 0 else 'Insincere question'
    
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

Interface of our demo:

![image](https://github.com/hughiephan/DPL/assets/16631121/34f56380-3a73-4071-86be-c478ab3fcc0a)

## Exercise
Run prediction on Test Dataset to see how well our model can generalize:
```
test = pd.read_csv("/kaggle/input/quora-insincere-questions-classification/test.csv")
```

## References
- https://stackoverflow.com/questions/20827741/nltk-naivebayesclassifier-training-for-sentiment-analysis
