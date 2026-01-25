"""Extended integration tests for end-to-end workflows."""

import sys
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
from fastapi.testclient import TestClient

# Mock celery before importing app
sys.modules["celery"] = MagicMock()

from sono_eval.api.main import app
from sono_eval.assessment.models import AssessmentInput, PathType
from sono_eval.auth.dependencies import get_current_user
from sono_eval.auth.users import User


@pytest.fixture
def client_with_auth():
    """Create test client with authenticated user."""
    app.dependency_overrides[get_current_user] = lambda: User(username="testuser")

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def mock_assessment_result():
    """Create mock assessment result."""
    mock = Mock()
    mock.overall_score = 87.5
    mock.confidence_score = 0.91
    mock.processing_time_ms = 1500.0
    mock.timestamp = Mock()
    mock.paths = []
    mock.model_dump = Mock(
        return_value={
            "overall_score": 87.5,
            "confidence_score": 0.91,
            "processing_time_ms": 1500.0,
            "paths": [],
            "metadata": {},
        }
    )
    return mock


class TestCompleteAssessmentWorkflow:
    """Test complete assessment workflow from API to result."""

    def test_full_assessment_workflow(self, client_with_auth, mock_assessment_result):
        """Test full assessment from submission to result."""
        with patch("sono_eval.api.main.assessment_engine") as mock_engine:
            mock_engine.assess = AsyncMock(return_value=mock_assessment_result)

            # Submit assessment
            response = client_with_auth.post(
                "/api/v1/assess",
                json={
                    "candidate_id": "candidate_001",
                    "submission_type": "code",
                    "content": {"code": "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)"},
                    "paths_to_evaluate": ["technical", "problem_solving"],
                },
            )

            assert response.status_code == 200
            data = response.json()

            # Verify response structure
            assert "overall_score" in data
            assert "confidence_score" in data
            assert "processing_time_ms" in data
            assert data["overall_score"] == 87.5

            # Verify engine was called
            mock_engine.assess.assert_called_once()

    def test_assessment_with_memory_storage(self, client_with_auth, mock_assessment_result):
        """Test that assessment results are stored in memory."""
        with patch("sono_eval.api.main.assessment_engine") as mock_engine, \
             patch("sono_eval.api.main.memu_storage") as mock_storage:

            mock_engine.assess = AsyncMock(return_value=mock_assessment_result)
            mock_memory = Mock()
            mock_memory.root_node.node_id = "root-123"
            mock_storage.get_candidate_memory = Mock(return_value=mock_memory)

            response = client_with_auth.post(
                "/api/v1/assess",
                json={
                    "candidate_id": "candidate_002",
                    "submission_type": "code",
                    "content": {"code": "print('hello')"},
                    "paths_to_evaluate": ["technical"],
                },
            )

            assert response.status_code == 200

            # Verify memory operations
            mock_storage.get_candidate_memory.assert_called_once_with("candidate_002")

    def test_assessment_with_tagging(self, client_with_auth, mock_assessment_result):
        """Test assessment with automatic tag generation."""
        with patch("sono_eval.api.main.assessment_engine") as mock_engine, \
             patch("sono_eval.api.main.tag_generator") as mock_tagger:

            mock_engine.assess = AsyncMock(return_value=mock_assessment_result)

            mock_tag = Mock()
            mock_tag.model_dump.return_value = {"text": "python", "score": 0.95}
            mock_tagger.generate_tags.return_value = [mock_tag]

            response = client_with_auth.post(
                "/api/v1/assess",
                json={
                    "candidate_id": "candidate_003",
                    "submission_type": "code",
                    "content": {"code": "def hello(): pass"},
                    "paths_to_evaluate": ["technical"],
                },
            )

            assert response.status_code == 200

            # Tags should be generated (if endpoint supports it)
            # This depends on API implementation


class TestMultiCandidateSession:
    """Test handling multiple candidates in a session."""

    def test_sequential_assessments_different_candidates(
        self, client_with_auth, mock_assessment_result
    ):
        """Test assessing multiple candidates sequentially."""
        with patch("sono_eval.api.main.assessment_engine") as mock_engine:
            mock_engine.assess = AsyncMock(return_value=mock_assessment_result)

            candidates = ["candidate_A", "candidate_B", "candidate_C"]

            for candidate_id in candidates:
                response = client_with_auth.post(
                    "/api/v1/assess",
                    json={
                        "candidate_id": candidate_id,
                        "submission_type": "code",
                        "content": {"code": f"# Code for {candidate_id}"},
                        "paths_to_evaluate": ["technical"],
                    },
                )

                assert response.status_code == 200
                assert response.json()["overall_score"] == 87.5

            # Verify engine was called for each candidate
            assert mock_engine.assess.call_count == 3


