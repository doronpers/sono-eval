"""
Mobile-optimized companion interface for Sono-Eval.

Provides an interactive, explanatory, and non-linear assessment experience
optimized for mobile devices.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml  # type: ignore
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from sono_eval.assessment.engine import AssessmentEngine
from sono_eval.assessment.models import AssessmentInput, PathType
from sono_eval.mobile.session import MobileSessionManager
from sono_eval.utils.logger import get_logger

logger = get_logger(__name__)
session_manager = MobileSessionManager()

# Get the mobile module directory
MOBILE_DIR = Path(__file__).parent
STATIC_DIR = MOBILE_DIR / "static"
TEMPLATES_DIR = MOBILE_DIR / "templates"
CONFIG_PATH = MOBILE_DIR / "mobile_config.yaml"


class MobileAssessmentState(BaseModel):
    """State for mobile assessment session."""

    candidate_id: str
    selected_paths: List[PathType] = Field(default_factory=list)
    current_step: int = 0
    answers: Dict[str, str] = Field(default_factory=dict)
    personalization: Dict[str, Any] = Field(default_factory=dict)


class MobilePathSelection(BaseModel):
    """Path selection for mobile assessment."""

    candidate_id: str
    paths: List[str]


class MobileSubmission(BaseModel):
    """Mobile assessment submission."""

    candidate_id: str
    paths: List[str]
    content: Dict[str, str]
    personalization: Dict[str, Any] = Field(default_factory=dict)


class InteractionEvent(BaseModel):
    """Single interaction event for tracking."""

    event_type: str
    session_id: str
    candidate_id: Optional[str] = None
    page: str
    timestamp: str
    data: Dict[str, Any] = Field(default_factory=dict)


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
            from typing import cast

            return cast(Dict[str, Any], yaml.safe_load(f))
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
        # Get or create session
        session_id = request.cookies.get("session_id")
        if not session_id or not session_manager.get_session(session_id):
            session_id = session_manager.create_session()

        session = session_manager.get_session(session_id)

        response = templates.TemplateResponse(
            request,
            "index.html",
            {
                "title": "Welcome to Sono-Eval",
                "current_step": session.current_step if session else 0,
            },
        )

        # Set persistent cookie
        if request.cookies.get("session_id") != session_id:
            response.set_cookie(
                key="session_id",
                value=session_id,
                max_age=30 * 24 * 60 * 60,  # 30 days
                httponly=True,
                samesite="lax",
            )

        return response

    @app.get("/setup", response_class=HTMLResponse)
    async def mobile_setup(request: Request):
        """Interactive setup wizard for remote candidates."""
        session_id = request.cookies.get("session_id")
        if session_id:
            session_manager.update_step(session_id, 1)

        return templates.TemplateResponse(
            request,
            "setup.html",
            {
                "title": "Setup Your Environment",
                "current_step": 1,
            },
        )

    @app.get("/start", response_class=HTMLResponse)
    async def mobile_start(request: Request):
        """Start assessment - candidate information."""
        session_id = request.cookies.get("session_id")
        if session_id:
            session_manager.update_step(session_id, 2)

        return templates.TemplateResponse(
            request,
            "start.html",
            {
                "title": "Let's Get Started",
                "current_step": 2,
            },
        )

    @app.get("/paths", response_class=HTMLResponse)
    async def mobile_paths(request: Request, candidate_id: Optional[str] = None):
        """Path selection with explanations."""
        # Update session
        session_id = request.cookies.get("session_id")
        if session_id:
            session_manager.update_step(session_id, 3)
            # If candidate ID provided, link it
            if candidate_id:
                session_manager.link_candidate(session_id, candidate_id)

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
            request,
            "paths.html",
            {
                "title": "Choose Your Focus Areas",
                "candidate_id": candidate_id or "guest",
                "paths": path_list,
                "current_step": 3,
            },
        )

    @app.get("/assess", response_class=HTMLResponse)
    async def mobile_assess(
        request: Request,
        candidate_id: Optional[str] = None,
        paths: Optional[str] = None,
    ):
        """Interactive assessment page."""
        session_id = request.cookies.get("session_id")
        if session_id:
            session_manager.update_step(session_id, 4)

        selected_paths = paths.split(",") if paths else []
        return templates.TemplateResponse(
            request,
            "assess.html",
            {
                "title": "Your Assessment",
                "candidate_id": candidate_id or "guest",
                "selected_paths": selected_paths,
                "current_step": 4,
            },
        )

    @app.get("/results", response_class=HTMLResponse)
    async def mobile_results(request: Request, assessment_id: Optional[str] = None):
        """Results page with detailed feedback."""
        return templates.TemplateResponse(
            request,
            "results.html",
            {
                "title": "Your Results",
                "assessment_id": assessment_id,
            },
        )

    @app.get("/insights", response_class=HTMLResponse)
    async def mobile_insights(request: Request, assessment_id: Optional[str] = None):
        """Dedicated insights page with learning journey and recommendations."""
        return templates.TemplateResponse(
            request,
            "insights.html",
            {
                "title": "Your Insights",
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

            # Mobile assessment result
            result_data = result.model_dump(mode="json")
            return {
                "success": True,
                "assessment_id": result.assessment_id,
                "result": result_data,
            }
        except Exception as e:
            logger.error(f"Error processing mobile assessment: {e}")
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": f"Assessment processing failed: {str(e)}",
                },
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
            recommendations = list(dict.fromkeys([r for r in recommendations if r in paths_config]))

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
                if event.event_type in [
                    "page_view",
                    "milestone",
                ]:
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

    @app.post("/api/mobile/session/store")
    async def store_session_data(data: Dict[str, Any]):
        """
        Store assessment result in server-side session for retrieval.

        This allows sharing results between pages without URL params.
        In production, use Redis or database for session storage.
        For now, return success and rely on client-side sessionStorage.
        """
        # In production, use Redis or database for session storage
        # For now, return success and rely on client-side sessionStorage
        return {"success": True, "message": "Data acknowledged"}

    @app.get("/mobile/advanced")
    async def advanced_features(request: Request):
        """Hidden advanced features page."""
        # Check if expert mode is unlocked
        return templates.TemplateResponse(
            request,
            "advanced.html",
            {
                "title": "Advanced Features",
            },
        )

    @app.get("/api/mobile/visualization/dashboard/{assessment_id}")
    async def get_dashboard_visualization(assessment_id: str):
        """
        Get complete dashboard visualization data for an assessment.

        Returns chart-ready data structures for all visualizations.
        """
        try:
            # In production, fetch from database
            # For now, return mock data structure
            # from sono_eval.assessment.dashboard import DashboardData

            # Mock dashboard data
            # In production: result = await fetch_assessment_result(assessment_id)
            # dashboard = DashboardData.from_assessment_result(result)

            return {
                "success": True,
                "assessment_id": assessment_id,
                "message": "Dashboard data endpoint ready. Integrate with assessment storage.",
            }
        except Exception as e:
            logger.error(f"Error generating dashboard visualization: {e}")
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": f"Failed to generate visualization data: {str(e)}",
                },
            )

    @app.get("/api/mobile/visualization/radar/{assessment_id}")
    async def get_radar_chart_data(assessment_id: str):
        """Get radar chart data for path scores."""
        try:
            # Mock implementation
            # In production: fetch result and generate chart data
            return {
                "success": True,
                "chart_data": {
                    "type": "radar",
                    "labels": [
                        "Technical",
                        "Design",
                        "Collaboration",
                        "Problem Solving",
                        "Communication",
                    ],
                    "datasets": [
                        {
                            "label": "Path Scores",
                            "data": [75, 82, 68, 79, 85],
                            "backgroundColor": "rgba(59, 130, 246, 0.2)",
                            "borderColor": "rgb(59, 130, 246)",
                        }
                    ],
                },
            }
        except Exception as e:
            logger.error(f"Error generating radar chart: {e}")
            return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

    @app.get("/api/mobile/visualization/progress/{assessment_id}")
    async def get_progress_ring_data(assessment_id: str):
        """Get progress ring data for overall score."""
        try:
            # Mock implementation
            return {
                "success": True,
                "chart_data": {
                    "type": "doughnut",
                    "labels": ["Score", "Remaining"],
                    "datasets": [
                        {
                            "data": [78, 22],
                            "backgroundColor": ["#3b82f6", "#e5e7eb"],
                        }
                    ],
                },
            }
        except Exception as e:
            logger.error(f"Error generating progress ring: {e}")
            return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

    @app.get("/api/mobile/visualization/breakdowns/{assessment_id}")
    async def get_path_breakdowns(assessment_id: str):
        """Get detailed breakdown charts for each path."""
        try:
            # Mock implementation
            return {
                "success": True,
                "charts": [
                    {
                        "path": "technical",
                        "type": "bar",
                        "labels": [
                            "Code Quality",
                            "Testing",
                            "Patterns",
                            "Performance",
                        ],
                        "datasets": [
                            {
                                "label": "Score",
                                "data": [80, 72, 85, 68],
                                "backgroundColor": "#3b82f6",
                            }
                        ],
                    }
                ],
            }
        except Exception as e:
            logger.error(f"Error generating breakdowns: {e}")
            return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

    @app.get("/api/mobile/visualization/trend/{candidate_id}")
    async def get_trend_data(candidate_id: str, limit: int = 10):
        """Get trend chart data for candidate's assessment history."""
        try:
            # Mock implementation
            # In production: fetch historical results for candidate
            return {
                "success": True,
                "chart_data": {
                    "type": "line",
                    "labels": ["01/15", "01/16", "01/17", "01/18", "01/19"],
                    "datasets": [
                        {
                            "label": "Score Over Time",
                            "data": [68, 72, 75, 78, 82],
                            "borderColor": "#22c55e",
                            "backgroundColor": "rgba(34, 197, 94, 0.1)",
                        }
                    ],
                },
                "trend_direction": "improving",
            }
        except Exception as e:
            logger.error(f"Error generating trend chart: {e}")
            return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

    @app.get("/api/mobile/visualization/motives/{assessment_id}")
    async def get_motives_chart_data(assessment_id: str):
        """Get micro-motives visualization data."""
        try:
            # Mock implementation
            return {
                "success": True,
                "chart_data": {
                    "type": "bar",
                    "labels": ["Mastery", "Quality", "Efficiency", "Innovation"],
                    "datasets": [
                        {
                            "label": "Strength",
                            "data": [85, 78, 72, 65],
                            "backgroundColor": [
                                "#3b82f6",
                                "#22c55e",
                                "#f59e0b",
                                "#8b5cf6",
                            ],
                        }
                    ],
                },
                "dominant_motive": "Mastery",
            }
        except Exception as e:
            logger.error(f"Error generating motives chart: {e}")
            return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

    return app


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


if __name__ == "__main__":
    import uvicorn

    app = create_mobile_app()
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)  # nosec B104
