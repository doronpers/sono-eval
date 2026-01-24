"""Rate limiting middleware for production API protection.

Supports both Redis backend (for distributed deployments) and
in-memory fallback (for single-instance deployments).
"""

import asyncio
import os
import time
from typing import Callable, Dict, List, Optional

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from sono_eval.utils.logger import get_logger

logger = get_logger(__name__)


class RateLimiterState:
    """In-memory state for rate limiting (single-instance fallback)."""

    def __init__(self, max_requests: int, window_seconds: int):
        """Initialize rate limiter state."""
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[float]] = {}
        self.lock = asyncio.Lock()

    async def is_allowed(self, key: str) -> bool:
        """Check if request is allowed."""
        async with self.lock:
            now = time.time()
            window_start = now - self.window_seconds

            if key not in self.requests:
                self.requests[key] = []

            # Remove old requests outside window
            self.requests[key] = [
                req_time for req_time in self.requests[key] if req_time > window_start
            ]

            # Check if limit exceeded
            if len(self.requests[key]) >= self.max_requests:
                return False

            # Record this request
            self.requests[key].append(now)

            # Cleanup old keys periodically
            if len(self.requests) > 10000:
                keys_to_remove = [
                    k for k, v in self.requests.items() if not v or v[0] < window_start
                ]
                for k in keys_to_remove:
                    del self.requests[k]

            return True

    def get_remaining(self, key: str) -> int:
        """Get remaining requests for a key."""
        if key not in self.requests:
            return self.max_requests
        return max(0, self.max_requests - len(self.requests[key]))


