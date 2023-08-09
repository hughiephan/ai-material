# Next Word Prediction using Bert - Masked Language Model

## Prerequisites Knowledge

BERT has a unique training approach, masked-language modeling (MLM) which mask 15% of tokens during model pre-training

![image](https://github.com/hughiephan/DPL/assets/16631121/3b9bd2c8-4229-4f7c-b3d6-82e4cc9253b2)

There are a total of three special token types in BERT: `[CLS]`, `[SEP]`, and `[MASK]`. `[CLS]` token stands for "classification" and is used at the beginning of a sentence or input sequence. It is used in various tasks like sentence classification and question answering to represent the entire input sequence. `[SEP]` token is used to separate two different sentences or segments within a single input sequence. It helps BERT to distinguish between different parts of the input during the pre-training and fine-tuning process. `[MASK]` token is used during the pre-training phase in the Masked Language Model (MLM) objective. It masks random tokens in the input, and BERT learns to predict those masked tokens based on the surrounding context.

## Step 1: Import libraries
```python
import numpy as np
import tensorflow as tf
from transformers import BertTokenizer, TFBertForMaskedLM
```

## Step 2: Load Bert Model

In bert-base-cased, "Apple" and "apple" are treated as two different words

```python
tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
model = TFBertForMaskedLM.from_pretrained('bert-base-cased')
```

## Step 3: Define the predictions
Takes a text input and returns the top 5 predicted words for a masked token within the text.

```python
def getPredictions(text, tokenizer=tokenizer, model=model):
    tokenized_inputs = tokenizer(text, return_tensors="tf")
    outputs = model(tokenized_inputs["input_ids"]) # Input IDs will be used for prediction
    top_5 = tf.math.top_k(outputs.logits, 5).indices[0].numpy() # Get 5 highest logits for each tokens
    decoded_output = tokenizer.batch_decode(top_5) # Transform the top 5 higest logists into words 
    mask_index = np.where(tokenized_inputs["input_ids"].numpy()[0]==103)[0][0] # Finds the index of the masked token
    decoded_output_words = decoded_output[mask_index] # Get the possible words for the [Mask] 
    print("Input: ", text)
    print("Possible words: ", decoded_output_words)
    print("\n")
```

Let's use `[CLS] The dog ate the [MASK] [SEP]` as our example. After we run predict, the output Logits will be `(1, 7, 28996)` which is equivalent to `batch_size` = 1 because we input 1 sentence, `num_tokens`: 7 because we have 7 tokens in the example sentence, and `vocab_size` = 28996 because we have 28996 possible words. But we only want the top 5 possible words for each tokens, so we filter the top 5 using `math.top_k(outputs.logits, 5)`. After that we will get `top_5.shape` = (7, 5) which is equivalent to 7 positions in the sentence, and 5 possible words for each position.

```text
Input: The dog ate the [MASK]  
Before Input to model: [CLS] The dog ate the [MASK] [SEP] # Total 7 Tokens. Postion of [MASK] here is 5.
Input IDs: [ 101, 1109, 3676, 8756, 1103, 103, 102]
Decoded Output: [
    '., " the )',                 # Possible words for [CLS]
    '. " the, ;',                 # Possible words for The
    'dog dogs Dog man cat',       # Possible words for dog
    'ate eats chewed eat took',   # Possible words for ate
    'the it that her his',        # Possible words for the
    '.! ;?...',                   # Possible words for [MASK]. Our mask_index (5) will point here
    '.? ; ",'                     # Possible words for [SEP]
]
```

## Step 4: Run predictions
```python
getPredictions("The dog ate the [MASK]")
getPredictions("The dog ate the [MASK].")
getPredictions("The boy played with the [MASK] at the park")
getPredictions("The boy played with the [MASK] at the park.")
```

![image](https://github.com/hughiephan/DPL/assets/16631121/f3bf5e54-fe9f-409f-93c9-4adbceca35ce)
