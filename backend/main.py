# backend/main.py
import os
from fastapi import FastAPI, HTTPException, Query, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from sqlalchemy.orm import Session
from db import SessionLocal
from crud import get_products, get_products_by_ids
from schemas import ProductOut, SearchResult
import numpy as np
import faiss
from embeddings import get_model, get_transform, open_image_from_path, open_image_from_url, image_to_embedding
from PIL import Image
import io
import requests

INDEX_PATH = os.path.join(os.path.dirname(__file__), "embeddings.index")
IDMAP_PATH = os.path.join(os.path.dirname(__file__), "id_map.npy")

app = FastAPI(title="Product API with Image Search")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# load FAISS index and idmap on startup
@app.on_event("startup")
def startup_event():
    global faiss_index, id_map, model, transform
    faiss_index = None
    id_map = None
    model = get_model(device="cpu")
    transform = get_transform()

    if os.path.exists(INDEX_PATH) and os.path.exists(IDMAP_PATH):
        faiss_index = faiss.read_index(INDEX_PATH)
        id_map = np.load(IDMAP_PATH)
        print(f"Loaded FAISS index with n={faiss_index.ntotal}")
    else:
        print("FAISS index or id_map not found; image search disabled.")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/products", response_model=List[ProductOut])
def list_products(
    skip: int = 0,
    limit: int = 50,
    category: Optional[str] = Query(None),
    brand: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
):
    db = next(get_db())
    items, total = get_products(db, skip=skip, limit=limit, category=category, brand=brand, query=q)
    return items

@app.post("/search/image", response_model=List[SearchResult])
def search_by_image(file: UploadFile = File(None), image_url: Optional[str] = Form(None), top_k: int = Form(5)):
    if faiss_index is None:
        raise HTTPException(status_code=503, detail="Image search index not available")

    # load image either from uploaded file or from image_url
    img = None
    if file:
        contents = file.file.read()
        img = Image.open(io.BytesIO(contents)).convert("RGB")
    elif image_url:
        try:
            img = open_image_from_url(image_url)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to fetch image from URL: {e}")
    else:
        raise HTTPException(status_code=400, detail="Provide file upload or image_url")

    emb = image_to_embedding(img, model, transform, device="cpu").astype("float32")
    emb = np.expand_dims(emb, axis=0)
    # Search
    D, I = faiss_index.search(emb, top_k)
    scores = D[0]
    inds = I[0]
    # map indices to product ids
    product_ids = []
    for i in inds:
        if i < 0:
            continue
        product_ids.append(int(id_map[int(i)]))
    # fetch products
    db = next(get_db())
    products = get_products_by_ids(db, product_ids)
    # reorder products to match scores order
    prod_map = {p.id: p for p in products}
    results = []
    for pid, score in zip(product_ids, scores.tolist()):
        p = prod_map.get(pid)
        if p:
            results.append({"product": p, "score": float(score)})
    return results

@app.get("/health")
def health():
    return {"ok": True}
