from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.category import Category

class CategoryRepository:
    # Handles all direct database operations for Categories
    
    @staticmethod
    async def get_all_active(db: AsyncSession):
        result = await db.execute(select(Category).filter(Category.is_active == True))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, category_id: int):
        result = await db.execute(select(Category).filter(Category.id == category_id))
        return result.scalars().first()

    @staticmethod
    async def get_by_name_or_slug(db: AsyncSession, name: str, slug: str):
        result = await db.execute(
            select(Category).filter((Category.name == name) | (Category.slug == slug))
        )
        return result.scalars().first()

    @staticmethod
    async def create(db: AsyncSession, category: Category):
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return category

    @staticmethod
    async def update(db: AsyncSession, category: Category):
        await db.commit()
        await db.refresh(category)
        return category

    @staticmethod
    async def delete(db: AsyncSession, category: Category):
        await db.delete(category)
        await db.commit()