"""Middleware for adding security headers to all responses."""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware that adds security headers to all responses.

    Headers added:
    - X-Content-Type-Options: nosniff
    - X-Frame-Options: DENY
    - X-XSS-Protection: 1; mode=block
    - Strict-Transport-Security: max-age=63072000; includeSubDomains; preload (Production only)
    - Content-Security-Policy: default-src 'self'; img-src 'self' data:; script-src 'self';
      style-src 'self' 'unsafe-inline'
    - Referrer-Policy: strict-origin-when-cross-origin
    """

    def __init__(self, app: ASGIApp, mode: str = "production") -> None:
        """Initialize middleware with environment mode."""
        super().__init__(app)
        self.mode = mode

    async def dispatch(self, request, call_next):
        """Process the request and add security headers."""
        response = await call_next(request)

        # Baseline security headers
        # CSP: Allow unsafe-inline in development for easier debugging
        # In production, consider using nonces or hashes instead
        # Default to allowing unsafe-inline if mode is not explicitly production
        csp_script_src = "'self' 'unsafe-inline' 'unsafe-hashes'" if self.mode != "production" else "'self'"
        
        # Force set CSP header (overwrite if exists) to ensure correct policy
        # This ensures we always use the correct CSP for the current mode
        
        headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            # Basic CSP - allows inline styles and scripts in development
            "Content-Security-Policy": (
                "default-src 'self'; "
                "img-src 'self' data: https:; "
                f"script-src {csp_script_src}; "
                "style-src 'self' 'unsafe-inline'; "
                "object-src 'none'; "
                "base-uri 'self';"
            ),
        }

        # HSTS only in production/staging to avoid locking out localhost dev
        if self.mode in ["production", "staging"]:
            headers["Strict-Transport-Security"] = (
                "max-age=63072000; includeSubDomains; preload"
            )

        for key, value in headers.items():
            # Always set CSP header to ensure correct policy (overwrite if exists)
            # Other headers: Don't overwrite if already set (e.g. by specific endpoint)
            if key == "Content-Security-Policy":
                response.headers[key] = value
            elif key not in response.headers:
                response.headers[key] = value

        return response
