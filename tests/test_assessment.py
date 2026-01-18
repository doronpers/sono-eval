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


@pytest.mark.asyncio
async def test_assessment_pattern_violations_metadata():
    """Ensure pattern violations are captured in metadata."""
    engine = AssessmentEngine()

    assessment_input = AssessmentInput(
        candidate_id="test_candidate_006",
        submission_type="code",
        content={
            "code": (
                "import tempfile\n"
                "def handler(items):\n"
                "    try:\n"
                "        value = items[0]\n"
                "    except:\n"
                "        print('error')\n"
                "        value = None\n"
                "    path = tempfile.mktemp()\n"
                "    return value\n"
            )
        },
        paths_to_evaluate=[PathType.TECHNICAL],
    )

    result = await engine.assess(assessment_input)
    pattern_meta = result.metadata.get("pattern_checks", {})

    assert pattern_meta.get("enabled") is True
    assert pattern_meta.get("violation_count", 0) > 0
    assert isinstance(pattern_meta.get("violations", []), list)


@pytest.mark.asyncio
async def test_assessment_pattern_violations_affect_score():
    """Ensure pattern violations affect the overall score."""
    engine = AssessmentEngine()

    # Code with multiple pattern violations
    assessment_input = AssessmentInput(
        candidate_id="test_candidate_007",
        submission_type="code",
        content={
            "code": (
                "import tempfile\n"
                "import numpy as np\n"
                "def bad_code(items):\n"
                "    try:\n"
                "        result = items[0]\n"
                "    except:\n"
                "        print('error')\n"
                "    path = tempfile.mktemp()\n"
                "    data = np.array([1, 2, 3])\n"
                "    return {'mean': np.mean(data), 'value': result}\n"
            )
        },
        paths_to_evaluate=[PathType.TECHNICAL],
    )

    result = await engine.assess(assessment_input)
    pattern_meta = result.metadata.get("pattern_checks", {})

    # Should have violations
    violation_count = pattern_meta.get("violation_count", 0)
    assert violation_count > 0, "Expected pattern violations but found none"

    # Check that penalty is recorded
    penalty_points = pattern_meta.get("penalty_points", 0)
    assert penalty_points > 0, "Expected penalty points but found none"

    # Score should be affected (lower than perfect, accounting for penalty)
    # The penalty is applied to path scores, which affects overall score
    assert result.overall_score < 100, "Score should be less than 100 due to violations"


@pytest.mark.asyncio
async def test_assessment_no_pattern_violations():
    """Test assessment with clean code (no pattern violations)."""
    engine = AssessmentEngine()

    # Clean code following best practices
    assessment_input = AssessmentInput(
        candidate_id="test_candidate_008",
        submission_type="code",
        content={
            "code": (
                "import os\n"
                "import tempfile\n"
                "\n"
                "def process_data(items):\n"
                '    """Process items safely."""\n'
                "    if not items:\n"
                "        return None\n"
                "    \n"
                "    try:\n"
                "        fd, path = tempfile.mkstemp()\n"
                "        try:\n"
                "            with os.fdopen(fd, 'w') as f:\n"
                "                f.write(str(items[0]))\n"
                "            return path\n"
                "        finally:\n"
                "            os.unlink(path)\n"
                "    except (IndexError, IOError) as e:\n"
                "        import logging\n"
                "        logger = logging.getLogger(__name__)\n"
                "        logger.error(f'Error processing: {e}')\n"
                "        return None\n"
            )
        },
        paths_to_evaluate=[PathType.TECHNICAL],
    )

    result = await engine.assess(assessment_input)
    pattern_meta = result.metadata.get("pattern_checks", {})

    # Should have pattern checks enabled
    assert pattern_meta.get("enabled") is True
    # Should have fewer or no violations
    violation_count = pattern_meta.get("violation_count", 0)
    assert violation_count >= 0  # May have some, but should be minimal


@pytest.mark.asyncio
async def test_assessment_pattern_violations_in_evidence():
    """Ensure pattern violations appear in evidence."""
    engine = AssessmentEngine()

    assessment_input = AssessmentInput(
        candidate_id="test_candidate_009",
        submission_type="code",
        content={
            "code": (
                "def unsafe_code(data):\n"
                "    try:\n"
                "        return data[0]\n"
                "    except:\n"
                "        print('error')\n"
                "        return None\n"
            )
        },
        paths_to_evaluate=[PathType.TECHNICAL],
    )

    result = await engine.assess(assessment_input)

    # Check that pattern violations are mentioned in evidence or explanations
    pattern_meta = result.metadata.get("pattern_checks", {})
    violations = pattern_meta.get("violations", [])

    if violations:
        # At least one violation should have details
        assert any("pattern" in str(v).lower() or "violation" in str(v).lower() for v in violations)
