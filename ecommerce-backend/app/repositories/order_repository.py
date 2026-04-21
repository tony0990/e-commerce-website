"""
Order and Wishlist Repositories (Ahmed)
=======================================
Data access layer for orders and wishlists.
"""

from typing import Optional, Sequence, List
from sqlalchemy import select, func
from app.repositories.base_repository import BaseRepository
from app.models.order import Order, OrderItem
from app.models.wishlist import Wishlist


class OrderRepository(BaseRepository[Order]):
    def __init__(self, db):
        super().__init__(Order, db)

    async def get_user_orders(self, user_id: int) -> Sequence[Order]:
        result = await self.db.execute(
            select(Order).where(Order.user_id == user_id).order_by(Order.created_at.desc())
        )
        return result.scalars().all()

    async def get_stats(self) -> dict:
        """Fetch dashboard statistics."""
        # Total Revenue
        revenue_result = await self.db.execute(select(func.sum(Order.total_amount)))
        total_revenue = revenue_result.scalar() or 0.0
        
        # Total orders
        total_orders = await self.count()
        
        # Pending orders
        pending_result = await self.db.execute(
            select(func.count()).select_from(Order).where(Order.status == "pending")
        )
        pending_orders = pending_result.scalar() or 0
        
        return {
            "total_revenue": total_revenue,
            "total_orders": total_orders,
            "pending_orders": pending_orders
        }

    async def get_sales_per_day(self, days: int = 7) -> List[dict]:
        """Fetch sales data for charts."""
        # Simple implementation for SQLite/MySQL compatibility
        query = select(
            func.date(Order.created_at).label("date"),
            func.sum(Order.total_amount).label("revenue")
        ).group_by("date").order_by("date").limit(days)
        
        result = await self.db.execute(query)
        return [{"date": row.date, "revenue": row.revenue} for row in result.all()]


class WishlistRepository(BaseRepository[Wishlist]):
    def __init__(self, db):
        super().__init__(Wishlist, db)

    async def get_user_wishlist(self, user_id: int) -> Sequence[Wishlist]:
        result = await self.db.execute(
            select(Wishlist).where(Wishlist.user_id == user_id)
        )
        return result.scalars().all()

    async def exists(self, user_id: int, product_id: int) -> bool:
        result = await self.db.execute(
            select(Wishlist).where(Wishlist.user_id == user_id, Wishlist.product_id == product_id)
        )
        return result.scalars().first() is not None
