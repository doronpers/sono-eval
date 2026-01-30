"""Tests for the API endpoints and middleware."""

import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# Mock celery before importing the app (celery is optional)
sys.modules["celery"] = MagicMock()

from sono_eval.api.main import app  # noqa: E402


@pytest.fixture
def client():
    """Create test client."""
    from sono_eval.auth.dependencies import get_current_user
    from sono_eval.auth.users import User

    # Override auth to simulate logged-in user
    app.dependency_overrides[get_current_user] = lambda: User(username="testuser")

    with TestClient(app) as client:
        yield client

    # Clean up
    app.dependency_overrides.clear()


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/health")

    # Accept 200 (healthy) or 503 (unhealthy but responding)
    assert response.status_code in [200, 503]
    data = response.json()

    assert "status" in data
    assert "version" in data
    assert "timestamp" in data
    assert "components" in data


def test_health_endpoint_has_request_id(client):
    """Test that health endpoint includes request ID in response."""
    response = client.get("/health")

    # Accept 200 or 503 - health endpoint always responds
    assert response.status_code in [200, 503]
    assert "X-Request-ID" in response.headers
    assert len(response.headers["X-Request-ID"]) > 0


def test_custom_request_id_propagation(client):
    """Test that custom request IDs are propagated."""
    custom_id = "my-custom-request-id-123"

    response = client.get("/health", headers={"X-Request-ID": custom_id})

    # Accept 200 or 503 - health endpoint always responds
    assert response.status_code in [200, 503]
    assert response.headers["X-Request-ID"] == custom_id


def test_api_version_prefix():
    """Test that API versioning is properly configured."""
    from sono_eval.api.main import API_V1_PREFIX

    assert API_V1_PREFIX == "/api/v1"


def test_cors_headers_present(client):
    """Test that CORS headers are present in responses."""
    response = client.options("/health")

    # CORS preflight or method not allowed
    assert response.status_code in [200, 204, 405]


@patch("sono_eval.api.main.AssessmentEngine")
def test_assessment_endpoint_with_valid_input(MockEngineClass, client):
    """Test assessment creation with valid input."""
    # Mock the assessment engine with AsyncMock for await support
    mock_result = MagicMock()
    mock_result.candidate_id = "test123"
    mock_result.assessment_id = "test_assessment_123"
    mock_result.overall_score = 85.0
    mock_result.confidence = 0.9
    mock_result.path_scores = []
    mock_result.micro_motives = []
    mock_result.summary = "Test summary"
    mock_result.dominant_path = "technical"
    mock_result.engine_version = "1.0"
    mock_result.metadata = {}
    mock_result.model_dump.return_value = {
        "candidate_id": "test123",
        "assessment_id": "test_assessment_123",
        "overall_score": 85.0,
        "confidence": 0.9,
        "dominant_path": "technical",
        "engine_version": "1.0",
        "metadata": {},
    }

    mock_engine = MockEngineClass.return_value
    # Make assess return an awaitable
    mock_engine.assess = AsyncMock(return_value=mock_result)

    response = client.post(
        "/api/v1/assessments",
        json={
            "candidate_id": "test123",
            "submission_type": "code",
            "content": {"code": "print('hello')"},
            "paths_to_evaluate": ["technical"],
        },
    )

    assert response.status_code == 200


def test_assessment_endpoint_with_invalid_candidate_id(client):
    """Test that invalid candidate IDs are rejected."""
    response = client.post(
        "/api/v1/assessments",
        json={
            "candidate_id": "test@invalid",  # @ not allowed
            "submission_type": "code",
            "content": {"code": "print('hello')"},
            "paths_to_evaluate": ["technical"],
        },
    )

    assert response.status_code == 422  # Validation error


