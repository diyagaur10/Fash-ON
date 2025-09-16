import json
from pathlib import Path
from db import init_db, SessionLocal, Product

def ingest_file(jsonl_file_path):
    """Ingest a JSONL file into the database"""
    init_db()  # creates tables if not exist
    db = SessionLocal()

    with open(jsonl_file_path, "r", encoding="utf-8") as f:
        for line in f:
            o = json.loads(line)
            product = Product(
                source=o.get("source"),
                category=o.get("category"),
                title=o.get("title"),
                brand=o.get("brand"),
                price_raw=o.get("price"),
                product_url=o.get("product_url"),
                image_url=o.get("image_url"),
                image_path=o.get("image_path"),
            )
            db.add(product)

    db.commit()
    db.close()
    print(f"Finished ingesting {jsonl_file_path.name}")

def run():
    scraper_dir = Path(__file__).resolve().parent.parent / "scraper"
    
    # List all scraped JSONL files
    files = ["myntra_products.jsonl", "newme_products.jsonl", "littlebox_products.jsonl", "savana_products.jsonl"]
    
    for file_name in files:
        jsonl_path = scraper_dir / file_name
        if jsonl_path.exists():
            ingest_file(jsonl_path)
        else:
            print(f"{file_name} not found!")

if __name__ == "__main__":
    run()
