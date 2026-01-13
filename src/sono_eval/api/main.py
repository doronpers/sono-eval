"""
FastAPI backend for Sono-Eval system.

Provides REST API for assessments, candidate management, and tagging.
"""

import re
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from time import time
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Request, Response, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, validator
from starlette.middleware.base import BaseHTTPMiddleware

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


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware to add unique request ID to each request."""
    
    async def dispatch(self, request: Request, call_next):
        """Add request ID and log request details."""
        # Generate or extract request ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        
        # Add to request state
        request.state.request_id = request_id
        
        # Log request start
        start_time = time()
        logger.info(
            f"Request started: {request.method} {request.url.path}",
            extra={"request_id": request_id}
        )
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration_ms = (time() - start_time) * 1000
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            
            # Log request completion
            logger.info(
                f"Request completed: {request.method} {request.url.path} - Status: {response.status_code}",
                extra={"request_id": request_id, "duration_ms": duration_ms}
            )
            
            return response
        except Exception as e:
            # Log error with request ID
            duration_ms = (time() - start_time) * 1000
            logger.error(
                f"Request failed: {request.method} {request.url.path} - Error: {str(e)}",
                extra={"request_id": request_id, "duration_ms": duration_ms},
                exc_info=True
            )
            raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the application."""
    # Startup
    global assessment_engine, memu_storage, tag_generator

    logger.info("Starting Sono-Eval API server")
    
    # Security: Validate configuration before starting
    _validate_security_config()
    
    assessment_engine = AssessmentEngine()
    memu_storage = MemUStorage()
    tag_generator = TagGenerator()

    logger.info("API server initialized")

    yield

    # Shutdown
    logger.info("Shutting down Sono-Eval API server")


def _validate_security_config():
    """Validate security-critical configuration at startup."""
    DEFAULT_SECRETS = [
        "your-secret-key-here-change-in-production",
        "change_this_secret_key_in_production",
    ]
    
    # Check for default secret key
    if config.secret_key in DEFAULT_SECRETS:
        if config.app_env == "production":
            raise ValueError(
                "CRITICAL SECURITY ERROR: SECRET_KEY is set to default value. "
                "You MUST change this in production. Generate a secure key with: "
                "python -c 'import secrets; print(secrets.token_urlsafe(32))'"
            )
        else:
            logger.warning(
                "WARNING: Using default SECRET_KEY. This is only acceptable in development. "
                "Generate a secure key for production with: "
                "python -c 'import secrets; print(secrets.token_urlsafe(32))'"
            )
    
    # Check Superset secret key
    if config.superset_secret_key in DEFAULT_SECRETS:
        if config.app_env == "production":
            raise ValueError(
                "CRITICAL SECURITY ERROR: SUPERSET_SECRET_KEY is set to default value. "
                "Change this immediately in production."
            )
        else:
            logger.warning("WARNING: Using default SUPERSET_SECRET_KEY (development only)")
    
    # Validate allowed hosts in production
    if config.app_env == "production":
        if not config.allowed_hosts or config.allowed_hosts == "*":
            logger.warning(
                "WARNING: ALLOWED_HOSTS not properly configured for production. "
                "Set specific domains to prevent CORS attacks."
            )
    
    logger.info("Security configuration validated")


app = FastAPI(
    title="Sono-Eval API",
    description="Explainable Multi-Path Developer Assessment System",
    version="0.1.0",
    lifespan=lifespan,
)

# Add Request ID middleware (must be first to track all requests)
app.add_middleware(RequestIDMiddleware)

# CORS middleware - configure via ALLOWED_HOSTS environment variable for production
# In production, set ALLOWED_HOSTS to specific origins (comma-separated)
# Default allows all origins for development ONLY
# Security: Validate CORS configuration at startup
if config.app_env == "production":
    if not config.allowed_hosts or config.allowed_hosts == "*":
        logger.error("CRITICAL: ALLOWED_HOSTS must be configured in production. Set specific domains.")
        raise ValueError("ALLOWED_HOSTS must be set to specific origins in production environment")
    cors_origins = [origin.strip() for origin in config.allowed_hosts.split(",")]
    logger.info(f"Production CORS configured for origins: {cors_origins}")
