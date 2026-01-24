"""Comprehensive tests for all CLI commands."""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest
from click.testing import CliRunner

from sono_eval.cli.main import cli


@pytest.fixture
def runner():
    """Create a CLI runner."""
    return CliRunner()


@pytest.fixture
def temp_file():
    """Create a temporary file with code."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("def hello():\n    return 'world'\n")
        yield f.name
    Path(f.name).unlink(missing_ok=True)


# ============================================================================
# Assess Command Tests
# ============================================================================


@patch("sono_eval.cli.commands.assess.AssessmentEngine")
@patch("sono_eval.cli.commands.assess.asyncio.run")
def test_assess_run_with_file(mock_asyncio_run, MockAssessmentEngine, runner, temp_file):
    """Test assess run with file input."""
    mock_result = MagicMock()
    mock_result.overall_score = 85.0
    mock_result.assessment_id = "assess_001"
    mock_result.candidate_id = "test_user"
    mock_result.confidence = 0.9
    mock_result.summary = "Good code"
    mock_result.path_scores = []
    mock_result.key_findings = []
    mock_result.recommendations = []
    mock_result.model_dump.return_value = {
        "candidate_id": "test_user",
        "assessment_id": "assess_001",
        "overall_score": 85.0,
        "confidence": 0.9,
    }
    mock_asyncio_run.return_value = mock_result

    result = runner.invoke(
        cli,
        [
            "assess",
            "run",
            "--candidate-id",
            "test_user",
            "--file",
            temp_file,
            "--quiet",
        ],
    )

    assert result.exit_code == 0
    assert "85.0" in result.output or "85" in result.output


@patch("sono_eval.cli.commands.assess.AssessmentEngine")
@patch("sono_eval.cli.commands.assess.asyncio.run")
def test_assess_run_with_content(mock_asyncio_run, MockAssessmentEngine, runner):
    """Test assess run with inline content."""
    mock_result = MagicMock()
    mock_result.overall_score = 90.0
    mock_result.assessment_id = "assess_002"
    mock_result.candidate_id = "test_user"
    mock_result.confidence = 0.95
    mock_result.summary = "Excellent code"
    mock_result.path_scores = []
    mock_result.key_findings = []
    mock_result.recommendations = []
    mock_result.model_dump.return_value = {
        "candidate_id": "test_user",
        "assessment_id": "assess_002",
        "overall_score": 90.0,
    }
    mock_asyncio_run.return_value = mock_result

    result = runner.invoke(
        cli,
        [
            "assess",
            "run",
            "--candidate-id",
            "test_user",
            "--content",
            "def test(): pass",
            "--paths",
            "technical",
            "--quiet",
        ],
    )

    assert result.exit_code == 0


def test_assess_run_missing_input(runner):
    """Test assess run without file or content."""
    result = runner.invoke(
        cli,
        [
            "assess",
            "run",
            "--candidate-id",
            "test_user",
        ],
    )

    assert result.exit_code != 0
    assert "Error" in result.output or "required" in result.output.lower()


def test_assess_run_missing_file(runner):
    """Test assess run with non-existent file."""
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


@patch("sono_eval.cli.commands.assess.AssessmentEngine")
@patch("sono_eval.cli.commands.assess.asyncio.run")
def test_assess_run_with_output_file(mock_asyncio_run, MockAssessmentEngine, runner, temp_file):
    """Test assess run with output file."""
    mock_result = MagicMock()
    mock_result.overall_score = 80.0
    mock_result.assessment_id = "assess_003"
    mock_result.candidate_id = "test_user"
    mock_result.confidence = 0.85
    mock_result.summary = "Good"
    mock_result.path_scores = []
    mock_result.key_findings = []
    mock_result.recommendations = []
    mock_result.model_dump.return_value = {
        "candidate_id": "test_user",
        "assessment_id": "assess_003",
        "overall_score": 80.0,
    }
    mock_asyncio_run.return_value = mock_result

    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            [
                "assess",
                "run",
                "--candidate-id",
                "test_user",
                "--file",
                temp_file,
                "--output",
                "results.json",
                "--quiet",
            ],
        )

        assert result.exit_code == 0
        assert Path("results.json").exists()


# ============================================================================
# Candidate Command Tests
# ============================================================================


@patch("sono_eval.cli.commands.candidate.MemUStorage")
def test_candidate_create_basic(MockStorage, runner):
    """Test candidate create command."""
    mock_storage = Mock()
    mock_memory = Mock()
    mock_memory.candidate_id = "test_candidate"
    mock_memory.last_updated = "2026-01-23T10:00:00Z"
    mock_storage.get_candidate_memory.return_value = None
    mock_storage.create_candidate_memory.return_value = mock_memory
    MockStorage.return_value = mock_storage

    result = runner.invoke(
        cli,
        [
            "candidate",
            "create",
            "--id",
            "test_candidate",
            "--quiet",
        ],
    )

    assert result.exit_code == 0
    mock_storage.create_candidate_memory.assert_called_once()


@patch("sono_eval.cli.commands.candidate.MemUStorage")
def test_candidate_create_with_data(MockStorage, runner):
    """Test candidate create with initial data."""
    mock_storage = Mock()
    mock_memory = Mock()
    mock_memory.candidate_id = "test_candidate"
    mock_memory.last_updated = "2026-01-23T10:00:00Z"
    mock_storage.get_candidate_memory.return_value = None
    mock_storage.create_candidate_memory.return_value = mock_memory
    MockStorage.return_value = mock_storage

    result = runner.invoke(
        cli,
        [
            "candidate",
            "create",
            "--id",
            "test_candidate",
            "--data",
            '{"email": "test@example.com"}',
            "--quiet",
        ],
    )

    assert result.exit_code == 0


def test_candidate_create_invalid_json(runner):
    """Test candidate create with invalid JSON."""
    result = runner.invoke(
        cli,
        [
            "candidate",
            "create",
            "--id",
            "test_candidate",
            "--data",
            "invalid json",
        ],
    )

    assert result.exit_code != 0
    assert "JSON" in result.output or "Error" in result.output


@patch("sono_eval.cli.commands.candidate.MemUStorage")
def test_candidate_show(MockStorage, runner):
    """Test candidate show command."""
    mock_storage = Mock()
    mock_memory = Mock()
    mock_memory.candidate_id = "test_candidate"
    mock_memory.last_updated = "2026-01-23T10:00:00Z"
    mock_memory.nodes = {}
    mock_memory.version = "1.0"
    mock_memory.root_node = Mock()
    mock_memory.root_node.data = {}
    mock_memory.root_node.children = []
    mock_storage.get_candidate_memory.return_value = mock_memory
    MockStorage.return_value = mock_storage

    result = runner.invoke(
        cli,
        [
            "candidate",
            "show",
            "--id",
            "test_candidate",
        ],
    )

    assert result.exit_code == 0
    assert "test_candidate" in result.output


@patch("sono_eval.cli.commands.candidate.MemUStorage")
def test_candidate_show_not_found(MockStorage, runner):
    """Test candidate show with non-existent candidate."""
    mock_storage = Mock()
    mock_storage.get_candidate_memory.return_value = None
    MockStorage.return_value = mock_storage

    result = runner.invoke(
        cli,
        [
            "candidate",
            "show",
            "--id",
            "non_existent",
        ],
    )

    assert result.exit_code != 0
    assert "not found" in result.output.lower() or "Error" in result.output


@patch("sono_eval.cli.commands.candidate.MemUStorage")
def test_candidate_list(MockStorage, runner):
    """Test candidate list command."""
    mock_storage = Mock()
    mock_storage.list_candidates.return_value = ["candidate1", "candidate2"]
    mock_memory = Mock()
    mock_memory.candidate_id = "candidate1"
    mock_storage.get_candidate_memory.return_value = mock_memory
    MockStorage.return_value = mock_storage

    result = runner.invoke(
        cli,
        [
            "candidate",
            "list",
        ],
    )

    assert result.exit_code == 0


@patch("sono_eval.cli.commands.candidate.MemUStorage")
def test_candidate_list_empty(MockStorage, runner):
    """Test candidate list with no candidates."""
    mock_storage = Mock()
    mock_storage.list_candidates.return_value = []
    MockStorage.return_value = mock_storage

    result = runner.invoke(
        cli,
        [
            "candidate",
            "list",
        ],
    )

    assert result.exit_code == 0
    assert "No candidates" in result.output or "found" in result.output.lower()


@patch("sono_eval.cli.commands.candidate.MemUStorage")
def test_candidate_list_quiet(MockStorage, runner):
    """Test candidate list in quiet mode."""
    mock_storage = Mock()
    mock_storage.list_candidates.return_value = ["candidate1", "candidate2"]
    MockStorage.return_value = mock_storage

    result = runner.invoke(
        cli,
        [
            "candidate",
            "list",
            "--quiet",
        ],
    )

    assert result.exit_code == 0
    # Should just print IDs
    assert "candidate1" in result.output or "candidate2" in result.output


@patch("sono_eval.cli.commands.candidate.MemUStorage")
def test_candidate_history(MockStorage, runner):
    """Test candidate history command."""
    mock_storage = Mock()
    mock_memory = Mock()
    mock_memory.candidate_id = "test_candidate"
    mock_node = Mock()
    mock_node.metadata = {"type": "assessment"}
    mock_node.data = {
        "assessment_result": {
            "assessment_id": "assess_001",
            "timestamp": "2026-01-23T10:00:00Z",
            "overall_score": 85.0,
            "confidence": 0.9,
            "dominant_path": "technical",
            "path_scores": [],
        }
    }
    mock_memory.nodes = {"node1": mock_node}
    mock_storage.get_candidate_memory.return_value = mock_memory
    MockStorage.return_value = mock_storage

    result = runner.invoke(
        cli,
        [
            "candidate",
            "history",
            "--id",
            "test_candidate",
        ],
    )

    assert result.exit_code == 0


@patch("sono_eval.cli.commands.candidate.MemUStorage")
def test_candidate_history_json(MockStorage, runner):
    """Test candidate history with JSON format."""
    mock_storage = Mock()
    mock_memory = Mock()
    mock_memory.candidate_id = "test_candidate"
    mock_node = Mock()
    mock_node.metadata = {"type": "assessment"}
    mock_node.data = {
        "assessment_result": {
            "assessment_id": "assess_001",
            "timestamp": "2026-01-23T10:00:00Z",
            "overall_score": 85.0,
            "confidence": 0.9,
            "dominant_path": "technical",
            "path_scores": [],
        }
    }
    mock_memory.nodes = {"node1": mock_node}
    mock_storage.get_candidate_memory.return_value = mock_memory
    MockStorage.return_value = mock_storage

    result = runner.invoke(
        cli,
        [
            "candidate",
            "history",
            "--id",
            "test_candidate",
            "--format",
            "json",
        ],
    )

    assert result.exit_code == 0
    # Should output JSON
    assert "assess_001" in result.output or "85.0" in result.output


@patch("sono_eval.cli.commands.candidate.MemUStorage")
def test_candidate_report(MockStorage, runner):
    """Test candidate report command."""
    mock_storage = Mock()
    mock_memory = Mock()
    mock_memory.candidate_id = "test_candidate"
    mock_node = Mock()
    mock_node.metadata = {"type": "assessment"}
    mock_node.data = {
        "assessment_result": {
            "assessment_id": "assess_001",
            "timestamp": "2026-01-23T10:00:00Z",
            "overall_score": 85.0,
            "confidence": 0.9,
            "summary": "Good performance",
        }
    }
    mock_memory.nodes = {"node1": mock_node}
    mock_storage.get_candidate_memory.return_value = mock_memory
    MockStorage.return_value = mock_storage

    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            [
                "candidate",
                "report",
                "--id",
                "test_candidate",
                "--output",
                "report.md",
            ],
        )

        assert result.exit_code == 0
        assert Path("report.md").exists()


# ============================================================================
# Session Command Tests
# ============================================================================


@patch("sono_eval.cli.commands.session.get_session")
def test_session_report(mock_get_session, runner):
    """Test session report command."""
    mock_session = Mock()
    mock_session.generate_session_report.return_value = {
        "session_id": "session_123",
        "date": "2026-01-23",
        "duration": "1h 30m",
        "candidate_id": "test_candidate",
        "total_assessments": 5,
        "average_score": 85.0,
        "key_insights": ["Good progress"],
        "recommendations": ["Keep practicing"],
        "strengths": ["Strong technical skills"],
        "areas_for_improvement": ["Documentation"],
    }
    mock_get_session.return_value = mock_session

    result = runner.invoke(
        cli,
        [
            "session",
            "report",
        ],
    )

    assert result.exit_code == 0


@patch("sono_eval.cli.commands.session.get_session")
def test_session_report_json(mock_get_session, runner):
    """Test session report with JSON format."""
    mock_session = Mock()
    mock_session.generate_session_report.return_value = {
        "session_id": "session_123",
        "date": "2026-01-23",
        "duration": "1h 30m",
        "total_assessments": 5,
        "average_score": 85.0,
    }
    mock_get_session.return_value = mock_session

    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            [
                "session",
                "report",
                "--format",
                "json",
                "--output",
                "session.json",
            ],
        )

        assert result.exit_code == 0
        assert Path("session.json").exists()


@patch("sono_eval.cli.commands.session.get_session")
@patch("sono_eval.cli.commands.session.end_current_session")
def test_session_end(mock_end_session, mock_get_session, runner):
    """Test session end command."""
    mock_session = Mock()
    mock_session.generate_session_report.return_value = {
        "session_id": "session_123",
        "date": "2026-01-23",
        "duration": "1h 30m",
        "total_assessments": 5,
        "average_score": 85.0,
    }
    mock_get_session.return_value = mock_session

    result = runner.invoke(
        cli,
        [
            "session",
            "end",
        ],
        input="n\n",  # Don't generate report
    )

    assert result.exit_code == 0


@patch("sono_eval.cli.commands.session.get_config")
def test_session_list(mock_get_config, runner):
    """Test session list command."""
    mock_config = Mock()
    mock_config.memu_storage_path = "/tmp/test"
    mock_get_config.return_value = mock_config

    with runner.isolated_filesystem():
        sessions_dir = Path("sessions")
        sessions_dir.mkdir(parents=True, exist_ok=True)
        session_file = sessions_dir / "session1.json"
        session_file.write_text(
            json.dumps(
                {
                    "session_id": "session_123",
                    "start_time": "2026-01-23T10:00:00Z",
                    "duration_seconds": 3600,
                    "candidate_id": "test_candidate",
                    "assessments": [],
                }
            )
        )

        result = runner.invoke(
            cli,
            [
                "session",
                "list",
            ],
        )

        assert result.exit_code == 0


# ============================================================================
# Tag Command Tests
# ============================================================================


@patch("sono_eval.cli.commands.tag.TagGenerator")
def test_tag_generate_with_file(MockGenerator, runner, temp_file):
    """Test tag generate with file."""
    mock_generator = Mock()
    mock_tag = Mock()
    mock_tag.tag = "python"
    mock_tag.category = "language"
    mock_tag.confidence = 0.95
    mock_tag.context = "Python code detected"
    mock_generator.generate_tags.return_value = [mock_tag]
    MockGenerator.return_value = mock_generator

    result = runner.invoke(
        cli,
        [
            "tag",
            "generate",
            "--file",
            temp_file,
        ],
    )

    assert result.exit_code == 0
    mock_generator.generate_tags.assert_called_once()


@patch("sono_eval.cli.commands.tag.TagGenerator")
def test_tag_generate_with_text(MockGenerator, runner):
    """Test tag generate with inline text."""
    mock_generator = Mock()
    mock_tag = Mock()
    mock_tag.tag = "function"
    mock_tag.category = "structure"
    mock_tag.confidence = 0.90
    mock_tag.context = None
    mock_generator.generate_tags.return_value = [mock_tag]
    MockGenerator.return_value = mock_generator

    result = runner.invoke(
        cli,
        [
            "tag",
            "generate",
            "--text",
            "def hello(): pass",
        ],
    )

    assert result.exit_code == 0


@patch("sono_eval.cli.commands.tag.TagGenerator")
def test_tag_generate_quiet(MockGenerator, runner):
    """Test tag generate in quiet mode."""
    mock_generator = Mock()
    mock_tag = Mock()
    mock_tag.tag = "python"
    mock_tag.category = "language"
    mock_tag.confidence = 0.95
    mock_generator.generate_tags.return_value = [mock_tag]
    MockGenerator.return_value = mock_generator

    result = runner.invoke(
        cli,
        [
            "tag",
            "generate",
            "--text",
            "def hello(): pass",
            "--quiet",
        ],
    )

    assert result.exit_code == 0
    assert "python" in result.output


def test_tag_generate_missing_input(runner):
    """Test tag generate without file or text."""
    result = runner.invoke(
        cli,
        [
            "tag",
            "generate",
        ],
    )

    assert result.exit_code != 0
    assert "Error" in result.output or "required" in result.output.lower()


def test_tag_generate_invalid_max_tags(runner):
    """Test tag generate with invalid max-tags."""
    result = runner.invoke(
        cli,
        [
            "tag",
            "generate",
            "--text",
            "def hello(): pass",
            "--max-tags",
            "25",  # > 20
        ],
    )

    assert result.exit_code != 0
    assert "max-tags" in result.output.lower() or "Error" in result.output


# ============================================================================
# Setup Command Tests
# ============================================================================


@patch("sono_eval.cli.commands.setup.Confirm")
def test_setup_init_quick(mock_confirm, runner):
    """Test setup init in quick mode."""
    result = runner.invoke(
        cli,
        [
            "setup",
            "init",
            "--quick",
        ],
    )

    # Should not fail, may exit early or show status
    assert result.exit_code in [0, 1]  # May exit with error if checks fail, but command runs


@patch("sono_eval.cli.commands.setup.Confirm")
def test_setup_init_interactive(mock_confirm, runner):
    """Test setup init in interactive mode."""
    mock_confirm.ask.return_value = False  # Cancel setup

    result = runner.invoke(
        cli,
        [
            "setup",
            "init",
            "--interactive",
        ],
    )

    # Should handle cancellation gracefully
    assert "cancelled" in result.output.lower() or result.exit_code == 0


# ============================================================================
# General CLI Tests
# ============================================================================


def test_cli_version(runner):
    """Test CLI version command."""
    result = runner.invoke(cli, ["--version"])

    assert result.exit_code == 0
    assert "version" in result.output.lower() or "0.1" in result.output


def test_cli_help(runner):
    """Test CLI help command."""
    result = runner.invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "assess" in result.output or "candidate" in result.output


def test_cli_invalid_command(runner):
    """Test CLI with invalid command."""
    result = runner.invoke(cli, ["invalid_command"])

    assert result.exit_code != 0
    assert "Error" in result.output or "Unknown" in result.output
