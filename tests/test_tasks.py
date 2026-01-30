"""Comprehensive tests for async task processing with Celery."""

import sys
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest

# Mock celery before importing tasks
sys.modules["celery"] = MagicMock()

from sono_eval.tasks.assessment import AssessmentTask, process_assessment_task


class TestAssessmentTask:
    """Test AssessmentTask class."""

    def test_task_initialization(self):
        """Test that task initializes with None engines."""
        task = AssessmentTask()

        assert task._engine is None
        assert task._storage is None

    def test_lazy_engine_loading(self):
        """Test lazy loading of assessment engine."""
        task = AssessmentTask()

        with patch("sono_eval.tasks.assessment.AssessmentEngine") as MockEngine:
            mock_engine = Mock()
            MockEngine.return_value = mock_engine

            engine = task.engine

            assert engine == mock_engine
            MockEngine.assert_called_once()

            # Second access should return same instance
            engine2 = task.engine
            assert engine2 is engine
            assert MockEngine.call_count == 1  # Not called again

    def test_lazy_storage_loading(self):
        """Test lazy loading of MemU storage."""
        task = AssessmentTask()

        with patch("sono_eval.tasks.assessment.MemUStorage") as MockStorage:
            mock_storage = Mock()
            MockStorage.return_value = mock_storage

            storage = task.storage

            assert storage == mock_storage
            MockStorage.assert_called_once()

            # Second access should return same instance
            storage2 = task.storage
            assert storage2 is storage
            assert MockStorage.call_count == 1


