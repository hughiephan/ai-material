# Lab Disaster Tweet

![image](https://github.com/hughiephan/DPL/assets/16631121/e5d6be87-db7c-4c50-89aa-2d9f615168cb)

## Dataset
Disaster Tweet

## Requirements
You must use a Deep Learning model

## Submission File
For each ID in the test set, you must predict 1 if the tweet is describing a real disaster, and 0 otherwise. The file should contain a header and have the following format:

```
id,target
0,0
2,0
3,1
9,0
11,0
```

## Coding
```python
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
from keras.layers import Dense, LSTM, Embedding, Activation
from keras.models import Model, Sequential
from keras.optimizers import RMSprop
from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
def encode_sentence(s):
    tokens = list(tokenizer.tokenize(s))
    tokens.append('[SEP]')
    return tokenizer.convert_tokens_to_ids(tokens)

max_len = 50
x_train = []
x_test = []
train_df = pd.read_csv('../input/dpl-disaster-tweets/train.csv')
test_df = pd.read_csv('../input/dpl-disaster-tweets/test.csv')
for tweet in train_df['text'].values:
    vec = encode_sentence(tweet)
    x_train.append(vec[:max_len] + [0] * (max_len - len(vec)))
for tweet in test_df['text'].values:
    vec = encode_sentence(tweet)
    x_test.append(vec[:max_len] + [0] * (max_len - len(vec)))
x_train = np.array(x_train)
n = np.amax(x_train)
y_train = train_df['target'].values
y_train = np.array(y_train)
```

## Training
```python
BATCH_SIZE = 32
model=Sequential()
model.add(Embedding(n + 1, BATCH_SIZE, mask_zero=True))
model.add(LSTM(BATCH_SIZE))
model.add(Dense(2, activation = 'sigmoid'))
model.compile(loss = 'sparse_categorical_crossentropy', optimizer = "RMSprop")
model.fit(x_train, y_train, epochs = 2, batch_size = BATCH_SIZE)
```

## Submit
```python
y_test = [np.argmax(model.predict(np.array([x_test_]),verbose = 0)) for x_test_ in x_test]
sub = pd.DataFrame({'id':test_df['id'].values, 'target':y_test})
sub.to_csv('submission.csv', index = False)
```
