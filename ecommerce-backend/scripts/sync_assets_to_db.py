import asyncio
import os
import sys
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

# Add parent directory to path to import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import settings
from app.models.product import Category, Product

# Define the asset manifest (Synchronized from frontend/js/products-data.js)
asset_manifest = [
    {"cat": "Electronics", "file": "10 Game-Changing Gadget Gifts Your Dad Will___.jpg", "folder": "electronics"},
    {"cat": "Electronics", "file": "25w Pd Schnell Ladegerät Für Ulefone Rugking 5 Pro Typ-c Lader Netzteil Charger.jpg", "folder": "electronics"},
    {"cat": "Electronics", "file": "Acoustic Energy 300 Series Speakers.jpg", "folder": "electronics"},
    {"cat": "Electronics", "file": "JBL Charge 3 Waterproof Bluetooth Speaker -Black (Renewed).jpg", "folder": "electronics"},
    {"cat": "Electronics", "file": "Portable Charger Power Bank 40800mAh with 3 Built-in Cables.jpg", "folder": "electronics"},
    {"cat": "Electronics", "file": "Solo il Meglio dalle Notizie _ StraNotizie_it.jpg", "folder": "electronics"},
    {"cat": "Electronics", "file": "electronics.png", "folder": "electronics"},
    
    {"cat": "Fashion", "file": "8 TÊNIS MASCULINOS para TRABALHAR - Modelos Versáteis de Sneakers Masculinos.jpg", "folder": "fashion"},
    {"cat": "Fashion", "file": "Letter Embossed Square Bag.jpg", "folder": "fashion"},
    {"cat": "Fashion", "file": "Louis Vuitton Bag.jpg", "folder": "fashion"},
    {"cat": "Fashion", "file": "Men's Minimalist Pure White Outdoor Casual Flat Sneakers, Lightweight Daily Versatile Lace-Up Skate Shoes, Student Hiking Shoes, Couple Casual White Shoes.jpg", "folder": "fashion"},
    {"cat": "Fashion", "file": "Negro elegante.jpg", "folder": "fashion"},
    {"cat": "Fashion", "file": "Round Neck Knitted Pullover Sweater - Dark Gray _ L.jpg", "folder": "fashion"},
    {"cat": "Fashion", "file": "Saint Laurent Classic Monogram Leather Tote _ Bragmybag.jpg", "folder": "fashion"},
    {"cat": "Fashion", "file": "Sara _ Pletený Sveter - Hnedá _ Biela _ 2XL.jpg", "folder": "fashion"},
    {"cat": "Fashion", "file": "ZITY Flannel Plaid Shirt for Men Regular Fit Long Sleeve Casual Button Down Shirts 07-Grey 3XL at Amazon Men’s Clothing store.jpg", "folder": "fashion"},
    {"cat": "Fashion", "file": "black bag.jpg", "folder": "fashion"},
    {"cat": "Fashion", "file": "download (25).jpg", "folder": "fashion"},
    {"cat": "Fashion", "file": "download (26).jpg", "folder": "fashion"},
    {"cat": "Fashion", "file": "download.jpg", "folder": "fashion"},
    {"cat": "Fashion", "file": "fashion.png", "folder": "fashion"},
    {"cat": "Fashion", "file": "👜 Wholesale PU Leather Hand Bags for Women! ✨__Elevate your style with our elegant candy-patterned tote bag_ This luxury designer handbag features a zipper closure and a casual tote shape, perfect for any occasion.jpg", "folder": "fashion"},

    {"cat": "Furniture", "file": "product_chair_1776804395107.png", "folder": "chair"},
    {"cat": "Home & Living", "file": "home.png", "folder": "home"},
    {"cat": "Watches", "file": "Maurice Lacroix Watch Pontos S Mens  PT6008-SS001-331-1 Watch.jpg", "folder": "watch"},
    {"cat": "Watches", "file": "Men's Watches _ Nordstrom.jpg", "folder": "watch"},
    {"cat": "Watches", "file": "Stainless Steel Business Casual Quartz Wristwatch And 1pc Link Chain Bracelet Set For Men.jpg", "folder": "watch"},
    {"cat": "Watches", "file": "Tissot Couturier Men's Watch Chronograph Quartz T0356171605100, Black, Strap_.jpg", "folder": "watch"},
    {"cat": "Watches", "file": "watch.png", "folder": "watch"},
    {"cat": "Watches", "file": "Womens Rolex Datejust Watch 16200 _ 36Mm _ Blue Mother Of Pearl Roman.jpg", "folder": "watch"},
    {"cat": "Watches", "file": "Womens Rolex Datejust Watch 16233 _ 36Mm _ Pink Roman Dial _ Jubilee B.jpg", "folder": "watch"}
]

def clean_name(filename):
    name = filename.split('.')[0]
    name = name.replace('-', ' ').replace('_', ' ')
    # Simple regex-like cleanup without importing re for speed
    import re
    name = re.sub(r'\d+', '', name)
    name = re.sub(r'\(.*\)', '', name)
    name = re.sub(r'download|category|product|amazon|nordstrom|mens|womens|wholesale|leather|monogram|classic|regular|fit|long|sleeve|casual|button|down|shirts|store|with|our|elegant|candy|patterned|tote|bag|this|luxury|designer|handbag|features|a|zipper|closure|and|shape|perfect|for|any|occasion', '', name, flags=re.IGNORECASE)
    name = ' '.join(name.split())
    return name.title() or "Premium Discovery Item"

async def sync():
    engine = create_async_engine(settings.DATABASE_URL)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with AsyncSessionLocal() as session:
        print("[*] Synchronizing Discovery Assets to Database...")
        
        # 1. Create/Get Categories
        categories = {}
        for cat_name in set(item["cat"] for item in asset_manifest):
            result = await session.execute(select(Category).where(Category.name == cat_name))
            category = result.scalars().first()
            if not category:
                category = Category(name=cat_name, description=f"Explore our curated {cat_name} collection.")
                session.add(category)
                await session.flush()
                print(f" [+] Created Category: {cat_name}")
            categories[cat_name] = category

        # 2. Add Products
        added_count = 0
        for item in asset_manifest:
            # Check if product exists (by filename in image_url)
            img_url = f"assets/{item['folder']}/{item['file']}"
            result = await session.execute(select(Product).where(Product.image_url == img_url))
            if not result.scalars().first():
                product = Product(
                    category_id=categories[item["cat"]].id,
                    name=clean_name(item["file"]),
                    description="A masterpiece of modern design and utility. This premium discovery blends aesthetic perfection with uncompromising performance.",
                    price=float(f"{os.urandom(1)[0] % 500 + 45}.99"),
                    stock=100,
                    image_url=img_url,
                    is_active=True
                )
                session.add(product)
                added_count += 1

        await session.commit()
        print(f"[*] Done! Added {added_count} new products to the database.")

if __name__ == "__main__":
    asyncio.run(sync())
