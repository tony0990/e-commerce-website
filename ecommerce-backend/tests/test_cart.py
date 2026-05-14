import pytest
import uuid
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from app.core.constants import API_V1_PREFIX, UserRole
from app.models.user import User
from app.models.product import Product, Category
from app.core.security import create_access_token

@pytest.fixture
async def user_token(db_session: AsyncSession) -> str:
    """Fixture to create a standard user and return an access token."""
    user = User(
        email=f"user_{uuid.uuid4()}@example.com",
        hashed_password="fake_hashed_password",
        first_name="Cart",
        last_name="User",
        role=UserRole.USER,
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return create_access_token({"sub": str(user.id)})


@pytest.fixture
async def sample_product(db_session: AsyncSession) -> Product:
    """Fixture to create a sample product in the database."""
    category = Category(name=f"Category_{uuid.uuid4()}", description="Test")
    db_session.add(category)
    await db_session.commit()
    await db_session.refresh(category)

    product = Product(
        name=f"Product_{uuid.uuid4()}",
        description="Test Product",
        price=19.99,
        stock=100,
        category_id=category.id,
        is_active=True
    )
    db_session.add(product)
    await db_session.commit()
    await db_session.refresh(product)
    return product


@pytest.mark.asyncio
async def test_add_to_cart(client: AsyncClient, user_token: str, sample_product: Product):
    """Test adding an item to the cart."""
    payload = {
        "product_id": sample_product.id,
        "quantity": 2
    }
    response = await client.post(
        f"{API_V1_PREFIX}/cart/items",
        json=payload,
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["message"] == "The Product Was Added Successfully To Cart"


@pytest.mark.asyncio
async def test_view_cart(client: AsyncClient, user_token: str, sample_product: Product):
    """Test viewing the cart."""
    # First add item
    await client.post(
        f"{API_V1_PREFIX}/cart/items",
        json={"product_id": sample_product.id, "quantity": 1},
        headers={"Authorization": f"Bearer {user_token}"}
    )

    response = await client.get(
        f"{API_V1_PREFIX}/cart/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert len(data["items"]) >= 1
    assert data["items"][0]["product_id"] == sample_product.id


@pytest.mark.asyncio
async def test_update_cart_item(client: AsyncClient, user_token: str, sample_product: Product):
    """Test updating cart item quantity."""
    # First add item
    await client.post(
        f"{API_V1_PREFIX}/cart/items",
        json={"product_id": sample_product.id, "quantity": 1},
        headers={"Authorization": f"Bearer {user_token}"}
    )

    # Get cart to find the item ID
    cart_response = await client.get(
        f"{API_V1_PREFIX}/cart/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    item_id = cart_response.json()["items"][0]["id"]

    # Update item
    response = await client.put(
        f"{API_V1_PREFIX}/cart/items/{item_id}",
        json={"quantity": 5},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["item"]["quantity"] == 5


@pytest.mark.asyncio
async def test_remove_from_cart(client: AsyncClient, user_token: str, sample_product: Product):
    """Test removing an item from the cart."""
    # First add item
    await client.post(
        f"{API_V1_PREFIX}/cart/items",
        json={"product_id": sample_product.id, "quantity": 1},
        headers={"Authorization": f"Bearer {user_token}"}
    )

    # Get cart to find the item ID
    cart_response = await client.get(
        f"{API_V1_PREFIX}/cart/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    item_id = cart_response.json()["items"][0]["id"]

    # Delete item
    response = await client.delete(
        f"{API_V1_PREFIX}/cart/items/{item_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify cart is empty
    cart_response = await client.get(
        f"{API_V1_PREFIX}/cart/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert len(cart_response.json()["items"]) == 0


@pytest.mark.asyncio
async def test_clear_cart(client: AsyncClient, user_token: str, sample_product: Product):
    """Test clearing the entire cart."""
    # Add item
    await client.post(
        f"{API_V1_PREFIX}/cart/items",
        json={"product_id": sample_product.id, "quantity": 2},
        headers={"Authorization": f"Bearer {user_token}"}
    )

    # Clear cart
    response = await client.delete(
        f"{API_V1_PREFIX}/cart/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify cart is empty
    cart_response = await client.get(
        f"{API_V1_PREFIX}/cart/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert len(cart_response.json()["items"]) == 0

