"""API routes for AI Question & Prompt Lab."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from aiseo.api.dependencies.container import (
    get_question_generator_service,
    get_reranker,
    get_ground_truth_validator,
)
from aiseo.application.analysis.question_generator import QuestionGeneratorService
from aiseo.domain.evaluation.ground_truth import GroundTruthValidationResult
from aiseo.domain.evaluation.rerank import SnippetPrediction
from aiseo.domain.intelligence.question import QuestionSet
from aiseo.ports.evaluation.ground_truth_port import GroundTruthPort
from aiseo.ports.retrieval.reranker_port import RerankerPort

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


class PredictSnippetRequest(BaseModel):
    question: str = Field(min_length=3)
    passages: list[str] = Field(min_length=1)
    brand: str | None = None


@router.post("/snippets/predict", response_model=SnippetPrediction)
async def predict_snippet(
    payload: PredictSnippetRequest,
    reranker: RerankerPort = Depends(get_reranker),
) -> SnippetPrediction:
    """Predict the optimal 40-60 word Featured Snippet candidate using BM25 and semantic reranking."""
    return await reranker.predict_aeo_snippet(
        question=payload.question,
        passages=payload.passages,
        brand=payload.brand,
    )


class VerifyGroundTruthRequest(BaseModel):
    domain: str
    brand: str
    keywords: list[str] = Field(default_factory=list)


@router.post("/verify/ground-truth", response_model=GroundTruthValidationResult)
async def verify_ground_truth(
    payload: VerifyGroundTruthRequest,
    validator: GroundTruthPort = Depends(get_ground_truth_validator),
) -> GroundTruthValidationResult:
    """Empirically validates domain & brand authority against live Google Suggest, Wikidata, and DuckDuckGo."""
    return await validator.verify_domain(
        domain=payload.domain,
        brand=payload.brand,
        keywords=payload.keywords,
    )
