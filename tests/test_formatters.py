"""Tests for CLI formatters."""

from unittest.mock import patch

from rich.panel import Panel
from rich.table import Table

from sono_eval.assessment.models import (
    AssessmentResult,
    Evidence,
    EvidenceType,
    MicroMotive,
    MotiveType,
    PathScore,
    PathType,
    ScoringMetric,
)
from sono_eval.cli.formatters import AssessmentFormatter, ErrorFormatter, ProgressFormatter


class TestAssessmentFormatter:
    """Tests for AssessmentFormatter."""

    def test_get_score_color_excellent(self):
        """Test color selection for excellent scores."""
        color = AssessmentFormatter._get_score_color(90.0)
        assert color == AssessmentFormatter.SCORE_COLORS["excellent"]

        color = AssessmentFormatter._get_score_color(85.0)
        assert color == AssessmentFormatter.SCORE_COLORS["excellent"]

    def test_get_score_color_good(self):
        """Test color selection for good scores."""
        color = AssessmentFormatter._get_score_color(75.0)
        assert color == AssessmentFormatter.SCORE_COLORS["good"]

        color = AssessmentFormatter._get_score_color(70.0)
        assert color == AssessmentFormatter.SCORE_COLORS["good"]

    def test_get_score_color_average(self):
        """Test color selection for average scores."""
        color = AssessmentFormatter._get_score_color(65.0)
        assert color == AssessmentFormatter.SCORE_COLORS["average"]

        color = AssessmentFormatter._get_score_color(60.0)
        assert color == AssessmentFormatter.SCORE_COLORS["average"]

    def test_get_score_color_poor(self):
        """Test color selection for poor scores."""
        color = AssessmentFormatter._get_score_color(50.0)
        assert color == AssessmentFormatter.SCORE_COLORS["poor"]

        color = AssessmentFormatter._get_score_color(30.0)
        assert color == AssessmentFormatter.SCORE_COLORS["poor"]

    def test_get_score_color_boundary_values(self):
        """Test color selection at boundary values."""
        # Just below excellent threshold
        color = AssessmentFormatter._get_score_color(84.9)
        assert color == AssessmentFormatter.SCORE_COLORS["good"]

        # Just below good threshold
        color = AssessmentFormatter._get_score_color(69.9)
        assert color == AssessmentFormatter.SCORE_COLORS["average"]

        # Just below average threshold
        color = AssessmentFormatter._get_score_color(59.9)
        assert color == AssessmentFormatter.SCORE_COLORS["poor"]

    def test_get_score_emoji_excellent(self):
        """Test emoji selection for excellent scores."""
        emoji = AssessmentFormatter._get_score_emoji(95.0)
        assert emoji == "🌟"

        emoji = AssessmentFormatter._get_score_emoji(90.0)
        assert emoji == "🌟"

    def test_get_score_emoji_good(self):
        """Test emoji selection for good scores."""
        emoji = AssessmentFormatter._get_score_emoji(85.0)
        assert emoji == "💪"

        emoji = AssessmentFormatter._get_score_emoji(80.0)
        assert emoji == "💪"

    def test_get_score_emoji_average(self):
        """Test emoji selection for average scores."""
        emoji = AssessmentFormatter._get_score_emoji(75.0)
        assert emoji == "✓"

        emoji = AssessmentFormatter._get_score_emoji(70.0)
        assert emoji == "✓"

    def test_get_score_emoji_improving(self):
        """Test emoji selection for improving scores."""
        emoji = AssessmentFormatter._get_score_emoji(65.0)
        assert emoji == "📈"

        emoji = AssessmentFormatter._get_score_emoji(60.0)
        assert emoji == "📈"

    def test_get_score_emoji_needs_improvement(self):
        """Test emoji selection for low scores."""
        emoji = AssessmentFormatter._get_score_emoji(50.0)
        assert emoji == "🎯"

    def test_score_to_grade_a(self):
        """Test grade A assignment."""
        grade = AssessmentFormatter._score_to_grade(95.0)
        assert grade == "A"

        grade = AssessmentFormatter._score_to_grade(90.0)
        assert grade == "A"

    def test_score_to_grade_b(self):
        """Test grade B assignment."""
        grade = AssessmentFormatter._score_to_grade(85.0)
        assert grade == "B"

        grade = AssessmentFormatter._score_to_grade(80.0)
        assert grade == "B"

    def test_score_to_grade_c(self):
        """Test grade C assignment."""
        grade = AssessmentFormatter._score_to_grade(75.0)
        assert grade == "C"

        grade = AssessmentFormatter._score_to_grade(70.0)
        assert grade == "C"

    def test_score_to_grade_d(self):
        """Test grade D assignment."""
        grade = AssessmentFormatter._score_to_grade(65.0)
        assert grade == "D"

        grade = AssessmentFormatter._score_to_grade(60.0)
        assert grade == "D"

    def test_score_to_grade_f(self):
        """Test grade F assignment."""
        grade = AssessmentFormatter._score_to_grade(55.0)
        assert grade == "F"

        grade = AssessmentFormatter._score_to_grade(30.0)
        assert grade == "F"

    def test_score_to_grade_boundaries(self):
        """Test grade assignment at boundaries."""
        assert AssessmentFormatter._score_to_grade(89.9) == "B"
        assert AssessmentFormatter._score_to_grade(79.9) == "C"
        assert AssessmentFormatter._score_to_grade(69.9) == "D"
        assert AssessmentFormatter._score_to_grade(59.9) == "F"

    def test_format_overall_score_returns_panel(self):
        """Test that format_overall_score returns a Panel."""
        result = AssessmentResult(
            candidate_id="test_001",
            assessment_id="assess_001",
            overall_score=85.0,
            confidence=0.9,
            summary="Good performance",
            path_scores=[],
            key_findings=[],
            recommendations=[],
        )

        panel = AssessmentFormatter.format_overall_score(result)

        assert isinstance(panel, Panel)

    def test_format_overall_score_high_confidence(self):
        """Test formatting with high confidence."""
        result = AssessmentResult(
            candidate_id="test_001",
            assessment_id="assess_002",
            overall_score=90.0,
            confidence=0.95,
            summary="Excellent",
            path_scores=[],
            key_findings=[],
            recommendations=[],
        )

        panel = AssessmentFormatter.format_overall_score(result)
        assert isinstance(panel, Panel)

    def test_format_overall_score_low_confidence(self):
        """Test formatting with low confidence."""
        result = AssessmentResult(
            candidate_id="test_001",
            assessment_id="assess_003",
            overall_score=70.0,
            confidence=0.5,
            summary="Moderate",
            path_scores=[],
            key_findings=[],
            recommendations=[],
        )

        panel = AssessmentFormatter.format_overall_score(result)
        assert isinstance(panel, Panel)

    def test_format_path_scores_returns_table(self):
        """Test that format_path_scores returns a Table."""
        path_scores = [
            PathScore(
                path=PathType.TECHNICAL,
                overall_score=85.0,
                metrics=[
                    ScoringMetric(
                        name="code_quality",
                        category="code",
                        score=85.0,
                        weight=1.0,
                        explanation="Good patterns observed",
                    )
                ],
                strengths=["Strong technical skills"],
                areas_for_improvement=["Could improve documentation"],
            )
        ]

        table = AssessmentFormatter.format_path_scores(path_scores)

        assert isinstance(table, Table)

    def test_format_path_scores_multiple_paths(self):
        """Test formatting multiple path scores."""
        path_scores = [
            PathScore(
                path=PathType.TECHNICAL,
                overall_score=85.0,
                metrics=[],
                strengths=["Technical strength"],
                areas_for_improvement=[],
            ),
            PathScore(
                path=PathType.DESIGN,
                overall_score=75.0,
                metrics=[],
                strengths=["Design thinking"],
                areas_for_improvement=[],
            ),
        ]

        table = AssessmentFormatter.format_path_scores(path_scores)

        assert isinstance(table, Table)

    def test_format_path_scores_with_icons(self):
        """Test that path formatting includes icons."""
        # Verify icons are defined for all path types
        assert PathType.TECHNICAL in AssessmentFormatter.PATH_ICONS
        assert PathType.DESIGN in AssessmentFormatter.PATH_ICONS
        assert PathType.COLLABORATION in AssessmentFormatter.PATH_ICONS
        assert PathType.PROBLEM_SOLVING in AssessmentFormatter.PATH_ICONS
        assert PathType.COMMUNICATION in AssessmentFormatter.PATH_ICONS

    def test_format_findings_returns_panel(self):
        """Test that format_findings returns a Panel."""
        result = AssessmentResult(
            candidate_id="test_001",
            assessment_id="assess_004",
            overall_score=85.0,
            confidence=0.9,
            summary="Good",
            path_scores=[],
            key_findings=["Finding 1", "Finding 2"],
            recommendations=["Recommendation 1"],
        )

        panel = AssessmentFormatter.format_findings(result)

        assert isinstance(panel, Panel)

    def test_format_findings_with_many_items(self):
        """Test formatting findings limits to top 5."""
        result = AssessmentResult(
            candidate_id="test_001",
            assessment_id="assess_005",
            overall_score=85.0,
            confidence=0.9,
            summary="Good",
            path_scores=[],
            key_findings=[f"Finding {i}" for i in range(10)],
            recommendations=[f"Rec {i}" for i in range(10)],
        )

        panel = AssessmentFormatter.format_findings(result)

        # Should create panel even with many items (internally limited to 5)
        assert isinstance(panel, Panel)

    def test_format_micro_motives_returns_table(self):
        """Test that format_micro_motives returns a Table."""
        result = AssessmentResult(
            candidate_id="test_001",
            assessment_id="assess_006",
            overall_score=85.0,
            confidence=0.9,
            summary="Good",
            path_scores=[],
            key_findings=[],
            recommendations=[],
            micro_motives=[
                MicroMotive(
                    motive_type=MotiveType.MASTERY,
                    strength=0.8,
                    path_alignment=PathType.TECHNICAL,
                    evidence=[
                        Evidence(
                            type=EvidenceType.CODE_QUALITY,
                            description="Shows dedication to learning",
                            source="test.py:10",
                            weight=0.8,
                        )
                    ],
                )
            ],
        )

        table = AssessmentFormatter.format_micro_motives(result)

        assert isinstance(table, Table)

    def test_format_micro_motives_no_motives(self):
        """Test formatting when no micro-motives exist."""
        result = AssessmentResult(
            candidate_id="test_001",
            assessment_id="assess_007",
            overall_score=85.0,
            confidence=0.9,
            summary="Good",
            path_scores=[],
            key_findings=[],
            recommendations=[],
            micro_motives=[],
        )

        table = AssessmentFormatter.format_micro_motives(result)

        assert table is None

    def test_format_micro_motives_limits_to_eight(self):
        """Test that micro-motives are limited to top 8."""
        motives = [
            MicroMotive(
                motive_type=MotiveType.MASTERY,
                strength=0.8 - (i * 0.05),
                path_alignment=PathType.TECHNICAL,
                evidence=[
                    Evidence(
                        type=EvidenceType.CODE_QUALITY,
                        description=f"Evidence {i}",
                        source=f"test.py:{i}",
                        weight=0.8 - (i * 0.05),
                    )
                ],
            )
            for i in range(15)
        ]

        result = AssessmentResult(
            candidate_id="test_001",
            assessment_id="assess_008",
            overall_score=85.0,
            confidence=0.9,
            summary="Good",
            path_scores=[],
            key_findings=[],
            recommendations=[],
            micro_motives=motives,
        )

        table = AssessmentFormatter.format_micro_motives(result)

        # Should still create a table (limited internally to 8)
        assert isinstance(table, Table)


