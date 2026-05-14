from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.category import CategoryCreate, CategoryOut
from app.api.deps import get_db, verify_admin # Imported verify_admin from deps
from app.services.category_service import CategoryService

router = APIRouter()

# 1. (Async GET All)
@router.get("/", response_model=List[CategoryOut])
async def get_all_categories(db: AsyncSession = Depends(get_db)):
    # Logic delegated to Service layer
    return await CategoryService.get_all_categories(db)

# 2. (Async GET by ID)
@router.get("/{category_id}", response_model=CategoryOut)
async def get_single_category(category_id: int, db: AsyncSession = Depends(get_db)):
    return await CategoryService.get_single_category(db, category_id)

# 3. (Async POST)
@router.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_in: CategoryCreate, 
    db: AsyncSession = Depends(get_db),
    _ = Depends(verify_admin) # Admin role verification injected here
):
    return await CategoryService.create_category(db, category_in)

# 4. (Async PUT)
@router.put("/{category_id}", response_model=CategoryOut)
async def update_category(
    category_id: int, 
    category_in: CategoryCreate, 
    db: AsyncSession = Depends(get_db),
    _ = Depends(verify_admin) # Admin role verification injected here
):
    return await CategoryService.update_category(db, category_id, category_in)

# 5. (Async DELETE)
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int, 
    db: AsyncSession = Depends(get_db),
    _ = Depends(verify_admin) # Admin role verification injected here
):
    await CategoryService.delete_category(db, category_id)
    return None