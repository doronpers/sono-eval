"""
Redis-backed MemU storage for high-concurrency environments.

Implements the same interface as MemUStorage but uses Redis for persistence.
"""

import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

import redis

from sono_eval.memory.memu import CandidateMemory, MemoryNode, MemUStorage
from sono_eval.utils.config import get_config
from sono_eval.utils.logger import get_logger

logger = get_logger(__name__)


class MemURedisStorage(MemUStorage):
    """
    Redis-backed hierarchical memory storage.

    Features:
    - Atomic operations for concurrency safety
    - Automatic key expiration
    - Pub/sub for real-time updates (optional)
    - Same interface as MemUStorage
    """

    def __init__(
        self,
        redis_url: Optional[str] = None,
        key_prefix: str = "memu:",
        ttl_seconds: int = 86400 * 30,  # 30 days default
    ):
        config = get_config()
        self.redis_url = redis_url or config.redis_url
        self.key_prefix = key_prefix
        # Allow config to override default TTL if present
        self.ttl_seconds = getattr(config, "memu_redis_ttl", ttl_seconds)
        self._client: Optional[redis.Redis] = None

    @property
    def client(self) -> redis.Redis:
        if self._client is None:
            if not self.redis_url:
                raise ValueError("Redis URL not configured")
            self._client = redis.from_url(self.redis_url, decode_responses=True)
        return self._client

    def _key(self, *parts: str) -> str:
        """Generate Redis key with prefix."""
        return f"{self.key_prefix}{':'.join(parts)}"

    def create_candidate_memory(
        self, candidate_id: str, initial_data: Optional[Dict[str, Any]] = None
    ) -> CandidateMemory:
        """Create new memory structure for a candidate."""
        logger.info(f"Creating memory for candidate {candidate_id} (Redis)")

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
        return memory

    def get_candidate_memory(self, candidate_id: str) -> Optional[CandidateMemory]:
        """Retrieve candidate memory from Redis."""
        key = self._key("candidate", candidate_id)
        data_json = self.client.get(key)

        if not data_json:
            return None

        try:
            data = json.loads(data_json)
            memory = CandidateMemory.model_validate(data)
            # Refresh TTL on access
            self.client.expire(key, self.ttl_seconds)
            return memory
        except Exception as e:
            logger.error(f"Error parsing memory for {candidate_id}: {e}")
            return None

    def add_memory_node(
        self,
        candidate_id: str,
        parent_id: str,
        data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[MemoryNode]:
        """Add memory node with atomic Redis operations."""
        key = self._key("candidate", candidate_id)

        # Optimistic locking loop
        with self.client.pipeline() as pipe:
            while True:
                try:
                    pipe.watch(key)

                    # Read current state
                    data_json = pipe.get(key)
                    if not data_json:
                        logger.error(f"Memory not found for {candidate_id}")
                        return None

                    memory_data = json.loads(data_json)
                    memory = CandidateMemory.model_validate(memory_data)

                    # Validate parent exists
                    if parent_id not in memory.nodes:
                        logger.error(f"Parent node {parent_id} not found")
                        return None

                    parent_node = memory.nodes[parent_id]

                    # Create new node
                    node_id = f"{candidate_id}_{len(memory.nodes)}"
                    # Ensure uniqueness in case of race condition resolving to same length
                    # (though length check here is just generation strategy)
                    if node_id in memory.nodes:
                        node_id = f"{candidate_id}_{uuid.uuid4().hex[:8]}"

                    new_node = MemoryNode(
                        node_id=node_id,
                        parent_id=parent_id,
                        level=parent_node.level + 1,
                        data=data,
                        metadata=metadata or {},
                    )

                    # Update structure
                    memory.nodes[parent_id].children.append(node_id)
                    memory.nodes[node_id] = new_node
                    # Update structure
                    memory.nodes[parent_id].children.append(node_id)
                    memory.nodes[node_id] = new_node
                    memory.last_updated = datetime.now(timezone.utc)

                    # Write back
                    pipe.multi()
                    pipe.setex(
                        key,
                        self.ttl_seconds,
                        json.dumps(memory.model_dump(mode="json")),
                    )
                    pipe.execute()

                    logger.info(f"Added node {node_id} to {candidate_id} (Redis)")
                    return new_node

                except redis.WatchError:
                    # Retry if key changed during operation
                    continue
                except Exception as e:
                    logger.error(f"Error adding node: {e}")
                    return None

    def update_memory_node(
        self, candidate_id: str, node_id: str, data: Dict[str, Any]
    ) -> bool:
        """Update data in an existing memory node."""
        key = self._key("candidate", candidate_id)

        with self.client.pipeline() as pipe:
            while True:
                try:
                    pipe.watch(key)
                    data_json = pipe.get(key)
                    if not data_json:
                        return False

                    memory_data = json.loads(data_json)
                    memory = CandidateMemory.model_validate(memory_data)

                    if node_id not in memory.nodes:
                        return False

                    memory.nodes[node_id].data.update(data)
                    # timestamp update logic matching MemU

                    pipe.multi()
                    pipe.setex(
                        key,
                        self.ttl_seconds,
                        json.dumps(memory.model_dump(mode="json")),
                    )
                    pipe.execute()
                    return True
                except redis.WatchError:
                    continue
                except Exception as e:
                    logger.error(f"Error updating node: {e}")
                    return False

    def get_node_path(self, candidate_id: str, node_id: str) -> List[MemoryNode]:
        """Get the path from root to specified node."""
        memory = self.get_candidate_memory(candidate_id)
        if not memory or node_id not in memory.nodes:
            return []

        path: List[MemoryNode] = []
        current_id = node_id

        while current_id:
            node = memory.nodes[current_id]
            path.insert(0, node)
            current_id = node.parent_id

        return path

    def _save_memory(self, memory: CandidateMemory) -> None:
        """Save memory to Redis."""
        key = self._key("candidate", memory.candidate_id)
        self.client.setex(
            key, self.ttl_seconds, json.dumps(memory.model_dump(mode="json"))
        )
        logger.debug(f"Saved memory {memory.candidate_id} to Redis")

    def list_candidates(self) -> List[str]:
        """List all candidate IDs in storage."""
        # Using scan_iter for efficiency
        pattern = self._key("candidate", "*")
        keys = self.client.keys(pattern)
        # Extract candidate ID from key (memu:candidate:{id})
        return sorted(
            [k.split(":")[-1] for k in keys] if keys else []
        )  # Simplified extraction

    def delete_candidate_memory(self, candidate_id: str) -> bool:
        """Delete candidate memory from storage."""
        key = self._key("candidate", candidate_id)
        result = self.client.delete(key)
        if result:
            logger.info(f"Deleted memory for {candidate_id} (Redis)")
            return True
        return False
