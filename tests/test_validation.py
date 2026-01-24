"""Tests for input validation."""

import pytest
from pydantic import ValidationError

from sono_eval.assessment.models import AssessmentInput, PathType


class TestAssessmentInputValidation:
    """Test validation logic in AssessmentInput model."""

    def test_valid_input(self):
        """Test valid input creation."""
        input_data = AssessmentInput(
            candidate_id="valid-user-123",
            submission_type="code",
            content={"code": "print('hello')"},
            paths_to_evaluate=[PathType.TECHNICAL],
        )
        assert input_data.candidate_id == "valid-user-123"

    def test_candidate_id_validation(self):
        """Test candidate_id validation."""
        # Valid cases
        AssessmentInput(
            candidate_id="user_123",
            submission_type="code",
            content={"code": "x"},
        )
        AssessmentInput(
            candidate_id="user-123",
            submission_type="code",
            content={"code": "x"},
        )

        # Invalid cases (injection prevention)
        with pytest.raises(ValidationError) as exc:
            AssessmentInput(
                candidate_id="user; drop table users;",
                submission_type="code",
                content={"code": "x"},
            )
        assert "alphanumeric" in str(exc.value)

        with pytest.raises(ValidationError):
            AssessmentInput(
                candidate_id="<script>alert(1)</script>",
                submission_type="code",
                content={"code": "x"},
            )

    def test_submission_type_validation(self):
        """Test submission_type validation."""
        with pytest.raises(ValidationError) as exc:
            AssessmentInput(
                candidate_id="user1",
                submission_type="invalid_type",
                content={"code": "x"},
            )
        assert "must be one of" in str(exc.value)

    def test_content_size_validation(self):
        """Test content size limits."""
        # Create huge content > 10MB
        huge_content = {"data": "x" * 10_000_001}

        with pytest.raises(ValidationError) as exc:
            AssessmentInput(
                candidate_id="user1",
                submission_type="code",
                content=huge_content,
            )
        assert "size exceeds maximum" in str(exc.value)

    def test_options_size_validation(self):
        """Test options size limits."""
        # Create huge options > 100KB
        huge_options = {"data": "x" * 100_001}

        with pytest.raises(ValidationError) as exc:
            AssessmentInput(
                candidate_id="user1",
                submission_type="code",
                content={"code": "x"},
                options=huge_options,
            )
        assert "options size exceeds" in str(exc.value)
