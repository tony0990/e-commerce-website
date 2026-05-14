"""
Cart API Routes
================
Endpoints for managing user shopping carts.
All routes require JWT authentication.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.models.cart import Cart, CartItem
from app.schemas.cart import CartOut, CartItemCreate, CartItemUpdate, CartSyncRequest
from app.repositories.cart_repository import CartRepository
from loguru import logger

router = APIRouter(prefix="/cart", tags=["Cart"])


# 1. GET /cart/ - Get user's cart
@router.get("/", response_model=CartOut)
async def view_cart(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get the current user's cart with all items."""
    repo = CartRepository(db)
    cart = await repo.get_cart(current_user.id)

    if not cart:
        return {"id": 0, "user_id": current_user.id, "items": []}
    return cart


# 2. POST /cart/items - Add item to cart
@router.post("/items", status_code=status.HTTP_201_CREATED)
async def add_to_cart(
    item_in: CartItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Add a product to the cart. If already in cart, quantity is increased."""
    repo = CartRepository(db)
    item = await repo.add_item(
        user_id=current_user.id,
        product_id=item_in.product_id,
        quantity=item_in.quantity,
    )
    logger.info(
        f"[CART] User {current_user.email} (ID:{current_user.id}) "
        f"added product {item_in.product_id} qty={item_in.quantity} to cart"
    )
    return {"message": "Product added to cart successfully", "item_id": item.id}


# 3. PUT /cart/items/{item_id} - Update quantity
@router.put("/items/{item_id}")
async def update_cart_item(
    item_id: int,
    item_in: CartItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update the quantity of a cart item."""
    repo = CartRepository(db)
    item = await repo.update_item(
        user_id=current_user.id,
        item_id=item_id,
        quantity=item_in.quantity,
    )
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found in your cart",
        )
    return {"message": "Quantity updated successfully"}


# 4. DELETE /cart/items/{item_id} - Remove item
@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_cart(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Remove a single item from the cart."""
    repo = CartRepository(db)
    removed = await repo.remove_item(
        user_id=current_user.id,
        item_id=item_id,
    )
    if not removed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found in your cart",
        )
    logger.info(
        f"[CART] User {current_user.email} (ID:{current_user.id}) "
        f"removed item {item_id} from cart"
    )
    return None


# 5. DELETE /cart/ - Clear entire cart
@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Remove all items from the cart."""
    repo = CartRepository(db)
    await repo.clear_cart(current_user.id)
    logger.info(
        f"[CART] User {current_user.email} (ID:{current_user.id}) cleared cart"
    )
    return None


# 6. POST /cart/sync - Sync local cart to database on login
@router.post("/sync", response_model=CartOut)
async def sync_cart(
    sync_data: CartSyncRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Sync local (localStorage) cart items to the database cart.
    Called after user logs in to merge their offline cart.
    """
    repo = CartRepository(db)
    cart = await repo.sync_items(
        user_id=current_user.id,
        items=[item.model_dump() for item in sync_data.items],
    )
    logger.info(
        f"[CART] User {current_user.email} (ID:{current_user.id}) "
        f"synced {len(sync_data.items)} items from local cart"
    )
    return cart