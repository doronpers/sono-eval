"""Tests for the MemU storage system."""

import pytest

from sono_eval.memory.memu import MemUStorage


@pytest.fixture
def temp_storage(tmp_path):
    """Create temporary storage for testing."""
    return MemUStorage(storage_path=tmp_path / "test_memory")


def test_storage_initialization(temp_storage):
    """Test that storage initializes correctly."""
    assert temp_storage is not None
    assert temp_storage.storage_path.exists()


def test_create_candidate_memory(temp_storage):
    """Test creating candidate memory."""
    memory = temp_storage.create_candidate_memory(
        "test_candidate_001", initial_data={"name": "Test User"}
    )

    assert memory is not None
    assert memory.candidate_id == "test_candidate_001"
    assert memory.root_node is not None
    assert memory.root_node.data["name"] == "Test User"


def test_retrieve_candidate_memory(temp_storage):
    """Test retrieving candidate memory."""
    # Create memory
    temp_storage.create_candidate_memory("test_candidate_002")

    # Retrieve memory
    memory = temp_storage.get_candidate_memory("test_candidate_002")

    assert memory is not None
    assert memory.candidate_id == "test_candidate_002"


def test_add_memory_node(temp_storage):
    """Test adding nodes to memory hierarchy."""
    memory = temp_storage.create_candidate_memory("test_candidate_003")

    # Add child node
    node = temp_storage.add_memory_node(
        "test_candidate_003",
        memory.root_node.node_id,
        data={"assessment": "result_1"},
        metadata={"type": "assessment"},
    )

    assert node is not None
    assert node.parent_id == memory.root_node.node_id
    assert node.level == 1
    assert node.data["assessment"] == "result_1"


def test_update_memory_node(temp_storage):
    """Test updating memory node data."""
    memory = temp_storage.create_candidate_memory("test_candidate_004")

    # Update root node
    success = temp_storage.update_memory_node(
        "test_candidate_004", memory.root_node.node_id, data={"updated": True}
    )

    assert success

    # Verify update
    updated_memory = temp_storage.get_candidate_memory("test_candidate_004")
    assert updated_memory.root_node.data["updated"] is True


def test_get_node_path(temp_storage):
    """Test retrieving path from root to node."""
    memory = temp_storage.create_candidate_memory("test_candidate_005")

    # Add nested nodes
    child1 = temp_storage.add_memory_node(
        "test_candidate_005", memory.root_node.node_id, data={"level": 1}
    )

    child2 = temp_storage.add_memory_node(
        "test_candidate_005", child1.node_id, data={"level": 2}
    )

    # Get path
    path = temp_storage.get_node_path("test_candidate_005", child2.node_id)

    assert len(path) == 3  # root + 2 children
    assert path[0].level == 0
    assert path[1].level == 1
    assert path[2].level == 2


def test_list_candidates(temp_storage):
    """Test listing all candidates."""
    # Create multiple candidates
    temp_storage.create_candidate_memory("candidate_a")
    temp_storage.create_candidate_memory("candidate_b")
    temp_storage.create_candidate_memory("candidate_c")

    candidates = temp_storage.list_candidates()

    assert len(candidates) == 3
    assert "candidate_a" in candidates
    assert "candidate_b" in candidates
    assert "candidate_c" in candidates


def test_delete_candidate_memory(temp_storage):
    """Test deleting candidate memory."""
    temp_storage.create_candidate_memory("test_candidate_006")

    # Delete
    success = temp_storage.delete_candidate_memory("test_candidate_006")
    assert success

    # Verify deletion
    memory = temp_storage.get_candidate_memory("test_candidate_006")
    assert memory is None


def test_max_depth_limit(temp_storage):
    """Test that max depth is enforced."""
    memory = temp_storage.create_candidate_memory("test_candidate_007")

    # Try to create nodes beyond max depth
    current_id = memory.root_node.node_id
    nodes_created = []

    for i in range(temp_storage.max_depth + 2):
        node = temp_storage.add_memory_node(
            "test_candidate_007", current_id, data={"level": i + 1}
        )
        if node:
            nodes_created.append(node)
            current_id = node.node_id
        else:
            break

    # Should not exceed max_depth
    assert len(nodes_created) <= temp_storage.max_depth
