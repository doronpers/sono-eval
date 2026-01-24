"""Tests for error handling utilities."""

from fastapi import status

from sono_eval.utils.errors import (
    ErrorCode,
    ErrorHelp,
    ErrorResponse,
    create_error_response,
    file_upload_error,
    internal_error,
    not_found_error,
    service_unavailable_error,
    validation_error,
)


def test_error_code_constants():
    """Test that error code constants are defined correctly."""
    assert ErrorCode.VALIDATION_ERROR == "VALIDATION_ERROR"
    assert ErrorCode.INVALID_INPUT == "INVALID_INPUT"
    assert ErrorCode.UNAUTHORIZED == "UNAUTHORIZED"
    assert ErrorCode.NOT_FOUND == "NOT_FOUND"
    assert ErrorCode.INTERNAL_ERROR == "INTERNAL_ERROR"
    assert ErrorCode.RATE_LIMIT_EXCEEDED == "RATE_LIMIT_EXCEEDED"


def test_error_help_model():
    """Test ErrorHelp model creation."""
    help_obj = ErrorHelp(
        valid_examples=[{"field": "value"}],
        suggestion="Try this instead",
        docs_url="https://docs.example.com",
    )

    assert help_obj.valid_examples == [{"field": "value"}]
    assert help_obj.suggestion == "Try this instead"
    assert help_obj.docs_url == "https://docs.example.com"


def test_error_help_model_optional_fields():
    """Test ErrorHelp model with optional fields."""
    help_obj = ErrorHelp()

    assert help_obj.valid_examples is None
    assert help_obj.suggestion is None
    assert help_obj.docs_url is None


def test_error_response_model():
    """Test ErrorResponse model creation."""
    response = ErrorResponse(
        error_code=ErrorCode.VALIDATION_ERROR,
        message="Invalid input",
        details={"field": "email"},
        request_id="req_123",
    )

    assert response.error is True
    assert response.error_code == ErrorCode.VALIDATION_ERROR
    assert response.message == "Invalid input"
    assert response.details == {"field": "email"}
    assert response.request_id == "req_123"


def test_create_error_response_basic(mock_request_id):
    """Test creating a basic error response."""
    exception = create_error_response(
        error_code=ErrorCode.VALIDATION_ERROR,
        message="Test error message",
        request_id=mock_request_id,
    )

    assert exception.status_code == status.HTTP_400_BAD_REQUEST
    assert exception.detail["error"] is True
    assert exception.detail["error_code"] == ErrorCode.VALIDATION_ERROR
    assert exception.detail["message"] == "Test error message"
    assert exception.detail["request_id"] == mock_request_id


def test_create_error_response_with_details():
    """Test creating error response with details."""
    details = {"field": "email", "reason": "invalid format"}

    exception = create_error_response(
        error_code=ErrorCode.INVALID_INPUT,
        message="Invalid email",
        details=details,
    )

    assert exception.detail["details"] == details


def test_create_error_response_with_help():
    """Test creating error response with help information."""
    help_obj = ErrorHelp(
        suggestion="Check the format",
        docs_url="https://docs.example.com",
    )

    exception = create_error_response(
        error_code=ErrorCode.VALIDATION_ERROR,
        message="Validation failed",
        help=help_obj,
    )

    assert exception.detail["help"]["suggestion"] == "Check the format"
    assert exception.detail["help"]["docs_url"] == "https://docs.example.com"


def test_create_error_response_custom_status_code():
    """Test creating error response with custom status code."""
    exception = create_error_response(
        error_code=ErrorCode.NOT_FOUND,
        message="Resource not found",
        status_code=status.HTTP_404_NOT_FOUND,
    )

    assert exception.status_code == status.HTTP_404_NOT_FOUND


def test_validation_error_basic():
    """Test creating a validation error."""
    exception = validation_error(message="Field is required")

    assert exception.status_code == status.HTTP_400_BAD_REQUEST
    assert exception.detail["error_code"] == ErrorCode.VALIDATION_ERROR
    assert exception.detail["message"] == "Field is required"


def test_validation_error_with_field():
    """Test validation error with field information."""
    exception = validation_error(message="Invalid email", field="email")

    assert exception.detail["details"]["field"] == "email"


def test_validation_error_with_details():
    """Test validation error with custom details."""
    details = {"min_length": 8, "max_length": 100}

    exception = validation_error(
        message="Invalid length",
        field="password",
        details=details,
    )

    assert exception.detail["details"]["field"] == "password"
    assert exception.detail["details"]["min_length"] == 8
    assert exception.detail["details"]["max_length"] == 100


