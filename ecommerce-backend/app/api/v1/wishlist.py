"""
Wishlist API Routes (Ahmed)
===========================
Endpoints for managing user wishlists.
"""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.order import WishlistBase, WishlistResponse
from app.services.ecommerce_service import WishlistService

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])


@router.post("/", response_model=WishlistResponse, status_code=status.HTTP_201_CREATED)
async def add_to_wishlist(
    data: WishlistBase,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    wishlist_service = WishlistService(db)
    return await wishlist_service.add_to_wishlist(current_user.id, data.product_id)


@router.get("/", response_model=List[WishlistResponse])
async def get_my_wishlist(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    wishlist_service = WishlistService(db)
    return await wishlist_service.get_wishlist(current_user.id)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_wishlist(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    wishlist_service = WishlistService(db)
    await wishlist_service.remove_from_wishlist(current_user.id, product_id)