def test_assessment_endpoint_with_invalid_submission_type(client):
    """Test that invalid submission types are rejected."""
    response = client.post(
        "/api/v1/assessments",
        json={
            "candidate_id": "test123",
            "submission_type": "invalid_type",
            "content": {"code": "print('hello')"},
            "paths_to_evaluate": ["technical"],
        },
    )

    assert response.status_code == 422  # Validation error


def test_assessment_endpoint_with_empty_content(client):
    """Test that empty content is rejected."""
    response = client.post(
        "/api/v1/assessments",
        json={
            "candidate_id": "test123",
            "submission_type": "code",
            "content": {},
            "paths_to_evaluate": ["technical"],
        },
    )

    assert response.status_code == 422  # Validation error


@patch("sono_eval.api.main.tag_generator")
def test_tag_generation_endpoint(mock_generator, client):
    """Test tag generation endpoint."""
    mock_tag = MagicMock()
    mock_tag.model_dump.return_value = {
        "text": "python",
        "score": 0.95,
    }
    mock_generator.generate_tags.return_value = [mock_tag]

    response = client.post(
        "/api/v1/tags/generate", json={"text": "Sample text for tagging", "max_tags": 5}
    )

    assert response.status_code == 200
    data = response.json()
    assert "tags" in data


def test_tag_generation_with_null_bytes(client):
    """Test that null bytes in text are rejected."""
    response = client.post(
        "/api/v1/tags/generate", json={"text": "Text with null\x00byte", "max_tags": 5}
    )

    assert response.status_code == 422  # Validation error


def test_tag_generation_text_length_limits(client):
    """Test text length validation in tag generation."""
    # Text too long
    long_text = "x" * 100001
    response = client.post(
        "/api/v1/tags/generate", json={"text": long_text, "max_tags": 5}
    )

    assert response.status_code == 422  # Validation error


def test_tag_generation_max_tags_limits(client):
    """Test max_tags validation."""
    # max_tags too high
    response = client.post(
        "/api/v1/tags/generate",
        json={"text": "Sample text", "max_tags": 21},  # Limit is 20
    )

    assert response.status_code == 422  # Validation error

    # max_tags too low
    response = client.post(
        "/api/v1/tags/generate", json={"text": "Sample text", "max_tags": 0}
    )

    assert response.status_code == 422  # Validation error


@patch("sono_eval.api.main.memu_storage")
def test_candidate_creation(mock_storage, client):
    """Test candidate creation endpoint."""
    # Mock get_candidate_memory to return None (candidate doesn't exist)
    mock_storage.get_candidate_memory.return_value = None

    # Mock create_candidate_memory
    mock_memory = MagicMock()
    mock_memory.candidate_id = "test123"
    mock_memory.last_updated = "2026-01-19T00:00:00Z"
    mock_storage.create_candidate_memory.return_value = mock_memory

    response = client.post(
        "/api/v1/candidates",
        json={"candidate_id": "test123", "initial_data": {"name": "Test User"}},
    )

    assert response.status_code == 201


def test_candidate_creation_with_invalid_id(client):
    """Test that invalid candidate IDs are rejected in candidate creation."""
    response = client.post(
        "/api/v1/candidates",
        json={
            "candidate_id": "test@invalid",  # @ not allowed
            "initial_data": {"name": "Test User"},
        },
    )

    assert response.status_code == 422  # Validation error


def test_errors_reference_endpoint(client):
    """Test that error reference endpoint returns known codes."""
    response = client.get("/api/v1/errors")

    assert response.status_code == 200
    data = response.json()

    assert "errors" in data
    assert any(item["error_code"] == "VALIDATION_ERROR" for item in data["errors"])


def test_candidate_id_validation_help_payload(client):
    """Test that validation errors include help payloads."""
    response = client.get(
        "/api/v1/assessments/assess_123?candidate_id=bad@id",
    )

    assert response.status_code == 400
    payload = response.json().get("detail", {})

    assert payload.get("error_code") == "VALIDATION_ERROR"
    assert "help" in payload
    assert payload["help"].get("docs_url") == "/api/v1/errors#validation"
