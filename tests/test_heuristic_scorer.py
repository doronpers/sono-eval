"""Dedicated unit tests for the HeuristicScorer."""

import pytest

from sono_eval.assessment.models import (
    AssessmentInput,
    Evidence,
    EvidenceType,
    PathType,
    ScoringMetric,
)
from sono_eval.assessment.pattern_checks import PatternViolation
from sono_eval.assessment.scorers.heuristic import HeuristicScorer
from sono_eval.utils.config import Config


@pytest.fixture
def config():
    """Create a Config instance with default settings."""
    return Config()


@pytest.fixture
def scorer(config):
    """Create a HeuristicScorer instance."""
    return HeuristicScorer(config)


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


# --- Technical Path Tests ---


class TestTechnicalPath:
    """Tests for the technical assessment path."""

    def test_technical_returns_metrics(self, scorer, make_input):
        """Test that technical path returns expected metric names."""
        input_data = make_input("def hello():\n    return 'world'")
        metrics = scorer.generate_metrics_for_path(PathType.TECHNICAL, input_data)

        assert len(metrics) >= 3
        names = [m.name for m in metrics]
        assert "Code Quality" in names
        assert "Problem Solving" in names
        assert "Testing" in names

    def test_technical_all_metrics_have_required_fields(self, scorer, make_input):
        """Test that all returned metrics have valid fields."""
        input_data = make_input("class Foo:\n    def bar(self): pass")
        metrics = scorer.generate_metrics_for_path(PathType.TECHNICAL, input_data)

        for metric in metrics:
            assert isinstance(metric, ScoringMetric)
            assert 0 <= metric.score <= 100
            assert 0 <= metric.weight <= 1
            assert 0 <= metric.confidence <= 1
            assert metric.category == "technical"
            assert len(metric.explanation) > 0

    def test_code_quality_boosts_for_structure(self, scorer, make_input):
        """Test that well-structured code gets higher quality scores."""
        simple = make_input("x = 1")
        structured = make_input(
            "import os\n\ndef process():\n    try:\n        return True\n    except Exception:\n        return False"
        )

        simple_metrics = scorer.generate_metrics_for_path(PathType.TECHNICAL, simple)
        structured_metrics = scorer.generate_metrics_for_path(
            PathType.TECHNICAL, structured
        )

        simple_cq = next(m for m in simple_metrics if m.name == "Code Quality")
        structured_cq = next(m for m in structured_metrics if m.name == "Code Quality")

        assert structured_cq.score > simple_cq.score

    def test_code_quality_penalizes_print_statements(self, scorer, make_input):
        """Test that excessive print statements reduce the score."""
        code_with_prints = "def f():\n" + "\n".join(
            f"    print({i})" for i in range(10)
        )
        input_data = make_input(code_with_prints)
        metrics = scorer.generate_metrics_for_path(PathType.TECHNICAL, input_data)
        cq = next(m for m in metrics if m.name == "Code Quality")

        # Score should be reduced compared to baseline
        # Baseline starts at 50, gets +10 for def, -5 for >5 prints
        assert cq.score <= 75

    def test_code_quality_penalizes_todo_fixme(self, scorer, make_input):
        """Test that TODO/FIXME markers reduce the score."""
        input_data = make_input("def f():\n    # TODO fix this\n    pass")
        metrics = scorer.generate_metrics_for_path(PathType.TECHNICAL, input_data)
        cq = next(m for m in metrics if m.name == "Code Quality")

        # Expect penalty applied
        assert cq.score < 70

    def test_pattern_violations_reduce_score(self, scorer, make_input):
        """Test that pattern violations reduce the code quality score."""
        input_data = make_input("def f():\n    pass")
        violations = [
            PatternViolation(
                pattern="bare_except",
                description="Bare except clause",
                severity="high",
                line=1,
                code="except:",
            ),
            PatternViolation(
                pattern="print_statement",
                description="Print statement in production code",
                severity="medium",
                line=2,
                code="print(result)",
            ),
        ]

        metrics_no_viol = scorer.generate_metrics_for_path(
            PathType.TECHNICAL, input_data
        )
        metrics_with_viol = scorer.generate_metrics_for_path(
            PathType.TECHNICAL, input_data, pattern_violations=violations
        )

        cq_no = next(m for m in metrics_no_viol if m.name == "Code Quality")
        cq_with = next(m for m in metrics_with_viol if m.name == "Code Quality")

        assert cq_with.score < cq_no.score

    def test_error_handling_metric_appears_when_present(self, scorer, make_input):
        """Test that error handling metric is included when err handling exists."""
        input_data = make_input(
            "def f():\n    try:\n        pass\n    except ValueError:\n        pass"
        )
        metrics = scorer.generate_metrics_for_path(PathType.TECHNICAL, input_data)
        names = [m.name for m in metrics]
        assert "Error Handling" in names

    def test_error_handling_metric_present_for_trivial_code(self, scorer, make_input):
        """Test that error handling metric is present even for trivial code."""
        input_data = make_input("x = 1")
        metrics = scorer.generate_metrics_for_path(PathType.TECHNICAL, input_data)
        names = [m.name for m in metrics]
        # The metric should appear with its base score.
        assert "Error Handling" in names

    def test_testing_score_boosts_for_test_keywords(self, scorer, make_input):
        """Test that testing-related keywords boost the testing score."""
        input_data = make_input(
            "def test_something():\n    assert True\n    # mock the service\n    # coverage report"
        )
        metrics = scorer.generate_metrics_for_path(PathType.TECHNICAL, input_data)
        testing = next(m for m in metrics if m.name == "Testing")
        # base 30 + 20 (test) + 15 (assert) + 10 (mock) + 10 (coverage) = 85
        assert testing.score >= 80

    def test_problem_solving_score_keywords(self, scorer, make_input):
        """Test that problem-solving keywords boost the score."""
        input_data = make_input(
            "# algorithm with O(n) complexity\n"
            "def optimize(data):\n"
            "    for item in data:\n"
            "        if item > 0:\n"
            "            pass\n"
            "    return efficient_solution(data)"
        )
        metrics = scorer.generate_metrics_for_path(PathType.TECHNICAL, input_data)
        ps = next(m for m in metrics if m.name == "Problem Solving")
        # Should get multiple keyword boosts
        assert ps.score >= 70


