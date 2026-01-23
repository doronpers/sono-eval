"""Rate limiting middleware for production API protection."""

import asyncio
import time
from typing import Callable, Dict, Optional

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from sono_eval.utils.logger import get_logger

logger = get_logger(__name__)


class RateLimiterState:
    """State for rate limiting."""

    def __init__(self, max_requests: int, window_seconds: int):
        """Initialize rate limiter state."""
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = {}
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

            # Cleanup old keys
            if len(self.requests) > 10000:  # Prevent unbounded memory
                keys_to_remove = [
                    k for k, v in self.requests.items() if not v or v[0] < window_start
                ]
                for k in keys_to_remove:
                    del self.requests[k]

            return True


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware for API protection."""

    def __init__(
        self,
        app,
        max_requests_per_minute: int = 60,
        max_requests_per_hour: int = 1000,
        exclude_paths: Optional[list] = None,
    ):
        """Initialize rate limit middleware."""
        super().__init__(app)
        self.per_minute = RateLimiterState(max_requests_per_minute, 60)
        self.per_hour = RateLimiterState(max_requests_per_hour, 3600)
        self.exclude_paths = exclude_paths or [
            "/health",
            "/api/v1/health",
            "/docs",
            "/openapi.json",
        ]

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Check rate limits before processing request."""
        # Skip rate limiting for excluded paths
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        # Get client identifier (IP or X-Forwarded-For)
        client_ip = request.headers.get(
            "X-Forwarded-For", request.client.host if request.client else "unknown"
        )

        # Check per-minute limit
        if not await self.per_minute.is_allowed(f"{client_ip}:minute"):
            logger.warning(
                "Rate limit (per-minute) exceeded",
                extra={"client_ip": client_ip, "request_id": request.state.request_id},
            )
            raise HTTPException(
                status_code=429,
                detail={
                    "error_code": "RATE_LIMIT_EXCEEDED",
                    "message": "Too many requests. Maximum 60 requests per minute.",
                    "retry_after": 60,
                },
            )

        # Check per-hour limit
        if not await self.per_hour.is_allowed(f"{client_ip}:hour"):
            logger.warning(
                "Rate limit (per-hour) exceeded",
                extra={"client_ip": client_ip, "request_id": request.state.request_id},
            )
            raise HTTPException(
                status_code=429,
                detail={
                    "error_code": "RATE_LIMIT_EXCEEDED",
                    "message": "Too many requests. Maximum 1000 requests per hour.",
                    "retry_after": 3600,
                },
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.per_minute.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(
            max(
                0,
                self.per_minute.max_requests
                - len(self.per_minute.requests.get(f"{client_ip}:minute", [])),  # noqa: B113
            )
        )
        return response
