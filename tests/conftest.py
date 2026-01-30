import sys
from pathlib import Path
from typing import Any, Dict
from unittest.mock import MagicMock

# Mock optional third-party modules before any imports that depend on them
for _mod_name in ["council_ai", "celery", "celery.result", "shared_ai_utils"]:
    if _mod_name not in sys.modules:
        sys.modules[_mod_name] = MagicMock()

import pytest

# Add src to python path for tests
src_path = str(Path(__file__).parent.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)


@pytest.fixture
def sample_code_simple() -> str:
    """Simple valid code for testing."""
    return "def hello(): return 'world'"


@pytest.fixture
def sample_code_with_violations() -> str:
    """Code with pattern violations for testing."""
    return """
def process_data(data):
    try:
        result = data[0]  # No bounds checking
        print(result)  # Using print instead of logging
    except:  # Bare except clause
        pass
    return result
"""


@pytest.fixture
def sample_code_complex() -> str:
    """More complex code for testing."""
    return """
class Calculator:
    '''A simple calculator class.'''

    def add(self, a: int, b: int) -> int:
        '''Add two numbers.'''
        return a + b

    def multiply(self, a: int, b: int) -> int:
        '''Multiply two numbers.'''
        return a * b
"""


@pytest.fixture
def sample_assessment_metadata() -> Dict[str, Any]:
    """Sample assessment metadata for testing."""
    return {
        "candidate_id": "test_candidate_001",
        "submission_type": "code",
        "timestamp": "2024-01-15T10:30:00Z",
        "session_id": "test_session_123",
    }


@pytest.fixture
def mock_request_id() -> str:
    """Mock request ID for testing."""
    return "req_test_12345"


# CLI Testing Fixtures


@pytest.fixture
def cli_runner():
    """Provide a Click CliRunner for testing CLI commands."""
    from click.testing import CliRunner

    return CliRunner()


@pytest.fixture
def mock_assessment_result():
    """Mock assessment result for testing."""
    from sono_eval.assessment.models import (
        AssessmentResult,
        MetricScore,
        PathScore,
        PathType,
    )

    return AssessmentResult(
        candidate_id="test_candidate",
        assessment_id="assess_12345",
        overall_score=85.0,
        confidence=0.9,
        summary="Strong technical skills demonstrated",
        path_scores=[
            PathScore(
                path=PathType.TECHNICAL,
                overall_score=85.0,
                confidence=0.9,
                metrics=[
                    MetricScore(
                        name="code_quality",
                        value=85.0,
                        weight=1.0,
                        evidence=["Good code structure"],
                    )
                ],
                strengths=["Clean code", "Good patterns"],
                areas_for_growth=["Documentation"],
            )
        ],
        key_findings=["Strong foundation", "Good practices"],
        recommendations=["Add more tests", "Improve docs"],
    )


@pytest.fixture
def mock_candidate_memory():
    """Mock candidate memory for testing."""
    from sono_eval.memory.memu import CandidateMemory, MemoryNode

    root_node = MemoryNode(
        node_id="root_123",
        data={"name": "Test Candidate"},
        metadata={},
        children=[],
    )

    return CandidateMemory(
        candidate_id="test_candidate",
        root_node=root_node,
        nodes={"root_123": root_node},
        last_updated="2024-01-15T10:30:00Z",
        version="1.0.0",
    )


@pytest.fixture
def temp_code_file(tmp_path):
    """Create a temporary code file for testing."""
    code_file = tmp_path / "test_code.py"
    code_file.write_text(
        """
def hello_world():
    return "Hello, World!"

class Calculator:
    def add(self, a, b):
        return a + b
"""
    )
    return str(code_file)


@pytest.fixture
def empty_file(tmp_path):
    """Create an empty file for testing."""
    empty_file = tmp_path / "empty.py"
    empty_file.write_text("")
    return str(empty_file)
