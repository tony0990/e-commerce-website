import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_db
from tests.conftest import override_get_db

client = TestClient(app)

def test_create_product_as_admin():
    response = client.post(
        "/api/v1/products/",
        json={"name": "Test Laptop", "price": 999.99, "stock": 10, "category_id": 1},
        headers={"Authorization": "Bearer ADMIN_TOKEN_HERE"}  # use test token
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Laptop"

def test_get_all_products_pagination():
    response = client.get("/api/v1/products/?page=1&size=5")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data

def test_search_and_filter():
    response = client.get("/api/v1/products/?search=laptop&min_price=500")
    assert response.status_code == 200
