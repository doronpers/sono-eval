"""Tests for error help utilities."""

from sono_eval.utils.error_help import (
    file_upload_help,
    not_found_help,
    service_help,
    validation_help,
)
from sono_eval.utils.errors import ErrorHelp


def test_validation_help_basic():
    """Test creating validation help."""
    help_obj = validation_help(
        field="email",
        example={"email": "user@example.com"},
        docs_url="https://docs.test.com/validation",
    )

    assert isinstance(help_obj, ErrorHelp)
    assert help_obj.valid_examples == [{"email": "user@example.com"}]
    assert "email" in help_obj.suggestion
    assert help_obj.docs_url == "https://docs.test.com/validation"


def test_validation_help_with_custom_suggestion():
    """Test validation help with custom suggestion."""
    help_obj = validation_help(
        field="password",
        example={"password": "secure123"},
        docs_url="https://docs.test.com",
        suggestion="Password must be at least 8 characters",
    )

    assert help_obj.suggestion == "Password must be at least 8 characters"


def test_validation_help_default_suggestion():
    """Test that validation help has a default suggestion."""
    help_obj = validation_help(
        field="username",
        example={"username": "john_doe"},
        docs_url="https://docs.test.com",
    )

    assert help_obj.suggestion is not None
    assert "username" in help_obj.suggestion
    assert "format" in help_obj.suggestion.lower()


def test_not_found_help_basic():
    """Test creating not found help."""
    help_obj = not_found_help(
        resource="candidate",
        example={"candidate_id": "cand_123"},
        docs_url="https://docs.test.com/candidates",
    )

    assert isinstance(help_obj, ErrorHelp)
    assert help_obj.valid_examples == [{"candidate_id": "cand_123"}]
    assert "candidate" in help_obj.suggestion
    assert help_obj.docs_url == "https://docs.test.com/candidates"


def test_not_found_help_with_custom_suggestion():
    """Test not found help with custom suggestion."""
    help_obj = not_found_help(
        resource="session",
        example={"session_id": "sess_456"},
        docs_url="https://docs.test.com",
        suggestion="Create a new session with: sono-eval session create",
    )

    assert help_obj.suggestion == "Create a new session with: sono-eval session create"


def test_not_found_help_default_suggestion():
    """Test that not found help has a default suggestion."""
    help_obj = not_found_help(
        resource="assessment",
        example={"assessment_id": "assess_789"},
        docs_url="https://docs.test.com",
    )

    assert help_obj.suggestion is not None
    assert "assessment" in help_obj.suggestion
    assert (
        "exists" in help_obj.suggestion.lower()
        or "create" in help_obj.suggestion.lower()
    )


def test_file_upload_help():
    """Test creating file upload help."""
    help_obj = file_upload_help(
        max_size_mb=10.0,
        extensions=["py", "js", "ts"],
        docs_url="https://docs.test.com/uploads",
    )

    assert isinstance(help_obj, ErrorHelp)
    assert len(help_obj.valid_examples) == 1
    assert help_obj.valid_examples[0]["max_size_mb"] == 10.0
    assert help_obj.valid_examples[0]["extensions"] == ["py", "js", "ts"]
    assert help_obj.docs_url == "https://docs.test.com/uploads"


def test_file_upload_help_suggestion():
    """Test file upload help has proper suggestion."""
    help_obj = file_upload_help(
        max_size_mb=5.0,
        extensions=["txt", "md"],
        docs_url="https://docs.test.com",
    )

    assert help_obj.suggestion is not None
    assert "file" in help_obj.suggestion.lower()
    assert "upload" in help_obj.suggestion.lower()


def test_file_upload_help_various_sizes():
    """Test file upload help with various size limits."""
    help_small = file_upload_help(
        max_size_mb=1.0,
        extensions=["txt"],
        docs_url="https://docs.test.com",
    )
    help_large = file_upload_help(
        max_size_mb=100.0,
        extensions=["zip"],
        docs_url="https://docs.test.com",
    )

    assert help_small.valid_examples[0]["max_size_mb"] == 1.0
    assert help_large.valid_examples[0]["max_size_mb"] == 100.0


def test_service_help_basic():
    """Test creating service help."""
    help_obj = service_help(
        service="Assessment Engine",
        docs_url="https://docs.test.com/services",
    )

    assert isinstance(help_obj, ErrorHelp)
    assert help_obj.valid_examples == [{"service": "Assessment Engine"}]
    assert "Assessment Engine" in help_obj.suggestion
    assert help_obj.docs_url == "https://docs.test.com/services"


def test_service_help_with_custom_hint():
    """Test service help with custom hint."""
    help_obj = service_help(
        service="Database",
        docs_url="https://docs.test.com",
        hint="Check database connection settings in config.yaml",
    )

    assert help_obj.suggestion == "Check database connection settings in config.yaml"


def test_service_help_default_hint():
    """Test that service help has a default hint."""
    help_obj = service_help(
        service="Redis Cache",
        docs_url="https://docs.test.com",
    )

    assert help_obj.suggestion is not None
    assert "Redis Cache" in help_obj.suggestion
    assert (
        "healthy" in help_obj.suggestion.lower()
        or "retry" in help_obj.suggestion.lower()
    )


def test_all_help_functions_return_error_help():
    """Test that all help functions return ErrorHelp instances."""
    validation = validation_help("field", {"key": "value"}, "http://test.com")
    not_found = not_found_help("resource", {"id": "123"}, "http://test.com")
    file_upload = file_upload_help(10.0, ["py"], "http://test.com")
    service = service_help("service", "http://test.com")

    assert isinstance(validation, ErrorHelp)
    assert isinstance(not_found, ErrorHelp)
    assert isinstance(file_upload, ErrorHelp)
    assert isinstance(service, ErrorHelp)


def test_help_objects_have_docs_urls():
    """Test that all help objects include documentation URLs."""
    validation = validation_help("field", {}, "http://validation.com")
    not_found = not_found_help("resource", {}, "http://notfound.com")
    file_upload = file_upload_help(5.0, [], "http://upload.com")
    service = service_help("svc", "http://service.com")

    assert validation.docs_url == "http://validation.com"
    assert not_found.docs_url == "http://notfound.com"
    assert file_upload.docs_url == "http://upload.com"
    assert service.docs_url == "http://service.com"


def test_help_objects_have_examples():
    """Test that all help objects include valid examples."""
    validation = validation_help("email", {"email": "test@test.com"}, "http://test.com")
    not_found = not_found_help("user", {"user_id": "123"}, "http://test.com")
    file_upload = file_upload_help(10.0, ["py", "js"], "http://test.com")
    service = service_help("api", "http://test.com")

    assert len(validation.valid_examples) > 0
    assert len(not_found.valid_examples) > 0
    assert len(file_upload.valid_examples) > 0
    assert len(service.valid_examples) > 0


def test_multiple_file_extensions():
    """Test file upload help with multiple extensions."""
    help_obj = file_upload_help(
        max_size_mb=25.0,
        extensions=["py", "js", "ts", "jsx", "tsx"],
        docs_url="https://docs.test.com",
    )

    extensions = help_obj.valid_examples[0]["extensions"]
    assert len(extensions) == 5
    assert "py" in extensions
    assert "tsx" in extensions
