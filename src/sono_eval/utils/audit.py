"""
Structured Audit Logging for Security and Compliance.

Provides a unified interface for logging security-critical events
in a structured JSON format suitable for SIEM ingestion.
"""

import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional

# Create specific logger for audit events
audit_logger = logging.getLogger("sono_eval.audit")


class AuditLogEncoder(json.JSONEncoder):
    """Custom encoder for audit log data."""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def _emit_log(level: int, event_type: str, message: str, **kwargs):
    """Emit a structured log record."""
    from sono_eval.utils.config import get_config

    config = get_config()
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "message": message,
        "environment": config.app_env,
        **kwargs,
    }

    # Serialize to JSON for structured logging
    try:
        json_entry = json.dumps(entry, cls=AuditLogEncoder)
        audit_logger.log(level, json_entry)
    except (TypeError, ValueError) as e:
        # Fallback if serialization fails
        audit_logger.error(f"Failed to serialize audit log: {e}")
        audit_logger.log(level, str(entry))


def log_security_event(
    event_type: str,
    message: str,
    severity: str = "INFO",
    user_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    resource_id: Optional[str] = None,
    action: Optional[str] = None,
    outcome: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
):
    """
    Log a general security event.

    Args:
        event_type: Category of event (e.g., 'AUTH_LOGIN', 'DATA_ACCESS')
        message: Human readable description
        severity: INFO, WARN, ERROR, CRITICAL
        user_id: ID of user triggering event
        ip_address: Source IP
        resource_id: ID of affected resource
        action: Action performed (read, write, delete)
        outcome: success, failure, denied
        details: Additional context
    """
    level_map = {
        "INFO": logging.INFO,
        "WARN": logging.WARNING,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    level = level_map.get(severity.upper(), logging.INFO)

    payload = {
        "severity": severity.upper(),
        "user_id": user_id,
        "ip_address": ip_address,
        "resource_id": resource_id,
        "action": action,
        "outcome": outcome,
        "details": details or {},
    }
    # Remove None values to keep logs clean
    clean_payload = {k: v for k, v in payload.items() if v is not None}

    _emit_log(level, event_type, message, **clean_payload)


def log_auth_attempt(
    user_id: str,
    success: bool,
    ip_address: str,
    method: str = "password",
    reason: Optional[str] = None,
):
    """Log an authentication attempt."""
    outcome = "success" if success else "failure"
    severity = "INFO" if success else "WARN"
    message = f"Authentication {outcome} for user {user_id}"

    log_security_event(
        event_type="AUTH_LOGIN",
        message=message,
        severity=severity,
        user_id=user_id,
        ip_address=ip_address,
        action="login",
        outcome=outcome,
        details={"method": method, "reason": reason},
    )


def log_access_denied(
    user_id: str,
    resource: str,
    action: str,
    ip_address: Optional[str] = None,
    reason: str = "insufficient_permissions",
):
    """Log an access denied event."""
    log_security_event(
        event_type="ACCESS_DENIED",
        message=f"Access denied to {resource} for user {user_id}",
        severity="WARN",
        user_id=user_id,
        ip_address=ip_address,
        resource_id=resource,
        action=action,
        outcome="denied",
        details={"reason": reason},
    )