class TestProcessAssessmentTask:
    """Test process_assessment_task function."""

    @pytest.fixture
    def mock_task_self(self):
        """Create mock self for bound task."""
        mock_self = Mock()
        mock_self.update_state = Mock()
        mock_self.retry = Mock(side_effect=Exception("Retry"))
        mock_self.request = Mock()
        mock_self.request.retries = 0
        mock_self.max_retries = 3
        return mock_self

    @pytest.fixture
    def sample_input_data(self):
        """Sample assessment input data."""
        return {
            "candidate_id": "test_candidate_123",
            "submission_type": "code",
            "content": {"code": "def hello(): return 'world'"},
            "paths_to_evaluate": ["technical", "problem_solving"],
        }

    @pytest.fixture
    def mock_result(self):
        """Mock assessment result."""
        mock = Mock()
        mock.overall_score = 85.5
        mock.processing_time_ms = 1250.0
        mock.model_dump = Mock(
            return_value={
                "overall_score": 85.5,
                "confidence_score": 0.92,
                "processing_time_ms": 1250.0,
                "paths": [],
            }
        )
        return mock

    def test_successful_assessment_task(
        self, mock_task_self, sample_input_data, mock_result
    ):
        """Test successful assessment processing."""
        # Mock the engine
        mock_engine = Mock()
        mock_engine.assess = AsyncMock(return_value=mock_result)
        mock_task_self.engine = mock_engine

        # Mock storage
        mock_storage = Mock()
        mock_memory = Mock()
        mock_memory.root_node.node_id = "root-123"
        mock_storage.get_candidate_memory = Mock(return_value=mock_memory)
        mock_storage.add_memory_node = Mock()
        mock_task_self.storage = mock_storage

        # Execute task
        with (
            patch("asyncio.new_event_loop") as mock_new_loop,
            patch("asyncio.set_event_loop"),
            patch("sono_eval.tasks.assessment.AssessmentInput") as MockInput,
        ):

            mock_loop = Mock()
            mock_new_loop.return_value = mock_loop
            mock_loop.run_until_complete = Mock(return_value=mock_result)
            mock_loop.close = Mock()

            mock_input = Mock()
            mock_input.candidate_id = "test_candidate_123"
            MockInput.model_validate = Mock(return_value=mock_input)

            result = process_assessment_task(
                mock_task_self, "assessment-001", sample_input_data
            )

            # Verify result
            assert result["job_status"] == "completed"
            assert result["overall_score"] == 85.5

            # Verify state updates were called
            assert mock_task_self.update_state.call_count == 2

            # Verify memory storage
            mock_storage.add_memory_node.assert_called_once()

    def test_assessment_task_with_input_validation(
        self, mock_task_self, sample_input_data, mock_result
    ):
        """Test that input is properly validated."""
        mock_engine = Mock()
        mock_engine.assess = AsyncMock(return_value=mock_result)
        mock_task_self.engine = mock_engine

        mock_storage = Mock()
        mock_storage.get_candidate_memory = Mock(return_value=None)
        mock_task_self.storage = mock_storage

        with (
            patch("asyncio.new_event_loop") as mock_new_loop,
            patch("asyncio.set_event_loop"),
            patch("sono_eval.tasks.assessment.AssessmentInput") as MockInput,
        ):

            mock_loop = Mock()
            mock_new_loop.return_value = mock_loop
            mock_loop.run_until_complete = Mock(return_value=mock_result)
            mock_loop.close = Mock()

            mock_input = Mock()
            mock_input.candidate_id = "test_candidate_123"
            MockInput.model_validate = Mock(return_value=mock_input)

            process_assessment_task(mock_task_self, "assessment-002", sample_input_data)

            # Verify input validation was called
            MockInput.model_validate.assert_called_once_with(sample_input_data)

    def test_assessment_task_stores_in_memory(
        self, mock_task_self, sample_input_data, mock_result
    ):
        """Test that assessment results are stored in memory."""
        mock_engine = Mock()
        mock_engine.assess = AsyncMock(return_value=mock_result)
        mock_task_self.engine = mock_engine

        mock_storage = Mock()
        mock_memory = Mock()
        mock_memory.root_node.node_id = "root-456"
        mock_storage.get_candidate_memory = Mock(return_value=mock_memory)
        mock_storage.add_memory_node = Mock()
        mock_task_self.storage = mock_storage

        with (
            patch("asyncio.new_event_loop") as mock_new_loop,
            patch("asyncio.set_event_loop"),
            patch("sono_eval.tasks.assessment.AssessmentInput") as MockInput,
        ):

            mock_loop = Mock()
            mock_new_loop.return_value = mock_loop
            mock_loop.run_until_complete = Mock(return_value=mock_result)
            mock_loop.close = Mock()

            mock_input = Mock()
            mock_input.candidate_id = "candidate_789"
            MockInput.model_validate = Mock(return_value=mock_input)

            process_assessment_task(mock_task_self, "assessment-003", sample_input_data)

            # Verify memory node was added
            mock_storage.add_memory_node.assert_called_once()
            call_args = mock_storage.add_memory_node.call_args

            assert call_args[0][0] == "candidate_789"  # candidate_id
            assert call_args[0][1] == "root-456"  # parent_id
            assert "assessment_result" in call_args[1]["data"]
            assert call_args[1]["metadata"]["type"] == "assessment"
            assert call_args[1]["metadata"]["async"] is True

    def test_assessment_task_candidate_not_found(
        self, mock_task_self, sample_input_data, mock_result
    ):
        """Test handling when candidate memory not found."""
        mock_engine = Mock()
        mock_engine.assess = AsyncMock(return_value=mock_result)
        mock_task_self.engine = mock_engine

        mock_storage = Mock()
        mock_storage.get_candidate_memory = Mock(return_value=None)  # Not found
        mock_task_self.storage = mock_storage

        with (
            patch("asyncio.new_event_loop") as mock_new_loop,
            patch("asyncio.set_event_loop"),
            patch("sono_eval.tasks.assessment.AssessmentInput") as MockInput,
        ):

            mock_loop = Mock()
            mock_new_loop.return_value = mock_loop
            mock_loop.run_until_complete = Mock(return_value=mock_result)
            mock_loop.close = Mock()

            mock_input = Mock()
            mock_input.candidate_id = "nonexistent"
            MockInput.model_validate = Mock(return_value=mock_input)

            result = process_assessment_task(
                mock_task_self, "assessment-004", sample_input_data
            )

            # Should still return result
            assert result["job_status"] == "completed"

    def test_assessment_task_failure_with_retry(
        self, mock_task_self, sample_input_data
    ):
        """Test task failure triggers retry."""
        mock_task_self.request.retries = 0

        # Mock engine to fail
        mock_engine = Mock()
        mock_engine.assess = AsyncMock(side_effect=Exception("Assessment failed"))
        mock_task_self.engine = mock_engine

        with (
            patch("asyncio.new_event_loop") as mock_new_loop,
            patch("asyncio.set_event_loop"),
            patch("sono_eval.tasks.assessment.AssessmentInput") as MockInput,
        ):

            mock_loop = Mock()
            mock_new_loop.return_value = mock_loop
            mock_loop.run_until_complete = Mock(
                side_effect=Exception("Assessment failed")
            )
            mock_loop.close = Mock()

            MockInput.model_validate = Mock(return_value=Mock())

            with pytest.raises(Exception):
                process_assessment_task(
                    mock_task_self, "assessment-005", sample_input_data
                )

            # Verify retry was called
            mock_task_self.retry.assert_called_once()

    def test_assessment_task_max_retries_exceeded(
        self, mock_task_self, sample_input_data
    ):
        """Test task returns failure after max retries."""
        mock_task_self.request.retries = 3  # Max retries
        mock_task_self.max_retries = 3
        mock_task_self.retry = Mock()  # Don't raise

        # Mock engine to fail
        mock_engine = Mock()
        mock_engine.assess = AsyncMock(side_effect=ValueError("Persistent error"))
        mock_task_self.engine = mock_engine

        with (
            patch("asyncio.new_event_loop") as mock_new_loop,
            patch("asyncio.set_event_loop"),
            patch("sono_eval.tasks.assessment.AssessmentInput") as MockInput,
        ):

            mock_loop = Mock()
            mock_new_loop.return_value = mock_loop
            mock_loop.run_until_complete = Mock(
                side_effect=ValueError("Persistent error")
            )
            mock_loop.close = Mock()

            MockInput.model_validate = Mock(return_value=Mock())

            result = process_assessment_task(
                mock_task_self, "assessment-006", sample_input_data
            )

            # Should return failure result
            assert result["job_status"] == "failed"
            assert "error" in result
            assert result["error_type"] == "ValueError"

            # Retry should NOT be called (max retries reached)
            mock_task_self.retry.assert_not_called()

    def test_assessment_task_state_updates(
        self, mock_task_self, sample_input_data, mock_result
    ):
        """Test that task state is updated during processing."""
        mock_engine = Mock()
        mock_engine.assess = AsyncMock(return_value=mock_result)
        mock_task_self.engine = mock_engine

        mock_storage = Mock()
        mock_storage.get_candidate_memory = Mock(return_value=None)
        mock_task_self.storage = mock_storage

        with (
            patch("asyncio.new_event_loop") as mock_new_loop,
            patch("asyncio.set_event_loop"),
            patch("sono_eval.tasks.assessment.AssessmentInput") as MockInput,
        ):

            mock_loop = Mock()
            mock_new_loop.return_value = mock_loop
            mock_loop.run_until_complete = Mock(return_value=mock_result)
            mock_loop.close = Mock()

            mock_input = Mock()
            mock_input.candidate_id = "test_candidate"
            MockInput.model_validate = Mock(return_value=mock_input)

            process_assessment_task(mock_task_self, "assessment-007", sample_input_data)

            # Verify state updates
            assert mock_task_self.update_state.call_count == 2

            # Check first update (PROCESSING)
            first_call = mock_task_self.update_state.call_args_list[0]
            assert first_call[1]["state"] == "PROCESSING"
            assert first_call[1]["meta"]["status"] == "processing"
            assert first_call[1]["meta"]["progress"] == 10

            # Check second update (STORING)
            second_call = mock_task_self.update_state.call_args_list[1]
            assert second_call[1]["state"] == "PROCESSING"
            assert second_call[1]["meta"]["status"] == "storing"
            assert second_call[1]["meta"]["progress"] == 80

    def test_assessment_task_exponential_backoff(
        self, mock_task_self, sample_input_data
    ):
        """Test retry uses exponential backoff."""
        mock_task_self.request.retries = 1  # Second attempt

        mock_engine = Mock()
        mock_engine.assess = AsyncMock(side_effect=Exception("Temporary failure"))
        mock_task_self.engine = mock_engine

        with (
            patch("asyncio.new_event_loop") as mock_new_loop,
            patch("asyncio.set_event_loop"),
            patch("sono_eval.tasks.assessment.AssessmentInput") as MockInput,
        ):

            mock_loop = Mock()
            mock_new_loop.return_value = mock_loop
            mock_loop.run_until_complete = Mock(
                side_effect=Exception("Temporary failure")
            )
            mock_loop.close = Mock()

            MockInput.model_validate = Mock(return_value=Mock())

            with pytest.raises(Exception):
                process_assessment_task(
                    mock_task_self, "assessment-008", sample_input_data
                )

            # Verify exponential backoff: 2^retries * 60
            # For retry 1: 2^1 * 60 = 120 seconds
            call_args = mock_task_self.retry.call_args
            assert call_args[1]["countdown"] == 120

    def test_assessment_task_asyncio_cleanup(
        self, mock_task_self, sample_input_data, mock_result
    ):
        """Test that asyncio event loop is properly cleaned up."""
        mock_engine = Mock()
        mock_engine.assess = AsyncMock(return_value=mock_result)
        mock_task_self.engine = mock_engine

        mock_storage = Mock()
        mock_storage.get_candidate_memory = Mock(return_value=None)
        mock_task_self.storage = mock_storage

        with (
            patch("asyncio.new_event_loop") as mock_new_loop,
            patch("asyncio.set_event_loop") as mock_set_loop,
            patch("sono_eval.tasks.assessment.AssessmentInput") as MockInput,
        ):

            mock_loop = Mock()
            mock_new_loop.return_value = mock_loop
            mock_loop.run_until_complete = Mock(return_value=mock_result)
            mock_loop.close = Mock()

            MockInput.model_validate = Mock(return_value=Mock(candidate_id="test"))

            process_assessment_task(mock_task_self, "assessment-009", sample_input_data)

            # Verify loop cleanup
            mock_loop.close.assert_called_once()


