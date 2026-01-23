"""
Enhanced Error Recovery for Sono-Eval

Integrates shared-ai-utils error recovery framework with sono-eval's existing
error handling system.
"""

from typing import Any, Dict, Optional

from sono_eval.utils.errors import ErrorHelp


def enhance_error_with_recovery(
    error_type: str,
    message: str,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Enhance error response with recovery steps.

    Args:
        error_type: Type of error (exception class name or error code)
        message: Error message
        context: Additional context

    Returns:
        Dictionary with enhanced error information including recovery steps
    """
    context = context or {}

    # Try to use shared-ai-utils error recovery if available
    try:
        from shared_ai_utils.errors import ErrorRecovery

        recovery = ErrorRecovery(error_type, context)
        recovery_steps = recovery.get_steps()

        # Convert recovery steps to ErrorHelp format
        suggestions = [step.description for step in recovery_steps]
        suggestion_text = " | ".join(suggestions[:3])  # First 3 steps

        # Get doc links from recovery steps
        doc_links = [step.doc_link for step in recovery_steps if step.doc_link]
        docs_url = doc_links[0] if doc_links else None

        return {
            "recovery_steps": [step.to_dict() for step in recovery_steps],
            "suggestion": suggestion_text,
            "docs_url": docs_url,
        }
    except ImportError:
        # Fallback: basic recovery suggestions
        return {
            "recovery_steps": [
                {
                    "description": "Review the error message for details",
                    "doc_link": "/api/v1/errors",
                }
            ],
            "suggestion": "See /api/v1/errors for error reference",
            "docs_url": "/api/v1/errors",
        }


def create_enhanced_error_help(
    error_type: str,
    context: Optional[Dict[str, Any]] = None,
) -> ErrorHelp:
    """Create enhanced ErrorHelp with recovery information.

    Args:
        error_type: Type of error
        context: Additional context

    Returns:
        ErrorHelp with recovery steps
    """
    recovery_info = enhance_error_with_recovery(error_type, "", context)

    return ErrorHelp(
        suggestion=recovery_info.get("suggestion"),
        docs_url=recovery_info.get("docs_url"),
        valid_examples=None,  # Can be populated from recovery steps if needed
    )
