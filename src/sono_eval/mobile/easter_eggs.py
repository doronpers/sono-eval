"""
Easter egg registry for Sono-Eval mobile companion.
"""

from typing import Dict, List, Optional


class EasterEgg:
    """Represents a discoverable feature or hidden content."""

    def __init__(self, id: str, name: str, description: str, discovery_hint: str):
        self.id = id
        self.name = name
        self.description = description
        self.discovery_hint = discovery_hint


class EasterEggRegistry:
    """Registry for managing and listing easter eggs."""

    def __init__(self):
        self._eggs: Dict[str, EasterEgg] = {}
        self._initialize_defaults()

    def _initialize_defaults(self):
        """Add default easter eggs to the registry."""
        default_eggs = [
            EasterEgg(
                "dark_mode_radical",
                "Radical Dark Mode",
                "A Dieter Rams inspired ultra-minimalist theme.",
                "Shake your device 3 times on the home screen.",
            ),
            EasterEgg(
                "hidden_stats",
                "Deep Insights",
                "Unlocks raw performance metrics for your assessment.",
                "Tap the version number 5 times.",
            ),
            EasterEgg(
                "zen_mode",
                "Zen Assessment",
                "Removes all timers and focuses purely on explanation.",
                "Long press the 'Start' button.",
            ),
        ]
        for egg in default_eggs:
            self._eggs[egg.id] = egg

    def list_eggs(self) -> List[Dict[str, str]]:
        """List all available eggs as dictionaries."""
        return [
            {
                "id": egg.id,
                "name": egg.name,
                "description": egg.description,
                "hint": egg.discovery_hint,
            }
            for egg in self._eggs.values()
        ]

    def get_egg(self, egg_id: str) -> Optional[EasterEgg]:
        """Retrieve a specific egg by ID."""
        return self._eggs.get(egg_id)


# Singleton registry instance
_registry = EasterEggRegistry()


def get_registry() -> EasterEggRegistry:
    """Get the global easter egg registry."""
    return _registry
