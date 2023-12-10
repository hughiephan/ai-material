## Finetune RoBerta and SVM - Riken Dataset (JAIST)

## Dataset
Private / Feedback Dataset

## Python
```python
import gc
import os
import sys
import cv2
import math
import time
import tqdm
import random
import numpy as np
import pandas as pd
import seaborn as sns
from tqdm import tqdm
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

from sklearn.svm import SVR

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold,StratifiedKFold

import torch
import torchvision
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.optim import Adam, lr_scheduler
from torch.utils.data import Dataset, DataLoader

from transformers import (AutoModel, AutoTokenizer, 
                          AutoModelForSequenceClassification)

import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff


from colorama import Fore, Back, Style
y_ = Fore.YELLOW
r_ = Fore.RED
g_ = Fore.GREEN
b_ = Fore.BLUE
m_ = Fore.MAGENTA
c_ = Fore.CYAN
sr_ = Style.RESET_ALL

# Read multiple input files
file_list = []
def getTrainData(dir_path):
    f_l = []
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            f_l.append(dir_path + '/' + path)
    return f_l
file_list = getTrainData("../input/readability/Y14")
file_list.extend(getTrainData("../input/readability/Y15"))
file_list = [i for i in file_list if "Y15_2-3_2_4" not in i] # This is use for test
print(file_list)

# Read multiple JSON inputs
dfs = []
for file in file_list:
    data = pd.read_json(file)
    dfs.append(data) 
train_data = pd.concat(dfs, ignore_index=True) 
```

```python
test_data = pd.read_json('../input/readability/Y15_2-3_2_4-test.json')

num_bins = int(np.floor(1 + np.log2(len(train_data))))
train_data.loc[:,'bins'] = pd.cut(train_data['score'],bins=num_bins,labels=False)

target = train_data['score'].to_numpy()
bins = train_data.bins.to_numpy()

def rmse_score(y_true,y_pred):
    return np.sqrt(mean_squared_error(y_true,y_pred))

config = {
    'batch_size':128,
    'max_len':256,
    'nfolds':5,
    'seed':42,
}

def seed_everything(seed=42):
    random.seed(seed)
    os.environ['PYTHONASSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True

seed_everything(seed=config['seed'])
```

```python
class CLRPDataset(Dataset):
    def __init__(self,df,tokenizer):
        self.excerpt = df['mecab'].to_numpy()
        self.tokenizer = tokenizer
    
    def __getitem__(self,idx):
        encode = self.tokenizer(self.excerpt[idx],return_tensors='pt',
                                max_length=config['max_len'],
                                padding='max_length',truncation=True)
        return encode
    
    def __len__(self):
        return len(self.excerpt)

class AttentionHead(nn.Module):
    def __init__(self, in_features, hidden_dim, num_targets):
        super().__init__()
        self.in_features = in_features
        self.middle_features = hidden_dim

        self.W = nn.Linear(in_features, hidden_dim)
        self.V = nn.Linear(hidden_dim, 1)
        self.out_features = hidden_dim

    def forward(self, features):
        att = torch.tanh(self.W(features))

        score = self.V(att)

        attention_weights = torch.softmax(score, dim=1)

        context_vector = attention_weights * features
        context_vector = torch.sum(context_vector, dim=1)

        return context_vector

class Model(nn.Module):
    def __init__(self):
        super(Model,self).__init__()
        self.roberta = AutoModel.from_pretrained('../input/roberta-base')    
        self.head = AttentionHead(768,768,1)
        self.dropout = nn.Dropout(0.1)
        self.linear = nn.Linear(self.head.out_features,1)

    def forward(self,**xb):
        x = self.roberta(**xb)[0]
        x = self.head(x)
        return x

def get_embeddings(df,path,plot_losses=True, verbose=True):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"{device} is used")
            
    model = Model()
    model.load_state_dict(torch.load(path))
    model.to(device)
    model.eval()
    
    tokenizer = AutoTokenizer.from_pretrained('../input/roberta-base')
    
    ds = CLRPDataset(df,tokenizer)
    dl = DataLoader(ds,
                  batch_size = config["batch_size"],
                  shuffle=False,
                  num_workers = 4,
                  pin_memory=True,
                  drop_last=False
                 )
        
    embeddings = list()
    with torch.no_grad():
        for i, inputs in tqdm(enumerate(dl)):
            inputs = {key:val.reshape(val.shape[0],-1).to(device) for key,val in inputs.items()}
            outputs = model(**inputs)
            outputs = outputs.detach().cpu().numpy()
            embeddings.extend(outputs)
    return np.array(embeddings)
```

```python
train_embeddings1 =  get_embeddings(train_data,'../input/clr-roberta/model0/model0.bin')
test_embeddings1 = get_embeddings(test_data,'../input/clr-roberta/model0/model0.bin')

train_embeddings2 =  get_embeddings(train_data,'../input/clr-roberta/model1/model1.bin')
test_embeddings2 = get_embeddings(test_data,'../input/clr-roberta/model1/model1.bin')

train_embeddings3 =  get_embeddings(train_data,'../input/clr-roberta/model2/model2.bin')
test_embeddings3 = get_embeddings(test_data,'../input/clr-roberta/model2/model2.bin')

train_embeddings4 =  get_embeddings(train_data,'../input/clr-roberta/model3/model3.bin')
test_embeddings4 = get_embeddings(test_data,'../input/clr-roberta/model3/model3.bin')

train_embeddings5 =  get_embeddings(train_data,'../input/clr-roberta/model4/model4.bin')
test_embeddings5 = get_embeddings(test_data,'../input/clr-roberta/model4/model4.bin')
```

## SVM
```python
def get_preds_svm(X,y,X_test,bins=bins,nfolds=5,C=10,kernel='rbf'):
    scores = list()
    preds = np.zeros((X_test.shape[0]))
    
    kfold = StratifiedKFold(n_splits=config['nfolds'],shuffle=True,random_state=config['seed'])
    for k, (train_idx,valid_idx) in enumerate(kfold.split(X,bins)):
        model = SVR(C=C,kernel=kernel,gamma='auto')
        X_train,y_train = X[train_idx], y[train_idx]
        X_valid,y_valid = X[valid_idx], y[valid_idx]
        model.fit(X_train,y_train)
        prediction = model.predict(X_valid)
        score = rmse_score(prediction, y_valid)
        print(f'Fold {k} , rmse score: {score}')
        scores.append(score)
        preds += model.predict(X_test)
    print("mean rmse",np.mean(scores))
    return np.array(preds)/nfolds

svm_preds1 = get_preds_svm(train_embeddings1,target,test_embeddings1)
svm_preds2 = get_preds_svm(train_embeddings2,target,test_embeddings2)
svm_preds3 = get_preds_svm(train_embeddings3,target,test_embeddings3)
svm_preds4 = get_preds_svm(train_embeddings4,target,test_embeddings4)
svm_preds5 = get_preds_svm(train_embeddings5,target,test_embeddings5)
```
