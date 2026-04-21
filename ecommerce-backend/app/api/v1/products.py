"""
Product API Routes (Tony)
==========================
Endpoints for managing and viewing products and categories.
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_admin_user
from app.schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse, 
    ProductListResponse, CategoryCreate, CategoryResponse
)
from app.services.ecommerce_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=ProductListResponse)
async def get_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    product_service = ProductService(db)
    items, total = await product_service.get_products(page, page_size, category_id, search)
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/categories", response_model=List[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    product_service = ProductService(db)
    return await product_service.get_categories()


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product_service = ProductService(db)
    return await product_service.get_product(product_id)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    data: ProductCreate, 
    admin=Depends(get_admin_user), 
    db: AsyncSession = Depends(get_db)
):
    product_service = ProductService(db)
    return await product_service.create_product(data)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int, 
    data: ProductUpdate, 
    admin=Depends(get_admin_user), 
    db: AsyncSession = Depends(get_db)
):
    product_service = ProductService(db)
    return await product_service.update_product(product_id, data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int, 
    admin=Depends(get_admin_user), 
    db: AsyncSession = Depends(get_db)
):
    product_service = ProductService(db)
    await product_service.delete_product(product_id)


@router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    data: CategoryCreate, 
    admin=Depends(get_admin_user), 
    db: AsyncSession = Depends(get_db)
):
    product_service = ProductService(db)
    return await product_service.create_category(data)
