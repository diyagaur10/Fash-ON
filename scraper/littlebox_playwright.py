import asyncio
import re
import json
import aiohttp
import hashlib
from pathlib import Path
from playwright.async_api import async_playwright

# Output paths
OUTPUT_FILE = Path(r"D:\FashON\fashion-search\scraper\littlebox_products.jsonl")
IMAGES_DIR = Path(r"D:\FashON\fashion-search\backend\data\images")
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Collections to scrape
COLLECTIONS = [
    "dresses",
    "tops",
    "bottoms",
    "outerwear",
    # Add more collections as needed
]

async def download_image(session, url):
    """Download image and save with unique hash name."""
    try:
        async with session.get(url) as resp:
            if resp.status == 200:
                content = await resp.read()
                image_hash = hashlib.md5(content).hexdigest()
                ext = url.split("?")[0].split(".")[-1]
                image_path = IMAGES_DIR / f"{image_hash}.{ext}"
                with open(image_path, "wb") as f:
                    f.write(content)
                return str(image_path)
    except Exception as e:
        print(f"Failed to download {url}: {e}")
    return ""

async def scrape_collection(page, session, collection_url):
    all_products = []
    page_number = 1

    while True:
        url = f"{collection_url}?page={page_number}"
        print(f"Scraping Page {page_number}: {url}")

        try:
            await page.goto(url, timeout=30000)
        except:
            print("Failed to load page or timeout.")
            break

        try:
            await page.wait_for_selector(".product-block", timeout=10000)
        except:
            print("No more products found or page timeout.")
            break

        product_blocks = await page.query_selector_all(".product-block")
        if not product_blocks:
            break

        for block in product_blocks:
            title_el = await block.query_selector(".product-block__title")
            title = await title_el.inner_text() if title_el else "No title"

            price_el = await block.query_selector(".product-price")
            price = await price_el.inner_text() if price_el else "No price"

            url_el = await block.query_selector("a[href*='/products/']")
            product_url = await url_el.get_attribute("href") if url_el else "No URL"
            if product_url and not product_url.startswith("http"):
                product_url = "https://littleboxindia.com" + product_url

            # Extract image URL from <img> tag
            image_el = await block.query_selector("img.rimage__image")
            image_url = ""
            if image_el:
                src = await image_el.get_attribute("data-srcset")
                if src:
                    urls = [u.strip().split(" ")[0] for u in src.split(",")]
                    image_url = "https:" + urls[-1] if urls else ""

            # Download image
            image_path = await download_image(session, image_url) if image_url else ""

            brand = "Littlebox India"
            category = collection_url.split("/")[-1]

            all_products.append({
                "source": "littlebox",
                "category": category,
                "title": title.strip(),
                "brand": brand,
                "price": price.strip(),
                "product_url": product_url,
                "image_url": image_url,
                "image_path": image_path
            })

        page_number += 1

    return all_products

async def main():
    all_products = []
    async with async_playwright() as p, aiohttp.ClientSession() as session:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for collection in COLLECTIONS:
            collection_url = f"https://littleboxindia.com/collections/{collection}"
            products = await scrape_collection(page, session, collection_url)
            all_products.extend(products)

        await browser.close()

    # Save all products to JSONL
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for product in all_products:
            f.write(json.dumps(product, ensure_ascii=False) + "\n")

    print(f"Scraping completed! {len(all_products)} products saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(main())
