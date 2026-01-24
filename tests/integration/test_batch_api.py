from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from sono_eval.api.main import app
from sono_eval.auth.users import User

client = TestClient(app)


@pytest.fixture
def mock_celery():
    with patch("sono_eval.core.celery_app.celery_app.Group") as mock_group:
        mock_job = MagicMock()
        mock_job.id = "test-batch-id"
        mock_result = MagicMock()
        mock_result.id = "test-batch-id"
        mock_job.apply_async.return_value = mock_result
        mock_group.return_value = mock_job
        yield mock_group


@pytest.fixture
def mock_user_dependency():
    user = User(
        id="test-user-id",
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        is_active=True,
        is_superuser=False,
    )
    with patch("sono_eval.api.routes.batch.get_current_user", return_value=user):
        yield


def test_submit_batch_assessment(mock_celery, mock_user_dependency):
    payload = {
        "items": [
            {
                "candidate_id": "candidate-1",
                "submission_type": "code",
                "content": {"code": "print('hello')"},
                "paths_to_evaluate": ["technical"],
            },
            {
                "candidate_id": "candidate-2",
                "submission_type": "code",
                "content": {"code": "print('world')"},
                "paths_to_evaluate": ["technical"],
            },
        ]
    }

    response = client.post("/api/v1/assessments/batch/", json=payload)

    assert response.status_code == 202
    data = response.json()
    assert data["batch_id"] == "test-batch-id"
    assert data["total"] == 2
    assert data["status"] == "pending"


@patch("celery.result.GroupResult.restore")
def test_get_batch_status(mock_restore, mock_user_dependency):
    mock_result = MagicMock()
    mock_result.children = [1, 2]  # 2 tasks
    mock_result.completed_count.return_value = 1
    mock_result.ready.return_value = False
    mock_result.results = []

    mock_restore.return_value = mock_result

    response = client.get("/api/v1/assessments/batch/test-batch-id")

    assert response.status_code == 200
    data = response.json()
    assert data["batch_id"] == "test-batch-id"
    assert data["total"] == 2
    assert data["completed"] == 1
    assert data["pending"] == 1
    assert data["status"] == "processing"
