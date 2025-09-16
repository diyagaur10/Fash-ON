# backend/build_embeddings.py
import os
import numpy as np
import faiss
from pathlib import Path
from db import SessionLocal
from db import Product
from embeddings import get_model, get_transform, open_image_from_path, open_image_from_url, image_to_embedding
from PIL import Image

INDEX_PATH = Path(__file__).resolve().parent / "embeddings.index"
IDMAP_PATH = Path(__file__).resolve().parent / "id_map.npy"

def build_index(image_source_priority=("image_path", "image_url")):
    db = SessionLocal()
    products = db.query(Product).all()
    print(f"Found {len(products)} products in DB")

    device = "cpu"
    model = get_model(device=device)
    transform = get_transform()

    embeddings = []
    id_map = []

    for idx, p in enumerate(products):
        # try local path first, then URL
        img = None
        tried = []
        if p.image_path:
            try:
                img = open_image_from_path(p.image_path)
            except Exception as e:
                tried.append(f"path:{e}")
                img = None
        if img is None and p.image_url:
            try:
                img = open_image_from_url(p.image_url)
            except Exception as e:
                tried.append(f"url:{e}")
                img = None
        if img is None:
            print(f"[skip] product id={p.id} no image ({p.image_path}, {p.image_url}) tried {tried}")
            continue
        try:
            emb = image_to_embedding(img, model, transform, device=device)
            embeddings.append(emb)
            id_map.append(p.id)
            if (len(embeddings) % 100) == 0:
                print(f"Processed {len(embeddings)} images...")
        except Exception as e:
            print(f"Failed embedding for product {p.id}: {e}")
    db.close()

    if not embeddings:
        raise RuntimeError("No embeddings were computed.")

    X = np.vstack(embeddings).astype("float32")
    dim = X.shape[1]
    print(f"Building FAISS index, dim={dim}, n={X.shape[0]}")
    index = faiss.IndexFlatIP(dim)  # using inner product on L2-normalized vectors = cosine
    index.add(X)
    faiss.write_index(index, str(INDEX_PATH))
    np.save(IDMAP_PATH, np.array(id_map, dtype=np.int64))
    print(f"Saved index at {INDEX_PATH} and id_map at {IDMAP_PATH}")

if __name__ == "__main__":
    build_index()
