

from typing import Optional
from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import verify_access_token
from app.core.constants import UserRole, ErrorMessages
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.utils.exceptions import UnauthorizedException, ForbiddenException


async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Dependency: Extract and validate JWT token to get the current user.
    Used to protect routes that require authentication.
    """
    if not authorization:
        raise UnauthorizedException(ErrorMessages.TOKEN_INVALID)

    # Extract token from "Bearer <token>" format
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise UnauthorizedException(ErrorMessages.TOKEN_INVALID)

    token = parts[1]
    payload = verify_access_token(token)
    if not payload:
        raise UnauthorizedException(ErrorMessages.TOKEN_INVALID)

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException(ErrorMessages.TOKEN_INVALID)

    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(int(user_id))

    if not user:
        raise UnauthorizedException(ErrorMessages.USER_NOT_FOUND)

    if not user.is_active:
        raise UnauthorizedException(ErrorMessages.USER_INACTIVE)

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Dependency: Get the current active user (alias for clarity)."""
    return current_user


async def get_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependency: Verify that the current user has admin role.
    Use this to protect admin-only endpoints.
    """
    user_role = current_user.role
    if isinstance(user_role, str):
        user_role = UserRole(user_role)

    if user_role != UserRole.ADMIN:
        raise ForbiddenException(ErrorMessages.FORBIDDEN)

    return current_user


def require_role(*roles: UserRole):
    """
    Factory dependency: Create a dependency that requires specific roles.
    Usage: Depends(require_role(UserRole.ADMIN, UserRole.USER))
    """
    async def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        user_role = current_user.role
        if isinstance(user_role, str):
            user_role = UserRole(user_role)

        if user_role not in roles:
            raise ForbiddenException(ErrorMessages.FORBIDDEN)
        return current_user

    return role_checker