class TestCleanupExpiredResults:
    """Test cleanup_expired_results task."""

    def test_cleanup_task_execution(self):
        """Test cleanup task executes successfully."""
        from sono_eval.tasks.assessment import cleanup_expired_results

        result = cleanup_expired_results()

        assert result["status"] == "completed"
        assert "items_cleaned" in result
        assert result["items_cleaned"] == 0  # No actual cleanup yet

    def test_cleanup_task_returns_stats(self):
        """Test cleanup task returns proper statistics."""
        from sono_eval.tasks.assessment import cleanup_expired_results

        result = cleanup_expired_results()

        assert "status" in result
        assert "items_cleaned" in result
        assert "message" in result
        assert result["message"] == "Cleanup completed successfully"


class TestTaskConfiguration:
    """Test task configuration and metadata."""

    def test_process_assessment_task_configuration(self):
        """Test that process_assessment_task has correct configuration."""
        # Task should be bound and have retry settings
        assert hasattr(process_assessment_task, "max_retries")
        assert hasattr(process_assessment_task, "default_retry_delay")

    def test_cleanup_task_configuration(self):
        """Test cleanup task configuration."""
        from sono_eval.tasks.assessment import cleanup_expired_results

        # Should be a registered Celery task
        assert callable(cleanup_expired_results)


