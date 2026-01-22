"""
Error recovery utilities for CLI with actionable suggestions.

Provides structured error types with recovery actions and retry commands
to improve user experience when errors occur.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class ErrorSeverity(Enum):
    """Error severity levels."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    FATAL = "fatal"


@dataclass
class RecoverableError:
    """
    Error with suggested recovery actions.

    Attributes:
        error_type: Type of error (e.g., 'validation', 'file_not_found')
        message: User-friendly error message
        recovery_actions: List of suggested actions to resolve the error
        retry_command: Optional command to retry with corrections
        is_fatal: Whether this error is fatal (cannot be recovered)
        severity: Error severity level
        context: Additional context information
    """

    error_type: str
    message: str
    recovery_actions: List[str] = field(default_factory=list)
    retry_command: Optional[str] = None
    is_fatal: bool = False
    severity: ErrorSeverity = ErrorSeverity.ERROR
    context: dict = field(default_factory=dict)

    @property
    def exit_code(self) -> int:
        """
        Get appropriate exit code for this error.

        Returns:
            0 for success, 1 for user errors, 2 for system errors
        """
        if self.severity == ErrorSeverity.INFO:
            return 0
        elif self.error_type in ["validation", "user_input", "file_not_found"]:
            return 1  # User error
        else:
            return 2  # System error


# Common error templates
def validation_error(field: str, message: str, example: Optional[str] = None) -> RecoverableError:
    """Create a validation error with recovery suggestions."""
    recovery_actions = [
        f"Check that {field} is provided correctly",
        f"Ensure {field} meets the required format",
    ]
    if example:
        recovery_actions.append(f"Example: {example}")

    return RecoverableError(
        error_type="validation",
        message=f"Validation failed for {field}: {message}",
        recovery_actions=recovery_actions,
        is_fatal=False,
        severity=ErrorSeverity.ERROR,
        context={"field": field, "example": example},
    )


def file_not_found_error(
    filepath: str, suggestions: Optional[List[str]] = None
) -> RecoverableError:
    """Create a file not found error with recovery suggestions."""
    recovery_actions = [
        "Check that the file path is correct",
        "Verify the file exists and is accessible",
        "Use an absolute path instead of a relative path",
    ]
    if suggestions:
        recovery_actions.extend(suggestions)

    return RecoverableError(
        error_type="file_not_found",
        message=f"File not found: {filepath}",
        recovery_actions=recovery_actions,
        retry_command=None,  # User needs to fix the path
        is_fatal=False,
        severity=ErrorSeverity.ERROR,
        context={"filepath": filepath},
    )


def connection_error(service: str, retry_command: Optional[str] = None) -> RecoverableError:
    """Create a connection error with retry suggestions."""
    return RecoverableError(
        error_type="connection",
        message=f"Failed to connect to {service}",
        recovery_actions=[
            f"Check that {service} is running",
            "Verify network connectivity",
            "Check firewall settings",
            "Try running the command again",
        ],
        retry_command=retry_command,
        is_fatal=False,
        severity=ErrorSeverity.WARNING,
        context={"service": service},
    )


def permission_error(resource: str) -> RecoverableError:
    """Create a permission error with recovery suggestions."""
    return RecoverableError(
        error_type="permission",
        message=f"Permission denied: {resource}",
        recovery_actions=[
            "Check file/directory permissions",
            "Ensure you have the necessary access rights",
            "Try running with appropriate permissions",
        ],
        is_fatal=True,
        severity=ErrorSeverity.FATAL,
        context={"resource": resource},
    )


def internal_error(error: Exception, context: Optional[str] = None) -> RecoverableError:
    """Create an internal error with debugging suggestions."""
    message = f"Internal error: {str(error)}"
    if context:
        message += f" (Context: {context})"

    return RecoverableError(
        error_type="internal",
        message=message,
        recovery_actions=[
            "This appears to be an internal error",
            "Try running with --debug flag for more information",
            "Report this issue if it persists",
        ],
        is_fatal=True,
        severity=ErrorSeverity.FATAL,
        context={"exception": str(error), "context": context},
    )


def missing_dependency_error(dependency: str, install_command: str) -> RecoverableError:
    """Create a missing dependency error with installation instructions."""
    return RecoverableError(
        error_type="missing_dependency",
        message=f"Required dependency not found: {dependency}",
        recovery_actions=[
            f"Install the missing dependency: {install_command}",
            "Verify your virtual environment is activated",
            "Check that all requirements are installed",
        ],
        retry_command=None,
        is_fatal=False,
        severity=ErrorSeverity.ERROR,
        context={"dependency": dependency, "install_command": install_command},
    )
