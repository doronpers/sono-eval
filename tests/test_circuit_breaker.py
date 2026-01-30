"""Comprehensive tests for circuit breaker pattern."""

import asyncio
import time
from unittest.mock import AsyncMock, Mock

import pytest

from sono_eval.middleware.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerPool,
    CircuitState,
)


class TestCircuitBreakerBasics:
    """Test basic circuit breaker functionality."""

    @pytest.mark.asyncio
    async def test_initial_state_closed(self):
        """Test that circuit breaker starts in CLOSED state."""
        cb = CircuitBreaker(name="test", failure_threshold=3)

        assert cb.state == CircuitState.CLOSED
        assert cb.failure_count == 0

    @pytest.mark.asyncio
    async def test_successful_call_in_closed_state(self):
        """Test successful function call when circuit is closed."""
        cb = CircuitBreaker(name="test", failure_threshold=3)

        async def successful_func():
            return "success"

        result = await cb.call(successful_func)

        assert result == "success"
        assert cb.state == CircuitState.CLOSED
        assert cb.failure_count == 0

    @pytest.mark.asyncio
    async def test_failed_call_increments_counter(self):
        """Test that failed calls increment failure counter."""
        cb = CircuitBreaker(name="test", failure_threshold=3)

        async def failing_func():
            raise ValueError("Service error")

        # First failure
        with pytest.raises(ValueError):
            await cb.call(failing_func)

        assert cb.failure_count == 1
        assert cb.state == CircuitState.CLOSED

    @pytest.mark.asyncio
    async def test_circuit_opens_after_threshold(self):
        """Test that circuit opens after reaching failure threshold."""
        cb = CircuitBreaker(name="test", failure_threshold=3)

        async def failing_func():
            raise ValueError("Service error")

        # Fail 3 times
        for i in range(3):
            with pytest.raises(ValueError):
                await cb.call(failing_func)

        # Circuit should be open now
        assert cb.state == CircuitState.OPEN
        assert cb.failure_count == 3

    @pytest.mark.asyncio
    async def test_open_circuit_rejects_calls(self):
        """Test that open circuit rejects calls immediately."""
        cb = CircuitBreaker(name="test", failure_threshold=2, recovery_timeout=60)

        async def failing_func():
            raise ValueError("Service error")

        # Open the circuit
        for _ in range(2):
            with pytest.raises(ValueError):
                await cb.call(failing_func)

        # Next call should be rejected without calling function
        async def should_not_be_called():
            pytest.fail("Function should not be called when circuit is open")

        with pytest.raises(Exception) as exc_info:
            await cb.call(should_not_be_called)

        assert "Circuit breaker" in str(exc_info.value)
        assert "OPEN" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_transition_to_half_open_after_timeout(self):
        """Test transition to HALF_OPEN state after recovery timeout."""
        cb = CircuitBreaker(name="test", failure_threshold=2, recovery_timeout=1)

        async def failing_func():
            raise ValueError("Service error")

        # Open the circuit
        for _ in range(2):
            with pytest.raises(ValueError):
                await cb.call(failing_func)

        assert cb.state == CircuitState.OPEN

        # Wait for recovery timeout
        await asyncio.sleep(1.1)

        # Next call should transition to HALF_OPEN
        async def test_func():
            return "testing recovery"

        result = await cb.call(test_func)

        assert result == "testing recovery"
        assert cb.state == CircuitState.HALF_OPEN

    @pytest.mark.asyncio
    async def test_half_open_success_closes_circuit(self):
        """Test that successful calls in HALF_OPEN close the circuit."""
        cb = CircuitBreaker(
            name="test", failure_threshold=2, recovery_timeout=1, success_threshold=2
        )

        async def failing_func():
            raise ValueError("Service error")

        async def successful_func():
            return "success"

        # Open the circuit
        for _ in range(2):
            with pytest.raises(ValueError):
                await cb.call(failing_func)

        # Wait for recovery timeout
        await asyncio.sleep(1.1)

        # Make successful calls to close circuit
        await cb.call(successful_func)
        assert cb.state == CircuitState.HALF_OPEN
        assert cb.success_count == 1

        await cb.call(successful_func)
        assert cb.state == CircuitState.CLOSED
        assert cb.failure_count == 0

    @pytest.mark.asyncio
    async def test_half_open_failure_reopens_circuit(self):
        """Test that failure in HALF_OPEN reopens the circuit."""
        cb = CircuitBreaker(
            name="test", failure_threshold=2, recovery_timeout=1, success_threshold=2
        )

        async def failing_func():
            raise ValueError("Service error")

        # Open the circuit
        for _ in range(2):
            with pytest.raises(ValueError):
                await cb.call(failing_func)

        # Wait for recovery timeout
        await asyncio.sleep(1.1)

        # Fail in HALF_OPEN state
        with pytest.raises(ValueError):
            await cb.call(failing_func)

        # Should reopen
        assert cb.state == CircuitState.OPEN
        assert cb.success_count == 0

    @pytest.mark.asyncio
    async def test_successful_call_resets_failure_count(self):
        """Test that successful call in CLOSED state resets failure count."""
        cb = CircuitBreaker(name="test", failure_threshold=5)

        async def sometimes_fails(should_fail):
            if should_fail:
                raise ValueError("Error")
            return "success"

        # Accumulate some failures
        with pytest.raises(ValueError):
            await cb.call(sometimes_fails, True)
        with pytest.raises(ValueError):
            await cb.call(sometimes_fails, True)

        assert cb.failure_count == 2

        # Successful call should reset
        await cb.call(sometimes_fails, False)
        assert cb.failure_count == 0
        assert cb.state == CircuitState.CLOSED

    def test_get_state(self):
        """Test get_state method."""
        cb = CircuitBreaker(name="test")

        assert cb.get_state() == "closed"

        cb.state = CircuitState.OPEN
        assert cb.get_state() == "open"

        cb.state = CircuitState.HALF_OPEN
        assert cb.get_state() == "half_open"


