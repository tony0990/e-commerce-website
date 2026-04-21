import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.models.product import Category, Product
from app.models.user import User
from app.core.security import hash_password
from app.core.constants import UserRole

async def seed_data():
    """Populate backend database with necessary frontend categories and products."""
    async with AsyncSessionLocal() as db:
        # Seed Admin User if not exists
        admin_res = await db.execute(select(User).where(User.email == "admin@ecommerce.com"))
        if not admin_res.scalars().first():
            db.add(User(
                email="admin@ecommerce.com",
                hashed_password=hash_password("Admin@123456"),
                first_name="Admin",
                last_name="User",
                role=UserRole.ADMIN,
                is_active=True
            ))
            await db.commit()

        # Seed Categories
        categories = ["Furniture", "Electronics", "Fashion", "Home & Living", "Watches"]
        category_map = {}
        for c in categories:
            res = await db.execute(select(Category).where(Category.name == c))
            cat = res.scalars().first()
            if not cat:
                cat = Category(name=c, description=f"{c} items")
                db.add(cat)
                await db.commit()
                await db.refresh(cat)
            category_map[c] = cat.id

        # Seed Products 1 to 60 to match frontend hardcoded IDs matching `cart.items`
        res = await db.execute(select(Product))
        if len(res.scalars().all()) == 0:
            for i in range(1, 60):
                if i < 12: cat_name = "Furniture"
                elif i < 18: cat_name = "Electronics"
                elif i < 30: cat_name = "Fashion"
                elif i < 41: cat_name = "Home & Living"
                else: cat_name = "Watches"
                
                prod = Product(
                    id=i,  # Force ID matching frontend cart
                    name=f"Premium Product #{i}",
                    description="A beautiful premium product.",
                    price=129.99,
                    stock=5000,
                    category_id=category_map[cat_name],
                    image_url=""
                )
                db.add(prod)
            await db.commit()
            print("Successfully seeded categories and products 1-59.")

if __name__ == "__main__":
    asyncio.run(seed_data())
