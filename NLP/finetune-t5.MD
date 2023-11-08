# Finetune T5 for ChatBot

## Step: Import libraries
```python
import pandas as pd
import torch
import pytorch_lightning as pl
import warnings
warnings.filterwarnings("ignore")
from sklearn.model_selection import train_test_split
from transformers import T5Tokenizer, T5ForConditionalGeneration  
from transformers import AdamW
from pytorch_lightning.callbacks import ModelCheckpoint
from torch.nn.utils.rnn import pad_sequence
pl.seed_everything(100)
```

## Step: Load dataset
Download the following dataset https://www.kaggle.com/datasets/kreeshrajani/3k-conversations-dataset-for-chatbot

```python
data = pd.read_csv("/kaggle/input/3k-conversations-dataset-for-chatbot/Conversation.csv")
data.drop(columns=['Unnamed: 0'],inplace=True)
```

## Step: Define variables
```python
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
INPUT_MAX_LEN = 128 
OUTPUT_MAX_LEN = 128 
TRAIN_BATCH_SIZE = 8 
VAL_BATCH_SIZE = 2
EPOCHS = 2
MODEL_NAME = "t5-base"
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME, model_max_length=512)
df_train, df_test = train_test_split(data,test_size = 0.2, random_state=100)
```

## Step: ChatDataset

![image](https://github.com/hughiephan/DPL/assets/16631121/a864171f-3d49-4edb-8ba8-21a676adb585)

Pytorch `Dataset` stores the samples and their corresponding labels. We will read the question, answer in `__init__` but leave the reading of each item to `__getitem__`. This is memory efficient because all the questions, and answers are not stored in the memory at once but read as required. We use `Tokenizer` to tokenize both the questions and answers. We override the `__len__` methods  so that `len(self.question)` returns the size of the dataset (it is also possible to use `len(self.answer)` as they both have the same size).

```python
class ChatDataset(Dataset):
  def __init__(self,question,answer):   
    self.question = question
    self.answer = answer
    self.tokenizer = tokenizer
  
  def __len__(self):
    return len(self.question)

  def __getitem__(self,item):
    question = str(self.question[item])
    question = ''.join(question.split())
    answer = str(self.answer[item])
    answer = ''.join(answer.split())
    input_tokenize = self.tokenizer(      
            question,
            add_special_tokens=True,
            max_length=INPUT_MAX_LEN,
            padding = 'max_length',
            truncation = True,
            return_attention_mask=True,
            return_tensors="pt"
    )
    output_tokenize = self.tokenizer(
            answer,
            add_special_tokens=True,
            max_length=OUTPUT_MAX_LEN,
            padding = 'max_length',
            truncation = True,
            return_attention_mask=True,
            return_tensors="pt"
            
    )
    input_ids = input_tokenize["input_ids"].flatten()
    attention_mask = input_tokenize["attention_mask"].flatten()
    labels = output_tokenize['input_ids'].flatten()
    out = {
            'question':question,      
            'answer':answer,
            'input_ids': input_ids,
            'attention_mask':attention_mask,
            'target':labels
    } 
    return out      

chatdataset = ChatDataset(            
    question = df_train.question.values,
    answer = df_train.answer.values
)
for (i, sample) in list(enumerate(chatdataset))[:1]:
    print(sample)
```

## Step: DataLoader

DataLoader wraps an iterable around the Dataset to enable easy access to the samples

```python
class T5DataLoad(pl.LightningDataModule):
    def __init__(self,df_train,df_test):
        super().__init__()
        self.df_train = df_train
        self.df_test = df_test
        self.tokenizer = tokenizer
    
    def setup(self, stage=None):
        self.train_data = ChatDataset(
            question = self.df_train.question.values,
            answer = self.df_train.answer.values
        )
        self.valid_data = ChatDataset(
            question = self.df_test.question.values,
            answer = self.df_test.answer.values
        )
        
    def train_dataloader(self):
        return torch.utils.data.DataLoader(
             self.train_data,
             batch_size= TRAIN_BATCH_SIZE,
             shuffle=True, 
             num_workers=2
        )
    
    def val_dataloader(self):
        return torch.utils.data.DataLoader(
            self.valid_data,
            batch_size= VAL_BATCH_SIZE,
            num_workers = 2
        )
```
