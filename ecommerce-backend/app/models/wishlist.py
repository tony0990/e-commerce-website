"""
Wishlist Model (Ahmed)
======================
SQLAlchemy model for user wishlists.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base


class Wishlist(Base):
    """User wishlist model representing saved products."""
    __tablename__ = "wishlists"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="wishlist_items")
    product = relationship("Product")

    def __repr__(self):
        return f"<Wishlist(user_id={self.user_id}, product_id={self.product_id})>"
