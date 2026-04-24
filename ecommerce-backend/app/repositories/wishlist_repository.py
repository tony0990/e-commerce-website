"""
Wishlist Repository (Ahmed)
==========================
Data access layer for user wishlists.
"""

from typing import Sequence
from sqlalchemy import select
from app.repositories.base_repository import BaseRepository
from app.models.wishlist import Wishlist


class WishlistRepository(BaseRepository[Wishlist]):
    def __init__(self, db):
        super().__init__(Wishlist, db)

    async def get_user_wishlist(self, user_id: int) -> Sequence[Wishlist]:
        """Fetch all wishlist items for a user including product data."""
        from sqlalchemy.orm import joinedload
        result = await self.db.execute(
            select(Wishlist)
            .where(Wishlist.user_id == user_id)
            .options(joinedload(Wishlist.product))
        )
        return result.scalars().all()

    async def exists(self, user_id: int, product_id: int) -> bool:
        """Check if a product is already in user's wishlist."""
        result = await self.db.execute(
            select(Wishlist).where(
                Wishlist.user_id == user_id, 
                Wishlist.product_id == product_id
            )
        )
        return result.scalars().first() is not None
