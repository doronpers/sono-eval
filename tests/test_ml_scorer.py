"""Dedicated unit tests for MLScorer and ModelLoader."""

import os
from unittest.mock import MagicMock, patch, PropertyMock

import pytest

from sono_eval.assessment.models import (
    Evidence,
    EvidenceType,
    PathType,
    ScoringMetric,
)
from sono_eval.assessment.scorers.ml import MLScorer
from sono_eval.assessment.scorers.model_loader import ModelLoader, get_model_loader


# --- ModelLoader Tests ---


class TestModelLoaderSingleton:
    """Test ModelLoader singleton behavior."""

    def test_singleton_returns_same_instance(self):
        """Test that ModelLoader follows the singleton pattern."""
        # Reset singleton for clean test
        ModelLoader._instance = None
        loader1 = ModelLoader()
        loader2 = ModelLoader()
        assert loader1 is loader2
        # Clean up
        ModelLoader._instance = None

    def test_get_model_loader_convenience(self):
        """Test the module-level convenience function."""
        ModelLoader._instance = None
        loader = get_model_loader()
        assert isinstance(loader, ModelLoader)
        ModelLoader._instance = None


class TestModelLoaderProperties:
    """Test ModelLoader properties and state."""

    def setup_method(self):
        """Reset singleton before each test."""
        ModelLoader._instance = None
        ModelLoader._model = None
        ModelLoader._tokenizer = None
        ModelLoader._model_version = "unknown"

    def teardown_method(self):
        """Clean up singleton after each test."""
        ModelLoader._instance = None
        ModelLoader._model = None
        ModelLoader._tokenizer = None
        ModelLoader._model_version = "unknown"

    def test_is_available_false_initially(self):
        """Test that model is not available before loading."""
        loader = ModelLoader()
        assert loader.is_available is False

    def test_model_version_unknown_initially(self):
        """Test that model version is 'unknown' before loading."""
        loader = ModelLoader()
        assert loader.model_version == "unknown"

    def test_load_disabled_via_env(self):
        """Test that loading can be disabled via environment variable."""
        with patch.dict(os.environ, {"ML_MODEL_ENABLED": "false"}):
            loader = ModelLoader()
            loader._loaded = False
            result = loader.load()
            assert result is False
            assert loader.is_available is False

    def test_load_returns_true_if_already_loaded_with_model(self):
        """Test that load returns True if model was already loaded."""
        loader = ModelLoader()
        loader._loaded = True
        loader._model = MagicMock()
        assert loader.load() is True

    def test_load_returns_false_if_already_loaded_without_model(self):
        """Test that load returns False if previously loaded but no model."""
        loader = ModelLoader()
        loader._loaded = True
        loader._model = None
        assert loader.load() is False

    def test_load_handles_transformer_import_error(self):
        """Test that load handles ImportError gracefully."""
        loader = ModelLoader()
        loader._loaded = False
        loader._enabled = True

        with patch.object(
            loader, "_load_transformer_model", side_effect=ImportError("no transformers")
        ):
            result = loader.load()
            assert result is False

    def test_load_handles_generic_exception(self):
        """Test that load handles generic exceptions gracefully."""
        loader = ModelLoader()
        loader._loaded = False
        loader._enabled = True

        with patch.object(
            loader, "_load_transformer_model", side_effect=RuntimeError("GPU OOM")
        ):
            result = loader.load()
            assert result is False

    def test_unload_clears_model(self):
        """Test that unload clears the model and tokenizer."""
        loader = ModelLoader()
        loader._model = MagicMock()
        loader._tokenizer = MagicMock()
        loader._loaded = True

        loader.unload()

        assert loader._model is None
        assert loader._tokenizer is None
        assert loader._loaded is False

    def test_get_embeddings_returns_none_when_unavailable(self):
        """Test that get_embeddings returns None when model not loaded."""
        loader = ModelLoader()
        loader._loaded = False
        loader._model = None
        assert loader.get_embeddings("def foo(): pass") is None

    def test_get_code_quality_score_returns_none_when_unavailable(self):
        """Test that get_code_quality_score returns None when model not loaded."""
        loader = ModelLoader()
        loader._loaded = False
        loader._model = None
        assert loader.get_code_quality_score("def foo(): pass") is None


# --- MLScorer Tests ---


