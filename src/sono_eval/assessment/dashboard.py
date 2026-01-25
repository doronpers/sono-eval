"""Dashboard data models for rich assessment visualization."""

import logging
from datetime import datetime
from typing import Any, ClassVar, Dict, List, Optional

from pydantic import BaseModel, Field

from sono_eval.assessment.models import AssessmentResult, PathType

# from shared_ai_utils import InsightsEngine


class ScoreBreakdown(BaseModel):
    """Breakdown of a score by components."""

    label: str
    score: float
    weight: float
    color: str  # Hex color for visualization


class ROIAnalysis(BaseModel):
    """ROI analysis data."""

    time_saved_minutes: float
    efficiency_gain_percent: float
    cost_saving: float
    label: str
    description: str


class DetailedTrendPoint(BaseModel):
    """Deep trend analysis point."""

    timestamp: datetime
    metrics: Dict[str, float]
    velocity: float
    acceleration: float


class PathVisualization(BaseModel):
    """Visualization data for a path score."""

    path: PathType
    score: float
    label: str
    icon: str
    color: str
    metrics_count: int
    top_strength: Optional[str] = None
    top_improvement: Optional[str] = None
    breakdown: List[ScoreBreakdown] = Field(default_factory=list)


class TrendPoint(BaseModel):
    """Single point in a trend chart."""

    timestamp: datetime
    score: float
    path: Optional[PathType] = None
    assessment_id: str


class MotiveVisualization(BaseModel):
    """Visualization data for micro-motives."""

    motive_type: str
    strength: float
    label: str
    description: str
    color: str


