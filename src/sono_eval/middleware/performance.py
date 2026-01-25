"""Request logging and performance monitoring middleware."""

import logging
import time
from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from sono_eval.utils.logger import get_logger

logger = get_logger(__name__)


class PerformanceLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for detailed request/response logging and performance monitoring."""

    def __init__(self, app, slow_request_threshold_ms: int = 1000):
        """Initialize performance logging middleware."""
        super().__init__(app)
        self.slow_request_threshold = slow_request_threshold_ms / 1000

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Log request and response details."""
        request_id = getattr(request.state, "request_id", "unknown")
        start_time = time.time()

        # Log incoming request
        logger.info(
            f"Incoming request: {request.method} {request.url.path}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client_ip": request.client.host if request.client else "unknown",
            },
        )

        try:
            response = await call_next(request)
            duration = time.time() - start_time

            # Log response
            log_level = (
                logging.WARNING
                if duration > self.slow_request_threshold
                else logging.INFO
            )
            log_message = (
                f"Request completed: {request.method} {request.url.path} "
                f"returned {response.status_code} in {duration:.3f}s"
            )

            logger.log(
                log_level,
                log_message,
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": int(duration * 1000),
                },
            )

            response.headers["X-Process-Time"] = str(duration)
            return response  # type: ignore

        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f"Request failed: {request.method} {request.url.path} after {duration:.3f}s",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "duration_ms": int(duration * 1000),
                    "error": str(e),
                },
            )
            raise
