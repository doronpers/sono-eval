from typing import Any, Dict, List, Optional, Tuple

from sono_eval.assessment.helpers import extract_text_content
from sono_eval.assessment.models import Evidence, EvidenceType, PathType, ScoringMetric
from sono_eval.utils.logger import get_logger

logger = get_logger(__name__)


class MLScorer:
    """Handles ML-based scoring and hybrid combination."""

    def __init__(self):
        self._ml_model = None
        self._use_ml = False

    def load_model_if_available(self) -> bool:
        """Attempt to load ML model."""
        if self._ml_model is not None:
            return True

        try:
            # Placeholder for ML model loading
            self._use_ml = False
            logger.debug("ML model not available, using heuristic analysis")
            return False
        except Exception as e:
            logger.debug(f"ML model loading failed: {e}, using heuristics")
            self._use_ml = False
            return False

    def get_insights(self, content: Any, path: PathType) -> Optional[Dict[str, Any]]:
        """Get ML model insights."""
        if not self._use_ml or self._ml_model is None:
            return None

        extract_text_content(content)

        try:
            # Placeholder for ML inference
            return {
                "pattern": "advanced_pattern_detected",
                "confidence": 0.75,
                "details": "ML model identified sophisticated code patterns",
                "recommendations": ["Consider advanced optimization techniques"],
            }
        except Exception as e:
            logger.debug(f"ML insight generation failed: {e}")
            return None

    def combine_scores(
        self,
        heuristic_score: float,
        ml_score: Optional[float],
        heuristic_confidence: float,
        ml_confidence: Optional[float],
        heuristic_evidence: List[Evidence],
        ml_insights: Optional[Dict[str, Any]],
    ) -> Tuple[float, float, List[Evidence], str]:
        """Combine heuristic and ML scores."""
        if ml_score is None or not self._use_ml:
            return (
                heuristic_score,
                heuristic_confidence,
                heuristic_evidence,
                "Score based on heuristic analysis of code patterns and structure. "
                "All scoring factors are explicitly identified and explainable.",
            )

        heuristic_weight = 0.6
        ml_weight = 0.4

        combined_score = (heuristic_score * heuristic_weight) + (ml_score * ml_weight)

        if ml_confidence is not None:
            combined_confidence = (heuristic_confidence * heuristic_weight) + (
                ml_confidence * ml_weight
            )
        else:
            combined_confidence = heuristic_confidence * 0.8

        combined_evidence = heuristic_evidence.copy()
        if ml_insights:
            pattern = ml_insights.get("pattern", "additional pattern")
            combined_evidence.append(
                Evidence(
                    type=EvidenceType.CODE_QUALITY,
                    description=f"ML model identified: {pattern}",
                    source="ml_analysis",
                    weight=ml_weight,
                    metadata={"source": "ml_model", "insights": ml_insights},
                )
            )

        heuristic_str = f"{heuristic_score:.1f}"
        ml_str = f"{ml_score:.1f}"
        evidence_count = len(heuristic_evidence)
        confidence_str = f"{combined_confidence:.1%}"
        explanation = (
            f"Score combines heuristic analysis ({heuristic_str}) "
            f"with ML insights ({ml_str}). "
            f"Heuristic analysis provides explainable evidence: "
            f"{evidence_count} indicators identified. "
            f"ML model contributes nuanced pattern recognition. "
            f"Combined confidence: {confidence_str}."
        )

        return combined_score, combined_confidence, combined_evidence, explanation

    def enhance_metrics(
        self,
        metrics: List[ScoringMetric],
        ml_insights: Dict[str, Any],
        path: PathType,
    ) -> List[ScoringMetric]:
        """Enhance heuristic metrics with ML insights."""
        if not ml_insights:
            return metrics

        # Add ML insights as additional evidence
        for metric in metrics:
            if ml_insights.get("pattern"):
                metric.evidence.append(
                    Evidence(
                        type=EvidenceType.CODE_QUALITY,
                        description=f"ML model identified: {ml_insights['pattern']}",
                        source="ml_analysis",
                        weight=0.3,
                        metadata={
                            "source": "ml_model",
                            "ml_confidence": ml_insights.get("confidence", 0.5),
                            "insights": ml_insights,
                        },
                    )
                )
                if ml_insights.get("confidence", 0.5) > 0.7:
                    metric.confidence = min(1.0, metric.confidence * 1.1)

        # Add specific ML metric
        if ml_insights.get("details"):
            metrics.append(
                ScoringMetric(
                    name="ML Pattern Recognition",
                    category="ml_insights",
                    score=float(ml_insights.get("score", 75.0)),
                    weight=0.2,
                    evidence=[
                        Evidence(
                            type=EvidenceType.CODE_QUALITY,
                            description=ml_insights.get("details", "ML model identified patterns"),
                            source="ml_analysis",
                            weight=0.5,
                            metadata={"source": "ml_model", **ml_insights},
                        )
                    ],
                    explanation=(
                        f"ML model analysis identified: {ml_insights.get('pattern', 'patterns')}. "
                        "This complements heuristic analysis with nuanced pattern recognition. "
                        f"ML confidence: {ml_insights.get('confidence', 0.5):.1%}."
                    ),
                    confidence=ml_insights.get("confidence", 0.5),
                )
            )

        return metrics