else:
    # Development: allow all origins but log warning
    cors_origins = ["*"]
    if config.allowed_hosts and config.allowed_hosts != "*":
        cors_origins = [origin.strip() for origin in config.allowed_hosts.split(",")]
    logger.warning(f"Development mode: CORS origins = {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Mount mobile companion app
mobile_app = create_mobile_app()
app.mount("/mobile", mobile_app)


# API Versioning - Define version prefix
API_V1_PREFIX = "/api/v1"


# Request/Response Models
class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    timestamp: str
    components: Dict[str, str]
    details: Optional[Dict[str, Any]] = None


class CandidateCreateRequest(BaseModel):
    """Request to create a candidate."""

    candidate_id: str = Field(..., min_length=1, max_length=100)
    initial_data: Optional[Dict] = None
    
    @validator('candidate_id')
    def validate_candidate_id(cls, v):
        """Validate candidate_id format to prevent injection attacks."""
        # Allow only alphanumeric, dash, underscore
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError(
                'candidate_id must contain only alphanumeric characters, dashes, and underscores'
            )
        return v


class TagRequest(BaseModel):
    """Request to generate tags."""

    text: str = Field(..., min_length=1, max_length=100000)
    max_tags: int = Field(default=5, ge=1, le=20)
    
    @validator('text')
    def validate_text(cls, v):
        """Validate text content."""
        # Basic sanitization - remove null bytes
        if '\x00' in v:
            raise ValueError('text contains invalid null bytes')
        return v


# Health check caching (5 second cache to avoid expensive operations on every call)
_health_check_cache: Dict[str, Any] = {}
_health_check_cache_time: float = 0
_HEALTH_CHECK_CACHE_TTL: float = 5.0  # 5 seconds


async def check_component_health(include_details: bool = True) -> Dict[str, Any]:
    """
    Check the health of all system components.
    
    Args:
        include_details: Whether to include detailed information (may expose paths)
    
    Returns:
        Dictionary with component statuses and details
    """
    global _health_check_cache, _health_check_cache_time
    
    # Check cache first
    current_time = time()
    if (
        _health_check_cache
        and (current_time - _health_check_cache_time) < _HEALTH_CHECK_CACHE_TTL
    ):
        cached_result = _health_check_cache.copy()
        # If cached result has details but we don't want them, remove them
        if not include_details and "details" in cached_result:
            cached_result["details"] = None
        return cached_result
    
    components = {}
    details: Dict[str, Any] = {} if include_details else {}
    overall_healthy = True
    
    # Check Assessment Engine
    try:
        if assessment_engine is None:
            components["assessment"] = "unavailable"
            if include_details:
                details["assessment"] = {"error": "Not initialized"}
            overall_healthy = False
        else:
            # Try a simple operation to verify it's working
            components["assessment"] = "operational"
            if include_details:
                details["assessment"] = {
                    "version": getattr(assessment_engine, "version", "unknown"),
                    "initialized": True
                }
    except Exception as e:
        components["assessment"] = "degraded"
        if include_details:
            details["assessment"] = {"error": "Initialization error"}
        logger.error(f"Assessment engine health check failed: {e}")
        overall_healthy = False
    
    # Check Memory Storage (MemU)
    try:
        if memu_storage is None:
            components["memory"] = "unavailable"
            if include_details:
                details["memory"] = {"error": "Not initialized"}
            overall_healthy = False
        else:
            # Check if storage path is accessible
            storage_path = config.get_storage_path()
            if storage_path.exists() and storage_path.is_dir():
                # Try to list candidates (lightweight operation)
                try:
                    candidates = memu_storage.list_candidates()
                    components["memory"] = "operational"
                    if include_details:
                        details["memory"] = {
                            "candidates_count": len(candidates),
                            "accessible": True
                        }
                except Exception as e:
                    components["memory"] = "degraded"
                    if include_details:
                        details["memory"] = {"error": "Storage access failed"}
                    logger.error(f"Memory storage health check failed: {e}")
                    overall_healthy = False
            else:
                components["memory"] = "degraded"
                if include_details:
                    details["memory"] = {"error": "Storage path not accessible"}
                overall_healthy = False
    except Exception as e:
        components["memory"] = "degraded"
        if include_details:
            details["memory"] = {"error": "Storage check failed"}
        logger.error(f"Memory storage health check error: {e}")
        overall_healthy = False
    
    # Check Tag Generator
    try:
        if tag_generator is None:
            components["tagging"] = "unavailable"
            if include_details:
                details["tagging"] = {"error": "Not initialized"}
            overall_healthy = False
        else:
            # Check if model cache directory exists
            cache_dir = config.get_cache_dir()
            if cache_dir.exists():
                components["tagging"] = "operational"
                if include_details:
                    details["tagging"] = {
                        "model_name": config.t5_model_name,
                        "initialized": True
                    }
            else:
                components["tagging"] = "degraded"
                if include_details:
                    details["tagging"] = {
                        "model_name": config.t5_model_name,
                        "warning": "Cache directory not found (models may download on first use)"
                    }
    except Exception as e:
        components["tagging"] = "degraded"
        if include_details:
            details["tagging"] = {"error": "Tagging check failed"}
        logger.error(f"Tag generator health check error: {e}")
        overall_healthy = False
    
    # Check Database (if configured)
    try:
        database_url = config.database_url
        if database_url.startswith("sqlite"):
            # SQLite - check if file path is writable
            db_path = database_url.replace("sqlite:///", "")
            if db_path:
                db_file = Path(db_path)
                # Check if directory is writable
                if db_file.parent.exists():
                    components["database"] = "operational"
                    if include_details:
                        details["database"] = {
                            "type": "sqlite",
                            "exists": db_file.exists()
                        }
                else:
                    components["database"] = "degraded"
                    if include_details:
                        details["database"] = {"error": "Database directory not accessible"}
                    overall_healthy = False
            else:
                components["database"] = "operational"
                if include_details:
                    details["database"] = {"type": "sqlite", "in_memory": True}
        else:
            # PostgreSQL or other - mark as configured but not tested
            components["database"] = "operational"
            if include_details:
                details["database"] = {
                    "type": "postgresql",
                    "configured": True,
                    "note": "Connection not tested"
                }
    except Exception as e:
        components["database"] = "degraded"
        if include_details:
            details["database"] = {"error": "Database check failed"}
        logger.error(f"Database health check error: {e}")
        overall_healthy = False
    
    # Check Redis (optional)
    try:
        # Try to connect to Redis (non-blocking check)
        try:
            import redis
            r = redis.Redis(
                host=config.redis_host,
                port=config.redis_port,
                db=config.redis_db,
                password=config.redis_password,
                socket_connect_timeout=1,
                socket_timeout=1
            )
            r.ping()
            components["redis"] = "operational"
            if include_details:
                details["redis"] = {"connected": True}
        except ImportError:
            components["redis"] = "unavailable"
            if include_details:
                details["redis"] = {"error": "redis package not installed"}
        except Exception as e:
            # Redis is optional, so this is not a failure
            components["redis"] = "unavailable"
            if include_details:
                details["redis"] = {
                    "note": "Redis is optional - system works without it",
                    "status": "unavailable"
                }
            logger.debug(f"Redis health check: {type(e).__name__}")
    except Exception as e:
        components["redis"] = "unavailable"
        if include_details:
            details["redis"] = {"error": "Redis check failed"}
        logger.error(f"Redis health check error: {e}")
    
    # Check File System
    try:
        storage_path = config.get_storage_path()
        cache_dir = config.get_cache_dir()
        tagstudio_root = config.get_tagstudio_root()
        
        all_paths_ok = True
        path_details = {}
        
        for name, path in [("storage", storage_path), ("cache", cache_dir), ("tagstudio", tagstudio_root)]:
            if path.exists() and path.is_dir():
                # Check if writable
                try:
                    test_file = path / ".health_check"
                    test_file.touch()
                    test_file.unlink()
                    path_details[name] = {"writable": True}
                except Exception:
                    path_details[name] = {"writable": False}
                    all_paths_ok = False
            else:
                path_details[name] = {"exists": False}
                all_paths_ok = False
        
        if all_paths_ok:
            components["filesystem"] = "operational"
            if include_details:
                details["filesystem"] = path_details
        else:
            components["filesystem"] = "degraded"
            if include_details:
                details["filesystem"] = path_details
            overall_healthy = False
    except Exception as e:
        components["filesystem"] = "degraded"
        if include_details:
            details["filesystem"] = {"error": "Filesystem check failed"}
        logger.error(f"Filesystem health check error: {e}")
        overall_healthy = False
    
    result: Dict[str, Any] = {
        "components": components,
        "healthy": overall_healthy
    }
    if include_details:
        result["details"] = details
    
    # Cache the result (always cache with details for efficiency)
    _health_check_cache = {
        "components": components,
        "healthy": overall_healthy,
        "details": details if include_details else {}
    }
    _health_check_cache_time = current_time
    
    return result


# Health and Status Endpoints
@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with API information."""
    health_data = await check_component_health(include_details=True)
    return HealthResponse(
        status="healthy" if health_data["healthy"] else "degraded",
        version="0.1.0",
        timestamp=datetime.utcnow().isoformat() + "Z",
        components=health_data["components"],
        details=health_data.get("details"),
    )


@app.get("/health", response_model=HealthResponse)
async def health_check(response: Response):
    """
    Health check endpoint.
    
    Returns basic health status without sensitive details.
    Suitable for load balancers and monitoring tools.
    """
    health_data = await check_component_health(include_details=False)
    
    # Set appropriate status code
    if not health_data["healthy"]:
        response.status_code = 503  # Service Unavailable
    
    return HealthResponse(
        status="healthy" if health_data["healthy"] else "unhealthy",
        version="0.1.0",
        timestamp=datetime.utcnow().isoformat() + "Z",
        components=health_data["components"],
        details=None,  # No sensitive details in basic health check
    )


@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check_v1(response: Response):
    """
    Health check endpoint (v1 API path).
    
    Returns detailed health status of all system components.
    Includes component details but sanitizes sensitive information.
    Suitable for monitoring and debugging.
    """
    health_data = await check_component_health(include_details=True)
    
    # Set appropriate status code
    if not health_data["healthy"]:
        response.status_code = 503  # Service Unavailable
    
    return HealthResponse(
        status="healthy" if health_data["healthy"] else "unhealthy",
        version="0.1.0",
        timestamp=datetime.utcnow().isoformat() + "Z",
        components=health_data["components"],
        details=health_data.get("details"),
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
        
    Security:
        - Validates file extension
        - Checks file size limit
        - Sanitizes filename
    """
    try:
        # Security: Validate file extension
        allowed_extensions = config.allowed_extensions.split(',')
        file_ext = file.filename.split('.')[-1].lower() if '.' in file.filename else ''
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type '.{file_ext}' not allowed. Allowed types: {', '.join(allowed_extensions)}"
            )
        
        # Security: Sanitize filename to prevent path traversal
        import re
        from pathlib import Path
        safe_filename = re.sub(r'[^a-zA-Z0-9._-]', '_', file.filename)
        safe_filename = Path(safe_filename).name  # Remove any path components
        
        # Read file content with size limit
        content = await file.read()
        
        # Security: Check file size
        if len(content) > config.max_upload_size:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size: {config.max_upload_size / 1024 / 1024:.1f}MB"
            )
        
        # Try to decode as text
        try:
            text_content = content.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="File must be valid UTF-8 text"
            )

        # Generate tags
        tags = []
        if tag_generator:
            semantic_tags = tag_generator.generate_tags(text_content)
            tags = [tag.model_dump() for tag in semantic_tags]

        return {
            "filename": safe_filename,
            "original_filename": file.filename,
            "size": len(content),
            "tags": tags,
            "status": "uploaded"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during file upload")


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
