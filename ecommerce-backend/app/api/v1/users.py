"""
Users API Routes (Tony)
========================
User management endpoints with role-based access control.
Admin endpoints for managing all users.
User endpoints for managing own profile.
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user, get_admin_user
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserUpdateAdmin,
    UserResponse,
    UserListResponse,
)
from app.services.user_service import UserService
from app.core.constants import UserRole, DEFAULT_PAGE, DEFAULT_PAGE_SIZE
from app.utils.responses import paginated_response

router = APIRouter(prefix="/users", tags=["Users"])


# ========================
# Admin Endpoints
# ========================

@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_users(
    page: int = Query(DEFAULT_PAGE, ge=1, description="Page number"),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=100, description="Items per page"),
    role: Optional[UserRole] = Query(None, description="Filter by role"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    search: Optional[str] = Query(None, description="Search by name or email"),
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get all users with pagination and filtering. **Admin only.**

    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 20, max: 100)
    - **role**: Filter by user role (admin/user)
    - **is_active**: Filter by active status
    - **search**: Search by name or email
    """
    user_service = UserService(db)
    users, total = await user_service.get_all_users(
        page=page,
        page_size=page_size,
        role=role,
        is_active=is_active,
        search=search,
    )

    users_data = [UserListResponse.model_validate(u).model_dump() for u in users]
    return paginated_response(
        data=users_data,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new user. **Admin only.**

    Allows admin to create users with specific roles.
    """
    user_service = UserService(db)
    user = await user_service.create_user(data)
    user_data = UserResponse.model_validate(user).model_dump()
    return {
        "success": True,
        "message": "User created successfully",
        "data": user_data,
    }


@router.get("/count")
async def get_user_count(
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Get total user count. **Admin only.**"""
    user_service = UserService(db)
    count = await user_service.get_user_count()
    return {"success": True, "data": {"count": count}}


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(
    user_id: int,
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific user by ID. **Admin only.**"""
    user_service = UserService(db)
    user = await user_service.get_user_by_id(user_id)
    user_data = UserResponse.model_validate(user).model_dump()
    return {"success": True, "data": user_data}


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def admin_update_user(
    user_id: int,
    data: UserUpdateAdmin,
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Update any user's profile, role, or status. **Admin only.**
    """
    user_service = UserService(db)
    user = await user_service.admin_update_user(user_id, data)
    user_data = UserResponse.model_validate(user).model_dump()
    return {
        "success": True,
        "message": "User updated successfully",
        "data": user_data,
    }


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: int,
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a user. **Admin only.**

    Admin cannot delete their own account.
    """
    user_service = UserService(db)
    result = await user_service.delete_user(user_id, admin.id)
    return result


@router.patch("/{user_id}/toggle-status")
async def toggle_user_status(
    user_id: int,
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Toggle a user's active/inactive status. **Admin only.**"""
    user_service = UserService(db)
    user = await user_service.toggle_user_status(user_id)
    return {
        "success": True,
        "message": f"User {'activated' if user.is_active else 'deactivated'} successfully",
        "data": {"id": user.id, "is_active": user.is_active},
    }


# ========================
# Current User Endpoints
# ========================

@router.get("/me/profile", status_code=status.HTTP_200_OK)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """Get the current user's profile."""
    user_data = UserResponse.model_validate(current_user).model_dump()
    return {"success": True, "data": user_data}


@router.put("/me/profile", status_code=status.HTTP_200_OK)
async def update_my_profile(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update the current user's own profile."""
    user_service = UserService(db)
    user = await user_service.update_user_profile(current_user.id, data)
    user_data = UserResponse.model_validate(user).model_dump()
    return {
        "success": True,
        "message": "Profile updated successfully",
        "data": user_data,
    }