def test_not_found_error_basic():
    """Test creating a not found error."""
    exception = not_found_error(resource_type="User")

    assert exception.status_code == status.HTTP_404_NOT_FOUND
    assert exception.detail["error_code"] == ErrorCode.NOT_FOUND
    assert exception.detail["message"] == "User not found"
    assert exception.detail["details"]["resource_type"] == "User"


def test_not_found_error_with_id():
    """Test not found error with resource ID."""
    exception = not_found_error(resource_type="Candidate", resource_id="cand_123")

    assert exception.detail["message"] == "Candidate not found: cand_123"
    assert exception.detail["details"]["resource_id"] == "cand_123"


def test_internal_error_default():
    """Test creating an internal error with default message."""
    exception = internal_error()

    assert exception.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert exception.detail["error_code"] == ErrorCode.INTERNAL_ERROR
    assert exception.detail["message"] == "An internal error occurred"


def test_internal_error_custom_message():
    """Test internal error with custom message."""
    exception = internal_error(message="Database connection failed")

    assert exception.detail["message"] == "Database connection failed"


def test_internal_error_with_details():
    """Test internal error with details."""
    details = {"database": "postgres", "error": "connection timeout"}

    exception = internal_error(message="Database error", details=details)

    assert exception.detail["details"] == details


def test_service_unavailable_error():
    """Test creating a service unavailable error."""
    exception = service_unavailable_error(service="Assessment Engine")

    assert exception.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert exception.detail["error_code"] == ErrorCode.SERVICE_UNAVAILABLE
    assert exception.detail["message"] == "Assessment Engine is currently unavailable"
    assert exception.detail["details"]["service"] == "Assessment Engine"


def test_file_upload_error_default():
    """Test file upload error with default error type."""
    exception = file_upload_error(message="Invalid file type")

    assert exception.status_code == status.HTTP_400_BAD_REQUEST
    assert exception.detail["error_code"] == ErrorCode.INVALID_FILE_TYPE
    assert exception.detail["message"] == "Invalid file type"


def test_file_upload_error_custom_type():
    """Test file upload error with custom error type."""
    exception = file_upload_error(
        message="File too large",
        error_type=ErrorCode.FILE_TOO_LARGE,
    )

    assert exception.detail["error_code"] == ErrorCode.FILE_TOO_LARGE


def test_file_upload_error_with_details():
    """Test file upload error with details."""
    details = {"max_size_mb": 10, "actual_size_mb": 25}

    exception = file_upload_error(
        message="File exceeds maximum size",
        error_type=ErrorCode.FILE_TOO_LARGE,
        details=details,
    )

    assert exception.detail["details"] == details


def test_error_response_exclude_none():
    """Test that None values are excluded from error response."""
    exception = create_error_response(
        error_code=ErrorCode.VALIDATION_ERROR,
        message="Test error",
    )

    # These fields should not be in the detail dict if None
    assert "details" not in exception.detail
    assert "request_id" not in exception.detail
    assert "help" not in exception.detail


def test_multiple_error_types_have_correct_status_codes():
    """Test that different error types have appropriate status codes."""
    # Validation errors - 400
    val_error = validation_error(message="Invalid")
    assert val_error.status_code == 400

    # Not found - 404
    not_found = not_found_error(resource_type="Resource")
    assert not_found.status_code == 404

    # Internal error - 500
    internal = internal_error()
    assert internal.status_code == 500

    # Service unavailable - 503
    unavailable = service_unavailable_error(service="Test")
    assert unavailable.status_code == 503


def test_error_response_serialization():
    """Test that error responses can be properly serialized."""
    help_obj = ErrorHelp(
        valid_examples=[{"example": "value"}],
        suggestion="Try this",
        docs_url="https://docs.test.com",
    )

    exception = create_error_response(
        error_code=ErrorCode.VALIDATION_ERROR,
        message="Test",
        details={"field": "test"},
        request_id="req_123",
        help=help_obj,
    )

    # Should be able to access all fields
    detail = exception.detail
    assert isinstance(detail, dict)
    assert detail["error"] is True
    assert detail["error_code"] == ErrorCode.VALIDATION_ERROR
    assert detail["message"] == "Test"
    assert detail["details"] == {"field": "test"}
    assert detail["request_id"] == "req_123"
    assert detail["help"]["suggestion"] == "Try this"