class RedisRateLimiterState:
    """Redis-backed state for rate limiting (distributed deployments)."""

    def __init__(self, max_requests: int, window_seconds: int, redis_url: str):
        """Initialize Redis rate limiter state."""
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.redis_url = redis_url
        self._redis: Optional[object] = None
        self._initialized = False

    def _get_redis(self) -> Optional[object]:
        """Lazy initialization of Redis client."""
        if self._initialized:
            return self._redis

        try:
            import redis

            self._redis = redis.from_url(
                self.redis_url,
                socket_connect_timeout=2,
                socket_timeout=2,
            )
            # Test connection
            self._redis.ping()  # type: ignore
            self._initialized = True
            logger.info("Redis rate limiter connected successfully")
            return self._redis
        except ImportError:
            logger.warning("Redis package not installed, rate limiting will use memory")
            self._initialized = True
            return None
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}, falling back to memory")
            self._initialized = True
            return None

    async def is_allowed(self, key: str) -> bool:
        """Check if request is allowed using Redis sliding window."""
        redis_client = self._get_redis()
        if redis_client is None:
            return True  # Allow if Redis unavailable (fallback handles it)

        try:
            now = time.time()
            window_start = now - self.window_seconds
            redis_key = f"ratelimit:{key}"

            # Use Redis pipeline for atomic operations
            pipe = redis_client.pipeline()  # type: ignore

            # Remove old entries outside window
            pipe.zremrangebyscore(redis_key, 0, window_start)

            # Count current requests in window
            pipe.zcard(redis_key)

            # Add current request with score = timestamp
            pipe.zadd(redis_key, {str(now): now})

            # Set expiry on key
            pipe.expire(redis_key, self.window_seconds + 1)

            results = pipe.execute()
            current_count = results[1]  # zcard result

            if current_count >= self.max_requests:
                # Remove the request we just added
                redis_client.zrem(redis_key, str(now))  # type: ignore
                return False

            return True

        except Exception as e:
            logger.debug(f"Redis rate limit check failed: {e}")
            return True  # Allow on Redis errors (fail open)

    def get_remaining(self, key: str) -> int:
        """Get remaining requests for a key."""
        redis_client = self._get_redis()
        if redis_client is None:
            return self.max_requests

        try:
            redis_key = f"ratelimit:{key}"
            now = time.time()
            window_start = now - self.window_seconds

            # Clean old entries and count
            redis_client.zremrangebyscore(redis_key, 0, window_start)  # type: ignore
            current_count = redis_client.zcard(redis_key)  # type: ignore
            return max(0, self.max_requests - current_count)
        except Exception:
            return self.max_requests


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware with Redis backend and memory fallback."""

    def __init__(
        self,
        app: object,
        max_requests_per_minute: int = 60,
        max_requests_per_hour: int = 1000,
        exclude_paths: Optional[List[str]] = None,
        redis_url: Optional[str] = None,
    ):
        """
        Initialize rate limit middleware.

        Args:
            app: FastAPI application
            max_requests_per_minute: Max requests per minute per client
            max_requests_per_hour: Max requests per hour per client
            exclude_paths: Paths to exclude from rate limiting
            redis_url: Redis URL for distributed rate limiting (optional)
        """
        super().__init__(app)

        # Get Redis URL from parameter or environment
        redis_url = redis_url or os.environ.get("RATE_LIMIT_REDIS_URL")
        use_redis = os.environ.get("RATE_LIMIT_REDIS_ENABLED", "true").lower() in (
            "true",
            "1",
            "yes",
        )

        # Initialize rate limiters
        if use_redis and redis_url:
            self.per_minute: RateLimiterState | RedisRateLimiterState = RedisRateLimiterState(
                max_requests_per_minute, 60, redis_url
            )
            self.per_hour: RateLimiterState | RedisRateLimiterState = RedisRateLimiterState(
                max_requests_per_hour, 3600, redis_url
            )
            self.backend = "redis"
            logger.info("Rate limiting configured with Redis backend")
        else:
            self.per_minute = RateLimiterState(max_requests_per_minute, 60)
            self.per_hour = RateLimiterState(max_requests_per_hour, 3600)
            self.backend = "memory"
            logger.info("Rate limiting configured with in-memory backend")

        # Memory fallback for Redis failures
        self._memory_fallback_minute = RateLimiterState(max_requests_per_minute, 60)
        self._memory_fallback_hour = RateLimiterState(max_requests_per_hour, 3600)

        self.exclude_paths = exclude_paths or [
            "/health",
            "/api/v1/health",
            "/docs",
            "/openapi.json",
            "/api/v1/status/liveness",
            "/api/v1/status/readiness",
        ]

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Check rate limits before processing request."""
        # Skip rate limiting for excluded paths
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        # Get client identifier (IP or X-Forwarded-For)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # Take first IP from X-Forwarded-For header
            client_ip = forwarded_for.split(",")[0].strip()
        else:
            client_ip = request.client.host if request.client else "unknown"

        request_id = getattr(request.state, "request_id", "unknown")

        # Check per-minute limit
        minute_allowed = await self.per_minute.is_allowed(f"{client_ip}:minute")
        if not minute_allowed:
            # Try memory fallback if using Redis
            if self.backend == "redis":
                minute_allowed = await self._memory_fallback_minute.is_allowed(
                    f"{client_ip}:minute"
                )

        if not minute_allowed:
            logger.warning(
                "Rate limit (per-minute) exceeded",
                extra={"client_ip": client_ip, "request_id": request_id},
            )
            raise HTTPException(
                status_code=429,
                detail={
                    "error_code": "RATE_LIMIT_EXCEEDED",
                    "message": (
                        "Too many requests. Maximum "
                        f"{self.per_minute.max_requests} requests per minute."
                    ),
                    "retry_after": 60,
                },
            )

        # Check per-hour limit
        hour_allowed = await self.per_hour.is_allowed(f"{client_ip}:hour")
        if not hour_allowed:
            if self.backend == "redis":
                hour_allowed = await self._memory_fallback_hour.is_allowed(f"{client_ip}:hour")

        if not hour_allowed:
            logger.warning(
                "Rate limit (per-hour) exceeded",
                extra={"client_ip": client_ip, "request_id": request_id},
            )
            raise HTTPException(
                status_code=429,
                detail={
                    "error_code": "RATE_LIMIT_EXCEEDED",
                    "message": (
                        "Too many requests. Maximum "
                        f"{self.per_hour.max_requests} requests per hour."
                    ),
                    "retry_after": 3600,
                },
            )

        response = await call_next(request)

        # Add rate limit headers
        remaining = self.per_minute.get_remaining(f"{client_ip}:minute")
        response.headers["X-RateLimit-Limit"] = str(self.per_minute.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Backend"] = self.backend

        return response
