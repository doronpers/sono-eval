"""
Assessment Engine with explainable, evidence-based scoring.

Implements multi-path assessment with Dark Horse micro-motive tracking.
"""

import time
from typing import Any, Dict, List, Optional

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
from sono_eval.assessment.pattern_checks import (
    PatternViolation,
    calculate_pattern_penalty,
    detect_pattern_violations,
    violations_to_metadata,
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
    - Hybrid heuristics + ML approach for enhanced explainability
    """

    def __init__(self):
        """Initialize the assessment engine."""
        self.config = get_config()
        self.version = self.config.assessment_engine_version
        self.enable_explanations = self.config.assessment_enable_explanations
        self.multi_path_tracking = self.config.assessment_multi_path_tracking
        self.pattern_checks_enabled = self.config.pattern_checks_enabled
        self.pattern_penalty_weights = {
            "low": self.config.pattern_penalty_low,
            "medium": self.config.pattern_penalty_medium,
            "high": self.config.pattern_penalty_high,
            "critical": self.config.pattern_penalty_high,
        }
        self.pattern_penalty_max = self.config.pattern_penalty_max
        self._ml_model = None  # Lazy-loaded ML model for hybrid scoring
        self._use_ml = False  # Flag to enable ML when available
        logger.info(f"Initialized AssessmentEngine v{self.version}")

    def _load_ml_model_if_available(self) -> bool:
        """
        Attempt to load ML model for hybrid scoring.

        Returns:
            True if ML model is available, False otherwise
        """
        if self._ml_model is not None:
            return True

        try:
            # Placeholder for ML model loading
            # In production, this would load a trained model
            # For now, we'll use heuristics but structure for ML integration
            self._use_ml = False
            logger.debug("ML model not available, using heuristic analysis")
            return False
        except Exception as e:
            logger.debug(f"ML model loading failed: {e}, using heuristics")
            self._use_ml = False
            return False

    def _combine_heuristic_and_ml_scores(
        self,
        heuristic_score: float,
        ml_score: Optional[float],
        heuristic_confidence: float,
        ml_confidence: Optional[float],
        heuristic_evidence: List[Evidence],
        ml_insights: Optional[Dict[str, Any]],
    ) -> tuple:
        """
        Combine heuristic and ML scores for enhanced explainability.

        This method provides a hybrid approach that:
        - Uses heuristics for explainability and transparency
        - Uses ML for pattern recognition and nuanced insights
        - Combines both for better accuracy while maintaining explainability

        Args:
            heuristic_score: Score from heuristic analysis
            ml_score: Score from ML model (if available)
            heuristic_confidence: Confidence in heuristic score
            ml_confidence: Confidence in ML score (if available)
            heuristic_evidence: Evidence from heuristic analysis
            ml_insights: Additional insights from ML model

        Returns:
            Tuple of (combined_score, combined_confidence, combined_evidence, explanation)
        """
        if ml_score is None or not self._use_ml:
            # Pure heuristic approach - fully explainable
            return (
                heuristic_score,
                heuristic_confidence,
                heuristic_evidence,
                "Score based on heuristic analysis of code patterns and structure. "
                "All scoring factors are explicitly identified and explainable.",
            )

        # Hybrid approach: Weighted combination
        # Heuristics provide base explainability, ML provides nuanced insights
        heuristic_weight = 0.6  # Favor heuristics for explainability
        ml_weight = 0.4

        # Combine scores
        combined_score = (heuristic_score * heuristic_weight) + (ml_score * ml_weight)

        # Combine confidence (weighted average)
        if ml_confidence is not None:
            combined_confidence = (heuristic_confidence * heuristic_weight) + (
                ml_confidence * ml_weight
            )
        else:
            combined_confidence = heuristic_confidence * 0.8  # Slightly reduce if ML uncertain

        # Combine evidence
        combined_evidence = heuristic_evidence.copy()
        if ml_insights:
            # Add ML insights as additional evidence
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

        # Enhanced explanation
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

    def _get_ml_insights(self, text: str, path: PathType) -> Optional[Dict[str, Any]]:
        """
        Get ML model insights for enhanced analysis.

        This is a placeholder for ML model integration. In production, this would:
        - Use trained models to identify patterns
        - Provide nuanced insights beyond heuristics
        - Return structured insights for combination with heuristics

        Args:
            text: Submission text to analyze
            path: Assessment path being evaluated

        Returns:
            Dictionary with ML insights or None if ML not available
        """
        if not self._use_ml or self._ml_model is None:
            return None

        # Placeholder for ML inference
        # In production, this would call the actual ML model
        try:
            # Example structure for ML insights
            return {
                "pattern": "advanced_pattern_detected",
                "confidence": 0.75,
                "details": "ML model identified sophisticated code patterns",
                "recommendations": ["Consider advanced optimization techniques"],
            }
        except Exception as e:
            logger.debug(f"ML insight generation failed: {e}")
            return None

    async def assess(self, assessment_input: AssessmentInput) -> AssessmentResult:
        """
        Perform comprehensive assessment with hybrid heuristics + ML approach.

        Args:
            assessment_input: Assessment input data

        Returns:
            Complete assessment result with scores and explanations
        """
        start_time = time.time()
        logger.info(f"Starting assessment for candidate {assessment_input.candidate_id}")

        # Check for ML model availability (lazy load)
        self._load_ml_model_if_available()

        # Generate unique assessment ID
        assessment_id = f"assess_{int(time.time() * 1000)}"

        submission_text = self._extract_text_content(assessment_input.content)
        pattern_violations: List[PatternViolation] = []
        pattern_penalty = 0.0
        pattern_checks_active = (
            self.pattern_checks_enabled and assessment_input.submission_type == "code"
        )
        if pattern_checks_active:
            pattern_violations = detect_pattern_violations(submission_text)
            pattern_penalty = calculate_pattern_penalty(
                pattern_violations, self.pattern_penalty_weights, self.pattern_penalty_max
            )

        # Evaluate each path
        path_scores = []
        all_motives = []
        all_confidences = []

        for path in assessment_input.paths_to_evaluate:
            path_score = await self._evaluate_path(path, assessment_input, pattern_violations)
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

        # Calculate overall confidence from path confidences
        overall_confidence = (
            sum(all_confidences) / len(all_confidences) if all_confidences else 0.85
        )

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
                "assessment_mode": "hybrid" if self._use_ml else "heuristic",
                "ml_available": self._use_ml,
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
            f"mode={'hybrid' if self._use_ml else 'heuristic'}, time={processing_time:.2f}ms"
        )

        return result

    async def _evaluate_path(
        self,
        path: PathType,
        input_data: AssessmentInput,
        pattern_violations: Optional[List[PatternViolation]] = None,
    ) -> PathScore:
        """
        Evaluate a specific assessment path using hybrid approach.

        Combines heuristic analysis with ML insights for enhanced explainability.
        """
        logger.debug(f"Evaluating path: {path}")

        # Generate metrics for this path (heuristic-based)
        metrics = self._generate_metrics_for_path(path, input_data, pattern_violations)

        # Get ML insights if available
        submission_text = self._extract_text_content(input_data.content)
        ml_insights = self._get_ml_insights(submission_text, path)

        # Enhance metrics with ML insights if available
        if ml_insights and self._use_ml:
            metrics = self._enhance_metrics_with_ml(metrics, ml_insights, path)

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

    def _enhance_metrics_with_ml(
        self,
        metrics: List[ScoringMetric],
        ml_insights: Dict[str, Any],
        path: PathType,
    ) -> List[ScoringMetric]:
        """
        Enhance heuristic metrics with ML insights for better explainability.

        This method adds ML-identified patterns as additional evidence while
        maintaining the explainable nature of heuristic metrics.

        Args:
            metrics: List of heuristic-based metrics
            ml_insights: ML model insights
            path: Assessment path

        Returns:
            Enhanced list of metrics with ML insights integrated
        """
        if not ml_insights:
            return metrics

        # Add ML insights as additional evidence to relevant metrics
        for metric in metrics:
            if ml_insights.get("pattern"):
                # Add ML insight as additional evidence
                metric.evidence.append(
                    Evidence(
                        type=EvidenceType.CODE_QUALITY,
                        description=f"ML model identified: {ml_insights['pattern']}",
                        source="ml_analysis",
                        weight=0.3,  # ML insights have moderate weight
                        metadata={
                            "source": "ml_model",
                            "ml_confidence": ml_insights.get("confidence", 0.5),
                            "insights": ml_insights,
                        },
                    )
                )
                # Slightly adjust confidence based on ML agreement
                if ml_insights.get("confidence", 0.5) > 0.7:
                    metric.confidence = min(1.0, metric.confidence * 1.1)

        # Optionally add a new metric specifically for ML insights
        if ml_insights.get("details"):
            metrics.append(
                ScoringMetric(
                    name="ML Pattern Recognition",
                    category="ml_insights",
                    score=ml_insights.get("score", 75.0) if "score" in ml_insights else None,
                    weight=0.2,  # Lower weight to maintain heuristic dominance
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
                        f"This complements heuristic analysis with nuanced pattern recognition. "
                        f"ML confidence: {ml_insights.get('confidence', 0.5):.1%}."
                    ),
                    confidence=ml_insights.get("confidence", 0.5),
                )
            )

        return metrics

    def _generate_metrics_for_path(
        self,
        path: PathType,
        input_data: AssessmentInput,
        pattern_violations: Optional[List[PatternViolation]] = None,
    ) -> List[ScoringMetric]:
        """
        Generate scoring metrics for a specific path.

        Analyzes actual submission content using heuristics.
        Note: This uses heuristic analysis. For production, integrate ML models.
        """
        metrics = []
        content = input_data.content
        submission_text = self._extract_text_content(content)

        if path == PathType.TECHNICAL:
            # Analyze code quality
            code_quality_score = self._analyze_code_quality(submission_text, pattern_violations)
            code_quality_evidence = self._generate_code_quality_evidence(
                submission_text, pattern_violations
            )
            violation_count = len(pattern_violations or [])

            metrics.append(
                ScoringMetric(
                    name="Code Quality",
                    category="technical",
                    score=code_quality_score,
                    weight=0.3,
                    evidence=code_quality_evidence,
                    explanation=self._explain_code_quality(code_quality_score, violation_count),
                    confidence=0.85,
                )
            )

            # Analyze problem solving approach
            problem_solving_score = self._analyze_problem_solving(submission_text)
            problem_solving_evidence = self._generate_problem_solving_evidence(submission_text)

            metrics.append(
                ScoringMetric(
                    name="Problem Solving",
                    category="technical",
                    score=problem_solving_score,
                    weight=0.3,
                    evidence=problem_solving_evidence,
                    explanation=self._explain_problem_solving(problem_solving_score),
                    confidence=0.8,
                )
            )

            # Analyze testing approach
            testing_score = self._analyze_testing(submission_text)
            testing_evidence = self._generate_testing_evidence(submission_text)

            metrics.append(
                ScoringMetric(
                    name="Testing",
                    category="technical",
                    score=testing_score,
                    weight=0.2,
                    evidence=testing_evidence,
                    explanation=self._explain_testing(testing_score),
                    confidence=0.75,
                )
            )

            # Analyze error handling
            error_handling_score = self._analyze_error_handling(submission_text)
            if error_handling_score > 0:
                metrics.append(
                    ScoringMetric(
                        name="Error Handling",
                        category="technical",
                        score=error_handling_score,
                        weight=0.2,
                        evidence=self._generate_error_handling_evidence(submission_text),
                        explanation=self._explain_error_handling(error_handling_score),
                        confidence=0.8,
                    )
                )
        elif path == PathType.DESIGN:
            # Analyze architecture and design
            architecture_score = self._analyze_architecture(submission_text)
            design_thinking_score = self._analyze_design_thinking(submission_text)

            metrics.append(
                ScoringMetric(
                    name="Architecture",
                    category="design",
                    score=architecture_score,
                    weight=0.4,
                    evidence=self._generate_architecture_evidence(submission_text),
                    explanation=self._explain_architecture(architecture_score),
                    confidence=0.8,
                )
            )

            metrics.append(
                ScoringMetric(
                    name="Design Thinking",
                    category="design",
                    score=design_thinking_score,
                    weight=0.3,
                    evidence=self._generate_design_thinking_evidence(submission_text),
                    explanation=self._explain_design_thinking(design_thinking_score),
                    confidence=0.75,
                )
            )

            # Analyze scalability considerations
            scalability_score = self._analyze_scalability(submission_text)
            if scalability_score > 0:
                metrics.append(
                    ScoringMetric(
                        name="Scalability",
                        category="design",
                        score=scalability_score,
                        weight=0.3,
                        evidence=self._generate_scalability_evidence(submission_text),
                        explanation=self._explain_scalability(scalability_score),
                        confidence=0.7,
                    )
                )

        elif path == PathType.COLLABORATION:
            # Analyze documentation
            documentation_score = self._analyze_documentation(submission_text)

            metrics.append(
                ScoringMetric(
                    name="Documentation",
                    category="collaboration",
                    score=documentation_score,
                    weight=0.3,
                    evidence=self._generate_documentation_evidence(submission_text),
                    explanation=self._explain_documentation(documentation_score),
                    confidence=0.8,
                )
            )

            # Analyze code readability
            readability_score = self._analyze_readability(submission_text)

            metrics.append(
                ScoringMetric(
                    name="Code Readability",
                    category="collaboration",
                    score=readability_score,
                    weight=0.35,
                    evidence=self._generate_readability_evidence(submission_text),
                    explanation=self._explain_readability(readability_score),
                    confidence=0.85,
                )
            )

            # Analyze communication (from explanations)
            communication_score = self._analyze_communication(content)

            metrics.append(
                ScoringMetric(
                    name="Communication",
                    category="collaboration",
                    score=communication_score,
                    weight=0.35,
                    evidence=self._generate_communication_evidence(content),
                    explanation=self._explain_communication(communication_score),
                    confidence=0.75,
                )
            )

        elif path == PathType.PROBLEM_SOLVING:
            # Analyze analytical thinking
            analytical_score = self._analyze_analytical_thinking(submission_text)

            metrics.append(
                ScoringMetric(
                    name="Analytical Thinking",
                    category="problem_solving",
                    score=analytical_score,
                    weight=0.3,
                    evidence=self._generate_analytical_evidence(submission_text),
                    explanation=self._explain_analytical_thinking(analytical_score),
                    confidence=0.8,
                )
            )

            # Analyze debugging approach
            debugging_score = self._analyze_debugging_approach(submission_text)

            metrics.append(
                ScoringMetric(
                    name="Debugging Approach",
                    category="problem_solving",
                    score=debugging_score,
                    weight=0.25,
                    evidence=self._generate_debugging_evidence(submission_text),
                    explanation=self._explain_debugging(debugging_score),
                    confidence=0.75,
                )
            )

            # Analyze optimization
            optimization_score = self._analyze_optimization(submission_text)

            metrics.append(
                ScoringMetric(
                    name="Optimization",
                    category="problem_solving",
                    score=optimization_score,
                    weight=0.25,
                    evidence=self._generate_optimization_evidence(submission_text),
                    explanation=self._explain_optimization(optimization_score),
                    confidence=0.7,
                )
            )

            # Analyze complexity handling
            complexity_score = self._analyze_complexity_handling(submission_text)

            metrics.append(
                ScoringMetric(
                    name="Complexity Handling",
                    category="problem_solving",
                    score=complexity_score,
                    weight=0.2,
                    evidence=self._generate_complexity_evidence(submission_text),
                    explanation=self._explain_complexity(complexity_score),
                    confidence=0.75,
                )
            )

        return metrics

    def _identify_micro_motives(
        self, path: PathType, input_data: AssessmentInput
    ) -> List[MicroMotive]:
        """
        Identify micro-motives using Dark Horse model.

        Analyzes submission content to identify underlying motivations.
        """
        motives = []
        content = input_data.content
        submission_text = self._extract_text_content(content)
        text_lower = submission_text.lower()

        # Analyze for different motive types based on content
        if path == PathType.TECHNICAL:
            # Mastery motive
            mastery_indicators = []
            mastery_strength = 0.5

            if any(
                word in text_lower for word in ["algorithm", "optimize", "efficient", "complexity"]
            ):
                mastery_indicators.append("Deep technical understanding")
                mastery_strength += 0.2

            if "pattern" in text_lower or "design" in text_lower:
                mastery_indicators.append("Design pattern awareness")
                mastery_strength += 0.15

            if mastery_indicators:
                motives.append(
                    MicroMotive(
                        motive_type=MotiveType.MASTERY,
                        strength=min(1.0, mastery_strength),
                        indicators=mastery_indicators,
                        evidence=self._generate_motive_evidence(
                            submission_text, MotiveType.MASTERY
                        ),
                        path_alignment=path,
                    )
                )

            # Quality motive
            quality_indicators = []
            quality_strength = 0.4

            if "test" in text_lower or "error" in text_lower:
                quality_indicators.append("Quality-focused approach")
                quality_strength += 0.2

            if "clean" in text_lower or "readable" in text_lower:
                quality_indicators.append("Code quality awareness")
                quality_strength += 0.15

            if quality_indicators:
                motives.append(
                    MicroMotive(
                        motive_type=MotiveType.QUALITY,
                        strength=min(1.0, quality_strength),
                        indicators=quality_indicators,
                        evidence=self._generate_motive_evidence(
                            submission_text, MotiveType.QUALITY
                        ),
                        path_alignment=path,
                    )
                )

            # Efficiency motive
            if "optimize" in text_lower or "performance" in text_lower:
                motives.append(
                    MicroMotive(
                        motive_type=MotiveType.EFFICIENCY,
                        strength=0.6,
                        indicators=["Performance optimization focus"],
                        evidence=self._generate_motive_evidence(
                            submission_text, MotiveType.EFFICIENCY
                        ),
                        path_alignment=path,
                    )
                )

        elif path == PathType.DESIGN:
            # Innovation motive
            innovation_indicators = []
            innovation_strength = 0.4

            if "alternative" in text_lower or "approach" in text_lower:
                innovation_indicators.append("Explores multiple approaches")
                innovation_strength += 0.2

            if "creative" in text_lower or "novel" in text_lower:
                innovation_indicators.append("Creative thinking")
                innovation_strength += 0.15

            if innovation_indicators:
                motives.append(
                    MicroMotive(
                        motive_type=MotiveType.INNOVATION,
                        strength=min(1.0, innovation_strength),
                        indicators=innovation_indicators,
                        evidence=self._generate_motive_evidence(
                            submission_text, MotiveType.INNOVATION
                        ),
                        path_alignment=path,
                    )
                )

        elif path == PathType.COLLABORATION:
            # Collaboration motive
            collab_indicators = []
            collab_strength = 0.4

            if "document" in text_lower or "comment" in text_lower:
                collab_indicators.append("Documentation focus")
                collab_strength += 0.2

            if "team" in text_lower or "collaborate" in text_lower:
                collab_indicators.append("Team-oriented thinking")
                collab_strength += 0.15

            if collab_indicators:
                motives.append(
                    MicroMotive(
                        motive_type=MotiveType.COLLABORATION,
                        strength=min(1.0, collab_strength),
                        indicators=collab_indicators,
                        evidence=self._generate_motive_evidence(
                            submission_text, MotiveType.COLLABORATION
                        ),
                        path_alignment=path,
                    )
                )

        elif path == PathType.PROBLEM_SOLVING:
            # Exploration motive
            exploration_indicators = []
            exploration_strength = 0.4

            if "explore" in text_lower or "investigate" in text_lower:
                exploration_indicators.append("Exploratory approach")
                exploration_strength += 0.2

            if "analyze" in text_lower or "break" in text_lower:
                exploration_indicators.append("Analytical exploration")
                exploration_strength += 0.15

            if exploration_indicators:
                motives.append(
                    MicroMotive(
                        motive_type=MotiveType.EXPLORATION,
                        strength=min(1.0, exploration_strength),
                        indicators=exploration_indicators,
                        evidence=self._generate_motive_evidence(
                            submission_text, MotiveType.EXPLORATION
                        ),
                        path_alignment=path,
                    )
                )

        return motives

    def _generate_motive_evidence(self, text: str, motive_type: MotiveType) -> List[Evidence]:
        """Generate evidence for a micro-motive."""
        evidence = []
        text_lower = text.lower()

        # Generate evidence based on motive type
        if motive_type == MotiveType.MASTERY:
            if "algorithm" in text_lower or "optimize" in text_lower:
                evidence.append(
                    Evidence(
                        type=EvidenceType.CODE_QUALITY,
                        description="Technical depth indicators present",
                        source="content_analysis",
                        weight=0.6,
                    )
                )
        elif motive_type == MotiveType.QUALITY:
            if "test" in text_lower or "error" in text_lower:
                evidence.append(
                    Evidence(
                        type=EvidenceType.TESTING,
                        description="Quality-focused indicators present",
                        source="content_analysis",
                        weight=0.6,
                    )
                )

        return evidence

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

    def _determine_dominant_path(self, path_scores: List[PathScore]) -> Optional[PathType]:
        """Determine the dominant assessment path."""
        if not path_scores:
            return None
        return max(path_scores, key=lambda ps: ps.overall_score).path

    def _identify_strengths(self, metrics: List[ScoringMetric]) -> List[str]:
        """Identify strengths from metrics."""
        return [f"{m.name}: {m.explanation}" for m in metrics if m.score >= 75.0]

    def _identify_improvements(self, metrics: List[ScoringMetric]) -> List[str]:
        """Identify areas for improvement."""
        return [
            f"{m.name}: Consider enhancing this area (current score: {m.score:.0f})"
            for m in metrics
            if m.score < 75.0
        ]

    def _generate_summary(self, path_scores: List[PathScore], motives: List[MicroMotive]) -> str:
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
                recommendations.append(f"Focus on {ps.path.value}: {ps.areas_for_improvement[0]}")
        return recommendations

    # Content Analysis Helper Methods

    def _extract_text_content(self, content: Dict[str, Any]) -> str:
        """Extract text content from submission."""
        text_parts = []

        # Try common content keys
        for key in ["code", "text", "content", "solution", "submission"]:
            if key in content:
                value = content[key]
                if isinstance(value, str):
                    text_parts.append(value)
                elif isinstance(value, list):
                    text_parts.extend(str(v) for v in value)

        # If no specific key, convert entire content to string
        if not text_parts:
            text_parts.append(str(content))

        return "\n".join(text_parts)

    def _analyze_code_quality(
        self, text: str, pattern_violations: Optional[List[PatternViolation]] = None
    ) -> float:
        """
        Analyze code quality using heuristics.

        Refined to prioritize "Density of Logic" over "Substantial Code"
        to align with minimalism and subtext preference.
        """
        score = 50.0  # Base score
        text_lower = text.lower()
        lines = text.split("\n")
        non_empty_lines = [
            line.strip() for line in lines if line.strip() and not line.strip().startswith("#")
        ]

        # Positive indicators - prioritize logic density
        if "def " in text or "function " in text or "class " in text:
            score += 10  # Structured code
        if "import " in text or "from " in text:
            score += 5  # Uses libraries

        # Density of Logic: Calculate meaningful code density
        logic_density = len(non_empty_lines) / max(len(lines), 1)
        if logic_density > 0.7:  # High density of meaningful code
            score += 8  # Prefer concise, logic-dense code
        elif logic_density > 0.5:
            score += 5

        if "try:" in text or "except" in text or "error" in text_lower:
            score += 10  # Error handling
        if "test" in text_lower or "assert" in text_lower:
            score += 10  # Testing awareness

        # Check for meaningful abstractions (functions, classes) relative to code size
        function_count = text.count("def ") + text.count("function ")
        class_count = text.count("class ")
        if len(non_empty_lines) > 0:
            abstraction_ratio = (function_count + class_count) / len(non_empty_lines)
            if abstraction_ratio > 0.1:  # Good abstraction density
                score += 7

        # Negative indicators
        if text.count("print(") > 5:
            score -= 5  # Too many prints (debugging code)
        if "todo" in text_lower or "fixme" in text_lower:
            score -= 3  # Incomplete code
        if len(non_empty_lines) > 0 and logic_density < 0.3:
            score -= 5  # Low logic density (too much whitespace/comments)

        if pattern_violations and self.pattern_checks_enabled:
            score -= self._calculate_pattern_penalty(pattern_violations)

        return min(100.0, max(0.0, score))

    def _generate_code_quality_evidence(
        self, text: str, pattern_violations: Optional[List[PatternViolation]] = None
    ) -> List[Evidence]:
        """Generate evidence for code quality."""
        evidence = []

        if "def " in text or "function " in text:
            evidence.append(
                Evidence(
                    type=EvidenceType.CODE_QUALITY,
                    description="Code uses functions/methods for organization",
                    source="code_structure",
                    weight=0.7,
                )
            )

        if "try:" in text or "except" in text:
            evidence.append(
                Evidence(
                    type=EvidenceType.CODE_QUALITY,
                    description="Error handling present in code",
                    source="error_handling",
                    weight=0.8,
                )
            )

        if pattern_violations and self.pattern_checks_enabled:
            for violation in pattern_violations[:10]:
                evidence.append(
                    Evidence(
                        type=EvidenceType.CODE_QUALITY,
                        description=(
                            f"Pattern violation: {violation.pattern} - " f"{violation.description}"
                        ),
                        source="pattern_checks",
                        weight=self._pattern_violation_weight(violation.severity),
                        metadata=violation.to_dict(),
                    )
                )

        return evidence

    def _calculate_pattern_penalty(self, violations: List[PatternViolation]) -> float:
        """Calculate penalty points based on pattern violations."""
        return calculate_pattern_penalty(
            violations, self.pattern_penalty_weights, self.pattern_penalty_max
        )

    def _pattern_violation_weight(self, severity: str) -> float:
        """Map violation severity to evidence weight."""
        weights = {
            "critical": 1.0,
            "high": 0.9,
            "medium": 0.7,
            "low": 0.5,
        }
        return weights.get(severity, 0.6)

    def _explain_code_quality(self, score: float, violation_count: int = 0) -> str:
        """Explain code quality score."""
        pattern_note = ""
        if violation_count > 0 and self.pattern_checks_enabled:
            pattern_note = (
                f" Pattern checks flagged {violation_count} potential issue"
                f"{'s' if violation_count != 1 else ''}."
            )

        if score >= 80:
            return (
                "Code demonstrates strong quality with good structure and practices" + pattern_note
            )
        elif score >= 60:
            return "Code shows solid fundamentals with room for improvement" + pattern_note
        else:
            return (
                "Code quality could be enhanced with better structure and practices" + pattern_note
            )

    def _analyze_problem_solving(self, text: str) -> float:
        """Analyze problem-solving approach."""
        score = 50.0
        text_lower = text.lower()

        # Algorithm indicators
        if any(word in text_lower for word in ["algorithm", "complexity", "optimize", "efficient"]):
            score += 15
        if any(word in text_lower for word in ["loop", "iterate", "recursion", "recursive"]):
            score += 10
        if "if " in text or "else" in text or "switch" in text_lower:
            score += 5  # Conditional logic

        # Approach indicators
        if any(word in text_lower for word in ["approach", "strategy", "method", "solution"]):
            score += 10

        return min(100.0, max(0.0, score))

    def _generate_problem_solving_evidence(self, text: str) -> List[Evidence]:
        """Generate evidence for problem solving."""
        evidence = []
        text_lower = text.lower()

        if "optimize" in text_lower or "efficient" in text_lower:
            evidence.append(
                Evidence(
                    type=EvidenceType.CODE_QUALITY,
                    description="Shows awareness of optimization",
                    source="code_analysis",
                    weight=0.7,
                )
            )

        return evidence

    def _explain_problem_solving(self, score: float) -> str:
        """Explain problem-solving score."""
        if score >= 75:
            return "Demonstrates strong problem-solving with clear approach"
        elif score >= 55:
            return "Shows good problem-solving fundamentals"
        else:
            return "Problem-solving approach could be more systematic"

    def _analyze_testing(self, text: str) -> float:
        """Analyze testing approach."""
        score = 30.0  # Lower base (testing is often missing)
        text_lower = text.lower()

        if "test" in text_lower:
            score += 20
        if "assert" in text_lower:
            score += 15
        if "mock" in text_lower or "stub" in text_lower:
            score += 10
        if "coverage" in text_lower:
            score += 10

        return min(100.0, max(0.0, score))

    def _generate_testing_evidence(self, text: str) -> List[Evidence]:
        """Generate evidence for testing."""
        evidence = []
        text_lower = text.lower()

        if "test" in text_lower:
            evidence.append(
                Evidence(
                    type=EvidenceType.TESTING,
                    description="Testing mentioned or present",
                    source="code_analysis",
                    weight=0.6,
                )
            )

        return evidence

    def _explain_testing(self, score: float) -> str:
        """Explain testing score."""
        if score >= 70:
            return "Good testing awareness and practices"
        elif score >= 40:
            return "Some testing present but could be more comprehensive"
        else:
            return "Testing approach needs development"

    def _analyze_error_handling(self, text: str) -> float:
        """Analyze error handling."""
        score = 40.0
        text_lower = text.lower()

        if "try:" in text or "except" in text:
            score += 25
        if "error" in text_lower or "exception" in text_lower:
            score += 15
        if "validate" in text_lower or "check" in text_lower:
            score += 10

        return min(100.0, max(0.0, score))

    def _generate_error_handling_evidence(self, text: str) -> List[Evidence]:
        """Generate evidence for error handling."""
        evidence = []

        if "try:" in text or "except" in text:
            evidence.append(
                Evidence(
                    type=EvidenceType.CODE_QUALITY,
                    description="Explicit error handling present",
                    source="code_analysis",
                    weight=0.8,
                )
            )

        return evidence

    def _explain_error_handling(self, score: float) -> str:
        """Explain error handling score."""
        if score >= 70:
            return "Robust error handling demonstrated"
        elif score >= 50:
            return "Basic error handling present"
        else:
            return "Error handling could be improved"

    def _analyze_architecture(self, text: str) -> float:
        """Analyze architecture and design."""
        score = 50.0
        text_lower = text.lower()

        if "class " in text or "module" in text_lower:
            score += 15
        if "interface" in text_lower or "abstract" in text_lower:
            score += 10
        if "pattern" in text_lower or "design" in text_lower:
            score += 10
        if "separation" in text_lower or "modular" in text_lower:
            score += 10

        return min(100.0, max(0.0, score))

    def _generate_architecture_evidence(self, text: str) -> List[Evidence]:
        """Generate evidence for architecture."""
        evidence = []

        if "class " in text:
            evidence.append(
                Evidence(
                    type=EvidenceType.ARCHITECTURE,
                    description="Object-oriented structure present",
                    source="code_structure",
                    weight=0.7,
                )
            )

        return evidence

    def _explain_architecture(self, score: float) -> str:
        """Explain architecture score."""
        if score >= 75:
            return "Well-structured architecture with clear organization"
        elif score >= 55:
            return "Good architectural awareness"
        else:
            return "Architecture could be more structured"

    def _analyze_design_thinking(self, text: str) -> float:
        """Analyze design thinking."""
        score = 50.0
        text_lower = text.lower()

        if any(word in text_lower for word in ["consider", "think", "approach", "design"]):
            score += 15
        if "trade" in text_lower and "off" in text_lower:
            score += 10
        if "alternative" in text_lower or "option" in text_lower:
            score += 10

        return min(100.0, max(0.0, score))

    def _generate_design_thinking_evidence(self, text: str) -> List[Evidence]:
        """Generate evidence for design thinking."""
        evidence = []
        text_lower = text.lower()

        if "consider" in text_lower or "think" in text_lower:
            evidence.append(
                Evidence(
                    type=EvidenceType.ARCHITECTURE,
                    description="Shows thoughtful design consideration",
                    source="content_analysis",
                    weight=0.6,
                )
            )

        return evidence

    def _explain_design_thinking(self, score: float) -> str:
        """Explain design thinking score."""
        if score >= 70:
            return "Demonstrates strong design thinking"
        elif score >= 50:
            return "Shows good design awareness"
        else:
            return "Design thinking could be more explicit"

    def _analyze_scalability(self, text: str) -> float:
        """Analyze scalability considerations."""
        score = 30.0
        text_lower = text.lower()

        if "scale" in text_lower or "scalable" in text_lower:
            score += 20
        if "performance" in text_lower or "efficient" in text_lower:
            score += 15
        if "concurrent" in text_lower or "parallel" in text_lower:
            score += 15

        return min(100.0, max(0.0, score))

    def _generate_scalability_evidence(self, text: str) -> List[Evidence]:
        """Generate evidence for scalability."""
        evidence = []
        text_lower = text.lower()

        if "scale" in text_lower:
            evidence.append(
                Evidence(
                    type=EvidenceType.ARCHITECTURE,
                    description="Scalability considerations mentioned",
                    source="content_analysis",
                    weight=0.6,
                )
            )

        return evidence

    def _explain_scalability(self, score: float) -> str:
        """Explain scalability score."""
        if score >= 60:
            return "Shows awareness of scalability concerns"
        else:
            return "Scalability considerations could be enhanced"

    def _analyze_documentation(self, text: str) -> float:
        """Analyze documentation quality."""
        score = 40.0
        text_lower = text.lower()

        # Check for comments
        comment_ratio = text.count("#") + text.count("//") + text.count("/*")
        if comment_ratio > len(text) / 50:  # Reasonable comment ratio
            score += 20

        if "readme" in text_lower or "doc" in text_lower:
            score += 15
        if '"""' in text or "'''" in text:  # Docstrings
            score += 15

        return min(100.0, max(0.0, score))

    def _generate_documentation_evidence(self, text: str) -> List[Evidence]:
        """Generate evidence for documentation."""
        evidence = []

        if '"""' in text or "'''" in text:
            evidence.append(
                Evidence(
                    type=EvidenceType.DOCUMENTATION,
                    description="Docstrings present in code",
                    source="code_analysis",
                    weight=0.7,
                )
            )

        return evidence

    def _explain_documentation(self, score: float) -> str:
        """Explain documentation score."""
        if score >= 70:
            return "Good documentation practices demonstrated"
        elif score >= 50:
            return "Some documentation present"
        else:
            return "Documentation could be improved"

    def _analyze_readability(self, text: str) -> float:
        """Analyze code readability."""
        score = 60.0

        # Check for meaningful variable names
        lines = text.split("\n")
        meaningful_names = sum(
            1
            for line in lines
            if any(word in line.lower() for word in ["name", "value", "result", "data", "item"])
        )
        if meaningful_names > len(lines) / 10:
            score += 15

        # Check line length (reasonable lines)
        avg_line_length = sum(len(line) for line in lines) / max(len(lines), 1)
        if 20 < avg_line_length < 100:
            score += 10

        return min(100.0, max(0.0, score))

    def _generate_readability_evidence(self, text: str) -> List[Evidence]:
        """Generate evidence for readability."""
        evidence = []

        evidence.append(
            Evidence(
                type=EvidenceType.CODE_QUALITY,
                description="Code structure analyzed for readability",
                source="code_analysis",
                weight=0.6,
            )
        )

        return evidence

    def _explain_readability(self, score: float) -> str:
        """Explain readability score."""
        if score >= 70:
            return "Code is readable and well-structured"
        elif score >= 55:
            return "Code readability is acceptable"
        else:
            return "Code readability could be improved"

    def _analyze_communication(self, content: Dict[str, Any]) -> float:
        """Analyze communication quality from explanations."""
        score = 50.0

        # Look for explanation fields
        explanation_text = ""
        for key in ["explanation", "reasoning", "approach", "thinking"]:
            if key in content:
                explanation_text += str(content[key]) + " "

        if len(explanation_text) > 50:
            score += 20
        if len(explanation_text) > 200:
            score += 15

        return min(100.0, max(0.0, score))

    def _generate_communication_evidence(self, content: Dict[str, Any]) -> List[Evidence]:
        """Generate evidence for communication."""
        evidence = []

        if any(key in content for key in ["explanation", "reasoning", "approach"]):
            evidence.append(
                Evidence(
                    type=EvidenceType.COMMUNICATION,
                    description="Explanations provided with submission",
                    source="submission_content",
                    weight=0.7,
                )
            )

        return evidence

    def _explain_communication(self, score: float) -> str:
        """Explain communication score."""
        if score >= 70:
            return "Clear and effective communication"
        elif score >= 50:
            return "Good communication demonstrated"
        else:
            return "Communication could be more detailed"

    def _analyze_analytical_thinking(self, text: str) -> float:
        """Analyze analytical thinking."""
        score = 50.0
        text_lower = text.lower()

        if any(word in text_lower for word in ["analyze", "analysis", "break", "down", "step"]):
            score += 15
        if "logic" in text_lower or "reasoning" in text_lower:
            score += 10
        if "pattern" in text_lower:
            score += 10

        return min(100.0, max(0.0, score))

    def _generate_analytical_evidence(self, text: str) -> List[Evidence]:
        """Generate evidence for analytical thinking."""
        evidence = []
        text_lower = text.lower()

        if "analyze" in text_lower or "break" in text_lower:
            evidence.append(
                Evidence(
                    type=EvidenceType.CODE_QUALITY,
                    description="Shows analytical approach",
                    source="content_analysis",
                    weight=0.6,
                )
            )

        return evidence

    def _explain_analytical_thinking(self, score: float) -> str:
        """Explain analytical thinking score."""
        if score >= 70:
            return "Strong analytical thinking demonstrated"
        elif score >= 50:
            return "Good analytical approach"
        else:
            return "Analytical thinking could be more explicit"

    def _analyze_debugging_approach(self, text: str) -> float:
        """Analyze debugging approach."""
        score = 40.0
        text_lower = text.lower()

        if "debug" in text_lower or "fix" in text_lower:
            score += 15
        if "error" in text_lower or "issue" in text_lower:
            score += 10
        if "test" in text_lower:
            score += 10

        return min(100.0, max(0.0, score))

    def _generate_debugging_evidence(self, text: str) -> List[Evidence]:
        """Generate evidence for debugging."""
        evidence = []
        text_lower = text.lower()

        if "debug" in text_lower:
            evidence.append(
                Evidence(
                    type=EvidenceType.CODE_QUALITY,
                    description="Debugging approach evident",
                    source="content_analysis",
                    weight=0.6,
                )
            )

        return evidence

    def _explain_debugging(self, score: float) -> str:
        """Explain debugging score."""
        if score >= 60:
            return "Good debugging awareness"
        else:
            return "Debugging approach could be more systematic"

    def _analyze_optimization(self, text: str) -> float:
        """Analyze optimization approach."""
        score = 40.0
        text_lower = text.lower()

        if "optimize" in text_lower or "optimization" in text_lower:
            score += 20
        if "efficient" in text_lower or "performance" in text_lower:
            score += 15
        if "complexity" in text_lower or "big o" in text_lower:
            score += 15

        return min(100.0, max(0.0, score))

    def _generate_optimization_evidence(self, text: str) -> List[Evidence]:
        """Generate evidence for optimization."""
        evidence = []
        text_lower = text.lower()

        if "optimize" in text_lower:
            evidence.append(
                Evidence(
                    type=EvidenceType.CODE_QUALITY,
                    description="Optimization considerations present",
                    source="content_analysis",
                    weight=0.6,
                )
            )

        return evidence

    def _explain_optimization(self, score: float) -> str:
        """Explain optimization score."""
        if score >= 65:
            return "Shows good optimization awareness"
        else:
            return "Optimization considerations could be enhanced"

    def _analyze_complexity_handling(self, text: str) -> float:
        """Analyze complexity handling."""
        score = 50.0
        text_lower = text.lower()

        if "complex" in text_lower or "complexity" in text_lower:
            score += 10
        if "simple" in text_lower or "simplify" in text_lower:
            score += 10
        if len(text.split("\n")) > 50:
            score += 10  # Handles larger codebases

        return min(100.0, max(0.0, score))

    def _generate_complexity_evidence(self, text: str) -> List[Evidence]:
        """Generate evidence for complexity handling."""
        evidence = []

        evidence.append(
            Evidence(
                type=EvidenceType.CODE_QUALITY,
                description="Code complexity analyzed",
                source="code_analysis",
                weight=0.5,
            )
        )

        return evidence

    def _explain_complexity(self, score: float) -> str:
        """Explain complexity handling score."""
        if score >= 65:
            return "Good handling of complexity"
        else:
            return "Complexity management could be improved"
