"""
Assessment Engine with explainable, evidence-based scoring.

Refactored to orchestrate specialized scorers for Heuristics, ML, and Micro-Motives.
"""

import time
from typing import List, Optional

from sono_eval.assessment.helpers import extract_text_content
from sono_eval.assessment.models import (
    AssessmentInput,
    AssessmentResult,
    MicroMotive,
    PathScore,
    PathType,
    ScoringMetric,
)
from sono_eval.assessment.pattern_checks import (
    PatternViolation,
    calculate_pattern_penalty,
    detect_pattern_violations,
    violations_to_metadata,
)
from sono_eval.assessment.scorers.council_scorer import CouncilScorer
from sono_eval.assessment.scorers.heuristic import HeuristicScorer
from sono_eval.assessment.scorers.ml import MLScorer
from sono_eval.assessment.scorers.motive import MicroMotiveScorer
from sono_eval.utils.config import get_config
from sono_eval.utils.logger import get_logger

logger = get_logger(__name__)


class AssessmentEngine:
    """
    Core assessment engine with explainable scoring.

    Acts as an orchestrator for:
    - HeuristicScorer: Rule-based analysis
    - MLScorer: ML model integration
    - MicroMotiveScorer: Dark Horse tracking
    """

    def __init__(self):
        """Initialize the assessment engine."""
        self.config = get_config()
        self.version = self.config.assessment_engine_version
        self.enable_explanations = self.config.assessment_enable_explanations
        self.pattern_checks_enabled = self.config.pattern_checks_enabled

        # Initialize Scorers
        self.heuristic_scorer = HeuristicScorer(self.config)
        self.ml_scorer = MLScorer()
        self.council_scorer = CouncilScorer()
        self.motive_scorer = MicroMotiveScorer()

        self.dark_horse_enabled = self.config.dark_horse_mode.lower() in (
            "enabled",
            "true",
            "1",
            "yes",
        )
        if not self.dark_horse_enabled:
            logger.info("Dark Horse micro-motive tracking is disabled")
        logger.info(f"Initialized AssessmentEngine v{self.version}")

    async def assess(self, assessment_input: AssessmentInput) -> AssessmentResult:
        """Perform comprehensive assessment with hybrid heuristics + ML approach."""
        start_time = time.time()
        logger.info(
            f"Starting assessment for candidate {assessment_input.candidate_id}"
        )

        # Check for AI/Council availability
        self.council_scorer.load_if_available()

        # Load ML model (CodeBERT or fallback to AST)
        self.ml_scorer.load_model_if_available()

        # Generate unique assessment ID
        assessment_id = f"assess_{int(time.time() * 1000)}"

        submission_text = extract_text_content(assessment_input.content)
        pattern_violations: List[PatternViolation] = []
        pattern_penalty = 0.0
        pattern_checks_active = (
            self.pattern_checks_enabled and assessment_input.submission_type == "code"
        )
        if pattern_checks_active:
            pattern_violations = detect_pattern_violations(submission_text)
            pattern_penalty = calculate_pattern_penalty(
                pattern_violations,
                self.heuristic_scorer.pattern_penalty_weights,
                self.heuristic_scorer.pattern_penalty_max,
            )

        # Evaluate each path
        path_scores = []
        all_motives = []
        all_confidences = []

        for path in assessment_input.paths_to_evaluate:
            path_score = await self._evaluate_path(
                path, assessment_input, pattern_violations
            )
            path_scores.append(path_score)
            all_motives.extend(path_score.motives)
            # Collect confidence from metrics
            if path_score.metrics:
                avg_confidence = sum(m.confidence for m in path_score.metrics) / len(
                    path_score.metrics
                )
                all_confidences.append(avg_confidence)

        # Calculate overall score
        overall_score = self._calculate_overall_score(path_scores)

        # Calculate overall confidence
        overall_confidence = (
            sum(all_confidences) / len(all_confidences) if all_confidences else 0.85
        )

        dominant_path = self._determine_dominant_path(path_scores)
        summary = self._generate_summary(path_scores, all_motives)
        key_findings = self._extract_key_findings(path_scores)
        recommendations = self._generate_recommendations(path_scores)

        processing_time = (time.time() - start_time) * 1000

        result = AssessmentResult(
            candidate_id=assessment_input.candidate_id,
            assessment_id=assessment_id,
            overall_score=overall_score,
            confidence=overall_confidence,
            path_scores=path_scores,
            micro_motives=all_motives,
            dominant_path=dominant_path,
            summary=summary,
            key_findings=key_findings,
            recommendations=recommendations,
            engine_version=self.version,
            processing_time_ms=processing_time,
            metadata={
                "assessment_mode": self._determine_assessment_mode(),
                "ml_model_available": self.ml_scorer._use_trained_model,
                "ml_model_version": self.ml_scorer.model_version,
                "council_available": self.council_scorer._available,
                "pattern_checks": {
                    "enabled": pattern_checks_active,
                    "violation_count": len(pattern_violations),
                    "penalty_points": pattern_penalty,
                    "violations": violations_to_metadata(pattern_violations),
                },
            },
        )

        logger.info(
            f"Assessment completed for {assessment_input.candidate_id}: "
            f"score={overall_score:.2f}, confidence={overall_confidence:.2%}, "
            f"mode={self._determine_assessment_mode()}, "
            f"time={processing_time:.2f}ms"
        )

        return result

    async def _evaluate_path(
        self,
        path: PathType,
        input_data: AssessmentInput,
        pattern_violations: Optional[List[PatternViolation]] = None,
    ) -> PathScore:
        """Evaluate a specific assessment path."""
        logger.debug(f"Evaluating path: {path}")

        # 1. Heuristic Scoring
        metrics = self.heuristic_scorer.generate_metrics_for_path(
            path, input_data, pattern_violations
        )

        # 2. ML Model Enhancement (CodeBERT or AST)
        ml_insights = self.ml_scorer.get_insights(input_data.content, path)
        if ml_insights:
            metrics = self.ml_scorer.enhance_metrics(metrics, ml_insights, path)

        # 3. AI/Council Enhancement
        council_insights = await self.council_scorer.get_insights(
            input_data.content, path
        )
        if council_insights:
            metrics = self.council_scorer.enhance_metrics(
                metrics, council_insights, path
            )

        # 4. Micro-Motives
        if self.dark_horse_enabled:
            motives = self.motive_scorer.identify_micro_motives(path, input_data)
        else:
            motives = []

        # 4. Final Path Score Calculation
        path_score = self._calculate_path_score(metrics)
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

    def _determine_assessment_mode(self) -> str:
        """Determine the current assessment mode based on available scorers."""
        modes = []
        if self.ml_scorer._use_trained_model:
            modes.append("ml")
        if self.council_scorer._available:
            modes.append("council")
        if modes:
            return "hybrid_" + "_".join(modes)
        return "heuristic"

    # --- Aggregation Helpers ---
    # Kept in engine as they aggregate results from scorers

    def _calculate_path_score(self, metrics: List[ScoringMetric]) -> float:
        if not metrics:
            return 0.0
        total_weight = sum(m.weight for m in metrics)
        if total_weight == 0:
            return sum(m.score for m in metrics) / len(metrics)
        weighted_sum = sum(m.score * m.weight for m in metrics)
        return weighted_sum / total_weight

    def _calculate_overall_score(self, path_scores: List[PathScore]) -> float:
        if not path_scores:
            return 0.0
        return sum(ps.overall_score for ps in path_scores) / len(path_scores)

    def _determine_dominant_path(
        self, path_scores: List[PathScore]
    ) -> Optional[PathType]:
        if not path_scores:
            return None
        return max(path_scores, key=lambda ps: ps.overall_score).path

    def _identify_strengths(self, metrics: List[ScoringMetric]) -> List[str]:
        return [f"{m.name}: {m.explanation}" for m in metrics if m.score >= 75.0]

    def _identify_improvements(self, metrics: List[ScoringMetric]) -> List[str]:
        return [
            f"{m.name}: Consider enhancing this area (current score: {m.score:.0f})"
            for m in metrics
            if m.score < 75.0
        ]

    def _generate_summary(
        self, path_scores: List[PathScore], motives: List[MicroMotive]
    ) -> str:
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
        recommendations = []
        for ps in path_scores:
            if ps.areas_for_improvement:
                recommendations.append(
                    f"Focus on {ps.path.value}: {ps.areas_for_improvement[0]}"
                )
        return recommendations
