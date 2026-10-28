"""Application service for analyzing AI model answers for brand mentions, sentiment, citations, and scores."""
from __future__ import annotations

import json
import re
from typing import Any

from pydantic import BaseModel, Field

from aiseo.adapters.evaluation.grounding_guard_adapter import GroundingGuardAdapter
from aiseo.domain.geo.answer_analysis import AnswerAnalysisResult, SentimentType
from aiseo.ports.evaluation.grounding_guard_port import GroundingGuardPort
from aiseo.ports.llm.llm_provider import LlmProvider, LlmRequest

_URL_REGEX = re.compile(r"https?://[^\s)\]}>,]+")


def extract_urls_from_text(text: str) -> list[str]:
    """Extract and normalize all HTTP/HTTPS links from raw response text."""
    matches = _URL_REGEX.findall(text)
    cleaned = [re.sub(r"[.,;:]+$", "", u) for u in matches]
    return list(dict.fromkeys(cleaned))[:20]


def analyze_deterministic(
    prompt_run_id: str,
    provider: str,
    question: str,
    answer: str,
    brand: str,
    provider_citations: list[str] | None = None,
    source_context: str | list[str] | None = None,
    grounding_guard: GroundingGuardPort | None = None,
) -> AnswerAnalysisResult:
    """Fast deterministic rule-based analysis used as baseline and fallback."""
    answer_clean = answer or ""
    lower_answer = answer_clean.lower()
    lower_brand = brand.strip().lower()

    brand_index = lower_answer.find(lower_brand) if lower_brand else -1
    brand_mentioned = brand_index >= 0

    mention_position = None
    if brand_mentioned:
        mention_position = max(1, len(answer_clean[:brand_index].strip().split()))

    extracted_citations = list(
        dict.fromkeys((provider_citations or []) + extract_urls_from_text(answer_clean))
    )[:20]

    # Evaluate factual grounding and hallucination metrics via GroundingGuard
    guard = grounding_guard or GroundingGuardAdapter()
    metrics = guard.verify_grounding(
        answer=answer_clean,
        source_context=source_context or "",
        brand=brand,
    )

    # Deterministic visibility score (0-100)
    score = 0
    if brand_mentioned:
        score += 55
    score += min(25, len(extracted_citations) * 5)
    if brand_mentioned and brand_index < 120:
        score += 20
    # Penalty if hallucinated claims detected
    if metrics.is_hallucinated:
        score = max(0, score - 25)
    score = max(0, min(100, score))

    # Basic sentiment heuristic
    positive_words = ["best", "leading", "recommend", "great", "excellent", "top", "reliable"]
    negative_words = ["avoid", "drawback", "poor", "expensive", "issue", "bug", "worse"]
    pos_count = sum(1 for w in positive_words if w in lower_answer)
    neg_count = sum(1 for w in negative_words if w in lower_answer)

    sentiment: SentimentType = "neutral"
    if pos_count > neg_count and pos_count > 0:
        sentiment = "positive"
    elif neg_count > pos_count and neg_count > 0:
        sentiment = "negative"
    elif pos_count > 0 and neg_count > 0:
        sentiment = "mixed"

    summary = (
        f"{brand} was cited and mentioned favorably in the {provider} answer."
        if brand_mentioned
        else f"{brand} was not mentioned in the {provider} response."
    )

    return AnswerAnalysisResult(
        prompt_run_id=prompt_run_id,
        provider=provider,
        question=question,
        brand=brand,
        brand_mentioned=brand_mentioned,
        mention_position=mention_position,
        competitors=[],
        extracted_citations=extracted_citations,
        sentiment=sentiment,
        visibility_score=score,
        summary=summary,
        analysis_model="deterministic",
        hallucination_score=metrics.hallucination_score,
        faithfulness_ratio=metrics.grounding_ratio,
        grounding_status=metrics.status,
        unverified_claims=metrics.unverified_claims,
    )