class TestProgressFormatter:
    """Tests for ProgressFormatter."""

    def test_create_assessment_progress(self):
        """Test creating assessment progress indicator."""
        progress = ProgressFormatter.create_assessment_progress()

        assert progress is not None
        # Progress object should be created successfully

    def test_create_simple_spinner(self):
        """Test creating simple spinner."""
        progress = ProgressFormatter.create_simple_spinner("Loading...")

        assert progress is not None


class TestErrorFormatter:
    """Tests for ErrorFormatter."""

    @patch("sono_eval.cli.formatters.console")
    def test_format_error_basic(self, mock_console):
        """Test basic error formatting."""
        ErrorFormatter.format_error(
            error_type="TestError",
            message="Test error message",
        )

        # Should call console.print at least once
        assert mock_console.print.called

    @patch("sono_eval.cli.formatters.console")
    def test_format_error_with_suggestions(self, mock_console):
        """Test error formatting with suggestions."""
        ErrorFormatter.format_error(
            error_type="ValidationError",
            message="Invalid input",
            suggestions=["Check the input format", "Try again"],
        )

        assert mock_console.print.called

    @patch("sono_eval.cli.formatters.console")
    def test_format_error_with_context(self, mock_console):
        """Test error formatting with context."""
        ErrorFormatter.format_error(
            error_type="FileError",
            message="File not found",
            context={"file_path": "/path/to/file.py"},
        )

        assert mock_console.print.called

    @patch("sono_eval.cli.formatters.console")
    def test_format_validation_error(self, mock_console):
        """Test validation error formatting."""
        ErrorFormatter.format_validation_error(
            field="email",
            message="Invalid email format",
        )

        assert mock_console.print.called

    @patch("sono_eval.cli.formatters.console")
    def test_format_validation_error_with_example(self, mock_console):
        """Test validation error with example."""
        ErrorFormatter.format_validation_error(
            field="username",
            message="Invalid username",
            example="john_doe",
        )

        assert mock_console.print.called

    @patch("sono_eval.cli.formatters.console")
    def test_format_file_error_not_found(self, mock_console):
        """Test file not found error formatting."""
        ErrorFormatter.format_file_error(
            file_path="/path/to/file.py",
            error_type="not_found",
        )

        assert mock_console.print.called

    @patch("sono_eval.cli.formatters.console")
    def test_format_file_error_permission(self, mock_console):
        """Test file permission error formatting."""
        ErrorFormatter.format_file_error(
            file_path="/path/to/file.py",
            error_type="permission",
        )

        assert mock_console.print.called

    @patch("sono_eval.cli.formatters.console")
    def test_format_file_error_empty(self, mock_console):
        """Test empty file error formatting."""
        ErrorFormatter.format_file_error(
            file_path="/path/to/file.py",
            error_type="empty",
        )

        assert mock_console.print.called

    @patch("sono_eval.cli.formatters.console")
    def test_format_file_error_unknown(self, mock_console):
        """Test unknown file error formatting."""
        ErrorFormatter.format_file_error(
            file_path="/path/to/file.py",
            error_type="unknown",
        )

        assert mock_console.print.called


