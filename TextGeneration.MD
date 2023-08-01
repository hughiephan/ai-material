# Text Generation with LSTM

Take a sequence of characters as input and the immediate next character as the target. As long as it can predict what is the next character given what are preceding, we can run the model in a loop to generate a long piece of text

![image](https://github.com/hughiephan/DPL/assets/16631121/8c8dcba1-2d21-41eb-97c8-0ac7ec05c10f)

## Step 1: Import Neural Network and necessary librarires
```
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
```

## Step 2: Load Dataset
Download Alice in Wonderland Dataset from: https://www.kaggle.com/datasets/thala321/alice-in-wonderland

```
filename = "../input/alice-in-wonderland/wonderland.txt"
raw_text = open(filename, 'r', encoding='utf-8').read()
raw_text = raw_text.lower()
```

Output of raw_text [0:50]

![image](https://github.com/hughiephan/DPL/assets/16631121/7a420ef1-3395-4fa7-bb81-2817161cbd52)

## Step 3: Map unique characters to integers
`char_to_int` and `int_to_char` functions are our word index, we can use these functions to transform texts to sequences back and forth. A simpler approach is using a Tokenizer which will function the same way.

```
chars = sorted(list(set(raw_text))) # Unique characters in the dataset
char_to_int = dict((c, i) for i, c in enumerate(chars)) # A dictionary to map unique characters to integers. When we call enumerate function, we will get something like this [(0, 'A'), (1, 'B'), (2, 'C'), (3, 'D')]
int_to_char = dict((i, c) for c, i in char_to_int.items()) # A dictionary to transform integers back to characters. This is just reversing of char_to_int.
```

chars (46 characters)

![image](https://github.com/hughiephan/DPL/assets/16631121/25d54010-ccc6-4e42-a2a6-669cfef57c5c)

char_to_int

![image](https://github.com/hughiephan/DPL/assets/16631121/db4f7e07-eb25-4242-afee-88113fd216c5)

int_to_char

![image](https://github.com/hughiephan/DPL/assets/16631121/d0fd86fb-1c5c-43f7-a7bc-354be8fe9705)

## Step 4: Prepare data for training 

Loop through all the text, and get a sequence of 100 words as input and the 101st word as output. Then we format both input and output characters into integers.

```
n_chars = len(raw_text) # 143146 characters
n_vocab = len(chars) # 46. Note that we are calculating the list `chars`, not the number `n_chars`
dataX = []
dataY = []
for i in range(0, n_chars - 100, 1):
    seq_in = raw_text[i:i + 100] # This is like a sliding window, getting 100 characters at a time
    seq_out = raw_text[i + 100]
    dataX.append([char_to_int[char] for char in seq_in])
    dataY.append(char_to_int[seq_out])
```

Output of seq_in and seq_out

![image](https://github.com/hughiephan/DPL/assets/16631121/d26de4c5-e585-4e39-ab99-9e31c6b8a2a6)

With their respective sequence 

![image](https://github.com/hughiephan/DPL/assets/16631121/d73ec2da-4d6c-40ef-ad99-176aa6581d67)

## Step 5: Reshape into LSTM Input Format

In this tutorial, we will use our LSTM as our Language Model. But to use LSTM, we need to have these three values as input:
- n_sequence: Number of samples in our Feature X
- n_timestep: Length of a sample
- n_feature: Number of features which describe our sample

Accordingly, we will get:
- n_sequence = 143146 - 100 samples = 143046 samples. This is because we use a sliding window of size 100.
- n_timestep = 100 characters being processed at 100 timesteps.
- n_feature = 1. Because we use 1-dimension vectors to represent our characters

```
n_sequence = len(dataX)
X = torch.tensor(dataX, dtype=torch.float32).reshape(n_sequence, 100, 1)
X = X / float(n_vocab) # Normalize the input between 0 to 1
y = torch.tensor(dataY)
```

X.shape

![image](https://github.com/hughiephan/DPL/assets/16631121/84703a36-b2c9-4b43-94d3-aa2e1f9297df)

## Step 6: Build our Language Model based on LSTM

In LSTM `input_size` = `n_feature`, in our case it's 1 because we are dealing with 1-dimension vectors (tokenized characters) at each timestep. We need `batch_first=True` because our Input data from the previous step is in this format `(batch_size, seq_len, features)`. Then we just define the hyperparameters, 256 hidden units, and 1 LSTM layer.

```
class LanguageModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(input_size=1, hidden_size=256, num_layers=1, batch_first=True) 
        self.dropout = nn.Dropout(0.2)
        self.linear = nn.Linear(256, n_vocab)
    def forward(self, x):
        x, _ = self.lstm(x)
        x = x[:, -1, :] # X is the output of LSTM, it will have this shape [batch_size, seq_len, hidden_size]. We only need to get the last value of the output sequence so we use -1.
        x = self.dropout(x)
        x = self.linear(x) # Predicting one of the 46 characters in the vocab
        return x
```

![image](https://github.com/hughiephan/DPL/assets/16631121/0985737b-4c56-4c61-a66a-8c39b9334e92)

## Step 7: Start training
```
model = LanguageModel()
optimizer = optim.Adam(model.parameters())
loss_fn = nn.CrossEntropyLoss()
loader = data.DataLoader(data.TensorDataset(X, y), shuffle=True, batch_size=128)
model.train()
for epoch in range(10): # This will take a while
    print("Running Epoch %d ..." % epoch)
    for X_batch, y_batch in loader:
        y_pred = model(X_batch)
        loss = loss_fn(y_pred, y_batch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
print("Finished training")
```

## Step 8: Make a prediction 

```
def predict(prompt):
    pattern = [char_to_int[c] for c in prompt]
    with torch.no_grad():
        for i in range(1000):
            x = np.reshape(pattern, (1, len(pattern), 1)) / float(n_vocab) # Reshape and normalize
            x = torch.tensor(x, dtype=torch.float32)
            prediction = model(x)
            index = int(prediction.argmax()) # Predict an integer
            pattern.append(index) # Append the new character into the prompt for the next iteration
            pattern = pattern[1:]
    return ''.join([int_to_char[i] for i in pattern]) # Convert all the integers into characters
```

From our Neural Network, because we are outputting 46 nodes so we need to use argmax to find the highest number and use it as our prediction. For example, we choose index 1 because 2.6911 is the highest. After that we will look up what is 1 represent in word index using `int_to_char`. 

![image](https://github.com/hughiephan/DPL/assets/16631121/34c59c6b-6e53-4d3b-8bc8-cc6872e59f5e)

Prompt

![image](https://github.com/hughiephan/DPL/assets/16631121/97e254b7-88f9-4da9-8269-4c2068799fe4)

The output here sounds like a baby trying to talk. Adding more layers and hidden units would make the output more natural.

![image](https://github.com/hughiephan/DPL/assets/16631121/de95b7f7-8602-4b10-9844-8e7f041f179b)

## Step 9: Deploy the model with gradio

```
model.eval() # Change to evaluation mode because we don't want Dropout Layer to automatically drop Neural Network nodes when we are making prediction
def text_generation(prompt):
    return predict(prompt)
gr.Interface(fn=text_generation, inputs=["prompt"], outputs=["text"]).launch()
```

![image](https://github.com/hughiephan/DPL/assets/16631121/d3bce2ea-fa3d-4ca1-ba9f-fd8e4ff3bbf8)

