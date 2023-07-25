# Text Generation with LSTM


Step: Import Neural Network and necessary librarires
```py
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
```

Step: Load Dataset
```py
filename = "../input/alice-in-wonderland/wonderland.txt"
raw_text = open(filename, 'r', encoding='utf-8').read()
raw_text = raw_text.lower()
```

Step: Map unique characters to integers
```py
chars = sorted(list(set(raw_text)))
char_to_int = dict((c, i) for i, c in enumerate(chars)) # create mapping of unique chars to integers
```

Step: Prepare data for training 
```py
n_chars = len(raw_text)
n_vocab = len(chars)
seq_length = 100
dataX = []
dataY = []
for i in range(0, n_chars - seq_length, 1): # prepare the dataset of input to output pairs encoded as integers
    seq_in = raw_text[i:i + seq_length]
    seq_out = raw_text[i + seq_length]
    dataX.append([char_to_int[char] for char in seq_in])
    dataY.append(char_to_int[seq_out])
n_patterns = len(dataX)
X = torch.tensor(dataX, dtype=torch.float32).reshape(n_patterns, seq_length, 1) # reshape X to be [samples, time steps, features]
X = X / float(n_vocab)
y = torch.tensor(dataY)
```

Step: Build our Language Model based on LSTM
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

Step: Start training
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

Step: Make a prediction 

```py
int_to_char = dict((i, c) for c, i in char_to_int.items())
start = np.random.randint(0, len(raw_text)-seq_length)
prompt = raw_text[start:start+seq_length]
pattern = [char_to_int[c] for c in prompt]
model.eval()
print('Prompt: "%s"' % prompt)
with torch.no_grad():
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
