"""Comprehensive tests for REPL interactive mode."""

import sys
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

import pytest

from sono_eval.assessment.models import AssessmentResult, PathType
from sono_eval.cli.repl import ReplSession


class TestReplSessionInitialization:
    """Test REPL session initialization."""

    def test_repl_session_init(self):
        """Test that REPL session initializes correctly."""
        with patch("sono_eval.cli.repl.AssessmentEngine") as MockEngine:
            session = ReplSession()

            assert session.current_candidate is None
            assert session.last_result is None
            assert session.history == []
            MockEngine.assert_called_once()

    def test_repl_session_engine_creation(self):
        """Test that AssessmentEngine is created."""
        with patch("sono_eval.cli.repl.AssessmentEngine") as MockEngine:
            mock_engine = Mock()
            MockEngine.return_value = mock_engine

            session = ReplSession()

            assert session.engine == mock_engine


class TestReplCommandParsing:
    """Test command parsing in REPL."""

    def test_handle_command_parsing_simple(self):
        """Test parsing simple commands."""
        with patch("sono_eval.cli.repl.AssessmentEngine"):
            session = ReplSession()

            with patch.object(session, "cmd_help") as mock_help:
                session.handle_command("help")
                mock_help.assert_called_once_with("")

    def test_handle_command_parsing_with_args(self):
        """Test parsing commands with arguments."""
        with patch("sono_eval.cli.repl.AssessmentEngine"):
            session = ReplSession()

            with patch.object(session, "cmd_candidate") as mock_candidate:
                session.handle_command("candidate test_user_123")
                mock_candidate.assert_called_once_with("test_user_123")

    def test_handle_command_unknown(self):
        """Test handling unknown commands."""
        with (
            patch("sono_eval.cli.repl.AssessmentEngine"),
            patch("sono_eval.cli.repl.console") as mock_console,
        ):

            session = ReplSession()
            session.handle_command("unknown_command")

            # Should print error message
            assert mock_console.print.called

    def test_handle_command_case_insensitive(self):
        """Test that commands are case-insensitive."""
        with patch("sono_eval.cli.repl.AssessmentEngine"):
            session = ReplSession()

            with patch.object(session, "cmd_help") as mock_help:
                session.handle_command("HELP")
                mock_help.assert_called_once()

                session.handle_command("Help")
                assert mock_help.call_count == 2


class TestCmdCandidate:
    """Test candidate command."""

    def test_cmd_candidate_set(self):
        """Test setting candidate ID."""
        with (
            patch("sono_eval.cli.repl.AssessmentEngine"),
            patch("sono_eval.cli.repl.console") as mock_console,
        ):

            session = ReplSession()
            session.cmd_candidate("test_candidate_123")

            assert session.current_candidate == "test_candidate_123"
            mock_console.print.assert_called()

    def test_cmd_candidate_show_current(self):
        """Test showing current candidate."""
        with (
            patch("sono_eval.cli.repl.AssessmentEngine"),
            patch("sono_eval.cli.repl.console") as mock_console,
        ):

            session = ReplSession()
            session.current_candidate = "existing_candidate"

            session.cmd_candidate("")

            # Should display current candidate
            mock_console.print.assert_called()

    def test_cmd_candidate_show_none(self):
        """Test showing when no candidate set."""
        with (
            patch("sono_eval.cli.repl.AssessmentEngine"),
            patch("sono_eval.cli.repl.console") as mock_console,
        ):

            session = ReplSession()
            session.cmd_candidate("")

            # Should display message about no candidate
            mock_console.print.assert_called()


