"""Tests for structured logging functionality."""

import json
import logging
import pytest
from unittest.mock import patch, MagicMock
from sono_eval.utils.logger import get_logger, StructuredFormatter


def test_get_logger_returns_logger():
    """Test that get_logger returns a logger instance."""
    logger = get_logger("test_logger")
    
    assert logger is not None
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_logger"


def test_get_logger_with_custom_level():
    """Test logger with custom log level."""
    logger = get_logger("test_logger", level="DEBUG")
    
    assert logger.level == logging.DEBUG


def test_structured_formatter_formats_as_json():
    """Test that StructuredFormatter produces valid JSON."""
    formatter = StructuredFormatter()
    
    # Create a log record
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test.py",
        lineno=42,
        msg="Test message",
        args=(),
        exc_info=None,
    )
    record.funcName = "test_function"
    record.module = "test_module"
    
    # Format the record
    formatted = formatter.format(record)
    
    # Should be valid JSON
    log_data = json.loads(formatted)
    
    assert log_data["message"] == "Test message"
    assert log_data["level"] == "INFO"
    assert log_data["logger"] == "test_logger"
    assert log_data["module"] == "test_module"
    assert log_data["function"] == "test_function"
    assert log_data["line"] == 42
    assert "timestamp" in log_data


def test_structured_formatter_includes_request_id():
    """Test that request_id is included when present."""
    formatter = StructuredFormatter()
    
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test.py",
        lineno=42,
        msg="Test message",
        args=(),
        exc_info=None,
    )
    record.funcName = "test_function"
    record.module = "test_module"
    record.request_id = "test-request-id-123"
    
    formatted = formatter.format(record)
    log_data = json.loads(formatted)
    
    assert log_data["request_id"] == "test-request-id-123"


def test_structured_formatter_includes_duration():
    """Test that duration_ms is included when present."""
    formatter = StructuredFormatter()
    
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test.py",
        lineno=42,
        msg="Test message",
        args=(),
        exc_info=None,
    )
    record.funcName = "test_function"
    record.module = "test_module"
    record.duration_ms = 123.45
    
    formatted = formatter.format(record)
    log_data = json.loads(formatted)
    
    assert log_data["duration_ms"] == 123.45


def test_structured_formatter_includes_user_id():
    """Test that user_id is included when present."""
    formatter = StructuredFormatter()
    
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test.py",
        lineno=42,
        msg="Test message",
        args=(),
        exc_info=None,
    )
    record.funcName = "test_function"
    record.module = "test_module"
    record.user_id = "user-123"
    
    formatted = formatter.format(record)
    log_data = json.loads(formatted)
    
    assert log_data["user_id"] == "user-123"


def test_structured_formatter_includes_exception():
    """Test that exceptions are formatted properly."""
    formatter = StructuredFormatter()
    
    try:
        raise ValueError("Test exception")
    except ValueError:
        import sys
        exc_info = sys.exc_info()
    
    record = logging.LogRecord(
        name="test_logger",
        level=logging.ERROR,
        pathname="test.py",
        lineno=42,
        msg="Error occurred",
        args=(),
        exc_info=exc_info,
    )
    record.funcName = "test_function"
    record.module = "test_module"
    
    formatted = formatter.format(record)
    log_data = json.loads(formatted)
    
    assert "exception" in log_data
    assert "ValueError" in log_data["exception"]
    assert "Test exception" in log_data["exception"]


def test_logger_uses_structured_format_in_production():
    """Test that structured logging is used in production."""
    with patch("sono_eval.utils.logger.get_config") as mock_get_config:
        mock_config = MagicMock()
        mock_config.app_env = "production"
        mock_config.log_level = "INFO"
        mock_get_config.return_value = mock_config
        
        logger = get_logger("test_logger_prod")
        
        # Check that the handler has StructuredFormatter
        if logger.handlers:
            handler = logger.handlers[0]
            assert isinstance(handler.formatter, StructuredFormatter)


def test_logger_uses_plain_format_in_development():
    """Test that plain logging is used in development by default."""
    with patch("sono_eval.utils.logger.get_config") as mock_get_config:
        mock_config = MagicMock()
        mock_config.app_env = "development"
        mock_config.log_level = "INFO"
        mock_get_config.return_value = mock_config
        
        logger = get_logger("test_logger_dev")
        
        # Check that the handler does not have StructuredFormatter
        if logger.handlers:
            handler = logger.handlers[0]
            assert not isinstance(handler.formatter, StructuredFormatter)


def test_logger_respects_structured_parameter():
    """Test that structured parameter overrides default behavior."""
    with patch("sono_eval.utils.logger.get_config") as mock_get_config:
        mock_config = MagicMock()
        mock_config.app_env = "development"
        mock_config.log_level = "INFO"
        mock_get_config.return_value = mock_config
        
        # Force structured logging in development
        logger = get_logger("test_logger_structured", structured=True)
        
        if logger.handlers:
            handler = logger.handlers[0]
            assert isinstance(handler.formatter, StructuredFormatter)


def test_timestamp_format_is_iso8601():
    """Test that timestamps are in ISO 8601 format."""
    formatter = StructuredFormatter()
    
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test.py",
        lineno=42,
        msg="Test message",
        args=(),
        exc_info=None,
    )
    record.funcName = "test_function"
    record.module = "test_module"
    
    formatted = formatter.format(record)
    log_data = json.loads(formatted)
    
    # Timestamp should end with 'Z' (UTC indicator)
    assert log_data["timestamp"].endswith("Z")
    # Should contain 'T' separator
    assert "T" in log_data["timestamp"]
