"""
Assessment background tasks.

Handles asynchronous assessment processing using Celery.
"""

import asyncio
from typing import Any, Dict

from celery import Task

from sono_eval.assessment.engine import AssessmentEngine
from sono_eval.assessment.models import AssessmentInput
from sono_eval.memory.memu import MemUStorage
from sono_eval.tasks.celery_app import celery_app
from sono_eval.utils.logger import get_logger

logger = get_logger(__name__)


class AssessmentTask(Task):
    """
    Custom Celery task class for assessments.

    Maintains singleton instances of the assessment engine and storage
    to avoid repeated initialization overhead.
    """

    _engine: AssessmentEngine = None
    _storage: MemUStorage = None

    @property
    def engine(self) -> AssessmentEngine:
        """Lazy-load assessment engine."""
        if self._engine is None:
            logger.info("Initializing AssessmentEngine for worker")
            self._engine = AssessmentEngine()
        return self._engine

    @property
    def storage(self) -> MemUStorage:
        """Lazy-load MemU storage."""
        if self._storage is None:
            logger.info("Initializing MemUStorage for worker")
            self._storage = MemUStorage()
        return self._storage


@celery_app.task(
    bind=True,
    base=AssessmentTask,
    name="sono_eval.tasks.process_assessment",
    max_retries=3,
    default_retry_delay=60,  # Retry after 60 seconds
)
def process_assessment_task(
    self, assessment_id: str, input_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Process an assessment asynchronously.

    Args:
        self: Task instance (bound)
        assessment_id: Unique assessment identifier
        input_data: Assessment input data (dict form of AssessmentInput)

    Returns:
        Assessment result as dictionary

    Raises:
        Exception: If assessment fails after retries
    """
    try:
        logger.info(f"Starting async assessment {assessment_id}")

        # Update task state
        self.update_state(
            state="PROCESSING",
            meta={
                "assessment_id": assessment_id,
                "candidate_id": input_data.get("candidate_id"),
                "status": "processing",
                "progress": 10,
            },
        )

        # Parse input
        assessment_input = AssessmentInput.model_validate(input_data)

        # Run assessment (need to use asyncio since engine.assess is async)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(self.engine.assess(assessment_input))
        finally:
            loop.close()

        # Update progress
        self.update_state(
            state="PROCESSING",
            meta={
                "assessment_id": assessment_id,
                "candidate_id": assessment_input.candidate_id,
                "status": "storing",
                "progress": 80,
            },
        )

        # Store result in memory
        memory = self.storage.get_candidate_memory(assessment_input.candidate_id)
        if memory:
            self.storage.add_memory_node(
                assessment_input.candidate_id,
                memory.root_node.node_id,
                data={"assessment_result": result.model_dump(mode="json")},
                metadata={"type": "assessment", "async": True},
            )
            logger.info(
                f"Stored async assessment {assessment_id} for {assessment_input.candidate_id}"
            )
        else:
            logger.warning(
                f"Candidate {assessment_input.candidate_id} not found - result not stored in memory"
            )

        # Convert result to dict for Celery
        result_dict: Dict[str, Any] = result.model_dump(mode="json")
        result_dict["job_status"] = "completed"

        logger.info(
            f"Completed async assessment {assessment_id}: "
            f"score={result.overall_score:.2f}, "
            f"time={result.processing_time_ms:.2f}ms"
        )

        return result_dict

    except Exception as exc:
        logger.error(
            f"Error processing assessment {assessment_id}: {exc}", exc_info=True
        )

        # Retry with exponential backoff
        if self.request.retries < self.max_retries:
            logger.info(
                f"Retrying assessment {assessment_id} "
                f"(attempt {self.request.retries + 1}/{self.max_retries})"
            )
            raise self.retry(exc=exc, countdown=2**self.request.retries * 60)
        else:
            # All retries exhausted
            logger.error(f"Assessment {assessment_id} failed after all retries")
            return {
                "assessment_id": assessment_id,
                "job_status": "failed",
                "error": str(exc),
                "error_type": type(exc).__name__,
            }


@celery_app.task(name="sono_eval.tasks.cleanup_expired_results")
def cleanup_expired_results() -> Dict[str, Any]:
    """
    Periodic task to clean up expired assessment results.

    This task should be scheduled to run periodically (e.g., hourly).

    Returns:
        Cleanup statistics
    """
    logger.info("Running expired results cleanup")

    # TODO: Implement cleanup logic
    # - Remove old job results from Redis
    # - Archive old assessments
    # - Clean up temporary files

    return {
        "status": "completed",
        "items_cleaned": 0,
        "message": "Cleanup completed successfully",
    }
