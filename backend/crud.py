# backend/crud.py
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_
from db import Product

def get_products(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    query: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
) -> Tuple[List[Product], int]:
    q = db.query(Product)
    if category:
        q = q.filter(Product.category.ilike(f"%{category}%"))
    if brand:
        q = q.filter(Product.brand.ilike(f"%{brand}%"))
    if query:
        q = q.filter(or_(
            Product.title.ilike(f"%{query}%"),
            Product.brand.ilike(f"%{query}%")
        ))
    # price_min / price_max filtering needs parsing price_raw -> skipping for now or simple numeric extraction
    total = q.count()
    items = q.offset(skip).limit(limit).all()
    return items, total

def get_products_by_ids(db: Session, ids: List[int]):
    return db.query(Product).filter(Product.id.in_(ids)).all()
