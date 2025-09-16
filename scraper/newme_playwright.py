import os
import json
import uuid
import asyncio
import requests
from playwright.async_api import async_playwright

OUTPUT_DIR = "D:\\FashON\\fashion-search\\backend\\data"
IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")
JSON_PATH = os.path.join(OUTPUT_DIR, "newme_products.json")

os.makedirs(IMAGE_DIR, exist_ok=True)

async def scrape_newme():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        all_products = []

        for page_num in range(1, 3):  # scrape first 2 pages
            url = f"https://newme.asia/womens-collection/bottoms?page={page_num}"
            print(f"\n🔎 Scraping Page {page_num}: {url}")
            await page.goto(url, timeout=60000)

            # Scroll to load all products
            previous_height = None
            for _ in range(5):  # scroll 5 times
                current_height = await page.evaluate("document.body.scrollHeight")
                if current_height == previous_height:
                    break
                previous_height = current_height
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(2)

            # Wait for at least one product to appear
            product_cards = page.locator(".product-card")
            try:
                await product_cards.first.wait_for(state="visible", timeout=60000)
            except:
                print("⚠️ No products found on this page.")
                continue

            count = await product_cards.count()
            print(f"Found {count} products on page {page_num}")

            for idx in range(count):
                card = product_cards.nth(idx)
                try:
                    title = await card.locator("h3.product-title").inner_text()
                except:
                    title = None
                try:
                    brand = await card.locator(".brand-name").inner_text()
                except:
                    brand = "Newme"
                try:
                    price = await card.locator(".product-price").inner_text()
                except:
                    price = None
                try:
                    product_url = await card.locator("a").get_attribute("href")
                    if product_url and not product_url.startswith("http"):
                        product_url = "https://newme.asia" + product_url
                except:
                    product_url = None
                try:
                    image_url = await card.locator("img").get_attribute("src")
                except:
                    image_url = None

                # Download image
                image_path = None
                if image_url:
                    try:
                        img_data = requests.get(image_url, timeout=10).content
                        image_filename = f"{uuid.uuid4().hex[:12]}.jpg"
                        image_path = os.path.join(IMAGE_DIR, image_filename)
                        with open(image_path, "wb") as f:
                            f.write(img_data)
                    except:
                        image_path = None

                product_data = {
                    "source": "newme",
                    "category": "bottoms",
                    "title": title,
                    "brand": brand,
                    "price": price,
                    "product_url": product_url,
                    "image_url": image_url,
                    "image_path": image_path,
                }

                print(f"    Product {idx+1}: {title} | {price}")
                all_products.append(product_data)

        await browser.close()

        # Save JSON
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(all_products, f, indent=4, ensure_ascii=False)

        print(f"\n✅ Saved {len(all_products)} products to {JSON_PATH}")


if __name__ == "__main__":
    asyncio.run(scrape_newme())
