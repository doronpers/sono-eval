"""Tests for dashboard data generation and visualization."""

from datetime import datetime, timezone

import pytest

from sono_eval.assessment.dashboard import (
    DashboardData,
    DetailedTrendPoint,
    MotiveVisualization,
    PathVisualization,
    ROIAnalysis,
    ScoreBreakdown,
    TrendPoint,
)
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


@pytest.fixture
def sample_assessment_result():
    """Create a sample assessment result for testing."""
    return AssessmentResult(
        candidate_id="test_user",
        assessment_id="assess_001",
        overall_score=85.0,
        confidence=0.9,
        summary="Good performance with strong technical skills",
        path_scores=[
            PathScore(
                path=PathType.TECHNICAL,
                overall_score=90.0,
                metrics=[
                    ScoringMetric(
                        name="code_quality",
                        category="code",
                        score=90.0,
                        weight=1.0,
                        explanation="Excellent code quality",
                    )
                ],
                strengths=["Strong technical skills"],
                areas_for_improvement=["Could improve documentation"],
            ),
            PathScore(
                path=PathType.DESIGN,
                overall_score=80.0,
                metrics=[],
                strengths=["Good design thinking"],
                areas_for_improvement=[],
            ),
        ],
        micro_motives=[
            MicroMotive(
                motive_type=MotiveType.MASTERY,
                strength=0.85,
                path_alignment=PathType.TECHNICAL,
                evidence=[
                    Evidence(
                        type=EvidenceType.CODE_QUALITY,
                        description="Shows dedication to learning",
                        source="test.py:10",
                        weight=0.85,
                    )
                ],
            )
        ],
        key_findings=["Strong technical foundation"],
        recommendations=["Continue practicing"],
    )


@pytest.fixture
def historical_results():
    """Create historical assessment results for trend analysis."""
    return [
        AssessmentResult(
            candidate_id="test_user",
            assessment_id="assess_000",
            overall_score=75.0,
            confidence=0.8,
            summary="Previous assessment",
            path_scores=[],
            key_findings=[],
            recommendations=[],
        ),
        AssessmentResult(
            candidate_id="test_user",
            assessment_id="assess_001",
            overall_score=85.0,
            confidence=0.9,
            summary="Current assessment",
            path_scores=[],
            key_findings=[],
            recommendations=[],
        ),
    ]


class TestDashboardData:
    """Test DashboardData model and transformations."""

    def test_from_assessment_result_basic(self, sample_assessment_result):
        """Test basic dashboard data creation."""
        dashboard = DashboardData.from_assessment_result(sample_assessment_result)

        assert dashboard.overall_score == 85.0
        assert dashboard.confidence == 0.9
        assert dashboard.candidate_id == "test_user"
        assert dashboard.assessment_id == "assess_001"
        assert len(dashboard.path_scores) == 2

    def test_from_assessment_result_with_historical(
        self, sample_assessment_result, historical_results
    ):
        """Test dashboard data creation with historical data."""
        dashboard = DashboardData.from_assessment_result(
            sample_assessment_result, historical_results=historical_results
        )

        assert dashboard.overall_score == 85.0
        assert len(dashboard.trend_data) > 0
        assert dashboard.trend_direction in ["improving", "declining", "stable"]

    def test_score_to_grade(self):
        """Test score to grade conversion."""
        assert DashboardData._score_to_grade(95.0) == "A"
        assert DashboardData._score_to_grade(85.0) == "B"
        assert DashboardData._score_to_grade(75.0) == "C"
        assert DashboardData._score_to_grade(65.0) == "D"
        assert DashboardData._score_to_grade(55.0) == "F"

    def test_generate_headline(self, sample_assessment_result):
        """Test headline generation."""
        dashboard = DashboardData.from_assessment_result(sample_assessment_result)
        assert dashboard.headline
        assert isinstance(dashboard.headline, str)
        assert len(dashboard.headline) > 0

    def test_path_visualizations(self, sample_assessment_result):
        """Test path visualization data."""
        dashboard = DashboardData.from_assessment_result(sample_assessment_result)

        assert len(dashboard.path_scores) == 2
        technical_path = next(
            (p for p in dashboard.path_scores if p.path == PathType.TECHNICAL), None
        )
        assert technical_path is not None
        assert technical_path.score == 90.0
        assert technical_path.icon
        assert technical_path.color

    def test_radar_chart_data(self, sample_assessment_result):
        """Test radar chart data generation."""
        dashboard = DashboardData.from_assessment_result(sample_assessment_result)

        assert isinstance(dashboard.radar_chart_data, dict)
        assert PathType.TECHNICAL.value in dashboard.radar_chart_data
        assert dashboard.radar_chart_data[PathType.TECHNICAL.value] == 90.0

    def test_motive_visualizations(self, sample_assessment_result):
        """Test micro-motive visualization data."""
        dashboard = DashboardData.from_assessment_result(sample_assessment_result)

        assert len(dashboard.motives) > 0
        mastery_motive = next((m for m in dashboard.motives if m.motive_type == "mastery"), None)
        assert mastery_motive is not None
        assert mastery_motive.strength == 0.85

    def test_trend_direction_improving(self, sample_assessment_result):
        """Test trend direction detection for improving scores."""
        improving_history = [
            AssessmentResult(
                candidate_id="test_user",
                assessment_id=f"assess_{i}",
                overall_score=70.0 + (i * 5),
                confidence=0.8,
                summary="Assessment",
                path_scores=[],
                key_findings=[],
                recommendations=[],
            )
            for i in range(5)
        ]

        dashboard = DashboardData.from_assessment_result(
            sample_assessment_result, historical_results=improving_history
        )

        assert dashboard.trend_direction == "improving"

    def test_trend_direction_declining(self, sample_assessment_result):
        """Test trend direction detection for declining scores."""
        declining_history = [
            AssessmentResult(
                candidate_id="test_user",
                assessment_id=f"assess_{i}",
                overall_score=90.0 - (i * 5),
                confidence=0.8,
                summary="Assessment",
                path_scores=[],
                key_findings=[],
                recommendations=[],
            )
            for i in range(5)
        ]

        dashboard = DashboardData.from_assessment_result(
            sample_assessment_result, historical_results=declining_history
        )

        assert dashboard.trend_direction == "declining"

    def test_trend_direction_stable(self, sample_assessment_result):
        """Test trend direction detection for stable scores."""
        stable_history = [
            AssessmentResult(
                candidate_id="test_user",
                assessment_id=f"assess_{i}",
                overall_score=85.0,
                confidence=0.8,
                summary="Assessment",
                path_scores=[],
                key_findings=[],
                recommendations=[],
            )
            for i in range(5)
        ]

        dashboard = DashboardData.from_assessment_result(
            sample_assessment_result, historical_results=stable_history
        )

        assert dashboard.trend_direction == "stable"

    def test_confidence_label(self, sample_assessment_result):
        """Test confidence label assignment."""
        dashboard = DashboardData.from_assessment_result(sample_assessment_result)

        assert dashboard.confidence_label in ["High", "Medium", "Low"]
        assert dashboard.confidence_label == "High"  # 0.9 >= 0.8

    def test_strengths_and_improvements(self, sample_assessment_result):
        """Test strengths and improvements extraction."""
        dashboard = DashboardData.from_assessment_result(sample_assessment_result)

        assert len(dashboard.strengths) > 0
        assert len(dashboard.improvements) > 0
        assert "Strong technical skills" in dashboard.strengths

    def test_recommendations(self, sample_assessment_result):
        """Test recommendations extraction."""
        dashboard = DashboardData.from_assessment_result(sample_assessment_result)

        assert len(dashboard.recommendations) > 0
        assert "Continue practicing" in dashboard.recommendations


