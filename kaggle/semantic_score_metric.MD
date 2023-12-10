# Semantic Score Metric - Riken Dataset (JAIST)

## Dataset
Private / Feedback Dataset

## Coding
```python
!pip install fugashi
!pip install ipadic

from transformers import BertJapaneseTokenizer, BertModel
from datasets import load_dataset,Dataset,DatasetDict
import torch
import os
import scipy.spatial
import warnings
import pandas as pd
import pickle
#warnings.filterwarnings("ignore")    
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
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
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
def load_riken_dataset():
    file_list = []
    riken_data = []
    def getTrainData(dir_path):
        f_l = []
        for path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, path)):
                f_l.append(dir_path + '/' + path)
        return f_l
    file_list = getTrainData("../input/readability/Y14")
    file_list.extend(getTrainData("../input/readability/Y15"))
    for file in file_list:
        if ("Y14_1-2_1_3.json" in file or "Y14_2-2_1_4.json" in file):
            data = pd.read_json(file)
            riken_data.append(data) 
    return file_list, riken_data
riken_data = load_riken_dataset()[1]
pd_data = pd.concat(riken_data, ignore_index=True) 
dataset = Dataset.from_pandas(pd_data)
train_testvalid = dataset.train_test_split(test_size=0.2,seed=15)
test_valid = train_testvalid['test'].train_test_split(test_size=0.5,seed=15)
dataset = DatasetDict({
    'train': train_testvalid['train'],
    'test': test_valid['test'],
    'valid': test_valid['train']})
train = dataset["train"].to_pandas()
test = dataset["test"].to_pandas()
valid = dataset["valid"].to_pandas()
train['Raw'] = train['Char'].map(lambda x:  x.replace(" ", ""))
model = SentenceBertJapanese("sonoisa/sentence-bert-base-ja-mean-tokens")
sentence_vectors = model.encode(train.Char)
queries = ['その橋が架かってしまった原因としては、おそらく言語の障害は主因ではなく、異国の相手の考え方や価値観を理解するということである。もしお互いに認め合いの習慣が養えれば、その橋を簡単に渡せると思います。']
query_embeddings = model.encode(queries).numpy()
closest_n = 10
for query, query_embedding in zip(queries, query_embeddings):
    distances = scipy.spatial.distance.cdist([query_embedding], sentence_vectors, metric="cosine")[0]
    results = zip(range(len(distances)), distances)
    results = sorted(results, key=lambda x: x[1])
    print("\n\n======================\n\n")
    print("Query:", query)
    print("\nTop 10 most similar sentences in corpus:")
    for idx, distance in results[0:closest_n]:
        print(train.loc[idx]["Raw"], "(Score: %.4f)" % train.loc[idx]["score"] , "(Cosine Score: %.4f)" % (distance / 2))
```
