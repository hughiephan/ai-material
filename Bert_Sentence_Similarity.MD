# Sentence Similarity with Sentence Bert Japanese

Sentence-BERT is a variant of BERT that has been fine-tuned to produce sentence embeddings. 

![image](https://github.com/hughiephan/DPL/assets/16631121/a92de1fa-a508-41b4-b1ac-4d095c95df44)

In Sentence-BERT, there is only one embedding for the entire sequence rather than one embedding per token.

![image](https://github.com/hughiephan/DPL/assets/16631121/87de6fcc-7b0f-4b4b-8123-f927e915660f)

![image](https://github.com/hughiephan/DPL/assets/16631121/6d7c71e6-20ce-4f18-9bab-9dfbad29fa34)

## Step 1
Transformers library is used to load the pre-trained BERT model and tokenizer for the Japanese Language (You can also use it for English or Vietnamese Bert). 
Then we use `scipy.spatial` to calculate the cosine distances between vectors and find related sentences. Cosine similarity is a metric used to determine how similar the documents (other similarity measuring techniques are Euclidean distance or Manhattan distance)

![image](https://github.com/hughiephan/DPL/assets/16631121/714f3f61-e76e-42d4-91e9-c508d91485bb)

```
import warnings
warnings.filterwarnings("ignore")
import torch
import scipy.spatial
from transformers import BertJapaneseTokenizer, BertModel
```

`_mean_pooling` is a helper function to perform mean pooling over the token embeddings based on the attention mask. Mean pooling is used to obtain a single vector representation for the whole sentence.

![image](https://github.com/hughiephan/DPL/assets/16631121/45f9e2e1-2993-492d-9f89-733539533bb2)

## Step
```python
class SentenceBertJapanese:
    def __init__(self, model_name_or_path, device=None):
        self.tokenizer = BertJapaneseTokenizer.from_pretrained(model_name_or_path)
        self.model = BertModel.from_pretrained(model_name_or_path)
        self.model.eval()
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = torch.device(device)
        self.model.to(device)
    def _mean_pooling(self, model_output, attention_mask):
        ....
    def encode(self, sentences, batch_size=8):
        ....
```

## Step: Continue to define our SentenceBert
```python
class SentenceBertJapanese:
    def __init__(self, model_name_or_path, device=None):
        ....
    def _mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    def encode(self, sentences, batch_size=8):
        ....
```

## Step:
```python
class SentenceBertJapanese:
    def __init__(self, model_name_or_path, device=None):
        ....
    def _mean_pooling(self, model_output, attention_mask):
        ....
    @torch.no_grad()
    def encode(self, sentences, batch_size=8):
        all_embeddings = []
        iterator = range(0, len(sentences), batch_size)
        for batch_idx in iterator:
            batch = sentences[batch_idx:batch_idx + batch_size]
            encoded_input = self.tokenizer.batch_encode_plus(batch, padding="longest", 
                                           truncation=True, return_tensors="pt").to(self.device)
            model_output = self.model(**encoded_input)
            sentence_embeddings = self._mean_pooling(model_output, encoded_input["attention_mask"]).to('cpu')
            all_embeddings.extend(sentence_embeddings)
        return torch.stack(all_embeddings)
```

## Step: Setup our model
```python
sentences = ["お辞儀をしている男性会社員", "笑い袋", "テクニカルエバンジェリスト（女性）", "戦うAI", "笑う男性（5段階）"]
model = SentenceBertJapanese("sonoisa/sentence-bert-base-ja-mean-tokens")
sentence_vectors = model.encode(sentences)
queries = ['暴走したAI', '暴走した人工知能', 'いらすとやさんに感謝', 'つづく']
query_embeddings = model.encode(queries).numpy()
```

## Step: Find the similar sentences
```python
for query, query_embedding in zip(queries, query_embeddings):
    distances = scipy.spatial.distance.cdist([query_embedding], sentence_vectors, metric="cosine")[0]
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
```
