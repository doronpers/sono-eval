from typing import List, Optional

from sono_eval.assessment.helpers import extract_text_content
from sono_eval.assessment.models import (
    AssessmentInput,
    Evidence,
    EvidenceType,
    PathType,
    ScoringMetric,
)
from sono_eval.assessment.pattern_checks import PatternViolation, calculate_pattern_penalty


class HeuristicScorer:
    """Handles heuristic-based scoring for different assessment paths."""

    def __init__(self, config):
        self.config = config
        self.pattern_checks_enabled = config.pattern_checks_enabled
        self.pattern_penalty_weights = {
            "low": config.pattern_penalty_low,
            "medium": config.pattern_penalty_medium,
            "high": config.pattern_penalty_high,
            "critical": config.pattern_penalty_high,
        }
        self.pattern_penalty_max = config.pattern_penalty_max

    def generate_metrics_for_path(
        self,
        path: PathType,
        input_data: AssessmentInput,
        pattern_violations: Optional[List[PatternViolation]] = None,
    ) -> List[ScoringMetric]:
        """Generate scoring metrics for a specific path."""
        metrics = []
        content = input_data.content
        submission_text = extract_text_content(content)

        if path == PathType.TECHNICAL:
            metrics.extend(self._analyze_technical(submission_text, pattern_violations))
        elif path == PathType.DESIGN:
            metrics.extend(self._analyze_design(submission_text))
        elif path == PathType.COLLABORATION:
            metrics.extend(self._analyze_collaboration(submission_text, content))
        elif path == PathType.PROBLEM_SOLVING:
            metrics.extend(self._analyze_problem_solving_path(submission_text))

        return metrics

    def _analyze_technical(
        self, text: str, pattern_violations: Optional[List[PatternViolation]]
    ) -> List[ScoringMetric]:
        metrics = []

        # Code Quality
        code_score = self._analyze_code_quality(text, pattern_violations)
        code_evidence = self._generate_code_quality_evidence(text, pattern_violations)
        violation_count = len(pattern_violations or [])

        metrics.append(
            ScoringMetric(
                name="Code Quality",
                category="technical",
                score=code_score,
                weight=0.3,
                evidence=code_evidence,
                explanation=self._explain_code_quality(code_score, violation_count),
                confidence=0.85,
            )
        )

        # Problem Solving (Technical Context)
        ps_score = self._analyze_problem_solving(text)
        metrics.append(
            ScoringMetric(
                name="Problem Solving",
                category="technical",
                score=ps_score,
                weight=0.3,
                evidence=self._generate_problem_solving_evidence(text),
                explanation=self._explain_problem_solving(ps_score),
                confidence=0.8,
            )
        )

        # Testing
        test_score = self._analyze_testing(text)
        metrics.append(
            ScoringMetric(
                name="Testing",
                category="technical",
                score=test_score,
                weight=0.2,
                evidence=self._generate_testing_evidence(text),
                explanation=self._explain_testing(test_score),
                confidence=0.75,
            )
        )

        # Error Handling
        err_score = self._analyze_error_handling(text)
        if err_score > 0:
            metrics.append(
                ScoringMetric(
                    name="Error Handling",
                    category="technical",
                    score=err_score,
                    weight=0.2,
                    evidence=self._generate_error_handling_evidence(text),
                    explanation=self._explain_error_handling(err_score),
                    confidence=0.8,
                )
            )

        return metrics

    def _analyze_design(self, text: str) -> List[ScoringMetric]:
        metrics = []

        # Architecture
        arch_score = self._analyze_architecture(text)
        metrics.append(
            ScoringMetric(
                name="Architecture",
                category="design",
                score=arch_score,
                weight=0.4,
                evidence=self._generate_architecture_evidence(text),
                explanation=self._explain_architecture(arch_score),
                confidence=0.8,
            )
        )

        # Design Thinking
        dt_score = self._analyze_design_thinking(text)
        metrics.append(
            ScoringMetric(
                name="Design Thinking",
                category="design",
                score=dt_score,
                weight=0.3,
                evidence=self._generate_design_thinking_evidence(text),
                explanation=self._explain_design_thinking(dt_score),
                confidence=0.75,
            )
        )

        # Scalability
        scale_score = self._analyze_scalability(text)
        if scale_score > 0:
            metrics.append(
                ScoringMetric(
                    name="Scalability",
                    category="design",
                    score=scale_score,
                    weight=0.3,
                    evidence=self._generate_scalability_evidence(text),
                    explanation=self._explain_scalability(scale_score),
                    confidence=0.7,
                )
            )

        return metrics

    def _analyze_collaboration(self, text: str, content: dict) -> List[ScoringMetric]:
        metrics = []

        # Documentation
        doc_score = self._analyze_documentation(text)
        metrics.append(
            ScoringMetric(
                name="Documentation",
                category="collaboration",
                score=doc_score,
                weight=0.3,
                evidence=self._generate_documentation_evidence(text),
                explanation=self._explain_documentation(doc_score),
                confidence=0.8,
            )
        )

        # Readability
        read_score = self._analyze_readability(text)
        metrics.append(
            ScoringMetric(
                name="Code Readability",
                category="collaboration",
                score=read_score,
                weight=0.35,
                evidence=self._generate_readability_evidence(text),
                explanation=self._explain_readability(read_score),
                confidence=0.85,
            )
        )

        # Communication
        comm_score = self._analyze_communication(content)
        metrics.append(
            ScoringMetric(
                name="Communication",
                category="collaboration",
                score=comm_score,
                weight=0.35,
                evidence=self._generate_communication_evidence(content),
                explanation=self._explain_communication(comm_score),
                confidence=0.75,
            )
        )

        return metrics

    def _analyze_problem_solving_path(self, text: str) -> List[ScoringMetric]:
        metrics = []

        # Analytical Thinking
        anal_score = self._analyze_analytical_thinking(text)
        metrics.append(
            ScoringMetric(
                name="Analytical Thinking",
                category="problem_solving",
                score=anal_score,
                weight=0.3,
                evidence=self._generate_analytical_evidence(text),
                explanation=self._explain_analytical_thinking(anal_score),
                confidence=0.8,
            )
        )

        # Debugging
        debug_score = self._analyze_debugging_approach(text)
        metrics.append(
            ScoringMetric(
                name="Debugging Approach",
                category="problem_solving",
                score=debug_score,
                weight=0.25,
                evidence=self._generate_debugging_evidence(text),
                explanation=self._explain_debugging(debug_score),
                confidence=0.75,
            )
        )

        # Optimization
        opt_score = self._analyze_optimization(text)
        metrics.append(
            ScoringMetric(
                name="Optimization",
                category="problem_solving",
                score=opt_score,
                weight=0.25,
                evidence=self._generate_optimization_evidence(text),
                explanation=self._explain_optimization(opt_score),
                confidence=0.7,
            )
        )

        # Complexity
        comp_score = self._analyze_complexity_handling(text)
        metrics.append(
            ScoringMetric(
                name="Complexity Handling",
                category="problem_solving",
                score=comp_score,
                weight=0.2,
                evidence=self._generate_complexity_evidence(text),
                explanation=self._explain_complexity(comp_score),
                confidence=0.75,
            )
        )

        return metrics

    # --- Analysis Implementation Methods ---

    def _analyze_code_quality(
        self, text: str, pattern_violations: Optional[List[PatternViolation]] = None
    ) -> float:
        score = 50.0
        text_lower = text.lower()
        lines = text.split("\n")
        non_empty_lines = [
            line.strip() for line in lines if line.strip() and not line.strip().startswith("#")
        ]

        if "def " in text or "function " in text or "class " in text:
            score += 10
        if "import " in text or "from " in text:
            score += 5

        logic_density = len(non_empty_lines) / max(len(lines), 1)
        if logic_density > 0.7:
            score += 8
        elif logic_density > 0.5:
            score += 5

        if "try:" in text or "except" in text or "error" in text_lower:
            score += 10
        if "test" in text_lower or "assert" in text_lower:
            score += 10

        function_count = text.count("def ") + text.count("function ")
        class_count = text.count("class ")
        if len(non_empty_lines) > 0:
            abstraction_ratio = (function_count + class_count) / len(non_empty_lines)
            if abstraction_ratio > 0.1:
                score += 7

        if text.count("print(") > 5:
            score -= 5
        if "todo" in text_lower or "fixme" in text_lower:
            score -= 3
        if len(non_empty_lines) > 0 and logic_density < 0.3:
            score -= 5

        if pattern_violations and self.pattern_checks_enabled:
            score -= calculate_pattern_penalty(
                pattern_violations,
                self.pattern_penalty_weights,
                self.pattern_penalty_max,
            )

        return min(100.0, max(0.0, score))

    def _generate_code_quality_evidence(
        self, text: str, pattern_violations: Optional[List[PatternViolation]] = None
    ) -> List[Evidence]:
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
            weights = {
                "critical": 1.0,
                "high": 0.9,
                "medium": 0.7,
                "low": 0.5,
            }
            for violation in pattern_violations[:10]:
                evidence.append(
                    Evidence(
                        type=EvidenceType.CODE_QUALITY,
                        description=(
                            f"Pattern violation: {violation.pattern} - " f"{violation.description}"
                        ),
                        source="pattern_checks",
                        weight=weights.get(violation.severity, 0.6),
                        metadata=violation.to_dict(),
                    )
                )
        return evidence

    def _explain_code_quality(self, score: float, violation_count: int = 0) -> str:
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

    # ... (Other methods continue in same pattern)
    # I will rely on the fact that I've seen the other methods and can implement them,
    # but to be concise in this tool call, I will include them all.

    def _analyze_problem_solving(self, text: str) -> float:
        score = 50.0
        text_lower = text.lower()
        if any(w in text_lower for w in ["algorithm", "complexity", "optimize", "efficient"]):
            score += 15
        if any(w in text_lower for w in ["loop", "iterate", "recursion", "recursive"]):
            score += 10
        if "if " in text or "else" in text or "switch" in text_lower:
            score += 5
        if any(w in text_lower for w in ["approach", "strategy", "method", "solution"]):
            score += 10
        return min(100.0, max(0.0, score))

    def _generate_problem_solving_evidence(self, text: str) -> List[Evidence]:
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
        if score >= 75:
            return "Demonstrates strong problem-solving with clear approach"
        elif score >= 55:
            return "Shows good problem-solving fundamentals"
        return "Problem-solving approach could be more systematic"

    def _analyze_testing(self, text: str) -> float:
        score = 30.0
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
        evidence = []
        if "test" in text.lower():
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
        if score >= 70:
            return "Good testing awareness and practices"
        elif score >= 40:
            return "Some testing present but could be more comprehensive"
        return "Testing approach needs development"

    def _analyze_error_handling(self, text: str) -> float:
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
        if score >= 70:
            return "Robust error handling demonstrated"
        elif score >= 50:
            return "Basic error handling present"
        return "Error handling could be improved"

    def _analyze_architecture(self, text: str) -> float:
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
        if score >= 75:
            return "Well-structured architecture with clear organization"
        elif score >= 55:
            return "Good architectural awareness"
        return "Architecture could be more structured"

    def _analyze_design_thinking(self, text: str) -> float:
        score = 50.0
        text_lower = text.lower()
        if any(w in text_lower for w in ["consider", "think", "approach", "design"]):
            score += 15
        if "trade" in text_lower and "off" in text_lower:
            score += 10
        if "alternative" in text_lower or "option" in text_lower:
            score += 10
        return min(100.0, max(0.0, score))

    def _generate_design_thinking_evidence(self, text: str) -> List[Evidence]:
        evidence = []
        if "consider" in text.lower() or "think" in text.lower():
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
        if score >= 70:
            return "Demonstrates strong design thinking"
        elif score >= 50:
            return "Shows good design awareness"
        return "Design thinking could be more explicit"

    def _analyze_scalability(self, text: str) -> float:
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
        evidence = []
        if "scale" in text.lower():
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
        if score >= 60:
            return "Shows awareness of scalability concerns"
        return "Scalability considerations could be enhanced"

    def _analyze_documentation(self, text: str) -> float:
        score = 40.0
        text_lower = text.lower()
        comment_ratio = text.count("#") + text.count("//") + text.count("/*")
        if comment_ratio > len(text) / 50:
            score += 20
        if "readme" in text_lower or "doc" in text_lower:
            score += 15
        if '"""' in text or "'''" in text:
            score += 15
        return min(100.0, max(0.0, score))

    def _generate_documentation_evidence(self, text: str) -> List[Evidence]:
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
        if score >= 70:
            return "Good documentation practices demonstrated"
        elif score >= 50:
            return "Some documentation present"
        return "Documentation could be improved"

    def _analyze_readability(self, text: str) -> float:
        score = 60.0
        lines = text.split("\n")
        meaningful_names = sum(
            1
            for line in lines
            if any(w in line.lower() for w in ["name", "value", "result", "data", "item"])
        )
        if meaningful_names > len(lines) / 10:
            score += 15
        avg_line_length = sum(len(line) for line in lines) / max(len(lines), 1)
        if 20 < avg_line_length < 100:
            score += 10
        return min(100.0, max(0.0, score))

    def _generate_readability_evidence(self, text: str) -> List[Evidence]:
        return [
            Evidence(
                type=EvidenceType.CODE_QUALITY,
                description="Code structure analyzed for readability",
                source="code_analysis",
                weight=0.6,
            )
        ]

    def _explain_readability(self, score: float) -> str:
        if score >= 70:
            return "Code is readable and well-structured"
        elif score >= 55:
            return "Code readability is acceptable"
        return "Code readability could be improved"

    def _analyze_communication(self, content: dict) -> float:
        score = 50.0
        explanation_text = ""
        for key in ["explanation", "reasoning", "approach", "thinking"]:
            if key in content:
                explanation_text += str(content[key]) + " "
        if len(explanation_text) > 50:
            score += 20
        if len(explanation_text) > 200:
            score += 15
        return min(100.0, max(0.0, score))

    def _generate_communication_evidence(self, content: dict) -> List[Evidence]:
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
        if score >= 70:
            return "Clear and effective communication"
        elif score >= 50:
            return "Good communication demonstrated"
        return "Communication could be more detailed"

    def _analyze_analytical_thinking(self, text: str) -> float:
        score = 50.0
        text_lower = text.lower()
        if any(w in text_lower for w in ["analyze", "analysis", "break", "down", "step"]):
            score += 15
        if "logic" in text_lower or "reasoning" in text_lower:
            score += 10
        if "pattern" in text_lower:
            score += 10
        return min(100.0, max(0.0, score))

    def _generate_analytical_evidence(self, text: str) -> List[Evidence]:
        evidence = []
        if "analyze" in text.lower() or "break" in text.lower():
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
        if score >= 70:
            return "Strong analytical thinking demonstrated"
        elif score >= 50:
            return "Good analytical approach"
        return "Analytical thinking could be more explicit"

    def _analyze_debugging_approach(self, text: str) -> float:
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
        evidence = []
        if "debug" in text.lower():
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
        if score >= 60:
            return "Good debugging awareness"
        return "Debugging approach could be more systematic"

    def _analyze_optimization(self, text: str) -> float:
        score = 40.0
        text_lower = text.lower()
        if "optimize" in text_lower or "performance" in text_lower:
            score += 15
        if "efficient" in text_lower or "fast" in text_lower:
            score += 10
        if "complexity" in text_lower or "o(" in text_lower:
            score += 15
        return min(100.0, max(0.0, score))

    def _generate_optimization_evidence(self, text: str) -> List[Evidence]:
        evidence = []
        if "o(" in text.lower() or "complexity" in text.lower():
            evidence.append(
                Evidence(
                    type=EvidenceType.CODE_QUALITY,
                    description="Time/space complexity considered",
                    source="code_analysis",
                    weight=0.7,
                )
            )
        return evidence

    def _explain_optimization(self, score: float) -> str:
        if score >= 70:
            return "Strong optimization mindset"
        elif score >= 50:
            return "Aware of optimization"
        return "Optimization could be considered more"

    def _analyze_complexity_handling(self, text: str) -> float:
        score = 50.0
        text_lower = text.lower()
        if "complex" in text_lower or "complexity" in text_lower:
            score += 10
        if "simple" in text_lower or "simplify" in text_lower:
            score += 10
        if len(text.split("\n")) > 50:
            score += 10
        return min(100.0, max(0.0, score))

    def _generate_complexity_evidence(self, text: str) -> List[Evidence]:
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
        if score >= 65:
            return "Good handling of complexity"
        return "Complexity management could be improved"
