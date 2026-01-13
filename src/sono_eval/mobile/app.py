"""
Mobile-optimized companion interface for Sono-Eval.

Provides an interactive, explanatory, and non-linear assessment experience
optimized for mobile devices.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from sono_eval.assessment.engine import AssessmentEngine
from sono_eval.assessment.models import AssessmentInput, PathType
from sono_eval.utils.logger import get_logger

logger = get_logger(__name__)

# Get the mobile module directory
MOBILE_DIR = Path(__file__).parent
STATIC_DIR = MOBILE_DIR / "static"
TEMPLATES_DIR = MOBILE_DIR / "templates"
CONFIG_PATH = MOBILE_DIR / "mobile_config.yaml"


class MobileAssessmentState(BaseModel):
    """State for mobile assessment session."""

    candidate_id: str
    selected_paths: List[PathType] = []
    current_step: int = 0
    answers: Dict[str, str] = {}
    personalization: Dict[str, str] = {}


class MobilePathSelection(BaseModel):
    """Path selection for mobile assessment."""

    candidate_id: str
    paths: List[str]


class MobileSubmission(BaseModel):
    """Mobile assessment submission."""

    candidate_id: str
    paths: List[str]
    content: Dict[str, str]
    personalization: Dict[str, str] = {}


def load_mobile_config() -> Dict[str, Any]:
    """Load mobile configuration from YAML."""
    if not CONFIG_PATH.exists():
        logger.warning(f"Mobile config not found at {CONFIG_PATH}, using defaults")
        return {"paths": {}}

    try:
        with open(CONFIG_PATH, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Error loading mobile config: {e}")
        return {"paths": {}}


def create_mobile_app() -> FastAPI:
    """
    Create mobile companion FastAPI application.

    Returns:
        Configured FastAPI app for mobile interface
    """
    app = FastAPI(
        title="Sono-Eval Mobile Companion",
        description="Mobile-optimized interactive assessment experience",
        version="0.1.1",
    )

    # Mount static files
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    # Setup templates
    templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

    # Initialize assessment engine
    assessment_engine = AssessmentEngine()

    # Load config
    config = load_mobile_config()

    @app.get("/", response_class=HTMLResponse)
    async def mobile_home(request: Request):
        """Mobile home page with welcome and explanation."""
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "title": "Welcome to Sono-Eval",
            },
        )

    @app.get("/start", response_class=HTMLResponse)
    async def mobile_start(request: Request):
        """Start assessment - candidate information."""
        return templates.TemplateResponse(
            "start.html",
            {
                "request": request,
                "title": "Let's Get Started",
            },
        )

    @app.get("/paths", response_class=HTMLResponse)
    async def mobile_paths(request: Request, candidate_id: Optional[str] = None):
        """Path selection with explanations."""
        path_list = []
        for path_id, path_info in config.get("paths", {}).items():
            path_list.append(
                {
                    "id": path_id,
                    "name": path_info.get("title", path_id.title()),
                    "icon": path_info.get("icon", "📝"),
                    "description": path_info.get("overview", ""),
                    "time": path_info.get("time", ""),
                }
            )

        return templates.TemplateResponse(
            "paths.html",
            {
                "request": request,
                "title": "Choose Your Focus Areas",
                "candidate_id": candidate_id or "guest",
                "paths": path_list,
            },
        )

    @app.get("/assess", response_class=HTMLResponse)
    async def mobile_assess(
        request: Request, candidate_id: Optional[str] = None, paths: Optional[str] = None
    ):
        """Interactive assessment page."""
        selected_paths = paths.split(",") if paths else []
        return templates.TemplateResponse(
            "assess.html",
            {
                "request": request,
                "title": "Your Assessment",
                "candidate_id": candidate_id or "guest",
                "selected_paths": selected_paths,
            },
        )

    @app.get("/results", response_class=HTMLResponse)
    async def mobile_results(request: Request, assessment_id: Optional[str] = None):
        """Results page with detailed feedback."""
        return templates.TemplateResponse(
            "results.html",
            {
                "request": request,
                "title": "Your Results",
                "assessment_id": assessment_id,
            },
        )

    # --- API Endpoints ---

    @app.post("/api/mobile/assess")
    async def mobile_submit_assessment(submission: MobileSubmission):
        """Submit mobile assessment for evaluation."""
        try:
            # Convert string paths to PathType enum
            path_types = []
            for path_str in submission.paths:
                try:
                    path_types.append(PathType(path_str.lower()))
                except ValueError:
                    logger.warning(f"Invalid path type: {path_str}")

            # Create assessment input
            assessment_input = AssessmentInput(
                candidate_id=submission.candidate_id,
                submission_type="mobile_interactive",
                content=submission.content,
                paths_to_evaluate=path_types,
                options={
                    "personalization": submission.personalization,
                    "source": "mobile_companion",
                },
            )

            # Run assessment
            result = await assessment_engine.assess(assessment_input)

            return {
                "success": True,
                "assessment_id": result.assessment_id,
                "result": result.model_dump(mode="json"),
            }
        except Exception as e:
            logger.error(f"Error processing mobile assessment: {e}")
            return JSONResponse(
                status_code=500,
                content={"success": False, "error": f"Assessment processing failed: {str(e)}"},
            )

    @app.get("/api/mobile/explain/{path}")
    async def mobile_explain_path(path: str):
        """Get detailed explanation for a specific path."""
        path_lower = path.lower()
        paths_config = config.get("paths", {})

        if path_lower in paths_config:
            return {"success": True, "explanation": paths_config[path_lower]}

        raise HTTPException(status_code=404, detail=f"Path '{path}' not found")

    return app


if __name__ == "__main__":
    import uvicorn

    app = create_mobile_app()
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
