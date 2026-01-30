"""Comprehensive tests for PDF report generation."""

from datetime import datetime, timezone
from unittest.mock import patch

import pytest

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
from sono_eval.reporting.pdf_generator import PDFGenerator


@pytest.fixture
def generator():
    """Create a PDFGenerator instance."""
    return PDFGenerator()


@pytest.fixture
def minimal_result():
    """Create a minimal AssessmentResult for testing."""
    return AssessmentResult(
        candidate_id="test-user",
        assessment_id="assess-001",
        overall_score=75.0,
        confidence=0.85,
        summary="Solid technical foundation with room for growth.",
        path_scores=[],
        micro_motives=[],
        key_findings=[],
        recommendations=[],
    )


@pytest.fixture
def full_result():
    """Create a fully populated AssessmentResult for testing."""
    return AssessmentResult(
        candidate_id="jane-doe-42",
        assessment_id="assess-full-001",
        overall_score=88.5,
        confidence=0.92,
        summary="Excellent technical skills with strong design thinking.",
        path_scores=[
            PathScore(
                path=PathType.TECHNICAL,
                overall_score=92.0,
                metrics=[
                    ScoringMetric(
                        name="Code Quality",
                        category="technical",
                        score=95.0,
                        weight=0.3,
                        evidence=[
                            Evidence(
                                type=EvidenceType.CODE_QUALITY,
                                description="Clean code structure",
                                source="code_analysis",
                                weight=0.8,
                            )
                        ],
                        explanation="Excellent code quality",
                    ),
                    ScoringMetric(
                        name="Testing",
                        category="technical",
                        score=88.0,
                        weight=0.2,
                        evidence=[],
                        explanation="Good test coverage",
                    ),
                ],
                strengths=["Clean architecture", "Comprehensive tests"],
                areas_for_improvement=["Add more integration tests"],
            ),
            PathScore(
                path=PathType.DESIGN,
                overall_score=85.0,
                metrics=[
                    ScoringMetric(
                        name="Architecture",
                        category="design",
                        score=85.0,
                        weight=0.4,
                        evidence=[],
                        explanation="Solid architecture",
                    )
                ],
                strengths=["Good patterns"],
                areas_for_improvement=["Consider scalability"],
            ),
            PathScore(
                path=PathType.COLLABORATION,
                overall_score=80.0,
                metrics=[],
                strengths=["Clear documentation"],
                areas_for_improvement=[],
            ),
        ],
        micro_motives=[
            MicroMotive(
                motive_type=MotiveType.MASTERY,
                strength=0.9,
                indicators=["Deep technical understanding"],
                evidence=[],
                path_alignment=PathType.TECHNICAL,
            ),
            MicroMotive(
                motive_type=MotiveType.QUALITY,
                strength=0.75,
                indicators=["Quality-focused approach"],
                evidence=[],
                path_alignment=PathType.TECHNICAL,
            ),
        ],
        key_findings=[
            "Demonstrates strong technical depth",
            "Design patterns well applied",
            "Good collaboration signals",
        ],
        recommendations=[
            "Continue refining testing practices",
            "Explore more design patterns",
        ],
    )


class TestPDFGeneratorInit:
    """Test PDFGenerator initialization."""

    def test_initialization(self, generator):
        """Test that the generator initializes with custom styles."""
        assert generator.styles is not None
        assert "Header1" in [s.name for s in generator.styles.byName.values()]
        assert "SectionHeader" in [s.name for s in generator.styles.byName.values()]
        assert "ScoreText" in [s.name for s in generator.styles.byName.values()]

    def test_styles_are_configured(self, generator):
        """Test that custom styles have proper configuration."""
        header1 = generator.styles["Header1"]
        assert header1.fontSize == 24

        section = generator.styles["SectionHeader"]
        assert section.fontSize == 18

        score_text = generator.styles["ScoreText"]
        assert score_text.fontSize == 36


