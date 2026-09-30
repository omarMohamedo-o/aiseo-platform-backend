"""Circuit breaker pattern for external service calls."""
from __future__ import annotations

import logging
import time
from collections.abc import Awaitable, Callable
from enum import Enum
from typing import TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


class CircuitState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitBreakerOpenError(Exception):
    """Raised when an operation is attempted while the circuit is open."""


class CircuitBreaker:
    """Protects external systems from cascading failures by failing fast when unhealthy."""

    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout_seconds: float = 30.0,
        half_open_success_threshold: int = 2,
    ) -> None:
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout_seconds = recovery_timeout_seconds
        self.half_open_success_threshold = half_open_success_threshold

        self._state = CircuitState.CLOSED
        self._consecutive_failures = 0
        self._consecutive_successes = 0
        self._last_failure_time: float = 0.0

    @property
    def state(self) -> CircuitState:
        if self._state == CircuitState.OPEN:
            elapsed = time.monotonic() - self._last_failure_time
            if elapsed >= self.recovery_timeout_seconds:
                logger.info(
                    f"CircuitBreaker '{self.name}' transitioning from OPEN to HALF_OPEN "
                    f"after {elapsed:.1f}s"
                )
                self._state = CircuitState.HALF_OPEN
                self._consecutive_successes = 0
        return self._state

    async def execute(self, func: Callable[[], Awaitable[T]]) -> T:
        current_state = self.state

        if current_state == CircuitState.OPEN:
            logger.warning(
                f"CircuitBreaker '{self.name}' is OPEN. Fast-failing execution."
            )
            raise CircuitBreakerOpenError(
                f"Circuit breaker '{self.name}' is open. Upstream service is temporarily unavailable."
            )

        try:
            result = await func()
            self._record_success()
            return result
        except Exception:
            self._record_failure()
            raise

    def _record_success(self) -> None:
        if self._state == CircuitState.HALF_OPEN:
            self._consecutive_successes += 1
            if self._consecutive_successes >= self.half_open_success_threshold:
                logger.info(
                    f"CircuitBreaker '{self.name}' recovered: transitioning to CLOSED"
                )
                self._state = CircuitState.CLOSED
                self._consecutive_failures = 0
        elif self._state == CircuitState.CLOSED:
            self._consecutive_failures = 0

    def _record_failure(self) -> None:
        self._last_failure_time = time.monotonic()
        self._consecutive_failures += 1

        if self._state == CircuitState.HALF_OPEN:
            logger.warning(
                f"CircuitBreaker '{self.name}' probe failed in HALF_OPEN: returning to OPEN"
            )
            self._state = CircuitState.OPEN
        elif self._consecutive_failures >= self.failure_threshold:
            logger.error(
                f"CircuitBreaker '{self.name}' failure threshold reached "
                f"({self._consecutive_failures}/{self.failure_threshold}): transitioning to OPEN"
            )
            self._state = CircuitState.OPEN
