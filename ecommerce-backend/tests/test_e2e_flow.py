import pytest
from httpx import AsyncClient
from fastapi import status
from app.core.constants import API_V1_PREFIX, OrderStatus

@pytest.mark.asyncio
async def test_e2e_user_journey(client: AsyncClient, admin_token: str, user_token: str, test_product):
    """
    Simulate a full end-to-end user journey:
    1. Admin creates a new category and product.
    2. User browses products.
    3. User adds items to wishlist (if implemented) or creates an order.
    4. User tracks the order.
    5. Admin updates the order status.
    6. User verifies the updated order status.
    """
    # 1. Admin creates a category
    category_res = await client.post(
        f"{API_V1_PREFIX}/products/categories",
        json={"name": "Electronics", "description": "Tech gadgets"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert category_res.status_code == status.HTTP_201_CREATED
    category_id = category_res.json()["id"]

    # Admin creates a product in that category
    product_res = await client.post(
        f"{API_V1_PREFIX}/products/",
        json={
            "name": "Smartphone X",
            "description": "Latest model",
            "price": 799.99,
            "stock": 50,
            "category_id": category_id
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert product_res.status_code == status.HTTP_201_CREATED
    product_id = product_res.json()["id"]

    # 2. User browses products
    list_res = await client.get(f"{API_V1_PREFIX}/products/")
    assert list_res.status_code == status.HTTP_200_OK
    assert len(list_res.json()["items"]) >= 1

    # 3. User creates an order
    order_res = await client.post(
        f"{API_V1_PREFIX}/orders",
        json={
            "items": [{"product_id": product_id, "quantity": 2}],
            "shipping_address": "123 Main St",
            "shipping_city": "New York",
            "shipping_state": "NY",
            "shipping_zip": "10001",
            "shipping_country": "USA",
            "payment_method": "Credit Card"
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert order_res.status_code == status.HTTP_201_CREATED
    order_data = order_res.json()
    order_id = order_data["id"]

    # 4. User tracks the order
    track_res = await client.get(
        f"{API_V1_PREFIX}/orders/{order_id}/track",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert track_res.status_code == status.HTTP_200_OK
    assert track_res.json()["status"] == OrderStatus.PENDING.value

    # 5. Admin updates the order status
    update_res = await client.patch(
        f"{API_V1_PREFIX}/orders/{order_id}/status",
        json={"status": OrderStatus.CONFIRMED.value},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert update_res.status_code == status.HTTP_200_OK

    # Admin updates it to processing
    update_res_proc = await client.patch(
        f"{API_V1_PREFIX}/orders/{order_id}/status",
        json={"status": OrderStatus.PROCESSING.value},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert update_res_proc.status_code == status.HTTP_200_OK

    # Admin updates it to shipped
    update_res2 = await client.patch(
        f"{API_V1_PREFIX}/orders/{order_id}/status",
        json={"status": OrderStatus.SHIPPED.value},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert update_res2.status_code == status.HTTP_200_OK

    # 6. User verifies the updated order status
    track_res2 = await client.get(
        f"{API_V1_PREFIX}/orders/{order_id}/track",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert track_res2.status_code == status.HTTP_200_OK
    assert track_res2.json()["status"] == OrderStatus.SHIPPED.value
