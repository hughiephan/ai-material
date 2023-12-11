# Pre-trained Embedding for NLP

```python
!pip install bert-for-tf2
import warnings 
warnings.filterwarnings('ignore')
import bert
import math
import numpy as np
import csv
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_datasets as tfds
from tensorflow.keras.models import Model
tfds.disable_progress_bar()

# Load IMDb Reviews dataset from TensorFlow Datasets
imdb, info = tfds.load("imdb_reviews", with_info=True, as_supervised=True) # Get a tuple (features, label) alongs with info
train_data, test_data = imdb['train'], imdb['test']
training_sentences = []
total = 0

# Preprocess training data by limiting it to the first 100 sentences and truncating to 128 characters
for s,l in train_data:
    if total >= 100: # Limit to 100 training sentences
        break
    sentence_str = str(s.numpy())
    sentence_str = sentence_str[:128]
    training_sentences.append(sentence_str)
    total += 1

# Helper function to generate masks for padding tokenized input sequences
def get_masks(tokens, max_seq_length):
    """Mask for padding"""
    if len(tokens)>max_seq_length:
        raise IndexError("Token length more than max seq length!")
    return [1]*len(tokens) + [0] * (max_seq_length - len(tokens))

# Helper function to generate segment IDs for each token in the input sequences
def get_segments(tokens, max_seq_length):
    """Segments: 0 for the first sequence, 1 for the second"""
    if len(tokens) > max_seq_length:
        raise IndexError("Token length more than max seq length!")
    segments = []
    current_segment_id = 0
    for token in tokens:
        segments.append(current_segment_id)
        if token == "[SEP]":
            current_segment_id = 1
    return segments + [0] * (max_seq_length - len(tokens))

# Helper function to convert tokens to token IDs using a tokenizer's vocabulary
def get_ids(tokens, tokenizer, max_seq_length):
    """Token ids from Tokenizer vocab"""
    token_ids = tokenizer.convert_tokens_to_ids(tokens)
    input_ids = token_ids + [0] * (max_seq_length-len(token_ids))
    return input_ids
```

```python
FullTokenizer = bert.bert_tokenization.FullTokenizer
max_seq_length = 128 # Maximum sequence length for BERT input

# Define input layers for the BERT model
input_word_ids = tf.keras.layers.Input(shape=(max_seq_length,), dtype=tf.int32,name="input_word_ids")
input_mask = tf.keras.layers.Input(shape=(max_seq_length,), dtype=tf.int32, name="input_mask")
segment_ids = tf.keras.layers.Input(shape=(max_seq_length,), dtype=tf.int32, name="segment_ids")

# Load the BERT model as a KerasLayer from TensorFlow Hub
bert_layer = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/1", trainable=True)

# Connect the input layers to the BERT model to obtain pooled and sequence outputs
pooled_output, sequence_output = bert_layer([input_word_ids, input_mask, segment_ids])

# Create a Keras Model with the input and output layers to form the BERT-based model
model = Model(inputs=[input_word_ids, input_mask, segment_ids], outputs=[pooled_output, sequence_output])

# Get the vocabulary file and do_lower_case flag from the BERT layer
vocab_file = bert_layer.resolved_object.vocab_file.asset_path.numpy()
do_lower_case = bert_layer.resolved_object.do_lower_case.numpy()

# Initialize the tokenizer using the FullTokenizer class
tokenizer = FullTokenizer(vocab_file, do_lower_case)
stokens_list = []
input_ids = []
input_masks = []
input_segments = []
for sentence in training_sentences:
    stokens = tokenizer.tokenize(sentence)
    stokens = ["[CLS]"] + stokens + ["[SEP]"]
    stokens_list.append(stokens)
    input_ids.append(get_ids(stokens, tokenizer, max_seq_length))
    input_masks.append(get_masks(stokens, max_seq_length))
    input_segments.append(get_segments(stokens, max_seq_length))

pool_embs, all_embs = model.predict([np.array(input_ids),np.array(input_masks),np.array(input_segments)])
print(np.shape(all_embs))
```

```python
FullTokenizer = bert.bert_tokenization.FullTokenizer
max_seq_length = 128 # Maximum sequence length for BERT input

# Define input layers for the BERT model
input_word_ids = tf.keras.layers.Input(shape=(max_seq_length,), dtype=tf.int32,name="input_word_ids")
input_mask = tf.keras.layers.Input(shape=(max_seq_length,), dtype=tf.int32, name="input_mask")
segment_ids = tf.keras.layers.Input(shape=(max_seq_length,), dtype=tf.int32, name="segment_ids")

# Load the BERT model as a KerasLayer from TensorFlow Hub
bert_layer = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/1", trainable=True)

# Connect the input layers to the BERT model to obtain pooled and sequence outputs
pooled_output, sequence_output = bert_layer([input_word_ids, input_mask, segment_ids])

# Create a Keras Model with the input and output layers to form the BERT-based model
model = Model(inputs=[input_word_ids, input_mask, segment_ids], outputs=[pooled_output, sequence_output])

# Get the vocabulary file and do_lower_case flag from the BERT layer
vocab_file = bert_layer.resolved_object.vocab_file.asset_path.numpy()
do_lower_case = bert_layer.resolved_object.do_lower_case.numpy()

# Initialize the tokenizer using the FullTokenizer class
tokenizer = FullTokenizer(vocab_file, do_lower_case)
stokens_list = []
input_ids = []
input_masks = []
input_segments = []
for sentence in training_sentences:
    stokens = tokenizer.tokenize(sentence)
    stokens = ["[CLS]"] + stokens + ["[SEP]"]
    stokens_list.append(stokens)
    input_ids.append(get_ids(stokens, tokenizer, max_seq_length))
    input_masks.append(get_masks(stokens, max_seq_length))
    input_segments.append(get_segments(stokens, max_seq_length))

pool_embs, all_embs = model.predict([np.array(input_ids),np.array(input_masks),np.array(input_segments)])
print(np.shape(all_embs))
```

Then use https://projector.tensorflow.org to visualize the embedding
