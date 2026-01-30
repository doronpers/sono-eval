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


class TestDashboardChartMethods:
    """Test chart data generation methods."""

    @pytest.fixture
    def dashboard_with_data(self, sample_assessment_result):
        """Create dashboard with populated data."""
        return DashboardData.from_assessment_result(sample_assessment_result)

    @pytest.fixture
    def dashboard_with_trends(self, sample_assessment_result, historical_results):
        """Create dashboard with trend data."""
        return DashboardData.from_assessment_result(
            sample_assessment_result, historical_results=historical_results
        )

    def test_get_progress_ring_data(self, dashboard_with_data):
        """Test progress ring chart data."""
        data = dashboard_with_data.get_progress_ring_data()

        assert data["type"] == "doughnut"
        assert "labels" in data
        assert "datasets" in data
        assert len(data["datasets"]) == 1

        dataset = data["datasets"][0]
        assert len(dataset["data"]) == 2
        score, remaining = dataset["data"]
        assert score + remaining == 100.0

    def test_get_path_breakdown_charts(self, dashboard_with_data):
        """Test path breakdown chart data."""
        charts = dashboard_with_data.get_path_breakdown_charts()

        assert isinstance(charts, list)
        for chart in charts:
            assert chart["type"] == "bar"
            assert "path" in chart
            assert "labels" in chart
            assert "datasets" in chart

    def test_get_path_breakdown_skips_empty(self, sample_assessment_result):
        """Test that path breakdown skips paths with no metrics."""
        # Design path has no metrics breakdown in our fixture
        dashboard = DashboardData.from_assessment_result(sample_assessment_result)
        charts = dashboard.get_path_breakdown_charts()

        # Only Technical path has metrics
        paths_with_charts = [c["path"] for c in charts]
        assert PathType.TECHNICAL.value in paths_with_charts

    def test_get_trend_chart_data_with_trends(self, dashboard_with_trends):
        """Test trend chart data when trends exist."""
        data = dashboard_with_trends.get_trend_chart_data()

        assert data is not None
        assert data["type"] == "line"
        assert "labels" in data
        assert "datasets" in data
        assert len(data["datasets"][0]["data"]) > 0

    def test_get_trend_chart_data_without_trends(self, dashboard_with_data):
        """Test that trend chart returns None when no trend data exists."""
        dashboard_with_data.trend_data = []
        data = dashboard_with_data.get_trend_chart_data()
        assert data is None

    def test_trend_chart_color_improving(self, sample_assessment_result):
        """Test that improving trend uses green color."""
        improving = [
            AssessmentResult(
                candidate_id="test_user",
                assessment_id=f"assess_{i}",
                overall_score=60.0 + (i * 8),
                confidence=0.8,
                summary="Assessment",
                path_scores=[],
                key_findings=[],
                recommendations=[],
            )
            for i in range(5)
        ]
        dashboard = DashboardData.from_assessment_result(
            sample_assessment_result, historical_results=improving
        )
        data = dashboard.get_trend_chart_data()
        assert data is not None
        assert data["datasets"][0]["borderColor"] == "#22c55e"

    def test_trend_chart_color_declining(self, sample_assessment_result):
        """Test that declining trend uses red color."""
        declining = [
            AssessmentResult(
                candidate_id="test_user",
                assessment_id=f"assess_{i}",
                overall_score=95.0 - (i * 8),
                confidence=0.8,
                summary="Assessment",
                path_scores=[],
                key_findings=[],
                recommendations=[],
            )
            for i in range(5)
        ]
        dashboard = DashboardData.from_assessment_result(
            sample_assessment_result, historical_results=declining
        )
        data = dashboard.get_trend_chart_data()
        assert data is not None
        assert data["datasets"][0]["borderColor"] == "#ef4444"

    def test_get_motive_chart_data_with_motives(self, dashboard_with_data):
        """Test motive chart data when motives exist."""
        data = dashboard_with_data.get_motive_chart_data()

        assert data is not None
        assert data["type"] == "bar"
        assert len(data["datasets"][0]["data"]) > 0
        # Strength should be in percentage (0-100)
        assert all(0 <= d <= 100 for d in data["datasets"][0]["data"])

    def test_get_motive_chart_data_without_motives(self, dashboard_with_data):
        """Test that motive chart returns None when no motives exist."""
        dashboard_with_data.motives = []
        data = dashboard_with_data.get_motive_chart_data()
        assert data is None

    def test_get_roi_chart_data(self, dashboard_with_data):
        """Test ROI chart data generation."""
        data = dashboard_with_data.get_roi_chart_data()

        assert data is not None
        assert data["type"] == "bar"
        assert len(data["datasets"][0]["data"]) == 2

    def test_get_roi_chart_data_without_roi(self, dashboard_with_data):
        """Test that ROI chart returns None when no ROI data exists."""
        dashboard_with_data.roi_analysis = None
        data = dashboard_with_data.get_roi_chart_data()
        assert data is None


