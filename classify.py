import os
import torch
import torch.nn as nn
import numpy as np
from PIL import Image
from torchvision import transforms, models

device_name = "cuda:0:" if torch.cuda.is_available() else "cpu"
device = torch.device(device_name)

resnet_model = models.resnet50(pretrained=True)

for param in resnet_model.parameters():
    param.requires_grad = True

n_inputs = resnet_model.fc.in_features

resnet_model.fc = nn.Sequential(nn.Linear(n_inputs, 2048),
                nn.LeakyReLU(negative_slope=0.2),
                nn.Dropout(p=0.4),
                nn.Linear(2048, 2048),
                nn.LeakyReLU(negative_slope=0.2),
                nn.Dropout(p=0.4),
                nn.Linear(2048, 3),
                nn.LogSoftmax(dim=1))

for name, child in resnet_model.named_children():
    for name2, params in child.named_parameters():
        params.requires_grad = True

resnet_model.to(device)

resnet_model.load_state_dict(torch.load('models/bt_total_resnet_torch.pt',map_location=torch.device('cpu')))

resnet_model.eval()

transform = transforms.Compose([transforms.Resize((512, 512)), transforms.ToTensor()])

LABELS = ['Meningioma', 'Glioma', 'Pitutary']


def classify(img_name):
    if not os.path.exists(img_name):
        print("File does not exits. Exiting...\n")
        exit()
    
    img = Image.open(img_name)
    
    img = transform(img)
    
    img = img[None, ...]
    
    if device_name=="cuda:0:":
        img = img.cuda()
    
    with torch.no_grad():
        y_hat = resnet_model.forward(img)
    
        predicted = torch.max(y_hat.data, 1)[1] 
    
        return(LABELS[predicted.data])