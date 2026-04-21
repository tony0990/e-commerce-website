"""
Cache Service (Hanfy + Tony)
==============================
Simple in-memory caching service.
Falls back gracefully when Redis is unavailable.
"""

import json
import time
from typing import Optional, Any, Dict
from app.core.config import settings


class CacheService:
    """
    In-memory cache service with TTL support.
    Uses a simple dictionary-based cache as fallback when Redis is unavailable.
    """

    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._default_ttl = settings.CACHE_EXPIRE_SECONDS

    async def get(self, key: str) -> Optional[Any]:
        """
        Get a value from cache.

        Args:
            key: The cache key.

        Returns:
            Cached value or None if expired/not found.
        """
        if key in self._cache:
            entry = self._cache[key]
            if entry["expires_at"] > time.time():
                return entry["value"]
            else:
                del self._cache[key]
        return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Set a value in cache with TTL.

        Args:
            key: The cache key.
            value: The value to cache.
            ttl: Time to live in seconds. Uses default if not specified.

        Returns:
            True if successful.
        """
        ttl = ttl or self._default_ttl
        self._cache[key] = {
            "value": value,
            "expires_at": time.time() + ttl,
        }
        return True

    async def delete(self, key: str) -> bool:
        """Delete a key from cache."""
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    async def exists(self, key: str) -> bool:
        """Check if a key exists and is not expired."""
        value = await self.get(key)
        return value is not None

    async def clear(self) -> bool:
        """Clear all cached entries."""
        self._cache.clear()
        return True

    async def clear_pattern(self, pattern: str) -> int:
        """
        Clear cache keys matching a pattern.
        Simple glob-style matching (prefix*).
        """
        prefix = pattern.rstrip("*")
        keys_to_delete = [k for k in self._cache if k.startswith(prefix)]
        for key in keys_to_delete:
            del self._cache[key]
        return len(keys_to_delete)

    async def get_stats(self) -> dict:
        """Get cache statistics."""
        now = time.time()
        active_keys = sum(1 for v in self._cache.values() if v["expires_at"] > now)
        expired_keys = len(self._cache) - active_keys
        return {
            "total_keys": len(self._cache),
            "active_keys": active_keys,
            "expired_keys": expired_keys,
        }


# Singleton cache instance
cache_service = CacheService()
