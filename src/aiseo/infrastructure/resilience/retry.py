"""Async retry with exponential backoff and jitter."""
from __future__ import annotations

import asyncio
import logging
import random
from collections.abc import Awaitable, Callable
from typing import TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


async def retry_async(
    func: Callable[[], Awaitable[T]],
    *,
    max_retries: int = 3,
    initial_delay: float = 0.5,
    backoff_factor: float = 2.0,
    max_delay: float = 10.0,
    jitter: bool = True,
    retryable_exceptions: tuple[type[Exception], ...] = (Exception,),
    non_retryable_exceptions: tuple[type[Exception], ...] = (),
) -> T:
    """Execute an async function with exponential backoff retry.

    Deterministic/non-retryable exceptions fail immediately on first attempt.
    """
    delay = initial_delay
    last_exc: Exception | None = None

    for attempt in range(max_retries + 1):
        try:
            return await func()
        except non_retryable_exceptions:
            raise
        except retryable_exceptions as exc:
            last_exc = exc
            if attempt == max_retries:
                logger.warning(
                    f"All {max_retries + 1} attempts exhausted. Final failure: {exc}"
                )
                raise

            sleep_time = min(delay, max_delay)
            if jitter:
                sleep_time = sleep_time * (0.5 + random.random() * 0.5)

            logger.info(
                f"Attempt {attempt + 1} failed ({type(exc).__name__}: {exc}). "
                f"Retrying in {sleep_time:.2f}s..."
            )
            await asyncio.sleep(sleep_time)
            delay *= backoff_factor

    if last_exc:
        raise last_exc
    raise RuntimeError("Unexpected retry loop termination")
