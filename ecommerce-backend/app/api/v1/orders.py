"""
Order API Routes (Ahmed)
========================
Endpoints for creating and viewing orders.
"""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user, get_admin_user
from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse, DashboardStats
from app.services.ecommerce_service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    order_service = OrderService(db)
    return await order_service.create_order(current_user.id, data)


@router.get("/me", response_model=List[OrderResponse])
async def get_my_orders(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    order_service = OrderService(db)
    return await order_service.get_user_orders(current_user.id)


@router.get("/", response_model=List[OrderResponse])
async def get_all_orders(
    admin=Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    order_service = OrderService(db)
    return await order_service.get_all_orders()


@router.get("/admin/stats", response_model=DashboardStats)
async def get_stats(
    admin=Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    order_service = OrderService(db)
    return await order_service.get_dashboard_stats()
