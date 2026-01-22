"""
Memory module initialization.

Exports main MemU components and factory function.
"""

from sono_eval.memory.memu import CandidateMemory, MemoryNode, MemUStorage
from sono_eval.utils.config import get_config

__all__ = ["CandidateMemory", "MemoryNode", "MemUStorage", "get_storage"]


def get_storage():
    """Get appropriate storage backend based on configuration."""
    config = get_config()

    # Check if configured for Redis
    # We use getattr to safely check for attributes that might be added to config later
    memu_backend = getattr(config, "memu_backend", "filesystem")
    redis_url = getattr(config, "redis_url", None)

    if memu_backend == "redis" and redis_url:
        from sono_eval.memory.memu_redis import MemURedisStorage

        return MemURedisStorage(redis_url=redis_url)
    else:
        return MemUStorage()
