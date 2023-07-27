# Text Generation with LSTM

Take a sequence of characters as input and the immediate next character as the target. As long as it can predict what is the next character given what are preceding, we can run the model in a loop to generate a long piece of text

## Step 1: Import Neural Network and necessary librarires
```py
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
```

## Step 2: Load Dataset
Download Alice in Wonderland Dataset from: https://www.kaggle.com/datasets/thala321/alice-in-wonderland

```py
filename = "../input/alice-in-wonderland/wonderland.txt"
raw_text = open(filename, 'r', encoding='utf-8').read()
raw_text = raw_text.lower()
```

## Step 3: Map unique characters to integers
```py
chars = sorted(list(set(raw_text)))
char_to_int = dict((c, i) for i, c in enumerate(chars)) # A dictionary to map of unique characters to integers
int_to_char = dict((i, c) for c, i in char_to_int.items()) # A dictionary to tranform integers back to characters
```

char_to_int

![image](https://github.com/hughiephan/DPL/assets/16631121/db4f7e07-eb25-4242-afee-88113fd216c5)

int_to_char

![image](https://github.com/hughiephan/DPL/assets/16631121/d0fd86fb-1c5c-43f7-a7bc-354be8fe9705)


## Step 4: Prepare data for training 

Loop through all the text, get a sequence out 100 words as input and the 101-th word as output. Then format both input and output characters as integers.

```py
n_chars = len(raw_text)
n_vocab = len(chars)
seq_length = 100
dataX = []
dataY = []
for i in range(0, n_chars - seq_length, 1):
    seq_in = raw_text[i:i + seq_length]
    seq_out = raw_text[i + seq_length]
    dataX.append([char_to_int[char] for char in seq_in])
    dataY.append(char_to_int[seq_out])
```

Output of seq_in and seq_out

![image](https://github.com/hughiephan/DPL/assets/16631121/d26de4c5-e585-4e39-ab99-9e31c6b8a2a6)

## Step 5: Reshape in to LSTM Input Format
```py
n_patterns = len(dataX)
X = torch.tensor(dataX, dtype=torch.float32).reshape(n_patterns, seq_length, 1) # reshape X to be [samples, time steps, features]
X = X / float(n_vocab) # normalize the input between 0 to 1
y = torch.tensor(dataY)
```

Input data for LSTM are [Batch Size, Sequence Length, Input Dimension], with 143046 samples, 100 number of time steps that will be inputted into LSTM network, and in 1-dimensional space becaue we are dealing with text.

For example: Your input sentence to LSTM network is = ["I hate to eat apples"], then every single token would be fed as input at each timestep. So the Sequence Length would total number of tokens in a sentence that is 5.

![image](https://github.com/hughiephan/DPL/assets/16631121/84703a36-b2c9-4b43-94d3-aa2e1f9297df)

## Step 6: Build our Language Model based on LSTM
```py
class LanguageModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(input_size=1, hidden_size=256, num_layers=1, batch_first=True)
        self.dropout = nn.Dropout(0.2)
        self.linear = nn.Linear(256, n_vocab)
    def forward(self, x):
        x, _ = self.lstm(x)
        x = x[:, -1, :] # take only the last output
        x = self.linear(self.dropout(x))
        return x
```

## Step 7: Start training
```py
model = LanguageModel()
optimizer = optim.Adam(model.parameters())
loss_fn = nn.CrossEntropyLoss(reduction="sum")
loader = data.DataLoader(data.TensorDataset(X, y), shuffle=True, batch_size=128)
for epoch in range(20):
    model.train()
    for X_batch, y_batch in loader:
        y_pred = model(X_batch)
        loss = loss_fn(y_pred, y_batch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    model.eval()
    loss = 0
    with torch.no_grad():
        for X_batch, y_batch in loader:
            y_pred = model(X_batch)
            loss += loss_fn(y_pred, y_batch)
        print("Epoch %d: Cross-entropy: %.4f" % (epoch, loss))
```

## Step 8: Make a prediction 

```
start = np.random.randint(0, len(raw_text)-seq_length)
prompt = raw_text[start:start+seq_length]
pattern = [char_to_int[c] for c in prompt]
model.eval()
print('Prompt: "%s"' % prompt)
with torch.no_grad(): # a sequence of 1,000 characters in length
    for i in range(1000):
        x = np.reshape(pattern, (1, len(pattern), 1)) / float(n_vocab)
        x = torch.tensor(x, dtype=torch.float32)
        prediction = model(x)
        index = int(prediction.argmax()) # convert logits into one character
        result = int_to_char[index]
        print(result, end="")
        pattern.append(index) # append the new character into the prompt for the next iteration
        pattern = pattern[1:]
```

Prompt

![image](https://github.com/hughiephan/DPL/assets/16631121/97e254b7-88f9-4da9-8269-4c2068799fe4)

Output

![image](https://github.com/hughiephan/DPL/assets/16631121/08a1da04-aa92-4896-8b0f-e91f8c6e5f17)
