"""Unit tests for resilience patterns: retry and circuit breaker."""
from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock

import pytest

from aiseo.infrastructure.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerOpenError,
    CircuitState,
)
from aiseo.infrastructure.resilience.retry import retry_async


@pytest.mark.asyncio
async def test_retry_async_succeeds_first_attempt() -> None:
    mock_func = AsyncMock(return_value="success")
    result = await retry_async(mock_func, max_retries=3, initial_delay=0.01)
    assert result == "success"
    assert mock_func.call_count == 1


@pytest.mark.asyncio
async def test_retry_async_retries_on_transient_failure_then_succeeds() -> None:
    mock_func = AsyncMock(side_effect=[ValueError("transient error"), "recovered"])
    result = await retry_async(
        mock_func,
        max_retries=2,
        initial_delay=0.01,
        retryable_exceptions=(ValueError,),
    )
    assert result == "recovered"
    assert mock_func.call_count == 2


@pytest.mark.asyncio
async def test_retry_async_fails_immediately_on_non_retryable_exception() -> None:
    mock_func = AsyncMock(side_effect=PermissionError("denied"))
    with pytest.raises(PermissionError):
        await retry_async(
            mock_func,
            max_retries=3,
            initial_delay=0.01,
            retryable_exceptions=(Exception,),
            non_retryable_exceptions=(PermissionError,),
        )
    assert mock_func.call_count == 1


def _get_state(cb: CircuitBreaker) -> CircuitState:
    return cb.state


@pytest.mark.asyncio
async def test_circuit_breaker_closed_to_open_transitions() -> None:
    breaker = CircuitBreaker(
        name="test-breaker",
        failure_threshold=3,
        recovery_timeout_seconds=0.1,
        half_open_success_threshold=1,
    )
    assert _get_state(breaker) == CircuitState.CLOSED

    # 3 failures trip the breaker
    for _ in range(3):
        with pytest.raises(RuntimeError):
            await breaker.execute(AsyncMock(side_effect=RuntimeError("upstream down")))

    assert _get_state(breaker) == CircuitState.OPEN

    # While OPEN, fast fails without invoking func
    mock_call = AsyncMock(return_value="ok")
    with pytest.raises(CircuitBreakerOpenError):
        await breaker.execute(mock_call)
    assert mock_call.call_count == 0

    # Wait for recovery timeout to transition to HALF_OPEN
    await asyncio.sleep(0.15)
    assert _get_state(breaker) == CircuitState.HALF_OPEN

    # Probe succeeds -> transitions to CLOSED
    success_call = AsyncMock(return_value="recovered")
    res = await breaker.execute(success_call)
    assert res == "recovered"
    assert _get_state(breaker) == CircuitState.CLOSED
