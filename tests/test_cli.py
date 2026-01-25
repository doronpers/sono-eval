"""Tests for the ALL CLI commands."""

from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from sono_eval.cli.main import cli


@pytest.fixture
def runner():
    """Create a CLI runner."""
    return CliRunner()


@patch("sono_eval.cli.commands.assess.AssessmentEngine")
@patch("sono_eval.cli.commands.assess.asyncio.run")
def test_assess_run_command(mock_asyncio_run, MockAssessmentEngine, runner):
    """Test the 'assess run' command."""
    # Mock engine instance and result
    _ = MockAssessmentEngine.return_value
    mock_result = MagicMock()
    mock_result.overall_score = 95.0
    mock_result.model_dump.return_value = {
        "candidate_id": "test_user",
        "overall_score": 95.0,
        "confidence": 0.9,
    }
    # asyncio.run returns the result of the coroutine
    mock_asyncio_run.return_value = mock_result

    # Create a temporary file to assess
    with runner.isolated_filesystem():
        with open("test_submission.py", "w") as f:
            f.write("print('hello')")

        result = runner.invoke(
            cli,
            [
                "assess",
                "run",
                "--candidate-id",
                "test_user",
                "--file",
                "test_submission.py",
                "--quiet",
            ],
        )

        assert result.exit_code == 0
        # Check output contains score format from formatters (might vary)
        # But our mock result has overall_score=95.0
        # The formatter usually prints "Overall Score: 95.0"
        # Let's check for standard output strings likely to be present
        assert "95.0" in result.output


def test_assess_run_missing_file(runner):
    """Test 'assess run' with missing file."""
    result = runner.invoke(
        cli,
        [
            "assess",
            "run",
            "--candidate-id",
            "test_user",
            "--file",
            "non_existent.py",
        ],
    )

    assert result.exit_code != 0
    # Click usually prints error about invalid path
    assert "Error" in result.output or "Invalid value" in result.output