class TestDashboardEdgeCases:
    """Test edge cases for DashboardData."""

    def test_empty_path_scores(self):
        """Test dashboard creation with no path scores."""
        result = AssessmentResult(
            candidate_id="user",
            assessment_id="assess-empty",
            overall_score=50.0,
            confidence=0.5,
            summary="No paths evaluated.",
            path_scores=[],
            key_findings=[],
            recommendations=[],
        )
        dashboard = DashboardData.from_assessment_result(result)

        assert len(dashboard.path_scores) == 0
        assert dashboard.radar_chart_data == {}
        assert len(dashboard.strengths) == 0
        assert len(dashboard.improvements) == 0

    def test_duplicate_strengths_deduped(self):
        """Test that duplicate strengths are deduplicated."""
        result = AssessmentResult(
            candidate_id="user",
            assessment_id="assess-dup",
            overall_score=80.0,
            confidence=0.8,
            summary="Test",
            path_scores=[
                PathScore(
                    path=PathType.TECHNICAL,
                    overall_score=80.0,
                    metrics=[],
                    strengths=["Strong skills", "Strong skills", "Another strength"],
                    areas_for_improvement=[],
                ),
            ],
            key_findings=[],
            recommendations=[],
        )
        dashboard = DashboardData.from_assessment_result(result)
        assert len(dashboard.strengths) == 2  # Deduped

    def test_strengths_limited_to_five(self):
        """Test that strengths are limited to 5 items."""
        result = AssessmentResult(
            candidate_id="user",
            assessment_id="assess-many",
            overall_score=90.0,
            confidence=0.9,
            summary="Test",
            path_scores=[
                PathScore(
                    path=PathType.TECHNICAL,
                    overall_score=90.0,
                    metrics=[],
                    strengths=[f"Strength {i}" for i in range(10)],
                    areas_for_improvement=[],
                ),
            ],
            key_findings=[],
            recommendations=[],
        )
        dashboard = DashboardData.from_assessment_result(result)
        assert len(dashboard.strengths) <= 5

    def test_all_grade_boundaries(self):
        """Test all grade boundary values."""
        assert DashboardData._score_to_grade(100.0) == "A"
        assert DashboardData._score_to_grade(90.0) == "A"
        assert DashboardData._score_to_grade(89.9) == "B"
        assert DashboardData._score_to_grade(80.0) == "B"
        assert DashboardData._score_to_grade(79.9) == "C"
        assert DashboardData._score_to_grade(70.0) == "C"
        assert DashboardData._score_to_grade(69.9) == "D"
        assert DashboardData._score_to_grade(60.0) == "D"
        assert DashboardData._score_to_grade(59.9) == "F"
        assert DashboardData._score_to_grade(0.0) == "F"

    def test_all_headline_tiers(self):
        """Test all headline generation tiers."""
        for score, expected_fragment in [
            (95.0, "Exceptional"),
            (85.0, "Strong"),
            (75.0, "Solid"),
            (65.0, "Room"),
            (45.0, "Opportunities"),
        ]:
            result = AssessmentResult(
                candidate_id="user",
                assessment_id="assess",
                overall_score=score,
                confidence=0.8,
                summary="Test",
                path_scores=[],
                key_findings=[],
                recommendations=[],
            )
            headline = DashboardData._generate_headline(result)
            assert expected_fragment in headline

    def test_all_confidence_labels(self):
        """Test all confidence label thresholds."""
        for confidence, expected_label in [
            (0.9, "High"),
            (0.8, "High"),
            (0.7, "Medium"),
            (0.6, "Medium"),
            (0.5, "Low"),
            (0.1, "Low"),
        ]:
            result = AssessmentResult(
                candidate_id="user",
                assessment_id="assess",
                overall_score=80.0,
                confidence=confidence,
                summary="Test",
                path_scores=[],
                key_findings=[],
                recommendations=[],
            )
            dashboard = DashboardData.from_assessment_result(result)
            assert dashboard.confidence_label == expected_label

    def test_motive_description_known_types(self):
        """Test motive description for all known types."""
        for motive_type in ["mastery", "efficiency", "quality", "innovation",
                            "collaboration", "exploration"]:
            desc = DashboardData._get_motive_description(motive_type)
            assert len(desc) > 0
            assert desc != "Underlying motivation pattern"

    def test_motive_description_unknown_type(self):
        """Test motive description for unknown type."""
        desc = DashboardData._get_motive_description("unknown_type")
        assert desc == "Underlying motivation pattern"

    def test_dominant_motive_selection(self):
        """Test that dominant motive is the one with highest strength."""
        result = AssessmentResult(
            candidate_id="user",
            assessment_id="assess",
            overall_score=80.0,
            confidence=0.8,
            summary="Test",
            path_scores=[],
            micro_motives=[
                MicroMotive(
                    motive_type=MotiveType.QUALITY,
                    strength=0.5,
                    path_alignment=PathType.TECHNICAL,
                ),
                MicroMotive(
                    motive_type=MotiveType.MASTERY,
                    strength=0.95,
                    path_alignment=PathType.TECHNICAL,
                ),
                MicroMotive(
                    motive_type=MotiveType.EFFICIENCY,
                    strength=0.6,
                    path_alignment=PathType.TECHNICAL,
                ),
            ],
            key_findings=[],
            recommendations=[],
        )
        dashboard = DashboardData.from_assessment_result(result)
        assert dashboard.dominant_motive == "Mastery"

    def test_historical_results_limited_to_10(self):
        """Test that only last 10 historical results are used."""
        result = AssessmentResult(
            candidate_id="user",
            assessment_id="assess",
            overall_score=80.0,
            confidence=0.8,
            summary="Test",
            path_scores=[],
            key_findings=[],
            recommendations=[],
        )
        history = [
            AssessmentResult(
                candidate_id="user",
                assessment_id=f"assess_{i}",
                overall_score=70.0 + i,
                confidence=0.8,
                summary="Hist",
                path_scores=[],
                key_findings=[],
                recommendations=[],
            )
            for i in range(20)
        ]

        dashboard = DashboardData.from_assessment_result(result, historical_results=history)
        assert len(dashboard.trend_data) == 10

    def test_hex_to_rgb(self):
        """Test hex to RGB conversion."""
        assert DashboardData._hex_to_rgb("#ff0000") == "255, 0, 0"
        assert DashboardData._hex_to_rgb("#00ff00") == "0, 255, 0"
        assert DashboardData._hex_to_rgb("#0000ff") == "0, 0, 255"
        assert DashboardData._hex_to_rgb("#ffffff") == "255, 255, 255"

    def test_hex_to_rgba(self):
        """Test hex to RGBA conversion."""
        assert DashboardData._hex_to_rgba("#ff0000", 0.5) == "255, 0, 0, 0.5"
        assert DashboardData._hex_to_rgba("#000000", 1.0) == "0, 0, 0, 1.0"

    def test_get_score_color_hex(self):
        """Test score color mapping."""
        assert DashboardData._get_score_color_hex(90.0) == "#22c55e"  # green
        assert DashboardData._get_score_color_hex(75.0) == "#3b82f6"  # blue
        assert DashboardData._get_score_color_hex(65.0) == "#f59e0b"  # amber
        assert DashboardData._get_score_color_hex(40.0) == "#ef4444"  # red
