# Transformer Block

```python
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_datasets as tfds
import warnings 
warnings.filterwarnings('ignore')
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras_nlp.layers import TokenAndPositionEmbedding
tfds.disable_progress_bar()
```

```python
vocab_size = 10000
embedding_dim= 516
sequence_len = 120
num_heads = 1  # Number of attention heads
ff_dim = 32  # Hidden layer size in feed forward network inside transformer
```

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
```

```python
tokenizer = Tokenizer(num_words = vocab_size, oov_token="")
tokenizer.fit_on_texts(training_sentences)
sequences = tokenizer.texts_to_sequences(training_sentences)
padded = pad_sequences(sequences, maxlen=sequence_len, truncating='post')
testing_sequences = tokenizer.texts_to_sequences(testing_sentences)
testing_padded = pad_sequences(testing_sequences, maxlen=sequence_len)
```

```python
class TransformerBlock(layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, rate=0.1):
        super().__init__()
        self.att = layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.ffn = keras.Sequential(
            [layers.Dense(ff_dim, activation="relu"), layers.Dense(embed_dim),]
        )
        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = layers.Dropout(rate)
        self.dropout2 = layers.Dropout(rate)

    def call(self, inputs, training):
        attn_output = self.att(inputs, inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)
```

```python
input_layer = tf.keras.layers.Input(shape=(sequence_len,))
output = TokenAndPositionEmbedding(vocabulary_size=vocab_size, sequence_length=sequence_len, embedding_dim=embedding_dim)(input_layer)
output = TransformerBlock(embedding_dim, num_heads, ff_dim)(output)
output = tf.keras.layers.Flatten()(output)
output = tf.keras.layers.Dense(64, activation='relu')(output)
output = tf.keras.layers.Dense(10, activation='relu')(output)
output = tf.keras.layers.Dense(1, activation='sigmoid')(output)
model = tf.keras.Model(inputs=input_layer, outputs=output)
model.summary()
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(padded, training_labels_final, epochs=5, validation_data = (testing_padded, testing_labels_final))
```

![image](https://github.com/hughiephan/DPL/assets/16631121/77a2bb1c-aaf3-42c9-bdd6-55fd08a9c2d6)

