```python
from tensorflow import math, matmul, reshape, shape, transpose, cast, float32
from tensorflow.keras.layers import LayerNormalization, Layer, Dense, ReLU, Dropout
from keras.backend import softmax
from numpy import random

class DotProductAttention(Layer):
    def __init__(self, **kwargs):
        super(DotProductAttention, self).__init__(**kwargs)
    def call(self, queries, keys, values, d_k, mask=None):
        scores = matmul(queries, keys, transpose_b=True) / math.sqrt(cast(d_k, float32))
        if mask is not None:
            scores += -1e9 * mask
        weights = softmax(scores)
        return matmul(weights, values)

class MultiHeadAttention(Layer):
    def __init__(self, h, d_k, d_v, d_model, **kwargs):
        super(MultiHeadAttention, self).__init__(**kwargs)
        self.attention = DotProductAttention()  # Scaled dot product attention
        self.heads = h  # Number of attention heads to use
        self.d_k = d_k  # Dimensionality of the linearly projected queries and keys
        self.d_v = d_v  # Dimensionality of the linearly projected values
        self.d_model = d_model  # Dimensionality of the model
        self.W_q = Dense(d_k)  # Learned projection matrix for the queries
        self.W_k = Dense(d_k)  # Learned projection matrix for the keys
        self.W_v = Dense(d_v)  # Learned projection matrix for the values
        self.W_o = Dense(d_model)  # Learned projection matrix for the multi-head output
 
    def reshape_tensor(self, x, heads, flag):
        if flag:
            x = reshape(x, shape=(shape(x)[0], shape(x)[1], heads, -1))
            x = transpose(x, perm=(0, 2, 1, 3))
        else:
            x = transpose(x, perm=(0, 2, 1, 3))
            x = reshape(x, shape=(shape(x)[0], shape(x)[1], self.d_k))
        return x
 
    def call(self, queries, keys, values, mask=None):
        q_reshaped = self.reshape_tensor(self.W_q(queries), self.heads, True)
        k_reshaped = self.reshape_tensor(self.W_k(keys), self.heads, True)
        v_reshaped = self.reshape_tensor(self.W_v(values), self.heads, True)
        o_reshaped = self.attention(q_reshaped, k_reshaped, v_reshaped, self.d_k, mask)
        output = self.reshape_tensor(o_reshaped, self.heads, False)
        return self.W_o(output)

class AddNormalization(Layer):
    def __init__(self, **kwargs):
        super(AddNormalization, self).__init__(**kwargs)
        self.layer_norm = LayerNormalization()  # Layer normalization layer
 
    def call(self, x, sublayer_x):
        add = x + sublayer_x
        return self.layer_norm(add)

class FeedForward(Layer):
    def __init__(self, d_ff, d_model, **kwargs):
        super(FeedForward, self).__init__(**kwargs)
        self.fully_connected1 = Dense(d_ff)  # First fully connected layer
        self.fully_connected2 = Dense(d_model)  # Second fully connected layer
        self.activation = ReLU()  # ReLU activation layer
 
    def call(self, x):
        x_fc1 = self.fully_connected1(x)
        return self.fully_connected2(self.activation(x_fc1))

class EncoderLayer(Layer):
    def __init__(self, h, d_k, d_v, d_model, d_ff, rate, **kwargs):
        super(EncoderLayer, self).__init__(**kwargs)
        self.multihead_attention = MultiHeadAttention(h, d_k, d_v, d_model)
        self.dropout1 = Dropout(rate)
        self.add_norm1 = AddNormalization()
        self.feed_forward = FeedForward(d_ff, d_model)
        self.dropout2 = Dropout(rate)
        self.add_norm2 = AddNormalization()
 
    def call(self, x, padding_mask, training):
        multihead_output = self.multihead_attention(x, x, x, padding_mask)
        multihead_output = self.dropout1(multihead_output, training=training)
        addnorm_output = self.add_norm1(x, multihead_output)
        feedforward_output = self.feed_forward(addnorm_output)
        feedforward_output = self.dropout2(feedforward_output, training=training)
        return self.add_norm2(addnorm_output, feedforward_output)

class Encoder(Layer):
    def __init__(self, vocab_size, sequence_length, h, d_k, d_v, d_model, d_ff, n, rate, **kwargs):
        super(Encoder, self).__init__(**kwargs)

        self.pos_encoding = tf.keras.layers.Embedding(vocab_size, d_model, input_length=sequence_length)
        self.dropout = Dropout(rate)
        self.encoder_layer = [EncoderLayer(h, d_k, d_v, d_model, d_ff, rate) for _ in range(n)]
 
    def call(self, input_sentence, padding_mask, training):
        pos_encoding_output = self.pos_encoding(input_sentence)
        x = self.dropout(pos_encoding_output, training=training)
        for i, layer in enumerate(self.encoder_layer):
            x = layer(x, padding_mask, training)
        return x

enc_vocab_size = 20 # Vocabulary size for the encoder
input_seq_length = 5  # Maximum length of the input sequence
h = 8  # Number of self-attention heads
d_k = 64  # Dimensionality of the linearly projected queries and keys
d_v = 64  # Dimensionality of the linearly projected values
d_ff = 2048  # Dimensionality of the inner fully connected layer
d_model = 512  # Dimensionality of the model sub-layers' outputs
n = 6  # Number of layers in the encoder stack
batch_size = 64  # Batch size from the training process
dropout_rate = 0.1  # Frequency of dropping the input units in the dropout layers
input_seq = random.random((batch_size, input_seq_length))
encoder = Encoder(enc_vocab_size, input_seq_length, h, d_k, d_v, d_model, d_ff, n, dropout_rate)
print(encoder(input_seq, None, True))
```

## Reference
- https://machinelearningmastery.com/implementing-the-transformer-encoder-from-scratch-in-tensorflow-and-keras/
- https://machinelearningmastery.com/how-to-implement-multi-head-attention-from-scratch-in-tensorflow-and-keras/
