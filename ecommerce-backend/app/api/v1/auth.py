"""
Auth API Routes (Ahmed)
========================
Authentication endpoints: register, login, refresh token, change password.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    RefreshTokenRequest,
    ChangePasswordRequest,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    """
    Register a new user account.

    - **email**: Valid email address (must be unique)
    - **password**: Minimum 8 characters
    - **confirm_password**: Must match password
    - **first_name**: User's first name
    - **last_name**: User's last name
    """
    auth_service = AuthService(db)
    result = await auth_service.register(data)
    return result


@router.post("/login")
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    """
    Authenticate user and return JWT tokens.

    - **email**: Registered email address
    - **password**: Account password
    """
    auth_service = AuthService(db)
    result = await auth_service.login(data.email, data.password)
    return result


@router.post("/refresh")
async def refresh_token(
    data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Get new access and refresh tokens using a valid refresh token.
    """
    auth_service = AuthService(db)
    result = await auth_service.refresh_token(data.refresh_token)
    return result


@router.post("/change-password")
async def change_password(
    data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Change the current user's password.

    Requires authentication. Must provide current password for verification.
    """
    auth_service = AuthService(db)
    result = await auth_service.change_password(
        user_id=current_user.id,
        current_password=data.current_password,
        new_password=data.new_password,
        confirm_password=data.confirm_new_password,
    )
    return result


@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get the current authenticated user's information.
    """
    from app.core.constants import UserRole
    return {
        "success": True,
        "data": {
            "id": current_user.id,
            "email": current_user.email,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "phone": current_user.phone,
            "address": current_user.address,
            "city": current_user.city,
            "state": current_user.state,
            "zip_code": current_user.zip_code,
            "country": current_user.country,
            "role": current_user.role.value if isinstance(current_user.role, UserRole) else current_user.role,
            "is_active": current_user.is_active,
            "avatar_url": current_user.avatar_url,
            "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
            "updated_at": current_user.updated_at.isoformat() if current_user.updated_at else None,
        },
    }
