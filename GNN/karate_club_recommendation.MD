# Karate Club Recommendation with Graph Neural Network

## Step 1: Import libraries
```python
!pip install torch_geometric
import torch
import networkx as nx
import matplotlib.pyplot as plt
from torch.nn import Linear
from torch_geometric.nn import GCNConv
from torch_geometric.datasets import KarateClub
%matplotlib inline
```

## Step 2: Import data
```python
dataset = KarateClub()
data = dataset[0]
```

![image](https://github.com/hughiephan/DPL/assets/16631121/8a68ffc1-6ce7-461a-8551-401e13395153)

## Step 3: Define the model
```python
class GCN(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = GCNConv(dataset.num_features, 4)
        self.conv2 = GCNConv(4, 4)
        self.conv3 = GCNConv(4, 2)
        self.classifier = Linear(2, dataset.num_classes)

    def forward(self, x, edge_index):
        h = self.conv1(x, edge_index)
        h = h.tanh()
        h = self.conv2(h, edge_index)
        h = h.tanh()
        h = self.conv3(h, edge_index)
        h = h.tanh() 
        out = self.classifier(h)
        return out, h
```

## Step 4: Setup training
```python
model = GCN()
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

def train(data):
    optimizer.zero_grad() 
    out, h = model(data.x, data.edge_index) 
    loss = criterion(out[data.train_mask], data.y[data.train_mask]) 
    loss.backward()  
    optimizer.step()  
    return loss, h
```

## Step 5: Train and Visualize
```python
for epoch in range(61):
    loss, h = train(data)
    if epoch % 20 == 0:
        h = h.detach().cpu().numpy()
        plt.figure(figsize=(7,7))
        plt.xticks([])
        plt.yticks([])
        plt.scatter(h[:, 0], h[:, 1], s=140, c=data.y, cmap="Set2")
        plt.xlabel(f'Epoch: {epoch}, Loss: {loss.item():.4f}', fontsize=16)
        plt.show()
```

![image](https://github.com/hughiephan/DPL/assets/16631121/84a6088a-c884-4d04-ae51-878251509215)

## Reference:
- PyG Tutorial 1.Introduction: Hands-on Graph Neural Networks
