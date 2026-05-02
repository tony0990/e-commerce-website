"""
E-Commerce Services (Tony + Ahmed)
==================================
Business logic layer for products, orders, and wishlists.
"""

from typing import List, Optional, Tuple, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.product_repository import ProductRepository, CategoryRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.wishlist_repository import WishlistRepository
from app.repositories.user_repository import UserRepository
from app.models.product import Product, Category
from app.models.order import Order, OrderItem
from app.models.wishlist import Wishlist
from app.schemas.product import ProductCreate, ProductUpdate, CategoryCreate
from app.schemas.order import OrderCreate
from app.utils.exceptions import NotFoundException, BadRequestException
from app.services.cache_service import cache_service
from app.schemas.product import ProductResponse



class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.product_repo = ProductRepository(db)
        self.category_repo = CategoryRepository(db)

    async def get_products(self, page: int, page_size: int, category_id: Optional[int], search: Optional[str]):
        # Cache key based on query params
        cache_key = f"products:list:p{page}:s{page_size}:c{category_id or 0}:q{search or ''}"
        cached_data = await cache_service.get(cache_key)
        if cached_data:
            return cached_data["items"], cached_data["total"]

        items, total = await self.product_repo.get_all_paged(page, page_size, category_id, search)
        
        # Serialize for cache
        serialized_items = [ProductResponse.model_validate(item).model_dump(mode="json") for item in items]
        await cache_service.set(cache_key, {"items": serialized_items, "total": total})
        
        return items, total

    async def get_product(self, product_id: int):
        cache_key = f"product:{product_id}"
        cached_product = await cache_service.get(cache_key)
        if cached_product:
            # Return as dict or convert back to model if needed by caller
            # For simplicity, most callers expect the model
            return cached_product

        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundException("Product not found")
        
        # Cache serialized product
        serialized = ProductResponse.model_validate(product).model_dump(mode="json")
        await cache_service.set(cache_key, serialized)
        return product

    async def create_product(self, data: ProductCreate):
        product = Product(**data.model_dump())
        result = await self.product_repo.create(product)
        # Invalidate lists
        await cache_service.clear_pattern("products:list:*")
        return result

    async def update_product(self, product_id: int, data: ProductUpdate):
        result = await self.product_repo.update(product_id, **data.model_dump(exclude_unset=True))
        # Invalidate specific product and lists
        await cache_service.delete(f"product:{product_id}")
        await cache_service.clear_pattern("products:list:*")
        return result

    async def delete_product(self, product_id: int):
        result = await self.product_repo.delete(product_id)
        # Invalidate specific product and lists
        await cache_service.delete(f"product:{product_id}")
        await cache_service.clear_pattern("products:list:*")
        return result


    async def get_categories(self):
        cache_key = "categories:all"
        cached = await cache_service.get(cache_key)
        if cached: return cached
        
        categories = await self.category_repo.get_all()
        # Serialize list of objects
        from app.schemas.product import CategoryResponse
        serialized = [CategoryResponse.model_validate(c).model_dump(mode="json") for c in categories]
        await cache_service.set(cache_key, serialized)
        return categories

    async def create_category(self, data: CategoryCreate):
        category = Category(**data.model_dump())
        result = await self.category_repo.create(category)
        await cache_service.delete("categories:all")
        return result



class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.order_repo = OrderRepository(db)
        self.product_repo = ProductRepository(db)

    async def create_order(self, user_id: int, data: OrderCreate):
        """Create a new order with items."""
        total_amount = 0.0
        order_items = []
        
        for item_data in data.items:
            product = await self.product_repo.get_by_id(item_data.product_id)
            if not product:
                raise NotFoundException(f"Product {item_data.product_id} not found")
            if product.stock < item_data.quantity:
                raise BadRequestException(f"Insufficient stock for {product.name}")
            
            # Deduct stock
            await self.product_repo.update(product.id, stock=product.stock - item_data.quantity)
            
            item_total = product.price * item_data.quantity
            total_amount += item_total
            
            order_items.append(OrderItem(
                product_id=product.id,
                quantity=item_data.quantity,
                unit_price=product.price,
                total_price=item_total,
                product=product
            ))
            
        order = Order(
            user_id=user_id,
            total_amount=total_amount,
            shipping_address=data.shipping_address,
            shipping_city=data.shipping_city,
            shipping_state=data.shipping_state,
            shipping_zip=data.shipping_zip,
            shipping_country=data.shipping_country,
            payment_method=data.payment_method,
            notes=data.notes,
            items=order_items
        )
        return await self.order_repo.create(order)

    async def get_user_orders(self, user_id: int):
        return await self.order_repo.get_user_orders(user_id)

    async def get_all_orders(self):
        return await self.order_repo.get_all()

    async def get_dashboard_stats(self):
        stats = await self.order_repo.get_stats()
        # Add user count
        user_repo = UserRepository(self.db)
        stats["total_users"] = await user_repo.count()
        
        # Add top items (stub)
        stats["top_selling_products"] = []
        
        # Add sales over time
        stats["sales_over_time"] = await self.order_repo.get_sales_per_day()
        
        return stats


class WishlistService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.wishlist_repo = WishlistRepository(db)

    async def add_to_wishlist(self, user_id: int, product_id: int):
        if await self.wishlist_repo.exists(user_id, product_id):
            return {"message": "Already in wishlist"}
        
        wish_item = Wishlist(user_id=user_id, product_id=product_id)
        return await self.wishlist_repo.create(wish_item)

    async def remove_from_wishlist(self, user_id: int, product_id: int):
        # Implementation of delete by user_id and product_id
        from sqlalchemy import delete
        query = delete(Wishlist).where(Wishlist.user_id == user_id, Wishlist.product_id == product_id)
        await self.db.execute(query)
        await self.db.commit()
        return {"success": True}

    async def get_wishlist(self, user_id: int):
        return await self.wishlist_repo.get_user_wishlist(user_id)
