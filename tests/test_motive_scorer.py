"""Dedicated unit tests for the MicroMotiveScorer."""

import pytest

from sono_eval.assessment.models import (
    AssessmentInput,
    Evidence,
    EvidenceType,
    MicroMotive,
    MotiveType,
    PathType,
)
from sono_eval.assessment.scorers.motive import MicroMotiveScorer


@pytest.fixture
def scorer():
    """Create a MicroMotiveScorer instance."""
    return MicroMotiveScorer()


@pytest.fixture
def make_input():
    """Factory fixture to create AssessmentInput with given code."""

    def _make(code: str, **kwargs):
        content = {"code": code}
        content.update(kwargs.pop("extra_content", {}))
        return AssessmentInput(
            candidate_id="test-user",
            submission_type="code",
            content=content,
            **kwargs,
        )

    return _make


# --- Technical Motives ---


class TestTechnicalMotives:
    """Tests for technical path motive identification."""

    def test_mastery_motive_detected(self, scorer, make_input):
        """Test that mastery motive is detected from algorithm/optimize keywords."""
        input_data = make_input(
            "def optimize_algorithm():\n"
            "    # O(n) complexity analysis\n"
            "    # design pattern implementation\n"
            "    pass"
        )
        motives = scorer.identify_micro_motives(PathType.TECHNICAL, input_data)

        mastery = [m for m in motives if m.motive_type == MotiveType.MASTERY]
        assert len(mastery) == 1
        assert mastery[0].strength > 0.5
        assert mastery[0].path_alignment == PathType.TECHNICAL
        assert len(mastery[0].indicators) >= 1

    def test_mastery_strength_increases_with_indicators(self, scorer, make_input):
        """Test that mastery strength increases with more indicators."""
        basic = make_input("def algorithm(): pass")
        detailed = make_input(
            "def algorithm():\n    # optimize with design pattern\n    pass"
        )

        basic_motives = scorer.identify_micro_motives(PathType.TECHNICAL, basic)
        detailed_motives = scorer.identify_micro_motives(PathType.TECHNICAL, detailed)

        basic_mastery = next(
            (m for m in basic_motives if m.motive_type == MotiveType.MASTERY), None
        )
        detailed_mastery = next(
            (m for m in detailed_motives if m.motive_type == MotiveType.MASTERY), None
        )

        assert basic_mastery is not None
        assert detailed_mastery is not None
        assert detailed_mastery.strength > basic_mastery.strength

    def test_quality_motive_detected(self, scorer, make_input):
        """Test that quality motive is detected from test/error keywords."""
        input_data = make_input(
            "def test_something():\n"
            "    # error handling with clean code\n"
            "    # readable implementation\n"
            "    pass"
        )
        motives = scorer.identify_micro_motives(PathType.TECHNICAL, input_data)

        quality = [m for m in motives if m.motive_type == MotiveType.QUALITY]
        assert len(quality) == 1
        assert quality[0].strength > 0.4
        assert len(quality[0].indicators) >= 1

    def test_efficiency_motive_detected(self, scorer, make_input):
        """Test that efficiency motive is detected from optimize/performance keywords."""
        input_data = make_input("def optimize_performance(): pass")
        motives = scorer.identify_micro_motives(PathType.TECHNICAL, input_data)

        efficiency = [m for m in motives if m.motive_type == MotiveType.EFFICIENCY]
        assert len(efficiency) == 1
        assert efficiency[0].strength == 0.6

    def test_no_motives_for_trivial_code(self, scorer, make_input):
        """Test that trivial code produces no motives."""
        input_data = make_input("x = 1")
        motives = scorer.identify_micro_motives(PathType.TECHNICAL, input_data)
        assert len(motives) == 0

    def test_multiple_motives_can_coexist(self, scorer, make_input):
        """Test that multiple motives can be identified simultaneously."""
        input_data = make_input(
            "def optimize_algorithm():\n"
            "    # test the error handling\n"
            "    # clean readable code\n"
            "    # performance optimization\n"
            "    pass"
        )
        motives = scorer.identify_micro_motives(PathType.TECHNICAL, input_data)

        motive_types = {m.motive_type for m in motives}
        assert MotiveType.MASTERY in motive_types
        assert MotiveType.QUALITY in motive_types
        assert MotiveType.EFFICIENCY in motive_types

    def test_mastery_strength_capped_at_one(self, scorer, make_input):
        """Test that mastery strength is capped at 1.0."""
        input_data = make_input(
            "algorithm optimize efficient complexity design pattern"
        )
        motives = scorer.identify_micro_motives(PathType.TECHNICAL, input_data)
        mastery = next(
            (m for m in motives if m.motive_type == MotiveType.MASTERY), None
        )
        assert mastery is not None
        assert mastery.strength <= 1.0


# --- Design Motives ---


