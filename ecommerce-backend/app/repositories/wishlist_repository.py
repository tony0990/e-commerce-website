"""
Wishlist Repository
===================
Handles database operations for user wishlists.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, and_

from app.models.wishlist import Wishlist
from app.repositories.base_repository import BaseRepository

class WishlistRepository(BaseRepository[Wishlist]):
    def __init__(self, db: AsyncSession):
        super().__init__(Wishlist, db)

    async def get_user_wishlist(self, user_id: int) -> List[Wishlist]:
        query = select(Wishlist).where(Wishlist.user_id == user_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def exists(self, user_id: int, product_id: int) -> bool:
        query = select(Wishlist).where(
            and_(Wishlist.user_id == user_id, Wishlist.product_id == product_id)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None
