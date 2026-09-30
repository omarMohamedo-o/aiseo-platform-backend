"""API routes for AI model visibility simulation and answer analysis."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from aiseo.api.dependencies.container import (
    get_answer_analyzer_service,
    get_prompt_executor_service,
)
from aiseo.application.analysis.answer_analyzer import AnswerAnalyzerService
from aiseo.application.analysis.prompt_executor import (
    PromptExecutorService,
    ProviderExecutionResult,
)
from aiseo.domain.geo.answer_analysis import AnswerAnalysisResult

router = APIRouter(prefix="/api/v1/visibility", tags=["visibility"])


class ExecutePromptsRequest(BaseModel):
    providers: list[str] = Field(default_factory=lambda: ["openai", "gemini"])
    questions: list[str] = Field(min_length=1)
    system_prompt: str | None = None


class AnalyzeAnswersRequest(BaseModel):
    brand: str
    items: list[dict[str, Any]]


@router.post("/prompts/execute", response_model=list[ProviderExecutionResult])
async def execute_prompts(
    payload: ExecutePromptsRequest,
    service: PromptExecutorService = Depends(get_prompt_executor_service),
) -> list[ProviderExecutionResult]:
    return await service.execute_matrix(
        providers=payload.providers,
        questions=payload.questions,
        system_prompt=payload.system_prompt,
    )


@router.post("/answers/analyze", response_model=list[AnswerAnalysisResult])
async def analyze_answers(
    payload: AnalyzeAnswersRequest,
    service: AnswerAnalyzerService = Depends(get_answer_analyzer_service),
) -> list[AnswerAnalysisResult]:
    return await service.analyze_answers(
        brand=payload.brand,
        items=payload.items,
    )