class TestDesignMotives:
    """Tests for design path motive identification."""

    def test_innovation_motive_detected(self, scorer, make_input):
        """Test that innovation motive is detected from alternative/creative keywords."""
        input_data = make_input(
            "# alternative approach\n" "# creative novel solution\n" "def solve(): pass"
        )
        motives = scorer.identify_micro_motives(PathType.DESIGN, input_data)

        innovation = [m for m in motives if m.motive_type == MotiveType.INNOVATION]
        assert len(innovation) == 1
        assert innovation[0].strength > 0.4
        assert innovation[0].path_alignment == PathType.DESIGN

    def test_no_innovation_for_basic_code(self, scorer, make_input):
        """Test that basic code yields no innovation motive."""
        input_data = make_input("x = 1 + 2")
        motives = scorer.identify_micro_motives(PathType.DESIGN, input_data)
        assert len(motives) == 0

    def test_innovation_strength_increases_with_keywords(self, scorer, make_input):
        """Test that innovation strength grows with more keywords."""
        basic = make_input("# alternative approach")
        full = make_input("# alternative approach with creative novel ideas")

        basic_motives = scorer.identify_micro_motives(PathType.DESIGN, basic)
        full_motives = scorer.identify_micro_motives(PathType.DESIGN, full)

        basic_innov = next(
            (m for m in basic_motives if m.motive_type == MotiveType.INNOVATION), None
        )
        full_innov = next(
            (m for m in full_motives if m.motive_type == MotiveType.INNOVATION), None
        )

        assert basic_innov is not None
        assert full_innov is not None
        assert full_innov.strength > basic_innov.strength


# --- Collaboration Motives ---


class TestCollaborationMotives:
    """Tests for collaboration path motive identification."""

    def test_collaboration_motive_detected(self, scorer, make_input):
        """Test that collaboration motive is detected from team/document keywords."""
        input_data = make_input(
            "# Document the team collaboration strategy\n" "def collaborate(): pass"
        )
        motives = scorer.identify_micro_motives(PathType.COLLABORATION, input_data)

        collab = [m for m in motives if m.motive_type == MotiveType.COLLABORATION]
        assert len(collab) == 1
        assert collab[0].path_alignment == PathType.COLLABORATION
        assert len(collab[0].indicators) >= 1

    def test_no_collaboration_for_unrelated_code(self, scorer, make_input):
        """Test that unrelated code yields no collaboration motive."""
        input_data = make_input("x = 42")
        motives = scorer.identify_micro_motives(PathType.COLLABORATION, input_data)
        assert len(motives) == 0


# --- Problem Solving Motives ---


class TestProblemSolvingMotives:
    """Tests for problem solving path motive identification."""

    def test_exploration_motive_detected(self, scorer, make_input):
        """Test that exploration motive is detected from explore/investigate keywords."""
        input_data = make_input(
            "# Explore and investigate the problem\n"
            "# Analyze and break down the requirements\n"
            "def solve(): pass"
        )
        motives = scorer.identify_micro_motives(PathType.PROBLEM_SOLVING, input_data)

        exploration = [m for m in motives if m.motive_type == MotiveType.EXPLORATION]
        assert len(exploration) == 1
        assert exploration[0].path_alignment == PathType.PROBLEM_SOLVING

    def test_no_exploration_for_simple_code(self, scorer, make_input):
        """Test that simple code yields no exploration motive."""
        input_data = make_input("result = 1 + 2")
        motives = scorer.identify_micro_motives(PathType.PROBLEM_SOLVING, input_data)
        assert len(motives) == 0


# --- Evidence Generation ---


class TestMotiveEvidence:
    """Tests for motive evidence generation."""

    def test_mastery_evidence_generated(self, scorer):
        """Test that mastery motive generates evidence."""
        evidence = scorer.generate_motive_evidence(
            "algorithm and optimize the solution", MotiveType.MASTERY
        )
        assert len(evidence) > 0
        assert evidence[0].type == EvidenceType.CODE_QUALITY
        assert "depth" in evidence[0].description.lower()

    def test_quality_evidence_generated(self, scorer):
        """Test that quality motive generates evidence."""
        evidence = scorer.generate_motive_evidence(
            "test the error handling", MotiveType.QUALITY
        )
        assert len(evidence) > 0
        assert evidence[0].type == EvidenceType.TESTING

    def test_no_evidence_without_keywords(self, scorer):
        """Test that no evidence is generated without matching keywords."""
        evidence = scorer.generate_motive_evidence("x = 1", MotiveType.MASTERY)
        assert len(evidence) == 0

    def test_evidence_for_unknown_motive_type(self, scorer):
        """Test that unhandled motive types return empty evidence."""
        evidence = scorer.generate_motive_evidence("some code", MotiveType.INNOVATION)
        assert len(evidence) == 0


# --- MicroMotive Model Validation ---


class TestMicroMotiveModel:
    """Tests for MicroMotive model constraints."""

    def test_motive_fields(self, scorer, make_input):
        """Test that returned motives have all required fields."""
        input_data = make_input("def optimize_algorithm(): pass")
        motives = scorer.identify_micro_motives(PathType.TECHNICAL, input_data)

        for motive in motives:
            assert isinstance(motive, MicroMotive)
            assert isinstance(motive.motive_type, MotiveType)
            assert 0.0 <= motive.strength <= 1.0
            assert isinstance(motive.indicators, list)
            assert isinstance(motive.evidence, list)
            assert isinstance(motive.path_alignment, PathType)

    def test_all_paths_produce_valid_motives(self, scorer, make_input):
        """Test that all path types produce valid motive structures."""
        rich_code = (
            "def optimize_algorithm():\n"
            "    # alternative creative approach\n"
            "    # document team collaboration\n"
            "    # explore and analyze the pattern\n"
            "    # test error handling\n"
            "    pass"
        )
        input_data = make_input(rich_code)

        for path in PathType:
            motives = scorer.identify_micro_motives(path, input_data)
            for motive in motives:
                assert 0.0 <= motive.strength <= 1.0
                assert motive.path_alignment == path
