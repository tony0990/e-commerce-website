import pytest
from httpx import AsyncClient
from fastapi import status
from app.core.constants import SuccessMessages, API_V1_PREFIX

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """Test user registration."""
    payload = {
        "email": "test@example.com",
        "password": "Password123!",
        "confirm_password": "Password123!",
        "first_name": "Test",
        "last_name": "User"
    }
    response = await client.post(f"{API_V1_PREFIX}/auth/register", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["success"] is True
    assert data["message"] == SuccessMessages.USER_CREATED
    assert data["data"]["user"]["email"] == "test@example.com"

@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    """Test user login."""
    # First, register
    register_payload = {
        "email": "login@example.com",
        "password": "Password123!",
        "confirm_password": "Password123!",
        "first_name": "Login",
        "last_name": "User"
    }
    await client.post(f"{API_V1_PREFIX}/auth/register", json=register_payload)
    
    # Then, login
    login_payload = {
        "email": "login@example.com",
        "password": "Password123!"
    }
    response = await client.post(f"{API_V1_PREFIX}/auth/login", json=login_payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]["tokens"]
    assert "refresh_token" in data["data"]["tokens"]


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    """Test login with wrong password."""
    login_payload = {
        "email": "nonexistent@example.com",
        "password": "WrongPassword123"
    }
    response = await client.post(f"{API_V1_PREFIX}/auth/login", json=login_payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