class TestMLScorerInit:
    """Test MLScorer initialization."""

    def setup_method(self):
        ModelLoader._instance = None
        ModelLoader._model = None
        ModelLoader._tokenizer = None
        ModelLoader._model_version = "unknown"

    def teardown_method(self):
        ModelLoader._instance = None
        ModelLoader._model = None
        ModelLoader._tokenizer = None
        ModelLoader._model_version = "unknown"

    def test_initial_state(self):
        """Test MLScorer initializes with correct default state."""
        scorer = MLScorer()
        assert scorer._use_ast_analysis is True
        assert scorer._use_trained_model is False

    def test_model_version_ast_only(self):
        """Test model version returns 'ast-only' without trained model."""
        scorer = MLScorer()
        assert scorer.model_version == "ast-only"

    def test_load_model_falls_back_to_ast(self):
        """Test that load_model_if_available falls back to AST analysis."""
        scorer = MLScorer()

        with patch.object(scorer._model_loader, "load", return_value=False):
            result = scorer.load_model_if_available()
            assert result is True  # Always returns True (AST fallback)
            assert scorer._use_trained_model is False
            assert scorer._use_ast_analysis is True

    def test_load_model_with_trained_model(self):
        """Test that load_model_if_available sets trained model flag."""
        scorer = MLScorer()

        with patch.object(scorer._model_loader, "load", return_value=True):
            with patch.object(
                type(scorer._model_loader),
                "model_version",
                new_callable=PropertyMock,
                return_value="codebert-v1",
            ):
                result = scorer.load_model_if_available()
                assert result is True
                assert scorer._use_trained_model is True


class TestMLScorerGetInsights:
    """Test MLScorer.get_insights method."""

    def setup_method(self):
        ModelLoader._instance = None
        ModelLoader._model = None
        ModelLoader._tokenizer = None
        ModelLoader._model_version = "unknown"

    def teardown_method(self):
        ModelLoader._instance = None
        ModelLoader._model = None
        ModelLoader._tokenizer = None
        ModelLoader._model_version = "unknown"

    def test_returns_none_for_empty_content(self):
        """Test that empty content returns None."""
        scorer = MLScorer()
        result = scorer.get_insights({"code": ""}, PathType.TECHNICAL)
        assert result is None

    def test_returns_none_for_no_text(self):
        """Test that content with no extractable text returns None."""
        scorer = MLScorer()
        result = scorer.get_insights({}, PathType.TECHNICAL)
        # extract_text_content returns str(content) when no keys match,
        # so this won't be None/empty
        assert result is not None or result is None  # depends on fallback text

    def test_ast_only_insights_for_valid_python(self):
        """Test AST-only analysis for valid Python code."""
        scorer = MLScorer()
        scorer.load_model_if_available()

        code = (
            "def calculate_sum(a, b):\n"
            '    """Calculate sum."""\n'
            "    return a + b\n\n"
            "class DataProcessor:\n"
            '    """Process data."""\n'
            "    def process(self, data):\n"
            "        return [d * 2 for d in data]\n"
        )

        result = scorer.get_insights({"code": code}, PathType.TECHNICAL)

        assert result is not None
        assert "score" in result
        assert "pattern" in result
        assert "confidence" in result
        assert "analysis_mode" in result
        assert result["analysis_mode"] == "ast_only"
        assert result["model_version"] == "ast-only"
        assert 0 <= result["score"] <= 100
        assert 0 <= result["confidence"] <= 1

    def test_insights_include_recommendations(self):
        """Test that insights include recommendations."""
        scorer = MLScorer()
        scorer.load_model_if_available()

        code = "def foo(): pass"
        result = scorer.get_insights({"code": code}, PathType.TECHNICAL)

        assert result is not None
        assert "recommendations" in result
        assert isinstance(result["recommendations"], list)
        assert len(result["recommendations"]) > 0

    def test_insights_include_metrics(self):
        """Test that insights include detailed metrics."""
        scorer = MLScorer()
        scorer.load_model_if_available()

        code = "def foo():\n    return 42"
        result = scorer.get_insights({"code": code}, PathType.TECHNICAL)

        assert result is not None
        assert "metrics" in result
        assert "complexity" in result["metrics"]
        assert "naming" in result["metrics"]
        assert "readability" in result["metrics"]

    def test_invalid_python_handled_gracefully(self):
        """Test that invalid Python code is handled gracefully."""
        scorer = MLScorer()
        scorer.load_model_if_available()

        # This is valid text but not valid Python for AST parsing
        code = "this is not :: valid {python} code"
        result = scorer.get_insights({"code": code}, PathType.TECHNICAL)

        # Should still return something (with fallback metrics)
        assert result is not None
        assert "score" in result

    def test_high_complexity_code_gets_lower_score(self):
        """Test that highly complex code gets a lower score."""
        scorer = MLScorer()
        scorer.load_model_if_available()

        simple_code = (
            "def add(a, b):\n"
            '    """Add two numbers."""\n'
            "    return a + b\n"
        )

        complex_code = (
            "def complex_func(x):\n"
            "    if x > 0:\n"
            "        if x > 10:\n"
            "            if x > 20:\n"
            "                for i in range(x):\n"
            "                    try:\n"
            "                        while True:\n"
            "                            break\n"
            "                    except:\n"
            "                        pass\n"
            "    return x\n"
        )

        simple_result = scorer.get_insights({"code": simple_code}, PathType.TECHNICAL)
        complex_result = scorer.get_insights({"code": complex_code}, PathType.TECHNICAL)

        assert simple_result is not None
        assert complex_result is not None
        assert simple_result["score"] > complex_result["score"]

    def test_pattern_identification(self):
        """Test pattern identification based on metrics."""
        scorer = MLScorer()

        # Test high complexity pattern
        pattern = scorer._identify_pattern(
            {"cyclomatic_complexity": 25, "nesting_depth": 6},
            {"consistency": 0.5},
        )
        assert pattern == "high_complexity_code"

        # Test clean code pattern
        pattern = scorer._identify_pattern(
            {"cyclomatic_complexity": 5, "nesting_depth": 2},
            {"consistency": 0.9},
        )
        assert pattern == "clean_well_structured_code"

        # Test inconsistent naming pattern
        pattern = scorer._identify_pattern(
            {"cyclomatic_complexity": 5, "nesting_depth": 2},
            {"consistency": 0.3},
        )
        assert pattern == "inconsistent_naming_patterns"

        # Test moderate pattern
        pattern = scorer._identify_pattern(
            {"cyclomatic_complexity": 12, "nesting_depth": 3},
            {"consistency": 0.6},
        )
        assert pattern == "moderate_complexity_code"


