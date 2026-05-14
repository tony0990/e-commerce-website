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
        socket_timeout=2,
    )
    redis_client.ping()
    logger.success("Redis connected successfully")
except Exception as e:
    logger.warning(f"Redis not available: {e}. Caching will be disabled.")
    redis_client = None


def get_cache(key: str) -> Optional[Any]:
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


def set_cache(key: str, value: Any, expire: int = 300) -> bool:
    if not redis_client:
        return False
    try:
        redis_client.set(key, json.dumps(value, default=str), ex=expire)
        return True
    except Exception as e:
        logger.error(f"Cache set error: {e}")
        return False


def delete_cache(key: str) -> bool:
    if not redis_client:
        return False
    try:
        redis_client.delete(key)
        return True
    except Exception as e:
        logger.error(f"Cache delete error: {e}")
        return False


def delete_pattern(pattern: str = "product:*") -> bool:
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


# Aliases expected by app/services/cache_service.py
def get(key: str) -> Optional[Any]:
    return get_cache(key)


def set(key: str, value: Any, expire: int = 300) -> bool:
    return set_cache(key, value, expire)


def delete(key: str) -> bool:
    return delete_cache(key)