class TestCmdAssess:
    """Test assess command."""

    @pytest.fixture
    def mock_result(self):
        """Create mock assessment result."""
        return Mock(
            overall_score=85.5,
            timestamp=Mock(strftime=Mock(return_value="12:34:56")),
            spec=AssessmentResult,
        )

    def test_cmd_assess_with_file_path(self, tmp_path, mock_result):
        """Test assess command with file path."""
        # Create test file
        test_file = tmp_path / "test.py"
        test_file.write_text("def hello(): return 'world'")

        with (
            patch("sono_eval.cli.repl.AssessmentEngine") as MockEngine,
            patch("sono_eval.cli.repl.Confirm") as MockConfirm,
            patch("sono_eval.cli.repl.Prompt") as MockPrompt,
            patch("sono_eval.cli.repl.console"),
            patch("sono_eval.cli.repl.ProgressFormatter"),
            patch("sono_eval.cli.repl.AssessmentFormatter"),
            patch("asyncio.run") as mock_run,
        ):

            mock_engine = Mock()
            MockEngine.return_value = mock_engine
            mock_run.return_value = mock_result
            MockConfirm.ask.return_value = True

            session = ReplSession()
            session.current_candidate = "test_user"

            session.cmd_assess(str(test_file))

            assert session.last_result == mock_result
            assert len(session.history) == 1

    def test_cmd_assess_file_not_found(self, tmp_path):
        """Test assess command with non-existent file."""
        nonexistent = tmp_path / "nonexistent.py"

        with (
            patch("sono_eval.cli.repl.AssessmentEngine"),
            patch("sono_eval.cli.repl.ErrorFormatter") as MockErrorFormatter,
            patch("sono_eval.cli.repl.file_not_found_error") as mock_error,
            patch("sono_eval.cli.repl.console"),
        ):

            mock_error.return_value = Mock()

            session = ReplSession()
            session.current_candidate = "test_user"

            session.cmd_assess(str(nonexistent))

            # Should call error formatter
            MockErrorFormatter.format_recoverable_error.assert_called_once()

    def test_cmd_assess_file_too_large(self, tmp_path):
        """Test assess command with file too large."""
        large_file = tmp_path / "large.py"
        # Create file larger than 1MB
        with open(large_file, "w") as f:
            f.write("x" * (1_000_001))

        with (
            patch("sono_eval.cli.repl.AssessmentEngine"),
            patch("sono_eval.cli.repl.ErrorFormatter") as MockErrorFormatter,
            patch("sono_eval.cli.repl.validation_error") as mock_error,
            patch("sono_eval.cli.repl.console"),
        ):

            mock_error.return_value = Mock()

            session = ReplSession()
            session.current_candidate = "test_user"

            session.cmd_assess(str(large_file))

            # Should call validation error
            mock_error.assert_called()

    def test_cmd_assess_empty_file(self, tmp_path):
        """Test assess command with empty file."""
        empty_file = tmp_path / "empty.py"
        empty_file.write_text("")

        with (
            patch("sono_eval.cli.repl.AssessmentEngine"),
            patch("sono_eval.cli.repl.ErrorFormatter") as MockErrorFormatter,
            patch("sono_eval.cli.repl.validation_error") as mock_error,
            patch("sono_eval.cli.repl.console"),
        ):

            mock_error.return_value = Mock()

            session = ReplSession()
            session.current_candidate = "test_user"

            session.cmd_assess(str(empty_file))

            # Should call validation error for empty content
            mock_error.assert_called()

    def test_cmd_assess_prompts_for_candidate(self, tmp_path, mock_result):
        """Test that assess prompts for candidate if not set."""
        test_file = tmp_path / "test.py"
        test_file.write_text("def hello(): pass")

        with (
            patch("sono_eval.cli.repl.AssessmentEngine") as MockEngine,
            patch("sono_eval.cli.repl.Prompt") as MockPrompt,
            patch("sono_eval.cli.repl.Confirm") as MockConfirm,
            patch("sono_eval.cli.repl.console"),
            patch("sono_eval.cli.repl.ProgressFormatter"),
            patch("sono_eval.cli.repl.AssessmentFormatter"),
            patch("asyncio.run") as mock_run,
        ):

            mock_engine = Mock()
            MockEngine.return_value = mock_engine
            mock_run.return_value = mock_result
            MockPrompt.ask.return_value = "prompted_candidate"
            MockConfirm.ask.return_value = True

            session = ReplSession()
            session.current_candidate = None

            session.cmd_assess(str(test_file))

            # Should have prompted for candidate
            MockPrompt.ask.assert_called()
            assert session.current_candidate == "prompted_candidate"

    def test_cmd_assess_assessment_failure(self, tmp_path):
        """Test handling when assessment fails."""
        test_file = tmp_path / "test.py"
        test_file.write_text("def hello(): pass")

        with (
            patch("sono_eval.cli.repl.AssessmentEngine") as MockEngine,
            patch("sono_eval.cli.repl.Confirm") as MockConfirm,
            patch("sono_eval.cli.repl.console"),
            patch("sono_eval.cli.repl.ProgressFormatter"),
            patch("sono_eval.cli.repl.ErrorFormatter") as MockErrorFormatter,
            patch("sono_eval.cli.repl.internal_error") as mock_error,
            patch("asyncio.run") as mock_run,
        ):

            mock_engine = Mock()
            MockEngine.return_value = mock_engine
            mock_run.side_effect = Exception("Assessment error")
            MockConfirm.ask.return_value = True
            mock_error.return_value = Mock()

            session = ReplSession()
            session.current_candidate = "test"

            session.cmd_assess(str(test_file))

            # Should call error formatter
            MockErrorFormatter.format_recoverable_error.assert_called()


