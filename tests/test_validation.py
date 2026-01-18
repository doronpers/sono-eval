"""Tests for input validation in assessment models."""

import pytest
from pydantic import ValidationError

from sono_eval.assessment.models import AssessmentInput, PathType


def test_valid_candidate_id():
    """Test that valid candidate IDs are accepted."""
    valid_ids = [
        "test123",
        "test_candidate",
        "test-candidate",
        "test_123-456",
        "ABC123",
    ]

    for candidate_id in valid_ids:
        assessment_input = AssessmentInput(
            candidate_id=candidate_id,
            submission_type="code",
            content={"code": "print('hello')"},
            paths_to_evaluate=[PathType.TECHNICAL],
        )
        assert assessment_input.candidate_id == candidate_id


def test_invalid_candidate_id():
    """Test that invalid candidate IDs are rejected."""
    invalid_ids = [
        "test@candidate",  # @ not allowed
        "test candidate",  # space not allowed
        "test#123",  # # not allowed
        "test.candidate",  # . not allowed
        "test/candidate",  # / not allowed
        "test\\candidate",  # \ not allowed
    ]

    for candidate_id in invalid_ids:
        with pytest.raises(ValidationError) as exc_info:
            AssessmentInput(
                candidate_id=candidate_id,
                submission_type="code",
                content={"code": "print('hello')"},
                paths_to_evaluate=[PathType.TECHNICAL],
            )
        assert "must contain only alphanumeric" in str(exc_info.value)


def test_candidate_id_length_limits():
    """Test candidate ID length constraints."""
    # Too short (empty)
    with pytest.raises(ValidationError):
        AssessmentInput(
            candidate_id="",
            submission_type="code",
            content={"code": "print('hello')"},
            paths_to_evaluate=[PathType.TECHNICAL],
        )

    # Too long
    long_id = "a" * 101
    with pytest.raises(ValidationError):
        AssessmentInput(
            candidate_id=long_id,
            submission_type="code",
            content={"code": "print('hello')"},
            paths_to_evaluate=[PathType.TECHNICAL],
        )

    # Valid length
    valid_id = "a" * 100
    assessment_input = AssessmentInput(
        candidate_id=valid_id,
        submission_type="code",
        content={"code": "print('hello')"},
        paths_to_evaluate=[PathType.TECHNICAL],
    )
    assert assessment_input.candidate_id == valid_id


def test_valid_submission_types():
    """Test that valid submission types are accepted."""
    valid_types = ["code", "project", "interview", "portfolio", "test"]

    for submission_type in valid_types:
        assessment_input = AssessmentInput(
            candidate_id="test123",
            submission_type=submission_type,
            content={"data": "sample"},
            paths_to_evaluate=[PathType.TECHNICAL],
        )
        assert assessment_input.submission_type == submission_type


def test_invalid_submission_type():
    """Test that invalid submission types are rejected."""
    with pytest.raises(ValidationError) as exc_info:
        AssessmentInput(
            candidate_id="test123",
            submission_type="invalid_type",
            content={"code": "print('hello')"},
            paths_to_evaluate=[PathType.TECHNICAL],
        )
    assert "must be one of" in str(exc_info.value)


def test_empty_content_rejected():
    """Test that empty content is rejected."""
    with pytest.raises(ValidationError) as exc_info:
        AssessmentInput(
            candidate_id="test123",
            submission_type="code",
            content={},
            paths_to_evaluate=[PathType.TECHNICAL],
        )
    assert "cannot be empty" in str(exc_info.value)


def test_content_size_limit():
    """Test that overly large content is rejected."""
    # Create content larger than 10MB
    large_content = {"data": "x" * 11_000_000}

    with pytest.raises(ValidationError) as exc_info:
        AssessmentInput(
            candidate_id="test123",
            submission_type="code",
            content=large_content,
            paths_to_evaluate=[PathType.TECHNICAL],
        )
    assert "exceeds maximum allowed" in str(exc_info.value)


def test_valid_content_size():
    """Test that reasonable content size is accepted."""
    # Create content under 10MB
    content = {"code": "x" * 1000}

    assessment_input = AssessmentInput(
        candidate_id="test123",
        submission_type="code",
        content=content,
        paths_to_evaluate=[PathType.TECHNICAL],
    )
    assert assessment_input.content == content


def test_submission_type_length_limit():
    """Test submission type length constraints."""
    # Too long
    long_type = "a" * 51
    with pytest.raises(ValidationError):
        AssessmentInput(
            candidate_id="test123",
            submission_type=long_type,
            content={"code": "print('hello')"},
            paths_to_evaluate=[PathType.TECHNICAL],
        )
