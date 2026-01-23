"""Tests for ML model loader and integration."""

import pytest

from sono_eval.assessment.scorers.model_loader import ModelLoader, get_model_loader


class TestModelLoader:
    """Tests for ModelLoader class."""

    def test_singleton_pattern(self):
        """Test that ModelLoader uses singleton pattern."""
        loader1 = get_model_loader()
        loader2 = get_model_loader()
        assert loader1 is loader2

    def test_model_loader_initialization(self):
        """Test model loader initializes correctly."""
        loader = ModelLoader()
        assert loader.is_available is False  # Not loaded yet
        assert loader.model_version == "unknown"

    def test_model_loader_fallback(self):
        """Test graceful fallback when model unavailable."""
        loader = ModelLoader()
        # This should not raise even if transformers not installed
        result = loader.load()
        # Result depends on environment - either True (model loaded) or False (fallback)
        assert isinstance(result, bool)

    def test_get_code_quality_score_without_loading(self):
        """Test that scoring returns None when model not loaded."""
        loader = ModelLoader()
        # Don't call load() first
        result = loader.get_code_quality_score("def hello(): pass")
        # Should return None since model not available
        if not loader.is_available:
            assert result is None


class TestMLScorerIntegration:
    """Tests for MLScorer with trained model integration."""

    def test_ml_scorer_loads_successfully(self):
        """Test MLScorer load_model_if_available returns True."""
        from sono_eval.assessment.scorers.ml import MLScorer

        scorer = MLScorer()
        result = scorer.load_model_if_available()
        # Should always return True (either model or AST fallback)
        assert result is True

    def test_ml_scorer_model_version_property(self):
        """Test model_version property returns valid string."""
        from sono_eval.assessment.scorers.ml import MLScorer

        scorer = MLScorer()
        scorer.load_model_if_available()
        version = scorer.model_version
        assert isinstance(version, str)
        assert len(version) > 0

    def test_ml_scorer_insights_include_analysis_mode(self):
        """Test that get_insights includes analysis_mode."""
        from sono_eval.assessment.models import PathType
        from sono_eval.assessment.scorers.ml import MLScorer

        scorer = MLScorer()
        scorer.load_model_if_available()

        code = """
def calculate_sum(a, b):
    \"\"\"Calculate sum of two numbers.\"\"\"
    return a + b
"""
        insights = scorer.get_insights({"code": code}, PathType.TECHNICAL)
        assert insights is not None
        assert "analysis_mode" in insights
        assert insights["analysis_mode"] in ["hybrid_ml", "ast_only"]
        assert "model_version" in insights

    def test_ml_scorer_hybrid_combination(self):
        """Test that ML scorer properly combines AST and model scores."""
        from sono_eval.assessment.models import PathType
        from sono_eval.assessment.scorers.ml import MLScorer

        scorer = MLScorer()
        scorer.load_model_if_available()

        # Good code should score well
        good_code = """
class DataProcessor:
    \"\"\"Process data items with proper structure.\"\"\"

    def process(self, items):
        \"\"\"Process each item efficiently.\"\"\"
        return [self._transform(item) for item in items]

    def _transform(self, item):
        \"\"\"Transform a single item.\"\"\"
        return item * 2
"""
        insights = scorer.get_insights({"code": good_code}, PathType.TECHNICAL)
        assert insights is not None
        assert insights["score"] > 60  # Should score reasonably well


class TestAssessmentEngineMLIntegration:
    """Tests for AssessmentEngine with ML scorer integration."""

    @pytest.mark.asyncio
    async def test_engine_metadata_includes_ml_info(self):
        """Test that assessment metadata includes ML model information."""
        from sono_eval.assessment.engine import AssessmentEngine
        from sono_eval.assessment.models import AssessmentInput, PathType

        engine = AssessmentEngine()
        assessment_input = AssessmentInput(
            candidate_id="test_ml_integration",
            submission_type="code",
            content={"code": "def hello(): return 'world'"},
            paths_to_evaluate=[PathType.TECHNICAL],
        )

        result = await engine.assess(assessment_input)

        # Check ML metadata is present
        assert "ml_model_available" in result.metadata
        assert "ml_model_version" in result.metadata
        assert isinstance(result.metadata["ml_model_available"], bool)
        assert isinstance(result.metadata["ml_model_version"], str)

    @pytest.mark.asyncio
    async def test_engine_uses_correct_assessment_mode(self):
        """Test that assessment mode reflects available scorers."""
        from sono_eval.assessment.engine import AssessmentEngine
        from sono_eval.assessment.models import AssessmentInput, PathType

        engine = AssessmentEngine()
        assessment_input = AssessmentInput(
            candidate_id="test_mode",
            submission_type="code",
            content={"code": "print('test')"},
            paths_to_evaluate=[PathType.TECHNICAL],
        )

        result = await engine.assess(assessment_input)

        # Mode should be set based on available scorers
        mode = result.metadata["assessment_mode"]
        assert mode in ["heuristic", "hybrid_ml", "hybrid_council", "hybrid_ml_council"]
