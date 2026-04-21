"""
User Repository (Tony)
=======================
Data access layer for user-related database operations.
Implements the repository pattern for clean separation of concerns.
"""

from typing import Optional, List, Tuple
from sqlalchemy import select, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.constants import UserRole


class UserRepository:
    """Repository for User database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: User) -> User:
        """Create a new user in the database."""
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get a user by their ID."""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by their email address."""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 20,
        role: Optional[UserRole] = None,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
    ) -> Tuple[List[User], int]:
        """
        Get all users with pagination and filtering.

        Returns:
            Tuple of (list of users, total count).
        """
        query = select(User)
        count_query = select(func.count(User.id))

        # Apply filters
        if role is not None:
            query = query.where(User.role == role)
            count_query = count_query.where(User.role == role)
        if is_active is not None:
            query = query.where(User.is_active == is_active)
            count_query = count_query.where(User.is_active == is_active)
        if search:
            search_filter = f"%{search}%"
            query = query.where(
                (User.email.ilike(search_filter))
                | (User.first_name.ilike(search_filter))
                | (User.last_name.ilike(search_filter))
            )
            count_query = count_query.where(
                (User.email.ilike(search_filter))
                | (User.first_name.ilike(search_filter))
                | (User.last_name.ilike(search_filter))
            )

        # Get total count
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        # Apply pagination
        query = query.order_by(User.created_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        users = result.scalars().all()

        return list(users), total

    async def update(self, user_id: int, **kwargs) -> Optional[User]:
        """Update a user's fields."""
        # Remove None values
        update_data = {k: v for k, v in kwargs.items() if v is not None}
        if not update_data:
            return await self.get_by_id(user_id)

        await self.db.execute(
            update(User).where(User.id == user_id).values(**update_data)
        )
        await self.db.flush()
        return await self.get_by_id(user_id)

    async def delete(self, user_id: int) -> bool:
        """Delete a user by ID."""
        result = await self.db.execute(
            delete(User).where(User.id == user_id)
        )
        await self.db.flush()
        return result.rowcount > 0

    async def count(self) -> int:
        """Get total number of users."""
        result = await self.db.execute(select(func.count(User.id)))
        return result.scalar()

    async def exists_by_email(self, email: str) -> bool:
        """Check if a user exists with the given email."""
        result = await self.db.execute(
            select(func.count(User.id)).where(User.email == email)
        )
        return result.scalar() > 0

    async def deactivate(self, user_id: int) -> Optional[User]:
        """Deactivate a user account."""
        return await self.update(user_id, is_active=False)

    async def activate(self, user_id: int) -> Optional[User]:
        """Activate a user account."""
        return await self.update(user_id, is_active=True)
