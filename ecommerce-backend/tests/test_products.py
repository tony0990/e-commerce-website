import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_product_as_admin(client: AsyncClient, admin_token: str):
    response = await client.post(
        "/api/v1/products/",
        json={"name": "Test Laptop", "price": 999.99, "stock": 10, "category_id": 1, "description": "Good laptop"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    # Based on app design, 201 should be created
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_get_all_products_pagination(client: AsyncClient):
    response = await client.get("/api/v1/products/?page=1&size=5")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data or "items" in data

@pytest.mark.asyncio
async def test_search_and_filter(client: AsyncClient):
    response = await client.get("/api/v1/products/?search=laptop&min_price=500")
    assert response.status_code == 200