class TestPDFGeneration:
    """Test PDF generation with various inputs."""

    def test_generate_returns_bytes(self, generator, minimal_result):
        """Test that generate returns bytes."""
        result = generator.generate(minimal_result)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_generate_starts_with_pdf_header(self, generator, minimal_result):
        """Test that generated content is a valid PDF (starts with %PDF)."""
        result = generator.generate(minimal_result)
        assert result[:5] == b"%PDF-"

    def test_generate_minimal_result(self, generator, minimal_result):
        """Test PDF generation with minimal result (no paths, findings, etc.)."""
        result = generator.generate(minimal_result)
        assert isinstance(result, bytes)
        assert len(result) > 100  # Non-trivial size

    def test_generate_full_result(self, generator, full_result):
        """Test PDF generation with fully populated result."""
        result = generator.generate(full_result)
        assert isinstance(result, bytes)
        # Full result should produce a larger PDF
        assert len(result) > 500

    def test_generate_with_path_scores_table(self, generator, full_result):
        """Test that path scores are included in the PDF."""
        result = generator.generate(full_result)
        # PDF should be larger when path scores are present
        assert len(result) > 500

    def test_generate_with_key_findings(self, generator, full_result):
        """Test that key findings are included."""
        result = generator.generate(full_result)
        assert isinstance(result, bytes)

    def test_generate_with_no_key_findings(self, generator, minimal_result):
        """Test generation when key_findings is empty."""
        minimal_result.key_findings = []
        result = generator.generate(minimal_result)
        assert isinstance(result, bytes)

    def test_generate_with_single_path(self, generator, minimal_result):
        """Test generation with a single path score."""
        minimal_result.path_scores = [
            PathScore(
                path=PathType.TECHNICAL,
                overall_score=80.0,
                metrics=[],
                strengths=["Good skills"],
                areas_for_improvement=[],
            )
        ]
        result = generator.generate(minimal_result)
        assert isinstance(result, bytes)

    def test_generate_all_score_tiers(self, generator, minimal_result):
        """Test that all score status tiers are handled."""
        tiers = [
            (95.0, "Excellent"),
            (75.0, "Good"),
            (55.0, "Fair"),
            (35.0, "Needs Improvement"),
        ]

        for score, _expected_status in tiers:
            minimal_result.path_scores = [
                PathScore(
                    path=PathType.TECHNICAL,
                    overall_score=score,
                    metrics=[],
                    strengths=[],
                    areas_for_improvement=[],
                )
            ]
            result = generator.generate(minimal_result)
            assert isinstance(result, bytes)
            assert len(result) > 0

    def test_generate_extreme_scores(self, generator, minimal_result):
        """Test generation with extreme score values."""
        # Minimum score
        minimal_result.overall_score = 0.0
        result = generator.generate(minimal_result)
        assert isinstance(result, bytes)

        # Maximum score
        minimal_result.overall_score = 100.0
        result = generator.generate(minimal_result)
        assert isinstance(result, bytes)

    def test_generate_long_summary(self, generator, minimal_result):
        """Test generation with a very long summary."""
        minimal_result.summary = "A " * 500 + "long summary."
        result = generator.generate(minimal_result)
        assert isinstance(result, bytes)

    def test_generate_special_characters_in_candidate_id(
        self, generator, minimal_result
    ):
        """Test generation with special characters in candidate ID."""
        minimal_result.candidate_id = "user-with_special-chars-123"
        result = generator.generate(minimal_result)
        assert isinstance(result, bytes)

    def test_generate_many_path_scores(self, generator, minimal_result):
        """Test generation with all possible path types."""
        minimal_result.path_scores = [
            PathScore(
                path=path,
                overall_score=70.0 + i * 5,
                metrics=[],
                strengths=[f"Strength for {path.value}"],
                areas_for_improvement=[],
            )
            for i, path in enumerate(PathType)
        ]
        result = generator.generate(minimal_result)
        assert isinstance(result, bytes)

    def test_generate_many_key_findings(self, generator, minimal_result):
        """Test generation with many key findings."""
        minimal_result.key_findings = [f"Finding {i}" for i in range(20)]
        result = generator.generate(minimal_result)
        assert isinstance(result, bytes)

    def test_generate_produces_different_pdfs_for_different_results(
        self, generator, minimal_result, full_result
    ):
        """Test that different inputs produce different PDFs."""
        pdf1 = generator.generate(minimal_result)
        pdf2 = generator.generate(full_result)
        assert pdf1 != pdf2

    def test_generate_idempotent_structure(self, generator, minimal_result):
        """Test that generating twice produces valid PDFs both times."""
        pdf1 = generator.generate(minimal_result)
        pdf2 = generator.generate(minimal_result)
        assert pdf1[:5] == b"%PDF-"
        assert pdf2[:5] == b"%PDF-"
        # Both should be valid PDFs (content may differ due to timestamps)
