from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.cart import CartOut, CartItemCreate, CartItemUpdate
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.services.cart_service import CartService

router = APIRouter(prefix="/cart", tags=["Cart"])

# 1. (POST)
@router.post("/items", status_code=status.HTTP_201_CREATED)
async def add_to_cart(
        item_in: CartItemCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # Logic delegated to Service layer
    return await CartService.add_to_cart(db, current_user.id, item_in)

# 2. (GET)
@router.get("/", response_model=CartOut)
async def view_cart(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return await CartService.view_cart(db, current_user.id)

# 3. (PUT)
@router.put("/items/{item_id}")
async def update_cart_item(
        item_id: int,
        item_in: CartItemUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return await CartService.update_cart_item(db, current_user.id, item_id, item_in)

# 4. (DELETE)
@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_cart(
        item_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    await CartService.remove_from_cart(db, current_user.id, item_id)
    return None

# 5. (DELETE)
@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    await CartService.clear_cart(db, current_user.id)
    return None