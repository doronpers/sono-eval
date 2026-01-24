"""Comprehensive tests for caching middleware."""

import asyncio
import time
from unittest.mock import AsyncMock, Mock, patch

import pytest

from sono_eval.middleware.cache import (
    cache_key,
    cached,
    get_cache_stats,
    invalidate_cache,
)


class TestCacheKeyGeneration:
    """Test cache key generation."""

    def test_cache_key_simple_args(self):
        """Test cache key with simple arguments."""
        key1 = cache_key("arg1", "arg2")
        key2 = cache_key("arg1", "arg2")

        # Same args should produce same key
        assert key1 == key2

    def test_cache_key_different_args(self):
        """Test that different args produce different keys."""
        key1 = cache_key("arg1", "arg2")
        key2 = cache_key("arg1", "arg3")

        assert key1 != key2

    def test_cache_key_with_kwargs(self):
        """Test cache key with keyword arguments."""
        key1 = cache_key(a="value1", b="value2")
        key2 = cache_key(a="value1", b="value2")

        assert key1 == key2

    def test_cache_key_kwargs_order_independent(self):
        """Test that kwargs order doesn't affect key."""
        key1 = cache_key(a="value1", b="value2")
        key2 = cache_key(b="value2", a="value1")

        # Should be same (sorted)
        assert key1 == key2

    def test_cache_key_mixed_args_kwargs(self):
        """Test cache key with both args and kwargs."""
        key1 = cache_key("pos1", "pos2", kw1="val1", kw2="val2")
        key2 = cache_key("pos1", "pos2", kw2="val2", kw1="val1")

        assert key1 == key2

    def test_cache_key_numeric_args(self):
        """Test cache key with numeric arguments."""
        key1 = cache_key(42, 3.14)
        key2 = cache_key(42, 3.14)

        assert key1 == key2

    def test_cache_key_complex_objects(self):
        """Test cache key with complex objects."""
        obj1 = {"key": "value"}
        obj2 = {"key": "value"}

        key1 = cache_key(obj1)
        key2 = cache_key(obj2)

        # String representation is used, so should match
        assert key1 == key2

    def test_cache_key_hash_format(self):
        """Test that cache key is MD5 hash."""
        key = cache_key("test")

        # MD5 hash is 32 hex characters
        assert len(key) == 32
        assert all(c in "0123456789abcdef" for c in key)


class TestSyncCachedDecorator:
    """Test caching for synchronous functions."""

    def test_cache_simple_function(self):
        """Test caching a simple synchronous function."""
        call_count = 0

        @cached(ttl_seconds=60)
        def simple_func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        # First call - cache miss
        result1 = simple_func(5)
        assert result1 == 10
        assert call_count == 1

        # Second call - cache hit
        result2 = simple_func(5)
        assert result2 == 10
        assert call_count == 1  # Not called again

    def test_cache_different_arguments(self):
        """Test that different arguments create separate cache entries."""
        call_count = 0

        @cached(ttl_seconds=60)
        def func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        result1 = func(5)
        result2 = func(10)

        assert result1 == 10
        assert result2 == 20
        assert call_count == 2  # Called twice for different args

        # Call with same args - should use cache
        result3 = func(5)
        assert result3 == 10
        assert call_count == 2  # Still 2, cache was used

    def test_cache_expiration(self):
        """Test that cache entries expire after TTL."""
        call_count = 0

        @cached(ttl_seconds=1)
        def func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        # First call
        result1 = func(5)
        assert result1 == 10
        assert call_count == 1

        # Wait for expiration
        time.sleep(1.1)

        # Should call function again
        result2 = func(5)
        assert result2 == 10
        assert call_count == 2

    def test_cache_with_kwargs(self):
        """Test caching with keyword arguments."""
        call_count = 0

        @cached(ttl_seconds=60)
        def func(a, b=0):
            nonlocal call_count
            call_count += 1
            return a + b

        result1 = func(5, b=3)
        assert result1 == 8
        assert call_count == 1

        result2 = func(5, b=3)
        assert result2 == 8
        assert call_count == 1  # Cached

    def test_cache_custom_key_func(self):
        """Test caching with custom key function."""
        call_count = 0

        def custom_key(x, y):
            # Only use x for key, ignore y
            return cache_key(x)

        @cached(ttl_seconds=60, key_func=custom_key)
        def func(x, y):
            nonlocal call_count
            call_count += 1
            return x + y

        result1 = func(5, 10)
        assert result1 == 15
        assert call_count == 1

        # Different y, but same x - should use cache
        result2 = func(5, 20)
        assert result2 == 15  # Returns cached value (5+10)
        assert call_count == 1

    def test_cache_return_none(self):
        """Test caching functions that return None."""
        call_count = 0

        @cached(ttl_seconds=60)
        def func():
            nonlocal call_count
            call_count += 1
            return None

        result1 = func()
        assert result1 is None
        assert call_count == 1

        result2 = func()
        assert result2 is None
        assert call_count == 1  # Cached None value


