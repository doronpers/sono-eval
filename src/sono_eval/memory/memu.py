"""
MemU: Persistent Hierarchical Memory Storage for Candidates.

Implements hierarchical memory with efficient storage and retrieval.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from sono_eval.utils.config import get_config
from sono_eval.utils.logger import get_logger

logger = get_logger(__name__)


class MemoryNode(BaseModel):
    """Node in the hierarchical memory structure."""
    node_id: str
    parent_id: Optional[str] = None
    level: int = 0
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    data: Dict[str, Any] = Field(default_factory=dict)
    children: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CandidateMemory(BaseModel):
    """Complete memory structure for a candidate."""
    candidate_id: str
    root_node: MemoryNode
    nodes: Dict[str, MemoryNode] = Field(default_factory=dict)
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0"


class MemUStorage:
    """
    Persistent hierarchical memory storage.
    
    Features:
    - Hierarchical structure with configurable depth
    - Efficient storage and retrieval
    - Version control for memory snapshots
    - Caching for frequently accessed data
    """

    def __init__(self, storage_path: Optional[Path] = None):
        """Initialize MemU storage."""
        self.config = get_config()
        self.storage_path = storage_path or self.config.get_storage_path()
        self.max_depth = self.config.memu_max_depth
        self.cache_size = self.config.memu_cache_size
        self._cache: Dict[str, CandidateMemory] = {}
        
        # Ensure storage directory exists
        self.storage_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Initialized MemU storage at {self.storage_path}")

    def create_candidate_memory(
        self, candidate_id: str, initial_data: Optional[Dict[str, Any]] = None
    ) -> CandidateMemory:
        """
        Create new memory structure for a candidate.

        Args:
            candidate_id: Unique candidate identifier
            initial_data: Optional initial data

        Returns:
            New CandidateMemory instance
        """
        logger.info(f"Creating memory for candidate {candidate_id}")
        
        root_node = MemoryNode(
            node_id=f"{candidate_id}_root",
            level=0,
            data=initial_data or {},
        )

        memory = CandidateMemory(
            candidate_id=candidate_id,
            root_node=root_node,
            nodes={root_node.node_id: root_node},
        )

        self._save_memory(memory)
        self._cache[candidate_id] = memory

        return memory

    def get_candidate_memory(self, candidate_id: str) -> Optional[CandidateMemory]:
        """
        Retrieve candidate memory from storage or cache.

        Args:
            candidate_id: Candidate identifier

        Returns:
            CandidateMemory if found, None otherwise
        """
        # Check cache first
        if candidate_id in self._cache:
            logger.debug(f"Retrieved {candidate_id} from cache")
            return self._cache[candidate_id]

        # Load from disk
        memory = self._load_memory(candidate_id)
        if memory:
            # Add to cache
            self._cache[candidate_id] = memory
            # Manage cache size
            if len(self._cache) > self.cache_size:
                # Remove oldest entry
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
        
        return memory

    def add_memory_node(
        self,
        candidate_id: str,
        parent_id: str,
        data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[MemoryNode]:
        """
        Add a new memory node to the hierarchy.

        Args:
            candidate_id: Candidate identifier
            parent_id: Parent node identifier
            data: Node data
            metadata: Optional metadata

        Returns:
            Created MemoryNode if successful
        """
        memory = self.get_candidate_memory(candidate_id)
        if not memory:
            logger.error(f"Memory not found for candidate {candidate_id}")
            return None

        # Check if parent exists
        if parent_id not in memory.nodes:
            logger.error(f"Parent node {parent_id} not found")
            return None

        parent_node = memory.nodes[parent_id]

        # Check depth limit
        if parent_node.level >= self.max_depth - 1:
            logger.warning(f"Max depth {self.max_depth} reached")
            return None

        # Create new node
        node_id = f"{candidate_id}_{len(memory.nodes)}"
        new_node = MemoryNode(
            node_id=node_id,
            parent_id=parent_id,
            level=parent_node.level + 1,
            data=data,
            metadata=metadata or {},
        )

        # Update parent's children
        parent_node.children.append(node_id)

        # Add to memory
        memory.nodes[node_id] = new_node
        memory.last_updated = datetime.utcnow()

        # Save
        self._save_memory(memory)

        logger.info(f"Added node {node_id} to {candidate_id}")
        return new_node

    def update_memory_node(
        self, candidate_id: str, node_id: str, data: Dict[str, Any]
    ) -> bool:
        """
        Update data in an existing memory node.

        Args:
            candidate_id: Candidate identifier
            node_id: Node identifier
            data: Updated data

        Returns:
            True if successful
        """
        memory = self.get_candidate_memory(candidate_id)
        if not memory or node_id not in memory.nodes:
            return False

        memory.nodes[node_id].data.update(data)
        memory.nodes[node_id].timestamp = datetime.utcnow()
        memory.last_updated = datetime.utcnow()

        self._save_memory(memory)
        logger.info(f"Updated node {node_id} for {candidate_id}")
        return True

    def get_node_path(
        self, candidate_id: str, node_id: str
    ) -> List[MemoryNode]:
        """
        Get the path from root to specified node.

        Args:
            candidate_id: Candidate identifier
            node_id: Target node identifier

        Returns:
            List of nodes from root to target
        """
        memory = self.get_candidate_memory(candidate_id)
        if not memory or node_id not in memory.nodes:
            return []

        path = []
        current_id = node_id
        
        while current_id:
            node = memory.nodes[current_id]
            path.insert(0, node)
            current_id = node.parent_id

        return path

    def _save_memory(self, memory: CandidateMemory) -> None:
        """Save memory to disk."""
        file_path = self.storage_path / f"{memory.candidate_id}.json"
        with open(file_path, "w") as f:
            json.dump(memory.model_dump(mode="json"), f, indent=2, default=str)
        logger.debug(f"Saved memory to {file_path}")

    def _load_memory(self, candidate_id: str) -> Optional[CandidateMemory]:
        """Load memory from disk."""
        file_path = self.storage_path / f"{candidate_id}.json"
        if not file_path.exists():
            logger.debug(f"Memory file not found: {file_path}")
            return None

        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            memory = CandidateMemory.model_validate(data)
            logger.debug(f"Loaded memory from {file_path}")
            return memory
        except Exception as e:
            logger.error(f"Error loading memory: {e}")
            return None

    def list_candidates(self) -> List[str]:
        """List all candidate IDs in storage."""
        candidates = []
        for file_path in self.storage_path.glob("*.json"):
            candidates.append(file_path.stem)
        return sorted(candidates)

    def delete_candidate_memory(self, candidate_id: str) -> bool:
        """
        Delete candidate memory from storage.

        Args:
            candidate_id: Candidate identifier

        Returns:
            True if successful
        """
        file_path = self.storage_path / f"{candidate_id}.json"
        if file_path.exists():
            file_path.unlink()
            if candidate_id in self._cache:
                del self._cache[candidate_id]
            logger.info(f"Deleted memory for {candidate_id}")
            return True
        return False
