"""Tests for audit logging utility."""

import json
import logging
from unittest.mock import patch

import pytest

from sono_eval.utils.audit import log_access_denied, log_auth_attempt, log_security_event


class TestAuditLogger:
    """Test audit logging functionality."""

    @pytest.fixture
    def mock_logger(self):
        """Mock the underlying logger."""
        with patch("sono_eval.utils.audit.audit_logger") as mock:
            yield mock

    def test_log_security_event_structure(self, mock_logger):
        """Test that security events are logged as JSON."""
        log_security_event(
            event_type="TEST_EVENT",
            message="Test message",
            severity="INFO",
            user_id="user_123",
            ip_address="1.2.3.4",
        )

        assert mock_logger.log.called
        # Check args
        args = mock_logger.log.call_args
        level = args[0][0]
        msg = args[0][1]

        assert level == logging.INFO

        # Verify JSON structure
        data = json.loads(msg)
        assert data["event_type"] == "TEST_EVENT"
        assert data["message"] == "Test message"
        assert data["user_id"] == "user_123"
        assert data["ip_address"] == "1.2.3.4"
        assert "timestamp" in data

    def test_log_auth_attempt_success(self, mock_logger):
        """Test logging successful auth attempt."""
        log_auth_attempt(user_id="user_123", success=True, ip_address="1.2.3.4", method="oauth")

        args = mock_logger.log.call_args
        msg = args[0][1]
        data = json.loads(msg)

        assert data["event_type"] == "AUTH_LOGIN"
        assert data["outcome"] == "success"
        assert data["severity"] == "INFO"
        assert data["details"]["method"] == "oauth"

    def test_log_auth_attempt_failure(self, mock_logger):
        """Test logging failed auth attempt."""
        log_auth_attempt(
            user_id="user_123",
            success=False,
            ip_address="1.2.3.4",
            reason="invalid_password",
        )

        args = mock_logger.log.call_args
        msg = args[0][1]
        data = json.loads(msg)

        assert data["event_type"] == "AUTH_LOGIN"
        assert data["outcome"] == "failure"
        assert data["severity"] == "WARN"
        assert data["details"]["reason"] == "invalid_password"

    def test_log_access_denied(self, mock_logger):
        """Test logging access denied event."""
        log_access_denied(
            user_id="user_123",
            resource="admin_panel",
            action="read",
            ip_address="1.2.3.4",
        )

        args = mock_logger.log.call_args
        msg = args[0][1]
        data = json.loads(msg)

        assert data["event_type"] == "ACCESS_DENIED"
        assert data["severity"] == "WARN"
        assert data["resource_id"] == "admin_panel"
        assert data["outcome"] == "denied"
