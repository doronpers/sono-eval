"""Tests for CLI assess command."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from sono_eval.cli.commands.assess import assess


class TestAssessRunCommand:
    """Tests for assess run command."""

    @patch("sono_eval.cli.commands.assess.AssessmentEngine")
    def test_assess_run_with_file_basic(
        self, mock_engine_class, cli_runner, temp_code_file, mock_assessment_result
    ):
        """Test basic assessment with file input."""
        # Setup mock
        mock_engine = MagicMock()
        mock_engine.assess = AsyncMock(return_value=mock_assessment_result)
        mock_engine_class.return_value = mock_engine

        # Run command
        result = cli_runner.invoke(
            assess,
            [
                "run",
                "--candidate-id",
                "test_candidate",
                "--file",
                temp_code_file,
                "--quiet",
            ],
        )

        # Verify
        assert result.exit_code == 0
        assert "85.00" in result.output  # Score output in quiet mode

    @patch("sono_eval.cli.commands.assess.AssessmentEngine")
    def test_assess_run_with_content(
        self, mock_engine_class, cli_runner, mock_assessment_result
    ):
        """Test assessment with inline content."""
        # Setup mock
        mock_engine = MagicMock()
        mock_engine.assess = AsyncMock(return_value=mock_assessment_result)
        mock_engine_class.return_value = mock_engine

        # Run command
        result = cli_runner.invoke(
            assess,
            [
                "run",
                "--candidate-id",
                "john_doe",
                "--content",
                "def hello(): return 'world'",
                "--quiet",
            ],
        )

        # Verify
        assert result.exit_code == 0
        assert "85.00" in result.output

    def test_assess_run_missing_content(self, cli_runner):
        """Test that missing content/file raises error."""
        result = cli_runner.invoke(assess, ["run", "--candidate-id", "test_candidate"])

        # Should abort due to missing content
        assert result.exit_code != 0

    def test_assess_run_file_not_found(self, cli_runner):
        """Test handling of non-existent file."""
        result = cli_runner.invoke(
            assess,
            [
                "run",
                "--candidate-id",
                "test_candidate",
                "--file",
                "/nonexistent/file.py",
            ],
        )

        # Should fail because file doesn't exist (Click validates path)
        assert result.exit_code != 0

    @patch("sono_eval.cli.commands.assess.AssessmentEngine")
    def test_assess_run_empty_file(self, mock_engine_class, cli_runner, empty_file):
        """Test handling of empty file."""
        result = cli_runner.invoke(
            assess,
            ["run", "--candidate-id", "test_candidate", "--file", empty_file],
        )

        # Should abort due to empty file
        assert result.exit_code != 0

    @patch("sono_eval.cli.commands.assess.AssessmentEngine")
    def test_assess_run_with_specific_paths(
        self, mock_engine_class, cli_runner, temp_code_file, mock_assessment_result
    ):
        """Test assessment with specific paths."""
        # Setup mock
        mock_engine = MagicMock()
        mock_engine.assess = AsyncMock(return_value=mock_assessment_result)
        mock_engine_class.return_value = mock_engine

        # Run command with specific paths
        result = cli_runner.invoke(
            assess,
            [
                "run",
                "--candidate-id",
                "test_candidate",
                "--file",
                temp_code_file,
                "--paths",
                "technical",
                "--paths",
                "design",
                "--quiet",
            ],
        )

        # Verify
        assert result.exit_code == 0

    @patch("sono_eval.cli.commands.assess.AssessmentEngine")
    def test_assess_run_with_output_file(
        self,
        mock_engine_class,
        cli_runner,
        temp_code_file,
        mock_assessment_result,
        tmp_path,
    ):
        """Test saving results to output file."""
        # Setup mock
        mock_engine = MagicMock()
        mock_engine.assess = AsyncMock(return_value=mock_assessment_result)
        mock_engine_class.return_value = mock_engine

        output_file = tmp_path / "results.json"

        # Run command
        result = cli_runner.invoke(
            assess,
            [
                "run",
                "--candidate-id",
                "test_candidate",
                "--file",
                temp_code_file,
                "--output",
                str(output_file),
                "--quiet",
            ],
        )

        # Verify
        assert result.exit_code == 0
        assert output_file.exists()

    @patch("sono_eval.cli.commands.assess.AssessmentEngine")
    def test_assess_run_verbose_mode(
        self, mock_engine_class, cli_runner, temp_code_file, mock_assessment_result
    ):
        """Test verbose mode output."""
        # Setup mock
        mock_engine = MagicMock()
        mock_engine.assess = AsyncMock(return_value=mock_assessment_result)
        mock_engine_class.return_value = mock_engine

        # Run command in verbose mode
        result = cli_runner.invoke(
            assess,
            [
                "run",
                "--candidate-id",
                "test_candidate",
                "--file",
                temp_code_file,
                "--verbose",
            ],
        )

        # Verify - verbose mode shows more output
        assert result.exit_code == 0

    @patch("sono_eval.cli.commands.assess.AssessmentEngine")
    def test_assess_run_invalid_path(
        self, mock_engine_class, cli_runner, temp_code_file, mock_assessment_result
    ):
        """Test handling of invalid path type."""
        # Setup mock
        mock_engine = MagicMock()
        mock_engine.assess = AsyncMock(return_value=mock_assessment_result)
        mock_engine_class.return_value = mock_engine

        # Run command with invalid path
        result = cli_runner.invoke(
            assess,
            [
                "run",
                "--candidate-id",
                "test_candidate",
                "--file",
                temp_code_file,
                "--paths",
                "invalid_path",
            ],
        )

        # Should abort because no valid paths
        assert result.exit_code != 0

    @patch("sono_eval.cli.commands.assess.AssessmentEngine")
    def test_assess_run_with_submission_type(
        self, mock_engine_class, cli_runner, temp_code_file, mock_assessment_result
    ):
        """Test specifying submission type."""
        # Setup mock
        mock_engine = MagicMock()
        mock_engine.assess = AsyncMock(return_value=mock_assessment_result)
        mock_engine_class.return_value = mock_engine

        # Run command with custom type
        result = cli_runner.invoke(
            assess,
            [
                "run",
                "--candidate-id",
                "test_candidate",
                "--file",
                temp_code_file,
                "--type",
                "project",
                "--quiet",
            ],
        )

        # Verify
        assert result.exit_code == 0

    @patch("sono_eval.cli.commands.assess.AssessmentEngine")
    def test_assess_run_engine_error(
        self, mock_engine_class, cli_runner, temp_code_file
    ):
        """Test handling of assessment engine errors."""
        # Setup mock to raise error
        mock_engine = MagicMock()
        mock_engine.assess = AsyncMock(side_effect=Exception("Engine failure"))
        mock_engine_class.return_value = mock_engine

        # Run command
        result = cli_runner.invoke(
            assess,
            [
                "run",
                "--candidate-id",
                "test_candidate",
                "--file",
                temp_code_file,
            ],
        )

        # Should handle error gracefully
        assert result.exit_code != 0

    @patch("sono_eval.cli.commands.assess.AssessmentEngine")
    @patch("sono_eval.cli.commands.assess.MemUStorage")
    def test_assess_run_saves_to_memory(
        self,
        mock_storage_class,
        mock_engine_class,
        cli_runner,
        temp_code_file,
        mock_assessment_result,
        mock_candidate_memory,
    ):
        """Test that assessment is saved to memory storage."""
        # Setup mocks
        mock_engine = MagicMock()
        mock_engine.assess = AsyncMock(return_value=mock_assessment_result)
        mock_engine_class.return_value = mock_engine

        mock_storage = MagicMock()
        mock_storage.get_candidate_memory.return_value = mock_candidate_memory
        mock_storage.add_memory_node.return_value = None
        mock_storage_class.return_value = mock_storage

        # Run command
        result = cli_runner.invoke(
            assess,
            [
                "run",
                "--candidate-id",
                "test_candidate",
                "--file",
                temp_code_file,
                "--quiet",
            ],
        )

        # Verify memory was called
        assert result.exit_code == 0
        mock_storage.get_candidate_memory.assert_called_once_with("test_candidate")

    @patch("sono_eval.cli.commands.assess.AssessmentEngine")
    def test_assess_run_all_paths_when_none_specified(
        self, mock_engine_class, cli_runner, temp_code_file, mock_assessment_result
    ):
        """Test that all paths are evaluated when none specified."""
        # Setup mock
        mock_engine = MagicMock()
        mock_engine.assess = AsyncMock(return_value=mock_assessment_result)
        mock_engine_class.return_value = mock_engine

        # Run command without specifying paths
        result = cli_runner.invoke(
            assess,
            [
                "run",
                "--candidate-id",
                "test_candidate",
                "--file",
                temp_code_file,
                "--quiet",
            ],
        )

        # Verify
        assert result.exit_code == 0

        # Check that assess was called
        assert mock_engine.assess.called

        # Get the assessment input that was passed
        call_args = mock_engine.assess.call_args
        assessment_input = call_args[0][0]

        # Should have all path types
        from sono_eval.assessment.models import PathType

        assert len(assessment_input.paths_to_evaluate) == len(PathType)

    @patch("sono_eval.cli.commands.assess.AssessmentEngine")
    def test_assess_run_respects_quiet_flag(
        self, mock_engine_class, cli_runner, temp_code_file, mock_assessment_result
    ):
        """Test that quiet mode only outputs score."""
        # Setup mock
        mock_engine = MagicMock()
        mock_engine.assess = AsyncMock(return_value=mock_assessment_result)
        mock_engine_class.return_value = mock_engine

        # Run in quiet mode
        result = cli_runner.invoke(
            assess,
            [
                "run",
                "--candidate-id",
                "test_candidate",
                "--file",
                temp_code_file,
                "--quiet",
            ],
        )

        # Should only show the score
        assert result.exit_code == 0
        assert "85.00" in result.output
        # Should not show verbose output
        assert "Running assessment" not in result.output

    @patch("sono_eval.cli.commands.assess.AssessmentEngine")
    def test_assess_run_creates_valid_assessment_input(
        self, mock_engine_class, cli_runner, temp_code_file, mock_assessment_result
    ):
        """Test that AssessmentInput is created correctly."""
        # Setup mock
        mock_engine = MagicMock()
        mock_engine.assess = AsyncMock(return_value=mock_assessment_result)
        mock_engine_class.return_value = mock_engine

        # Run command
        result = cli_runner.invoke(
            assess,
            [
                "run",
                "--candidate-id",
                "john_doe",
                "--file",
                temp_code_file,
                "--type",
                "code",
                "--paths",
                "technical",
                "--quiet",
            ],
        )

        # Verify
        assert result.exit_code == 0

        # Check assessment input
        call_args = mock_engine.assess.call_args[0]
        assessment_input = call_args[0]

        assert assessment_input.candidate_id == "john_doe"
        assert assessment_input.submission_type == "code"
        assert "code" in assessment_input.content

    @patch("sono_eval.cli.commands.assess.AssessmentEngine")
    @patch("builtins.open", side_effect=PermissionError("Access denied"))
    def test_assess_run_permission_error(
        self, mock_open, mock_engine_class, cli_runner
    ):
        """Test handling of file permission errors."""
        result = cli_runner.invoke(
            assess,
            [
                "run",
                "--candidate-id",
                "test_candidate",
                "--file",
                "protected_file.py",
            ],
        )

        # Should handle permission error
        assert result.exit_code != 0


class TestAssessGroup:
    """Tests for assess command group."""

    def test_assess_group_help(self, cli_runner):
        """Test that assess command shows help."""
        result = cli_runner.invoke(assess, ["--help"])

        assert result.exit_code == 0
        assert "Assessment commands" in result.output

    def test_assess_run_help(self, cli_runner):
        """Test that assess run shows help."""
        result = cli_runner.invoke(assess, ["run", "--help"])

        assert result.exit_code == 0
        assert "Run an assessment" in result.output
        assert "--candidate-id" in result.output
        assert "--file" in result.output
        assert "--content" in result.output
