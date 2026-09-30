"""Structured logging configuration.

Routes through the stdlib `logging` module (handlers, levels, propagation,
and any log-aggregation integration all work normally) rather than writing
directly to stdout via structlog's PrintLogger.
"""

from __future__ import annotations

import logging
import logging.config

import structlog


def configure_logging(environment: str = "development") -> None:
    """Configure stdlib logging + structlog once, at process startup."""
    log_level = logging.DEBUG if environment == "development" else logging.INFO

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "formatter": "structured",
                }
            },
            "formatters": {
                "structured": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processor": (
                        structlog.dev.ConsoleRenderer()
                        if environment == "development"
                        else structlog.processors.JSONRenderer()
                    ),
                }
            },
            "root": {"handlers": ["default"], "level": log_level},
        }
    )

    shared_processors: list = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]

    structlog.configure(
        processors=shared_processors,
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name)
