"""Tests for CLI candidate command."""

from unittest.mock import MagicMock, patch

import pytest

from sono_eval.cli.commands.candidate import candidate


class TestCandidateCreateCommand:
    """Tests for candidate create command."""

    @patch("sono_eval.cli.commands.candidate.MemUStorage")
    def test_create_basic(self, mock_storage_class, cli_runner, mock_candidate_memory):
        """Test creating a basic candidate."""
        # Setup mock
        mock_storage = MagicMock()
        mock_storage.get_candidate_memory.return_value = None  # Doesn't exist
        mock_storage.create_candidate_memory.return_value = mock_candidate_memory
        mock_storage_class.return_value = mock_storage

        # Run command
        result = cli_runner.invoke(candidate, ["create", "--id", "john_doe", "--quiet"])

        # Verify
        assert result.exit_code == 0
        mock_storage.create_candidate_memory.assert_called_once_with("john_doe", None)

    @patch("sono_eval.cli.commands.candidate.MemUStorage")
    def test_create_with_data(
        self, mock_storage_class, cli_runner, mock_candidate_memory
    ):
        """Test creating a candidate with initial data."""
        # Setup mock
        mock_storage = MagicMock()
        mock_storage.get_candidate_memory.return_value = None
        mock_storage.create_candidate_memory.return_value = mock_candidate_memory
        mock_storage_class.return_value = mock_storage

        # Run command with JSON data
        result = cli_runner.invoke(
            candidate,
            [
                "create",
                "--id",
                "john_doe",
                "--data",
                '{"email": "john@example.com"}',
                "--quiet",
            ],
        )

        # Verify
        assert result.exit_code == 0
        mock_storage.create_candidate_memory.assert_called_once()
        call_args = mock_storage.create_candidate_memory.call_args
        assert call_args[0][0] == "john_doe"
        assert call_args[0][1] == {"email": "john@example.com"}

    @patch("sono_eval.cli.commands.candidate.MemUStorage")
    def test_create_invalid_json(self, mock_storage_class, cli_runner):
        """Test creating with invalid JSON data."""
        # Setup mock
        mock_storage = MagicMock()
        mock_storage_class.return_value = mock_storage

        # Run command with invalid JSON
        result = cli_runner.invoke(
            candidate,
            ["create", "--id", "john_doe", "--data", "invalid-json"],
        )

        # Should fail due to invalid JSON
        assert result.exit_code != 0

    @patch("sono_eval.cli.commands.candidate.MemUStorage")
    def test_create_existing_candidate(
        self, mock_storage_class, cli_runner, mock_candidate_memory
    ):
        """Test creating a candidate that already exists."""
        # Setup mock - candidate already exists
        mock_storage = MagicMock()
        mock_storage.get_candidate_memory.return_value = mock_candidate_memory
        mock_storage_class.return_value = mock_storage

        # Run command (non-interactive mode will auto-abort)
        result = cli_runner.invoke(
            candidate, ["create", "--id", "existing_candidate"], input="n\n"
        )

        # Should show warning and ask for confirmation
        assert "already exists" in result.output

    @patch("sono_eval.cli.commands.candidate.MemUStorage")
    def test_create_validation_error(self, mock_storage_class, cli_runner):
        """Test creating with validation error."""
        # Setup mock to raise ValueError
        mock_storage = MagicMock()
        mock_storage.get_candidate_memory.return_value = None
        mock_storage.create_candidate_memory.side_effect = ValueError(
            "Invalid candidate ID"
        )
        mock_storage_class.return_value = mock_storage

        # Run command
        result = cli_runner.invoke(
            candidate, ["create", "--id", "invalid id!", "--quiet"]
        )

        # Should handle validation error
        assert result.exit_code != 0

    def test_create_missing_id(self, cli_runner):
        """Test that missing ID raises error."""
        result = cli_runner.invoke(candidate, ["create"])

        # Should fail due to missing required option
        assert result.exit_code != 0


