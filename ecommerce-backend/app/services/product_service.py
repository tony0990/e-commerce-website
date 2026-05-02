from fastapi import HTTPException, status
from app.repositories.product_repository import ProductRepository
from app.core.cache import cache  # your Redis cache helper
from app.services.cache_service import CacheService  # if you want extra layer
import json
from typing import Optional, Dict

class ProductService:
    CACHE_PREFIX = "product"
    CACHE_ALL_KEY = f"{CACHE_PREFIX}:all"
    CACHE_TTL = 300  # 5 minutes

    def __init__(self, db):
        self.repo = ProductRepository(db)

    def _get_cache_key(self, product_id: int = None) -> str:
        return f"{self.CACHE_PREFIX}:{product_id}" if product_id else self.CACHE_ALL_KEY

    def get_all(self, page: int = 1, size: int = 10, filters: Optional[Dict] = None):
        cache_key = f"{self.CACHE_ALL_KEY}:page:{page}:size:{size}:filters:{json.dumps(filters or {})}"
        
        # Cache-Aside
        cached = cache.get(cache_key)
        if cached:
            return cached

        result = self.repo.get_paginated(page=page, size=size, filters=filters)
        cache.set(cache_key, result, expire=self.CACHE_TTL)
        return result

    def get_by_id(self, product_id: int):
        cache_key = self._get_cache_key(product_id)
        cached = cache.get(cache_key)
        if cached:
            return cached

        product = self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        cache.set(cache_key, product, expire=self.CACHE_TTL)
        return product

    def create(self, product_data: dict):
        # Validation
        if product_data.get("price", 0) <= 0:
            raise HTTPException(status_code=400, detail="Price must be greater than 0")
        if product_data.get("stock", -1) < 0:
            raise HTTPException(status_code=400, detail="Stock cannot be negative")

        product = self.repo.create(product_data)
        # Invalidate cache
        cache.delete(self.CACHE_ALL_KEY)
        return product

    def update(self, product_id: int, updates: dict):
        product = self.repo.update(product_id, updates)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        # Invalidate cache
        cache.delete(self.CACHE_ALL_KEY)
        cache.delete(self._get_cache_key(product_id))
        return product

    def delete(self, product_id: int):
        if not self.repo.delete(product_id):
            raise HTTPException(status_code=404, detail="Product not found")
        # Invalidate cache
        cache.delete(self.CACHE_ALL_KEY)
        cache.delete(self._get_cache_key(product_id))
        return {"message": "Product deleted successfully"}