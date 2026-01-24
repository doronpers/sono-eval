"""Integration tests for API endpoints."""

import sys
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# Mock celery before importing app
sys.modules["celery"] = MagicMock()

from sono_eval.api.main import app  # noqa: E402
from sono_eval.auth.dependencies import get_current_user  # noqa: E402
from sono_eval.auth.users import User  # noqa: E402


@pytest.fixture
def client_with_auth():
    """Create test client with authenticated user."""
    # Override auth to simulate logged-in user
    app.dependency_overrides[get_current_user] = lambda: User(username="testuser")

    with TestClient(app) as client:
        yield client

    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture
def client_no_auth():
    """Create test client without auth override."""
    with TestClient(app) as client:
        yield client


def test_file_upload_flow(client_with_auth):
    """Test full file upload flow with valid content."""
    files = {"file": ("test.py", b"def hello():\n    print('world')", "text/x-python")}

    with patch("sono_eval.api.main.tag_generator") as mock_tagger:
        mock_tag = MagicMock()
        mock_tag.model_dump.return_value = {"text": "python", "score": 0.99}
        mock_tagger.generate_tags.return_value = [mock_tag]

        response = client_with_auth.post("/api/v1/files/upload", files=files)

        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "test.py"
        assert data["status"] == "uploaded"
        assert len(data["tags"]) == 1
        assert data["tags"][0]["text"] == "python"


def test_file_upload_invalid_extension(client_with_auth):
    """Test upload with disallowed extension."""
    files = {"file": ("malicious.exe", b"binarycontent", "application/octet-stream")}

    response = client_with_auth.post("/api/v1/files/upload", files=files)

    assert response.status_code in [400, 422]
    assert "extension" in response.text.lower()


def test_rate_limiting_integration(client_no_auth):
    """
    Test rate limiting behavior.

    Note: Testing rate limits in integration requires hitting limits.
    Skipping to keep test suite fast. Logic covered in unit tests.
    """
    pytest.skip("Skipping rate limit integration test (requires high request volume)")