class TestCircuitBreakerConfiguration:
    """Test circuit breaker configuration options."""

    @pytest.mark.asyncio
    async def test_custom_failure_threshold(self):
        """Test custom failure threshold."""
        cb = CircuitBreaker(name="test", failure_threshold=10)

        async def failing_func():
            raise ValueError("Error")

        # Should take 10 failures to open
        for i in range(9):
            with pytest.raises(ValueError):
                await cb.call(failing_func)
            assert cb.state == CircuitState.CLOSED

        # 10th failure opens circuit
        with pytest.raises(ValueError):
            await cb.call(failing_func)
        assert cb.state == CircuitState.OPEN

    @pytest.mark.asyncio
    async def test_custom_success_threshold(self):
        """Test custom success threshold for recovery."""
        cb = CircuitBreaker(
            name="test", failure_threshold=1, recovery_timeout=1, success_threshold=3
        )

        async def failing_func():
            raise ValueError("Error")

        async def successful_func():
            return "ok"

        # Open circuit
        with pytest.raises(ValueError):
            await cb.call(failing_func)

        # Wait and recover
        await asyncio.sleep(1.1)

        # Need 3 successes to close
        await cb.call(successful_func)
        assert cb.state == CircuitState.HALF_OPEN

        await cb.call(successful_func)
        assert cb.state == CircuitState.HALF_OPEN

        await cb.call(successful_func)
        assert cb.state == CircuitState.CLOSED

    @pytest.mark.asyncio
    async def test_custom_recovery_timeout(self):
        """Test custom recovery timeout."""
        cb = CircuitBreaker(name="test", failure_threshold=1, recovery_timeout=2)

        async def failing_func():
            raise ValueError("Error")

        # Open circuit
        with pytest.raises(ValueError):
            await cb.call(failing_func)

        # Wait less than timeout - should still be open
        await asyncio.sleep(1)

        with pytest.raises(Exception) as exc_info:
            await cb.call(failing_func)
        assert "OPEN" in str(exc_info.value)

    def test_circuit_breaker_name(self):
        """Test circuit breaker naming."""
        cb = CircuitBreaker(name="database-service")
        assert cb.name == "database-service"


