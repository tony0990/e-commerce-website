"""
Cache Service
=============
Service layer for cache operations.
Wraps Redis helper functions from app.core.cache.
"""

from typing import Any, Optional
import logging

from app.core.cache import (
    get,
    set,
    delete,
    delete_pattern,
)

logger = logging.getLogger(__name__)


class CacheService:
    """
    Service layer for cache operations.

    Provides a clean abstraction layer over Redis cache helpers.
    """

    @staticmethod
    def get(key: str) -> Optional[Any]:
        """
        Retrieve item from cache by key.
        """

        return get(key)

    @staticmethod
    def set(
        key: str,
        value: Any,
        expire: int = 300,
    ) -> bool:
        """
        Store item in cache with expiration time.

        Default expiration:
        300 seconds = 5 minutes
        """

        return set(key, value, expire)

    @staticmethod
    def delete(key: str) -> bool:
        """
        Delete one cache key.
        """

        return delete(key)

    @staticmethod
    def delete_pattern(pattern: str) -> bool:
        """
        Delete multiple keys using a pattern.

        Example:
        product:*
        """

        return delete_pattern(pattern)

    @staticmethod
    def invalidate_product_cache(
        product_id: Optional[int] = None,
    ) -> None:
        """
        Invalidate product-related cache after product updates.

        Example:
        - Product create
        - Product update
        - Product delete
        """

        try:
            delete_pattern("product:all*")
            delete_pattern("product:page*")

            if product_id:
                delete(f"product:{product_id}")

            logger.info(
                f"Product cache invalidated "
                f"{'for ID ' + str(product_id) if product_id else 'globally'}"
            )

        except Exception as e:
            logger.error(
                f"Failed to invalidate product cache: {e}"
            )


# Shared singleton instance used across the project
cache_service = CacheService()