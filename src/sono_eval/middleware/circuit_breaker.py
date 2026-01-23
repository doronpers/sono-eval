"""Circuit breaker pattern for resilient external service calls."""

import asyncio
import time
from enum import Enum
from typing import Any, Awaitable, Callable, Optional

from sono_eval.utils.logger import get_logger

logger = get_logger(__name__)


class CircuitState(str, Enum):
    """Circuit breaker states."""

    CLOSED = "closed"  # Operating normally
    OPEN = "open"  # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered


class CircuitBreaker:
    """Circuit breaker for handling service failures gracefully."""

    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        success_threshold: int = 2,
    ):
        """Initialize circuit breaker."""
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[float] = None
        self.lock = asyncio.Lock()

    async def call(self, func: Callable[..., Awaitable[Any]], *args: Any, **kwargs: Any) -> Any:
        """Execute function with circuit breaker protection."""
        async with self.lock:
            if self.state == CircuitState.OPEN:
                if time.time() - self.last_failure_time > self.recovery_timeout:
                    logger.info(f"Circuit breaker '{self.name}' transitioning to HALF_OPEN")
                    self.state = CircuitState.HALF_OPEN
                    self.success_count = 0
                else:
                    raise Exception(
                        f"Circuit breaker '{self.name}' is OPEN. Service is unavailable."
                    )

        try:
            result = await func(*args, **kwargs)

            async with self.lock:
                if self.state == CircuitState.HALF_OPEN:
                    self.success_count += 1
                    if self.success_count >= self.success_threshold:
                        logger.info(f"Circuit breaker '{self.name}' closed (recovered)")
                        self.state = CircuitState.CLOSED
                        self.failure_count = 0
                elif self.state == CircuitState.CLOSED:
                    self.failure_count = 0

            return result

        except Exception as e:
            async with self.lock:
                self.failure_count += 1
                self.last_failure_time = time.time()

                if self.state == CircuitState.HALF_OPEN:
                    logger.warning(f"Circuit breaker '{self.name}' reopening (recovery failed)")
                    self.state = CircuitState.OPEN
                    self.success_count = 0
                elif self.failure_count >= self.failure_threshold:
                    logger.error(
                        f"Circuit breaker '{self.name}' opened after {self.failure_count} failures"
                    )
                    self.state = CircuitState.OPEN

            raise e

    def get_state(self) -> str:
        """Get current circuit breaker state."""
        return self.state.value


class CircuitBreakerPool:
    """Pool of circuit breakers for different services."""

    def __init__(self):
        """Initialize circuit breaker pool."""
        self.breakers: dict[str, CircuitBreaker] = {}

    def get_or_create(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        success_threshold: int = 2,
    ) -> CircuitBreaker:
        """Get or create a circuit breaker."""
        if name not in self.breakers:
            self.breakers[name] = CircuitBreaker(
                name=name,
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                success_threshold=success_threshold,
            )
        return self.breakers[name]

    def get_status(self) -> dict[str, str]:
        """Get status of all circuit breakers."""
        return {name: breaker.get_state() for name, breaker in self.breakers.items()}


# Global circuit breaker pool
circuit_breaker_pool = CircuitBreakerPool()
