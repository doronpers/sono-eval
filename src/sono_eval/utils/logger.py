"""Logging configuration for Sono-Eval with structured logging support."""

import json
import logging
import sys
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from sono_eval.utils.config import get_config

# Context variables for logging
REQUEST_ID_CTX: ContextVar[Optional[str]] = ContextVar("request_id", default=None)
USER_ID_CTX: ContextVar[Optional[str]] = ContextVar("user_id", default=None)


def set_request_context(
    request_id: Optional[str] = None, user_id: Optional[str] = None
):
    """Set logging context variables."""
    if request_id:
        REQUEST_ID_CTX.set(request_id)
    if user_id:
        USER_ID_CTX.set(user_id)


def clear_request_context():
    """Clear logging context variables."""
    REQUEST_ID_CTX.set(None)
    USER_ID_CTX.set(None)


class StructuredFormatter(logging.Formatter):
    """JSON structured logging formatter."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured JSON."""
        log_data: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Automatically add context from contextvars
        request_id = REQUEST_ID_CTX.get()
        user_id = USER_ID_CTX.get()

        if request_id:
            log_data["request_id"] = request_id
        if user_id:
            log_data["user_id"] = user_id

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Allow record-specific overrides
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms

        return json.dumps(log_data)


def get_logger(
    name: str, level: Optional[str] = None, structured: bool = False
) -> logging.Logger:
    """
    Get a configured logger instance.

    Args:
        name: Logger name (typically __name__)
        level: Optional log level override
        structured: Use structured JSON logging

    Returns:
        Configured logger instance
    """
    config = get_config()
    log_level = level or config.log_level

    # Use structured logging in production by default
    if config.app_env == "production" and not structured:
        structured = True

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))

    # Only add handler if it doesn't already exist
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, log_level.upper()))

        if structured:
            formatter: logging.Formatter = StructuredFormatter()
        else:
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
