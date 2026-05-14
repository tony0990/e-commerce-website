"""
Cart Repository
================
Database operations for shopping cart.
Handles CRUD operations for Cart and CartItem models.
"""

from typing import Optional, List

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.cart import Cart, CartItem
from app.models.product import Product


class CartRepository:
    """
    Repository layer for Cart model.

    Handles:
    - get_or_create_cart
    - add/update/remove items
    - get user cart
    - clear cart
    - sync cart items
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create_cart(self, user_id: int) -> Cart:
        """Get existing cart for user or create a new one."""
        result = await self.db.execute(
            select(Cart)
            .options(
                selectinload(Cart.items)
                .selectinload(CartItem.product)
                .selectinload(Product.category)
            )
            .where(Cart.user_id == user_id)
        )
        cart = result.scalar_one_or_none()

        if not cart:
            cart = Cart(user_id=user_id)
            self.db.add(cart)
            await self.db.flush()
            await self.db.refresh(cart)

        return cart

    async def get_cart(self, user_id: int) -> Optional[Cart]:
        """Get user's cart with all items and product details."""
        result = await self.db.execute(
            select(Cart)
            .options(
                selectinload(Cart.items)
                .selectinload(CartItem.product)
                .selectinload(Product.category)
            )
            .where(Cart.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def add_item(
        self, user_id: int, product_id: int, quantity: int = 1
    ) -> CartItem:
        """Add item to cart or update quantity if exists."""
        cart = await self.get_or_create_cart(user_id)

        # Check if item already in cart
        result = await self.db.execute(
            select(CartItem).where(
                CartItem.cart_id == cart.id,
                CartItem.product_id == product_id,
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            existing.quantity += quantity
            await self.db.flush()
            await self.db.refresh(existing)
            return existing
        else:
            item = CartItem(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity,
            )
            self.db.add(item)
            await self.db.flush()
            await self.db.refresh(item)
            return item

    async def update_item(
        self, user_id: int, item_id: int, quantity: int
    ) -> Optional[CartItem]:
        """Update quantity of a cart item."""
        cart = await self.get_cart(user_id)
        if not cart:
            return None

        result = await self.db.execute(
            select(CartItem).where(
                CartItem.id == item_id,
                CartItem.cart_id == cart.id,
            )
        )
        item = result.scalar_one_or_none()

        if not item:
            return None

        item.quantity = quantity
        await self.db.flush()
        await self.db.refresh(item)
        return item

    async def remove_item(self, user_id: int, item_id: int) -> bool:
        """Remove an item from the cart."""
        cart = await self.get_cart(user_id)
        if not cart:
            return False

        result = await self.db.execute(
            select(CartItem).where(
                CartItem.id == item_id,
                CartItem.cart_id == cart.id,
            )
        )
        item = result.scalar_one_or_none()

        if not item:
            return False

        await self.db.delete(item)
        await self.db.flush()
        return True

    async def clear_cart(self, user_id: int) -> bool:
        """Remove all items from user's cart."""
        cart = await self.get_cart(user_id)
        if not cart:
            return False

        await self.db.execute(
            delete(CartItem).where(CartItem.cart_id == cart.id)
        )
        await self.db.flush()
        return True

    async def sync_items(
        self, user_id: int, items: List[dict]
    ) -> Cart:
        """
        Sync local cart items to the database cart.
        Merges items - if product already in cart, updates quantity.
        """
        cart = await self.get_or_create_cart(user_id)

        for item_data in items:
            product_id = item_data.get("product_id")
            quantity = item_data.get("quantity", 1)

            result = await self.db.execute(
                select(CartItem).where(
                    CartItem.cart_id == cart.id,
                    CartItem.product_id == product_id,
                )
            )
            existing = result.scalar_one_or_none()

            if existing:
                existing.quantity = max(existing.quantity, quantity)
            else:
                new_item = CartItem(
                    cart_id=cart.id,
                    product_id=product_id,
                    quantity=quantity,
                )
                self.db.add(new_item)

        await self.db.flush()

        # Reload cart with relationships
        return await self.get_or_create_cart(user_id)
