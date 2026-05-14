from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy.orm import selectinload
from app.models.cart import Cart, CartItem

class CartRepository:
    # Handles direct database operations for Cart and CartItems
    
    @staticmethod
    async def get_cart_by_user(db: AsyncSession, user_id: int, load_items: bool = False):
        query = select(Cart).filter(Cart.user_id == user_id)
        if load_items:
            # Eager load items to prevent DetachedInstanceError in async operations
            query = query.options(selectinload(Cart.items))
            
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def create_cart(db: AsyncSession, user_id: int):
        cart = Cart(user_id=user_id)
        db.add(cart)
        await db.commit()
        await db.refresh(cart)
        return cart

    @staticmethod
    async def get_item(db: AsyncSession, cart_id: int, product_id: int = None, item_id: int = None):
        query = select(CartItem).filter(CartItem.cart_id == cart_id)
        if product_id:
            query = query.filter(CartItem.product_id == product_id)
        if item_id:
            query = query.filter(CartItem.id == item_id)
            
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def add_item(db: AsyncSession, item: CartItem):
        db.add(item)
        await db.commit()
        await db.refresh(item)
        return item

    @staticmethod
    async def update_item(db: AsyncSession, item: CartItem):
        await db.commit()
        await db.refresh(item)
        return item

    @staticmethod
    async def delete_item(db: AsyncSession, item: CartItem):
        await db.delete(item)
        await db.commit()

    @staticmethod
    async def clear_cart_items(db: AsyncSession, cart_id: int):
        await db.execute(delete(CartItem).where(CartItem.cart_id == cart_id))
        await db.commit()