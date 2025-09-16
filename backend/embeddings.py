# backend/embeddings.py
import torch
import torch.nn as nn
import torchvision.transforms as T
from PIL import Image
import io
import requests
import numpy as np

# Create model - resnet50 backbone
def get_model(device="cpu"):
    import torchvision.models as models
    model = models.resnet50(pretrained=True)
    # remove fc layer: output 2048
    modules = list(model.children())[:-1]  # remove fc
    model = nn.Sequential(*modules)
    model.to(device)
    model.eval()
    return model

# Preprocess for resnet
def get_transform():
    transform = T.Compose([
        T.Resize(256),
        T.CenterCrop(224),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]),
    ])
    return transform

def open_image_from_path(path):
    return Image.open(path).convert("RGB")

def open_image_from_url(url, timeout=10):
    # support protocol-less urls starting with //
    if url and url.startswith("//"):
        url = "https:" + url
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return Image.open(io.BytesIO(r.content)).convert("RGB")

def image_to_embedding(img: Image.Image, model, transform, device="cpu"):
    x = transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        feat = model(x)  # shape (1, 2048, 1, 1)
        feat = feat.reshape(feat.shape[0], -1)  # (1, 2048)
        emb = feat.cpu().numpy()[0]
        # L2 normalize
        norm = np.linalg.norm(emb)
        if norm > 0:
            emb = emb / norm
    return emb.astype("float32")
