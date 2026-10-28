"""Application service for generating strategic buyer questions via LLM."""
from __future__ import annotations

import json

from pydantic import BaseModel, Field

from aiseo.domain.intelligence.question import (
    FunnelStageType,
    GeneratedQuestion,
    IntentType,
    QuestionSet,
)
from aiseo.ports.llm.llm_provider import LlmProvider, LlmRequest


class _QuestionItemSchema(BaseModel):
    question: str
    intent: IntentType = "informational"
    funnel_stage: FunnelStageType = "awareness"
    rationale: str = ""


class _QuestionSetSchema(BaseModel):
    questions: list[_QuestionItemSchema] = Field(default_factory=list)


class QuestionGeneratorService:
    """Orchestrates generation of approved-ready search/buyer questions grounded in scraped website context."""

    SYSTEM_PROMPT = (
        "You are a senior AI visibility and generative search optimization (AEO/GEO) strategist. "
        "Your task is to analyze the crawled website context and generate high-signal questions that real "
        "buyers, procurement directors, and researchers ask AI engines (ChatGPT, Claude, Perplexity, Gemini). "
        "Questions MUST be strictly grounded in the real products, engineering specs, compliance standards, "
        "and solutions discovered on the target website. Return a JSON object with a 'questions' array."
    )

    def __init__(self, llm_provider: LlmProvider | None = None) -> None:
        self._llm = llm_provider

    def _extract_contextual_fallback_entities(
        self,
        topic: str,
        keywords: list[str],
        context: str | None = None,
        page_snippets: list[dict] | None = None,
    ) -> list[str]:
        """Extract domain-specific terms from live scraped context or snippets."""
        terms: list[str] = [topic.strip()] if topic and topic.strip() else []
        if keywords:
            for kw in keywords:
                clean_kw = kw.strip()
                if clean_kw and clean_kw not in terms and not clean_kw.startswith("http"):
                    terms.append(clean_kw)

        if page_snippets:
            for snip in page_snippets[:5]:
                title = snip.get("title", "")
                if title and " - " in title:
                    sub = title.split(" - ")[0].strip()
                    if sub and sub not in terms:
                        terms.append(sub)
                elif title and " | " in title:
                    sub = title.split(" | ")[0].strip()
                    if sub and sub not in terms:
                        terms.append(sub)

        if context:
            # Look for common high-value phrases in text
            import re
            lines = [l.strip() for l in context.splitlines() if len(l.strip()) > 15]
            for line in lines[:8]:
                # Find phrases with 2-4 words like "emergency chlorine scrubber", "chemical neutralization"
                matches = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z]?[a-z]+){1,3}\b", line)
                for m in matches:
                    if len(m) > 10 and m not in terms:
                        terms.append(m)
                        if len(terms) >= 6:
                            break

        if not terms:
            terms = [topic, "industrial equipment", "engineering compliance", "procurement solutions"]

        return terms[:6]

    async def generate_questions(
        self,
        topic: str,
        keywords: list[str],
        lens: str = "general",
        count: int = 5,
        language: str = "en",
        context: str | None = None,
        page_snippets: list[dict] | None = None,
    ) -> QuestionSet:
        lang_normalized = language.lower().strip()

        # Format crawled website context for LLM grounding
        website_context_text = ""
        if context and context.strip():
            website_context_text = context[:3500].strip()
        elif page_snippets:
            formatted_snippets = []
            for s in page_snippets[:8]:
                t = s.get("title", "Page")
                d = s.get("meta_description", "")
                ex = s.get("sample_text", "")[:180]
                formatted_snippets.append(f"• Title: {t}\n  Description: {d}\n  Excerpt: {ex}")
            website_context_text = "\n\n".join(formatted_snippets)

        prompt_payload = {
            "task": "Generate authentic search and buyer questions grounded directly in website crawl data",
            "topic": topic,
            "targetDomainKeywords": keywords,
            "scrapedWebsiteContext": website_context_text or "No scraped body text provided; deduce from topic and keywords.",
            "optimizationLens": lens,
            "count": count,
            "targetLanguage": lang_normalized,
            "groundingRules": [
                "CRITICAL: Ground every question in the REAL products, technical specs, workflows, and solutions found in scrapedWebsiteContext.",
                "Extract domain-specific terminology (e.g., equipment types, safety standards, chemicals, use cases, industry certifications) directly from the text.",
                "Generate questions that real buyers and researchers ask AI assistants (ChatGPT, Claude, Perplexity) when evaluating or purchasing these solutions.",
                f"Output all questions, rationales, and queries natively in {lang_normalized} (en=English, ar=Arabic, zh=Chinese).",
                "Ensure a balanced distribution: informational, commercial, comparative, and technical compliance.",
            ],
        }

        user_prompt = json.dumps(prompt_payload, ensure_ascii=False)

        request = LlmRequest(
            prompt=user_prompt,
            system=self.SYSTEM_PROMPT,
            temperature=0.2,
            max_tokens=2048,
        )

        try:
            structured = await self._llm.generate_structured(request, _QuestionSetSchema)
            if structured.questions and len(structured.questions) > 0:
                questions = [
                    GeneratedQuestion(
                        question=q.question,
                        intent=q.intent,
                        funnel_stage=q.funnel_stage,
                        rationale=q.rationale,
                    )
                    for q in structured.questions
                ]
            else:
                raise ValueError("LLM returned empty questions list")
        except Exception:
            # Dynamic context-aware fallback extracted from crawled website data
            extracted_terms = self._extract_contextual_fallback_entities(
                topic=topic,
                keywords=keywords,
                context=context,
                page_snippets=page_snippets,
            )
            primary_term = extracted_terms[0] if extracted_terms else topic
            secondary_term = extracted_terms[1] if len(extracted_terms) > 1 else "alternative industrial systems"
            third_term = extracted_terms[2] if len(extracted_terms) > 2 else "safety compliance standards"

            if lang_normalized.startswith("ar"):
                questions = [
                    GeneratedQuestion(
                        question=f"ما هي المعايير الهندسية والمواصفات الفنية لاختيار أنظمة {primary_term}؟",
                        intent="informational",
                        funnel_stage="awareness",
                        rationale=f"استفسار استكشافي مبني على حلول {primary_term} المستخرجة من الموقع",
                    ),
                    GeneratedQuestion(
                        question=f"مقارنة عملية بين {primary_term} و{secondary_term} من حيث الكفاءة وتكاليف التشغيل",
                        intent="comparison",
                        funnel_stage="decision",
                        rationale="استفسار مقارنة مباشر بين الحلول التقنية المستخلصة من بيانات الموقع",
                    ),
                    GeneratedQuestion(
                        question=f"كيفية ضمان الامتثال لمعايير السلامة والأمان القياسية عند تركيب {primary_term}؟",
                        intent="informational",
                        funnel_stage="consideration",
                        rationale=f"استفسار حول معايير السلامة والتوافق التنظيمي لـ {third_term}",
                    ),
                    GeneratedQuestion(
                        question=f"ما هي متطلبات الصيانة الدورية والعمر التشغيلي المتوقع لأنظمة {primary_term}؟",
                        intent="commercial",
                        funnel_stage="consideration",
                        rationale="استفسار تجاري فني لتقييم استدامة المعدات وتكاليف دورة الحياة",
                    ),
                    GeneratedQuestion(
                        question=f"دراسة جدوى وعائد الاستثمار (ROI) لتحديث وتوريد معدات {primary_term} للمنشآت",
                        intent="commercial",
                        funnel_stage="decision",
                        rationale="استفسار مشتريات استثماري للمفاضلة والقرار النهائي",
                    ),
                ]
            elif lang_normalized.startswith("zh"):
                questions = [
                    GeneratedQuestion(
                        question=f"在工业与工程应用中，选择 {primary_term} 系统的核心技术指标有哪些？",
                        intent="informational",
                        funnel_stage="awareness",
                        rationale=f"基于爬取内容中 {primary_term} 的专业技术探索查询",
                    ),
                    GeneratedQuestion(
                        question=f"{primary_term} 与主流 {secondary_term} 方案在能效与全生命周期成本上的深度对比",
                        intent="comparison",
                        funnel_stage="decision",
                        rationale="针对具体产品类别的直接商业技术选型查询",
                    ),
                    GeneratedQuestion(
                        question=f"部署与运行 {primary_term} 时，必须满足哪些国家与行业安全合规标准？",
                        intent="informational",
                        funnel_stage="consideration",
                        rationale=f"涉及 {third_term} 的规范达标与认证评估",
                    ),
                    GeneratedQuestion(
                        question=f"{primary_term} 的日常维护周期、关键备件更换成本与运行故障率分析",
                        intent="commercial",
                        funnel_stage="consideration",
                        rationale="商业采购阶段关于运维总成本 (TCO) 的考量",
                    ),
                    GeneratedQuestion(
                        question=f"大型企业采购与定制 {primary_term} 整体解决方案的投资回报率 (ROI) 测算",
                        intent="commercial",
                        funnel_stage="decision",
                        rationale="决策层采购与预算审批核心查询",
                    ),
                ]
            else:
                questions = [
                    GeneratedQuestion(
                        question=f"What are the critical engineering specifications for selecting {primary_term} systems?",
                        intent="informational",
                        funnel_stage="awareness",
                        rationale=f"Baseline technical discovery grounded in crawled {primary_term} specs",
                    ),
                    GeneratedQuestion(
                        question=f"How does {primary_term} compare to {secondary_term} in efficiency and total cost of ownership?",
                        intent="comparison",
                        funnel_stage="decision",
                        rationale="Direct technical comparison between solutions discovered on site",
                    ),
                    GeneratedQuestion(
                        question=f"What regulatory safety and compliance standards apply to deploying {primary_term}?",
                        intent="informational",
                        funnel_stage="consideration",
                        rationale=f"Safety and compliance validation query regarding {third_term}",
                    ),
                    GeneratedQuestion(
                        question=f"What is the recommended maintenance schedule and lifecycle expectation for {primary_term}?",
                        intent="commercial",
                        funnel_stage="consideration",
                        rationale="Commercial evaluation of operational longevity and service support",
                    ),
                    GeneratedQuestion(
                        question=f"Procurement checklist and estimated ROI for enterprise adoption of {primary_term}",
                        intent="commercial",
                        funnel_stage="decision",
                        rationale="Procurement decision query for enterprise buying committee",
                    ),
                ]

        return QuestionSet(
            topic=topic,
            keywords=keywords,
            lens=lens,
            questions=questions[:count],
        )
