"""
Personalization utilities for Sono-Eval CLI.

Provides personalized experience based on past interactions.
"""

from typing import Any, Dict, List

from sono_eval.memory.memu import MemUStorage
from sono_eval.utils.config import get_config
from sono_eval.utils.logger import get_logger

logger = get_logger(__name__)


class PersonalizationEngine:
    """Provides personalized experience based on user history."""

    def __init__(self, candidate_id: str):
        """Initialize personalization engine."""
        self.candidate_id = candidate_id
        self.storage = MemUStorage()
        self.config = get_config()

    def get_user_profile(self) -> Dict[str, Any]:
        """Get user profile with past interaction data."""
        memory = self.storage.get_candidate_memory(self.candidate_id)

        if not memory:
            return {
                "candidate_id": self.candidate_id,
                "total_assessments": 0,
                "average_score": 0.0,
                "preferred_paths": [],
                "improvement_areas": [],
                "strengths": [],
                "recent_topics": [],
            }

        # Collect assessment data
        assessments = []
        for node in memory.nodes.values():
            if node.metadata.get("type") == "assessment":
                result_data = node.data.get("assessment_result")
                if result_data:
                    assessments.append(result_data)

        # Calculate statistics
        total_assessments = len(assessments)
        scores = [
            a.get("overall_score", 0) for a in assessments if "overall_score" in a
        ]
        average_score = sum(scores) / len(scores) if scores else 0.0

        # Analyze preferred paths
        path_counts: Dict[str, int] = {}
        for assessment in assessments:
            if "path_scores" in assessment:
                for ps in assessment["path_scores"]:
                    path = (
                        ps.get("path", {}).get("value", "")
                        if isinstance(ps.get("path"), dict)
                        else str(ps.get("path", ""))
                    )
                    if path:
                        path_counts[path] = path_counts.get(path, 0) + 1

        sorted_paths = sorted(path_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        preferred_paths = [path for path, _ in sorted_paths]

        # Extract improvement areas and strengths
        improvement_areas: List[str] = []
        strengths: List[str] = []

        for assessment in assessments[-5:]:  # Last 5 assessments
            if "path_scores" in assessment:
                for ps in assessment["path_scores"]:
                    if "areas_for_improvement" in ps:
                        improvement_areas.extend(ps["areas_for_improvement"][:2])
                    if "strengths" in ps:
                        strengths.extend(ps["strengths"][:2])

        # Deduplicate
        improvement_areas = list(dict.fromkeys(improvement_areas))[:5]
        strengths = list(dict.fromkeys(strengths))[:5]

        # Extract recent topics from summaries
        recent_topics = []
        for assessment in assessments[-3:]:
            summary = assessment.get("summary", "")
            if summary:
                # Extract key phrases (simple approach)
                words = summary.lower().split()
                recent_topics.extend([w for w in words if len(w) > 4][:3])

        recent_topics = list(dict.fromkeys(recent_topics))[:5]

        return {
            "candidate_id": self.candidate_id,
            "total_assessments": total_assessments,
            "average_score": round(average_score, 2),
            "preferred_paths": preferred_paths,
            "improvement_areas": improvement_areas,
            "strengths": strengths,
            "recent_topics": recent_topics,
            "last_assessment_date": (
                assessments[-1].get("timestamp", "")[:10] if assessments else None
            ),
        }

    def get_personalized_recommendations(self) -> List[str]:
        """Get personalized recommendations based on user history."""
        profile = self.get_user_profile()
        recommendations = []

        if profile["total_assessments"] == 0:
            recommendations.append(
                "Start with a technical assessment to establish your baseline"
            )
            recommendations.append(
                "Try different assessment paths to discover your strengths"
            )
        elif profile["total_assessments"] < 3:
            recommendations.append(
                "Continue building your assessment history for better insights"
            )
            if profile["average_score"] < 70:
                recommendations.append(
                    "Focus on the improvement areas identified in your assessments"
                )
        else:
            if profile["average_score"] < 60:
                recommendations.append(
                    "Consider focusing on fundamental skills before advanced topics"
                )
            elif profile["average_score"] > 85:
                recommendations.append(
                    "Explore more challenging assessments to continue growing"
                )

            if profile["improvement_areas"]:
                recommendations.append(
                    f"Work on: {', '.join(profile['improvement_areas'][:2])}"
                )

            if len(profile["preferred_paths"]) < 3:
                recommendations.append(
                    "Try assessments in different paths to get a well-rounded evaluation"
                )

        return recommendations

    def get_greeting_message(self) -> str:
        """Get personalized greeting message."""
        profile = self.get_user_profile()

        if profile["total_assessments"] == 0:
            return "Welcome to Sono-Eval! Let's start your first assessment."
        elif profile["total_assessments"] == 1:
            return "Welcome back! You've completed 1 assessment. Ready for another?"
        else:
            last_date = profile.get("last_assessment_date")
            if last_date:
                return (
                    f"Welcome back! You've completed {profile['total_assessments']} "
                    f"assessments. Last assessment: {last_date}"
                )
            else:
                return f"Welcome back! You've completed {profile['total_assessments']} assessments."

    def get_contextual_insights(self) -> List[str]:
        """Get contextual insights based on user history."""
        profile = self.get_user_profile()
        insights = []

        if profile["total_assessments"] > 0:
            if profile["average_score"] >= 80:
                insights.append(
                    "Your consistently high scores show strong technical skills"
                )
            elif profile["average_score"] < 60:
                insights.append(
                    "Focus on fundamentals - your scores show room for growth"
                )

            if profile["strengths"]:
                insights.append(
                    f"Your strengths include: {', '.join(profile['strengths'][:2])}"
                )

            if len(profile["preferred_paths"]) > 0:
                insights.append(
                    f"You've focused on: {', '.join(profile['preferred_paths'])}"
                )

        return insights
