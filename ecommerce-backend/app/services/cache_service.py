"""
Cache Service (Hanfy + Tony)
==============================
Simple in-memory caching service.
Falls back gracefully when Redis is unavailable.
"""

import json
import time
from typing import Optional, Any, Dict
import redis.asyncio as redis
from app.core.config import settings
from loguru import logger


class CacheService:
    """
    Cache service with Redis support and local memory fallback.
    Implements Cache-Aside Pattern utilities.
    """

    def __init__(self):
        self._local_cache: Dict[str, Dict[str, Any]] = {}
        self._default_ttl = settings.CACHE_EXPIRE_SECONDS
        self._redis: Optional[redis.Redis] = None
        self._use_redis = False

    async def _get_redis(self) -> redis.Redis:
        """Lazy initialization of Redis connection."""
        if self._redis is None:
            try:
                self._redis = redis.from_url(
                    settings.REDIS_URL, 
                    decode_responses=True,
                    socket_connect_timeout=2
                )
                await self._redis.ping()
                self._use_redis = True
                logger.info(f"Connected to Redis at {settings.REDIS_URL}")
            except Exception as e:
                logger.warning(f"Failed to connect to Redis: {str(e)}. Falling back to in-memory cache.")
                self._use_redis = False
        return self._redis

    async def get(self, key: str) -> Optional[Any]:
        """Get a value from Redis or local cache."""
        if self._use_redis or self._redis is None:
            try:
                r = await self._get_redis()
                if self._use_redis:
                    value = await r.get(key)
                    return json.loads(value) if value else None
            except Exception as e:
                logger.error(f"Redis GET failed for key {key}: {str(e)}")
                self._use_redis = False

        # Fallback to local cache
        if key in self._local_cache:
            entry = self._local_cache[key]
            if entry["expires_at"] > time.time():
                return entry["value"]
            else:
                del self._local_cache[key]
        return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set a value in Redis and local cache."""
        ttl = ttl or self._default_ttl
        
        # Try Redis
        if self._use_redis or self._redis is None:
            try:
                r = await self._get_redis()
                if self._use_redis:
                    await r.set(key, json.dumps(value), ex=ttl)
            except Exception as e:
                logger.error(f"Redis SET failed for key {key}: {str(e)}")
                self._use_redis = False

        # Always update local cache as buffer
        self._local_cache[key] = {
            "value": value,
            "expires_at": time.time() + ttl,
        }
        return True

    async def delete(self, key: str) -> bool:
        """Delete a key from Redis and local cache."""
        success = False
        if self._use_redis:
            try:
                r = await self._get_redis()
                await r.delete(key)
                success = True
            except Exception as e:
                logger.error(f"Redis DELETE failed for key {key}: {str(e)}")
        
        if key in self._local_cache:
            del self._local_cache[key]
            success = True
        return success

    async def exists(self, key: str) -> bool:
        """Check if a key exists and is not expired."""
        value = await self.get(key)
        return value is not None

    async def clear(self) -> bool:
        """Clear all cached entries."""
        self._local_cache.clear()
        return True

    async def clear_pattern(self, pattern: str) -> int:
        """Clear cache keys matching a pattern."""
        count = 0
        if self._use_redis:
            try:
                r = await self._get_redis()
                keys = await r.keys(pattern)
                if keys:
                    count = await r.delete(*keys)
            except Exception as e:
                logger.error(f"Redis clear_pattern failed: {str(e)}")

        # Local clear
        prefix = pattern.rstrip("*")
        local_keys = [k for k in self._local_cache if k.startswith(prefix)]
        for k in local_keys:
            if k not in self._local_cache: continue
            del self._local_cache[k]
            if not self._use_redis: count += 1
            
        return count

    async def get_stats(self) -> dict:
        """Get cache statistics."""
        now = time.time()
        active_keys = sum(1 for v in self._local_cache.values() if v["expires_at"] > now)
        expired_keys = len(self._local_cache) - active_keys
        return {
            "total_keys": len(self._local_cache),
            "active_keys": active_keys,
            "expired_keys": expired_keys,
        }


# Singleton cache instance
cache_service = CacheService()
