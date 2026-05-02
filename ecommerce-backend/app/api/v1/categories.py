from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryOut
from app.api.deps import get_db
from app.core.cache import get_cache, set_cache, delete_cache
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryOut
from app.api.deps import get_db
from app.core.cache import get_cache, set_cache, delete_cache
router = APIRouter()

#  (Async GET)---------------------------------------------------------------
@router.get("/", response_model=List[CategoryOut])
async def get_all_categories(db: AsyncSession = Depends(get_db)): # خلينا الـ db تكون AsyncSession
    cached_categories = get_cache("all_categories")

    if cached_categories:
        return cached_categories

    result = await db.execute(select(Category).filter(Category.is_active == True))
    categories = result.scalars().all()
    categories_data = [
        {
            "id": c.id,
            "name": c.name,
            "slug": c.slug,
            "description": c.description,
            "is_active": c.is_active,
            "created_at": c.created_at.isoformat() if c.created_at else None,
            "updated_at": c.updated_at.isoformat() if c.updated_at else None
        }
        for c in categories
    ]

    if categories_data:
        set_cache("all_categories", categories_data)

    return categories

# ID (Async GET)-------------------------------------------------------------------------------------
@router.get("/{category_id}", response_model=CategoryOut)
async def get_single_category(category_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).filter(Category.id == category_id))
    category = result.scalars().first()

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This Category Does not Exist")

    return category


# 3. (POST)----------------------------------------------------------------------------------------

@router.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(category_in: CategoryCreate, db: Session = Depends(get_db)):
    existing_category = db.query(Category).filter(
        (Category.name == category_in.name) | (Category.slug == category_in.slug)
    ).first()

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This Category Name OR Slug IS Already Exist(slug)"
        )

    new_category = Category(
        name=category_in.name,
        slug=category_in.slug,
        description=category_in.description,
        is_active=category_in.is_active
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    delete_cache("all_categories")

    return new_category


# 4.  (PUT)----------------------------------------------------------------------------------------------------

@router.put("/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, category_in: CategoryCreate, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This Category Does Not Exist")

    category.name = category_in.name
    category.slug = category_in.slug
    category.description = category_in.description
    category.is_active = category_in.is_active

    db.commit()
    db.refresh(category)

    delete_cache("all_categories")

    return category


# 5. (DELETE)--------------------------------------------------------------------------------------------------------
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This Category Does Not Exist")

    db.delete(category)
    db.commit()

    delete_cache("all_categories")

    return None