"""Tests for mobile session management."""

from unittest.mock import MagicMock, patch

import pytest

from sono_eval.memory.memu import CandidateMemory, MemoryNode
from sono_eval.mobile.session import MobileSessionManager


@pytest.fixture
def mock_storage():
    with patch("sono_eval.mobile.session.MemUStorage") as MockStorage:
        storage_instance = MockStorage.return_value
        yield storage_instance


def test_create_session(mock_storage):
    """Test creating a new session."""
    manager = MobileSessionManager()
    session_id = manager.create_session("test_candidate")

    assert session_id is not None
    mock_storage.create_candidate_memory.assert_called_once()
    call_args = mock_storage.create_candidate_memory.call_args
    assert call_args.kwargs["candidate_id"] == f"session_{session_id}"
    assert call_args.kwargs["initial_data"]["candidate_id"] == "test_candidate"


def test_get_session_found(mock_storage):
    """Test retrieving an existing session."""
    manager = MobileSessionManager()
    session_id = "12345"

    # Mock return value
    mock_memory = MagicMock(spec=CandidateMemory)
    mock_memory.root_node = MagicMock(spec=MemoryNode)
    # Use real dict for data to avoid parsing issues if validation happens,
    # but here we just return dict structure
    mock_memory.root_node.data = {
        "session_id": session_id,
        "candidate_id": "guest",
        "current_step": 2,
        "selected_paths": ["technical"],
        "answers": {},
        # Add basic datetime strings if needed by parser, generally pydantic handles it
    }
    mock_storage.get_candidate_memory.return_value = mock_memory

    session = manager.get_session(session_id)

    assert session is not None
    assert session.session_id == session_id
    assert session.current_step == 2
    mock_storage.get_candidate_memory.assert_called_with(f"session_{session_id}")


def test_get_session_not_found(mock_storage):
    """Test retrieving a non-existent session."""
    manager = MobileSessionManager()
    mock_storage.get_candidate_memory.return_value = None

    session = manager.get_session("missing")
    assert session is None


def test_update_step(mock_storage):
    """Test updating session step."""
    manager = MobileSessionManager()
    session_id = "12345"

    # Setup mock to return session first
    mock_memory = MagicMock(spec=CandidateMemory)
    mock_memory.root_node = MagicMock(spec=MemoryNode)
    mock_memory.root_node.data = {
        "session_id": session_id,
        "candidate_id": "guest",
        "current_step": 1,
    }
    mock_storage.get_candidate_memory.return_value = mock_memory

    # Perform update
    success = manager.update_step(session_id, 3)

    assert success is True
    # Verify update called
    mock_storage.update_memory_node.assert_called_once()
    call_args = mock_storage.update_memory_node.call_args
    assert call_args.kwargs["candidate_id"] == f"session_{session_id}"
    assert call_args.kwargs["data"]["current_step"] == 3
