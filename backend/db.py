from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# Use SQLite for MVP
DB_URL = "sqlite:///./products.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(32), index=True)
    category = Column(String(64), index=True)
    title = Column(Text)
    brand = Column(String(128), index=True)
    price_raw = Column(String(64))
    product_url = Column(Text)
    image_url = Column(Text)
    image_path = Column(Text)

def init_db():
    Base.metadata.create_all(bind=engine)
