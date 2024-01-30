from django.db import models
import torch.nn as nn
import torch
import numpy as np

# Define the neural network
class Net(nn.Module):
    def __init__(self, size):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(11, size)  # 11 input features
        self.fc2 = nn.Linear(size, size)
        self.fc3 = nn.Linear(size, 4)
        self.residual = nn.Linear(size, size)  # Residual connection
        self.drop = nn.Dropout(0.7)

    def forward(self, x):
        x = self.drop(torch.relu(self.fc1(x)))

        x = self.drop(torch.relu(self.fc2(x)))

        identity = self.residual(x)
        x = x + identity
        x = self.drop(torch.relu(self.fc2(x)))

        x = self.drop(torch.relu(self.fc2(x)))

        
        x = self.fc3(x)
        return x
    