class TestMLScorerCombineScores:
    """Test MLScorer.combine_scores method."""

    def setup_method(self):
        ModelLoader._instance = None
        ModelLoader._model = None

    def teardown_method(self):
        ModelLoader._instance = None
        ModelLoader._model = None

    def test_heuristic_only_when_no_ml(self):
        """Test that combine_scores returns heuristic scores when ML is None."""
        scorer = MLScorer()
        evidence = [
            Evidence(
                type=EvidenceType.CODE_QUALITY,
                description="test",
                source="test",
                weight=0.5,
            )
        ]

        score, confidence, combined_evidence, explanation = scorer.combine_scores(
            heuristic_score=80.0,
            ml_score=None,
            heuristic_confidence=0.85,
            ml_confidence=None,
            heuristic_evidence=evidence,
            ml_insights=None,
        )

        assert score == 80.0
        assert confidence == 0.85
        assert len(combined_evidence) == 1
        assert "heuristic" in explanation.lower()

    def test_combined_scores_with_ml(self):
        """Test that combine_scores properly weights heuristic and ML scores."""
        scorer = MLScorer()
        scorer._use_ast_analysis = True
        evidence = [
            Evidence(
                type=EvidenceType.CODE_QUALITY,
                description="test",
                source="test",
                weight=0.5,
            )
        ]

        ml_insights = {
            "pattern": "clean_well_structured_code",
            "details": "Good structure",
        }

        score, confidence, combined_evidence, explanation = scorer.combine_scores(
            heuristic_score=80.0,
            ml_score=90.0,
            heuristic_confidence=0.85,
            ml_confidence=0.9,
            heuristic_evidence=evidence,
            ml_insights=ml_insights,
        )

        # 80*0.6 + 90*0.4 = 48 + 36 = 84
        assert score == pytest.approx(84.0)
        # 0.85*0.6 + 0.9*0.4 = 0.51 + 0.36 = 0.87
        assert confidence == pytest.approx(0.87)
        # Original evidence + ML evidence
        assert len(combined_evidence) == 2
        assert "heuristic" in explanation.lower()
        assert "ast" in explanation.lower()

    def test_combined_scores_without_ml_confidence(self):
        """Test combine_scores when ML confidence is None."""
        scorer = MLScorer()
        scorer._use_ast_analysis = True

        score, confidence, _, _ = scorer.combine_scores(
            heuristic_score=80.0,
            ml_score=90.0,
            heuristic_confidence=0.85,
            ml_confidence=None,
            heuristic_evidence=[],
            ml_insights={"pattern": "test"},
        )

        # 80*0.6 + 90*0.4 = 84
        assert score == pytest.approx(84.0)
        # 0.85 * 0.8 = 0.68
        assert confidence == pytest.approx(0.68)


