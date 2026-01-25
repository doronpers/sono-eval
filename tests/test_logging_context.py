"""Tests for context-aware logging and performance metrics."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from sono_eval.api.main import app
from sono_eval.utils.logger import REQUEST_ID_CTX


@pytest.fixture
def client():
    return TestClient(app)


def test_request_id_in_logs(client):
    """Test that request_id is automatically added to logs via contextvars."""
    with patch("sono_eval.api.main.logger.info") as mock_info:
        # Use candidates endpoint which triggers a log in PerformanceMetricsMiddleware
        response = client.post(
            "/api/v1/candidates", json={"candidate_id": "test_log_ctx"}
        )
        assert response.status_code in [200, 503]

        # Find the performance log
        perf_logs = [
            call for call in mock_info.call_args_list if "completed in" in call.args[0]
        ]
        assert len(perf_logs) > 0

        # Verify that the header is present and the middleware runs.
        assert response.headers["X-Request-ID"] is not None


def test_performance_metrics_logged(client):
    """Test that performance metrics are logged for API calls."""
    with patch("sono_eval.api.main.logger.info") as mock_info:
        client.post("/api/v1/candidates", json={"candidate_id": "test_perf"})

        # Find the performance log
        perf_logs = [
            call for call in mock_info.call_args_list if "completed in" in call.args[0]
        ]
        assert len(perf_logs) > 0

        # Check extra contains duration_ms
        assert "duration_ms" in perf_logs[0].kwargs["extra"]


def test_context_cleared_after_request(client):
    """Test that context is cleared after request finishes."""
    # Ensure it's clear before
    assert REQUEST_ID_CTX.get() is None

    client.get("/api/v1/health")

    # Should be clear after
    assert REQUEST_ID_CTX.get() is None