class TestCandidateShowCommand:
    """Tests for candidate show command."""

    @patch("sono_eval.cli.commands.candidate.MemUStorage")
    def test_show_basic(self, mock_storage_class, cli_runner, mock_candidate_memory):
        """Test showing candidate information."""
        # Setup mock
        mock_storage = MagicMock()
        mock_storage.get_candidate_memory.return_value = mock_candidate_memory
        mock_storage_class.return_value = mock_storage

        # Run command
        result = cli_runner.invoke(candidate, ["show", "--id", "test_candidate"])

        # Verify
        assert result.exit_code == 0
        assert "test_candidate" in result.output
        assert "Last Updated" in result.output

    @patch("sono_eval.cli.commands.candidate.MemUStorage")
    def test_show_not_found(self, mock_storage_class, cli_runner):
        """Test showing non-existent candidate."""
        # Setup mock - candidate doesn't exist
        mock_storage = MagicMock()
        mock_storage.get_candidate_memory.return_value = None
        mock_storage_class.return_value = mock_storage

        # Run command
        result = cli_runner.invoke(candidate, ["show", "--id", "nonexistent"])

        # Should show error
        assert result.exit_code != 0
        assert "not found" in result.output

    @patch("sono_eval.cli.commands.candidate.MemUStorage")
    def test_show_verbose(self, mock_storage_class, cli_runner, mock_candidate_memory):
        """Test showing candidate with verbose output."""
        # Setup mock
        mock_storage = MagicMock()
        mock_storage.get_candidate_memory.return_value = mock_candidate_memory
        mock_storage_class.return_value = mock_storage

        # Run command in verbose mode
        result = cli_runner.invoke(
            candidate, ["show", "--id", "test_candidate", "--verbose"]
        )

        # Verify
        assert result.exit_code == 0
        assert "Memory Structure" in result.output

    def test_show_missing_id(self, cli_runner):
        """Test that missing ID raises error."""
        result = cli_runner.invoke(candidate, ["show"])

        # Should fail due to missing required option
        assert result.exit_code != 0


class TestCandidateListCommand:
    """Tests for candidate list command."""

    @patch("sono_eval.cli.commands.candidate.MemUStorage")
    def test_list_with_candidates(
        self, mock_storage_class, cli_runner, mock_candidate_memory
    ):
        """Test listing candidates."""
        # Setup mock
        mock_storage = MagicMock()
        mock_storage.list_candidates.return_value = ["john_doe", "jane_smith"]
        mock_storage.get_candidate_memory.return_value = mock_candidate_memory
        mock_storage_class.return_value = mock_storage

        # Run command
        result = cli_runner.invoke(candidate, ["list"])

        # Verify
        assert result.exit_code == 0
        assert "Candidates" in result.output

    @patch("sono_eval.cli.commands.candidate.MemUStorage")
    def test_list_quiet_mode(self, mock_storage_class, cli_runner):
        """Test listing candidates in quiet mode."""
        # Setup mock
        mock_storage = MagicMock()
        mock_storage.list_candidates.return_value = ["john_doe", "jane_smith"]
        mock_storage_class.return_value = mock_storage

        # Run command in quiet mode
        result = cli_runner.invoke(candidate, ["list", "--quiet"])

        # Verify
        assert result.exit_code == 0
        assert "john_doe" in result.output
        assert "jane_smith" in result.output
        # Should not show table header in quiet mode
        assert "Candidates" not in result.output

    @patch("sono_eval.cli.commands.candidate.MemUStorage")
    def test_list_no_candidates(self, mock_storage_class, cli_runner):
        """Test listing when no candidates exist."""
        # Setup mock
        mock_storage = MagicMock()
        mock_storage.list_candidates.return_value = []
        mock_storage_class.return_value = mock_storage

        # Run command
        result = cli_runner.invoke(candidate, ["list"])

        # Verify
        assert result.exit_code == 0
        assert "No candidates found" in result.output

    @patch("sono_eval.cli.commands.candidate.MemUStorage")
    def test_list_error_handling(self, mock_storage_class, cli_runner):
        """Test error handling during list."""
        # Setup mock to raise error
        mock_storage = MagicMock()
        mock_storage.list_candidates.side_effect = Exception("Storage error")
        mock_storage_class.return_value = mock_storage

        # Run command
        result = cli_runner.invoke(candidate, ["list"])

        # Should handle error
        assert result.exit_code != 0


