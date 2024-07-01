# -*- coding: utf-8 -*-
"""ML-GoogleNet.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17t4d37CfopIJk1tLrqn8kzPFsO5mliDN
"""

from google.colab import drive
drive.mount('/content/drive')

import torch
import torchvision
import torch.nn.functional as F
import torch.optim as optim
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

# Mount Google Drive and define device
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

# Define data transformations
transform_train = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(30),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])



from google.colab import drive
drive.mount('/content/drive')

import torch
import torchvision
import torch.nn.functional as F
import torch.optim as optim
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

# Mount Google Drive and define device
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

# Define data transformations
transform_train = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(30),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

transform_test = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Define paths and create data loaders
batch_size = 32
path = '/content/drive/MyDrive/ML/Data'

train_dataset = datasets.ImageFolder(root=f'{path}/train', transform=transform_train)
val_dataset = datasets.ImageFolder(root=f'{path}/val', transform=transform_test)
test_dataset = datasets.ImageFolder(root=f'{path}/test', transform=transform_test)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

print(f'Training set size: {len(train_dataset)}')
print(f'Validation set size: {len(val_dataset)}')
print(f'Test set size: {len(test_dataset)}')
classes = test_dataset.classes
print(f'Classes: {classes}')
# Load pretrained GoogleNet (Inception) model and modify the classifier
googlenet = models.googlenet(pretrained=True)

# Freeze parameters in the convolutional layers
for param in googlenet.parameters():
    param.requires_grad = False

# Modify the classifier
num_features = googlenet.fc.in_features
googlenet.fc = nn.Linear(num_features, len(classes))

googlenet.to(device)

# Hyperparameters
lr = 0.001
epochs = 10
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(googlenet.fc.parameters(), lr=lr)

# Training function
def train(model, train_loader, optimizer, criterion, epochs):
    model.train()
    for epoch in range(epochs):
        running_loss = 0.0
        for inputs, targets in train_loader:
            inputs, targets = inputs.to(device), targets.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * inputs.size(0)
        epoch_loss = running_loss / len(train_loader.dataset)
        print(f"Epoch [{epoch + 1}/{epochs}], Loss: {epoch_loss:.4f}")

# Evaluation function
def evaluate(model, loader):
    model.eval()
    correct = 0
    total = 0
    all_preds = []
    all_labels = []
    with torch.no_grad():
        for inputs, targets in loader:
            inputs, targets = inputs.to(device), targets.to(device)
            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            total += targets.size(0)
            correct += (predicted == targets).sum().item()
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(targets.cpu().numpy())
    accuracy = correct / total * 100
    return accuracy, np.array(all_labels), np.array(all_preds)

# Train the model
train(googlenet, train_loader, optimizer, criterion, epochs)

# Evaluate on training data
train_accuracy, _, _ = evaluate(googlenet, train_loader)
print(f"Accuracy on training data: {train_accuracy:.2f}%")

# Evaluate on test data
test_accuracy, actual_labels, predicted_labels = evaluate(googlenet, test_loader)
print(f"Accuracy on testing data: {test_accuracy:.2f}%")

# Compute metrics
accuracy = accuracy_score(actual_labels, predicted_labels)
precision = precision_score(actual_labels, predicted_labels, average='weighted')
recall = recall_score(actual_labels, predicted_labels, average='weighted')
f1 = f1_score(actual_labels, predicted_labels, average='weighted')

print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1-score: {f1:.2f}")

# Compute confusion matrix
cm = confusion_matrix(actual_labels, predicted_labels)

# Plot and save confusion matrix
fig = plt.gcf()
classes = [str(i) for i in range(1, len(classes) + 1)]
sb.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.title(f'Confusion matrix | Train acc. {np.round(train_accuracy, 2)} | Test acc. {np.round(test_accuracy, 2)}')
plt.draw()
plt.pause(0.01)
fig.savefig("ConfusionMatrixTest.png")
plt.clf()

# Compute confusion matrix
cm = confusion_matrix(actual_labels, predicted_labels)

# Plot and save confusion matrix
fig = plt.gcf()
classes = [str(i) for i in range(1, len(classes) + 1)]
sb.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.title(f'Confusion matrix | Train acc. {np.round(train_accuracy, 2)} | Test acc. {np.round(test_accuracy, 2)}')
plt.draw()
plt.pause(0.01)
fig.savefig("ConfusionMatrixTest.png")
plt.clf()