class DashboardData(BaseModel):
    """
    Complete dashboard visualization data.

    This model transforms raw assessment results into
    visualization-ready data structures.
    """

    # Overview
    overall_score: float
    overall_grade: str  # A, B, C, D, F
    confidence: float
    confidence_label: str  # "High", "Medium", "Low"

    # Summary
    summary: str
    headline: str  # Short headline for the result

    # Visualizations
    path_scores: List[PathVisualization]
    radar_chart_data: Dict[str, float]  # For spider/radar chart

    # Findings
    strengths: List[str]
    improvements: List[str]
    recommendations: List[str]

    # Motives (if available)
    motives: List[MotiveVisualization] = Field(default_factory=list)
    dominant_motive: Optional[str] = None

    # Advanced Analytics
    roi_analysis: Optional[ROIAnalysis] = None
    detailed_trends: List[DetailedTrendPoint] = Field(default_factory=list)

    # Trends (if historical data available)
    trend_data: List[TrendPoint] = Field(default_factory=list)
    trend_direction: str = "stable"  # "improving", "declining", "stable"

    # Metadata
    assessment_id: str
    candidate_id: str
    timestamp: datetime
    engine_version: str
    processing_time_ms: Optional[float] = None

    @classmethod
    def from_assessment_result(
        cls,
        result: AssessmentResult,
        historical_results: Optional[List[AssessmentResult]] = None,
    ) -> "DashboardData":
        """Transform AssessmentResult into visualization-ready DashboardData."""
        # Calculate grade
        grade = cls._score_to_grade(result.overall_score)

        # Confidence label
        confidence_label = (
            "High"
            if result.confidence >= 0.8
            else "Medium" if result.confidence >= 0.6 else "Low"
        )

        # Generate headline
        headline = cls._generate_headline(result)

        # Build path visualizations
        path_visualizations = []
        radar_data = {}
        all_strengths = []
        all_improvements = []

        path_colors = {
            PathType.TECHNICAL: "#3b82f6",  # blue
            PathType.DESIGN: "#8b5cf6",  # purple
            PathType.COLLABORATION: "#22c55e",  # green
            PathType.PROBLEM_SOLVING: "#f59e0b",  # amber
            PathType.COMMUNICATION: "#06b6d4",  # cyan
        }

        path_icons = {
            PathType.TECHNICAL: "⚙️",
            PathType.DESIGN: "🎨",
            PathType.COLLABORATION: "🤝",
            PathType.PROBLEM_SOLVING: "🧩",
            PathType.COMMUNICATION: "💬",
        }

        for ps in result.path_scores:
            path_viz = PathVisualization(
                path=ps.path,
                score=ps.overall_score,
                label=ps.path.value.replace("_", " ").title(),
                icon=path_icons.get(ps.path, "📝"),
                color=path_colors.get(ps.path, "#6b7280"),
                metrics_count=len(ps.metrics),
                top_strength=ps.strengths[0] if ps.strengths else None,
                top_improvement=(
                    ps.areas_for_improvement[0] if ps.areas_for_improvement else None
                ),
                breakdown=[
                    ScoreBreakdown(
                        label=m.name,
                        score=m.score,
                        weight=m.weight,
                        color=path_colors.get(ps.path, "#6b7280"),
                    )
                    for m in ps.metrics
                ],
            )
            path_visualizations.append(path_viz)
            radar_data[ps.path.value] = ps.overall_score

            all_strengths.extend(ps.strengths or [])
            all_improvements.extend(ps.areas_for_improvement or [])

        # Build motive visualizations
        motive_visualizations = []
        motive_colors = {
            "mastery": "#3b82f6",
            "efficiency": "#f59e0b",
            "quality": "#22c55e",
            "innovation": "#8b5cf6",
            "collaboration": "#06b6d4",
            "exploration": "#ec4899",
        }

        for motive in result.micro_motives:
            motive_viz = MotiveVisualization(
                motive_type=motive.motive_type.value,
                strength=motive.strength,
                label=motive.motive_type.value.replace("_", " ").title(),
                description=cls._get_motive_description(motive.motive_type.value),
                color=motive_colors.get(motive.motive_type.value.lower(), "#6b7280"),
            )
            motive_visualizations.append(motive_viz)

        dominant_motive = None
        if motive_visualizations:
            dominant_motive = max(motive_visualizations, key=lambda m: m.strength).label

        # Build trend data
        trend_data = []
        trend_direction = "stable"

        if historical_results:
            for hist in historical_results[-10:]:  # Last 10 assessments
                trend_data.append(
                    TrendPoint(
                        timestamp=hist.timestamp,
                        score=hist.overall_score,
                        assessment_id=hist.assessment_id,
                    )
                )

            if len(trend_data) >= 2:
                recent_avg = sum(t.score for t in trend_data[-3:]) / min(
                    3, len(trend_data)
                )
                older_avg = (
                    sum(t.score for t in trend_data[:-3]) / max(1, len(trend_data) - 3)
                    if len(trend_data) > 3
                    else recent_avg
                )

                if recent_avg > older_avg + 5:
                    trend_direction = "improving"
                elif recent_avg < older_avg - 5:
                    trend_direction = "declining"

        # Generate advanced insights
        roi = None
        detailed_trends: List[DetailedTrendPoint] = []

        try:
            # Adapter for InsightsEngine - map AssessmentResult to dict expected by analyzer
            # This is a lightweight integration where we treat the result as a metric set
            # adapter_data = {
            #     "assessment_id": result.assessment_id,
            #     "score": result.overall_score,
            #     "timestamp": result.timestamp.isoformat(),
            #     "metrics": [
            #         {"name": m.name, "score": m.score, "weight": m.weight}
            #         for ps in result.path_scores
            #         for m in ps.metrics
            #     ],
            # }

            # Use shared engine for calculations if applicable
            # For now, we manually construct the logic since InsightsEngine expects
            # a specific protocol, but we'll prepare the data structure
            # In a full integration, we'd pass a Protocol-compliant adapter

            # Simple ROI calculation based on "time to value" proxy (score * complexity)
            roi = ROIAnalysis(
                time_saved_minutes=result.overall_score * 0.5,  # Mock calc
                efficiency_gain_percent=result.overall_score / 100 * 15,
                cost_saving=result.overall_score * 2.5,
                label="Estimated Efficiency",
                description="Projected time savings based on code quality",
            )

        except Exception as e:
            # Fallback if insights generation fails
            logging.getLogger(__name__).warning(
                "Failed to generate advanced insights: %s", str(e)
            )

        return cls(
            overall_score=result.overall_score,
            overall_grade=grade,
            confidence=result.confidence,
            confidence_label=confidence_label,
            summary=result.summary,
            headline=headline,
            path_scores=path_visualizations,
            radar_chart_data=radar_data,
            strengths=list(dict.fromkeys(all_strengths))[:5],  # Dedupe, limit 5
            improvements=list(dict.fromkeys(all_improvements))[:5],
            recommendations=result.recommendations or [],
            motives=motive_visualizations,
            dominant_motive=dominant_motive,
            trend_data=trend_data,
            trend_direction=trend_direction,
            roi_analysis=roi,
            detailed_trends=detailed_trends,
            assessment_id=result.assessment_id,
            candidate_id=result.candidate_id,
            timestamp=result.timestamp,
            engine_version=result.engine_version,
            processing_time_ms=result.processing_time_ms,
        )

    @staticmethod
    def _score_to_grade(score: float) -> str:
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    @staticmethod
    def _generate_headline(result: AssessmentResult) -> str:
        score = result.overall_score
        if score >= 90:
            return "Exceptional Performance! 🌟"
        elif score >= 80:
            return "Strong Results! 💪"
        elif score >= 70:
            return "Solid Foundation ✓"
        elif score >= 60:
            return "Room to Grow 📈"
        else:
            return "Opportunities Ahead 🎯"

    @staticmethod
    def _get_motive_description(motive_type: str) -> str:
        descriptions = {
            "mastery": "Drive to deeply understand and excel",
            "efficiency": "Focus on optimizing and streamlining",
            "quality": "Commitment to excellence and correctness",
            "innovation": "Desire to create and explore new approaches",
            "collaboration": "Value placed on teamwork and communication",
            "exploration": "Curiosity and willingness to investigate",
        }
        return descriptions.get(motive_type.lower(), "Underlying motivation pattern")

    # Chart-ready data methods

    def get_radar_chart_data(self) -> Dict[str, Any]:
        """
        Get data formatted for a radar/spider chart.

        Returns:
            Dictionary with labels and dataset for Chart.js radar chart
        """
        labels = []
        data = []
        background_colors = []

        for path_viz in self.path_scores:
            labels.append(path_viz.label)
            data.append(path_viz.score)
            background_colors.append(path_viz.color)

        return {
            "type": "radar",
            "labels": labels,
            "datasets": [
                {
                    "label": "Path Scores",
                    "data": data,
                    "backgroundColor": f"rgba({self._hex_to_rgba(self.PATH_COLORS.get(PathType.TECHNICAL, '#3b82f6'), 0.2)})",  # noqa: E501
                    "borderColor": f"rgb({self._hex_to_rgb(self.PATH_COLORS.get(PathType.TECHNICAL, '#3b82f6'))})",  # noqa: E501
                    "borderWidth": 2,
                    "pointBackgroundColor": background_colors,
                    "pointBorderColor": "#fff",
                    "pointHoverBackgroundColor": "#fff",
                    "pointHoverBorderColor": background_colors,
                }
            ],
            "options": {
                "scales": {
                    "r": {
                        "beginAtZero": True,
                        "max": 100,
                        "ticks": {"stepSize": 20},
                    }
                },
                "plugins": {"legend": {"display": False}},
            },
        }

    def get_progress_ring_data(self) -> Dict[str, Any]:
        """
        Get data for progress ring/doughnut chart showing overall completion.

        Returns:
            Dictionary with data for Chart.js doughnut chart
        """
        score = self.overall_score
        remaining = 100 - score

        return {
            "type": "doughnut",
            "labels": ["Score", "Remaining"],
            "datasets": [
                {
                    "data": [score, remaining],
                    "backgroundColor": [
                        self._get_score_color_hex(score),
                        "#e5e7eb",  # gray for remaining
                    ],
                    "borderWidth": 0,
                    "cutout": "75%",
                }
            ],
            "options": {
                "plugins": {
                    "legend": {"display": False},
                    "tooltip": {"enabled": False},
                },
                "rotation": -90,
                "circumference": 180,
            },
        }

    def get_path_breakdown_charts(self) -> List[Dict[str, Any]]:
        """
        Get individual breakdown charts for each path.

        Returns:
            List of chart configurations, one per path
        """
        charts = []

        for path_viz in self.path_scores:
            if not path_viz.breakdown:
                continue

            labels = [b.label for b in path_viz.breakdown]
            data = [b.score for b in path_viz.breakdown]
            colors = [b.color for b in path_viz.breakdown]

            chart_data = {
                "type": "bar",
                "path": path_viz.path.value,
                "labels": labels,
                "datasets": [
                    {
                        "label": "Score",
                        "data": data,
                        "backgroundColor": colors,
                        "borderRadius": 8,
                    }
                ],
                "options": {
                    "indexAxis": "y",  # Horizontal bars
                    "scales": {
                        "x": {"beginAtZero": True, "max": 100},
                    },
                    "plugins": {
                        "legend": {"display": False},
                    },
                },
            }
            charts.append(chart_data)

        return charts

    def get_trend_chart_data(self) -> Optional[Dict[str, Any]]:
        """
        Get data for trend line chart showing score history.

        Returns:
            Dictionary with data for Chart.js line chart, or None if no trend data
        """
        if not self.trend_data:
            return None

        labels = [t.timestamp.strftime("%m/%d %H:%M") for t in self.trend_data]
        data = [t.score for t in self.trend_data]

        # Determine trend color
        trend_color = (
            "#22c55e"
            if self.trend_direction == "improving"
            else "#ef4444" if self.trend_direction == "declining" else "#6b7280"
        )

        return {
            "type": "line",
            "labels": labels,
            "datasets": [
                {
                    "label": "Score Over Time",
                    "data": data,
                    "borderColor": trend_color,
                    "backgroundColor": f"rgba({self._hex_to_rgba(trend_color, 0.1)})",
                    "tension": 0.4,
                    "fill": True,
                    "pointRadius": 4,
                    "pointHoverRadius": 6,
                }
            ],
            "options": {
                "scales": {
                    "y": {"beginAtZero": True, "max": 100},
                },
                "plugins": {
                    "legend": {"display": False},
                },
            },
        }

    def get_motive_chart_data(self) -> Optional[Dict[str, Any]]:
        """
        Get data for micro-motives bar chart.

        Returns:
            Dictionary with data for Chart.js horizontal bar chart, or None if no motives
        """
        if not self.motives:
            return None

        # Sort by strength
        sorted_motives = sorted(self.motives, key=lambda m: m.strength, reverse=True)[
            :8
        ]  # Top 8

        labels = [m.label for m in sorted_motives]
        data = [m.strength * 100 for m in sorted_motives]  # Convert to percentage
        colors = [m.color for m in sorted_motives]

        return {
            "type": "bar",
            "labels": labels,
            "datasets": [
                {
                    "label": "Strength",
                    "data": data,
                    "backgroundColor": colors,
                    "borderRadius": 8,
                }
            ],
            "options": {
                "indexAxis": "y",  # Horizontal bars
                "scales": {
                    "x": {"beginAtZero": True, "max": 100},
                },
                "plugins": {
                    "legend": {"display": False},
                },
            },
        }

    def get_roi_chart_data(self) -> Optional[Dict[str, Any]]:
        """
        Get data for ROI visualization.

        Returns:
            Chart.js data for ROI metrics
        """
        if not self.roi_analysis:
            return None

        return {
            "type": "bar",
            "labels": ["Time Saved (min)", "Cost Saving ($)"],
            "datasets": [
                {
                    "label": "Projected Savings",
                    "data": [
                        self.roi_analysis.time_saved_minutes,
                        self.roi_analysis.cost_saving,
                    ],
                    "backgroundColor": ["#3b82f6", "#22c55e"],
                    "borderRadius": 8,
                }
            ],
            "options": {
                "plugins": {"legend": {"display": False}},
                "scales": {"y": {"beginAtZero": True}},
            },
        }

    @staticmethod
    def _hex_to_rgb(hex_color: str) -> str:
        """Convert hex color to RGB string."""
        hex_color = hex_color.lstrip("#")
        r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
        return f"{r}, {g}, {b}"

    @staticmethod
    def _hex_to_rgba(hex_color: str, alpha: float) -> str:
        """Convert hex color to RGBA string."""
        hex_color = hex_color.lstrip("#")
        r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
        return f"{r}, {g}, {b}, {alpha}"

    @staticmethod
    def _get_score_color_hex(score: float) -> str:
        """Get hex color for a score value."""
        if score >= 85:
            return "#22c55e"  # green
        elif score >= 70:
            return "#3b82f6"  # blue
        elif score >= 60:
            return "#f59e0b"  # amber
        else:
            return "#ef4444"  # red

    PATH_COLORS: ClassVar[Dict[PathType, str]] = {
        PathType.TECHNICAL: "#3b82f6",
        PathType.DESIGN: "#8b5cf6",
        PathType.COLLABORATION: "#22c55e",
        PathType.PROBLEM_SOLVING: "#f59e0b",
        PathType.COMMUNICATION: "#06b6d4",
    }