class _SingleAnalysisSchema(BaseModel):
    index: int
    brand_mentioned: bool
    mention_position: int | None = None
    competitors: list[str] = Field(default_factory=list)
    extracted_citations: list[str] = Field(default_factory=list)
    sentiment: SentimentType = "neutral"
    visibility_score: int = Field(ge=0, le=100)
    summary: str


class _AnalysisBatchSchema(BaseModel):
    analyses: list[_SingleAnalysisSchema] = Field(default_factory=list)


class AnswerAnalyzerService:
    """Orchestrates comprehensive evidence extraction across multi-model AI responses."""

    SYSTEM_PROMPT = (
        "You are an evidence analyst for AI visibility and Generative Engine Optimization (GEO). "
        "Analyze only what is explicitly present in each answer. Do not hallucinate competitors or citations. "
        "Return a JSON object containing an 'analyses' array."
    )

    def __init__(
        self,
        llm_provider: LlmProvider | None = None,
        grounding_guard: GroundingGuardPort | None = None,
    ) -> None:
        self._llm = llm_provider
        self._guard = grounding_guard or GroundingGuardAdapter()

    async def analyze_answers(
        self,
        brand: str,
        items: list[dict[str, Any]],
    ) -> list[AnswerAnalysisResult]:
        """Analyze a batch of model responses for a given brand.

        Items format: [{'prompt_run_id': str, 'provider': str, 'question': str, 'answer': str, 'citations': list[str], 'source_context': str | list[str]}]
        """
        results: list[AnswerAnalysisResult] = []
        deterministic_map: dict[int, AnswerAnalysisResult] = {}

        for idx, item in enumerate(items):
            context = item.get("source_context") or item.get("context")
            det = analyze_deterministic(
                prompt_run_id=str(item.get("prompt_run_id", idx)),
                provider=item.get("provider", "unknown"),
                question=item.get("question", ""),
                answer=item.get("answer", ""),
                brand=brand,
                provider_citations=item.get("citations", []),
                source_context=context,
                grounding_guard=self._guard,
            )
            deterministic_map[idx] = det

        if not self._llm or not items:
            return list(deterministic_map.values())

        # Attempt deep LLM analysis
        try:
            payload = {
                "brand": brand,
                "answers": [
                    {
                        "index": idx,
                        "provider": item.get("provider"),
                        "question": item.get("question"),
                        "answer": item.get("answer"),
                        "citations": item.get("citations", []),
                    }
                    for idx, item in enumerate(items)
                ],
            }

            req = LlmRequest(
                prompt=json.dumps(payload),
                system=self.SYSTEM_PROMPT,
                temperature=0.0,
                max_tokens=2048,
            )

            structured = await self._llm.generate_structured(req, _AnalysisBatchSchema)
            llm_results_by_index = {a.index: a for a in structured.analyses}

            for idx, item in enumerate(items):
                base = deterministic_map[idx]
                llm_analysis = llm_results_by_index.get(idx)
                if not llm_analysis:
                    results.append(base)
                    continue

                all_citations = list(
                    dict.fromkeys(base.extracted_citations + llm_analysis.extracted_citations)
                )[:20]

                results.append(
                    AnswerAnalysisResult(
                        prompt_run_id=base.prompt_run_id,
                        provider=base.provider,
                        question=base.question,
                        brand=brand,
                        brand_mentioned=llm_analysis.brand_mentioned,
                        mention_position=llm_analysis.mention_position or base.mention_position,
                        competitors=llm_analysis.competitors[:12],
                        extracted_citations=all_citations,
                        sentiment=llm_analysis.sentiment,
                        visibility_score=llm_analysis.visibility_score,
                        summary=llm_analysis.summary or base.summary,
                        analysis_model="llm-verified",
                        hallucination_score=base.hallucination_score,
                        faithfulness_ratio=base.faithfulness_ratio,
                        grounding_status=base.grounding_status,
                        unverified_claims=base.unverified_claims,
                    )
                )

            return results
        except Exception:
            return list(deterministic_map.values())
