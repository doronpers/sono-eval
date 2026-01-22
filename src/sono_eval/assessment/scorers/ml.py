from typing import Any, Dict, List, Optional, Tuple

from sono_eval.assessment.helpers import extract_text_content
from sono_eval.assessment.models import Evidence, EvidenceType, PathType, ScoringMetric
from sono_eval.assessment.scorers.ml_utils import (
    CodeComplexityAnalyzer,
    NamingConventionValidator,
    ReadabilityAnalyzer,
    calculate_confidence_from_evidence,
    extract_docstrings_and_comments,
)
from sono_eval.utils.logger import get_logger

logger = get_logger(__name__)


class MLScorer:
    """Handles ML-based scoring and hybrid combination using AST and code analysis."""

    def __init__(self):
        self._ml_model = None
        self._use_ast_analysis = True  # Always available

    def load_model_if_available(self) -> bool:
        """
        Attempt to load ML model.

        Currently uses AST-based analysis as the lightweight "ML" approach.
        Future: Could load sentence-transformers or custom trained models.
        """
        if self._ml_model is not None:
            return True

        # For now, use AST + readability analysis (always available)
        self._use_ast_analysis = True
        logger.info("Using AST-based code analysis (lightweight ML approach)")
        return True

    def get_insights(self, content: Any, path: PathType) -> Optional[Dict[str, Any]]:
        """Get ML model insights using AST and readability analysis."""
        if not self._use_ast_analysis:
            return None

        text = extract_text_content(content)
        if not text:
            return None

        try:
            # Analyze code complexity
            complexity_metrics = CodeComplexityAnalyzer.analyze(text)

            # Analyze naming conventions
            naming_metrics = NamingConventionValidator.analyze(text)

            # Analyze documentation readability
            docs_text = extract_docstrings_and_comments(text)
            readability_metrics = ReadabilityAnalyzer.analyze(docs_text)

            # Calculate aggregated score
            complexity_score = self._score_complexity(complexity_metrics)
            naming_score = naming_metrics.get("consistency", 0.5) * 100
            readability_score = self._score_readability(readability_metrics)

            # Combine scores
            overall_score = (complexity_score + naming_score + readability_score) / 3

            # Determine pattern based on metrics
            pattern = self._identify_pattern(complexity_metrics, naming_metrics)

            # Calculate confidence based on evidence count
            evidence_count = (
                len(complexity_metrics) + len(naming_metrics) + len(readability_metrics)
            )
            confidence = calculate_confidence_from_evidence(evidence_count)

            return {
                "pattern": pattern,
                "confidence": confidence,
                "score": overall_score,
                "details": (
                    f"Code complexity analysis: {len(complexity_metrics)} metrics. "
                    f"Naming consistency: {naming_metrics.get('consistency', 0):.1%}. "
                    f"Documentation quality analyzed."
                ),
                "recommendations": self._generate_recommendations(
                    complexity_metrics, naming_metrics, readability_metrics
                ),
                "metrics": {
                    "complexity": complexity_metrics,
                    "naming": naming_metrics,
                    "readability": readability_metrics,
                },
            }
        except Exception as e:
            logger.debug(f"AST analysis failed: {e}")
            return None

    def _score_complexity(self, metrics: Dict[str, float]) -> float:
        """Score based on code complexity metrics."""
        complexity = metrics.get("cyclomatic_complexity", 1)
        nesting = metrics.get("nesting_depth", 0)
        func_length = metrics.get("function_length_avg", 0)

        # Lower complexity = higher score
        complexity_score = max(0, 100 - (complexity * 5))
        nesting_score = max(0, 100 - (nesting * 10))
        length_score = max(0, 100 - (func_length * 2))

        return (complexity_score + nesting_score + length_score) / 3

    def _score_readability(self, metrics: Dict[str, float]) -> float:
        """Score based on readability metrics."""
        flesch = metrics.get("flesch_reading_ease", 0)
        if flesch == 0:  # No documentation
            return 50.0

        # Flesch Reading Ease: 90-100 = very easy, 0-30 = very hard
        # For technical docs, 50-70 is good
        if 50 <= flesch <= 70:
            return 90.0
        elif 40 <= flesch < 50 or 70 < flesch <= 80:
            return 75.0
        elif 30 <= flesch < 40 or 80 < flesch <= 90:
            return 60.0
        else:
            return 50.0

    def _identify_pattern(self, complexity_metrics: Dict, naming_metrics: Dict) -> str:
        """Identify code pattern based on metrics."""
        complexity = complexity_metrics.get("cyclomatic_complexity", 1)
        nesting = complexity_metrics.get("nesting_depth", 0)
        naming_consistency = naming_metrics.get("consistency", 0)

        if complexity > 20 or nesting > 5:
            return "high_complexity_code"
        elif naming_consistency > 0.8 and complexity < 10:
            return "clean_well_structured_code"
        elif naming_consistency < 0.5:
            return "inconsistent_naming_patterns"
        else:
            return "moderate_complexity_code"

    def _generate_recommendations(
        self, complexity_metrics: Dict, naming_metrics: Dict, readability_metrics: Dict
    ) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []

        complexity = complexity_metrics.get("cyclomatic_complexity", 1)
        if complexity > 15:
            recommendations.append("Consider breaking down complex functions into smaller units")

        nesting = complexity_metrics.get("nesting_depth", 0)
        if nesting > 4:
            recommendations.append("Reduce nesting depth for better readability")

        func_length = complexity_metrics.get("function_length_avg", 0)
        if func_length > 50:
            recommendations.append("Functions are lengthy; consider refactoring")

        naming_consistency = naming_metrics.get("consistency", 0)
        if naming_consistency < 0.7:
            recommendations.append("Improve naming convention consistency")

        flesch = readability_metrics.get("flesch_reading_ease", 0)
        if flesch == 0:
            recommendations.append("Add documentation and docstrings")
        elif flesch < 40:
            recommendations.append("Simplify documentation for better readability")

        if not recommendations:
            recommendations.append("Code quality is good; continue following best practices")

        return recommendations

    def combine_scores(
        self,
        heuristic_score: float,
        ml_score: Optional[float],
        heuristic_confidence: float,
        ml_confidence: Optional[float],
        heuristic_evidence: List[Evidence],
        ml_insights: Optional[Dict[str, Any]],
    ) -> Tuple[float, float, List[Evidence], str]:
        """Combine heuristic and AST-based scores."""
        if ml_score is None or not self._use_ast_analysis:
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
                    description=f"AST analysis identified: {pattern}",
                    source="ast_analysis",
                    weight=ml_weight,
                    metadata={"source": "ast_analyzer", "insights": ml_insights},
                )
            )

        heuristic_str = f"{heuristic_score:.1f}"
        ml_str = f"{ml_score:.1f}"
        evidence_count = len(heuristic_evidence)
        confidence_str = f"{combined_confidence:.1%}"

        ml_details = ml_insights.get("details", "AST-based code analysis") if ml_insights else ""

        explanation = (
            f"Score combines heuristic analysis ({heuristic_str}) "
            f"with AST-based insights ({ml_str}). "
            f"Heuristic analysis provides explainable evidence: "
            f"{evidence_count} indicators identified. "
            f"AST analysis adds: {ml_details}. "
            f"Combined confidence: {confidence_str}."
        )

        return combined_score, combined_confidence, combined_evidence, explanation

    def enhance_metrics(
        self,
        metrics: List[ScoringMetric],
        ml_insights: Dict[str, Any],
        path: PathType,
    ) -> List[ScoringMetric]:
        """Enhance heuristic metrics with AST-based insights."""
        if not ml_insights:
            return metrics

        # Add AST insights as additional evidence
        for metric in metrics:
            if ml_insights.get("pattern"):
                metric.evidence.append(
                    Evidence(
                        type=EvidenceType.CODE_QUALITY,
                        description=f"AST analysis identified: {ml_insights['pattern']}",
                        source="ast_analysis",
                        weight=0.3,
                        metadata={
                            "source": "ast_analyzer",
                            "confidence": ml_insights.get("confidence", 0.5),
                            "insights": ml_insights,
                        },
                    )
                )
                if ml_insights.get("confidence", 0.5) > 0.7:
                    metric.confidence = min(1.0, metric.confidence * 1.1)

        # Add specific AST metric
        if ml_insights.get("details"):
            metrics.append(
                ScoringMetric(
                    name="Code Structure Analysis",
                    category="code_quality",
                    score=float(ml_insights.get("score", 75.0)),
                    weight=0.2,
                    evidence=[
                        Evidence(
                            type=EvidenceType.CODE_QUALITY,
                            description=ml_insights.get(
                                "details", "AST analysis identified patterns"
                            ),
                            source="ast_analysis",
                            weight=0.5,
                            metadata={"source": "ast_analyzer", **ml_insights},
                        )
                    ],
                    explanation=(
                        f"AST analysis identified: {ml_insights.get('pattern', 'patterns')}. "
                        "This complements heuristic analysis with structural validation. "
                        f"Analysis confidence: {ml_insights.get('confidence', 0.5):.1%}."
                    ),
                    confidence=ml_insights.get("confidence", 0.5),
                )
            )

        return metrics
