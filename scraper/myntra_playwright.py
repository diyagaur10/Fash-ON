# Example scraper placeholder
import asyncio, json, time
from pathlib import Path
from playwright.async_api import async_playwright
from common import download_image

OUT = Path(__file__).resolve().parent / "myntra_products.jsonl"

async def scrape_query(page, query: str, max_pages: int = 2):
    base = f"https://www.myntra.com/{query}"
    products = []
    for p in range(1, max_pages+1):
        url = f"{base}?p={p}"
        await page.goto(url, timeout=120000, wait_until="domcontentloaded")
        cards = await page.locator('.product-base').all()
        print(f"{query} page {p}: found {len(cards)} product cards")
        if cards:
            html = await cards[0].inner_html()
            print(f"First card HTML:\n{html[:500]}")
        for idx, c in enumerate(cards):
            # Robust extraction for each field
            brand, title, price, img, link, img_path = None, None, None, None, None, None
            try:
                brand = await c.locator('.product-brand').inner_text(timeout=5000)
            except Exception as e:
                print(f"    Brand not found for product {idx+1}: {e}")
            try:
                title = await c.locator('.product-product').inner_text(timeout=5000)
            except Exception as e:
                print(f"    Title not found for product {idx+1}: {e}")
            try:
                price = await c.locator('.product-discountedPrice').inner_text(timeout=5000)
            except Exception:
                try:
                    price = await c.locator('.product-price').inner_text(timeout=5000)
                except Exception as e:
                    print(f"    Price not found for product {idx+1}: {e}")
            # Try to get the main image inside the clickable link first, fallback to any img if error or None
            img = None
            try:
                img = await c.locator('a img.img-responsive').first.get_attribute('src', timeout=5000)
            except Exception:
                pass
            if not img:
                try:
                    img = await c.locator('img.img-responsive').first.get_attribute('src', timeout=5000)
                except Exception as e:
                    print(f"    Image not found for product {idx+1}: {e}")
            try:
                link = await c.locator('a').get_attribute('href', timeout=5000)
                if link and not link.startswith('http'):
                    link = 'https://www.myntra.com/' + link.lstrip('/')
            except Exception as e:
                print(f"    Link not found for product {idx+1}: {e}")
            img_path = download_image(img) if img else None
            products.append({
                "source": "myntra",
                "category": query,
                "title": title,
                "brand": brand,
                "price": price,
                "product_url": link,
                "image_url": img,
                "image_path": str(img_path) if img_path else None
            })
            print(f"  Product {idx+1}/{len(cards)} scraped: {brand} - {title}")
        print(f"{query} page {p} completed. {len(products)} products scraped so far.")
        await asyncio.sleep(1.0)  # be polite
    return products

async def main():
    queries = ["dresses", "saree", "tshirts", "jeans", "tops"]
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        with open(OUT, "w", encoding="utf-8") as f:
            for q in queries:
                items = await scrape_query(page, q, max_pages=5)  # increase later
                for it in items:
                    f.write(json.dumps(it, ensure_ascii=False) + "\n")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
