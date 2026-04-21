"""
User Service (Tony)
====================
Business logic layer for user management operations.
Handles CRUD operations, profile updates, and admin user management.
"""

from typing import Optional, Tuple, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserUpdateAdmin
from app.core.security import hash_password
from app.core.constants import UserRole, ErrorMessages, SuccessMessages
from app.utils.exceptions import (
    NotFoundException,
    ConflictException,
    ForbiddenException,
)


class UserService:
    """Service for handling user management business logic."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def get_user_by_id(self, user_id: int) -> User:
        """Get a single user by ID."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException(ErrorMessages.USER_NOT_FOUND)
        return user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a single user by email."""
        return await self.user_repo.get_by_email(email)

    async def get_all_users(
        self,
        page: int = 1,
        page_size: int = 20,
        role: Optional[UserRole] = None,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
    ) -> Tuple[List[User], int]:
        """Get paginated list of users with optional filters."""
        skip = (page - 1) * page_size
        return await self.user_repo.get_all(
            skip=skip,
            limit=page_size,
            role=role,
            is_active=is_active,
            search=search,
        )

    async def create_user(self, data: UserCreate) -> User:
        """Create a new user (admin operation)."""
        if await self.user_repo.exists_by_email(data.email):
            raise ConflictException(ErrorMessages.USER_ALREADY_EXISTS)

        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
            phone=data.phone,
            role=data.role,
            is_active=True,
        )
        return await self.user_repo.create(user)

    async def update_user_profile(self, user_id: int, data: UserUpdate) -> User:
        """Update a user's own profile."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException(ErrorMessages.USER_NOT_FOUND)

        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return user

        updated_user = await self.user_repo.update(user_id, **update_data)
        return updated_user

    async def admin_update_user(self, user_id: int, data: UserUpdateAdmin) -> User:
        """Admin update a user's profile, role, or status."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException(ErrorMessages.USER_NOT_FOUND)

        update_data = data.model_dump(exclude_unset=True)

        # If email is being changed, check for conflicts
        if "email" in update_data and update_data["email"] != user.email:
            if await self.user_repo.exists_by_email(update_data["email"]):
                raise ConflictException(ErrorMessages.USER_ALREADY_EXISTS)

        if not update_data:
            return user

        updated_user = await self.user_repo.update(user_id, **update_data)
        return updated_user

    async def delete_user(self, user_id: int, current_user_id: int) -> dict:
        """Delete a user (admin only). Cannot delete yourself."""
        if user_id == current_user_id:
            raise ForbiddenException("You cannot delete your own account")

        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException(ErrorMessages.USER_NOT_FOUND)

        await self.user_repo.delete(user_id)
        return {"message": SuccessMessages.USER_DELETED, "success": True}

    async def get_user_count(self) -> int:
        """Get total user count."""
        return await self.user_repo.count()

    async def toggle_user_status(self, user_id: int) -> User:
        """Toggle a user's active status."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException(ErrorMessages.USER_NOT_FOUND)

        if user.is_active:
            return await self.user_repo.deactivate(user_id)
        else:
            return await self.user_repo.activate(user_id)
