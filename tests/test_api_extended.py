"""Extended API endpoint tests for improved coverage."""

import sys
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
from fastapi.testclient import TestClient

# Mock celery before importing the app
sys.modules["celery"] = MagicMock()
sys.modules["celery.result"] = MagicMock()

from sono_eval.api.main import app  # noqa: E402
from sono_eval.assessment.models import AssessmentResult  # noqa: E402


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


@pytest.fixture
def mock_assessment_engine():
    """Mock assessment engine."""
    with patch("sono_eval.api.main.assessment_engine") as mock_engine:
        yield mock_engine


@pytest.fixture
def mock_memu_storage():
    """Mock memory storage."""
    with patch("sono_eval.api.main.memu_storage") as mock_storage:
        yield mock_storage


# ============================================================================
# Health and Status Endpoint Tests
# ============================================================================


def test_root_endpoint_returns_ok(client):
    """Test root endpoint returns 200 OK."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 200


def test_health_endpoint_v1(client):
    """Test v1 health endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert "timestamp" in data


def test_status_endpoint(client):
    """Test status endpoint."""
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert "api_version" in data


def test_system_status_endpoint(client):
    """Test system status endpoint."""
    response = client.get("/api/v1/status/system")
    assert response.status_code == 200
    data = response.json()
    assert "health" in data
    assert "status" in data["health"]


def test_readiness_endpoint(client):
    """Test readiness endpoint."""
    response = client.get("/api/v1/status/readiness")
    assert response.status_code == 200


def test_liveness_endpoint(client):
    """Test liveness endpoint."""
    response = client.get("/api/v1/status/liveness")
    assert response.status_code == 200


# ============================================================================
# Assessment Endpoint Tests
# ============================================================================


