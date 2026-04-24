# app/core/cache.py


import redis
import json
from typing import Any, Optional
import logging

logger = logging.getLogger(__name__)

# Global Redis client 
try:
    redis_client = redis.Redis(
        host="localhost",
        port=6379,
        db=0,
        decode_responses=True,
        socket_connect_timeout=2,
        socket_timeout=2
    )
    # Test connection
    redis_client.ping()
    logger.info(" Redis connected successfully")
except Exception as e:
    logger.warning(f" Redis not available: {e}. Caching will be disabled.")
    redis_client = None


def get(key: str) -> Optional[Any]:
    """Get data from cache"""
    if not redis_client:
        return None
    try:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        logger.error(f"Cache get error: {e}")
        return None


def set(key: str, value: Any, expire: int = 300) -> bool:
    """Set data in cache (expire in seconds, default 5 minutes)"""
    if not redis_client:
        return False
    try:
        redis_client.set(
            key, 
            json.dumps(value, default=str), 
            ex=expire
        )
        return True
    except Exception as e:
        logger.error(f"Cache set error: {e}")
        return False


def delete(key: str) -> bool:
    """Delete key from cache"""
    if not redis_client:
        return False
    try:
        redis_client.delete(key)
        return True
    except Exception as e:
        logger.error(f"Cache delete error: {e}")
        return False


def delete_pattern(pattern: str = "product:*") -> bool:
    """Delete multiple keys by pattern (useful for invalidation)"""
    if not redis_client:
        return False
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
        return True
    except Exception as e:
        logger.error(f"Cache delete_pattern error: {e}")
        return False