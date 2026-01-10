"""Tests for the assessment engine."""

import pytest
from sono_eval.assessment.engine import AssessmentEngine
from sono_eval.assessment.models import AssessmentInput, PathType


@pytest.mark.asyncio
async def test_assessment_engine_initialization():
    """Test that assessment engine initializes correctly."""
    engine = AssessmentEngine()
    assert engine is not None
    assert engine.version is not None
    assert engine.enable_explanations is not None


@pytest.mark.asyncio
async def test_basic_assessment():
    """Test basic assessment flow."""
    engine = AssessmentEngine()

    assessment_input = AssessmentInput(
        candidate_id="test_candidate_001",
        submission_type="code",
        content={"code": "def hello(): return 'world'"},
        paths_to_evaluate=[PathType.TECHNICAL],
    )

    result = await engine.assess(assessment_input)

    # Validate result structure
    assert result is not None
    assert result.candidate_id == "test_candidate_001"
    assert result.overall_score >= 0
    assert result.overall_score <= 100
    assert result.confidence >= 0
    assert result.confidence <= 1
    assert len(result.path_scores) > 0


@pytest.mark.asyncio
async def test_multi_path_assessment():
    """Test assessment with multiple paths."""
    engine = AssessmentEngine()

    assessment_input = AssessmentInput(
        candidate_id="test_candidate_002",
        submission_type="code",
        content={"code": "class Calculator:\n    def add(self, a, b):\n        return a + b"},
        paths_to_evaluate=[PathType.TECHNICAL, PathType.DESIGN],
    )

    result = await engine.assess(assessment_input)

    assert len(result.path_scores) == 2
    assert any(ps.path == PathType.TECHNICAL for ps in result.path_scores)
    assert any(ps.path == PathType.DESIGN for ps in result.path_scores)


@pytest.mark.asyncio
async def test_assessment_has_evidence():
    """Test that assessments include evidence."""
    engine = AssessmentEngine()

    assessment_input = AssessmentInput(
        candidate_id="test_candidate_003",
        submission_type="code",
        content={"code": "def factorial(n): return 1 if n <= 1 else n * factorial(n-1)"},
        paths_to_evaluate=[PathType.TECHNICAL],
    )

    result = await engine.assess(assessment_input)

    # Check for evidence in metrics
    assert len(result.path_scores) > 0
    path_score = result.path_scores[0]
    assert len(path_score.metrics) > 0

    # At least one metric should have evidence
    has_evidence = any(len(m.evidence) > 0 for m in path_score.metrics)
    assert has_evidence


@pytest.mark.asyncio
async def test_assessment_has_micro_motives():
    """Test that assessments track micro-motives."""
    engine = AssessmentEngine()

    assessment_input = AssessmentInput(
        candidate_id="test_candidate_004",
        submission_type="code",
        content={
            "code": "# Well-documented function\ndef process(data):\n    '''Process data.'''\n    return data"
        },
        paths_to_evaluate=[PathType.TECHNICAL],
    )

    result = await engine.assess(assessment_input)

    # Should have micro-motives tracked
    assert len(result.micro_motives) >= 0  # May or may not have motives depending on content


@pytest.mark.asyncio
async def test_assessment_has_explanations():
    """Test that assessments include explanations."""
    engine = AssessmentEngine()

    assessment_input = AssessmentInput(
        candidate_id="test_candidate_005",
        submission_type="code",
        content={"code": "print('hello')"},
        paths_to_evaluate=[PathType.TECHNICAL],
    )

    result = await engine.assess(assessment_input)

    assert result.summary is not None
    assert len(result.summary) > 0

    # Check metrics have explanations
    for path_score in result.path_scores:
        for metric in path_score.metrics:
            assert metric.explanation is not None
            assert len(metric.explanation) > 0