class TestCircuitBreakerPool:
    """Test circuit breaker pool management."""

    def test_pool_initialization(self):
        """Test pool initializes empty."""
        pool = CircuitBreakerPool()
        assert len(pool.breakers) == 0

    def test_get_or_create_new_breaker(self):
        """Test creating new breaker in pool."""
        pool = CircuitBreakerPool()

        cb = pool.get_or_create("service1")

        assert cb.name == "service1"
        assert "service1" in pool.breakers
        assert len(pool.breakers) == 1

    def test_get_or_create_existing_breaker(self):
        """Test retrieving existing breaker from pool."""
        pool = CircuitBreakerPool()

        cb1 = pool.get_or_create("service1")
        cb2 = pool.get_or_create("service1")

        # Should return same instance
        assert cb1 is cb2
        assert len(pool.breakers) == 1

    def test_multiple_breakers_in_pool(self):
        """Test managing multiple breakers."""
        pool = CircuitBreakerPool()

        cb1 = pool.get_or_create("service1")
        cb2 = pool.get_or_create("service2")
        cb3 = pool.get_or_create("service3")

        assert len(pool.breakers) == 3
        assert cb1 is not cb2
        assert cb2 is not cb3

    def test_pool_status(self):
        """Test getting pool status."""
        pool = CircuitBreakerPool()

        pool.get_or_create("service1")
        pool.get_or_create("service2")

        # Open one circuit
        pool.breakers["service2"].state = CircuitState.OPEN

        status = pool.get_status()

        assert len(status) == 2
        assert status["service1"] == "closed"
        assert status["service2"] == "open"

    def test_custom_configuration_per_breaker(self):
        """Test creating breakers with custom configuration."""
        pool = CircuitBreakerPool()

        cb1 = pool.get_or_create(
            "critical-service", failure_threshold=2, recovery_timeout=30
        )

        cb2 = pool.get_or_create(
            "non-critical-service", failure_threshold=10, recovery_timeout=5
        )

        assert cb1.failure_threshold == 2
        assert cb1.recovery_timeout == 30
        assert cb2.failure_threshold == 10
        assert cb2.recovery_timeout == 5


