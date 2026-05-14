"""
Order Item Model
================
SQLAlchemy model for products inside an order.
Each row represents one product line inside an order.
"""

from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class OrderItem(Base):
    """
    Represents one product line inside an order.

    Example:
    order_id=15, product_id=2, quantity=3,
    unit_price=500, total_price=1500.
    """

    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
    )

    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)

    order = relationship(
        "Order",
        back_populates="items",
    )

    product = relationship(
        "Product",
        lazy="selectin",
    )

    def __repr__(self):
        return (
            f"<OrderItem(id={self.id}, "
            f"order_id={self.order_id}, "
            f"product_id={self.product_id}, "
            f"quantity={self.quantity})>"
        )