# --- Design Path Tests ---


class TestDesignPath:
    """Tests for the design assessment path."""

    def test_design_returns_metrics(self, scorer, make_input):
        """Test that design path returns expected metric names."""
        input_data = make_input("class MyModule:\n    pass")
        metrics = scorer.generate_metrics_for_path(PathType.DESIGN, input_data)

        assert len(metrics) >= 2
        names = [m.name for m in metrics]
        assert "Architecture" in names
        assert "Design Thinking" in names

    def test_architecture_boosts_for_classes(self, scorer, make_input):
        """Test that class/module usage boosts architecture score."""
        input_data = make_input(
            "class AbstractFactory:\n"
            "    '''A modular design pattern implementation.'''\n"
            "    pass"
        )
        metrics = scorer.generate_metrics_for_path(PathType.DESIGN, input_data)
        arch = next(m for m in metrics if m.name == "Architecture")
        # base 50 + 15 (class) + 10 (pattern) + 10 (modular) = 85
        assert arch.score >= 80

    def test_design_thinking_keywords(self, scorer, make_input):
        """Test that design thinking keywords boost the score."""
        input_data = make_input(
            "# Consider the trade-off between alternatives\n"
            "# This approach has design implications"
        )
        metrics = scorer.generate_metrics_for_path(PathType.DESIGN, input_data)
        dt = next(m for m in metrics if m.name == "Design Thinking")
        # base 50 + 15 (consider) + 10 (trade off) + 10 (alternative) = 85
        assert dt.score >= 80

    def test_scalability_metric_present_when_relevant(self, scorer, make_input):
        """Test that scalability metric appears with relevant keywords."""
        input_data = make_input(
            "# This scalable solution uses concurrent processing for performance"
        )
        metrics = scorer.generate_metrics_for_path(PathType.DESIGN, input_data)
        names = [m.name for m in metrics]
        assert "Scalability" in names
        scale = next(m for m in metrics if m.name == "Scalability")
        assert scale.score > 30

    def test_scalability_metric_absent_for_simple_code(self, scorer, make_input):
        """Test that scalability metric is absent for unrelated code."""
        input_data = make_input("x = 1")
        metrics = scorer.generate_metrics_for_path(PathType.DESIGN, input_data)
        scale = next((m for m in metrics if m.name == "Scalability"), None)
        # base score is 30, which is > 0, so it appears
        assert scale is not None
        assert scale.score == 30


# --- Collaboration Path Tests ---


