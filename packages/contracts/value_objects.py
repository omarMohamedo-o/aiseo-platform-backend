"""Strong, immutable value objects. Invalid states cannot enter the domain."""

from __future__ import annotations

import re
import uuid
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, field_validator

from aiseo.domain.errors import InvalidUrlError

_LANGUAGE_CODE_RE = re.compile(r"^[a-z]{2}(-[A-Z]{2})?$")


class ValueObject(BaseModel):
    """Base class for immutable, validated value objects."""

    model_config = ConfigDict(frozen=True, extra="forbid")


class TenantId(ValueObject):
    value: uuid.UUID


class WebsiteId(ValueObject):
    value: uuid.UUID


class PageId(ValueObject):
    value: uuid.UUID


class CrawlJobId(ValueObject):
    value: uuid.UUID


class Url(ValueObject):
    value: str

    @field_validator("value")
    @classmethod
    def _validate_url(cls, raw: str) -> str:
        parsed = urlparse(raw)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise InvalidUrlError(f"Invalid URL: {raw!r}")
        return raw

    @property
    def domain(self) -> str:
        return urlparse(self.value).netloc


class DomainName(ValueObject):
    value: str

    @field_validator("value")
    @classmethod
    def _validate_domain(cls, raw: str) -> str:
        if not raw or " " in raw or "." not in raw:
            raise InvalidUrlError(f"Invalid domain name: {raw!r}")
        return raw.lower()


class Score(ValueObject):
    """A normalized score in [0, 100]."""

    value: float

    @field_validator("value")
    @classmethod
    def _validate_range(cls, v: float) -> float:
        if not (0.0 <= v <= 100.0):
            raise ValueError(f"Score must be within [0, 100], got {v}")
        return round(v, 2)


class Keyword(ValueObject):
    text: str

    @field_validator("text")
    @classmethod
    def _normalize(cls, v: str) -> str:
        normalized = v.strip().lower()
        if not normalized:
            raise ValueError("Keyword text must not be empty")
        return normalized


class LanguageCode(ValueObject):
    value: str

    @field_validator("value")
    @classmethod
    def _validate(cls, v: str) -> str:
        if not _LANGUAGE_CODE_RE.match(v):
            raise ValueError(f"Invalid language code: {v!r}")
        return v


class CountryCode(ValueObject):
    value: str

    @field_validator("value")
    @classmethod
    def _validate(cls, v: str) -> str:
        if len(v) != 2 or not v.isalpha():
            raise ValueError(f"Invalid ISO-3166 alpha-2 country code: {v!r}")
        return v.upper()


class CrawlDepth(ValueObject):
    value: int

    @field_validator("value")
    @classmethod
    def _validate(cls, v: int) -> int:
        if v < 0:
            raise ValueError("CrawlDepth must be >= 0")
        return v


class TokenCount(ValueObject):
    value: int

    @field_validator("value")
    @classmethod
    def _validate(cls, v: int) -> int:
        if v < 0:
            raise ValueError("TokenCount must be >= 0")
        return v