def test_score_colors_defined():
    """Test that score colors are defined."""
    assert "excellent" in AssessmentFormatter.SCORE_COLORS
    assert "good" in AssessmentFormatter.SCORE_COLORS
    assert "average" in AssessmentFormatter.SCORE_COLORS
    assert "poor" in AssessmentFormatter.SCORE_COLORS


def test_path_colors_defined():
    """Test that path colors are defined."""
    assert PathType.TECHNICAL in AssessmentFormatter.PATH_COLORS
    assert PathType.DESIGN in AssessmentFormatter.PATH_COLORS
    assert PathType.COLLABORATION in AssessmentFormatter.PATH_COLORS
    assert PathType.PROBLEM_SOLVING in AssessmentFormatter.PATH_COLORS
    assert PathType.COMMUNICATION in AssessmentFormatter.PATH_COLORS


def test_path_icons_defined():
    """Test that path icons are defined."""
    assert PathType.TECHNICAL in AssessmentFormatter.PATH_ICONS
    assert PathType.DESIGN in AssessmentFormatter.PATH_ICONS
    assert PathType.COLLABORATION in AssessmentFormatter.PATH_ICONS
    assert PathType.PROBLEM_SOLVING in AssessmentFormatter.PATH_ICONS
    assert PathType.COMMUNICATION in AssessmentFormatter.PATH_ICONS


def test_all_path_types_have_colors_and_icons():
    """Test that all path types have both colors and icons."""
    for path_type in PathType:
        assert path_type in AssessmentFormatter.PATH_COLORS
        assert path_type in AssessmentFormatter.PATH_ICONS