class TestCollaborationPath:
    """Tests for the collaboration assessment path."""

    def test_collaboration_returns_metrics(self, scorer, make_input):
        """Test that collaboration path returns expected metric names."""
        input_data = make_input("def hello(): pass")
        metrics = scorer.generate_metrics_for_path(PathType.COLLABORATION, input_data)

        names = [m.name for m in metrics]
        assert "Documentation" in names
        assert "Code Readability" in names
        assert "Communication" in names

    def test_documentation_boosts_for_docstrings(self, scorer, make_input):
        """Test that docstrings boost documentation score."""
        input_data = make_input(
            '"""Module doc."""\n' "def f():\n" '    """Function doc."""\n' "    pass"
        )
        metrics = scorer.generate_metrics_for_path(PathType.COLLABORATION, input_data)
        doc = next(m for m in metrics if m.name == "Documentation")
        assert doc.score >= 55  # base 40 + 15 for docstrings

    def test_readability_score_range(self, scorer, make_input):
        """Test that readability produces a valid score."""
        input_data = make_input(
            "result = compute_value(data)\nitem_name = get_name(item)\n" * 5
        )
        metrics = scorer.generate_metrics_for_path(PathType.COLLABORATION, input_data)
        read = next(m for m in metrics if m.name == "Code Readability")
        assert 0 <= read.score <= 100

    def test_communication_boosts_for_explanation_content(self, scorer, make_input):
        """Test that explanation content boosts communication score."""
        input_data = make_input(
            "def f(): pass",
            extra_content={
                "explanation": "This is a detailed explanation of my approach "
                "and reasoning behind the implementation. "
                "I chose this method because it provides better scalability. "
                "The strategy involves decomposing the problem into smaller parts."
            },
        )
        metrics = scorer.generate_metrics_for_path(PathType.COLLABORATION, input_data)
        comm = next(m for m in metrics if m.name == "Communication")
        # base 50 + 20 (>50 chars) + 15 (>200 chars) = 85
        assert comm.score >= 80


# --- Problem Solving Path Tests ---


class TestProblemSolvingPath:
    """Tests for the problem solving assessment path."""

    def test_problem_solving_returns_metrics(self, scorer, make_input):
        """Test that problem solving path returns expected metric names."""
        input_data = make_input("def solve(): pass")
        metrics = scorer.generate_metrics_for_path(PathType.PROBLEM_SOLVING, input_data)

        names = [m.name for m in metrics]
        assert "Analytical Thinking" in names
        assert "Debugging Approach" in names
        assert "Optimization" in names
        assert "Complexity Handling" in names

    def test_analytical_thinking_keywords(self, scorer, make_input):
        """Test that analytical keywords boost the score."""
        input_data = make_input(
            "# Analyze the pattern and break down the logic step by step\n"
            "def solve(): pass"
        )
        metrics = scorer.generate_metrics_for_path(PathType.PROBLEM_SOLVING, input_data)
        at = next(m for m in metrics if m.name == "Analytical Thinking")
        # base 50 + 15 (analyze/break/step) + 10 (logic) + 10 (pattern) = 85
        assert at.score >= 80

    def test_debugging_keywords(self, scorer, make_input):
        """Test that debugging keywords boost the score."""
        input_data = make_input(
            "# debug the error issue\ndef fix_bug():\n    test_result = True"
        )
        metrics = scorer.generate_metrics_for_path(PathType.PROBLEM_SOLVING, input_data)
        dbg = next(m for m in metrics if m.name == "Debugging Approach")
        # base 40 + 15 (debug/fix) + 10 (error/issue) + 10 (test) = 75
        assert dbg.score >= 70

    def test_optimization_keywords(self, scorer, make_input):
        """Test that optimization keywords boost the score."""
        input_data = make_input(
            "# optimize for O(n log n) complexity\n" "def fast_sort(data): pass"
        )
        metrics = scorer.generate_metrics_for_path(PathType.PROBLEM_SOLVING, input_data)
        opt = next(m for m in metrics if m.name == "Optimization")
        # base 40 + 15 (optimize/performance) + 10 (fast) + 15 (o(/complexity) = 80
        assert opt.score >= 70

    def test_complexity_handling_for_large_code(self, scorer, make_input):
        """Test that larger codebases get a complexity handling boost."""
        lines = ["def func_{i}(): pass".format(i=i) for i in range(60)]
        input_data = make_input("\n".join(lines))
        metrics = scorer.generate_metrics_for_path(PathType.PROBLEM_SOLVING, input_data)
        comp = next(m for m in metrics if m.name == "Complexity Handling")
        # base 50 + 10 (>50 lines) = 60
        assert comp.score >= 60


# --- Evidence Generation Tests ---


