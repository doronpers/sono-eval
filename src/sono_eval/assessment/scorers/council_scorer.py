import re
from typing import Any, Dict, List, Optional

from council_ai import Council  # type: ignore

from sono_eval.assessment.helpers import extract_text_content
from sono_eval.assessment.models import Evidence, EvidenceType, PathType, ScoringMetric
from sono_eval.utils.logger import get_logger

logger = get_logger(__name__)


class CouncilScorer:
    """
    Scorer that leverages Council AI personas for deep, multi-perspective assessment.
    Replaces/Augments the placeholder MLScorer.
    """

    def __init__(self):
        self._council: Optional[Council] = None
        self._available = False

    def load_if_available(self) -> bool:
        """Initialize Council AI if configuration allows."""
        if self._council is not None:
            return True

        try:
            # Initialize with 'coding' domain which includes relevant personas (Rams, Holman, etc.)
            # We assume API keys are set in environment (ANTHROPIC_API_KEY, etc.)
            self._council = Council.for_domain("coding")
            self._available = True
            logger.info("Council AI initialized successfully for assessment")
            return True
        except Exception as e:
            logger.warning(f"Council AI initialization failed: {e}")
            self._available = False
            return False

    async def get_insights(
        self, content: Any, path: PathType
    ) -> Optional[Dict[str, Any]]:
        """
        Consult the council for insights on the provided content.

        Args:
            content: The submission content (code, text, etc.)
            path: The assessment path (technical, creative, etc.)

        Returns:
            Dictionary containing synthesis, score_estimation, and detailed feedback.
        """
        if not self._available or self._council is None:
            return None

        text = extract_text_content(content)
        if not text:
            return None

        # Construct a prompt that asks for specific assessment criteria
        query = (
            f"Assess this submission for the '{path.value}' path.\n"
            f"Provide a critical review focusing on:\n"
            f"1. Strengths\n"
            f"2. Weaknesses\n"
            f"3. A numerical score estimation (0-100) based on quality and best practices.\n\n"
            f"Code/Content:\n{text[:8000]}"  # Truncate to avoid context limits if necessary
        )

        try:
            # Use async consultation
            result = await self._council.consult_async(query)

            # Extract score from synthesis if possible (naive regex extraction)
            score_match = re.search(
                r"score[:\s]+(\d+)/100", result.synthesis, re.IGNORECASE
            )
            score_est = float(score_match.group(1)) if score_match else None

            return {
                "synthesis": result.synthesis,
                "responses": [
                    {"persona": r.persona.name, "content": r.content}
                    for r in result.responses
                ],
                "score": score_est,
                "confidence": 0.85,  # High confidence in AI council?
            }
        except Exception as e:
            logger.error(f"Council consultation error: {e}")
            return None

    def enhance_metrics(
        self,
        metrics: List[ScoringMetric],
        council_insights: Dict[str, Any],
        path: PathType,
    ) -> List[ScoringMetric]:
        """Enhance heuristic metrics with Council insights."""
        if not council_insights:
            return metrics

        # specific Council metric
        synthesis = council_insights.get("synthesis", "No synthesis provided.")
        score = council_insights.get("score")

        # Create a new metric for the Council's assessment
        council_metric = ScoringMetric(
            name="AI Council Review",
            category="ai_assessment",
            score=score if score is not None else 80.0,  # Fallback score
            weight=0.4,  # Significant weight
            evidence=[
                Evidence(
                    type=EvidenceType.CODE_QUALITY,
                    description="Council Consensus",
                    source="council_ai",
                    weight=1.0,
                    metadata={"synthesis": synthesis},
                )
            ],
            explanation=(
                f"The AI Council (various personas) reviewed the submission. "
                f"Consensus: {synthesis[:200]}..."
            ),
            confidence=council_insights.get("confidence", 0.8),
        )

        metrics.append(council_metric)
        return metrics
