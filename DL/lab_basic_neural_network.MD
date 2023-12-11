# Lab Basic Neural Network

## Question
Implement Backward Propgation, Loss Function, Optimizer and a new Neural Network

## Scoring Criteria
You will be graded based on Originality of your implementation: Did you implement anything new in the model or just re-use it? How much work did you put into implementing your model? Result of your implementation: Accuracy, Loss, Cross-validation Q/A to test your understanding: How well do you understand your code? How well do you understand Neural Network concepts? Note: DO NOT add comments in your code

![image](https://github.com/hughiephan/DPL/assets/16631121/140d901d-9707-49a9-9f05-a3559f4c1d9e)

## Forward Propagation
```python
import torch
import torch.nn as nn
import torch.optim as optim
input = torch.tensor([[0.35, 0.9]], dtype=torch.float32)
output = torch.tensor([[0.5]], dtype=torch.float32)
class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(2, 2, bias=False)
        self.fc2 = nn.Linear(2, 1, bias=False)
        self.fc1.weight.data = torch.tensor([[0.1, 0.8], [0.4, 0.6]])
        self.fc2.weight.data = torch.tensor([[0.3], [0.9]]).t()
    def forward(self, x):
        out = self.fc1(x)
        print("Calculation after Linear layer: \n", out)
        out = nn.Sigmoid()(out)
        print("Calculation after Sigmoid layer (Activation Layer): \n", out)
        out = self.fc2(out)
        out = nn.Sigmoid()(out)
        print("Calculation at final layer: \n", out)
        return out
model = SimpleNet()
model(input)
```

## Question 1
Implement Backward Propagation to SimpleNet to calculate the updated weights.

## Question 2
Generate 1000 random data and use any libary to plot/visualize it.
```python
newIntput = torch.tensor([[Data1, Data2],[Data3, Data4],.....], dtype=torch.float32)
newOutput = torch.tensor([[Data501],[Data502],......], dtype=torch.float32)
```

## Question 3
Implement a new class NeuralNet that: Accept newInput. Have 2 hidden layers with bias enabled, and use ReLU Activation Function. (You can decide the number of nodes). Predict newOutput

## Question 4
Implement a Loss Function and an Optimizer then train the NeuralNet with 10 epochs
