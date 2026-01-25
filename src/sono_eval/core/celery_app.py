from celery import Celery

from sono_eval.utils.config import get_config

config = get_config()

# Initialize Celery
celery_app = Celery(
    "sono_eval",
    broker=config.celery_broker_url,
    backend=config.celery_result_backend,
    include=["sono_eval.tasks.assessment"],
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour hard limit
    worker_concurrency=4,
)

if __name__ == "__main__":
    celery_app.start()
