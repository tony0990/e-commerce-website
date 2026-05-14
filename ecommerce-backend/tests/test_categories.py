import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from app.core.constants import API_V1_PREFIX, UserRole
from app.models.user import User
from app.core.security import create_access_token
import uuid

@pytest.fixture
async def admin_token(db_session: AsyncSession) -> str:
    """Fixture to create an admin user and return an access token."""
    user = User(
        email=f"admin_{uuid.uuid4()}@example.com",
        hashed_password="fake_hashed_password",
        first_name="Admin",
        last_name="CategoryTest",
        role=UserRole.ADMIN,
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    return create_access_token({"sub": str(user.id)})


@pytest.mark.asyncio
async def test_create_category(client: AsyncClient, admin_token: str):
    """Test creating a new category as an admin."""
    payload = {
        "name": "Electronics",
        "slug": "electronics", 
        "description": "Electronic gadgets and devices"
        
    }
    response = await client.post(
        f"{API_V1_PREFIX}/categories/", 
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Electronics"
    assert data["slug"] == "electronics"
    assert data["description"] == "Electronic gadgets and devices"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_categories(client: AsyncClient, admin_token: str):
    """Test retrieving all categories."""
    payload = {
        "name": "Books",
        "slug": "books", # slug
        "description": "Reading material"
    }
    await client.post(
        f"{API_V1_PREFIX}/categories/", 
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    response = await client.get(f"{API_V1_PREFIX}/categories/") 
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(c["name"] == "Books" for c in data)


@pytest.mark.asyncio
async def test_create_category_unauthorized(client: AsyncClient):
    """Test that unauthorized users cannot create a category."""
    payload = {
        "name": "Toys",
        "slug": "toys",
        "description": "Children toys"
    }
    response = await client.post(
        f"{API_V1_PREFIX}/categories/",
        json=payload
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED