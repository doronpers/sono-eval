"""Tests for rate limiting."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from sono_eval.api.main import app
from sono_eval.auth import models, dependencies
from sono_eval.api.limiter import limiter


@pytest.fixture(autouse=True)
def reset_limiter():
    """Reset rate limiter before each test."""
    # Resetting the storage of the limiter
    # Attempting to use internal storage reset if reset() is not directly available
    # slowapi Limiter usually has a way, defaulting to simply clearing storage if possible
    # Inspecting structure: limiter.limiter is the limits.Limiter.
    # But usually a simple reset works if exposed.
    # Let's try mocking or just relying on internal clear.
    if hasattr(limiter, "reset"):
        limiter.reset()
    elif hasattr(limiter, "limiter") and hasattr(limiter.limiter, "storage"):
        limiter.limiter.storage.clear()


# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    """Create a new database session for a test."""
    models.Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        models.Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    """Create a test client with a test database session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[dependencies.get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_rate_limit_register(client):
    """Test rate limiting on register endpoint."""
    # Should work 5 times
    for i in range(5):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": f"test{i}@example.com",
                "password": "password123",
                "full_name": f"Test User {i}",
            },
        )
        assert response.status_code == 200

    # 6th time should fail
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "bloat@example.com",
            "password": "password123",
            "full_name": "Bloat User",
        },
    )
    assert response.status_code == 429


def test_security_headers_present(client):
    """Test that security headers are present in response."""
    response = client.get("/health")
    headers = response.headers

    assert headers.get("X-Frame-Options") == "DENY"
    assert headers.get("X-Content-Type-Options") == "nosniff"
    assert "Strict-Transport-Security" in headers
    assert "Content-Security-Policy" in headers
