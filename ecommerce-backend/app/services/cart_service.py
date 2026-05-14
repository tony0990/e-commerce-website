from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.cart_repository import CartRepository
from app.models.cart import CartItem
from app.schemas.cart import CartItemCreate, CartItemUpdate

class CartService:
    # Handles business logic for Cart operations
    
    @staticmethod
    async def add_to_cart(db: AsyncSession, user_id: int, item_in: CartItemCreate):
        # 1. Get or create cart for the user
        cart = await CartRepository.get_cart_by_user(db, user_id)
        if not cart:
            cart = await CartRepository.create_cart(db, user_id)

        # 2. Check if product already exists in cart
        existing_item = await CartRepository.get_item(db, cart.id, product_id=item_in.product_id)

        if existing_item:
            # Update quantity if exists
            existing_item.quantity += item_in.quantity
            await CartRepository.update_item(db, existing_item)
        else:
            # Add new item if it doesn't exist
            new_item = CartItem(
                cart_id=cart.id,
                product_id=item_in.product_id,
                quantity=item_in.quantity
            )
            await CartRepository.add_item(db, new_item)

        return {"message": "The Product Was Added Successfully To Cart"}

    @staticmethod
    async def view_cart(db: AsyncSession, user_id: int):
        # Fetch cart with eagerly loaded items
        cart = await CartRepository.get_cart_by_user(db, user_id, load_items=True)
        if not cart:
            return {"id": 0, "user_id": user_id, "items": []}
        return cart

    @staticmethod
    async def update_cart_item(db: AsyncSession, user_id: int, item_id: int, item_in: CartItemUpdate):
        cart = await CartRepository.get_cart_by_user(db, user_id)
        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Your Cart Doesn't Exist")
        
        item = await CartRepository.get_item(db, cart.id, item_id=item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This Item Doesn't Exist In Your Cart")

        item.quantity = item_in.quantity
        updated_item = await CartRepository.update_item(db, item)

        return {
            "message": "Quantity Updated Successfully", 
            "item": {
                "id": updated_item.id, 
                "quantity": updated_item.quantity, 
                "product_id": updated_item.product_id, 
                "cart_id": updated_item.cart_id
            }
        }

    @staticmethod
    async def remove_from_cart(db: AsyncSession, user_id: int, item_id: int):
        cart = await CartRepository.get_cart_by_user(db, user_id)
        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Your Cart Doesn't Exist")
            
        item = await CartRepository.get_item(db, cart.id, item_id=item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This Item Doesn't Exist In Your Cart")

        await CartRepository.delete_item(db, item)
        return True

    @staticmethod
    async def clear_cart(db: AsyncSession, user_id: int):
        cart = await CartRepository.get_cart_by_user(db, user_id)
        if cart:
            await CartRepository.clear_cart_items(db, cart.id)
        return True