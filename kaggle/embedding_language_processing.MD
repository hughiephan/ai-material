# Embedding for Language Processing4

```python
import warnings 
warnings.filterwarnings('ignore')
import pickle
import io
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
tfds.disable_progress_bar()

imdb, info = tfds.load("imdb_reviews", with_info=True, as_supervised=True) # Get a tuple (features, label) alongs with info
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
vocab_size = 10000 # 10000 unique words will be used for this model
embedding_dim= 16 # A vector of size 16 will be representing each word
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=120),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.summary()
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(padded, training_labels_final, epochs=5, validation_data = (testing_padded, testing_labels_final))
```

```python
e = model.layers[0]
weights = e.get_weights()[0]
encoder = info.features['text'].encoder
out_v = io.open('vecs.tsv', 'w', encoding='utf-8')
out_m = io.open('meta.tsv', 'w', encoding='utf-8')
for word_num in range(1,vocab_size):
    word = tokenizer.index_word[word_num + 1] # Extracting word for given index, +1 to remove the padding
    embeddings = weights[word_num] # Getting weights
    out_m.write(word + "\n")
    out_v.write("\t".join([str(x) for x in embeddings]) + "\n")
out_v.close()
out_m.close()
```

Then use https://projector.tensorflow.org to visualize the embedding

![image](https://github.com/hughiephan/DPL/assets/16631121/2f663f0d-2724-4489-8b32-4e0ffcce662a)
