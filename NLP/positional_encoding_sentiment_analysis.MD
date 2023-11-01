# Positional Encoding for Sentiment Analysis

![image](https://github.com/hughiephan/DPL/assets/16631121/1ce73c5f-ef72-4cec-894e-087fae9fec14)

## Step 1: Import libraries
```python
import pickle
import warnings 
warnings.filterwarnings('ignore')
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
tfds.disable_progress_bar()
```

## Step 2: Define variables
Our model can process up to 10.000 distinct words. A sentence will have maximum of 120 words, and each word will be represented by a 516 dimension vector.
```python
vocab_size = 10000
embedding_dim= 516
sequence_len = 120
```

## Step 3: Pre-process
```python
imdb = tfds.load("imdb_reviews", as_supervised=True)
train_data, test_data = imdb['train'], imdb['test']
training_sentences = []
training_labels = []
testing_sentences = []
testing_labels = []
for s,l in train_data:
    training_sentences.append(str(s.numpy()))
    training_labels.append(l.numpy())
for s,l in test_data:
    testing_sentences.append(str(s.numpy()))
    testing_labels.append(l.numpy())
training_labels_final = np.array(training_labels)
testing_labels_final = np.array(testing_labels)
tokenizer = Tokenizer(num_words = vocab_size, oov_token="")
tokenizer.fit_on_texts(training_sentences)
sequences = tokenizer.texts_to_sequences(training_sentences)
padded = pad_sequences(sequences, maxlen=sequence_len, truncating='post')
testing_sequences = tokenizer.texts_to_sequences(testing_sentences)
testing_padded = pad_sequences(testing_sequences, maxlen=sequence_len)
```

## Step 4: Build postional encoding from scratch
```python
def positional_encoding(sequence_len, embedding_dim):
    P = np.zeros((sequence_len, embedding_dim))
    for k in range(sequence_len):
        for i in range(int(embedding_dim/2)):
            denominator = np.power(10000, 2*i/embedding_dim)
            P[k, 2*i] = np.sin(k/denominator)
            P[k, 2*i+1] = np.cos(k/denominator)
    return P

cax = plt.matshow(positional_encoding(sequence_len, embedding_dim))
plt.gcf().colorbar(cax)
```

With `P = np.zeros((120, 516))`, we have:

![image](https://github.com/hughiephan/DPL/assets/16631121/635d4e15-a87a-45cf-a55a-9c9fa0e0d8c6)

Loop through `k and i`, we notice that for `i` we loop until it reach half of the embedding dimension, which is 258

![image](https://github.com/hughiephan/DPL/assets/16631121/a1febfff-b77c-426f-98a5-d37cd1076d43)

For each position, we just add a new value based on sin and cos. Even dimension `P[k, 2*i]` will be assigned with value of sin `np.sin(k/denominator)`, and odd dimension `P[k, 2*i+1]` will be assigned with value of cos `np.cos(k/denominator)`. Let this run for a while, and we will get

![image](https://github.com/hughiephan/DPL/assets/16631121/f1cfb8aa-9ca7-4a3d-84ee-b59a5836e832)

And finally, we get the whole postional encoding.

![image](https://github.com/hughiephan/DPL/assets/16631121/d8d399c3-9beb-4236-9129-5a245de36f12)

## Step 5: Positional Encoding Layer
```python
class PositionalEncoding(tf.keras.layers.Layer):
    def __init__(self, sequence_len, embedding_dim, **kwargs):
        super(PositionalEncoding, self).__init__(**kwargs)
        self.positional_encoding = positional_encoding(sequence_len, embedding_dim)     
    def call(self, inputs):
        return inputs + self.positional_encoding
```

Example Embedding of the sentence "This was an absolutely terrible movie. Don't be lured in by Christopher Walken or Michael Ironside. Both are great actors, but this must simply be their worst role in history. Even their great acting could not redeem this movie's ridiculous storyline" 

![image](https://github.com/hughiephan/DPL/assets/16631121/3900093f-f6cd-4abc-84ef-a8bd7d33e16a)

Our goal is to combine the Embedding with our Positional Encoding

![image](https://github.com/hughiephan/DPL/assets/16631121/fca01039-3f67-40d4-a353-2fa4cf142b85)

# Step 6: Add Positional Encoding Layer to our model
```
input_layer = tf.keras.layers.Input(shape=(sequence_len,))
output = tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=sequence_len)(input_layer)
output = PositionalEncoding(sequence_len, embedding_dim)(output)
output = tf.keras.layers.Flatten()(output)
output = tf.keras.layers.Dense(64, activation='relu')(output)
output = tf.keras.layers.Dense(10, activation='relu')(output)
output = tf.keras.layers.Dense(1, activation='sigmoid')(output)
model = tf.keras.Model(inputs=input_layer, outputs=output)
model.summary()
```

![image](https://github.com/hughiephan/DPL/assets/16631121/2c139e34-3415-4798-b0c1-002bfee92d88)

## Step 7: Train
```python
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(padded, training_labels_final, epochs=1, validation_data = (testing_padded, testing_labels_final))
```

![image](https://github.com/hughiephan/DPL/assets/16631121/7cacc1ee-7b5e-4309-b0bd-52dfdeba0dd6)

## Step 8: Make predictions
```python
sentences = [
    "This was an absolutely terrible movie. Don't be lured in by Christopher Walken or Michael Ironside. Both are great actors, but this must simply be their worst role in history. Even their great acting could not redeem this movie's ridiculous storyline",
    "Wonderful performances from Cher and Nicolas Cage (as always) gently row the plot along. There are no rapids to cross, no dangerous waters, just a warm and witty paddle through New York life at its best."
]

for sentence in sentences:
    input_sequence = tokenizer.texts_to_sequences([sentence])
    input_padded = pad_sequences(input_sequence, maxlen=sequence_len)
    prediction = model.predict(input_padded)
    print(sentence)
    print("Prediction ", prediction[0][0])
    if prediction[0][0] >= 0.5:
        print("The review is positive. \n")
    else:
        print("The review is negative. \n")
```

![image](https://github.com/hughiephan/DPL/assets/16631121/ce0804af-ab03-4787-9c1f-01e1a443a53f)

## Reference
- https://machinelearningmastery.com/a-gentle-introduction-to-positional-encoding-in-transformer-models-part-1
- https://vaclavkosar.com/ml/transformer-positional-embeddings-and-encodings
