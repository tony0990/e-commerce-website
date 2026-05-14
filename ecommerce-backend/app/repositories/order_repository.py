"""
Order Repository
================
Database operations for orders only.

This repository does not contain business logic.
It only reads/writes Order data from the database.

Important:
OrderResponse returns:
Order -> items -> product -> category

So we eager-load all required relationships using selectinload.
We also use populate_existing=True to force SQLAlchemy to reload relationships
after creating order items in the same session.
"""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.constants import OrderStatus
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product


class OrderRepository:
    """
    Repository layer for Order model.

    Handles:
    - create order
    - get order by id
    - get user order
    - get all user orders
    - get all orders
    - update status
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    def _order_load_options(self):
        """
        Common eager-loading options for order responses.

        Loads:
        - order.user
        - order.items
        - order.items.product
        - order.items.product.category

        This prevents MissingGreenlet errors during Pydantic serialization.
        """

        return (
            selectinload(Order.user),
            selectinload(Order.items)
            .selectinload(OrderItem.product)
            .selectinload(Product.category),
        )

    async def create(self, order: Order) -> Order:
        """
        Add a new order to the database.

        We do not commit here.
        Commit/rollback is handled by the database session lifecycle.
        """

        self.db.add(order)
        await self.db.flush()
        await self.db.refresh(order)

        return order

    async def get_by_id(self, order_id: int) -> Optional[Order]:
        """
        Get one order by ID with all response relationships loaded.

        populate_existing=True is important after creating order items
        in the same session because SQLAlchemy may otherwise return
        a cached Order object with empty items.
        """

        result = await self.db.execute(
            select(Order)
            .options(*self._order_load_options())
            .where(Order.id == order_id)
            .execution_options(populate_existing=True)
        )

        return result.scalar_one_or_none()

    async def get_user_order(
        self,
        order_id: int,
        user_id: int,
    ) -> Optional[Order]:
        """
        Get one order that belongs to a specific user.

        This prevents users from accessing orders that do not belong to them.
        """

        result = await self.db.execute(
            select(Order)
            .options(*self._order_load_options())
            .where(
                Order.id == order_id,
                Order.user_id == user_id,
            )
            .execution_options(populate_existing=True)
        )

        return result.scalar_one_or_none()

    async def get_orders_by_user(self, user_id: int) -> List[Order]:
        """
        Get all orders for one user.
        Used by GET /orders/me.
        """

        result = await self.db.execute(
            select(Order)
            .options(*self._order_load_options())
            .where(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .execution_options(populate_existing=True)
        )

        return list(result.scalars().unique().all())

    async def get_all(self) -> List[Order]:
        """
        Get all orders.
        Admin-only usage.
        """

        result = await self.db.execute(
            select(Order)
            .options(*self._order_load_options())
            .order_by(Order.created_at.desc())
            .execution_options(populate_existing=True)
        )

        return list(result.scalars().unique().all())

    async def update_status(
        self,
        order: Order,
        new_status: OrderStatus,
    ) -> Order:
        """
        Update order status only.

        Status transition validation happens in the service layer.
        """

        order.status = new_status

        await self.db.flush()
        await self.db.refresh(order)

        refreshed_order = await self.get_by_id(order.id)

        return refreshed_order

    async def get_stats(self) -> dict:
        """
        Get basic order statistics: total revenue, total orders, pending orders.
        """
        from sqlalchemy import func

        result_revenue = await self.db.execute(select(func.sum(Order.total_amount)))
        total_revenue = result_revenue.scalar() or 0.0

        result_orders = await self.db.execute(select(func.count(Order.id)))
        total_orders = result_orders.scalar() or 0

        result_pending = await self.db.execute(
            select(func.count(Order.id)).where(Order.status == OrderStatus.PENDING)
        )
        pending_orders = result_pending.scalar() or 0

        return {
            "total_revenue": total_revenue,
            "total_orders": total_orders,
            "pending_orders": pending_orders,
        }

    async def get_sales_per_day(self, days: int = 30) -> List[dict]:
        """
        Get total sales per day for the last X days.
        """
        from sqlalchemy import func, cast, String
        from datetime import datetime, timedelta, timezone

        start_date = datetime.now(timezone.utc) - timedelta(days=days)

        query = (
            select(
                func.substr(cast(Order.created_at, String), 1, 10).label('date'),
                func.sum(Order.total_amount).label('revenue')
            )
            .where(Order.created_at >= start_date)
            .group_by('date')
            .order_by('date')
        )
        
        result = await self.db.execute(query)
        rows = result.all()
        
        return [{"date": str(r.date), "revenue": float(r.revenue)} for r in rows]

    async def get_top_selling_products(self, limit: int = 5) -> List[dict]:
        """
        Get the top selling products based on order quantities.
        """
        from sqlalchemy import func, desc

        query = (
            select(
                Product.id,
                Product.name,
                Product.price,
                Product.image_url,
                func.sum(OrderItem.quantity).label('total_sold')
            )
            .join(OrderItem, Product.id == OrderItem.product_id)
            .join(Order, Order.id == OrderItem.order_id)
            .group_by(Product.id, Product.name, Product.price, Product.image_url)
            .order_by(desc('total_sold'))
            .limit(limit)
        )
        
        result = await self.db.execute(query)
        rows = result.all()
        
        return [{
            "id": r.id, 
            "name": r.name, 
            "price": r.price, 
            "image_url": r.image_url, 
            "total_sold": r.total_sold
        } for r in rows]