"""
Session management for Sono-Eval CLI.

Tracks user sessions, provides exit confirmation, and generates session reports.
"""

import json
import signal
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from rich.console import Console
from rich.prompt import Confirm

from sono_eval.utils.config import get_config
from sono_eval.utils.logger import get_logger

console = Console()
logger = get_logger(__name__)


class SessionManager:
    """Manages user sessions with persistence and exit confirmation."""

    def __init__(self, candidate_id: Optional[str] = None):
        """Initialize session manager."""
        self.config = get_config()
        self.candidate_id = candidate_id
        self.session_id = str(uuid4())
        self.start_time = datetime.now(timezone.utc)
        self.end_time: Optional[datetime] = None
        self.assessments: List[Dict[str, Any]] = []
        self.notes: List[str] = []
        self._exit_confirmation_enabled = True
        self._original_signal_handlers: Dict[int, Any] = {}

        # Setup signal handlers for graceful exit
        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        """Setup signal handlers for exit confirmation."""
        if sys.platform != "win32":
            try:
                self._original_signal_handlers[signal.SIGINT] = signal.signal(
                    signal.SIGINT, self._handle_sigint
                )
                self._original_signal_handlers[signal.SIGTERM] = signal.signal(
                    signal.SIGTERM, self._handle_sigterm
                )
            except (ValueError, OSError) as e:
                logger.warning(f"Could not set up signal handlers: {e}")

    def _handle_sigint(self, signum, frame):
        """Handle SIGINT (Ctrl+C) with confirmation."""
        if self._exit_confirmation_enabled:
            if Confirm.ask(
                "\n[yellow]⚠[/yellow]  Exit Sono-Eval? This will end your session."
            ):
                self.end_session()
                sys.exit(0)
            else:
                console.print("[green]Continuing session...[/green]")
        else:
            self.end_session()
            sys.exit(0)

    def _handle_sigterm(self, signum, frame):
        """Handle SIGTERM with confirmation."""
        if self._exit_confirmation_enabled:
            if Confirm.ask(
                "\n[yellow]⚠[/yellow]  Exit Sono-Eval? This will end your session."
            ):
                self.end_session()
                sys.exit(0)
        else:
            self.end_session()
            sys.exit(0)

    def add_assessment(self, assessment_data: Dict[str, Any]):
        """Add an assessment to the session."""
        self.assessments.append(
            {
                **assessment_data,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )
        self._save_session()

    def add_note(self, note: str):
        """Add a note to the session."""
        self.notes.append(f"[{datetime.now(timezone.utc).isoformat()}] {note}")
        self._save_session()

    def end_session(self):
        """End the current session."""
        self.end_time = datetime.now(timezone.utc)
        self._save_session()
        self._restore_signal_handlers()

    def _restore_signal_handlers(self):
        """Restore original signal handlers."""
        for sig, handler in self._original_signal_handlers.items():
            signal.signal(sig, handler)

    def _save_session(self):
        """Save session data to disk."""
        try:
            sessions_dir = Path(self.config.memu_storage_path).parent / "sessions"
            sessions_dir.mkdir(parents=True, exist_ok=True)

            session_data = {
                "session_id": self.session_id,
                "candidate_id": self.candidate_id,
                "start_time": self.start_time.isoformat(),
                "end_time": self.end_time.isoformat() if self.end_time else None,
                "assessments": self.assessments,
                "notes": self.notes,
                "duration_seconds": (
                    (self.end_time or datetime.now(timezone.utc)) - self.start_time
                ).total_seconds(),
            }

            session_file = sessions_dir / f"{self.session_id}.json"
            with open(session_file, "w") as f:
                json.dump(session_data, f, indent=2, default=str)

            logger.debug(f"Saved session {self.session_id}")
        except Exception as e:
            logger.error(f"Failed to save session: {e}")

    def generate_session_report(self) -> Dict[str, Any]:
        """Generate a comprehensive session report."""
        duration = (self.end_time or datetime.now(timezone.utc)) - self.start_time
        duration_str = f"{int(duration.total_seconds() // 60)}m {int(duration.total_seconds() % 60)}s"

        # Calculate statistics
        total_assessments = len(self.assessments)
        avg_score = 0.0
        if total_assessments > 0:
            scores = [
                a.get("overall_score", 0)
                for a in self.assessments
                if "overall_score" in a
            ]
            if scores:
                avg_score = sum(scores) / len(scores)

        # Extract insights
        key_insights: List[str] = []
        recommendations: List[str] = []
        strengths: List[str] = []
        areas_for_improvement: List[str] = []

        for assessment in self.assessments:
            if "key_findings" in assessment:
                key_insights.extend(assessment["key_findings"][:2])
            if "recommendations" in assessment:
                recommendations.extend(assessment["recommendations"][:2])
            if "path_scores" in assessment:
                for ps in assessment["path_scores"]:
                    if "strengths" in ps:
                        strengths.extend(ps["strengths"][:1])
                    if "areas_for_improvement" in ps:
                        areas_for_improvement.extend(ps["areas_for_improvement"][:1])

        # Deduplicate
        key_insights = list(dict.fromkeys(key_insights))[:5]
        recommendations = list(dict.fromkeys(recommendations))[:5]
        strengths = list(dict.fromkeys(strengths))[:5]
        areas_for_improvement = list(dict.fromkeys(areas_for_improvement))[:5]

        return {
            "session_id": self.session_id,
            "candidate_id": self.candidate_id,
            "date": self.start_time.strftime("%Y-%m-%d"),
            "duration": duration_str,
            "total_assessments": total_assessments,
            "average_score": round(avg_score, 2),
            "key_insights": key_insights,
            "recommendations": recommendations,
            "strengths": strengths,
            "areas_for_improvement": areas_for_improvement,
            "notes": self.notes,
        }

    def disable_exit_confirmation(self):
        """Disable exit confirmation (useful for scripts)."""
        self._exit_confirmation_enabled = False

    def enable_exit_confirmation(self):
        """Enable exit confirmation."""
        self._exit_confirmation_enabled = True


# Global session manager instance
_current_session: Optional[SessionManager] = None


def get_session(candidate_id: Optional[str] = None) -> SessionManager:
    """Get or create the current session."""
    global _current_session
    if _current_session is None:
        _current_session = SessionManager(candidate_id)
    return _current_session


def end_current_session():
    """End the current session."""
    global _current_session
    if _current_session:
        _current_session.end_session()
        _current_session = None
