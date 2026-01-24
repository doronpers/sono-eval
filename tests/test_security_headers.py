"""Tests for security headers middleware."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from sono_eval.middleware.security_headers import SecurityHeadersMiddleware


@pytest.fixture
def app():
    """Create a test application."""
    app = FastAPI()

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app


def test_startup_headers_development(app):
    """Test that headers are added in development mode."""
    app.add_middleware(SecurityHeadersMiddleware, mode="development")
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "Strict-Transport-Security" not in response.headers  # Not in dev


def test_startup_headers_production(app):
    """Test that HSTS is added in production mode."""
    app.add_middleware(SecurityHeadersMiddleware, mode="production")
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert "Strict-Transport-Security" in response.headers
    assert "max-age=63072000" in response.headers["Strict-Transport-Security"]


def test_headers_not_duplicated():
    """Test that middleware doesn't overwrite existing headers."""
    app = FastAPI()

    from fastapi import Response

    @app.get("/")
    async def root(response: Response):
        # Endpoint sets its own header
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        return {"message": "Hello"}

    # Middleware should respect existing headers?
    # Our implementation says: if key not in response.headers: response.headers[key] = value
    # But checking response.headers in middleware happens AFTER endpoint?
    # Yes, middleware calls `response = await call_next(request)` then checks headers.
    # So endpoint headers come first.

    # Let's test with a custom response
    from fastapi import Response

    @app.get("/custom")
    async def custom():
        response = Response(content="ok")
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        return response

    app.add_middleware(SecurityHeadersMiddleware, mode="production")
    client = TestClient(app)

    response = client.get("/custom")

    assert response.headers["X-Frame-Options"] == "SAMEORIGIN"  # Should be preserved
    assert response.headers["X-Content-Type-Options"] == "nosniff"  # Should be added