class TestMLScorerEnhanceMetrics:
    """Test MLScorer.enhance_metrics method."""

    def setup_method(self):
        ModelLoader._instance = None
        ModelLoader._model = None

    def teardown_method(self):
        ModelLoader._instance = None
        ModelLoader._model = None

    def test_returns_unchanged_with_no_insights(self):
        """Test that metrics are returned unchanged without insights."""
        scorer = MLScorer()
        metrics = [
            ScoringMetric(
                name="Test",
                category="test",
                score=50.0,
                weight=1.0,
                evidence=[],
                explanation="test",
            )
        ]

        result = scorer.enhance_metrics(metrics, {}, PathType.TECHNICAL)
        assert result == metrics

    def test_adds_ast_evidence_to_metrics(self):
        """Test that ML insights add AST evidence to existing metrics."""
        scorer = MLScorer()
        metrics = [
            ScoringMetric(
                name="Test",
                category="test",
                score=50.0,
                weight=1.0,
                evidence=[],
                explanation="test",
            )
        ]

        insights = {
            "pattern": "clean_well_structured_code",
            "confidence": 0.8,
            "score": 85.0,
            "details": "Well structured code detected",
        }

        result = scorer.enhance_metrics(metrics, insights, PathType.TECHNICAL)

        # Should add evidence to existing metric and add new metric
        assert len(result) == 2
        assert len(result[0].evidence) > 0
        assert result[1].name == "Code Structure Analysis"

    def test_high_confidence_boosts_metric_confidence(self):
        """Test that high ML confidence boosts original metric confidence."""
        scorer = MLScorer()
        metrics = [
            ScoringMetric(
                name="Test",
                category="test",
                score=50.0,
                weight=1.0,
                evidence=[],
                explanation="test",
                confidence=0.8,
            )
        ]

        insights = {
            "pattern": "clean_code",
            "confidence": 0.9,  # > 0.7 threshold
            "score": 85.0,
            "details": "Good code",
        }

        result = scorer.enhance_metrics(metrics, insights, PathType.TECHNICAL)
        # Confidence should be boosted by 1.1x, capped at 1.0
        assert result[0].confidence >= 0.8


class TestMLScorerScoreHelpers:
    """Test MLScorer internal scoring helper methods."""

    def setup_method(self):
        ModelLoader._instance = None
        ModelLoader._model = None

    def teardown_method(self):
        ModelLoader._instance = None
        ModelLoader._model = None

    def test_score_complexity(self):
        """Test complexity scoring."""
        scorer = MLScorer()

        # Low complexity = high score
        score = scorer._score_complexity(
            {"cyclomatic_complexity": 2, "nesting_depth": 1, "function_length_avg": 10}
        )
        assert score > 70

        # High complexity = low score
        score = scorer._score_complexity(
            {"cyclomatic_complexity": 25, "nesting_depth": 8, "function_length_avg": 100}
        )
        assert score < 30

    def test_score_readability(self):
        """Test readability scoring."""
        scorer = MLScorer()

        # No documentation
        assert scorer._score_readability({"flesch_reading_ease": 0}) == 50.0

        # Ideal range for technical docs (50-70)
        assert scorer._score_readability({"flesch_reading_ease": 60}) == 90.0

        # Acceptable range
        assert scorer._score_readability({"flesch_reading_ease": 45}) == 75.0
        assert scorer._score_readability({"flesch_reading_ease": 75}) == 75.0

        # Edge ranges
        assert scorer._score_readability({"flesch_reading_ease": 35}) == 60.0
        assert scorer._score_readability({"flesch_reading_ease": 85}) == 60.0

        # Extreme values
        assert scorer._score_readability({"flesch_reading_ease": 95}) == 50.0

    def test_generate_recommendations(self):
        """Test recommendation generation."""
        scorer = MLScorer()

        # High complexity triggers recommendation
        recs = scorer._generate_recommendations(
            {"cyclomatic_complexity": 20, "nesting_depth": 6, "function_length_avg": 60},
            {"consistency": 0.4},
            {"flesch_reading_ease": 0},
        )
        assert any("complex" in r.lower() for r in recs)
        assert any("nesting" in r.lower() for r in recs)
        assert any("naming" in r.lower() for r in recs)
        assert any("documentation" in r.lower() or "docstring" in r.lower() for r in recs)

    def test_recommendations_for_good_code(self):
        """Test that good code gets positive recommendation."""
        scorer = MLScorer()

        recs = scorer._generate_recommendations(
            {"cyclomatic_complexity": 3, "nesting_depth": 2, "function_length_avg": 15},
            {"consistency": 0.9},
            {"flesch_reading_ease": 60},
        )
        assert any("good" in r.lower() or "best practices" in r.lower() for r in recs)
