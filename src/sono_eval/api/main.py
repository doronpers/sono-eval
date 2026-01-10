"""
FastAPI backend for Sono-Eval system.

Provides REST API for assessments, candidate management, and tagging.
"""

from contextlib import asynccontextmanager
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from sono_eval.assessment.engine import AssessmentEngine
from sono_eval.assessment.models import AssessmentInput, AssessmentResult
from sono_eval.memory.memu import MemUStorage
from sono_eval.tagging.generator import TagGenerator
from sono_eval.mobile.app import create_mobile_app
from sono_eval.utils.config import get_config
from sono_eval.utils.logger import get_logger

logger = get_logger(__name__)


# Global instances
assessment_engine: Optional[AssessmentEngine] = None
memu_storage: Optional[MemUStorage] = None
tag_generator: Optional[TagGenerator] = None
config = get_config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the application."""
    # Startup
    global assessment_engine, memu_storage, tag_generator

    logger.info("Starting Sono-Eval API server")
    assessment_engine = AssessmentEngine()
    memu_storage = MemUStorage()
    tag_generator = TagGenerator()

    logger.info("API server initialized")

    yield

    # Shutdown
    logger.info("Shutting down Sono-Eval API server")


app = FastAPI(
    title="Sono-Eval API",
    description="Explainable Multi-Path Developer Assessment System",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount mobile companion app
mobile_app = create_mobile_app()
app.mount("/mobile", mobile_app)


# Request/Response Models
class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    components: Dict[str, str]


class CandidateCreateRequest(BaseModel):
    """Request to create a candidate."""

    candidate_id: str
    initial_data: Optional[Dict] = None


class TagRequest(BaseModel):
    """Request to generate tags."""

    text: str
    max_tags: int = 5


# Health and Status Endpoints
@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with API information."""
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        components={
            "assessment": "operational",
            "memory": "operational",
            "tagging": "operational",
        },
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        components={
            "assessment": "operational",
            "memory": "operational",
            "tagging": "operational",
        },
    )


@app.get("/status")
async def status():
    """Detailed status information."""
    return {
        "api_version": "0.1.0",
        "assessment_engine_version": assessment_engine.version if assessment_engine else "unknown",
        "config": {
            "multi_path_tracking": config.assessment_multi_path_tracking,
            "explanations_enabled": config.assessment_enable_explanations,
            "dark_horse_mode": config.dark_horse_mode,
        },
    }


# Assessment Endpoints
@app.post("/api/v1/assessments", response_model=AssessmentResult)
async def create_assessment(assessment_input: AssessmentInput):
    """
    Create a new assessment.

    Args:
        assessment_input: Assessment input data

    Returns:
        Complete assessment result with scores and explanations
    """
    if not assessment_engine:
        raise HTTPException(status_code=503, detail="Assessment engine not initialized")

    try:
        result = await assessment_engine.assess(assessment_input)

        # Store result in memory if candidate exists
        if memu_storage:
            memory = memu_storage.get_candidate_memory(assessment_input.candidate_id)
            if memory:
                memu_storage.add_memory_node(
                    assessment_input.candidate_id,
                    memory.root_node.node_id,
                    data={"assessment_result": result.model_dump(mode="json")},
                    metadata={"type": "assessment"},
                )

        return result
    except Exception as e:
        logger.error(f"Error creating assessment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/assessments/{assessment_id}")
async def get_assessment(assessment_id: str):
    """Get assessment by ID (placeholder - would need persistent storage)."""
    raise HTTPException(status_code=501, detail="Not implemented - requires persistent storage")


# Candidate Management Endpoints
@app.post("/api/v1/candidates")
async def create_candidate(request: CandidateCreateRequest):
    """
    Create a new candidate in memory storage.

    Args:
        request: Candidate creation request

    Returns:
        Created candidate memory
    """
    if not memu_storage:
        raise HTTPException(status_code=503, detail="Memory storage not initialized")

    try:
        memory = memu_storage.create_candidate_memory(request.candidate_id, request.initial_data)
        return {
            "candidate_id": memory.candidate_id,
            "created": memory.last_updated,
            "status": "created",
        }
    except Exception as e:
        logger.error(f"Error creating candidate: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/candidates/{candidate_id}")
async def get_candidate(candidate_id: str):
    """
    Get candidate memory.

    Args:
        candidate_id: Candidate identifier

    Returns:
        Candidate memory structure
    """
    if not memu_storage:
        raise HTTPException(status_code=503, detail="Memory storage not initialized")

    memory = memu_storage.get_candidate_memory(candidate_id)
    if not memory:
        raise HTTPException(status_code=404, detail="Candidate not found")

    return memory.model_dump(mode="json")


@app.get("/api/v1/candidates")
async def list_candidates():
    """List all candidates."""
    if not memu_storage:
        raise HTTPException(status_code=503, detail="Memory storage not initialized")

    candidates = memu_storage.list_candidates()
    return {"candidates": candidates, "count": len(candidates)}


@app.delete("/api/v1/candidates/{candidate_id}")
async def delete_candidate(candidate_id: str):
    """Delete a candidate."""
    if not memu_storage:
        raise HTTPException(status_code=503, detail="Memory storage not initialized")

    success = memu_storage.delete_candidate_memory(candidate_id)
    if not success:
        raise HTTPException(status_code=404, detail="Candidate not found")

    return {"status": "deleted", "candidate_id": candidate_id}


# Tagging Endpoints
@app.post("/api/v1/tags/generate")
async def generate_tags(request: TagRequest):
    """
    Generate semantic tags for text.

    Args:
        request: Tag generation request

    Returns:
        List of generated tags
    """
    if not tag_generator:
        raise HTTPException(status_code=503, detail="Tag generator not initialized")

    try:
        tags = tag_generator.generate_tags(request.text, max_tags=request.max_tags)
        return {"tags": [tag.model_dump() for tag in tags], "count": len(tags)}
    except Exception as e:
        logger.error(f"Error generating tags: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/files/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file for assessment.

    Args:
        file: Uploaded file

    Returns:
        File information and initial tags
    """
    try:
        content = await file.read()
        text_content = content.decode("utf-8")

        # Generate tags
        tags = []
        if tag_generator:
            semantic_tags = tag_generator.generate_tags(text_content)
            tags = [tag.model_dump() for tag in semantic_tags]

        return {"filename": file.filename, "size": len(content), "tags": tags, "status": "uploaded"}
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def create_app() -> FastAPI:
    """Factory function to create the FastAPI app."""
    return app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "sono_eval.api.main:app",
        host=config.api_host,
        port=config.api_port,
        reload=config.debug,
    )
