"""
Auth Schemas (Ahmed)
=====================
Pydantic schemas for authentication requests and responses.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.core.constants import MIN_PASSWORD_LENGTH


class LoginRequest(BaseModel):
    """Login request schema."""
    email: EmailStr
    password: str = Field(..., min_length=MIN_PASSWORD_LENGTH)


class RegisterRequest(BaseModel):
    """User registration request schema."""
    email: EmailStr
    password: str = Field(..., min_length=MIN_PASSWORD_LENGTH, max_length=128)
    confirm_password: str = Field(..., min_length=MIN_PASSWORD_LENGTH)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)


class TokenResponse(BaseModel):
    """JWT token response schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""
    refresh_token: str


class ChangePasswordRequest(BaseModel):
    """Change password request schema."""
    current_password: str
    new_password: str = Field(..., min_length=MIN_PASSWORD_LENGTH, max_length=128)
    confirm_new_password: str


class AuthResponse(BaseModel):
    """Authentication response with user info and tokens."""
    message: str
    success: bool = True
    user: dict
    tokens: TokenResponse
