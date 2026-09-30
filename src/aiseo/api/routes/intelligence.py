"""API routes for AI Question & Prompt Lab."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from aiseo.api.dependencies.container import get_question_generator_service
from aiseo.application.analysis.question_generator import QuestionGeneratorService
from aiseo.domain.intelligence.question import QuestionSet

router = APIRouter(prefix="/api/v1/intelligence", tags=["intelligence"])


class GenerateQuestionsRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=200)
    keywords: list[str] = Field(default_factory=list)
    lens: str = "general"
    count: int = Field(default=5, ge=1, le=20)
    context: str | None = None
    language: str = "en"


@router.post("/questions/generate", response_model=QuestionSet)
async def generate_questions(
    payload: GenerateQuestionsRequest,
    service: QuestionGeneratorService = Depends(get_question_generator_service),
) -> QuestionSet:
    return await service.generate_questions(
        topic=payload.topic,
        keywords=payload.keywords,
        lens=payload.lens,
        count=payload.count,
        language=payload.language,
        context=payload.context,
    )
