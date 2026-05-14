"""
Order Schemas
=============
Pydantic schemas for order requests and responses.
Used for validation and API response formatting.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict

from app.core.constants import OrderStatus, PaymentStatus
from app.schemas.product import ProductResponse
from app.schemas.user import UserResponse


class OrderItemBase(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class OrderItemCreate(OrderItemBase):
    """
    Used when the user sends products while placing an order.
    """
    pass


class OrderItemResponse(OrderItemBase):
    """
    Returned inside the order response.
    Represents one product line inside the order.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    unit_price: float
    total_price: float
    product: Optional[ProductResponse] = None


class OrderBase(BaseModel):
    """
    Shared shipping and payment fields.
    """

    shipping_address: str = Field(..., min_length=3)
    shipping_city: str = Field(..., min_length=2)
    shipping_state: Optional[str] = None
    shipping_zip: str = Field(..., min_length=2)
    shipping_country: str = Field(default="Egypt", min_length=2)

    payment_method: str = Field(
        default="COD",
        description="Payment method, for example: COD or Online",
        max_length=50,
    )

    notes: Optional[str] = None


class OrderCreate(OrderBase):
    """
    Request body for placing an order.
    """

    items: List[OrderItemCreate] = Field(..., min_length=1)



PlaceOrderRequest = OrderCreate


class OrderStatusUpdate(BaseModel):
    """
    Request body for admin status update.
    """

    status: OrderStatus


class OrderUpdate(BaseModel):
    """
    Optional update schema.
    Useful if later you want to update status, payment status,
    or tracking number from one endpoint.
    """

    status: Optional[OrderStatus] = None
    payment_status: Optional[PaymentStatus] = None
    tracking_number: Optional[str] = None


class OrderResponse(OrderBase):
    """
    Full order response returned by the API.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int

    total_amount: float
    shipping_cost: float
    tax_amount: float

    status: OrderStatus
    payment_status: PaymentStatus
    tracking_number: Optional[str] = None

    created_at: datetime
    updated_at: Optional[datetime] = None

    user: Optional[UserResponse] = None
    items: List[OrderItemResponse] = []


class OrderTrackResponse(BaseModel):
    """
    Simple response for tracking an order.
    """

    order_id: int
    status: OrderStatus
    tracking_number: Optional[str] = None
    message: str

class WishlistBase(BaseModel):
    product_id: int = Field(..., gt=0)


class WishlistResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    product_id: int
    created_at: datetime
    product: Optional[ProductResponse] = None