class TestCmdResult:
    """Test result command."""

    def test_cmd_result_with_result(self):
        """Test displaying last result."""
        with (
            patch("sono_eval.cli.repl.AssessmentEngine"),
            patch("sono_eval.cli.repl.AssessmentFormatter") as MockFormatter,
            patch("sono_eval.cli.repl.console"),
        ):

            session = ReplSession()
            session.last_result = Mock()

            session.cmd_result("")

            MockFormatter.format_complete_result.assert_called_once()

    def test_cmd_result_without_result(self):
        """Test result command when no result available."""
        with (
            patch("sono_eval.cli.repl.AssessmentEngine"),
            patch("sono_eval.cli.repl.console") as mock_console,
        ):

            session = ReplSession()
            session.last_result = None

            session.cmd_result("")

            # Should print message about no result
            mock_console.print.assert_called()


class TestCmdHistory:
    """Test history command."""

    def test_cmd_history_with_entries(self):
        """Test displaying history with entries."""
        with (
            patch("sono_eval.cli.repl.AssessmentEngine"),
            patch("sono_eval.cli.repl.console") as mock_console,
            patch("sono_eval.cli.repl.Table"),
            patch("sono_eval.cli.repl.AssessmentFormatter"),
        ):

            session = ReplSession()
            session.history = [
                {
                    "candidate_id": "user1",
                    "score": 85.5,
                    "timestamp": Mock(strftime=Mock(return_value="10:30:00")),
                },
                {
                    "candidate_id": "user2",
                    "score": 92.0,
                    "timestamp": Mock(strftime=Mock(return_value="11:45:00")),
                },
            ]

            session.cmd_history("")

            # Should print table
            mock_console.print.assert_called()

    def test_cmd_history_empty(self):
        """Test history command when no history."""
        with (
            patch("sono_eval.cli.repl.AssessmentEngine"),
            patch("sono_eval.cli.repl.console") as mock_console,
        ):

            session = ReplSession()
            session.cmd_history("")

            # Should print message about no history
            mock_console.print.assert_called()

    def test_cmd_history_limits_to_ten(self):
        """Test that history shows only last 10 entries."""
        with (
            patch("sono_eval.cli.repl.AssessmentEngine"),
            patch("sono_eval.cli.repl.console"),
            patch("sono_eval.cli.repl.Table") as MockTable,
            patch("sono_eval.cli.repl.AssessmentFormatter"),
        ):

            mock_table = Mock()
            MockTable.return_value = mock_table

            session = ReplSession()
            # Add 15 history entries
            session.history = [
                {
                    "candidate_id": f"user{i}",
                    "score": 80.0,
                    "timestamp": Mock(strftime=Mock(return_value="10:00:00")),
                }
                for i in range(15)
            ]

            session.cmd_history("")

            # Should only show last 10
            assert mock_table.add_row.call_count == 10


class TestCmdPaths:
    """Test paths command."""

    def test_cmd_paths(self):
        """Test displaying available paths."""
        with (
            patch("sono_eval.cli.repl.AssessmentEngine"),
            patch("sono_eval.cli.repl.console") as mock_console,
            patch("sono_eval.cli.repl.InteractiveFormatter") as MockFormatter,
        ):

            session = ReplSession()
            session.cmd_paths("")

            MockFormatter.show_path_selection_menu.assert_called_once()


class TestCmdHelp:
    """Test help command."""

    def test_cmd_help(self):
        """Test displaying help."""
        with (
            patch("sono_eval.cli.repl.AssessmentEngine"),
            patch("sono_eval.cli.repl.console") as mock_console,
            patch("sono_eval.cli.repl.Table"),
        ):

            session = ReplSession()
            session.cmd_help("")

            # Should print help table
            mock_console.print.assert_called()


class TestCmdClear:
    """Test clear command."""

    def test_cmd_clear(self):
        """Test clearing screen."""
        with (
            patch("sono_eval.cli.repl.AssessmentEngine"),
            patch("sono_eval.cli.repl.console") as mock_console,
        ):

            session = ReplSession()
            session.cmd_clear("")

            mock_console.clear.assert_called_once()


class TestCmdExit:
    """Test exit command."""

    def test_cmd_exit(self):
        """Test exit command."""
        with (
            patch("sono_eval.cli.repl.AssessmentEngine"),
            patch("sono_eval.cli.repl.console") as mock_console,
            patch("sys.exit") as mock_exit,
        ):

            session = ReplSession()
            session.cmd_exit("")

            mock_console.print.assert_called()
            mock_exit.assert_called_once_with(0)

    def test_cmd_quit_alias(self):
        """Test that quit is alias for exit."""
        with (
            patch("sono_eval.cli.repl.AssessmentEngine"),
            patch("sono_eval.cli.repl.console"),
            patch("sys.exit") as mock_exit,
        ):

            session = ReplSession()
            session.cmd_exit("")  # quit maps to cmd_exit

            mock_exit.assert_called_once_with(0)


