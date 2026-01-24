"""
ML utilities for code analysis and readability scoring.

Provides AST-based code complexity analysis and text readability metrics
without requiring heavy ML frameworks.
"""

import ast
import re
from typing import Dict, List

import textstat  # type: ignore

from sono_eval.utils.logger import get_logger

logger = get_logger(__name__)


class CodeComplexityAnalyzer:
    """Analyze code complexity using Python's AST module."""

    @staticmethod
    def analyze(code: str) -> Dict[str, float]:
        """
        Analyze code complexity metrics.

        Args:
            code: Python source code to analyze

        Returns:
            Dictionary with complexity metrics
        """
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            logger.debug(f"Code parsing failed: {e}")
            return {
                "cyclomatic_complexity": 0.0,
                "nesting_depth": 0.0,
                "function_length_avg": 0.0,
                "class_count": 0,
                "function_count": 0,
            }

        analyzer = _ComplexityVisitor()
        analyzer.visit(tree)

        return {
            "cyclomatic_complexity": analyzer.complexity,
            "nesting_depth": analyzer.max_nesting,
            "function_length_avg": analyzer.avg_function_length,
            "class_count": analyzer.class_count,
            "function_count": analyzer.function_count,
        }


class _ComplexityVisitor(ast.NodeVisitor):
    """AST visitor for calculating complexity metrics."""

    def __init__(self):
        self.complexity = 1  # Base complexity
        self.max_nesting = 0
        self.current_nesting = 0
        self.function_count = 0
        self.class_count = 0
        self.function_lengths: List[int] = []

    def visit_If(self, node):
        self.complexity += 1
        self._track_nesting(node)

    def visit_For(self, node):
        self.complexity += 1
        self._track_nesting(node)

    def visit_While(self, node):
        self.complexity += 1
        self._track_nesting(node)

    def visit_ExceptHandler(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_With(self, node):
        self.complexity += 1
        self._track_nesting(node)

    def visit_FunctionDef(self, node):
        self.function_count += 1
        # Count lines in function
        if hasattr(node, "lineno") and hasattr(node, "end_lineno"):
            length = node.end_lineno - node.lineno + 1
            self.function_lengths.append(length)
        self._track_nesting(node)

    def visit_AsyncFunctionDef(self, node):
        self.function_count += 1
        if hasattr(node, "lineno") and hasattr(node, "end_lineno"):
            length = node.end_lineno - node.lineno + 1
            self.function_lengths.append(length)
        self._track_nesting(node)

    def visit_ClassDef(self, node):
        self.class_count += 1
        self._track_nesting(node)

    def _track_nesting(self, node):
        """Track nesting depth."""
        self.current_nesting += 1
        self.max_nesting = max(self.max_nesting, self.current_nesting)
        self.generic_visit(node)
        self.current_nesting -= 1

    @property
    def avg_function_length(self) -> float:
        """Calculate average function length."""
        if not self.function_lengths:
            return 0.0
        return sum(self.function_lengths) / len(self.function_lengths)


class ReadabilityAnalyzer:
    """Analyze text readability using textstat library."""

    @staticmethod
    def analyze(text: str) -> Dict[str, float]:
        """
        Analyze text readability metrics.

        Args:
            text: Text content to analyze (docstrings, comments, documentation)

        Returns:
            Dictionary with readability scores
        """
        if not text or len(text.strip()) < 10:
            return {
                "flesch_reading_ease": 0.0,
                "flesch_kincaid_grade": 0.0,
                "gunning_fog": 0.0,
                "smog_index": 0.0,
                "automated_readability_index": 0.0,
            }

        try:
            return {
                "flesch_reading_ease": textstat.flesch_reading_ease(text),
                "flesch_kincaid_grade": textstat.flesch_kincaid_grade(text),
                "gunning_fog": textstat.gunning_fog(text),
                "smog_index": textstat.smog_index(text),
                "automated_readability_index": textstat.automated_readability_index(text),
            }
        except Exception as e:
            logger.debug(f"Readability analysis failed: {e}")
            return {
                "flesch_reading_ease": 0.0,
                "flesch_kincaid_grade": 0.0,
                "gunning_fog": 0.0,
                "smog_index": 0.0,
                "automated_readability_index": 0.0,
            }


class NamingConventionValidator:
    """Validate naming conventions in code."""

    SNAKE_CASE_PATTERN = re.compile(r"^[a-z_][a-z0-9_]*$")
    PASCAL_CASE_PATTERN = re.compile(r"^[A-Z][a-zA-Z0-9]*$")
    CAMEL_CASE_PATTERN = re.compile(r"^[a-z][a-zA-Z0-9]*$")
    SCREAMING_SNAKE_CASE_PATTERN = re.compile(r"^[A-Z_][A-Z0-9_]*$")

    @classmethod
    def analyze(cls, code: str) -> Dict[str, float]:
        """
        Analyze naming convention consistency.

        Args:
            code: Python source code to analyze

        Returns:
            Dictionary with naming convention scores
        """
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return {
                "snake_case_ratio": 0.0,
                "pascal_case_ratio": 0.0,
                "consistency": 0.0,
            }

        visitor = _NamingVisitor()
        visitor.visit(tree)

        total_names = visitor.total_identifiers
        if total_names == 0:
            return {
                "snake_case_ratio": 0.0,
                "pascal_case_ratio": 0.0,
                "consistency": 0.0,
            }

        snake_ratio = visitor.snake_case_count / total_names
        pascal_ratio = visitor.pascal_case_count / total_names

        # Consistency is high if one convention dominates
        consistency = max(snake_ratio, pascal_ratio)

        return {
            "snake_case_ratio": snake_ratio,
            "pascal_case_ratio": pascal_ratio,
            "consistency": consistency,
        }


class _NamingVisitor(ast.NodeVisitor):
    """AST visitor for checking naming conventions."""

    def __init__(self):
        self.total_identifiers = 0
        self.snake_case_count = 0
        self.pascal_case_count = 0

    def visit_FunctionDef(self, node):
        self._check_name(node.name, expected_snake=True)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self._check_name(node.name, expected_snake=True)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self._check_name(node.name, expected_pascal=True)
        self.generic_visit(node)

    def visit_Name(self, node):
        # Check variable names
        if isinstance(node.ctx, ast.Store):
            self._check_name(node.id, expected_snake=True)
        self.generic_visit(node)

    def _check_name(self, name: str, expected_snake=False, expected_pascal=False):
        """Check if name follows conventions."""
        # Skip private/magic names
        if name.startswith("_"):
            return

        self.total_identifiers += 1

        if NamingConventionValidator.SNAKE_CASE_PATTERN.match(name):
            self.snake_case_count += 1
        elif NamingConventionValidator.PASCAL_CASE_PATTERN.match(name):
            self.pascal_case_count += 1


def calculate_confidence_from_evidence(evidence_count: int, metric_variance: float = 0.0) -> float:
    """
    Calculate confidence score based on evidence strength.

    Args:
        evidence_count: Number of evidence points collected
        metric_variance: Variance in metric scores (0-1)

    Returns:
        Confidence score between 0 and 1
    """
    # More evidence = higher confidence (up to 0.9)
    evidence_factor = min(0.9, evidence_count * 0.15)

    # Lower variance = higher confidence
    variance_penalty = metric_variance * 0.3

    confidence = max(0.1, min(1.0, evidence_factor - variance_penalty))
    return confidence


def extract_docstrings_and_comments(code: str) -> str:
    """
    Extract docstrings and comments from Python code.

    Args:
        code: Python source code

    Returns:
        Combined text from docstrings and comments
    """
    parts: List[str] = []

    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                docstring = ast.get_docstring(node)
                if docstring:
                    parts.append(docstring)
    except SyntaxError:
        pass

    # Extract comments
    for line in code.split("\n"):
        stripped = line.strip()
        if stripped.startswith("#"):
            parts.append(stripped[1:].strip())

    return " ".join(parts)
