"""Pattern checks for code quality assessment."""

import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List


@dataclass(frozen=True)
class PatternViolation:
    """Structured pattern violation record."""

    pattern: str
    line: int
    code: str
    description: str
    severity: str
    confidence: float = 0.8

    def to_dict(self) -> Dict[str, Any]:
        """Serialize violation to a dictionary for metadata."""
        return {
            "pattern": self.pattern,
            "line": self.line,
            "code": self.code,
            "description": self.description,
            "severity": self.severity,
            "confidence": self.confidence,
        }


PatternRule = Dict[str, str]


DEFAULT_PATTERN_RULES: Dict[str, PatternRule] = {
    "numpy_json_serialization": {
        "regex": r"json\.dumps\([^)]*np\.|json\.dumps\([^)]*numpy",
        "description": "NumPy types in JSON serialization",
        "severity": "high",
    },
    "bounds_checking": {
        "regex": r"\w+\[0\](?!\s+if\s+\w+)",
        "description": "List access without bounds checking",
        "severity": "medium",
    },
    "specific_exceptions": {
        "regex": r"except\s*:",
        "description": "Bare except clause",
        "severity": "medium",
    },
    "structured_logging": {
        "regex": r"\bprint\s*\(",
        "description": "Using print instead of logging",
        "severity": "low",
    },
    "temp_file_handling": {
        "regex": r"tempfile\.mktemp\(",
        "description": "Using deprecated mktemp function",
        "severity": "high",
    },
}


def detect_pattern_violations(
    code: str, rules: Dict[str, PatternRule] | None = None
) -> List[PatternViolation]:
    """Detect pattern violations in code using regex rules."""
    rules = rules or DEFAULT_PATTERN_RULES
    violations: List[PatternViolation] = []

    for line_num, line in enumerate(code.split("\n"), 1):
        for pattern_name, pattern_info in rules.items():
            if re.search(pattern_info["regex"], line):
                violations.append(
                    PatternViolation(
                        pattern=pattern_name,
                        line=line_num,
                        code=line.strip(),
                        description=pattern_info["description"],
                        severity=pattern_info["severity"],
                        confidence=0.8,
                    )
                )

    return violations


def calculate_pattern_penalty(
    violations: Iterable[PatternViolation],
    severity_weights: Dict[str, float],
    max_penalty: float,
) -> float:
    """Calculate a capped penalty score based on unique pattern violations."""
    total_penalty = 0.0
    seen: set[str] = set()

    for violation in violations:
        if violation.pattern in seen:
            continue
        seen.add(violation.pattern)
        total_penalty += severity_weights.get(violation.severity, 0.0)

    return min(max_penalty, total_penalty)


def violations_to_metadata(
    violations: Iterable[PatternViolation],
) -> List[Dict[str, Any]]:
    """Convert pattern violations to metadata-friendly dictionaries."""
    return [violation.to_dict() for violation in violations]
