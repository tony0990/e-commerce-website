"""
Inventory Service
=================
Handles product stock validation, stock deduction, and stock restore.
This file contains inventory business logic only.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import ErrorMessages
from app.models.product import Product
from app.utils.exceptions import BadRequestException, NotFoundException


class InventoryService:
    """
    Service layer for inventory and stock operations.

    Used by OrderService when placing or cancelling orders.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_product_by_id(self, product_id: int) -> Product:
        """
        Get product from database and validate that it exists and is active.
        """

        result = await self.db.execute(
            select(Product).where(Product.id == product_id)
        )

        product = result.scalar_one_or_none()

        if not product or not product.is_active:
            raise NotFoundException(ErrorMessages.PRODUCT_NOT_FOUND)

        return product

    async def validate_quantity(self, quantity: int) -> None:
        """
        Validate that requested quantity is positive.
        """

        if quantity <= 0:
            raise BadRequestException(ErrorMessages.INVALID_QUANTITY)

    async def validate_stock(
        self,
        product: Product,
        quantity: int,
    ) -> None:
        """
        Validate that product has enough stock.
        """

        await self.validate_quantity(quantity)

        if product.stock < quantity:
            raise BadRequestException(
                f"{ErrorMessages.INSUFFICIENT_STOCK}: "
                f"{product.name} has only {product.stock} item(s) available"
            )

    async def deduct_stock(
        self,
        product: Product,
        quantity: int,
    ) -> Product:
        """
        Deduct quantity from product stock after order placement.
        """

        await self.validate_stock(product, quantity)

        product.stock -= quantity

        await self.db.flush()
        await self.db.refresh(product)

        return product

    async def restore_stock(
        self,
        product: Product,
        quantity: int,
    ) -> Product:
        """
        Restore quantity back to product stock.

        Used when an order is cancelled after stock was deducted.
        """

        await self.validate_quantity(quantity)

        product.stock += quantity

        await self.db.flush()
        await self.db.refresh(product)

        return product