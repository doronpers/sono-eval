"""
Dashboard data models for rich assessment visualization.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from sono_eval.assessment.models import AssessmentResult, PathType


class ScoreBreakdown(BaseModel):
    """Breakdown of a score by components."""

    label: str
    score: float
    weight: float
    color: str  # Hex color for visualization


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
        """
        Transform AssessmentResult into visualization-ready DashboardData.
        """
        # Calculate grade
        grade = cls._score_to_grade(result.overall_score)

        # Confidence label
        confidence_label = (
            "High" if result.confidence >= 0.8 else "Medium" if result.confidence >= 0.6 else "Low"
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
                top_improvement=(ps.areas_for_improvement[0] if ps.areas_for_improvement else None),
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
                recent_avg = sum(t.score for t in trend_data[-3:]) / min(3, len(trend_data))
                older_avg = (
                    sum(t.score for t in trend_data[:-3]) / max(1, len(trend_data) - 3)
                    if len(trend_data) > 3
                    else recent_avg
                )

                if recent_avg > older_avg + 5:
                    trend_direction = "improving"
                elif recent_avg < older_avg - 5:
                    trend_direction = "declining"

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
