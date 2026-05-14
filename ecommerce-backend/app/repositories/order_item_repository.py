"""
Order Item Repository
=====================
Database operations for order items only.
"""

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order_item import OrderItem


class OrderItemRepository:
    """
    Repository layer for OrderItem model.
    Handles database operations only.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_many(
        self,
        items: List[OrderItem],
    ) -> List[OrderItem]:
        """
        Insert multiple order items into the database.

        Example:
        One order may contain many products,
        so we insert all OrderItem rows together.
        """
        self.db.add_all(items)

        await self.db.flush()

        for item in items:
            await self.db.refresh(item)

        return items

    async def get_by_order_id(
        self,
        order_id: int,
    ) -> List[OrderItem]:
        """
        Get all items that belong to one order.
        """
        result = await self.db.execute(
            select(OrderItem)
            .where(OrderItem.order_id == order_id)
        )

        return list(result.scalars().all())