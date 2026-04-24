"""
Order and Wishlist Schemas (Ahmed)
==================================
Pydantic schemas for orders, order items, and wishlists.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from app.core.constants import OrderStatus, PaymentStatus
from app.schemas.product import ProductResponse


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


class OrderItemResponse(OrderItemBase):
    id: int
    unit_price: float
    total_price: float
    product: ProductResponse

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    shipping_address: str
    shipping_city: str
    shipping_state: Optional[str] = None
    shipping_zip: str
    shipping_country: str = "Egypt"
    payment_method: str = Field(..., description="'COD' or 'Online'")
    notes: Optional[str] = None


class OrderCreate(OrderBase):
    items: List[OrderItemBase]


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    payment_status: Optional[PaymentStatus] = None
    tracking_number: Optional[str] = None


class OrderResponse(OrderBase):
    id: int
    user_id: int
    total_amount: float
    shipping_cost: float
    tax_amount: float
    status: OrderStatus
    payment_status: PaymentStatus
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True


class WishlistBase(BaseModel):
    product_id: int


class WishlistResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    created_at: datetime
    product: ProductResponse

    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    total_revenue: float
    total_orders: int
    total_users: int
    pending_orders: int
    top_selling_products: List[dict]
    sales_over_time: List[dict]
