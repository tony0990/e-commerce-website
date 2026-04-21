"""
Base Repository (Tony)
======================
Generic repository with basic CRUD operations.
"""

from typing import TypeVar, Generic, Type, Any, Optional, List, Sequence
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base class for all repositories."""

    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get_by_id(self, id: Any) -> Optional[ModelType]:
        """Fetch a single record by ID."""
        result = await self.db.execute(select(self.model).filter(self.model.id == id))
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        """Fetch multiple records with pagination."""
        query = select(self.model).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create(self, obj: ModelType) -> ModelType:
        """Create a new record."""
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def update(self, id: Any, **kwargs) -> Optional[ModelType]:
        """Update an existing record."""
        query = update(self.model).where(self.model.id == id).values(**kwargs).execution_options(synchronize_session="fetch")
        await self.db.execute(query)
        await self.db.commit()
        return await self.get_by_id(id)

    async def delete(self, id: Any) -> bool:
        """Delete a record."""
        query = delete(self.model).where(self.model.id == id)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0

    async def count(self) -> int:
        """Count total records."""
        result = await self.db.execute(select(func.count()).select_from(self.model))
        return result.scalar() or 0
