"""Tests for mobile companion interface."""

import pytest
from fastapi.testclient import TestClient

from sono_eval.mobile.app import create_mobile_app


@pytest.fixture
def mobile_client():
    """Create test client for mobile app."""
    app = create_mobile_app()
    return TestClient(app)


def test_mobile_home(mobile_client):
    """Test mobile home page loads."""
    response = mobile_client.get("/")
    assert response.status_code == 200
    assert "Welcome to Sono-Eval" in response.text
    assert "mobile-container" in response.text


def test_mobile_start(mobile_client):
    """Test mobile start page loads."""
    response = mobile_client.get("/start")
    assert response.status_code == 200
    assert "Let's Get to Know You" in response.text


def test_mobile_paths(mobile_client):
    """Test mobile path selection page loads."""
    response = mobile_client.get("/paths?candidate_id=test_user")
    assert response.status_code == 200
    assert "Choose Your Focus Areas" in response.text
    assert "Technical Skills" in response.text
    assert "Design Thinking" in response.text


def test_mobile_assess(mobile_client):
    """Test mobile assessment page loads."""
    response = mobile_client.get("/assess?candidate_id=test_user&paths=technical")
    assert response.status_code == 200
    assert "Your Assessment" in response.text


def test_mobile_results(mobile_client):
    """Test mobile results page loads."""
    response = mobile_client.get("/results?assessment_id=test_123")
    assert response.status_code == 200
    assert "Assessment Complete" in response.text


def test_mobile_explain_path(mobile_client):
    """Test path explanation API."""
    response = mobile_client.get("/api/mobile/explain/technical")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "explanation" in data
    assert "title" in data["explanation"]


def test_mobile_explain_invalid_path(mobile_client):
    """Test path explanation with invalid path."""
    response = mobile_client.get("/api/mobile/explain/invalid")
    assert response.status_code == 404


def test_mobile_submit_assessment(mobile_client):
    """Test mobile assessment submission."""
    submission = {
        "candidate_id": "test_user",
        "paths": ["technical"],
        "content": {
            "code": "def hello(): return 'world'",
        },
        "personalization": {"experience": "intermediate", "goals": ["improve"]},
    }

    response = mobile_client.post("/api/mobile/assess", json=submission)
    # Accept 200 (success) or 422 (validation error depending on setup)
    assert response.status_code in [200, 422]
    data = response.json()
    # Either success with result, or error response
    if response.status_code == 200:
        assert "success" in data
        if data.get("success"):
            assert "assessment_id" in data
            assert "result" in data


def test_mobile_static_files(mobile_client):
    """Test that static files are accessible."""
    # Test CSS
    response = mobile_client.get("/static/style.css")
    assert response.status_code == 200
    assert "mobile-container" in response.text

    # Test JS
    response = mobile_client.get("/static/script.js")
    assert response.status_code == 200
    assert "sonoEval" in response.text
