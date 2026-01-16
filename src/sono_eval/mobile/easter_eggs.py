"""
Easter Eggs & Speakeasy Discoveries for Sono-Eval.

Value-driven hidden features that reward exploration with utility.
"""

from typing import Dict, List, Optional

from sono_eval.utils.logger import get_logger

logger = get_logger(__name__)


class EasterEggRegistry:
    """Registry for easter eggs and hidden features."""

    def __init__(self):
        self.eggs: Dict[str, Dict] = {}
        self._register_default_eggs()

    def _register_default_eggs(self):
        """Register default easter eggs."""
        self.register(
            "konami_code",
            {
                "name": "Expert Mode",
                "description": "Unlocks advanced metrics, raw data access, and comparison tools",
                "method": "keyboard",
                "value": "Access to expert-level analysis features",
            },
        )
        self.register(
            "triple_click_logo",
            {
                "name": "Keyboard Shortcuts",
                "description": "Reveals comprehensive keyboard shortcuts cheat sheet",
                "method": "click",
                "value": "Power user productivity tips",
            },
        )
        self.register(
            "insights_url",
            {
                "name": "Insights Dashboard",
                "description": "Unlocks hidden insights dashboard with trend analysis",
                "method": "url",
                "value": "Advanced analytics and trend visualization",
            },
        )
        self.register(
            "deep_dive_comment",
            {
                "name": "Pattern Recognition",
                "description": "Triggers bonus pattern recognition analysis",
                "method": "code",
                "value": "Deeper code analysis and pattern detection",
            },
        )
        self.register(
            "all_paths_complete",
            {
                "name": "Full Profile Analysis",
                "description": "Unlocks cross-path insights and comparison",
                "method": "achievement",
                "value": "Comprehensive skill profile analysis",
            },
        )

    def register(self, egg_id: str, egg_data: Dict):
        """Register an easter egg."""
        self.eggs[egg_id] = egg_data

    def get_egg(self, egg_id: str) -> Optional[Dict]:
        """Get easter egg by ID."""
        return self.eggs.get(egg_id)

    def list_eggs(self) -> List[Dict]:
        """List all registered easter eggs."""
        return list(self.eggs.values())

    def check_code_comment(self, code: str) -> Optional[str]:
        """
        Check if code contains easter egg comments.

        Returns egg_id if found, None otherwise.
        """
        code_lower = code.lower()

        # Deep dive comment
        if "// sono-eval: analyze-architecture" in code_lower or "// deep dive" in code_lower:
            return "deep_dive_comment"

        # Pattern recognition
        if "// sono-eval: pattern-recognition" in code_lower:
            return "pattern_recognition"

        return None


# Global registry instance
_registry = EasterEggRegistry()


def get_registry() -> EasterEggRegistry:
    """Get the global easter egg registry."""
    return _registry


def check_code_for_eggs(code: str) -> List[str]:
    """
    Check code for easter egg patterns.

    Returns list of discovered egg IDs.
    """
    discovered = []
    egg_id = _registry.check_code_comment(code)
    if egg_id:
        discovered.append(egg_id)
    return discovered