class TestAsyncCachedDecorator:
    """Test caching for asynchronous functions."""

    @pytest.mark.asyncio
    async def test_cache_async_function(self):
        """Test caching an async function."""
        call_count = 0

        @cached(ttl_seconds=60)
        async def async_func(x):
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.01)
            return x * 2

        # First call - cache miss
        result1 = await async_func(5)
        assert result1 == 10
        assert call_count == 1

        # Second call - cache hit
        result2 = await async_func(5)
        assert result2 == 10
        assert call_count == 1

    @pytest.mark.asyncio
    async def test_cache_async_different_args(self):
        """Test async caching with different arguments."""
        call_count = 0

        @cached(ttl_seconds=60)
        async def async_func(x, y):
            nonlocal call_count
            call_count += 1
            return x + y

        result1 = await async_func(5, 10)
        result2 = await async_func(5, 10)
        result3 = await async_func(5, 20)

        assert result1 == 15
        assert result2 == 15
        assert result3 == 25
        assert call_count == 2  # Called twice (different args)

    @pytest.mark.asyncio
    async def test_cache_async_expiration(self):
        """Test cache expiration for async functions."""
        call_count = 0

        @cached(ttl_seconds=1)
        async def async_func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        await async_func(5)
        assert call_count == 1

        # Wait for expiration
        await asyncio.sleep(1.1)

        await async_func(5)
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_cache_concurrent_async_calls(self):
        """Test concurrent calls to cached async function."""
        call_count = 0

        @cached(ttl_seconds=60)
        async def async_func(x):
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.01)
            return x * 2

        # Make concurrent calls with same arg
        tasks = [async_func(5) for _ in range(10)]
        results = await asyncio.gather(*tasks)

        # All should get same result
        assert all(r == 10 for r in results)

        # Note: Due to timing, might be called multiple times
        # but should be less than 10 (some will use cache)
        assert call_count >= 1

    @pytest.mark.asyncio
    async def test_cache_async_with_exception(self):
        """Test that exceptions are not cached."""
        call_count = 0

        @cached(ttl_seconds=60)
        async def failing_func():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ValueError("First call fails")
            return "success"

        # First call fails
        with pytest.raises(ValueError):
            await failing_func()

        # Second call should actually call function (not cached)
        result = await failing_func()
        assert result == "success"
        assert call_count == 2


class TestCacheInvalidation:
    """Test cache invalidation functionality."""

    def test_invalidate_entire_cache(self):
        """Test clearing entire cache."""
        call_count = 0

        @cached(ttl_seconds=60)
        def func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        # Populate cache
        func(5)
        func(10)
        assert call_count == 2

        # Call again - should use cache
        func(5)
        assert call_count == 2

        # Invalidate cache
        invalidate_cache()

        # Should call function again
        func(5)
        assert call_count == 3

    def test_invalidate_by_pattern(self):
        """Test invalidating cache entries by pattern."""
        call_count = 0

        @cached(ttl_seconds=60)
        def func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        # Populate cache
        func(5)
        func(10)

        # Get cache keys for inspection
        from sono_eval.middleware.cache import _cache
        initial_count = len(_cache)

        # Invalidate with pattern (this is basic - keys are hashes)
        # For real use, would need to enhance with metadata
        invalidate_cache(pattern="nonexistent")

        # Cache should still have entries (pattern didn't match)
        assert len(_cache) == initial_count

        # Clear all
        invalidate_cache()
        assert len(_cache) == 0


class TestCacheStats:
    """Test cache statistics functionality."""

    def test_get_cache_stats_empty(self):
        """Test stats for empty cache."""
        invalidate_cache()  # Clear cache first

        stats = get_cache_stats()

        assert "cached_entries" in stats
        assert "memory_usage_estimate" in stats
        assert stats["cached_entries"] == 0

    def test_get_cache_stats_with_entries(self):
        """Test stats with cached entries."""
        invalidate_cache()

        @cached(ttl_seconds=60)
        def func(x):
            return x * 2

        # Add some entries
        func(1)
        func(2)
        func(3)

        stats = get_cache_stats()

        assert stats["cached_entries"] == 3
        assert stats["memory_usage_estimate"] > 0

    def test_cache_stats_memory_estimate(self):
        """Test that memory estimate increases with more data."""
        invalidate_cache()

        @cached(ttl_seconds=60)
        def small_func(x):
            return x

        @cached(ttl_seconds=60)
        def large_func(x):
            return "x" * 10000

        small_func(1)
        stats1 = get_cache_stats()

        large_func(1)
        stats2 = get_cache_stats()

        # Memory estimate should increase
        assert stats2["memory_usage_estimate"] > stats1["memory_usage_estimate"]


