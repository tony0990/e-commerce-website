import pytest
import json
from unittest.mock import patch
from app.core.cache import get_cache, set_cache, delete_cache, delete_pattern

# 1. Cache Hit Test
@patch("app.core.cache.redis_client")
def test_get_cache_hit(mock_redis):
    """Test retrieving existing data from cache (Cache Hit)."""
    # Prepare the mock data that Redis will return
    test_data = {"product_id": 1, "name": "Laptop"}
    mock_redis.get.return_value = json.dumps(test_data)
    
    # Execute the cache retrieval function
    result = get_cache("product:1")
    
    # Verify the result matches the expected output
    assert result == test_data
    mock_redis.get.assert_called_once_with("product:1")

# 2. Cache Miss Test
@patch("app.core.cache.redis_client")
def test_get_cache_miss(mock_redis):
    """Test retrieving non-existing data from cache (Cache Miss)."""
    # Simulate Redis finding no data for the requested key
    mock_redis.get.return_value = None
    
    # Execute the cache retrieval function
    result = get_cache("missing_key")
    
    # Verify the result is None
    assert result is None
    mock_redis.get.assert_called_once_with("missing_key")

# 3. Cache Set Test
@patch("app.core.cache.redis_client")
def test_set_cache(mock_redis):
    """Test saving data to cache."""
    # Simulate a successful save operation in Redis
    mock_redis.set.return_value = True
    
    data_to_save = {"category": "Electronics"}
    result = set_cache("category:1", data_to_save, expire=600)
    
    # Verify the execution was successful
    assert result is True
    mock_redis.set.assert_called_once()
    
    # Ensure the data was serialized to JSON correctly before saving
    called_args = mock_redis.set.call_args[0]
    called_kwargs = mock_redis.set.call_args[1]
    
    assert called_args[0] == "category:1"
    assert json.loads(called_args[1]) == data_to_save
    assert called_kwargs["ex"] == 600

# 4. Cache Invalidation Test (Single Key)
@patch("app.core.cache.redis_client")
def test_delete_cache(mock_redis):
    """Test deleting a single key from cache."""
    # Simulate a successful delete operation
    mock_redis.delete.return_value = 1
    
    result = delete_cache("cart:123")
    
    # Verify the delete function was called with the correct key
    assert result is True
    mock_redis.delete.assert_called_once_with("cart:123")

# 5. Cache Invalidation Test (Pattern)
@patch("app.core.cache.redis_client")
def test_delete_pattern(mock_redis):
    """Test deleting multiple keys using a pattern."""
    # Simulate scan_iter finding two keys matching the pattern
    mock_redis.scan_iter.return_value = iter(["product:1", "product:2"])
    mock_redis.delete.return_value = 2
    
    result = delete_pattern("product:*")
    
    # Verify both the scanning and deleting processes executed properly
    assert result is True
    mock_redis.scan_iter.assert_called_once_with(match="product:*")
    mock_redis.delete.assert_called_once_with("product:1", "product:2")

# 6. Redis Unavailable Test (Graceful Degradation)
@patch("app.core.cache.redis_client", None)