class TestReplSessionInteractivity:
    """Test interactive REPL session behavior."""

    def test_start_displays_welcome(self):
        """Test that start displays welcome message."""
        with (
            patch("sono_eval.cli.repl.AssessmentEngine"),
            patch("sono_eval.cli.repl.WelcomeFormatter") as MockWelcome,
            patch("sono_eval.cli.repl.console") as mock_console,
            patch("sono_eval.cli.repl.Prompt") as MockPrompt,
        ):

            # Make Prompt.ask raise EOFError to exit loop
            MockPrompt.ask.side_effect = EOFError()

            session = ReplSession()

            try:
                session.start()
            except EOFError:
                pass

            MockWelcome.show_welcome.assert_called_once()

    def test_start_handles_keyboard_interrupt(self):
        """Test handling of Ctrl+C during session."""
        with (
            patch("sono_eval.cli.repl.AssessmentEngine"),
            patch("sono_eval.cli.repl.WelcomeFormatter"),
            patch("sono_eval.cli.repl.console") as mock_console,
            patch("sono_eval.cli.repl.Prompt") as MockPrompt,
        ):

            # First KeyboardInterrupt, then EOFError to exit
            MockPrompt.ask.side_effect = [KeyboardInterrupt(), EOFError()]

            session = ReplSession()
            session.start()

            # Should have printed interrupted message
            assert any(
                "Interrupted" in str(call) for call in mock_console.print.call_args_list
            )

    def test_start_handles_eof(self):
        """Test handling of EOF (Ctrl+D)."""
        with (
            patch("sono_eval.cli.repl.AssessmentEngine"),
            patch("sono_eval.cli.repl.WelcomeFormatter"),
            patch("sono_eval.cli.repl.console") as mock_console,
            patch("sono_eval.cli.repl.Prompt") as MockPrompt,
        ):

            MockPrompt.ask.side_effect = EOFError()

            session = ReplSession()
            session.start()

            # Should have printed goodbye message
            assert any(
                "Goodbye" in str(call) for call in mock_console.print.call_args_list
            )

    def test_start_handles_empty_input(self):
        """Test that empty input is handled gracefully."""
        with (
            patch("sono_eval.cli.repl.AssessmentEngine"),
            patch("sono_eval.cli.repl.WelcomeFormatter"),
            patch("sono_eval.cli.repl.console"),
            patch("sono_eval.cli.repl.Prompt") as MockPrompt,
        ):

            # Empty string, then EOFError to exit
            MockPrompt.ask.side_effect = ["", "  ", EOFError()]

            session = ReplSession()

            with patch.object(session, "handle_command") as mock_handle:
                session.start()

                # Empty inputs should not call handle_command
                mock_handle.assert_not_called()


class TestReplEdgeCases:
    """Test edge cases in REPL."""

    def test_assess_with_unicode_content(self, tmp_path, mock_result=None):
        """Test assessing file with unicode content."""
        test_file = tmp_path / "unicode.py"
        test_file.write_text("# 你好世界\ndef hello(): return '🌍'", encoding="utf-8")

        with (
            patch("sono_eval.cli.repl.AssessmentEngine") as MockEngine,
            patch("sono_eval.cli.repl.Confirm") as MockConfirm,
            patch("sono_eval.cli.repl.console"),
            patch("sono_eval.cli.repl.ProgressFormatter"),
            patch("sono_eval.cli.repl.AssessmentFormatter"),
            patch("asyncio.run") as mock_run,
        ):

            mock_engine = Mock()
            MockEngine.return_value = mock_engine
            mock_run.return_value = Mock(
                overall_score=85.0,
                timestamp=Mock(strftime=Mock(return_value="12:00:00")),
            )
            MockConfirm.ask.return_value = True

            session = ReplSession()
            session.current_candidate = "test"

            # Should handle unicode without errors
            session.cmd_assess(str(test_file))

    def test_assess_non_utf8_file(self, tmp_path):
        """Test handling non-UTF-8 encoded file."""
        test_file = tmp_path / "binary.dat"
        test_file.write_bytes(b"\x80\x81\x82")  # Invalid UTF-8

        with (
            patch("sono_eval.cli.repl.AssessmentEngine"),
            patch("sono_eval.cli.repl.ErrorFormatter") as MockErrorFormatter,
            patch("sono_eval.cli.repl.RecoverableError"),
            patch("sono_eval.cli.repl.ErrorSeverity"),
            patch("sono_eval.cli.repl.console"),
        ):

            session = ReplSession()
            session.current_candidate = "test"

            session.cmd_assess(str(test_file))

            # Should handle encoding error
            MockErrorFormatter.format_recoverable_error.assert_called()

    def test_command_with_extra_whitespace(self):
        """Test commands with extra whitespace."""
        with patch("sono_eval.cli.repl.AssessmentEngine"):
            session = ReplSession()

            with patch.object(session, "cmd_candidate") as mock_candidate:
                session.handle_command("candidate    test_user   ")
                # Should parse correctly despite whitespace
                assert mock_candidate.called
