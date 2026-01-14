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
from sono_eval.mobile.easter_eggs import get_registry
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


class InteractionEvent(BaseModel):
    """Single interaction event for tracking."""

    event_type: str
    session_id: str
    candidate_id: Optional[str] = None
    page: str
    timestamp: str
    data: Dict[str, Any] = {}


class TrackingBatch(BaseModel):
    """Batch of interaction events."""

    events: List[InteractionEvent]


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

            # Check for easter eggs in code
            easter_eggs = []
            code_content = submission.content.get("code", "")
            if code_content:
                from sono_eval.mobile.easter_eggs import check_code_for_eggs
                easter_eggs = check_code_for_eggs(code_content)

            # Run assessment
            result = await assessment_engine.assess(assessment_input)

            # Add easter egg info to result if discovered
            result_data = result.model_dump(mode="json")
            if easter_eggs:
                result_data["easter_eggs_discovered"] = easter_eggs
                logger.info(f"Easter eggs discovered in assessment: {easter_eggs}")

            return {
                "success": True,
                "assessment_id": result.assessment_id,
                "result": result_data,
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

    @app.get("/api/mobile/recommendations")
    async def get_path_recommendations(
        candidate_id: Optional[str] = None,
        experience: Optional[str] = None,
        goals: Optional[str] = None,
    ):
        """
        Get personalized path recommendations based on candidate goals and experience.
        
        Uses goals and experience level to suggest relevant assessment paths.
        """
        try:
            # Parse goals if provided as comma-separated string
            goals_list = []
            if goals:
                goals_list = [g.strip() for g in goals.split(",") if g.strip()]

            recommendations = []
            paths_config = config.get("paths", {})

            # Recommendation logic based on goals
            if "strengths" in goals_list or "benchmark" in goals_list:
                recommendations.extend(["technical", "design"])
            if "improve" in goals_list:
                recommendations.append("problem_solving")
            if "practice" in goals_list:
                recommendations.extend(["technical", "collaboration"])

            # Experience-based recommendations
            if experience == "beginner":
                recommendations.extend(["technical", "problem_solving"])
            elif experience == "advanced":
                recommendations.extend(["design", "collaboration"])

            # Remove duplicates and filter to valid paths
            recommendations = list(
                dict.fromkeys([r for r in recommendations if r in paths_config])
            )

            # Build recommendation details
            recommended_paths = []
            for path_id in recommendations:
                path_info = paths_config.get(path_id, {})
                recommended_paths.append(
                    {
                        "id": path_id,
                        "name": path_info.get("title", path_id.title()),
                        "icon": path_info.get("icon", "📝"),
                        "reason": _get_recommendation_reason(path_id, goals_list, experience),
                    }
                )

            return {
                "success": True,
                "recommendations": recommended_paths,
                "count": len(recommended_paths),
            }
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return {"success": False, "recommendations": [], "count": 0}


def _get_recommendation_reason(path_id: str, goals: List[str], experience: Optional[str]) -> str:
    """Generate a reason for why a path is recommended."""
    reasons = {
        "technical": "Helps you understand your coding skills and technical practices",
        "design": "Reveals your system thinking and architecture approach",
        "collaboration": "Shows how well you communicate and work with others",
        "problem_solving": "Demonstrates your analytical and debugging capabilities",
    }
    base_reason = reasons.get(path_id, "Relevant to your goals")

    if "strengths" in goals:
        return f"{base_reason} - perfect for identifying your strengths"
    elif "improve" in goals:
        return f"{base_reason} - great for finding areas to improve"
    elif "practice" in goals:
        return f"{base_reason} - excellent for interview practice"
    else:
        return base_reason

    @app.post("/api/mobile/track")
    async def track_interactions(batch: TrackingBatch):
        """
        Track user interactions for analytics and personalization.
        
        Accepts anonymous tracking (session_id only) and links to candidate_id when available.
        """
        try:
            # Store interaction events (in production, this would go to a database)
            # For now, we'll log them and could store in memory/file system
            
            for event in batch.events:
                # Log important events
                if event.event_type in ['page_view', 'easter_egg_discovered', 'milestone']:
                    logger.info(
                        f"Tracking: {event.event_type} - "
                        f"session={event.session_id[:8]}... "
                        f"candidate={event.candidate_id or 'anonymous'} "
                        f"page={event.page}"
                    )
                
                # Link candidate_id to session if provided
                if event.candidate_id and event.session_id:
                    # In production, store this mapping in a database
                    # For now, we'll just acknowledge it
                    pass

            # Return success (in production, could return analytics insights)
            return {
                "success": True,
                "events_received": len(batch.events),
                "message": "Events tracked successfully",
            }
        except Exception as e:
            logger.error(f"Error tracking interactions: {e}")
            # Don't fail the request - tracking should be non-blocking
            return JSONResponse(
                status_code=200,  # Return 200 even on error to not break user flow
                content={
                    "success": False,
                    "error": "Tracking failed but request processed",
                },
            )

    @app.get("/api/mobile/easter-eggs")
    async def list_easter_eggs():
        """List available easter eggs (for discovery documentation)."""
        registry = get_registry()
        eggs = registry.list_eggs()
        return {
            "success": True,
            "eggs": eggs,
            "count": len(eggs),
            "message": "Easter eggs are discoverable features that unlock valuable functionality",
        }

    @app.get("/mobile/advanced")
    async def advanced_features(request: Request):
        """Hidden advanced features page."""
        # Check if expert mode is unlocked
        return templates.TemplateResponse(
            "advanced.html",
            {
                "request": request,
                "title": "Advanced Features",
            },
        )

    return app


if __name__ == "__main__":
    import uvicorn

    app = create_mobile_app()
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
