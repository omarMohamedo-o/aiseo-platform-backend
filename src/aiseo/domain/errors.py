"""Explicit internal error hierarchy. Provider/framework exceptions are normalized
into these at the adapter boundary; business code only ever sees these types."""
from __future__ import annotations


class AiseoError(Exception):
    """Base class for all platform errors."""


class InvalidUrlError(AiseoError):
    pass


class WebsiteNotFoundError(AiseoError):
    pass


class UnauthorizedTenantAccessError(AiseoError):
    pass


class CrawlLimitExceededError(AiseoError):
    pass


class ProviderError(AiseoError):
    """Base class for normalized provider errors."""


class ProviderUnavailableError(ProviderError):
    pass


class ProviderRateLimitError(ProviderError):
    pass


class ProviderTimeoutError(ProviderError):
    pass


class ProviderAuthenticationError(ProviderError):
    pass


class InvalidModelOutputError(AiseoError):
    pass


class InvalidEmbeddingError(AiseoError):
    pass


class UnsupportedLanguageError(AiseoError):
    pass