class TestDashboardModels:
    """Test dashboard data models."""

    def test_score_breakdown(self):
        """Test ScoreBreakdown model."""
        breakdown = ScoreBreakdown(
            label="Code Quality",
            score=90.0,
            weight=1.0,
            color="#3b82f6",
        )

        assert breakdown.label == "Code Quality"
        assert breakdown.score == 90.0
        assert breakdown.weight == 1.0
        assert breakdown.color == "#3b82f6"

    def test_path_visualization(self):
        """Test PathVisualization model."""
        viz = PathVisualization(
            path=PathType.TECHNICAL,
            score=90.0,
            label="Technical",
            icon="⚙️",
            color="#3b82f6",
            metrics_count=5,
            top_strength="Strong skills",
            top_improvement="Documentation",
        )

        assert viz.path == PathType.TECHNICAL
        assert viz.score == 90.0
        assert viz.label == "Technical"
        assert viz.icon == "⚙️"

    def test_motive_visualization(self):
        """Test MotiveVisualization model."""
        viz = MotiveVisualization(
            motive_type="mastery",
            strength=0.85,
            label="Mastery",
            description="Dedication to learning",
            color="#3b82f6",
        )

        assert viz.motive_type == "mastery"
        assert viz.strength == 0.85
        assert viz.label == "Mastery"

    def test_trend_point(self):
        """Test TrendPoint model."""
        point = TrendPoint(
            timestamp=datetime.now(timezone.utc),
            score=85.0,
            path=PathType.TECHNICAL,
            assessment_id="assess_001",
        )

        assert point.score == 85.0
        assert point.path == PathType.TECHNICAL
        assert point.assessment_id == "assess_001"

    def test_roi_analysis(self):
        """Test ROIAnalysis model."""
        roi = ROIAnalysis(
            time_saved_minutes=300.0,
            efficiency_gain_percent=15.0,
            cost_saving=500.0,
            label="Pattern Application",
            description="Time saved by applying patterns",
        )

        assert roi.time_saved_minutes == 300.0
        assert roi.efficiency_gain_percent == 15.0
        assert roi.cost_saving == 500.0

    def test_detailed_trend_point(self):
        """Test DetailedTrendPoint model."""
        point = DetailedTrendPoint(
            timestamp=datetime.now(timezone.utc),
            metrics={"score": 85.0, "confidence": 0.9},
            velocity=5.0,
            acceleration=1.0,
        )

        assert point.metrics["score"] == 85.0
        assert point.velocity == 5.0
        assert point.acceleration == 1.0
