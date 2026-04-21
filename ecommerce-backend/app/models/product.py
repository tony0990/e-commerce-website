"""
Product and Category Models (Tony)
==================================
SQLAlchemy models for products and their categories.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class Category(Base):
    """Category model for grouping products."""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"


class Product(Base):
    """Product model for the e-commerce store."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String(255), index=True, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    image_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    category = relationship("Category", back_populates="products")
    # Wishlist relationship will be added later

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"
