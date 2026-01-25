from typing import Any, Dict, List, Optional

from celery.result import GroupResult
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from sono_eval.assessment.models import AssessmentInput
from sono_eval.auth.dependencies import get_current_user
from sono_eval.auth.users import User
from sono_eval.core.celery_app import celery_app
from sono_eval.tasks.assessment import process_assessment_task

router = APIRouter(tags=["batch"])


class BatchSubmission(BaseModel):
    """Request to submit a batch of assessments."""

    items: List[AssessmentInput] = Field(..., min_length=1, max_length=100)
    callback_url: Optional[str] = None


class BatchStatus(BaseModel):
    """Status of a batch processing job."""

    batch_id: str
    total: int
    completed: int
    failed: int
    pending: int
    status: str  # "pending", "processing", "completed", "failed"
    results: Optional[List[Dict[str, Any]]] = None


@router.post("/", response_model=BatchStatus, status_code=status.HTTP_202_ACCEPTED)
async def submit_batch(
    submission: BatchSubmission,
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    """Submit a batch of assessments for asynchronous processing."""
    import time

    # Create Celery tasks
    tasks: List[Any] = []
    for item in submission.items:
        # Convert input to dict for serialization
        task_input = item.model_dump(mode="json")
        # Add user context if needed
        task_input["_user_id"] = str(current_user.username)

        # Generate unique assessment ID for this task
        assessment_id = f"assess_{int(time.time() * 1000)}_{len(tasks)}"

        # Create task signature - task expects (assessment_id, input_data)
        tasks.append(process_assessment_task.s(assessment_id, task_input))

    # Create a group
    job = celery_app.group(tasks)
    result = job.apply_async()
    result.save()  # Ensure result is saved to backend

    return BatchStatus(
        batch_id=result.id,
        total=len(tasks),
        completed=0,
        failed=0,
        pending=len(tasks),
        status="pending",
    )


@router.get("/{batch_id}", response_model=BatchStatus)
async def get_batch_status(
    batch_id: str, current_user: User = Depends(get_current_user)  # noqa: B008
):
    """Get the status of a batch job."""
    try:
        # Restore GroupResult from backend
        result = GroupResult.restore(batch_id, app=celery_app)
    except Exception:
        raise HTTPException(status_code=404, detail="Batch not found")

    if not result:
        raise HTTPException(status_code=404, detail="Batch not found")

    # Calculate stats
    total = len(result.children) if result.children else 0
    completed = result.completed_count()

    # Check if ready
    is_ready = result.ready()
    state = "completed" if is_ready else "processing"

    # Retrieve results if completed
    results = []
    failed = 0

    if is_ready:
        for res in result.results:
            if res.failed():
                failed += 1
                results.append({"error": str(res.result), "status": "failed"})
            else:
                results.append({"data": res.result, "status": "completed"})

    return BatchStatus(
        batch_id=batch_id,
        total=total,
        completed=completed,
        failed=failed,
        pending=total - completed,
        status=state,
        results=results if is_ready else None,
    )
