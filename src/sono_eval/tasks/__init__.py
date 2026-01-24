"""
Asynchronous task processing for Sono-Eval.

Provides Celery-based background task execution for long-running operations.
"""

from sono_eval.core.celery_app import celery_app
from sono_eval.tasks.assessment import process_assessment_task

__all__ = ["celery_app", "process_assessment_task"]
