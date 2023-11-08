# Finetune T5 for ChatBot

## Step: Import libraries
```python
import pandas as pd
import torch
import pytorch_lightning as pl
import warnings
warnings.filterwarnings("ignore")
from sklearn.model_selection import train_test_split
from pytorch_lightning.callbacks import ModelCheckpoint
from transformers import T5Tokenizer, T5ForConditionalGeneration  
from transformers import AdamW
from torch.utils.data import Dataset, DataLoader
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
INPUT_MAX_LEN = 128 
OUTPUT_MAX_LEN = 128 
tokenizer = T5Tokenizer.from_pretrained("t5-base", model_max_length=512)
t5 = T5ForConditionalGeneration.from_pretrained("t5-base", return_dict = True)
df_train, df_test = train_test_split(data,test_size = 0.2, random_state=100)
```

## Step: Define ChatDataset

![image](https://github.com/hughiephan/DPL/assets/16631121/a864171f-3d49-4edb-8ba8-21a676adb585)

Pytorch `Dataset` stores the samples and their corresponding labels. We will read the question, answer in `__init__` but leave the reading of each item to `__getitem__`. This is memory efficient because all the questions, and answers are not stored in the memory at once but read as required. We use `Tokenizer` to tokenize both the questions and answers. We override the `__len__` methods  so that `len(self.question)` returns the size of the dataset (it is also possible to use `len(self.answer)` as they both have the same size).

```python
class ChatDataset(Dataset):
  def __init__(self,question,answer):   
    self.question = question
    self.answer = answer
  
  def __len__(self):
    return len(self.question)

  def __getitem__(self,item):
    question = str(self.question[item])
    question = ''.join(question.split())
    answer = str(self.answer[item])
    answer = ''.join(answer.split())
    input_tokenize = tokenizer(      
            question,
            add_special_tokens=True,
            max_length=INPUT_MAX_LEN,
            padding = 'max_length',
            truncation = True,
            return_attention_mask=True,
            return_tensors="pt"
    )
    output_tokenize = tokenizer(
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

## Step: Define DataLoader

DataLoader wraps an iterable around the Dataset to enable easy access to the samples

```python
class ChatDataLoad(pl.LightningDataModule):
    def __init__(self,df_train,df_test):
        super().__init__()
        self.df_train = df_train
        self.df_test = df_test
    
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
        return DataLoader(
             self.train_data,
             batch_size= 8,
             shuffle=True, 
             num_workers=2
        )
    
    def val_dataloader(self):
        return DataLoader(
            self.valid_data,
            batch_size= 2,
            num_workers = 2
        )
    
dataload = ChatDataLoad(df_train,df_test)
dataload.setup()
```

## Step: Define ChatModel
```python
class ChatModel(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.model = t5

    def forward(self, input_ids, attention_mask, labels=None):
        output = t5(
            input_ids=input_ids, 
            attention_mask=attention_mask, 
            labels=labels
        )
        return output.loss, output.logits
    
    def training_step(self, batch, batch_idx):
        input_ids = batch["input_ids"]
        attention_mask = batch["attention_mask"]
        labels= batch["target"]
        loss, logits = self(input_ids , attention_mask, labels)
        self.log("train_loss", loss, prog_bar=True, logger=True)
        return {'loss': loss}
    
    def validation_step(self, batch, batch_idx):
        input_ids = batch["input_ids"]
        attention_mask = batch["attention_mask"]
        labels= batch["target"]
        loss, logits = self(input_ids, attention_mask, labels)
        self.log("val_loss", loss, prog_bar=True, logger=True)
        return {'val_loss': loss}

    def configure_optimizers(self):
        return AdamW(self.parameters(), lr=0.0001)
```

## Step: Training
```python
chatModel = ChatModel()
chatModel.to(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))
checkpoint = ModelCheckpoint(
    dirpath="/kaggle/working",
    filename='best-model',
    save_top_k=2,
    verbose=True,
    monitor="val_loss",
    mode="min"
)
trainer = pl.Trainer(
    callbacks = checkpoint,
    max_epochs= 1,
    gpus=1,
    accelerator="gpu"
)
trainer.fit(chatModel, dataload)
```

## Step: Predict
```python
train_model = ChatModel.load_from_checkpoint('/kaggle/working/best-model.ckpt')
train_model.freeze()

def generate_question(question):
    inputs_encoding =  tokenizer(
        question,
        add_special_tokens=True,
        max_length= INPUT_MAX_LEN,
        padding = 'max_length',
        truncation='only_first',
        return_attention_mask=True,
        return_tensors="pt"
    )

    generate_ids = train_model.model.generate(
        input_ids = inputs_encoding["input_ids"],
        attention_mask = inputs_encoding["attention_mask"],
        max_length = INPUT_MAX_LEN,
        num_beams = 4,
        num_return_sequences = 1,
        no_repeat_ngram_size=2,
        early_stopping=True,
    )

    preds = [
        tokenizer.decode(gen_id,
        skip_special_tokens=True, 
        clean_up_tokenization_spaces=True)
        for gen_id in generate_ids
    ]
    return "".join(preds)

ques = "hi, how are you doing?"
print("Ques: ",ques)
print("BOT: ",generate_question(ques))
```
