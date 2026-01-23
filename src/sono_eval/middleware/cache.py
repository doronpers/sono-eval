"""Response caching and performance optimization."""

import hashlib
import json
from functools import wraps
from typing import Any, Callable, Optional

from sono_eval.utils.logger import get_logger

logger = get_logger(__name__)

# Simple in-memory cache for demonstration
_cache: dict[str, tuple[Any, float]] = {}
_cache_ttl: dict[str, float] = {}


def cache_key(*args: Any, **kwargs: Any) -> str:
    """Generate cache key from function arguments."""
    key_parts = [str(arg) for arg in args]
    key_parts.extend([f"{k}={v}" for k, v in sorted(kwargs.items())])
    key_str = "|".join(key_parts)
    return hashlib.md5(key_str.encode(), usedforsecurity=False).hexdigest()  # noqa: B324


def cached(ttl_seconds: int = 300, key_func: Optional[Callable] = None):
    """Decorator for caching function results."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            cache_id = key_func(*args, **kwargs) if key_func else cache_key(*args, **kwargs)

            # Check if cached result exists and is still valid
            if cache_id in _cache:
                import time

                result, timestamp = _cache[cache_id]
                if time.time() - timestamp < ttl_seconds:
                    logger.debug(f"Cache hit for {func.__name__}")
                    return result

            # Call function and cache result
            result = await func(*args, **kwargs)
            import time

            _cache[cache_id] = (result, time.time())
            logger.debug(f"Cached result for {func.__name__}")
            return result

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            cache_id = key_func(*args, **kwargs) if key_func else cache_key(*args, **kwargs)

            # Check if cached result exists and is still valid
            if cache_id in _cache:
                import time

                result, timestamp = _cache[cache_id]
                if time.time() - timestamp < ttl_seconds:
                    logger.debug(f"Cache hit for {func.__name__}")
                    return result

            # Call function and cache result
            result = func(*args, **kwargs)
            import time

            _cache[cache_id] = (result, time.time())
            logger.debug(f"Cached result for {func.__name__}")
            return result

        # Determine if function is async
        import asyncio

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def invalidate_cache(pattern: Optional[str] = None) -> None:
    """Invalidate cache entries."""
    if pattern is None:
        _cache.clear()
        logger.info("Cleared entire cache")
    else:
        keys_to_remove = [k for k in _cache.keys() if pattern in k]
        for k in keys_to_remove:
            del _cache[k]
        logger.info(f"Invalidated {len(keys_to_remove)} cache entries matching '{pattern}'")


def get_cache_stats() -> dict[str, Any]:
    """Get cache statistics."""
    return {"cached_entries": len(_cache), "memory_usage_estimate": len(json.dumps(_cache))}
