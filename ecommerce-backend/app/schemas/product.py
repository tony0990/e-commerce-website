"""
Product and Category Schemas (Tony)
===================================
Pydantic schemas for products and categories.
"""

from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    image_url: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str
    price: float = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)
    image_url: Optional[str] = None
    is_active: bool = True
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None
    category_id: Optional[int] = None


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: Optional[CategoryResponse] = None

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    items: List[ProductResponse]
    total: int
    page: int
    page_size: int
