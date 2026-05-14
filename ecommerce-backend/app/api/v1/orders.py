"""
Orders API
==========
API routes for order placement, listing, tracking, and admin status updates.
"""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_admin_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.order import (
    OrderCreate,
    OrderResponse,
    OrderStatusUpdate,
    OrderTrackResponse,
)
from app.services.order_service import OrderService


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def place_order(
    order_data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Place a new order for the currently authenticated user.
    """

    service = OrderService(db)

    return await service.place_order(
        user_id=current_user.id,
        data=order_data,
    )


@router.get(
    "/me",
    response_model=List[OrderResponse],
)
async def get_my_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all orders for the currently authenticated user.
    """

    service = OrderService(db)

    return await service.get_my_orders(
        user_id=current_user.id,
    )


@router.get(
    "/all",
    response_model=List[OrderResponse],
)
async def get_all_orders(
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_admin_user),
):
    """
    Admin only:
    Get all orders in the system.
    """

    service = OrderService(db)

    return await service.get_all_orders()


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
)
async def get_order_by_id(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get one order by ID for the current user only.
    """

    service = OrderService(db)

    return await service.get_order_for_user(
        order_id=order_id,
        user_id=current_user.id,
    )


@router.patch(
    "/{order_id}/status",
    response_model=OrderResponse,
)
async def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_admin_user),
):
    """
    Admin only:
    Update order status after validating transition rules.
    """

    service = OrderService(db)

    return await service.update_order_status(
        order_id=order_id,
        new_status=status_data.status,
    )


@router.get(
    "/{order_id}/track",
    response_model=OrderTrackResponse,
)
async def track_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Track order status for the current user.
    """

    service = OrderService(db)

    order = await service.track_order(
        order_id=order_id,
        user_id=current_user.id,
    )

    return OrderTrackResponse(
        order_id=order.id,
        status=order.status,
        tracking_number=order.tracking_number,
        message=f"Your order is currently '{order.status.value}'",
    )