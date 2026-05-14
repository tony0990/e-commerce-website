"""
Order Tests
===========
Tests for order creation, inventory deduction, status updates,
tracking, and invalid business rules.
"""

import pytest
from httpx import AsyncClient

from app.core.constants import OrderStatus


@pytest.mark.asyncio
async def test_place_order_success(
    client: AsyncClient,
    user_token: str,
    test_product,
):
    response = await client.post(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "items": [
                {
                    "product_id": test_product.id,
                    "quantity": 2,
                }
            ],
            "shipping_address": "123 Cairo Street",
            "shipping_city": "Cairo",
            "shipping_state": "Cairo",
            "shipping_zip": "12345",
            "shipping_country": "Egypt",
            "payment_method": "COD",
            "notes": "Please deliver after 5 PM",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["user_id"] is not None
    assert data["status"] == OrderStatus.PENDING.value
    assert data["payment_status"] == "pending"
    assert data["payment_method"] == "COD"
    assert data["shipping_city"] == "Cairo"
    assert data["tracking_number"] is not None
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == test_product.id
    assert data["items"][0]["quantity"] == 2


@pytest.mark.asyncio
async def test_place_order_with_insufficient_stock(
    client: AsyncClient,
    user_token: str,
    test_product,
):
    response = await client.post(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "items": [
                {
                    "product_id": test_product.id,
                    "quantity": test_product.stock + 100,
                }
            ],
            "shipping_address": "123 Cairo Street",
            "shipping_city": "Cairo",
            "shipping_zip": "12345",
            "payment_method": "COD",
        },
    )

    assert response.status_code == 400
    assert "Insufficient stock" in response.json()["detail"]


@pytest.mark.asyncio
async def test_place_order_with_duplicate_product(
    client: AsyncClient,
    user_token: str,
    test_product,
):
    response = await client.post(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "items": [
                {
                    "product_id": test_product.id,
                    "quantity": 1,
                },
                {
                    "product_id": test_product.id,
                    "quantity": 2,
                },
            ],
            "shipping_address": "123 Cairo Street",
            "shipping_city": "Cairo",
            "shipping_zip": "12345",
            "payment_method": "COD",
        },
    )

    assert response.status_code == 400
    assert "Duplicate product" in response.json()["detail"]


@pytest.mark.asyncio
async def test_place_order_requires_authentication(
    client: AsyncClient,
    test_product,
):
    response = await client.post(
        "/api/v1/orders",
        json={
            "items": [
                {
                    "product_id": test_product.id,
                    "quantity": 1,
                }
            ],
            "shipping_address": "123 Cairo Street",
            "shipping_city": "Cairo",
            "shipping_zip": "12345",
            "payment_method": "COD",
        },
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_my_orders(
    client: AsyncClient,
    user_token: str,
    test_product,
):
    create_response = await client.post(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "items": [
                {
                    "product_id": test_product.id,
                    "quantity": 1,
                }
            ],
            "shipping_address": "123 Cairo Street",
            "shipping_city": "Cairo",
            "shipping_zip": "12345",
            "payment_method": "COD",
        },
    )

    assert create_response.status_code == 201

    response = await client.get(
        "/api/v1/orders/me",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_track_order(
    client: AsyncClient,
    user_token: str,
    test_product,
):
    create_response = await client.post(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "items": [
                {
                    "product_id": test_product.id,
                    "quantity": 1,
                }
            ],
            "shipping_address": "123 Cairo Street",
            "shipping_city": "Cairo",
            "shipping_zip": "12345",
            "payment_method": "COD",
        },
    )

    assert create_response.status_code == 201

    order_id = create_response.json()["id"]

    response = await client.get(
        f"/api/v1/orders/{order_id}/track",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["order_id"] == order_id
    assert data["status"] == OrderStatus.PENDING.value
    assert data["tracking_number"] is not None
    assert "currently" in data["message"]


@pytest.mark.asyncio
async def test_admin_can_get_all_orders(
    client: AsyncClient,
    admin_token: str,
):
    response = await client.get(
        "/api/v1/orders/all",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_user_cannot_get_all_orders(
    client: AsyncClient,
    user_token: str,
):
    response = await client.get(
        "/api/v1/orders/all",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_admin_can_update_order_status(
    client: AsyncClient,
    user_token: str,
    admin_token: str,
    test_product,
):
    create_response = await client.post(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "items": [
                {
                    "product_id": test_product.id,
                    "quantity": 1,
                }
            ],
            "shipping_address": "123 Cairo Street",
            "shipping_city": "Cairo",
            "shipping_zip": "12345",
            "payment_method": "COD",
        },
    )

    assert create_response.status_code == 201

    order_id = create_response.json()["id"]

    update_response = await client.patch(
        f"/api/v1/orders/{order_id}/status",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "status": OrderStatus.CONFIRMED.value,
        },
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["id"] == order_id
    assert data["status"] == OrderStatus.CONFIRMED.value


@pytest.mark.asyncio
async def test_user_cannot_update_order_status(
    client: AsyncClient,
    user_token: str,
    test_product,
):
    create_response = await client.post(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "items": [
                {
                    "product_id": test_product.id,
                    "quantity": 1,
                }
            ],
            "shipping_address": "123 Cairo Street",
            "shipping_city": "Cairo",
            "shipping_zip": "12345",
            "payment_method": "COD",
        },
    )

    assert create_response.status_code == 201

    order_id = create_response.json()["id"]

    update_response = await client.patch(
        f"/api/v1/orders/{order_id}/status",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "status": OrderStatus.CONFIRMED.value,
        },
    )

    assert update_response.status_code == 403


@pytest.mark.asyncio
async def test_invalid_order_status_transition(
    client: AsyncClient,
    user_token: str,
    admin_token: str,
    test_product,
):
    create_response = await client.post(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "items": [
                {
                    "product_id": test_product.id,
                    "quantity": 1,
                }
            ],
            "shipping_address": "123 Cairo Street",
            "shipping_city": "Cairo",
            "shipping_zip": "12345",
            "payment_method": "COD",
        },
    )

    assert create_response.status_code == 201

    order_id = create_response.json()["id"]

    response = await client.patch(
        f"/api/v1/orders/{order_id}/status",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "status": OrderStatus.SHIPPED.value,
        },
    )

    assert response.status_code == 400
    assert "Invalid order transition" in response.json()["detail"]