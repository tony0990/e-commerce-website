from pydantic import BaseModel, Field
from typing import List

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1, description="Quantity Must Be 1 Or More")

class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=1, description="Quantity Must Be 1 Or More")

class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True

class CartOut(BaseModel):
    id: int
    user_id: int
    items: List[CartItemOut] = []

    class Config:
        from_attributes = True



