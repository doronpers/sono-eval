import sys
from pathlib import Path
from typing import Any, Dict

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
