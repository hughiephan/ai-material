# How to use Sentence Similarity with Sentence Bert Japanese

Demonstrates how to use Sentence-BERT for encoding Japanese sentences into embeddings and how to find the most similar sentences in a given corpus based on cosine similarity.

## Objective

From Token Embeddings

![image](https://github.com/hughiephan/DPL/assets/16631121/fd65f24c-0443-4c20-aeab-7b67997a9c44)

To Sentence Embeddings

![image](https://github.com/hughiephan/DPL/assets/16631121/6b24747d-aca8-4b14-baf3-8c0d72829940)

Calculate the Cosine similarity between two sentence embeddings

![image](https://github.com/hughiephan/DPL/assets/16631121/ef5e8991-0924-4ed0-905a-5e3997ca82c1)


## Step 1: Import libraries
Transformers library is used to load the pre-trained BERT model and tokenizer for the Japanese Language (You can also use it for English or Vietnamese Bert). 
Then we use `scipy.spatial` to calculate the cosine distances between vectors and find related sentences. Cosine similarity is a metric used to determine how similar the documents (other similarity measuring techniques are Euclidean distance or Manhattan distance)

![image](https://github.com/hughiephan/DPL/assets/16631121/714f3f61-e76e-42d4-91e9-c508d91485bb)

```python
import warnings
warnings.filterwarnings("ignore")
import torch
import scipy.spatial
from transformers import BertJapaneseTokenizer, BertModel
```

## Step 2: Init Bert Japanese
Load the pre-trained Japanese model and tokenizer, which has been fine-tuned for sentence-level embeddings with mean pooling on Japanese text. In this tutorial, we only learn how to run Sentence Bert without further training or fine-tuning, so let's set our model to evaluate mode.

```python 
class SentenceBertJapanese:
    def __init__(self):
        self.tokenizer = BertJapaneseTokenizer.from_pretrained(sonoisa/sentence-bert-base-ja-mean-tokens)
        self.model = BertModel.from_pretrained(sonoisa/sentence-bert-base-ja-mean-tokens)
        self.model.eval()
    def _mean_pooling(self, token_embeddings, attention_mask):
        ....
    @torch.no_grad()
    def encode(self, sentences, batch_size=8):
        ....
```

## Step: Mean Pooling

`_mean_pooling` is our function to perform mean pooling over the token embeddings based on the attention mask. Mean pooling is used to obtain a single vector representation for the whole sentence.

BERT has a max length limit of tokens = 512

![image](https://github.com/hughiephan/DPL/assets/16631121/45f9e2e1-2993-492d-9f89-733539533bb2)

We want to create a mask with the same shape as token_embeddings but contains only the attention mask value (0 or 1). We can use this mask to set the embeddings of padding tokens to zero during the mean-pooling operation, ensuring that padding tokens do not contribute to the final sentence embeddings. `attention_mask` is a binary tensor of shape (batch_size, sequence_length), where batch_size is the number of sentences in the batch, and sequence_length is the maximum length of sentences after padding. When we use unsqueeze(-1) on attention_mask, it will add a new dimension to the last axis, resulting in a tensor of shape (batch_size, sequence_length, 1). Then broadcasts the tensor with shape (batch_size, sequence_length, 1) to the shape of token_embeddings, which is (batch_size, sequence_length, embedding_dim).

![image](https://github.com/hughiephan/DPL/assets/16631121/87de6fcc-7b0f-4b4b-8123-f927e915660f)

We take BERT’s token embeddings output and the sentence’s attention_mask tensor. We then resize the attention_mask to align to the higher 768-dimensionality of the token embeddings. We apply this resized mask in_mask to those token embeddings to exclude padding tokens from the mean pooling operation. Our mean pooling takes the average activation of values across each dimension to produce a single value. This brings our tensor sizes from (512*768) to (1*768)



```python
class SentenceBertJapanese:
    def __init__(self):
        ....
    def _mean_pooling(self, token_embeddings, attention_mask):
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    @torch.no_grad()
    def encode(self, sentences, batch_size=8):
        ....
```



## Step: Encode
`Encode` method takes a list of sentences, converts them to embeddings using mean pooling, and returns a tensor containing all the sentence embeddings. In Sentence-BERT, there is only one embedding for the entire sequence rather than one embedding per token. `mean_pooling` token embeddings to create sentence embeddings


```python
class SentenceBertJapanese:
    def __init__(self):
        ....
    def _mean_pooling(self, token_embeddings, attention_mask):
        ....
    @torch.no_grad()
    def encode(self, sentences, batch_size=8):
        all_embeddings = []
        iterator = range(0, len(sentences), batch_size)
        for batch_idx in iterator:
            batch = sentences[batch_idx:batch_idx + batch_size]
            encoded_input = self.tokenizer.batch_encode_plus(batch, padding="longest", truncation=True, return_tensors="pt")
            token_embeds  = self.model(**encoded_input)[0] # process tokens through model and extract token embeddings
            sentence_embeddings = self._mean_pooling(token_embeds , encoded_input["attention_mask"])
            all_embeddings.extend(sentence_embeddings)
        return torch.stack(all_embeddings)
```

## Step: Encode corpus

![image](https://github.com/hughiephan/DPL/assets/16631121/902dac23-99db-4f4e-84bd-0cc685b40c69)

The sentences list contains five Japanese sentences. The encode method is called to obtain the sentence embeddings for the given sentences.
```python
model = SentenceBertJapanese()
sentences = ["お辞儀をしている男性会社員", "笑い袋", "テクニカルエバンジェリスト（女性）", "戦うAI", "笑う男性（5段階）"]
corpus = model.encode(sentences)
```

## Step: Encode queries

The queries list contains four Japanese sentences that are used as queries. The encode method is called to obtain the embeddings for the queries.
```python
queries = ['暴走したAI']
query_embeddings = model.encode(queries).numpy()
```

## Step: Find similar sentences
For each query, cosine distances are computed between its embedding and the embeddings of all the sentences in the corpus. The results are sorted based on similarity (lower cosine distance means more similarity). The top 5 most similar sentences are printed for each query along with their similarity score.

![image](https://github.com/hughiephan/DPL/assets/16631121/6d7c71e6-20ce-4f18-9bab-9dfbad29fa34)

```python
for query, query_embedding in zip(queries, query_embeddings):
    distances = scipy.spatial.distance.cdist([query_embedding], corpus, metric="cosine")[0]
    results = zip(range(len(distances)), distances)
    results = sorted(results, key=lambda x: x[1])
    print("\n\n======================\n\n")
    print("Query:", query)
    print("\nTop 5 most similar sentences in corpus:")
    for idx, distance in results[0:5]:
        print(sentences[idx].strip(), "(Score: %.4f)" % (distance / 2))
```


Output
```
======================
Query: 暴走したAI

Top 5 most similar sentences in corpus:
戦うAI (Score: 0.1521)
心を持ったAI (Score: 0.1666)
武器を持つAI (Score: 0.1994)
人工知能・AI (Score: 0.2130)
画像認識をするAI (Score: 0.2306)
...
```