from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.category_repository import CategoryRepository
from app.models.category import Category
from app.schemas.category import CategoryCreate
from app.core.cache import get_cache, set_cache, delete_cache

class CategoryService:
    # Handles business logic and caching for Categories
    
    @staticmethod
    async def get_all_categories(db: AsyncSession):
        # 1. Check cache first
        cached_categories = get_cache("all_categories")
        if cached_categories:
            return cached_categories

        # 2. Fetch from DB if not in cache
        categories = await CategoryRepository.get_all_active(db)
        
        # 3. Serialize data for caching
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

        # 4. Set cache and return
        if categories_data:
            set_cache("all_categories", categories_data)

        return categories_data

    @staticmethod
    async def get_single_category(db: AsyncSession, category_id: int):
        category = await CategoryRepository.get_by_id(db, category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This Category Does not Exist")
        return category

    @staticmethod
    async def create_category(db: AsyncSession, category_in: CategoryCreate):
        # Check for duplicates
        existing_category = await CategoryRepository.get_by_name_or_slug(db, category_in.name, category_in.slug)
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This Category Name OR Slug Already Exists"
            )

        new_category = Category(
            name=category_in.name,
            slug=category_in.slug,
            description=category_in.description,
            is_active=category_in.is_active
        )
        
        created_category = await CategoryRepository.create(db, new_category)
        
        # Invalidate cache after creation
        delete_cache("all_categories")
        return created_category

    @staticmethod
    async def update_category(db: AsyncSession, category_id: int, category_in: CategoryCreate):
        category = await CategoryRepository.get_by_id(db, category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This Category Does Not Exist")

        category.name = category_in.name
        category.slug = category_in.slug
        category.description = category_in.description
        category.is_active = category_in.is_active

        updated_category = await CategoryRepository.update(db, category)
        
        # Invalidate cache after update
        delete_cache("all_categories")
        return updated_category

    @staticmethod
    async def delete_category(db: AsyncSession, category_id: int):
        category = await CategoryRepository.get_by_id(db, category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This Category Does Not Exist")

        await CategoryRepository.delete(db, category)
        
        # Invalidate cache after deletion
        delete_cache("all_categories")
        return True