import redis
import json
from typing import Any, Optional
from loguru import logger

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
    logger.success("Redis connected successfully")
except Exception as e:
    logger.warning(f"Redis not available: {e}. Caching will be disabled.")
    redis_client = None


def get_cache(key: str) -> Optional[Any]:
    """Get data from cache"""
    if not redis_client:
        return None
    try:
        data = redis_client.get(key)
        if data:
            logger.info(f"The Data Has Successfully Gathered For The Key: {key}")
            return json.loads(data)
        return None
    except Exception as e:
        logger.error(f"Cache get error: {e}")
        return None


def set_cache(key: str, value: Any, expire: int = 300) -> bool:
    """Set data in cache (expire in seconds, default 5 minutes)"""
    if not redis_client:
        return False
    try:
        redis_client.set(
            key,
            json.dumps(value, default=str),
            ex=expire
        )
        logger.info(f"The Key Saved Successfully: {key}")
        return True
    except Exception as e:
        logger.error(f"Cache set error: {e}")
        return False


def delete_cache(key: str) -> bool:
    """Delete key from cache"""
    if not redis_client:
        return False
    try:
        redis_client.delete(key)
        logger.info(f"The Cache Has Successfully Deleted For Key: {key}")
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
            logger.info(f"Successfully deleted {len(keys)} keys matching pattern: {pattern}")
        return True
    except Exception as e:
        logger.error(f"Cache delete_pattern error: {e}")
        return False