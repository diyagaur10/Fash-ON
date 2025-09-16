# Example scraper placeholder 
import asyncio, json, time
from pathlib import Path
from playwright.async_api import async_playwright
from common import download_image  # <-- already have this

import asyncio
from playwright.async_api import async_playwright
import json

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.savana.com/")
        await page.wait_for_selector('a.VerticalCard--verticalCard--wIhJb_3')
        product_cards = await page.query_selector_all('a.VerticalCard--verticalCard--wIhJb_3')
        products = []
        category_urls = {
            "dresses": "https://www.savana.com/activity/dresses-12023",
            "t-shirts": "https://www.savana.com/activity/t-shirts-12024",
            "tops-and-blouses": "https://www.savana.com/activity/tops-and-blouses-12025",
            "denim": "https://www.savana.com/activity/fresh-fits-in-denim-12026",
            "co-ords": "https://www.savana.com/activity/co-ords-12027",
            "bottoms": "https://www.savana.com/activity/bottoms-12028"
        }
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            products = []
            for category, url in category_urls.items():
                print(f"Scraping category: {category}")
                await page.goto(url)
                await page.wait_for_selector('a.VerticalCard--verticalCard--wIhJb_3')
                product_cards = await page.query_selector_all('a.VerticalCard--verticalCard--wIhJb_3')
                for card in product_cards:
                    title = await card.eval_on_selector('.VerticalCard--title--cwLz4Yd', 'el => el.textContent')
                    product_url = await card.get_attribute('href')
                    img = await card.query_selector('img.ub-image-img')
                    image_url = await img.get_attribute('src') if img else None
                    
                    # ✅ Download image and store local path (like Myntra)
                    image_path = download_image(image_url) if image_url else None
                    
                    price = None
                    if await card.query_selector('.BigSalePrice--bigSalePrice--X7V_adN'):
                        price = await card.eval_on_selector('.BigSalePrice--bigSalePrice--X7V_adN', 'el => el.textContent')
                    elif await card.query_selector('.BigSalePrice--price--eOCHVb7'):
                        price = await card.eval_on_selector('.BigSalePrice--price--eOCHVb7', 'el => el.textContent')
                    
                    # Extract color options for metadata (unchanged)
                    color_options = []
                    color_elements = await card.query_selector_all('.ColorPalette--color--N0gEXPg')
                    for color_el in color_elements:
                        color_name = await color_el.get_attribute('title')
                        color_img_el = await color_el.query_selector('img')
                        color_img_url = await color_img_el.get_attribute('src') if color_img_el else None
                        if color_name and color_img_url:
                            color_options.append({
                                "name": color_name,
                                "image_url": color_img_url
                            })
                    color_img = await card.query_selector('.ColorPalette--chosen--N0gEXPg img')
                    color = await color_img.get_attribute('alt') if color_img else None
                    
                    products.append({
                        "source": "savana",
                        "category": category,
                        "title": title,
                        "brand": "Savana",
                        "price": price,
                        "product_url": product_url,
                        "image_url": image_url,
                        "image_path": str(image_path) if image_path else None  # ✅ new field
                    })
        with open("savana_products.jsonl", "w", encoding="utf-8") as f:
            for product in products:
                f.write(json.dumps(product, ensure_ascii=False) + "\n")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
