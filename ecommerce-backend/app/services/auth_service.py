"""
Auth Service (Ahmed)
=====================
Business logic layer for authentication operations.
Handles login, registration, token management, and password changes.
"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
)
from app.core.constants import UserRole, ErrorMessages, SuccessMessages
from app.schemas.auth import RegisterRequest, TokenResponse
from app.utils.exceptions import (
    BadRequestException,
    UnauthorizedException,
    ConflictException,
)
from app.core.config import settings


class AuthService:
    """Service for handling authentication business logic."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def register(self, data: RegisterRequest) -> dict:
        """
        Register a new user account.

        Validates input, checks for duplicates, creates user, and returns tokens.
        """
        # Validate passwords match
        if data.password != data.confirm_password:
            raise BadRequestException("Passwords do not match")

        # Check if user already exists
        if await self.user_repo.exists_by_email(data.email):
            raise ConflictException(ErrorMessages.USER_ALREADY_EXISTS)

        # Create user
        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
            phone=data.phone,
            role=UserRole.USER,
            is_active=True,
        )
        user = await self.user_repo.create(user)

        # Generate tokens
        tokens = self._generate_tokens(user)

        return {
            "message": SuccessMessages.USER_CREATED,
            "success": True,
            "data": {
                "user": self._user_to_dict(user),
                "tokens": tokens,
            }
        }


    async def login(self, email: str, password: str) -> dict:
        """
        Authenticate a user and return tokens.
        """
        # Find user
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise UnauthorizedException(ErrorMessages.INVALID_CREDENTIALS)

        # Verify password
        if not verify_password(password, user.hashed_password):
            raise UnauthorizedException(ErrorMessages.INVALID_CREDENTIALS)

        # Check if active
        if not user.is_active:
            raise UnauthorizedException(ErrorMessages.USER_INACTIVE)

        # Generate tokens
        tokens = self._generate_tokens(user)

        return {
            "message": SuccessMessages.LOGIN_SUCCESS,
            "success": True,
            "data": {
                "user": self._user_to_dict(user),
                "tokens": tokens,
            }
        }


    async def refresh_token(self, refresh_token_str: str) -> dict:
        """
        Generate new tokens using a valid refresh token.
        """
        payload = verify_refresh_token(refresh_token_str)
        if not payload:
            raise UnauthorizedException(ErrorMessages.TOKEN_INVALID)

        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedException(ErrorMessages.TOKEN_INVALID)

        user = await self.user_repo.get_by_id(int(user_id))
        if not user or not user.is_active:
            raise UnauthorizedException(ErrorMessages.TOKEN_INVALID)

        tokens = self._generate_tokens(user)
        return {
            "message": "Token refreshed successfully",
            "success": True,
            "tokens": tokens,
        }

    async def change_password(
        self, user_id: int, current_password: str, new_password: str, confirm_password: str
    ) -> dict:
        """
        Change a user's password.
        """
        if new_password != confirm_password:
            raise BadRequestException("New passwords do not match")

        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise BadRequestException(ErrorMessages.USER_NOT_FOUND)

        if not verify_password(current_password, user.hashed_password):
            raise BadRequestException("Current password is incorrect")

        await self.user_repo.update(user_id, hashed_password=hash_password(new_password))
        return {"message": SuccessMessages.PASSWORD_CHANGED, "success": True}

    def _generate_tokens(self, user: User) -> dict:
        """Generate access and refresh tokens for a user."""
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value if isinstance(user.role, UserRole) else user.role,
        }
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        }

    @staticmethod
    def _user_to_dict(user: User) -> dict:
        """Convert a User model to a dictionary."""
        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone,
            "role": user.role.value if isinstance(user.role, UserRole) else user.role,
            "is_active": user.is_active,
        }