class TestCandidateDeleteCommand:
    """Tests for candidate delete command."""

    @patch("sono_eval.cli.commands.candidate.MemUStorage")
    def test_delete_basic(self, mock_storage_class, cli_runner, mock_candidate_memory):
        """Test deleting a candidate."""
        # Setup mock
        mock_storage = MagicMock()
        mock_storage.get_candidate_memory.return_value = mock_candidate_memory
        mock_storage.delete_candidate_memory.return_value = True
        mock_storage_class.return_value = mock_storage

        # Run command with confirmation
        result = cli_runner.invoke(
            candidate, ["delete", "--id", "test_candidate"], input="y\n"
        )

        # Verify
        assert result.exit_code == 0
        mock_storage.delete_candidate_memory.assert_called_once_with("test_candidate")

    @patch("sono_eval.cli.commands.candidate.MemUStorage")
    def test_delete_not_found(self, mock_storage_class, cli_runner):
        """Test deleting non-existent candidate."""
        # Setup mock - candidate doesn't exist
        mock_storage = MagicMock()
        mock_storage.get_candidate_memory.return_value = None
        mock_storage_class.return_value = mock_storage

        # Run command
        result = cli_runner.invoke(
            candidate, ["delete", "--id", "nonexistent"], input="y\n"
        )

        # Should show error
        assert result.exit_code != 0
        assert "not found" in result.output

    @patch("sono_eval.cli.commands.candidate.MemUStorage")
    def test_delete_cancelled(
        self, mock_storage_class, cli_runner, mock_candidate_memory
    ):
        """Test cancelling delete operation."""
        # Setup mock
        mock_storage = MagicMock()
        mock_storage.get_candidate_memory.return_value = mock_candidate_memory
        mock_storage_class.return_value = mock_storage

        # Run command and cancel
        result = cli_runner.invoke(
            candidate, ["delete", "--id", "test_candidate"], input="n\n"
        )

        # Should abort without deleting
        assert result.exit_code != 0
        mock_storage.delete_candidate_memory.assert_not_called()

    @patch("sono_eval.cli.commands.candidate.MemUStorage")
    def test_delete_with_force(
        self, mock_storage_class, cli_runner, mock_candidate_memory
    ):
        """Test deleting with force flag."""
        # Setup mock
        mock_storage = MagicMock()
        mock_storage.get_candidate_memory.return_value = mock_candidate_memory
        mock_storage.delete_candidate_memory.return_value = True
        mock_storage_class.return_value = mock_storage

        # Run command with force flag (no confirmation needed)
        result = cli_runner.invoke(
            candidate, ["delete", "--id", "test_candidate", "--force"]
        )

        # Verify
        assert result.exit_code == 0
        mock_storage.delete_candidate_memory.assert_called_once_with("test_candidate")


class TestCandidateExportCommand:
    """Tests for candidate export command."""

    @patch("sono_eval.cli.commands.candidate.MemUStorage")
    def test_export_basic(
        self, mock_storage_class, cli_runner, mock_candidate_memory, tmp_path
    ):
        """Test exporting a candidate."""
        # Setup mock
        mock_storage = MagicMock()
        mock_storage.get_candidate_memory.return_value = mock_candidate_memory
        mock_storage_class.return_value = mock_storage

        output_file = tmp_path / "export.json"

        # Run command
        result = cli_runner.invoke(
            candidate,
            ["export", "--id", "test_candidate", "--output", str(output_file)],
        )

        # Verify
        assert result.exit_code == 0
        assert output_file.exists()

    @patch("sono_eval.cli.commands.candidate.MemUStorage")
    def test_export_not_found(self, mock_storage_class, cli_runner, tmp_path):
        """Test exporting non-existent candidate."""
        # Setup mock - candidate doesn't exist
        mock_storage = MagicMock()
        mock_storage.get_candidate_memory.return_value = None
        mock_storage_class.return_value = mock_storage

        output_file = tmp_path / "export.json"

        # Run command
        result = cli_runner.invoke(
            candidate,
            ["export", "--id", "nonexistent", "--output", str(output_file)],
        )

        # Should show error
        assert result.exit_code != 0
        assert not output_file.exists()


class TestCandidateGroup:
    """Tests for candidate command group."""

    def test_candidate_group_help(self, cli_runner):
        """Test that candidate command shows help."""
        result = cli_runner.invoke(candidate, ["--help"])

        assert result.exit_code == 0
        assert "Candidate management" in result.output

    def test_candidate_create_help(self, cli_runner):
        """Test that candidate create shows help."""
        result = cli_runner.invoke(candidate, ["create", "--help"])

        assert result.exit_code == 0
        assert "Create a new candidate" in result.output
        assert "--id" in result.output

    def test_candidate_show_help(self, cli_runner):
        """Test that candidate show shows help."""
        result = cli_runner.invoke(candidate, ["show", "--help"])

        assert result.exit_code == 0
        assert "Show candidate information" in result.output

    def test_candidate_list_help(self, cli_runner):
        """Test that candidate list shows help."""
        result = cli_runner.invoke(candidate, ["list", "--help"])

        assert result.exit_code == 0
        assert "List all candidates" in result.output