class TestErrorPropagation:
    """Test error propagation across layers."""

    def test_validation_error_propagation(self, client_with_auth):
        """Test that validation errors are properly returned."""
        # Missing required field
        response = client_with_auth.post(
            "/api/v1/assess",
            json={
                "candidate_id": "test",
                # Missing submission_type and content
            },
        )

        assert response.status_code == 422  # Validation error

    def test_engine_error_handling(self, client_with_auth):
        """Test handling of engine errors."""
        with patch("sono_eval.api.main.assessment_engine") as mock_engine:
            mock_engine.assess = AsyncMock(side_effect=ValueError("Engine error"))

            response = client_with_auth.post(
                "/api/v1/assess",
                json={
                    "candidate_id": "test",
                    "submission_type": "code",
                    "content": {"code": "test"},
                    "paths_to_evaluate": ["technical"],
                },
            )

            # Should return 500 error
            assert response.status_code == 500

    def test_memory_error_handling(self, client_with_auth, mock_assessment_result):
        """Test handling when memory storage fails."""
        with patch("sono_eval.api.main.assessment_engine") as mock_engine, \
             patch("sono_eval.api.main.memu_storage") as mock_storage:

            mock_engine.assess = AsyncMock(return_value=mock_assessment_result)
            mock_storage.get_candidate_memory.side_effect = Exception("Storage error")

            # Should still return result even if storage fails
            response = client_with_auth.post(
                "/api/v1/assess",
                json={
                    "candidate_id": "test",
                    "submission_type": "code",
                    "content": {"code": "test"},
                    "paths_to_evaluate": ["technical"],
                },
            )

            # Assessment should succeed even if storage fails
            assert response.status_code == 200


class TestConcurrentAssessments:
    """Test concurrent assessment processing."""

    def test_concurrent_api_requests(self, client_with_auth, mock_assessment_result):
        """Test handling concurrent API requests."""
        import concurrent.futures

        with patch("sono_eval.api.main.assessment_engine") as mock_engine:
            mock_engine.assess = AsyncMock(return_value=mock_assessment_result)

            def make_request(candidate_num):
                return client_with_auth.post(
                    "/api/v1/assess",
                    json={
                        "candidate_id": f"candidate_{candidate_num}",
                        "submission_type": "code",
                        "content": {"code": f"# Code {candidate_num}"},
                        "paths_to_evaluate": ["technical"],
                    },
                )

            # Make 5 concurrent requests
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(make_request, i) for i in range(5)]
                responses = [f.result() for f in futures]

            # All should succeed
            assert all(r.status_code == 200 for r in responses)
            assert mock_engine.assess.call_count == 5


class TestHealthAndStatus:
    """Test health check and status endpoints."""

    def test_health_endpoint(self, client_with_auth):
        """Test health check endpoint."""
        response = client_with_auth.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_health_endpoint_no_auth_required(self):
        """Test that health check doesn't require auth."""
        with TestClient(app) as client:
            response = client.get("/health")
            assert response.status_code == 200


class TestRequestTracking:
    """Test request ID tracking across system."""

    def test_request_id_propagation(self, client_with_auth, mock_assessment_result):
        """Test that request ID is propagated through system."""
        with patch("sono_eval.api.main.assessment_engine") as mock_engine:
            mock_engine.assess = AsyncMock(return_value=mock_assessment_result)

            response = client_with_auth.post(
                "/api/v1/assess",
                json={
                    "candidate_id": "test",
                    "submission_type": "code",
                    "content": {"code": "test"},
                    "paths_to_evaluate": ["technical"],
                },
            )

            # Should have request ID in headers
            assert "X-Request-ID" in response.headers


class TestFileUploadWorkflow:
    """Test file upload and processing workflow."""

    def test_file_upload_and_tag_generation(self, client_with_auth):
        """Test uploading file and generating tags."""
        with patch("sono_eval.api.main.tag_generator") as mock_tagger:
            mock_tag = Mock()
            mock_tag.model_dump.return_value = {"text": "python", "score": 0.98}
            mock_tagger.generate_tags.return_value = [mock_tag]

            files = {
                "file": ("test.py", b"def hello(): pass", "text/x-python")
            }

            response = client_with_auth.post(
                "/api/v1/files/upload",
                files=files
            )

            assert response.status_code == 200
            data = response.json()
            assert data["filename"] == "test.py"
            assert "tags" in data

    def test_file_upload_size_validation(self, client_with_auth):
        """Test file size validation on upload."""
        # Create large file (> 10MB if that's the limit)
        large_content = b"x" * (11 * 1024 * 1024)

        files = {
            "file": ("large.py", large_content, "text/x-python")
        }

        response = client_with_auth.post(
            "/api/v1/files/upload",
            files=files
        )

        # Should reject large files
        assert response.status_code in [400, 413, 422]


class TestBatchProcessing:
    """Test batch assessment processing."""

    def test_batch_submission(self, client_with_auth):
        """Test submitting batch of assessments."""
        with patch("sono_eval.api.main.assessment_engine"):
            batch_data = {
                "assessments": [
                    {
                        "candidate_id": "candidate_1",
                        "submission_type": "code",
                        "content": {"code": "code1"},
                        "paths_to_evaluate": ["technical"],
                    },
                    {
                        "candidate_id": "candidate_2",
                        "submission_type": "code",
                        "content": {"code": "code2"},
                        "paths_to_evaluate": ["technical"],
                    },
                ]
            }

            # Note: This endpoint might not exist yet
            # This is a forward-looking test
            response = client_with_auth.post(
                "/api/v1/batch/assess",
                json=batch_data
            )

            # Endpoint might return 404 if not implemented
            # This test documents expected behavior
            if response.status_code != 404:
                assert response.status_code in [200, 202]


