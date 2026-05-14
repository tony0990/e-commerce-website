"""
Cart Schemas
=============
Pydantic schemas for cart operations.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.product import ProductResponse


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1, description="Quantity Must Be 1 Or More")


class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=1, description="Quantity Must Be 1 Or More")


class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: Optional[ProductResponse] = None

    class Config:
        from_attributes = True


class CartOut(BaseModel):
    id: int
    user_id: int
    items: List[CartItemOut] = []

    class Config:
        from_attributes = True


class CartSyncItem(BaseModel):
    """Single item from localStorage cart to sync."""
    product_id: int
    quantity: int = Field(default=1, ge=1)


class CartSyncRequest(BaseModel):
    """Request body for syncing local cart to database."""
    items: List[CartSyncItem] = []
