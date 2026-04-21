"""
Order Models (Ahmed)
====================
SQLAlchemy models for orders and order items.
Includes payment and shipping details.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum as SAEnum, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.constants import OrderStatus, PaymentStatus


class Order(Base):
    """Order model representing a customer purchase."""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Financial details
    total_amount = Column(Float, nullable=False)
    shipping_cost = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    
    # Status tracking
    status = Column(SAEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    payment_status = Column(SAEnum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    payment_method = Column(String(50), nullable=False) # 'COD' or 'Online'
    
    # Shipping details
    shipping_address = Column(Text, nullable=False)
    shipping_city = Column(String(100), nullable=False)
    shipping_state = Column(String(100), nullable=True)
    shipping_zip = Column(String(20), nullable=False)
    shipping_country = Column(String(100), default="Egypt")
    
    # Metadata
    tracking_number = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, status='{self.status}')>"


class OrderItem(Base):
    """Specific line item within an order."""
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")

    def __repr__(self):
        return f"<OrderItem(id={self.id}, order_id={self.order_id}, product_id={self.product_id})>"
