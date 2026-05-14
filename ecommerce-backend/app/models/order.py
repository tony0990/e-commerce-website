"""
Order Model
===========
SQLAlchemy model for customer orders.
Includes payment, shipping, status, and tracking details.
"""

from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    Enum as SAEnum,
    Text,
)
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.constants import OrderStatus, PaymentStatus


class Order(Base):
    """
    Represents one customer order.

    Example:
    User #3 placed order #15 with total_amount=2500,
    payment_method='COD', and status='pending'.
    """

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    total_amount = Column(Float, nullable=False, default=0.0)
    shipping_cost = Column(Float, nullable=False, default=0.0)
    tax_amount = Column(Float, nullable=False, default=0.0)

    status = Column(
        SAEnum(OrderStatus),
        nullable=False,
        default=OrderStatus.PENDING,
        server_default=OrderStatus.PENDING.value,
    )

    payment_status = Column(
        SAEnum(PaymentStatus),
        nullable=False,
        default=PaymentStatus.PENDING,
        server_default=PaymentStatus.PENDING.value,
    )

    payment_method = Column(String(50), nullable=False, default="COD")

    shipping_address = Column(Text, nullable=False)
    shipping_city = Column(String(100), nullable=False)
    shipping_state = Column(String(100), nullable=True)
    shipping_zip = Column(String(20), nullable=False)
    shipping_country = Column(String(100), nullable=False, default="Egypt")

    tracking_number = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user = relationship(
        "User",
        backref="orders",
        lazy="selectin",
    )

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self):
        return (
            f"<Order(id={self.id}, "
            f"user_id={self.user_id}, "
            f"status='{self.status}')>"
        )