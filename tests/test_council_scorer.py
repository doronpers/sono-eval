"""Comprehensive tests for Council AI scorer."""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from sono_eval.assessment.models import (
    Evidence,
    EvidenceType,
    PathType,
    ScoringMetric,
)
from sono_eval.assessment.scorers.council_scorer import CouncilScorer


class TestCouncilScorerInitialization:
    """Test CouncilScorer initialization."""

    def test_initialization_default_state(self):
        """Test scorer initializes with default state."""
        scorer = CouncilScorer()

        assert scorer._council is None
        assert scorer._available is False

    def test_load_if_available_success(self):
        """Test successful Council AI initialization."""
        scorer = CouncilScorer()

        with patch(
            "sono_eval.assessment.scorers.council_scorer.Council"
        ) as MockCouncil:
            mock_council = Mock()
            MockCouncil.for_domain.return_value = mock_council

            result = scorer.load_if_available()

            assert result is True
            assert scorer._available is True
            assert scorer._council == mock_council
            MockCouncil.for_domain.assert_called_once_with("coding")

    def test_load_if_available_already_loaded(self):
        """Test that load_if_available returns True if already loaded."""
        scorer = CouncilScorer()
        scorer._council = Mock()

        with patch(
            "sono_eval.assessment.scorers.council_scorer.Council"
        ) as MockCouncil:
            result = scorer.load_if_available()

            assert result is True
            # Should not try to initialize again
            MockCouncil.for_domain.assert_not_called()

    def test_load_if_available_failure(self):
        """Test handling when Council AI initialization fails."""
        scorer = CouncilScorer()

        with patch(
            "sono_eval.assessment.scorers.council_scorer.Council"
        ) as MockCouncil:
            MockCouncil.for_domain.side_effect = Exception("API key not found")

            result = scorer.load_if_available()

            assert result is False
            assert scorer._available is False
            assert scorer._council is None

    def test_load_if_available_import_error(self):
        """Test handling when Council AI package is not installed."""
        scorer = CouncilScorer()

        with patch(
            "sono_eval.assessment.scorers.council_scorer.Council"
        ) as MockCouncil:
            MockCouncil.for_domain.side_effect = ImportError(
                "No module named 'council_ai'"
            )

            result = scorer.load_if_available()

            assert result is False
            assert scorer._available is False


