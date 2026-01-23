"""Tests for CLI error recovery and formatting."""

from sono_eval.cli.error_recovery import (
    ErrorSeverity,
    RecoverableError,
    file_not_found_error,
    validation_error,
)


def test_recoverable_error_creation():
    """Test creating a recoverable error."""
    error = RecoverableError(
        error_type="test_error",
        message="Something went wrong",
        recovery_actions=["Try this", "Try that"],
        retry_command="retry --now",
        severity=ErrorSeverity.WARNING,
        context={"foo": "bar"},
    )

    assert error.error_type == "test_error"
    assert len(error.recovery_actions) == 2
    assert error.severity == ErrorSeverity.WARNING
    assert error.exit_code == 2  # System error default


def test_validation_error_helper():
    """Test validation error helper."""
    error = validation_error("field", "Invalid value", "valid_value")

    assert error.error_type == "validation"
    assert error.is_fatal is False
    assert error.exit_code == 1
    assert "Invalid value" in error.message


def test_file_not_found_helper():
    """Test file not found helper."""
    error = file_not_found_error("missing.txt", ["Check path"])

    assert error.error_type == "file_not_found"
    assert "missing.txt" in error.message
    assert error.exit_code == 1


def test_error_severity_levels():
    """Test exit codes for different severities."""
    info = RecoverableError("info", "msg", severity=ErrorSeverity.INFO)
    assert info.exit_code == 0

    user = RecoverableError("validation", "msg", severity=ErrorSeverity.ERROR)
    assert user.exit_code == 1

    system = RecoverableError("internal", "msg", severity=ErrorSeverity.FATAL)
    assert system.exit_code == 2
