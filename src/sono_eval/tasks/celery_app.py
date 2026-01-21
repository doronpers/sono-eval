"""
Celery application configuration for async task processing.
"""

from celery import Celery

from sono_eval.utils.config import get_config
from sono_eval.utils.logger import get_logger

logger = get_logger(__name__)

config = get_config()

# Configure Celery app
celery_app = Celery(
    "sono_eval",
    broker=config.celery_broker_url,
    backend=config.celery_result_backend,
    include=["sono_eval.tasks.assessment"],
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes max per task
    task_soft_time_limit=25 * 60,  # 25 minutes soft limit
    worker_prefetch_multiplier=1,  # Fetch one task at a time
    worker_max_tasks_per_child=100,  # Restart worker after 100 tasks
    result_expires=3600,  # Results expire after 1 hour
    task_acks_late=True,  # Acknowledge task after completion
    task_reject_on_worker_lost=True,  # Reject task if worker dies
)

logger.info("Celery app configured")
