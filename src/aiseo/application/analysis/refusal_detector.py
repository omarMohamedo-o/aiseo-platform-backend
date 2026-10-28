"""AI Engine Refusal and Commercial Deflection Classifier.

Detects when an AI generative engine (OpenAI ChatGPT, Anthropic Claude, Google Gemini,
or Perplexity) deflects a commercial or comparative brand query due to safety/policy
guardrails rather than true market absence.

Categorizing deflections prevents false-negative GEO visibility penalization.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import enum
import re
from dataclasses import dataclass
from typing import ClassVar


class RefusalCategory(str, enum.Enum):
    """Classification of AI engine refusal behaviors."""
    COMMERCIAL_POLICY = "commercial_policy"
    NEUTRALITY_DISCLAIMER = "neutrality_disclaimer"
    KNOWLEDGE_CUTOFF = "knowledge_cutoff"
    NONE = "none"


@dataclass(frozen=True)
class RefusalAnalysisResult:
    """Detailed verdict of AI engine deflection analysis."""
    is_refusal: bool
    category: RefusalCategory
    confidence: float
    detected_phrases: list[str]
    explanation: str
    rephrase_guidance: str | None


class RefusalDetector:
    """Enterprise classifier for AI model guardrail deflections and policy refusals."""

    _PATTERNS: ClassVar[list[tuple[RefusalCategory, list[re.Pattern[str]]]]] = [
        (
            RefusalCategory.COMMERCIAL_POLICY,
            [
                re.compile(r"as an ai(?: language model)?,? I (?:do not|cannot).*?(?:endorse|promote|recommend).*?(?:products|vendors|companies|brands)", re.IGNORECASE),
                re.compile(r"I (?:am not able to|cannot).*?recommend.*?specific (?:vendors|companies|brands)", re.IGNORECASE),
                re.compile(r"policy prevents me from endorsing or ranking specific proprietary solutions", re.IGNORECASE),
                re.compile(r"كنموذج (?:لغوي|ذكاء اصطناعي).*?لا (?:أستطيع|استطيع|يمكنني).*?(?:تفضيل|ترشيح|ترويج).*?(?:شركات|منتجات|علامات تجارية)", re.IGNORECASE | re.DOTALL),
                re.compile(r"لا (?:أقدم|اقدم) توصيات تجارية لشركات محددة", re.IGNORECASE),
            ],
        ),
        (
            RefusalCategory.NEUTRALITY_DISCLAIMER,
            [
                re.compile(r"I (?:strive|aim) to (?:remain|be) neutral and (?:do not|cannot) take sides between (?:competing )?(?:brands|vendors)", re.IGNORECASE),
                re.compile(r"as a neutral ai assistant, I do not favor any single company", re.IGNORECASE),
                re.compile(r"أنا نموذج ذكاء اصطناعي محايد ولا أفضل شركة على أخرى", re.IGNORECASE),
            ],
        ),
        (
            RefusalCategory.KNOWLEDGE_CUTOFF,
            [
                re.compile(r"my knowledge (?:cutoff|is limited to) (?:prevent|means) I cannot verify current (?:market )?availability", re.IGNORECASE),
                re.compile(r"I do not have access to real-time (?:market data|pricing|vendor catalogs)", re.IGNORECASE),
                re.compile(r"ليس لدي وصول إلى بيانات السوق الحالية أو الأسعار المباشرة", re.IGNORECASE),
            ],
        ),
    ]

    @classmethod
    def analyze(cls, text: str) -> RefusalAnalysisResult:
        """Classifies text into refusal categories with remediation prompt guidance."""
        if not text or len(text.strip()) < 10:
            return RefusalAnalysisResult(
                is_refusal=False,
                category=RefusalCategory.NONE,
                confidence=0.0,
                detected_phrases=[],
                explanation="Input too short to evaluate refusal.",
                rephrase_guidance=None,
            )

        detected_phrases: list[str] = []

        for category, patterns in cls._PATTERNS:
            for pattern in patterns:
                matches = pattern.findall(text)
                if matches:
                    matched_str = matches[0] if isinstance(matches[0], str) else str(matches[0])
                    detected_phrases.append(matched_str)
                    
                    guidance = (
                        "Rephrase your prompt from direct brand endorsement to objective technical "
                        "specifications, industry standard comparisons, or third-party benchmark evaluations."
                    )
                    
                    return RefusalAnalysisResult(
                        is_refusal=True,
                        category=category,
                        confidence=0.95,
                        detected_phrases=detected_phrases,
                        explanation=f"AI engine deflected evaluation under '{category.value}' guardrail.",
                        rephrase_guidance=guidance,
                    )

        return RefusalAnalysisResult(
            is_refusal=False,
            category=RefusalCategory.NONE,
            confidence=0.90,
            detected_phrases=[],
            explanation="Response is substantive with no guardrail refusal detected.",
            rephrase_guidance=None,
        )
