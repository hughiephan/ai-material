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
```

