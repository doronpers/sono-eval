"""
Assessment Engine with explainable, evidence-based scoring.

Implements multi-path assessment with Dark Horse micro-motive tracking.
"""

import time
from typing import Dict, List, Optional

from sono_eval.assessment.models import (
    AssessmentInput,
    AssessmentResult,
    Evidence,
    EvidenceType,
    MicroMotive,
    MotiveType,
    PathScore,
    PathType,
    ScoringMetric,
)
from sono_eval.utils.config import get_config
from sono_eval.utils.logger import get_logger

logger = get_logger(__name__)


class AssessmentEngine:
    """
    Core assessment engine with explainable scoring.
    
    Features:
    - Multi-path evaluation (technical, design, collaboration, etc.)
    - Evidence-based scoring with explanations
    - Dark Horse micro-motive tracking
    - Confidence scoring
    """

    def __init__(self):
        """Initialize the assessment engine."""
        self.config = get_config()
        self.version = self.config.assessment_engine_version
        self.enable_explanations = self.config.assessment_enable_explanations
        self.multi_path_tracking = self.config.assessment_multi_path_tracking
        logger.info(f"Initialized AssessmentEngine v{self.version}")

    async def assess(self, assessment_input: AssessmentInput) -> AssessmentResult:
        """
        Perform comprehensive assessment.

        Args:
            assessment_input: Assessment input data

        Returns:
            Complete assessment result with scores and explanations
        """
        start_time = time.time()
        logger.info(
            f"Starting assessment for candidate {assessment_input.candidate_id}"
        )

        # Generate unique assessment ID
        assessment_id = f"assess_{int(time.time() * 1000)}"

        # Evaluate each path
        path_scores = []
        all_motives = []

        for path in assessment_input.paths_to_evaluate:
            path_score = await self._evaluate_path(path, assessment_input)
            path_scores.append(path_score)
            all_motives.extend(path_score.motives)

        # Calculate overall score
        overall_score = self._calculate_overall_score(path_scores)
        
        # Determine dominant path
        dominant_path = self._determine_dominant_path(path_scores)

        # Generate summary and recommendations
        summary = self._generate_summary(path_scores, all_motives)
        key_findings = self._extract_key_findings(path_scores)
        recommendations = self._generate_recommendations(path_scores)

        processing_time = (time.time() - start_time) * 1000

        result = AssessmentResult(
            candidate_id=assessment_input.candidate_id,
            assessment_id=assessment_id,
            overall_score=overall_score,
            confidence=0.85,  # Could be calculated based on evidence strength
            path_scores=path_scores,
            micro_motives=all_motives,
            dominant_path=dominant_path,
            summary=summary,
            key_findings=key_findings,
            recommendations=recommendations,
            engine_version=self.version,
            processing_time_ms=processing_time,
        )

        logger.info(
            f"Assessment completed for {assessment_input.candidate_id}: "
            f"score={overall_score:.2f}, time={processing_time:.2f}ms"
        )

        return result

    async def _evaluate_path(
        self, path: PathType, input_data: AssessmentInput
    ) -> PathScore:
        """Evaluate a specific assessment path."""
        logger.debug(f"Evaluating path: {path}")

        # Generate metrics for this path
        metrics = self._generate_metrics_for_path(path, input_data)
        
        # Identify micro-motives
        motives = self._identify_micro_motives(path, input_data)

        # Calculate path score
        path_score = self._calculate_path_score(metrics)

        # Extract insights
        strengths = self._identify_strengths(metrics)
        improvements = self._identify_improvements(metrics)

        return PathScore(
            path=path,
            overall_score=path_score,
            metrics=metrics,
            motives=motives,
            strengths=strengths,
            areas_for_improvement=improvements,
        )

    def _generate_metrics_for_path(
        self, path: PathType, input_data: AssessmentInput
    ) -> List[ScoringMetric]:
        """Generate scoring metrics for a specific path."""
        metrics = []

        # Example metrics based on path type
        if path == PathType.TECHNICAL:
            metrics.extend([
                ScoringMetric(
                    name="Code Quality",
                    category="technical",
                    score=85.0,
                    weight=0.3,
                    evidence=[
                        Evidence(
                            type=EvidenceType.CODE_QUALITY,
                            description="Clean, well-structured code with good naming",
                            source="submission.py:1-50",
                            weight=0.8,
                        )
                    ],
                    explanation="Code demonstrates strong fundamentals with consistent style",
                    confidence=0.9,
                ),
                ScoringMetric(
                    name="Problem Solving",
                    category="technical",
                    score=78.0,
                    weight=0.3,
                    evidence=[
                        Evidence(
                            type=EvidenceType.CODE_QUALITY,
                            description="Efficient algorithm with O(n) complexity",
                            source="submission.py:25-40",
                            weight=0.7,
                        )
                    ],
                    explanation="Effective approach to problem solving",
                    confidence=0.85,
                ),
                ScoringMetric(
                    name="Testing",
                    category="technical",
                    score=70.0,
                    weight=0.2,
                    evidence=[
                        Evidence(
                            type=EvidenceType.TESTING,
                            description="Basic test coverage present",
                            source="test_submission.py",
                            weight=0.6,
                        )
                    ],
                    explanation="Tests cover main scenarios but could be more comprehensive",
                    confidence=0.8,
                ),
            ])
        elif path == PathType.DESIGN:
            metrics.extend([
                ScoringMetric(
                    name="Architecture",
                    category="design",
                    score=80.0,
                    weight=0.4,
                    evidence=[
                        Evidence(
                            type=EvidenceType.ARCHITECTURE,
                            description="Modular design with clear separation of concerns",
                            source="project_structure",
                            weight=0.8,
                        )
                    ],
                    explanation="Well-organized architecture",
                    confidence=0.85,
                ),
            ])
        elif path == PathType.COLLABORATION:
            metrics.extend([
                ScoringMetric(
                    name="Documentation",
                    category="collaboration",
                    score=75.0,
                    weight=0.3,
                    evidence=[
                        Evidence(
                            type=EvidenceType.DOCUMENTATION,
                            description="README and inline comments present",
                            source="README.md",
                            weight=0.7,
                        )
                    ],
                    explanation="Good documentation practices",
                    confidence=0.8,
                ),
            ])

        return metrics

    def _identify_micro_motives(
        self, path: PathType, input_data: AssessmentInput
    ) -> List[MicroMotive]:
        """Identify micro-motives using Dark Horse model."""
        motives = []

        # Example motive identification
        if path == PathType.TECHNICAL:
            motives.append(
                MicroMotive(
                    motive_type=MotiveType.MASTERY,
                    strength=0.8,
                    indicators=[
                        "Deep understanding of algorithms",
                        "Optimization focus",
                        "Clean code practices",
                    ],
                    path_alignment=path,
                )
            )
            motives.append(
                MicroMotive(
                    motive_type=MotiveType.QUALITY,
                    strength=0.7,
                    indicators=[
                        "Attention to edge cases",
                        "Consistent style",
                    ],
                    path_alignment=path,
                )
            )

        return motives

    def _calculate_path_score(self, metrics: List[ScoringMetric]) -> float:
        """Calculate weighted average score for a path."""
        if not metrics:
            return 0.0

        total_weight = sum(m.weight for m in metrics)
        if total_weight == 0:
            return sum(m.score for m in metrics) / len(metrics)

        weighted_sum = sum(m.score * m.weight for m in metrics)
        return weighted_sum / total_weight

    def _calculate_overall_score(self, path_scores: List[PathScore]) -> float:
        """Calculate overall score from path scores."""
        if not path_scores:
            return 0.0
        return sum(ps.overall_score for ps in path_scores) / len(path_scores)

    def _determine_dominant_path(
        self, path_scores: List[PathScore]
    ) -> Optional[PathType]:
        """Determine the dominant assessment path."""
        if not path_scores:
            return None
        return max(path_scores, key=lambda ps: ps.overall_score).path

    def _identify_strengths(self, metrics: List[ScoringMetric]) -> List[str]:
        """Identify strengths from metrics."""
        return [
            f"{m.name}: {m.explanation}"
            for m in metrics
            if m.score >= 75.0
        ]

    def _identify_improvements(self, metrics: List[ScoringMetric]) -> List[str]:
        """Identify areas for improvement."""
        return [
            f"{m.name}: Consider enhancing this area (current score: {m.score:.0f})"
            for m in metrics
            if m.score < 75.0
        ]

    def _generate_summary(
        self, path_scores: List[PathScore], motives: List[MicroMotive]
    ) -> str:
        """Generate assessment summary."""
        avg_score = self._calculate_overall_score(path_scores)
        top_path = self._determine_dominant_path(path_scores)
        
        summary = (
            f"Assessment shows an overall score of {avg_score:.1f}/100. "
            f"Strongest performance in {top_path.value if top_path else 'multiple areas'}. "
        )
        
        if motives:
            dominant_motive = max(motives, key=lambda m: m.strength)
            summary += (
                f"Primary micro-motive is {dominant_motive.motive_type.value} "
                f"with strength {dominant_motive.strength:.2f}."
            )
        
        return summary

    def _extract_key_findings(self, path_scores: List[PathScore]) -> List[str]:
        """Extract key findings from path scores."""
        findings = []
        for ps in path_scores:
            if ps.overall_score >= 80:
                findings.append(
                    f"Strong performance in {ps.path.value} (score: {ps.overall_score:.1f})"
                )
            elif ps.overall_score < 60:
                findings.append(
                    f"Opportunity for growth in {ps.path.value} (score: {ps.overall_score:.1f})"
                )
        return findings

    def _generate_recommendations(self, path_scores: List[PathScore]) -> List[str]:
        """Generate recommendations based on scores."""
        recommendations = []
        for ps in path_scores:
            if ps.areas_for_improvement:
                recommendations.append(
                    f"Focus on {ps.path.value}: {ps.areas_for_improvement[0]}"
                )
        return recommendations
