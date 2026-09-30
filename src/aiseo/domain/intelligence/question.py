"""Domain models for AI-generated search questions and buyer intents."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

IntentType = Literal["informational", "commercial", "comparison", "implementation"]
FunnelStageType = Literal["awareness", "consideration", "decision"]


class GeneratedQuestion(BaseModel):
    """An approved or proposed question that real buyers would ask an AI."""

    model_config = ConfigDict(frozen=True)

    question: str
    intent: IntentType = "informational"
    funnel_stage: FunnelStageType = "awareness"
    rationale: str = ""


class QuestionSet(BaseModel):
    """A collection of questions generated for a specific topic, brand, and lens."""

    model_config = ConfigDict(frozen=True)

    topic: str
    keywords: list[str] = Field(default_factory=list)
    lens: str = "general"
    questions: list[GeneratedQuestion] = Field(default_factory=list)
