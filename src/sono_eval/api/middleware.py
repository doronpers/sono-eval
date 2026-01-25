"""Middleware for security headers."""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers to every response."""

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        response = await call_next(request)

        # HSTS (HTTP Strict Transport Security)
        # Max-age: 1 year (31536000 seconds), include subdomains
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )

        # X-Frame-Options (Prevent Clickjacking)
        response.headers["X-Frame-Options"] = "DENY"

        # X-Content-Type-Options (Prevent MIME Sniffing)
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Content-Security-Policy (Restricted sources)
        # Default: self only. Adjust as needed for external scripts/images.
        # Allowing 'unsafe-inline' and 'unsafe-eval' for now to support React/FastAPI dev mode if needed,
        # but should be tightened for production.
        csp = (
            "default-src 'self'; "
            "img-src 'self' data: https:; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "object-src 'none'; "
            "base-uri 'self';"
        )
        response.headers["Content-Security-Policy"] = csp

        # Referrer-Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        return response
