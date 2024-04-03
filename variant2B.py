# -*- coding: utf-8 -*-
"""Variant2BCOMP_472_Project_Part_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XuEBDHCzl8FRuQyIhxy7vg28HU3BpzGr
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Subset
from torchvision.transforms import v2
from torchvision.datasets import ImageFolder
import time

import zipfile

import gdown
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Subset
from torchvision.transforms import v2
from torchvision.datasets import ImageFolder
import time

# Download the file using gdown
url = 'https://drive.google.com/uc?id=1zWLvGyTRz07z3swsYJwK0_d-MjXgXvHY'
output = 'COMP472Data.zip'
gdown.download(url, output, quiet=False)

# Unzip the downloaded file
with zipfile.ZipFile('COMP472Data.zip', 'r') as zip_ref:
    zip_ref.extractall('.')

path = '/content/COMP472Data'
transform = v2.Compose([v2.ToImage(),v2.Grayscale(),v2.ToDtype(torch.float32, scale=True)])
full_dataset = ImageFolder(path,transform)

#Hyperparameters
ttsplit = 0.2 #Train-Test Split %. Currently 80:20
vtsplit = 0.1 #Train-Validation Split %. Currently 90:10 ONLY splitting the traning data
batch_size = 32 #Batch size for model
learning_rate = 0.004083 #Learning rate for the model (step size for SGD)
num_epochs = 50 #Number of epochs to train on

# Split dataset indices
train_indices, test_indices = train_test_split(list(range(len(full_dataset))), test_size=ttsplit, random_state=42)
train_indices, val_indices = train_test_split(train_indices, test_size=vtsplit, random_state=42)

# Create subsets
train_set = Subset(full_dataset, train_indices)
val_set = Subset(full_dataset, val_indices)
test_set = Subset(full_dataset, test_indices)

# Create data loaders
train_loader = torch.utils.data.DataLoader(train_set, batch_size=batch_size, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_set, batch_size=batch_size, shuffle=False)
val_loader = torch.utils.data.DataLoader(val_set, batch_size=batch_size, shuffle=False)

import torch.nn as nn

model_variant2B = nn.Sequential(
    nn.Conv2d(1, 32, kernel_size=2, padding=1),  # Changed to 2x2
    nn.ReLU(),
    nn.BatchNorm2d(32),
    nn.Conv2d(32, 64, kernel_size=2, padding=1),  # Changed to 2x2
    nn.ReLU(),
    nn.BatchNorm2d(64),
    nn.MaxPool2d(2, 2),
    nn.Dropout(0.25),
    nn.Conv2d(64, 128, kernel_size=2, padding=1),  #2x2
    nn.ReLU(),
    nn.BatchNorm2d(128),
    nn.Conv2d(128, 128, kernel_size=2, padding=1),
    nn.ReLU(),
    nn.BatchNorm2d(128),
    nn.MaxPool2d(2, 2),
    nn.Dropout(0.25),
    nn.Conv2d(128, 256, kernel_size=2, padding=1),
    nn.ReLU(),
    nn.BatchNorm2d(256),
    nn.Conv2d(256, 256, kernel_size=2, padding=1),
    nn.ReLU(),
    nn.BatchNorm2d(256),
    nn.MaxPool2d(2, 2),
    nn.Dropout(0.25),
    nn.Flatten(),
    nn.Linear(256 * 7 * 7, 256),  # Adjusted input size
    nn.ReLU(),
    nn.BatchNorm1d(256),
    nn.Dropout(0.5),
    nn.Linear(256, 4)
)

# Set loss function and optimizer, currently CCE for classification and Adam as the optimizer, if you want to change the optimizer: https://pytorch.org/docs/stable/optim.html#algorithms
import torch.optim as optim
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model_variant2B.parameters(), lr=learning_rate)

# Initialize lists to store metrics
train_losses = []
train_accuracies = []
val_losses = []
val_accuracies = []

# Early stopping
best_val_loss = float('inf')
wait = 5  # Number of epochs to wait
counter = 0

# Training the model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_variant2B.to(device)

# Start training time
training_start_time = time.time()

for epoch in range(num_epochs):
    model_variant2B.train()
    running_loss, correct, total = 0, 0, 0
    epoch_start_time = time.time()

    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model_variant2B(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    # Calculate training metrics
    train_loss = running_loss / len(train_loader)
    train_accuracy = 100 * correct / total
    train_losses.append(train_loss)
    train_accuracies.append(train_accuracy)

    #training time per epoch
    train_epoch_time = time.time() - epoch_start_time
    print(f'Epoch {epoch + 1} training time: {train_epoch_time:.2f}')

    # Validation
    model_variant2B.eval()
    valRunning_loss, val_correct, val_total = 0, 0, 0
    val_start = time.time()

    with torch.no_grad():

        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            val_outputs = model_variant2B(images)
            val_loss = criterion(val_outputs, labels)
            valRunning_loss += val_loss.item()
            _, val_predicted = torch.max(val_outputs.data, 1)
            val_total += labels.size(0)
            val_correct += (val_predicted == labels).sum().item()

    # Calculate validation metrics
    val_loss = valRunning_loss / len(val_loader)
    val_accuracy = 100 * val_correct / val_total
    val_losses.append(val_loss)
    val_accuracies.append(val_accuracy)

    # Early stopping check
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        counter = 0  # Reset counter
        torch.save(model_variant2B.state_dict(), 'bestmodel_variant2B.pth')  # Save the best model
    else:
        counter += 1  # Increase counter

    if counter >= wait:
        print("Early stopping")
        break

    #validation metrics
    val_epoch_time = time.time() - val_start
    print(f'Epoch {epoch + 1} validation time: {val_epoch_time:.2f}')
    print(f'Epoch {epoch + 1}/{num_epochs}, Train Loss: {train_loss:.4f}, Train Accuracy: {train_accuracy:.2f}%, Validation Loss: {val_loss:.4f}, Validation Accuracy: {val_accuracy:.2f}%')

# training time
print("Total: %s seconds " % (time.time() - training_start_time))

# Plot training and validation metrics
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(train_losses, label='Train Loss', marker='o')
plt.plot(val_losses, label='Validation Loss', marker='o')
plt.title('Training and Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(train_accuracies, label='Train Accuracy', marker='o')
plt.plot(val_accuracies, label='Validation Accuracy', marker='o')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy (%)')
plt.legend()
plt.tight_layout()
plt.show()