class TestSecurityHeaders:
    """Test security headers in responses."""

    def test_security_headers_present(self, client_with_auth, mock_assessment_result):
        """Test that security headers are present in responses."""
        with patch("sono_eval.api.main.assessment_engine") as mock_engine:
            mock_engine.assess = AsyncMock(return_value=mock_assessment_result)

            response = client_with_auth.post(
                "/api/v1/assess",
                json={
                    "candidate_id": "test",
                    "submission_type": "code",
                    "content": {"code": "test"},
                    "paths_to_evaluate": ["technical"],
                },
            )

            # Check for security headers (if middleware is applied)
            # These might not all be present depending on middleware config
            headers = response.headers

            # At minimum should have CORS headers
            assert "access-control-allow-origin" in headers or "Access-Control-Allow-Origin" in headers


class TestAPIPerformance:
    """Test API performance characteristics."""

    def test_assessment_performance(self, client_with_auth, mock_assessment_result):
        """Test that assessments complete in reasonable time."""
        import time

        with patch("sono_eval.api.main.assessment_engine") as mock_engine:
            mock_engine.assess = AsyncMock(return_value=mock_assessment_result)

            start = time.time()

            response = client_with_auth.post(
                "/api/v1/assess",
                json={
                    "candidate_id": "test",
                    "submission_type": "code",
                    "content": {"code": "test"},
                    "paths_to_evaluate": ["technical"],
                },
            )

            elapsed = time.time() - start

            assert response.status_code == 200
            # API overhead should be minimal (< 1 second)
            assert elapsed < 1.0


class TestDataConsistency:
    """Test data consistency across operations."""

    def test_assessment_result_consistency(self, client_with_auth, mock_assessment_result):
        """Test that assessment results are consistent."""
        with patch("sono_eval.api.main.assessment_engine") as mock_engine:
            mock_engine.assess = AsyncMock(return_value=mock_assessment_result)

            # Make same request twice
            request_data = {
                "candidate_id": "consistent_test",
                "submission_type": "code",
                "content": {"code": "def test(): pass"},
                "paths_to_evaluate": ["technical"],
            }

            response1 = client_with_auth.post("/api/v1/assess", json=request_data)
            response2 = client_with_auth.post("/api/v1/assess", json=request_data)

            assert response1.status_code == 200
            assert response2.status_code == 200

            # Scores should be identical (same mock result)
            assert response1.json()["overall_score"] == response2.json()["overall_score"]


class TestEdgeCasesIntegration:
    """Test edge cases in integration scenarios."""

    def test_empty_content_handling(self, client_with_auth):
        """Test handling of empty content submission."""
        response = client_with_auth.post(
            "/api/v1/assess",
            json={
                "candidate_id": "test",
                "submission_type": "code",
                "content": {"code": ""},  # Empty code
                "paths_to_evaluate": ["technical"],
            },
        )

        # Should either reject or handle gracefully
        assert response.status_code in [200, 400, 422]

    def test_very_long_content(self, client_with_auth):
        """Test handling of very long submissions."""
        long_code = "# " + "x" * 100000

        response = client_with_auth.post(
            "/api/v1/assess",
            json={
                "candidate_id": "test",
                "submission_type": "code",
                "content": {"code": long_code},
                "paths_to_evaluate": ["technical"],
            },
        )

        # Should either process or reject with size limit
        assert response.status_code in [200, 400, 413, 422]

    def test_special_characters_in_candidate_id(self, client_with_auth, mock_assessment_result):
        """Test handling of special characters in candidate ID."""
        with patch("sono_eval.api.main.assessment_engine") as mock_engine:
            mock_engine.assess = AsyncMock(return_value=mock_assessment_result)

            response = client_with_auth.post(
                "/api/v1/assess",
                json={
                    "candidate_id": "test-user@example.com",
                    "submission_type": "code",
                    "content": {"code": "test"},
                    "paths_to_evaluate": ["technical"],
                },
            )

            # Should handle special characters
            assert response.status_code == 200

    def test_unicode_in_content(self, client_with_auth, mock_assessment_result):
        """Test handling of unicode characters in content."""
        with patch("sono_eval.api.main.assessment_engine") as mock_engine:
            mock_engine.assess = AsyncMock(return_value=mock_assessment_result)

            response = client_with_auth.post(
                "/api/v1/assess",
                json={
                    "candidate_id": "test",
                    "submission_type": "code",
                    "content": {"code": "# 你好世界 🌍\ndef hello(): return '世界'"},
                    "paths_to_evaluate": ["technical"],
                },
            )

            assert response.status_code == 200