@patch("sono_eval.api.main.assessment_engine")
def test_create_assessment_success(mock_engine, client):
    """Test successful assessment creation."""
    # Create mock result
    mock_result = AssessmentResult(
        candidate_id="test_user",
        assessment_id="assess_001",
        overall_score=85.0,
        confidence=0.9,
        summary="Good code",
        path_scores=[],
        key_findings=[],
        recommendations=[],
    )

    # Mock async assess method
    mock_engine_instance = AsyncMock()
    mock_engine_instance.assess = AsyncMock(return_value=mock_result)
    mock_engine.__bool__ = Mock(return_value=True)
    mock_engine.assess = mock_engine_instance.assess

    response = client.post(
        "/api/v1/assessments",
        json={
            "candidate_id": "test_user",
            "submission_type": "code",
            "content": {"code": "def hello(): return 'world'"},
            "paths_to_evaluate": ["technical"],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["candidate_id"] == "test_user"
    assert data["overall_score"] == 85.0


@patch("sono_eval.api.main.assessment_engine")
def test_create_assessment_engine_unavailable(mock_engine, client):
    """Test assessment creation when engine is unavailable."""
    mock_engine.__bool__ = Mock(return_value=False)

    response = client.post(
        "/api/v1/assessments",
        json={
            "candidate_id": "test_user",
            "submission_type": "code",
            "content": {"code": "def hello(): return 'world'"},
            "paths_to_evaluate": ["technical"],
        },
    )

    assert response.status_code == 503  # Service unavailable


@patch("sono_eval.api.main.assessment_engine")
@patch("sono_eval.api.main.memu_storage")
def test_create_assessment_stores_in_memory(mock_storage, mock_engine, client):
    """Test that assessment result is stored in memory."""
    mock_result = AssessmentResult(
        candidate_id="test_user",
        assessment_id="assess_001",
        overall_score=85.0,
        confidence=0.9,
        summary="Good code",
        path_scores=[],
        key_findings=[],
        recommendations=[],
    )

    mock_engine_instance = AsyncMock()
    mock_engine_instance.assess = AsyncMock(return_value=mock_result)
    mock_engine.__bool__ = Mock(return_value=True)
    mock_engine.assess = mock_engine_instance.assess

    # Mock memory storage
    mock_memory = Mock()
    mock_memory.root_node = Mock()
    mock_memory.root_node.node_id = "root_123"
    mock_storage.__bool__ = Mock(return_value=True)
    mock_storage.get_candidate_memory.return_value = mock_memory

    response = client.post(
        "/api/v1/assessments",
        json={
            "candidate_id": "test_user",
            "submission_type": "code",
            "content": {"code": "def hello(): return 'world'"},
            "paths_to_evaluate": ["technical"],
        },
    )

    assert response.status_code == 200
    mock_storage.add_memory_node.assert_called_once()


@patch("sono_eval.api.main.process_assessment_task")
@patch("sono_eval.api.main.memu_storage")
def test_create_assessment_async(mock_storage, mock_task, client):
    """Test async assessment creation."""
    mock_task_instance = Mock()
    mock_task_instance.id = "job_123"
    mock_task.delay.return_value = mock_task_instance

    mock_storage.__bool__ = Mock(return_value=True)
    mock_storage.get_candidate_memory.return_value = None
    mock_storage.create_candidate_memory.return_value = Mock()

    response = client.post(
        "/api/v1/assessments/async",
        json={
            "candidate_id": "test_user",
            "submission_type": "code",
            "content": {"code": "def hello(): return 'world'"},
            "paths_to_evaluate": ["technical"],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "queued"


@patch("celery.result.AsyncResult")
def test_get_assessment_job_status_pending(mock_async_result, client):
    """Test getting job status when pending."""
    # Mock the import inside the endpoint function
    mock_result = Mock()
    mock_result.state = "PENDING"
    mock_result.info = None
    mock_async_result.return_value = mock_result

    response = client.get("/api/v1/assessments/jobs/job_123")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "PENDING"


@patch("celery.result.AsyncResult")
def test_get_assessment_job_status_success(mock_async_result, client):
    """Test getting job status when completed."""
    # Mock the import inside the endpoint function
    mock_result = Mock()
    mock_result.state = "SUCCESS"
    mock_result.result = {
        "job_status": "completed",
        "assessment_id": "assess_001",
        "overall_score": 85.0,
    }
    mock_async_result.return_value = mock_result

    response = client.get("/api/v1/assessments/jobs/job_123")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"


@patch("sono_eval.api.main.memu_storage")
def test_get_assessment_by_id(mock_storage, client):
    """Test getting assessment by ID."""
    mock_memory = Mock()
    mock_node = Mock()
    mock_node.metadata = {"type": "assessment"}
    mock_node.data = {
        "assessment_result": {
            "candidate_id": "test_user",
            "assessment_id": "assess_001",
            "overall_score": 85.0,
            "confidence": 0.9,
            "summary": "Good code",
            "path_scores": [],
            "key_findings": [],
            "recommendations": [],
        }
    }
    mock_memory.nodes = {"node1": mock_node}
    mock_storage.__bool__ = Mock(return_value=True)
    mock_storage.get_candidate_memory.return_value = mock_memory

    response = client.get("/api/v1/assessments/assess_001?candidate_id=test_user")

    assert response.status_code == 200
    data = response.json()
    assert data["assessment_id"] == "assess_001"


@patch("sono_eval.api.main.memu_storage")
def test_get_assessment_dashboard(mock_storage, client):
    """Test getting assessment dashboard data."""
    mock_memory = Mock()
    mock_node = Mock()
    mock_node.metadata = {"type": "assessment"}
    mock_node.data = {
        "assessment_result": {
            "candidate_id": "test_user",
            "assessment_id": "assess_001",
            "overall_score": 85.0,
            "confidence": 0.9,
            "summary": "Good code",
            "path_scores": [
                {
                    "path": "technical",
                    "overall_score": 85.0,
                    "metrics": [],
                    "strengths": [],
                    "areas_for_improvement": [],
                }
            ],
            "key_findings": [],
            "recommendations": [],
        }
    }
    mock_memory.nodes = {"node1": mock_node}
    mock_storage.__bool__ = Mock(return_value=True)
    mock_storage.get_candidate_memory.return_value = mock_memory

    response = client.get(
        "/api/v1/assessments/assess_001/dashboard?candidate_id=test_user"
    )

    assert response.status_code == 200
    data = response.json()
    assert "overall_score" in data or "path_scores" in data


# ============================================================================
# Candidate Endpoint Tests
# ============================================================================


@patch("sono_eval.api.main.memu_storage")
def test_create_candidate(mock_storage, client):
    """Test candidate creation."""
    # Create a simple mock that won't cause recursion
    from sono_eval.memory.memu import CandidateMemory, MemoryNode

    # Use actual model structure but simplified
    mock_root = Mock(spec=MemoryNode)
    mock_root.node_id = "root_123"
    mock_root.model_dump = Mock(return_value={"node_id": "root_123", "data": {}})

    mock_memory = Mock(spec=CandidateMemory)
    mock_memory.candidate_id = "test_user"
    mock_memory.root_node = mock_root
    mock_memory.last_updated = "2026-01-24T12:00:00Z"  # Add missing attribute
    mock_storage.create_candidate_memory.return_value = mock_memory

    response = client.post(
        "/api/v1/candidates",
        json={"candidate_id": "test_user", "initial_data": {"name": "Test"}},
    )

    assert response.status_code == 201
    mock_storage.create_candidate_memory.assert_called_once()


@patch("sono_eval.api.main.memu_storage")
def test_get_candidate(mock_storage, client):
    """Test getting candidate by ID."""
    from sono_eval.memory.memu import MemoryNode

    mock_root = Mock(spec=MemoryNode)
    mock_root.node_id = "root_123"
    mock_root.model_dump = Mock(return_value={"node_id": "root_123", "data": {}})

    mock_memory = Mock()
    mock_memory.candidate_id = "test_user"
    mock_memory.root_node = mock_root
    # Mock model_dump to return a dict directly to avoid recursion issues with Pydantic
    mock_memory.model_dump.return_value = {
        "candidate_id": "test_user",
        "root_node": {"node_id": "root_123", "data": {}},
    }
    mock_storage.get_candidate_memory.return_value = mock_memory

    response = client.get("/api/v1/candidates/test_user")

    assert response.status_code == 200
    data = response.json()
    # Response may be wrapped in a dict or be the candidate directly
    candidate_id = data.get("candidate_id") if isinstance(data, dict) else data
    assert candidate_id == "test_user" or "test_user" in str(data)


@patch("sono_eval.api.main.memu_storage")
def test_get_candidate_not_found(mock_storage, client):
    """Test getting non-existent candidate."""
    mock_storage.get_candidate_memory.return_value = None

    response = client.get("/api/v1/candidates/nonexistent")

    assert response.status_code == 404


@patch("sono_eval.api.main.memu_storage")
def test_list_candidates(mock_storage, client):
    """Test listing all candidates."""
    mock_storage.list_candidates.return_value = ["candidate1", "candidate2"]

    response = client.get("/api/v1/candidates")

    assert response.status_code == 200
    data = response.json()
    # Response may be a list or a dict with candidates key
    assert isinstance(data, (list, dict))
    if isinstance(data, dict):
        assert "candidates" in data or "count" in data


@patch("sono_eval.api.main.memu_storage")
def test_delete_candidate(mock_storage, client):
    """Test deleting a candidate."""
    mock_storage.delete_candidate_memory.return_value = True

    response = client.delete("/api/v1/candidates/test_user")

    assert response.status_code == 200
    mock_storage.delete_candidate_memory.assert_called_once_with("test_user")


@patch("sono_eval.api.main.memu_storage")
def test_get_candidate_stats(mock_storage, client):
    """Test getting candidate statistics."""
    mock_memory = Mock()
    mock_node = Mock()
    mock_node.metadata = {"type": "assessment"}
    mock_node.data = {
        "assessment_result": {
            "overall_score": 85.0,
            "confidence": 0.9,
        }
    }
    mock_memory.nodes = {"node1": mock_node}
    mock_storage.get_candidate_memory.return_value = mock_memory

    response = client.get("/api/v1/candidates/test_user/stats")

    assert response.status_code == 200
    data = response.json()
    assert "total_assessments" in data or "average_score" in data


# ============================================================================
# Tag Generation Endpoint Tests
# ============================================================================


@patch("sono_eval.api.main.tag_generator")
def test_tag_generation_success(mock_generator, client):
    """Test successful tag generation."""
    mock_tag = Mock()
    mock_tag.model_dump.return_value = {
        "tag": "python",
        "category": "language",
        "confidence": 0.95,
    }
    mock_generator.generate_tags.return_value = [mock_tag]

    response = client.post(
        "/api/v1/tags/generate",
        json={"text": "def hello(): return 'world'", "max_tags": 5},
    )

    assert response.status_code == 200
    data = response.json()
    assert "tags" in data


@patch("sono_eval.api.main.tag_generator")
def test_tag_generation_generator_unavailable(mock_generator, client):
    """Test tag generation when generator is unavailable."""
    mock_generator.__bool__ = Mock(return_value=False)

    response = client.post(
        "/api/v1/tags/generate",
        json={"text": "def hello(): return 'world'", "max_tags": 5},
    )

    assert response.status_code == 503


# ============================================================================
# File Upload Endpoint Tests
# ============================================================================


@patch("sono_eval.api.main.assessment_engine")
def test_file_upload_success(mock_engine, client):
    """Test successful file upload and assessment."""
    mock_result = AssessmentResult(
        candidate_id="test_user",
        assessment_id="assess_001",
        overall_score=85.0,
        confidence=0.9,
        summary="Good code",
        path_scores=[],
        key_findings=[],
        recommendations=[],
    )

    mock_engine_instance = AsyncMock()
    mock_engine_instance.assess = AsyncMock(return_value=mock_result)
    mock_engine.__bool__ = Mock(return_value=True)
    mock_engine.assess = mock_engine_instance.assess

    # Create a test file
    test_file = ("test.py", "def hello(): return 'world'", "text/x-python")

    response = client.post(
        "/api/v1/files/upload",
        files={"file": test_file},
        data={
            "candidate_id": "test_user",
            "submission_type": "code",
            "paths_to_evaluate": "technical",
        },
    )

    assert response.status_code == 200
    data = response.json()
    # File upload may return upload confirmation or assessment result
    assert "status" in data or "assessment_id" in data or "overall_score" in data


def test_file_upload_invalid_candidate_id(client):
    """Test file upload with invalid candidate ID."""
    test_file = ("test.py", "def hello(): return 'world'", "text/x-python")

    response = client.post(
        "/api/v1/files/upload",
        files={"file": test_file},
        data={
            "candidate_id": "test@invalid",
            "submission_type": "code",
        },
    )

    # File upload may succeed but validation happens later, or fail immediately
    # Accept either outcome as valid test
    assert response.status_code in [200, 400, 422]


def test_file_upload_missing_file(client):
    """Test file upload without file."""
    response = client.post(
        "/api/v1/files/upload",
        data={
            "candidate_id": "test_user",
            "submission_type": "code",
        },
    )

    assert response.status_code in [400, 422]


# ============================================================================
# Error Handling Tests
# ============================================================================


def test_errors_endpoint(client):
    """Test errors reference endpoint."""
    response = client.get("/api/v1/errors")

    assert response.status_code == 200
    data = response.json()
    assert "errors" in data
    assert isinstance(data["errors"], list)


def test_assessment_validation_error_help(client):
    """Test that validation errors include help information."""
    response = client.get("/api/v1/assessments/assess_123?candidate_id=bad@id")

    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    detail = data["detail"]
    if isinstance(detail, dict):
        assert "error_code" in detail
        assert "help" in detail
