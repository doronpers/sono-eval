"""Tests for authentication system."""

import sys
from unittest.mock import MagicMock, patch

# Mock celery before importing the app (celery is optional)
sys.modules["celery"] = MagicMock()

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from sono_eval.api.main import app  # noqa: E402

# FAKE_USERS_DB is not used in tests directly, but was imported. Removing.


@pytest.fixture
def client():
    """Test client."""
    return TestClient(app)


def test_login_flow(client):
    """Test login with valid credentials."""
    response = client.post(
        "/api/v1/auth/token", data={"username": "admin", "password": "secret"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    """Test login with invalid password."""
    response = client.post(
        "/api/v1/auth/token", data={"username": "admin", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_unknown_user(client):
    """Test login with unknown user."""
    response = client.post(
        "/api/v1/auth/token", data={"username": "unknown", "password": "pass"}
    )
    assert response.status_code == 401


def test_protected_route_no_token(client):
    """Test accessing protected route without token."""
    # Using create_assessment as a protected route
    response = client.post("/api/v1/assessments", json={})
    assert response.status_code == 401


def test_protected_route_with_valid_token(client):
    """Test accessing protected route with valid token."""
    # Login first
    login_res = client.post(
        "/api/v1/auth/token", data={"username": "admin", "password": "secret"}
    )
    token = login_res.json()["access_token"]

    # Mock assessment engine to avoid actual processing logic failing
    with patch("sono_eval.api.main.assessment_engine") as _:
        # Mocking assess result would be complex, but we just want to pass Auth
        # If we get 422 (Validation Error), it means Auth passed!
        # If we get 401, Auth failed.

        response = client.post(
            "/api/v1/assessments",
            json={"candidate_id": "test", "submission_type": "code", "content": {}},
            headers={"Authorization": f"Bearer {token}"},
        )

        # We expect 422 because content is empty/invalid,
        # OR 200 if we mocked everything perfectly.
        # But definitely NOT 401.
        assert response.status_code != 401
