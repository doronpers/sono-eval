"""Tests for real ML scorer implementation using AST analysis."""

from sono_eval.assessment.scorers.ml import MLScorer
from sono_eval.assessment.scorers.ml_utils import CodeComplexityAnalyzer, NamingConventionValidator

SAMPLE_CODE_GOOD = """
def calculate_sum(a, b):
    \"\"\"Calculate sum of two numbers.\"\"\"
    return a + b

class DataProcessor:
    \"\"\"Process data items.\"\"\"
    def process(self, data):
        return [d * 2 for d in data]
"""

SAMPLE_CODE_COMPLEX = """
def complex_function(x):
    if x > 0:
        if x > 10:
            if x > 20:
                for i in range(x):
                    try:
                        while True:
                            break
                    except:
                        pass
    return x
"""


def test_complexity_analysis():
    """Test AST complexity analyzer."""
    metrics = CodeComplexityAnalyzer.analyze(SAMPLE_CODE_GOOD)
    # 2 functions + 1 class, simple complexity
    assert metrics["cyclomatic_complexity"] < 5
    assert metrics["class_count"] == 1

    metrics_complex = CodeComplexityAnalyzer.analyze(SAMPLE_CODE_COMPLEX)
    # High nesting and complexity
    assert metrics_complex["nesting_depth"] >= 5
    assert metrics_complex["cyclomatic_complexity"] > 5


def test_naming_conventions():
    """Test naming convention validator."""
    metrics = NamingConventionValidator.analyze(SAMPLE_CODE_GOOD)
    # Should be mostly consistent
    assert metrics["consistency"] > 0.7
    assert metrics["snake_case_ratio"] > 0


def test_ml_scorer_insights():
    """Test ML scorer generates insights."""
    scorer = MLScorer()

    # Test loading
    assert scorer.load_model_if_available() is True

    # Test scoring good code
    insights = scorer.get_insights(SAMPLE_CODE_GOOD, "test.py")
    assert insights is not None
    assert insights["score"] > 70
    assert "pattern" in insights
    assert insights["pattern"] in ["clean_well_structured_code", "moderate_complexity_code"]

    # Test scoring complex code
    insights_bad = scorer.get_insights(SAMPLE_CODE_COMPLEX, "complex.py")
    assert insights_bad is not None
    # Complexity penalizes score
    assert insights_bad["score"] < insights["score"]
    assert insights_bad["pattern"] == "high_complexity_code"
