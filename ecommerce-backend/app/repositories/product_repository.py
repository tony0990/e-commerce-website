"""
Product and Category Repositories (Tony)
=========================================
Data access layer for products and categories.
"""

from typing import Optional, Sequence, List
from sqlalchemy import select, func, or_
from app.repositories.base_repository import BaseRepository
from app.models.product import Product, Category


class ProductRepository(BaseRepository[Product]):
    def __init__(self, db):
        super().__init__(Product, db)

    async def get_all_paged(
        self, 
        page: int = 1, 
        page_size: int = 20, 
        category_id: Optional[int] = None,
        search: Optional[str] = None
    ) -> (Sequence[Product], int):
        skip = (page - 1) * page_size
        query = select(self.model)
        
        if category_id:
            query = query.where(self.model.category_id == category_id)
        if search:
            query = query.where(or_(
                self.model.name.ilike(f"%{search}%"),
                self.model.description.ilike(f"%{search}%")
            ))
            
        # Get total count for pagination
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.db.execute(count_query)
        
        # Get items
        result = await self.db.execute(query.offset(skip).limit(page_size))
        return result.scalars().all(), total.scalar() or 0


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, db):
        super().__init__(Category, db)
        
    async def get_by_name(self, name: str) -> Optional[Category]:
        result = await self.db.execute(select(Category).where(Category.name == name))
        return result.scalars().first()
