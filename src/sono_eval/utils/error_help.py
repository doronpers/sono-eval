"""Helpers for creating actionable API error guidance."""

from typing import Any, Dict, Optional

from sono_eval.utils.errors import ErrorHelp


def validation_help(
    field: str,
    example: Dict[str, Any],
    docs_url: str,
    suggestion: Optional[str] = None,
) -> ErrorHelp:
    """Create help payload for validation errors."""
    return ErrorHelp(
        valid_examples=[example],
        suggestion=suggestion or f"Ensure '{field}' matches the documented format.",
        docs_url=docs_url,
    )


def not_found_help(
    resource: str,
    example: Dict[str, Any],
    docs_url: str,
    suggestion: Optional[str] = None,
) -> ErrorHelp:
    """Create help payload for not found errors."""
    return ErrorHelp(
        valid_examples=[example],
        suggestion=suggestion or f"Confirm the {resource} exists or create it before retrying.",
        docs_url=docs_url,
    )


def file_upload_help(
    max_size_mb: float,
    extensions: list[str],
    docs_url: str,
) -> ErrorHelp:
    """Create help payload for file upload errors."""
    return ErrorHelp(
        valid_examples=[{"max_size_mb": max_size_mb, "extensions": extensions}],
        suggestion="Validate file type/size and retry the upload.",
        docs_url=docs_url,
    )


def service_help(service: str, docs_url: str, hint: Optional[str] = None) -> ErrorHelp:
    """Create help payload for service unavailable errors."""
    return ErrorHelp(
        valid_examples=[{"service": service}],
        suggestion=hint or f"Verify {service} is healthy and retry.",
        docs_url=docs_url,
    )
