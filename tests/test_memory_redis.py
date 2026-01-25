"""Tests for Redis-backed MemU storage."""

import json
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

from sono_eval.memory.memu_redis import MemURedisStorage
from sono_eval.memory.memu import CandidateMemory

# Skip tests if redis not installed or not configured
try:
    import redis

    redis_installed = True
except ImportError:
    redis_installed = False


@pytest.fixture
def mock_redis():
    """Mock Redis client."""
    mock = MagicMock()
    # Setup pipeline mock
    pipeline = MagicMock()
    pipeline.__enter__.return_value = pipeline
    mock.pipeline.return_value = pipeline
    return mock


@pytest.fixture
def redis_storage(mock_redis):
    """Create storage with mocked redis."""
    with patch("sono_eval.memory.memu_redis.redis.from_url", return_value=mock_redis):
        storage = MemURedisStorage(redis_url="redis://localhost:6379/0")
        # Ensure client is initialized while patch is active
        _ = storage.client
        yield storage


def test_init_validation():
    """Test initialization requires redis_url."""
    # Should raise error if accessed without URL
    with patch("sono_eval.memory.memu_redis.get_config") as mock_get_config:
        mock_config = MagicMock()
        mock_config.redis_url = None
        mock_config.memu_redis_ttl = 30
        mock_get_config.return_value = mock_config

        storage = MemURedisStorage(redis_url=None)
        with pytest.raises(ValueError):
            _ = storage.client


def test_create_candidate_memory(redis_storage, mock_redis):
    """Test creating candidate memory."""
    memory = redis_storage.create_candidate_memory("user123", {"initial": "data"})

    assert memory.candidate_id == "user123"
    assert "user123_root" in memory.nodes

    # Verify setex called
    mock_redis.setex.assert_called_once()
    args = mock_redis.setex.call_args
    assert args[0][0] == "memu:candidate:user123"
    assert args[0][1] == 2592000  # Default TTL


def test_get_candidate_memory_hit(redis_storage, mock_redis):
    """Test memory retrieval cache hit."""
    # Setup mock data
    mock_data = {
        "candidate_id": "user123",
        "root_node": {
            "node_id": "user123_root",
            "level": 0,
            "data": {},
            "children": [],
            "metadata": {},
            "timestamp": "2024-01-01T00:00:00Z",
        },
        "nodes": {
            "user123_root": {
                "node_id": "user123_root",
                "level": 0,
                "data": {},
                "children": [],
                "metadata": {},
                "timestamp": "2024-01-01T00:00:00Z",
            }
        },
        "last_updated": "2024-01-01T00:00:00Z",
        "version": "1.0",
    }

    mock_redis.get.return_value = json.dumps(mock_data)

    memory = redis_storage.get_candidate_memory("user123")

    assert memory is not None
    assert memory.candidate_id == "user123"
    # Verify TTL refresh
    mock_redis.expire.assert_called_once()


def test_get_candidate_memory_miss(redis_storage, mock_redis):
    """Test memory retrieval cache miss."""
    mock_redis.get.return_value = None
    memory = redis_storage.get_candidate_memory("user123")
    assert memory is None


def test_add_memory_node(redis_storage, mock_redis):
    """Test adding node with optimistic locking."""
    # Setup mock data for pipeline get
    mock_pipeline = mock_redis.pipeline.return_value

    # Existing memory state
    mock_data = {
        "candidate_id": "user123",
        "root_node": {
            "node_id": "user123_root",
            "level": 0,
            "data": {},
            "children": [],
            "metadata": {},
            "timestamp": "2024-01-01T00:00:00Z",
        },
        "nodes": {
            "user123_root": {
                "node_id": "user123_root",
                "level": 0,
                "data": {},
                "children": [],
                "metadata": {},
                "timestamp": "2024-01-01T00:00:00Z",
            }
        },
        "last_updated": "2024-01-01T00:00:00Z",
        "version": "1.0",
    }

    mock_pipeline.get.return_value = json.dumps(mock_data)

    new_node = redis_storage.add_memory_node("user123", "user123_root", {"new": "info"})

    assert new_node is not None
    assert new_node.parent_id == "user123_root"

    # Verify watch called
    mock_pipeline.watch.assert_called()
    # Verify transaction executed
    mock_pipeline.execute.assert_called()


def test_delete_candidate_memory(redis_storage, mock_redis):
    """Test deletion."""
    mock_redis.delete.return_value = 1
    result = redis_storage.delete_candidate_memory("user123")
    assert result is True
    mock_redis.delete.assert_called_with("memu:candidate:user123")