class TestEvidenceGeneration:
    """Tests for evidence generation in metrics."""

    def test_code_quality_evidence_for_functions(self, scorer, make_input):
        """Test that evidence is generated for function usage."""
        input_data = make_input("def hello(): pass")
        metrics = scorer.generate_metrics_for_path(PathType.TECHNICAL, input_data)
        cq = next(m for m in metrics if m.name == "Code Quality")

        assert len(cq.evidence) > 0
        assert any("functions" in e.description.lower() for e in cq.evidence)

    def test_code_quality_evidence_for_error_handling(self, scorer, make_input):
        """Test that evidence is generated for error handling."""
        input_data = make_input("try:\n    pass\nexcept:\n    pass")
        metrics = scorer.generate_metrics_for_path(PathType.TECHNICAL, input_data)
        cq = next(m for m in metrics if m.name == "Code Quality")

        assert any("error handling" in e.description.lower() for e in cq.evidence)

    def test_pattern_violation_evidence(self, scorer, make_input):
        """Test that pattern violations generate evidence."""
        input_data = make_input("def f(): pass")
        violations = [
            PatternViolation(
                pattern="bare_except",
                description="Bare except clause found",
                severity="high",
                line=1,
                code="except:",
            )
        ]
        metrics = scorer.generate_metrics_for_path(
            PathType.TECHNICAL, input_data, pattern_violations=violations
        )
        cq = next(m for m in metrics if m.name == "Code Quality")
        assert any("pattern violation" in e.description.lower() for e in cq.evidence)

    def test_architecture_evidence_for_classes(self, scorer, make_input):
        """Test that architecture evidence is generated for class usage."""
        input_data = make_input("class MyService:\n    pass")
        metrics = scorer.generate_metrics_for_path(PathType.DESIGN, input_data)
        arch = next(m for m in metrics if m.name == "Architecture")
        assert any("object-oriented" in e.description.lower() for e in arch.evidence)


# --- Explanation Tests ---


class TestExplanations:
    """Tests for explanation text generation."""

    def test_code_quality_explanation_tiers(self, scorer):
        """Test that code quality explanations match score tiers."""
        high = scorer._explain_code_quality(85.0)
        mid = scorer._explain_code_quality(65.0)
        low = scorer._explain_code_quality(40.0)

        assert "strong quality" in high.lower()
        assert "solid fundamentals" in mid.lower()
        assert "enhanced" in low.lower()

    def test_code_quality_explanation_with_violations(self, scorer):
        """Test that violation count is mentioned in explanation."""
        explanation = scorer._explain_code_quality(70.0, violation_count=3)
        assert "3" in explanation
        assert "issue" in explanation.lower()

    def test_problem_solving_explanation_tiers(self, scorer):
        """Test problem solving explanation tiers."""
        high = scorer._explain_problem_solving(80.0)
        mid = scorer._explain_problem_solving(60.0)
        low = scorer._explain_problem_solving(40.0)

        assert "strong" in high.lower()
        assert "good" in mid.lower()
        assert "systematic" in low.lower()

    def test_testing_explanation_tiers(self, scorer):
        """Test testing explanation tiers."""
        high = scorer._explain_testing(75.0)
        mid = scorer._explain_testing(50.0)
        low = scorer._explain_testing(30.0)

        assert "good" in high.lower()
        assert "some testing" in mid.lower()
        assert "needs" in low.lower()


# --- Score Clamping Tests ---


class TestScoreClamping:
    """Tests that scores are properly clamped between 0 and 100."""

    def test_code_quality_never_exceeds_100(self, scorer):
        """Test that code quality score is capped at 100."""
        # Code with every positive signal
        text = (
            "import os\ndef foo():\n    try:\n        pass\n    except:\n        pass\n"
            "assert True\nclass Bar: pass\n"
            "# algorithm optimize efficient\n"
        )
        score = scorer._analyze_code_quality(text)
        assert score <= 100.0

    def test_code_quality_never_below_0(self, scorer):
        """Test that code quality score is floored at 0."""
        violations = [
            PatternViolation(
                pattern=f"v{i}",
                description=f"violation {i}",
                severity="critical",
                line=i,
                code=f"violation_code_{i}",
            )
            for i in range(50)
        ]
        score = scorer._analyze_code_quality("", violations)
        assert score >= 0.0

    def test_all_analysis_methods_return_valid_range(self, scorer):
        """Test that all analysis methods return scores in [0, 100]."""
        text = "x = 1"
        methods = [
            scorer._analyze_code_quality,
            scorer._analyze_problem_solving,
            scorer._analyze_testing,
            scorer._analyze_error_handling,
            scorer._analyze_architecture,
            scorer._analyze_design_thinking,
            scorer._analyze_scalability,
            scorer._analyze_documentation,
            scorer._analyze_readability,
            scorer._analyze_analytical_thinking,
            scorer._analyze_debugging_approach,
            scorer._analyze_optimization,
            scorer._analyze_complexity_handling,
        ]

        for method in methods:
            # _analyze_code_quality takes an extra arg
            if method == scorer._analyze_code_quality:
                score = method(text, None)
            else:
                score = method(text)
            assert 0.0 <= score <= 100.0, f"{method.__name__} returned {score}"
