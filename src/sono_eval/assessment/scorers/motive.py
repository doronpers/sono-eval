from typing import List

from sono_eval.assessment.helpers import extract_text_content
from sono_eval.assessment.models import (
    AssessmentInput,
    Evidence,
    EvidenceType,
    MicroMotive,
    MotiveType,
    PathType,
)


class MicroMotiveScorer:
    """Handles Micro-Motive (Dark Horse) identification."""

    def identify_micro_motives(
        self, path: PathType, input_data: AssessmentInput
    ) -> List[MicroMotive]:
        """Identify micro-motives using Dark Horse model."""
        motives = []
        content = input_data.content
        submission_text = extract_text_content(content)
        text_lower = submission_text.lower()

        if path == PathType.TECHNICAL:
            motives.extend(self._analyze_technical_motives(text_lower, submission_text, path))
        elif path == PathType.DESIGN:
            motives.extend(self._analyze_design_motives(text_lower, submission_text, path))
        elif path == PathType.COLLABORATION:
            motives.extend(self._analyze_collaboration_motives(text_lower, submission_text, path))
        elif path == PathType.PROBLEM_SOLVING:
            motives.extend(self._analyze_problem_solving_motives(text_lower, submission_text, path))

        return motives

    def _analyze_technical_motives(self, text_lower: str, original_text: str, path: PathType):
        motives = []

        # Mastery
        mastery_inds = []
        mastery_str = 0.5
        if any(w in text_lower for w in ["algorithm", "optimize", "efficient", "complexity"]):
            mastery_inds.append("Deep technical understanding")
            mastery_str += 0.2
        if "pattern" in text_lower or "design" in text_lower:
            mastery_inds.append("Design pattern awareness")
            mastery_str += 0.15

        if mastery_inds:
            motives.append(
                MicroMotive(
                    motive_type=MotiveType.MASTERY,
                    strength=min(1.0, mastery_str),
                    indicators=mastery_inds,
                    evidence=self.generate_motive_evidence(original_text, MotiveType.MASTERY),
                    path_alignment=path,
                )
            )

        # Quality
        quality_inds = []
        quality_str = 0.4
        if "test" in text_lower or "error" in text_lower:
            quality_inds.append("Quality-focused approach")
            quality_str += 0.2
        if "clean" in text_lower or "readable" in text_lower:
            quality_inds.append("Code quality awareness")
            quality_str += 0.15

        if quality_inds:
            motives.append(
                MicroMotive(
                    motive_type=MotiveType.QUALITY,
                    strength=min(1.0, quality_str),
                    indicators=quality_inds,
                    evidence=self.generate_motive_evidence(original_text, MotiveType.QUALITY),
                    path_alignment=path,
                )
            )

        # Efficiency
        if "optimize" in text_lower or "performance" in text_lower:
            motives.append(
                MicroMotive(
                    motive_type=MotiveType.EFFICIENCY,
                    strength=0.6,
                    indicators=["Performance optimization focus"],
                    evidence=self.generate_motive_evidence(original_text, MotiveType.EFFICIENCY),
                    path_alignment=path,
                )
            )

        return motives

    def _analyze_design_motives(self, text_lower: str, original_text: str, path: PathType):
        motives = []

        # Innovation
        innov_inds = []
        innov_str = 0.4
        if "alternative" in text_lower or "approach" in text_lower:
            innov_inds.append("Explores multiple approaches")
            innov_str += 0.2
        if "creative" in text_lower or "novel" in text_lower:
            innov_inds.append("Creative thinking")
            innov_str += 0.15

        if innov_inds:
            motives.append(
                MicroMotive(
                    motive_type=MotiveType.INNOVATION,
                    strength=min(1.0, innov_str),
                    indicators=innov_inds,
                    evidence=self.generate_motive_evidence(original_text, MotiveType.INNOVATION),
                    path_alignment=path,
                )
            )
        return motives

    def _analyze_collaboration_motives(self, text_lower: str, original_text: str, path: PathType):
        motives = []

        # Collaboration
        collab_inds = []
        collab_str = 0.4
        if "document" in text_lower or "comment" in text_lower:
            collab_inds.append("Documentation focus")
            collab_str += 0.2
        if "team" in text_lower or "collaborate" in text_lower:
            collab_inds.append("Team-oriented thinking")
            collab_str += 0.15

        if collab_inds:
            motives.append(
                MicroMotive(
                    motive_type=MotiveType.COLLABORATION,
                    strength=min(1.0, collab_str),
                    indicators=collab_inds,
                    evidence=self.generate_motive_evidence(original_text, MotiveType.COLLABORATION),
                    path_alignment=path,
                )
            )
        return motives

    def _analyze_problem_solving_motives(self, text_lower: str, original_text: str, path: PathType):
        motives = []

        # Exploration
        expl_inds = []
        expl_str = 0.4
        if "explore" in text_lower or "investigate" in text_lower:
            expl_inds.append("Exploratory approach")
            expl_str += 0.2
        if "analyze" in text_lower or "break" in text_lower:
            expl_inds.append("Analytical exploration")
            expl_str += 0.15

        if expl_inds:
            motives.append(
                MicroMotive(
                    motive_type=MotiveType.EXPLORATION,
                    strength=min(1.0, expl_str),
                    indicators=expl_inds,
                    evidence=self.generate_motive_evidence(original_text, MotiveType.EXPLORATION),
                    path_alignment=path,
                )
            )
        return motives

    def generate_motive_evidence(self, text: str, motive_type: MotiveType) -> List[Evidence]:
        """Generate evidence for a micro-motive."""
        evidence = []
        text_lower = text.lower()

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
