import time
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms

# start timer
start = time.time()

# data loading
transform = transforms.ToTensor()
train_loader = torch.utils.data.DataLoader(
    datasets.MNIST('.', download=True, train=True, transform=transform),
    batch_size=64,
    shuffle=True
)

# define a tiny model
model = nn.Sequential(
    nn.Flatten(),
    nn.Linear(28 * 28, 128),
    nn.ReLU(),
    nn.Linear(128, 10)
)

loss_fn = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# train for 1 epoch
model.train()
for batch_idx, (data, target) in enumerate(train_loader):
    optimizer.zero_grad()
    output = model(data)
    loss = loss_fn(output, target)
    loss.backward()
    optimizer.step()
    if batch_idx % 100 == 0:
        print(f'Batch {batch_idx}, Loss: {loss.item()}')

# end timer
end = time.time()
print(f"\n🕒 Training time: {round(end - start, 2)} seconds")
