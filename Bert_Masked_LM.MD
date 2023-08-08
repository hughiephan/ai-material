# Next Word Prediction using Bert - Masked Language Model

## Prerequisites Knowledge

BERT has a unique training approach, masked-language modeling (MLM) which mask 15% of tokens during model pre-training

![image](https://github.com/hughiephan/DPL/assets/16631121/3b9bd2c8-4229-4f7c-b3d6-82e4cc9253b2)

Token Type Id is useful in task like Question Answering to separate then answer and question:

```text
Input: [CLS] HuggingFace is based in NYC [SEP] Where is HuggingFace based? [SEP]
Token Type IDs: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
```

Attention mask is a binary tensor indicating the position of the padded indices so that the model does not attend to them

![image](https://github.com/hughiephan/DPL/assets/16631121/937e4f2d-101d-4a11-80df-d2f1163973cd)

![image](https://github.com/hughiephan/DPL/assets/16631121/8df94107-ab6b-48ed-a851-ff9232070627)

## Step: Import libraries
```python
import numpy as np
import tensorflow as tf
from transformers import BertTokenizer, TFBertForMaskedLM
```

## Step: Load Bert Model
```python
tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
model = TFBertForMaskedLM.from_pretrained('bert-base-cased')
```

## Step: Run our model

For `[CLS] The dog ate the [MASK] [SEP]`, we will have 7 tokens.
Each token embedding will have the size of 28996 

Input -> Tokenized_inputs

```text
Input: The dog ate the [MASK] 
Input IDs: [ 101, 1109, 3676, 8756, 1103,  103,  102]
Token Type IDs: [0, 0, 0, 0, 0, 0, 0]
Attention Mask: [1, 1, 1, 1, 1, 1, 1]
```



Input and Output

```text
Input:  The dog ate the [MASK]
outputs.logits.shape: (1, 7, 28996)
```

```python
def getPredictions(text, tokenizer=tokenizer, model=model):
    tokenized_inputs = tokenizer(text, return_tensors="tf")
    outputs = model(tokenized_inputs["input_ids"])
    top_5 = tf.math.top_k(outputs.logits, 5).indices[0].numpy()
    decoded_output = tokenizer.batch_decode(top_5)
    mask_token = tokenizer.encode(tokenizer.mask_token)[1:-1]
    mask_index = np.where(tokenized_inputs["input_ids"].numpy()[0]==mask_token)[0][0]
    decoded_output_words = decoded_output[mask_index]
    print("Input: ", text)
    print("Possible words: ", decoded_output_words)
    print("\n")
```

## Step: Run predictions
```python
getPredictions("The dog ate the [MASK]")
getPredictions("The dog ate the [MASK].")
getPredictions("The boy played with the [MASK] at the park")
getPredictions("The boy played with the [MASK] at the park.")
```

![image](https://github.com/hughiephan/DPL/assets/16631121/f3bf5e54-fe9f-409f-93c9-4adbceca35ce)