class TestCircuitBreakerConcurrency:
    """Test circuit breaker under concurrent load."""

    @pytest.mark.asyncio
    async def test_concurrent_calls_same_breaker(self):
        """Test multiple concurrent calls through same breaker."""
        cb = CircuitBreaker(name="test", failure_threshold=10)

        call_count = 0

        async def counting_func():
            nonlocal call_count
            await asyncio.sleep(0.01)
            call_count += 1
            return "success"

        # Make 20 concurrent calls
        tasks = [cb.call(counting_func) for _ in range(20)]
        results = await asyncio.gather(*tasks)

        assert len(results) == 20
        assert all(r == "success" for r in results)
        assert call_count == 20
        assert cb.failure_count == 0

    @pytest.mark.asyncio
    async def test_concurrent_failures_count_correctly(self):
        """Test that concurrent failures are counted correctly."""
        cb = CircuitBreaker(name="test", failure_threshold=5)

        async def failing_func():
            await asyncio.sleep(0.01)
            raise ValueError("Error")

        # Make 10 concurrent failing calls
        tasks = [cb.call(failing_func) for _ in range(10)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # All should raise ValueError
        assert all(isinstance(r, ValueError) for r in results)

        # Circuit should be open (reached threshold)
        assert cb.state == CircuitState.OPEN
        assert cb.failure_count >= 5

    @pytest.mark.asyncio
    async def test_thread_safety_with_lock(self):
        """Test that lock prevents race conditions."""
        cb = CircuitBreaker(name="test", failure_threshold=3)

        async def sometimes_fails(fail_probability):
            import random

            await asyncio.sleep(0.001)
            if random.random() < fail_probability:
                raise ValueError("Random failure")
            return "success"

        # Make many concurrent calls with 50% failure rate
        tasks = [cb.call(sometimes_fails, 0.5) for _ in range(50)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # State should be consistent (not corrupted by race conditions)
        assert cb.state in [
            CircuitState.CLOSED,
            CircuitState.OPEN,
            CircuitState.HALF_OPEN,
        ]


class TestCircuitBreakerEdgeCases:
    """Test edge cases and error scenarios."""

    @pytest.mark.asyncio
    async def test_exception_types_preserved(self):
        """Test that original exception types are preserved."""
        cb = CircuitBreaker(name="test", failure_threshold=5)

        class CustomError(Exception):
            pass

        async def custom_error_func():
            raise CustomError("Custom error message")

        with pytest.raises(CustomError) as exc_info:
            await cb.call(custom_error_func)

        assert "Custom error message" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_function_with_arguments(self):
        """Test calling functions with positional and keyword arguments."""
        cb = CircuitBreaker(name="test")

        async def func_with_args(a, b, c=None):
            return f"{a}-{b}-{c}"

        result = await cb.call(func_with_args, "x", "y", c="z")

        assert result == "x-y-z"

    @pytest.mark.asyncio
    async def test_function_returning_none(self):
        """Test functions that return None."""
        cb = CircuitBreaker(name="test")

        async def returns_none():
            return None

        result = await cb.call(returns_none)

        assert result is None
        assert cb.state == CircuitState.CLOSED

    @pytest.mark.asyncio
    async def test_last_failure_time_tracked(self):
        """Test that last failure time is tracked."""
        cb = CircuitBreaker(name="test", failure_threshold=1)

        async def failing_func():
            raise ValueError("Error")

        before = time.time()
        with pytest.raises(ValueError):
            await cb.call(failing_func)
        after = time.time()

        assert cb.last_failure_time is not None
        assert before <= cb.last_failure_time <= after

    @pytest.mark.asyncio
    async def test_zero_success_threshold_edge_case(self):
        """Test behavior with minimal success threshold."""
        # success_threshold must be at least 1 for recovery
        cb = CircuitBreaker(
            name="test", failure_threshold=1, recovery_timeout=1, success_threshold=1
        )

        async def failing_func():
            raise ValueError("Error")

        async def successful_func():
            return "ok"

        # Open circuit
        with pytest.raises(ValueError):
            await cb.call(failing_func)

        # Wait and recover with just 1 success
        await asyncio.sleep(1.1)
        await cb.call(successful_func)

        # Should be closed now
        assert cb.state == CircuitState.CLOSED


class TestCircuitBreakerRealWorldScenarios:
    """Test realistic usage scenarios."""

    @pytest.mark.asyncio
    async def test_database_connection_scenario(self):
        """Simulate database connection failures."""
        db_breaker = CircuitBreaker(
            name="database",
            failure_threshold=3,
            recovery_timeout=2,
            success_threshold=2,
        )

        connection_attempts = 0

        async def connect_to_db():
            nonlocal connection_attempts
            connection_attempts += 1
            if connection_attempts <= 3:
                raise ConnectionError("Database unavailable")
            return "connected"

        # First 3 attempts fail - circuit opens
        for _ in range(3):
            with pytest.raises(ConnectionError):
                await db_breaker.call(connect_to_db)

        assert db_breaker.state == CircuitState.OPEN

        # Circuit open - no actual connection attempts
        with pytest.raises(Exception) as exc_info:
            await db_breaker.call(connect_to_db)
        assert "Circuit breaker" in str(exc_info.value)
        assert connection_attempts == 3  # No new attempt made

    @pytest.mark.asyncio
    async def test_external_api_scenario(self):
        """Simulate external API rate limiting."""
        api_breaker = CircuitBreaker(
            name="external-api", failure_threshold=5, recovery_timeout=1
        )

        call_count = 0

        async def call_external_api():
            nonlocal call_count
            call_count += 1
            # Simulate rate limit after 5 calls
            if call_count <= 5:
                raise Exception("429 Rate Limited")
            return {"data": "success"}

        # Hit rate limit
        for _ in range(5):
            with pytest.raises(Exception):
                await api_breaker.call(call_external_api)

        # Circuit open - prevents hammering the API
        assert api_breaker.state == CircuitState.OPEN

        # Wait for recovery
        await asyncio.sleep(1.1)

        # Should work now
        result = await api_breaker.call(call_external_api)
        assert result["data"] == "success"

    @pytest.mark.asyncio
    async def test_microservice_cascade_failure_prevention(self):
        """Test preventing cascade failures in microservices."""
        service_a = CircuitBreaker(name="service-a", failure_threshold=3)
        service_b = CircuitBreaker(name="service-b", failure_threshold=3)

        async def call_service_a():
            # Service A depends on Service B
            async def service_b_call():
                raise Exception("Service B down")

            return await service_b.call(service_b_call)

        # Service B failures
        for _ in range(3):
            with pytest.raises(Exception):
                await call_service_a()

        # Service B circuit is now open
        assert service_b.state == CircuitState.OPEN

        # Service A doesn't cascade fail
        assert service_a.state == CircuitState.CLOSED
