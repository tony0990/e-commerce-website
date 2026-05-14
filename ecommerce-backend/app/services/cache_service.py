from app.core.cache import get_cache, set_cache, delete_cache, delete_pattern
from typing import Any, Optional
import logging

logger = logging.getLogger(__name__)

class CacheService:
    """
    Service layer for cache operations.
    """

    @staticmethod
    def get(key: str) -> Optional[Any]:
        """Get item from cache"""
        return get_cache(key)

    @staticmethod
    def set(key: str, value: Any, expire: int = 300) -> bool:
        """Set item in cache with expiration time"""
        return set_cache(key, value, expire)

    @staticmethod
    def delete(key: str) -> bool:
        """Delete item from cache"""
        return delete_cache(key)

    @staticmethod
    def delete_pattern(pattern: str) -> bool:
        """Delete multiple keys using pattern (e.g., 'product:*')"""
        return delete_pattern(pattern)

    @staticmethod
    def invalidate_product_cache(product_id: Optional[int] = None):
        """Invalidate all product-related cache when data changes"""
        try:
            # Invalidate list cache
            delete_pattern("product:all*")
            delete_pattern("product:page*")
            
            # Invalidate single product cache if ID is provided
            if product_id:
                delete_cache(f"product:{product_id}")
            
            logger.info(f"Product cache invalidated {'for ID ' + str(product_id) if product_id else 'globally'}")
        except Exception as e:
            logger.error(f"Failed to invalidate product cache: {e}")