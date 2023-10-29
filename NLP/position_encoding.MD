
# Step
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
tokenizer = Tokenizer(num_words = 10000, oov_token="")
tokenizer.fit_on_texts(training_sentences)
sequences = tokenizer.texts_to_sequences(training_sentences)
padded = pad_sequences(sequences, maxlen=120, truncating='post')
testing_sequences = tokenizer.texts_to_sequences(testing_sentences)
testing_padded = pad_sequences(testing_sequences, maxlen=120)
vocab_size = 10000
embedding_dim= 16
```

## Step

```python
def positional_encoding(seq_length, embedding_dim):
    P = np.zeros((seq_length, embedding_dim))
    for k in range(seq_length):
        for i in range(int(embedding_dim/2)):
            denominator = np.power(10000, 2*i/embedding_dim)
            P[k, 2*i] = np.sin(k/denominator)
            P[k, 2*i+1] = np.cos(k/denominator)
    return P

P = positional_encoding(seq_length=120, embedding_dim=516)
cax = plt.matshow(P)
plt.gcf().colorbar(cax)
```

## Step: 

```python
class PositionalEncoding(tf.keras.layers.Layer):
    def __init__(self, max_seq_length, embedding_dim, **kwargs):
        super(PositionalEncoding, self).__init__(**kwargs)
        self.positional_encoding = positional_encoding(max_seq_length, embedding_dim)
                
    def call(self, inputs):
        return inputs + self.positional_encoding

input_layer = tf.keras.layers.Input(shape=(120,))
output = tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=120)(input_layer)
output = PositionalEncoding(120, embedding_dim)(output)
output = tf.keras.layers.Flatten()(output)
output = tf.keras.layers.Dense(64, activation='relu')(output)
output = tf.keras.layers.Dense(10, activation='relu')(output)
output = tf.keras.layers.Dense(1, activation='sigmoid')(output)
model = tf.keras.Model(inputs=input_layer, outputs=output)
model.summary()
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(padded, training_labels_final, epochs=5, validation_data = (testing_padded, testing_labels_final))
```

## Step:

```python
sentences = [
    "This was an absolutely terrible movie. Don't be lured in by Christopher Walken or Michael Ironside. Both are great actors, but this must simply be their worst role in history. Even their great acting could not redeem this movie's ridiculous storyline",
    "Wonderful performances from Cher and Nicolas Cage (as always) gently row the plot along. There are no rapids to cross, no dangerous waters, just a warm and witty paddle through New York life at its best."
]

for sentence in sentences:
    input_sequence = tokenizer.texts_to_sequences([sentence])
    input_padded = pad_sequences(input_sequence, maxlen=120)
    prediction = model.predict(input_padded)
    print(sentence)
    print("Prediction ", prediction[0][0])
    if prediction[0][0] >= 0.5:
        print("The review is positive. \n")
    else:
        print("The review is negative. \n")
```

## Reference
- https://machinelearningmastery.com/a-gentle-introduction-to-positional-encoding-in-transformer-models-part-1/
