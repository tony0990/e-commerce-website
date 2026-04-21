"""
Enhanced E-Commerce Seeding Script (Tony)
=========================================
Populates the database with 20 unique products per category.
Uses specific high-quality Unsplash image IDs.
"""

import asyncio
import random
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal, engine, Base, create_tables, drop_tables
from app.models.product import Category, Product


# --- Category Data ---
CATEGORIES = [
    {
        "name": "Electronics",
        "description": "Cutting-edge gadgets, computing, and high-performance tech.",
        "image_url": "https://images.unsplash.com/photo-1498049794561-7780e7231661?auto=format&fit=crop&w=1200&q=80"
    },
    {
        "name": "Fashion",
        "description": "Trendy apparel, designer wear, and premium accessories.",
        "image_url": "https://images.unsplash.com/photo-1445205170230-053b83016050?auto=format&fit=crop&w=1200&q=80"
    },
    {
        "name": "Home & Living",
        "description": "Modern furniture, elegant decor, and home essentials.",
        "image_url": "https://images.unsplash.com/photo-1484101403633-562f891dc89a?auto=format&fit=crop&w=1200&q=80"
    }
]

# --- Image ID Pools (Unsplash) ---
ELECTRONICS_IDS = [
    "photo-1496181133206-80ce9b88a853", "photo-1544244015-0df4b3ffc6b0", "photo-1505740420928-5e560c06d30e",
    "photo-1516035069371-29a1b244cc32", "photo-1523275335684-37898b6baf30", "photo-1511707171634-5f897ff02aa9",
    "photo-1545454675-3531b543be5d", "photo-1511467687858-23d96c32e4ae", "photo-1527443224154-c4a3942d3acf",
    "photo-1473966968600-fa801b869a1a", "photo-1622979135225-d2ba269cf1ac", "photo-1550009158-9ebf6d1706da",
    "photo-1588872657578-7efd1f1555ed", "photo-1526733160212-073c880839e5", "photo-1531297484001-80022131f5a1",
    "photo-1518770660439-4636190af475", "photo-1519389950473-47ba0277781c", "photo-1555527633-ee380c4e7239",
    "photo-1556656793-062ff9f1b7cd", "photo-1563013544-824ae1b704d3"
]

FASHION_IDS = [
    "photo-1551028719-00167b16eac5", "photo-1549298916-b41d501d3772", "photo-1572635196237-14b3f281503f",
    "photo-1524592094714-0f0654e20314", "photo-1539008835270-38361001550a", "photo-1584917033904-49122ea54670",
    "photo-1541643600914-78b084683601", "photo-1514327605112-b887c0e61c0a", "photo-1594938298603-c8148c4dae35",
    "photo-1515562141207-7a88bb7ce338", "photo-1556906781-9a412961c28c", "photo-1491553895911-0055eca6402d",
    "photo-1434389677669-e08b4cac3105", "photo-1503342217505-b0a15ec3261c", "photo-1523381235208-27d246304ca3",
    "photo-1520006403909-838d6b92c22e", "photo-1515886657613-9f3515b0c78f", "photo-1483985988355-763728e1935b",
    "photo-1490481651871-ab68ee25d43d", "photo-1516762689617-e1cffcef479d"
]

HOME_IDS = [
    "photo-1567538096630-e0c55bd6374c", "photo-1507473885765-e6ed45770d71", "photo-1544457070-4cd773b4d71e",
    "photo-1505691938895-1758d7eaa511", "photo-1555041469-a586c61ea9bc", "photo-1485955900006-10f4d324d411",
    "photo-1556910103-1c02745aae4d", "photo-1580210006596-f38fcb2f7678", "photo-1563861826100-9cb868fdbe1c",
    "photo-1513694203232-719a280e022f", "photo-1586023492125-27b2c045efd7", "photo-1522770179533-24471fcdba45",
    "photo-1513519247388-19345420d169", "photo-1583847268964-b28dc8f51f92", "photo-1581783898377-1c85bf937427",
    "photo-1540932239986-30128078f3c5", "photo-1519710192539-74b56d42c46a", "photo-1533090161767-e6ffed986c88",
    "photo-1512918728675-ed5a9ecdebfd", "photo-1524758631624-e2822e304c36"
]


async def seed():
    print("[*] Starting database refresh and seeding...")
    # Drop and recreate tables to ensure a clean state
    await drop_tables()
    await create_tables()

    async with AsyncSessionLocal() as db:
        # 1. Create Categories
        category_map = {}
        for cat_data in CATEGORIES:
            cat = Category(**cat_data)
            db.add(cat)
            await db.flush()
            category_map[cat.name] = cat.id
            print(f"  + Added Category: {cat.name}")

        # 2. Add Electronics Products
        print("  + Adding 20 Electronics products...")
        cat_id = category_map["Electronics"]
        for i, img_id in enumerate(ELECTRONICS_IDS):
            prod = Product(
                name=f"Premium Electronic Item {i+1}",
                description=f"High-quality electronic device with cutting-edge features. Modern design and exceptional performance for tech enthusiasts.",
                price=float(random.randint(99, 1499)),
                stock=random.randint(10, 50),
                category_id=cat_id,
                image_url=f"https://images.unsplash.com/{img_id}?auto=format&fit=crop&w=800&q=80"
            )
            db.add(prod)

        # 3. Add Fashion Products
        print("  + Adding 20 Fashion products...")
        cat_id = category_map["Fashion"]
        for i, img_id in enumerate(FASHION_IDS):
            prod = Product(
                name=f"Designer Fashion Piece {i+1}",
                description=f"Elegant and trendy apparel designed for comfort and style. Made from premium materials for a sophisticated look.",
                price=float(random.randint(45, 499)),
                stock=random.randint(20, 100),
                category_id=cat_id,
                image_url=f"https://images.unsplash.com/{img_id}?auto=format&fit=crop&w=800&q=80"
            )
            db.add(prod)

        # 4. Add Home Products
        print("  + Adding 20 Home & Living products...")
        cat_id = category_map["Home & Living"]
        for i, img_id in enumerate(HOME_IDS):
            prod = Product(
                name=f"Modern Home Essential {i+1}",
                description=f"Beautifully crafted home decor and furniture to elevate your living space. Functional design meets artisanal quality.",
                price=float(random.randint(30, 999)),
                stock=random.randint(5, 30),
                category_id=cat_id,
                image_url=f"https://images.unsplash.com/{img_id}?auto=format&fit=crop&w=800&q=80"
            )
            db.add(prod)

        await db.commit()
        print("[*] Seeding completed successfully with 60 products!")


if __name__ == "__main__":
    asyncio.run(seed())