class TestTaskEdgeCases:
    """Test edge cases and error scenarios."""

    @pytest.fixture
    def mock_task_self(self):
        """Create mock self for bound task."""
        mock_self = Mock()
        mock_self.update_state = Mock()
        mock_self.retry = Mock(side_effect=Exception("Retry"))
        mock_self.request = Mock()
        mock_self.request.retries = 0
        mock_self.max_retries = 3
        return mock_self

    def test_malformed_input_data(self, mock_task_self):
        """Test handling of malformed input data."""
        malformed_data = {
            "candidate_id": "test",
            # Missing required fields
        }

        with patch("sono_eval.tasks.assessment.AssessmentInput") as MockInput:
            MockInput.model_validate = Mock(side_effect=ValueError("Validation failed"))

            with pytest.raises(Exception):
                process_assessment_task(
                    mock_task_self, "assessment-bad", malformed_data
                )

            # Should trigger retry
            mock_task_self.retry.assert_called_once()

    def test_empty_input_data(self, mock_task_self):
        """Test handling of empty input data."""
        with patch("sono_eval.tasks.assessment.AssessmentInput") as MockInput:
            MockInput.model_validate = Mock(side_effect=ValueError("Empty input"))

            with pytest.raises(Exception):
                process_assessment_task(mock_task_self, "assessment-empty", {})

    def test_engine_initialization_failure(self, mock_task_self):
        """Test handling when engine fails to initialize."""
        # Remove engine property to simulate initialization failure
        mock_task_self.engine = Mock()
        mock_task_self.engine.assess = AsyncMock(
            side_effect=RuntimeError("Engine not initialized")
        )

        with (
            patch("asyncio.new_event_loop") as mock_new_loop,
            patch("asyncio.set_event_loop"),
            patch("sono_eval.tasks.assessment.AssessmentInput") as MockInput,
        ):

            mock_loop = Mock()
            mock_new_loop.return_value = mock_loop
            mock_loop.run_until_complete = Mock(
                side_effect=RuntimeError("Engine not initialized")
            )
            mock_loop.close = Mock()

            MockInput.model_validate = Mock(return_value=Mock())

            with pytest.raises(Exception):
                process_assessment_task(
                    mock_task_self,
                    "assessment-engine-fail",
                    {"candidate_id": "test", "content": {}},
                )
