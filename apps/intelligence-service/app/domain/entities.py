"""Domain models for NLP features extracted from text."""

from __future__ import annotations

from pydantic import BaseModel


class Entity(BaseModel):
    """A named entity extracted from text (e.g., Company, Person, Product)."""

    name: str
    label: str
    confidence: float | None = None
    count: int = 1


class Keyword(BaseModel):
    """A significant keyword or keyphrase extracted from text."""

    term: str
    score: float | None = None
    frequency: int = 1