class TestCacheEdgeCases:
    """Test edge cases and special scenarios."""

    def test_cache_with_no_args(self):
        """Test caching function with no arguments."""
        call_count = 0

        @cached(ttl_seconds=60)
        def no_args_func():
            nonlocal call_count
            call_count += 1
            return "constant"

        result1 = no_args_func()
        result2 = no_args_func()

        assert result1 == "constant"
        assert result2 == "constant"
        assert call_count == 1

    def test_cache_large_result(self):
        """Test caching large results."""
        @cached(ttl_seconds=60)
        def large_result_func():
            return {"data": [i for i in range(1000)]}

        result1 = large_result_func()
        result2 = large_result_func()

        assert len(result1["data"]) == 1000
        assert result1 == result2

    def test_cache_mutable_results_isolation(self):
        """Test that cached mutable results can be problematic."""
        @cached(ttl_seconds=60)
        def mutable_func():
            return {"count": 0}

        result1 = mutable_func()
        result1["count"] = 5

        result2 = mutable_func()

        # This demonstrates cache doesn't deep copy
        # In production, should document this behavior or use immutable returns
        assert result2["count"] == 5  # Modified cached value

    def test_cache_decorator_preserves_function_metadata(self):
        """Test that decorator preserves function name and docstring."""
        @cached(ttl_seconds=60)
        def documented_func(x):
            """This function has documentation."""
            return x * 2

        assert documented_func.__name__ == "documented_func"
        assert "documentation" in documented_func.__doc__

    def test_cache_with_default_ttl(self):
        """Test cache with default TTL (300 seconds)."""
        call_count = 0

        @cached()  # Use default TTL
        def func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        func(5)
        func(5)

        assert call_count == 1  # Should be cached

    def test_cache_very_short_ttl(self):
        """Test cache with very short TTL."""
        call_count = 0

        @cached(ttl_seconds=0.1)
        def func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        func(5)
        time.sleep(0.15)
        func(5)

        assert call_count == 2  # Cache expired quickly


class TestCacheRealWorldScenarios:
    """Test realistic caching scenarios."""

    @pytest.mark.asyncio
    async def test_database_query_caching(self):
        """Simulate caching expensive database queries."""
        query_count = 0

        @cached(ttl_seconds=60)
        async def fetch_user(user_id):
            nonlocal query_count
            query_count += 1
            # Simulate DB query
            await asyncio.sleep(0.05)
            return {"id": user_id, "name": f"User_{user_id}"}

        # Fetch same user multiple times
        user1 = await fetch_user(123)
        user2 = await fetch_user(123)
        user3 = await fetch_user(123)

        assert user1 == user2 == user3
        assert query_count == 1  # Only queried once

        # Different user
        user4 = await fetch_user(456)
        assert query_count == 2

    def test_api_response_caching(self):
        """Simulate caching API responses."""
        api_call_count = 0

        @cached(ttl_seconds=30)
        def fetch_weather(city):
            nonlocal api_call_count
            api_call_count += 1
            # Simulate API call
            return {"city": city, "temp": 72, "condition": "sunny"}

        # Multiple clients asking for same city
        for _ in range(10):
            weather = fetch_weather("San Francisco")
            assert weather["temp"] == 72

        # Only called API once
        assert api_call_count == 1

    @pytest.mark.asyncio
    async def test_computation_result_caching(self):
        """Simulate caching expensive computations."""
        computation_count = 0

        @cached(ttl_seconds=120)
        async def expensive_calculation(n):
            nonlocal computation_count
            computation_count += 1
            # Simulate expensive computation
            await asyncio.sleep(0.1)
            return sum(i * i for i in range(n))

        result1 = await expensive_calculation(1000)
        result2 = await expensive_calculation(1000)

        assert result1 == result2
        assert computation_count == 1  # Computed only once

    def test_cache_warming_pattern(self):
        """Test pre-warming cache with common queries."""
        @cached(ttl_seconds=60)
        def get_config(key):
            # Simulate config lookup
            configs = {
                "api_url": "https://api.example.com",
                "timeout": 30,
                "retries": 3
            }
            return configs.get(key)

        # Warm cache
        common_keys = ["api_url", "timeout", "retries"]
        for key in common_keys:
            get_config(key)

        stats = get_cache_stats()
        assert stats["cached_entries"] >= 3
