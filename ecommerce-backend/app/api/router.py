

from fastapi import APIRouter
from app.api.v1 import auth, users, products, orders, wishlist
from app.core.constants import API_V1_PREFIX

# Main API router
api_router = APIRouter(prefix=API_V1_PREFIX)

# Include v1 routers
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(products.router)
api_router.include_router(orders.router)
api_router.include_router(wishlist.router)