class TestGetInsights:
    """Test get_insights method."""

    @pytest.mark.asyncio
    async def test_get_insights_not_available(self):
        """Test that get_insights returns None when Council not available."""
        scorer = CouncilScorer()
        scorer._available = False

        result = await scorer.get_insights(
            {"code": "def hello(): pass"}, PathType.TECHNICAL
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_get_insights_successful(self):
        """Test successful insight generation."""
        scorer = CouncilScorer()
        scorer._available = True

        # Mock council response
        mock_response1 = Mock()
        mock_response1.persona.name = "Rams"
        mock_response1.content = "Good code structure, score: 85/100"

        mock_response2 = Mock()
        mock_response2.persona.name = "Holman"
        mock_response2.content = "Clean implementation"

        mock_result = Mock()
        mock_result.synthesis = "Overall good work with score: 85/100"
        mock_result.responses = [mock_response1, mock_response2]

        mock_council = Mock()
        mock_council.consult_async = AsyncMock(return_value=mock_result)
        scorer._council = mock_council

        with patch(
            "sono_eval.assessment.scorers.council_scorer.extract_text_content"
        ) as mock_extract:
            mock_extract.return_value = "def hello(): pass"

            result = await scorer.get_insights(
                {"code": "def hello(): pass"}, PathType.TECHNICAL
            )

            assert result is not None
            assert result["synthesis"] == "Overall good work with score: 85/100"
            assert result["score"] == 85.0
            assert result["confidence"] == 0.85
            assert len(result["responses"]) == 2
            assert result["responses"][0]["persona"] == "Rams"

    @pytest.mark.asyncio
    async def test_get_insights_empty_content(self):
        """Test handling of empty content."""
        scorer = CouncilScorer()
        scorer._available = True
        scorer._council = Mock()

        with patch(
            "sono_eval.assessment.scorers.council_scorer.extract_text_content"
        ) as mock_extract:
            mock_extract.return_value = ""

            result = await scorer.get_insights({}, PathType.TECHNICAL)

            assert result is None

    @pytest.mark.asyncio
    async def test_get_insights_council_error(self):
        """Test handling when Council consultation fails."""
        scorer = CouncilScorer()
        scorer._available = True

        mock_council = Mock()
        mock_council.consult_async = AsyncMock(
            side_effect=Exception("Council API error")
        )
        scorer._council = mock_council

        with patch(
            "sono_eval.assessment.scorers.council_scorer.extract_text_content"
        ) as mock_extract:
            mock_extract.return_value = "def hello(): pass"

            result = await scorer.get_insights(
                {"code": "def hello(): pass"}, PathType.TECHNICAL
            )

            assert result is None

    @pytest.mark.asyncio
    async def test_get_insights_score_extraction(self):
        """Test extraction of numerical score from synthesis."""
        scorer = CouncilScorer()
        scorer._available = True

        mock_result = Mock()
        mock_result.synthesis = (
            "The code quality is good. I would give it a score: 92/100"
        )
        mock_result.responses = []

        mock_council = Mock()
        mock_council.consult_async = AsyncMock(return_value=mock_result)
        scorer._council = mock_council

        with patch(
            "sono_eval.assessment.scorers.council_scorer.extract_text_content"
        ) as mock_extract:
            mock_extract.return_value = "code"

            result = await scorer.get_insights({"code": "code"}, PathType.TECHNICAL)

            assert result["score"] == 92.0

    @pytest.mark.asyncio
    async def test_get_insights_no_score_in_synthesis(self):
        """Test handling when score cannot be extracted."""
        scorer = CouncilScorer()
        scorer._available = True

        mock_result = Mock()
        mock_result.synthesis = "The code is good but needs improvement"
        mock_result.responses = []

        mock_council = Mock()
        mock_council.consult_async = AsyncMock(return_value=mock_result)
        scorer._council = mock_council

        with patch(
            "sono_eval.assessment.scorers.council_scorer.extract_text_content"
        ) as mock_extract:
            mock_extract.return_value = "code"

            result = await scorer.get_insights({"code": "code"}, PathType.TECHNICAL)

            assert result["score"] is None

    @pytest.mark.asyncio
    async def test_get_insights_different_paths(self):
        """Test insights for different assessment paths."""
        scorer = CouncilScorer()
        scorer._available = True

        mock_result = Mock()
        mock_result.synthesis = "Assessment complete"
        mock_result.responses = []

        mock_council = Mock()
        mock_council.consult_async = AsyncMock(return_value=mock_result)
        scorer._council = mock_council

        with patch(
            "sono_eval.assessment.scorers.council_scorer.extract_text_content"
        ) as mock_extract:
            mock_extract.return_value = "content"

            # Test different paths
            for path in [PathType.TECHNICAL, PathType.DESIGN, PathType.COLLABORATION]:
                result = await scorer.get_insights({"content": "test"}, path)
                assert result is not None

                # Verify path was included in query
                call_args = mock_council.consult_async.call_args[0][0]
                assert path.value in call_args.lower()

    @pytest.mark.asyncio
    async def test_get_insights_content_truncation(self):
        """Test that long content is truncated."""
        scorer = CouncilScorer()
        scorer._available = True

        mock_result = Mock()
        mock_result.synthesis = "Review complete"
        mock_result.responses = []

        mock_council = Mock()
        mock_council.consult_async = AsyncMock(return_value=mock_result)
        scorer._council = mock_council

        long_content = "x" * 10000

        with patch(
            "sono_eval.assessment.scorers.council_scorer.extract_text_content"
        ) as mock_extract:
            mock_extract.return_value = long_content

            await scorer.get_insights({"code": long_content}, PathType.TECHNICAL)

            # Verify content was truncated to 8000 chars
            call_args = mock_council.consult_async.call_args[0][0]
            # The query includes the content, should be limited
            assert len(call_args) < 10000

    @pytest.mark.asyncio
    async def test_get_insights_multiple_personas(self):
        """Test handling multiple persona responses."""
        scorer = CouncilScorer()
        scorer._available = True

        # Create multiple persona responses
        responses = []
        personas = ["Rams", "Holman", "Harper", "Torvalds"]
        for persona in personas:
            resp = Mock()
            resp.persona.name = persona
            resp.content = f"Feedback from {persona}"
            responses.append(resp)

        mock_result = Mock()
        mock_result.synthesis = "Consensus reached score: 80/100"
        mock_result.responses = responses

        mock_council = Mock()
        mock_council.consult_async = AsyncMock(return_value=mock_result)
        scorer._council = mock_council

        with patch(
            "sono_eval.assessment.scorers.council_scorer.extract_text_content"
        ) as mock_extract:
            mock_extract.return_value = "code"

            result = await scorer.get_insights({"code": "code"}, PathType.TECHNICAL)

            assert len(result["responses"]) == 4
            assert all(r["persona"] in personas for r in result["responses"])


class TestEnhanceMetrics:
    """Test enhance_metrics method."""

    def test_enhance_metrics_no_insights(self):
        """Test that metrics are unchanged when no insights provided."""
        scorer = CouncilScorer()

        original_metrics = [
            ScoringMetric(
                name="Test Metric",
                category="test",
                score=50.0,
                weight=1.0,
                evidence=[],
                explanation="Test",
                confidence=0.9,
            )
        ]

        result = scorer.enhance_metrics(original_metrics, None, PathType.TECHNICAL)

        assert len(result) == 1
        assert result == original_metrics

    def test_enhance_metrics_empty_insights(self):
        """Test handling of empty insights dict."""
        scorer = CouncilScorer()

        original_metrics = [
            ScoringMetric(
                name="Test Metric",
                category="test",
                score=50.0,
                weight=1.0,
                evidence=[],
                explanation="Test",
                confidence=0.9,
            )
        ]

        result = scorer.enhance_metrics(original_metrics, {}, PathType.TECHNICAL)

        # Should add council metric even with empty insights
        assert len(result) == 2

    def test_enhance_metrics_with_insights(self):
        """Test adding Council metric with insights."""
        scorer = CouncilScorer()

        original_metrics = [
            ScoringMetric(
                name="Heuristic Metric",
                category="heuristic",
                score=70.0,
                weight=0.6,
                evidence=[],
                explanation="Heuristic assessment",
                confidence=0.85,
            )
        ]

        council_insights = {
            "synthesis": "Excellent code quality with minor improvements needed",
            "score": 88.5,
            "confidence": 0.92,
            "responses": [],
        }

        result = scorer.enhance_metrics(
            original_metrics, council_insights, PathType.TECHNICAL
        )

        assert len(result) == 2

        # Check Council metric
        council_metric = result[1]
        assert council_metric.name == "AI Council Review"
        assert council_metric.category == "ai_assessment"
        assert council_metric.score == 88.5
        assert council_metric.weight == 0.4
        assert council_metric.confidence == 0.92

    def test_enhance_metrics_fallback_score(self):
        """Test fallback score when no score in insights."""
        scorer = CouncilScorer()

        original_metrics = []

        council_insights = {
            "synthesis": "Good work",
            "score": None,  # No score provided
            "confidence": 0.8,
        }

        result = scorer.enhance_metrics(
            original_metrics, council_insights, PathType.DESIGN
        )

        # Should use fallback score of 80.0
        assert result[0].score == 80.0

    def test_enhance_metrics_evidence_creation(self):
        """Test that evidence is properly created."""
        scorer = CouncilScorer()

        council_insights = {
            "synthesis": "Detailed analysis of the submission",
            "score": 75.0,
            "confidence": 0.88,
        }

        result = scorer.enhance_metrics([], council_insights, PathType.PROBLEM_SOLVING)

        # Check evidence
        metric = result[0]
        assert len(metric.evidence) == 1

        evidence = metric.evidence[0]
        assert evidence.type == EvidenceType.CODE_QUALITY
        assert evidence.description == "Council Consensus"
        assert evidence.source == "council_ai"
        assert evidence.weight == 1.0
        assert "synthesis" in evidence.metadata

    def test_enhance_metrics_synthesis_truncation(self):
        """Test that long synthesis is truncated in explanation."""
        scorer = CouncilScorer()

        long_synthesis = "x" * 500

        council_insights = {
            "synthesis": long_synthesis,
            "score": 85.0,
            "confidence": 0.9,
        }

        result = scorer.enhance_metrics([], council_insights, PathType.TECHNICAL)

        metric = result[0]
        # Explanation should truncate synthesis to 200 chars
        assert len(metric.explanation) < len(long_synthesis)
        assert "..." in metric.explanation

    def test_enhance_metrics_preserves_original(self):
        """Test that original metrics are preserved."""
        scorer = CouncilScorer()

        original_metrics = [
            ScoringMetric(
                name="Metric 1",
                category="cat1",
                score=60.0,
                weight=0.5,
                evidence=[],
                explanation="First",
                confidence=0.8,
            ),
            ScoringMetric(
                name="Metric 2",
                category="cat2",
                score=70.0,
                weight=0.5,
                evidence=[],
                explanation="Second",
                confidence=0.9,
            ),
        ]

        council_insights = {"synthesis": "Good", "score": 80.0, "confidence": 0.85}

        result = scorer.enhance_metrics(
            original_metrics, council_insights, PathType.TECHNICAL
        )

        # Original metrics should be first
        assert result[0].name == "Metric 1"
        assert result[1].name == "Metric 2"
        # Council metric added at end
        assert result[2].name == "AI Council Review"

    def test_enhance_metrics_confidence_fallback(self):
        """Test confidence fallback when not in insights."""
        scorer = CouncilScorer()

        council_insights = {
            "synthesis": "Review complete",
            "score": 90.0,
            # No confidence field
        }

        result = scorer.enhance_metrics([], council_insights, PathType.COMMUNICATION)

        metric = result[0]
        # Should use default confidence of 0.8
        assert metric.confidence == 0.8


class TestCouncilScorerIntegration:
    """Test integration scenarios."""

    @pytest.mark.asyncio
    async def test_full_workflow_available(self):
        """Test full workflow when Council is available."""
        scorer = CouncilScorer()

        # Mock successful initialization
        with patch(
            "sono_eval.assessment.scorers.council_scorer.Council"
        ) as MockCouncil:
            mock_council = Mock()
            MockCouncil.for_domain.return_value = mock_council

            # Initialize
            assert scorer.load_if_available() is True

            # Mock insights
            mock_result = Mock()
            mock_result.synthesis = "Excellent code, score: 95/100"
            mock_result.responses = []
            mock_council.consult_async = AsyncMock(return_value=mock_result)

            with patch(
                "sono_eval.assessment.scorers.council_scorer.extract_text_content"
            ) as mock_extract:
                mock_extract.return_value = "def test(): pass"

                # Get insights
                insights = await scorer.get_insights(
                    {"code": "def test(): pass"}, PathType.TECHNICAL
                )

                assert insights is not None
                assert insights["score"] == 95.0

                # Enhance metrics
                enhanced = scorer.enhance_metrics([], insights, PathType.TECHNICAL)

                assert len(enhanced) == 1
                assert enhanced[0].score == 95.0

    @pytest.mark.asyncio
    async def test_full_workflow_unavailable(self):
        """Test full workflow when Council is not available."""
        scorer = CouncilScorer()

        # Mock failed initialization
        with patch(
            "sono_eval.assessment.scorers.council_scorer.Council"
        ) as MockCouncil:
            MockCouncil.for_domain.side_effect = Exception("Not available")

            # Initialize fails
            assert scorer.load_if_available() is False

            # Get insights returns None
            insights = await scorer.get_insights(
                {"code": "def test(): pass"}, PathType.TECHNICAL
            )

            assert insights is None

            # Enhance metrics returns original
            original = []
            enhanced = scorer.enhance_metrics(original, insights, PathType.TECHNICAL)

            assert enhanced == original


class TestEdgeCases:
    """Test edge cases and error scenarios."""

    @pytest.mark.asyncio
    async def test_get_insights_with_none_content(self):
        """Test handling of None content."""
        scorer = CouncilScorer()
        scorer._available = True
        scorer._council = Mock()

        with patch(
            "sono_eval.assessment.scorers.council_scorer.extract_text_content"
        ) as mock_extract:
            mock_extract.return_value = None

            result = await scorer.get_insights(None, PathType.TECHNICAL)

            assert result is None

    @pytest.mark.asyncio
    async def test_score_extraction_variations(self):
        """Test score extraction with various formats."""
        scorer = CouncilScorer()
        scorer._available = True

        test_cases = [
            ("Score: 85/100", 85.0),
            ("I give it a score: 92/100", 92.0),
            ("SCORE: 78/100", 78.0),
            ("No score here", None),
            ("50 out of 100", None),  # Doesn't match pattern
        ]

        for synthesis, expected_score in test_cases:
            mock_result = Mock()
            mock_result.synthesis = synthesis
            mock_result.responses = []

            mock_council = Mock()
            mock_council.consult_async = AsyncMock(return_value=mock_result)
            scorer._council = mock_council

            with patch(
                "sono_eval.assessment.scorers.council_scorer.extract_text_content"
            ) as mock_extract:
                mock_extract.return_value = "code"

                result = await scorer.get_insights({"code": "code"}, PathType.TECHNICAL)

                assert result["score"] == expected_score
