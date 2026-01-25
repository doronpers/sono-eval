"""
Migrate existing filesystem MemU data to Redis.

Reads all JSON files from the data directory and writes them to the configured Redis instance.
"""

import json
import asyncio
from pathlib import Path
import sys

from sono_eval.utils.config import get_config
from sono_eval.utils.logger import get_logger
from sono_eval.memory.memu import MemUStorage
from sono_eval.memory.memu_redis import MemURedisStorage

logger = get_logger(__name__)


def migrate():
    """Execute migration."""
    config = get_config()

    if not config.redis_url:
        logger.error("REDIS_URL not configured. Cannot migrate.")
        sys.exit(1)

    logger.info("Starting migration from Filesystem to Redis...")

    # Initialize storages
    fs_storage = MemUStorage()  # Will use configured path

    try:
        redis_storage = MemURedisStorage(redis_url=config.redis_url)
        # Test connection
        redis_storage.client.ping()
        logger.info("Connected to Redis")
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        sys.exit(1)

    # List all candidates
    candidates = fs_storage.list_candidates()
    logger.info(f"Found {len(candidates)} candidates to migrate")

    success_count = 0
    fail_count = 0

    for candidate_id in candidates:
        try:
            logger.info(f"Migrating {candidate_id}...")
            # Load from FS
            memory = fs_storage.get_candidate_memory(candidate_id)
            if not memory:
                logger.warning(f"Could not load memory for {candidate_id}")
                fail_count += 1
                continue

            # Save to Redis (using internal save method to force overwrite)
            redis_storage._save_memory(memory)
            success_count += 1

        except Exception as e:
            logger.error(f"Error migrating {candidate_id}: {e}")
            fail_count += 1

    logger.info(f"Migration complete. Success: {success_count}, Failed: {fail_count}")


if __name__ == "__main__":
    migrate()
