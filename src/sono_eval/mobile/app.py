"""
Mobile-optimized companion interface for Sono-Eval.

Provides an interactive, explanatory, and non-linear assessment experience
optimized for mobile devices.
"""

from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
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


def create_mobile_app() -> FastAPI:
    """
    Create mobile companion FastAPI application.

    Returns:
        Configured FastAPI app for mobile interface
    """
    app = FastAPI(
        title="Sono-Eval Mobile Companion",
        description="Mobile-optimized interactive assessment experience",
        version="0.1.0",
    )

    # Mount static files
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    # Setup templates
    templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

    # Initialize assessment engine
    assessment_engine = AssessmentEngine()

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
        return templates.TemplateResponse(
            "paths.html",
            {
                "request": request,
                "title": "Choose Your Focus Areas",
                "candidate_id": candidate_id or "guest",
                "paths": [
                    {
                        "id": "technical",
                        "name": "Technical Skills",
                        "icon": "⚙️",
                        "description": "Code quality, architecture, testing, and best practices",
                        "time": "15-20 min",
                    },
                    {
                        "id": "design",
                        "name": "Design Thinking",
                        "icon": "🎨",
                        "description": "Problem analysis, solution design, and system architecture",
                        "time": "10-15 min",
                    },
                    {
                        "id": "collaboration",
                        "name": "Collaboration",
                        "icon": "🤝",
                        "description": "Communication, teamwork, and code review practices",
                        "time": "10-15 min",
                    },
                    {
                        "id": "problem_solving",
                        "name": "Problem Solving",
                        "icon": "🧩",
                        "description": "Analytical thinking, debugging, and optimization",
                        "time": "15-20 min",
                    },
                ],
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

    @app.post("/api/assess")
    async def mobile_submit_assessment(submission: MobileSubmission):
        """
        Submit mobile assessment for evaluation.

        Args:
            submission: Mobile assessment submission data

        Returns:
            Assessment result with detailed feedback
        """
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
            return {"success": False, "error": str(e)}

    @app.get("/api/explain/{path}")
    async def mobile_explain_path(path: str):
        """
        Get detailed explanation for a specific path.

        Args:
            path: Path type to explain

        Returns:
            Detailed explanation and guidance
        """
        explanations = {
            "technical": {
                "title": "Technical Skills Assessment",
                "overview": "We'll evaluate your code quality, architecture decisions, and technical practices.",
                "what_we_look_for": [
                    "Clean, readable code structure",
                    "Appropriate use of design patterns",
                    "Error handling and edge cases",
                    "Testing approach and coverage",
                    "Performance considerations",
                ],
                "tips": [
                    "Write code as if others will maintain it",
                    "Add comments only where needed",
                    "Consider edge cases and errors",
                    "Think about scalability",
                ],
            },
            "design": {
                "title": "Design Thinking Assessment",
                "overview": "We'll examine how you approach problems and design solutions.",
                "what_we_look_for": [
                    "Clear problem understanding",
                    "Systematic approach to solutions",
                    "Trade-off considerations",
                    "Architecture and component design",
                    "Scalability thinking",
                ],
                "tips": [
                    "Start with understanding the problem",
                    "Consider multiple approaches",
                    "Think about future changes",
                    "Document your reasoning",
                ],
            },
            "collaboration": {
                "title": "Collaboration Assessment",
                "overview": "We'll look at how you communicate and work with others.",
                "what_we_look_for": [
                    "Clear communication style",
                    "Documentation quality",
                    "Code review practices",
                    "Teamwork indicators",
                    "Knowledge sharing",
                ],
                "tips": [
                    "Write clear commit messages",
                    "Document non-obvious decisions",
                    "Consider the team perspective",
                    "Make code reviewable",
                ],
            },
            "problem_solving": {
                "title": "Problem Solving Assessment",
                "overview": "We'll assess your analytical and debugging capabilities.",
                "what_we_look_for": [
                    "Logical thinking process",
                    "Debugging methodology",
                    "Optimization approach",
                    "Handling complexity",
                    "Creative solutions",
                ],
                "tips": [
                    "Break down complex problems",
                    "Think step by step",
                    "Consider efficiency",
                    "Test your assumptions",
                ],
            },
        }

        path_lower = path.lower()
        if path_lower in explanations:
            return {"success": True, "explanation": explanations[path_lower]}
        else:
            return {"success": False, "error": "Path not found"}

    return app


if __name__ == "__main__":
    import uvicorn

    app = create_mobile_app()
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
