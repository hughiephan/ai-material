# SimpleRNN for Language Processing

## Coding
```python
import warnings 
warnings.filterwarnings('ignore')
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
tfds.disable_progress_bar()

imdb = tfds.load("imdb_reviews", as_supervised=True) # Get a tuple (features, label)
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
padded = pad_sequences(sequences, maxlen=120, truncating='post') # A maximum length of 120 words will be used for each piece of text,  trunc_type is set to be ‘post’ means the text will be truncated at the end
testing_sequences = tokenizer.texts_to_sequences(testing_sentences)
testing_padded = pad_sequences(testing_sequences, maxlen=120)
```

```python
vocab_size = 10000 # 10000 unique words will be used for this model
embedding_dim= 16 # A vector of size 16 will be representing each word
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=120), # Embedding is a weights matrix with every row as word vector for all unique words in our vocabulary. Read more here: https://hemantranvir.medium.com/spam-detection-using-rnn-simplernn-lstm-with-step-by-step-explanation-530367608071
    tf.keras.layers.SimpleRNN(32),
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.summary()
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(padded, training_labels_final, epochs=5, validation_data = (testing_padded, testing_labels_final))
```

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

![image](https://github.com/hughiephan/DPL/assets/16631121/f3d92734-1100-407a-9988-e92d58f2490b)
