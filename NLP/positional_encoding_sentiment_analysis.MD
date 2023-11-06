# Positional Encoding for Sentiment Analysis

![image](https://github.com/hughiephan/DPL/assets/16631121/1ce73c5f-ef72-4cec-894e-087fae9fec14)

Transformer-based language models, such as GPT-3, are widely used in many Natural Language Processing but the attention mechanism of the transformer has no notion of order. Therefore, the order of the words must explicitly be encoded. This positional information injected into the word representations is referred to as Position Encoding.

Prerequisites: You should have prior knowledge of MLP, Embedding and Transformer

## Step 1: Import libraries
```python
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_datasets as tfds
import warnings 
warnings.filterwarnings('ignore')
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
tfds.disable_progress_bar()
```

## Step 2: Define variables
Our model can process up to 10.000 distinct words. A sentence will have maximum of 120 words, and each word will be represented by a 516 dimension vector. These numbers are hyperparameters and can be freely adjusted.
```python
vocab_size = 10000
embedding_dim= 516
sequence_len = 120
```

## Step 3: Pre-process

We use the `imdb_reviews` dataset, which is already splitted into training and testing dataset. But we will need to further split them into the features `sentences` and target `labels`. Example of a sentence "I like this movie", with its corresponding label "1" stands for postive comment.

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

## Step 4: Tokenization

We apply Tokenization with `Tokenizer`, fitting the word index on our training dataset with `tokenizer.fit_on_texts`, and create sequences and padding them with `texts_to_sequences` and `pad_sequences`

![image](https://github.com/hughiephan/DPL/assets/16631121/641b2e5a-3949-4d2c-8f2c-d292493f462c)

```python
tokenizer = Tokenizer(num_words = vocab_size, oov_token="")
tokenizer.fit_on_texts(training_sentences)
sequences = tokenizer.texts_to_sequences(training_sentences)
padded = pad_sequences(sequences, maxlen=sequence_len, truncating='post')
testing_sequences = tokenizer.texts_to_sequences(testing_sentences)
testing_padded = pad_sequences(testing_sequences, maxlen=sequence_len)
```

## Step 5: Build postional encoding from scratch
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

Loop through `k` and `i`, we notice that for `i` we loop until it reach half of the embedding dimension, which is 258

![image](https://github.com/hughiephan/DPL/assets/16631121/4552c766-82bb-4828-9ee2-b1b0e171a8a6)

For each position, we just add a new value based on sin and cos. Even dimension `P[k, 2*i]` will be assigned with value of sin `np.sin(k/denominator)`, and odd dimension `P[k, 2*i+1]` will be assigned with value of cos `np.cos(k/denominator)`. We use denominator as 10000 to increase the probability that different positions will have unique encodings. Let this run for a while, and we will get

![image](https://github.com/hughiephan/DPL/assets/16631121/f1cfb8aa-9ca7-4a3d-84ee-b59a5836e832)

And finally, we get the whole postional encoding.

![image](https://github.com/hughiephan/DPL/assets/16631121/d8d399c3-9beb-4236-9129-5a245de36f12)

## Step 6: Positional Encoding Layer
```python
class PositionalEncoding(tf.keras.layers.Layer):
    def __init__(self, sequence_len, embedding_dim, **kwargs):
        super(PositionalEncoding, self).__init__(**kwargs)
        self.positional_encoding = positional_encoding(sequence_len, embedding_dim)     
    def call(self, inputs):
        return inputs + self.positional_encoding
```

Here's an example of the Embedding `inputs`, for the following sentence (trained in one epoch): "This was an absolutely terrible movie. Don't be lured in by Christopher Walken or Michael Ironside. Both are great actors, but this must simply be their worst role in history. Even their great acting could not redeem this movie's ridiculous storyline" 

![image](https://github.com/hughiephan/DPL/assets/16631121/3900093f-f6cd-4abc-84ef-a8bd7d33e16a)

Then combine the Embedding `inputs` with the Positional Encoding using `inputs + self.positional_encoding`

![image](https://github.com/hughiephan/DPL/assets/16631121/fca01039-3f67-40d4-a353-2fa4cf142b85)

# Step 7: Add Positional Encoding Layer to our model
```python
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

![image](https://github.com/hughiephan/DPL/assets/16631121/4834c11c-b718-48f9-8141-f8006a8df6f2)

## Step 8: Train
```python
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(padded, training_labels_final, epochs=5, validation_data = (testing_padded, testing_labels_final))
```

![image](https://github.com/hughiephan/DPL/assets/16631121/7cacc1ee-7b5e-4309-b0bd-52dfdeba0dd6)

## Step 9: Make predictions
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

## (Optional) Step 10: Visualize embedding

We point to the layer two Postional Embedding `model.get_layer(index=2)` but you can change to index=1 for the Embedding layer. If you train with `epochs=5` it will be a little hard to see the different between two layers. 

```python
sentences = "This was an absolutely terrible movie. Don't be lured in by Christopher Walken or Michael Ironside. Both are great actors, but this must simply be their worst role in history. Even their great acting could not redeem this movie's ridiculous storyline"
input_sequence = tokenizer.texts_to_sequences([sentence])
input_padded = pad_sequences(input_sequence, maxlen=sequence_len)
embedding_output = model.get_layer(index=2).output  
embedding_extractor = tf.keras.Model(model.input, embedding_output)
prediction = embedding_extractor.predict(input_padded)
cax = plt.matshow(tf.squeeze(prediction, axis=0))
plt.gcf().colorbar(cax)
```

## Reference
- https://machinelearningmastery.com/a-gentle-introduction-to-positional-encoding-in-transformer-models-part-1
- https://vaclavkosar.com/ml/transformer-positional-embeddings-and-encodings
- https://community.intel.com/t5/Blogs/Tech-Innovation/Artificial-Intelligence-AI/Is-Positional-Encoding-Required-In-All-Language-Models/post/1450078
