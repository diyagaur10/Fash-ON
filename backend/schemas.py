# backend/schemas.py
from pydantic import BaseModel
from typing import Optional

class ProductOut(BaseModel):
    id: int
    source: Optional[str]
    category: Optional[str]
    title: Optional[str]
    brand: Optional[str]
    price_raw: Optional[str]
    product_url: Optional[str]
    image_url: Optional[str]
    image_path: Optional[str]

    class Config:
        orm_mode = True

class SearchResult(BaseModel):
    product: ProductOut
    score: float
