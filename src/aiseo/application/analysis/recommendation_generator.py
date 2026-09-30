"""Application service for generating website-specific strategic recommendations via LLM."""
from __future__ import annotations

import json

from pydantic import BaseModel, Field

from aiseo.ports.llm.llm_provider import LlmProvider, LlmRequest


class _RecommendationItemSchema(BaseModel):
    category: str = ""
    title: str = ""
    impact: str = "High"
    description: str = ""
    action_items: list[str] = Field(default_factory=list)


class _RecommendationSetSchema(BaseModel):
    recommendations: list[_RecommendationItemSchema] = Field(default_factory=list)


# ------------------------------------------------------------------
# Benchmark data from the global leaderboard — what top websites do
# ------------------------------------------------------------------
TOP_WEBSITE_BENCHMARKS = {
    "common_traits": [
        "Schema.org JSON-LD on every page (Organization, Product, Service, FAQ, HowTo, BreadcrumbList)",
        "OpenGraph + Twitter Card meta tags on every single page",
        "Unique meta descriptions (150-160 chars) on every page",
        "H1 heading on every page with clear, descriptive text",
        "Proper heading hierarchy (H1 → H2 → H3) on every page",
        "FAQ/Q&A sections with direct-answer snippets on service/product pages",
        "Brand name mentioned in first 100 characters of every page",
        "Rich content depth: 800-2000+ words per service/product page",
        "Internal linking structure with 5-10+ contextual cross-links per page",
        "Canonical URLs on every page to prevent duplicate content",
        "Mobile-responsive viewport meta tag",
        "HTML lang attribute set correctly",
        "Image alt text on every image (descriptive, keyword-rich)",
        "sitemap.xml with all pages listed and up-to-date",
        "robots.txt properly configured",
        "Page load time under 3 seconds",
        "Breadcrumb navigation with BreadcrumbList schema",
        "Author/expertise signals (About page, team bios, credentials)",
        "Structured comparison tables and specification sheets",
        "Case studies, testimonials, and social proof content",
        "Regular content updates (freshness signals)",
        "Multi-language/hreflang support where applicable",
    ],
    "top_performers": [
        {"name": "FastAPI", "domain": "fastapi.tiangolo.com", "visibility": 98, "schema_score": 99, "direct_answer_score": 97},
        {"name": "Stripe Docs", "domain": "docs.stripe.com", "visibility": 97, "schema_score": 98, "direct_answer_score": 96},
        {"name": "MDN Web Docs", "domain": "developer.mozilla.org", "visibility": 96, "schema_score": 96, "direct_answer_score": 95},
        {"name": "Cloudflare", "domain": "cloudflare.com", "visibility": 94, "schema_score": 95, "direct_answer_score": 93},
        {"name": "AWS", "domain": "aws.amazon.com", "visibility": 92, "schema_score": 90, "direct_answer_score": 91},
    ],
    "industry_averages": {
        "Developer Tools": {"avg_visibility": 92, "avg_schema": 94, "avg_direct_answer": 93},
        "FinTech": {"avg_visibility": 84, "avg_schema": 90, "avg_direct_answer": 88},
        "E-Commerce": {"avg_visibility": 79, "avg_schema": 87, "avg_direct_answer": 82},
        "Cloud & Security": {"avg_visibility": 88, "avg_schema": 92, "avg_direct_answer": 90},
        "Engineering & Industry": {"avg_visibility": 76, "avg_schema": 80, "avg_direct_answer": 78},
        "Healthcare & Biotech": {"avg_visibility": 68, "avg_schema": 75, "avg_direct_answer": 72},
    },
}


class RecommendationGeneratorService:
    """Generates website-specific strategic AEO/GEO recommendations grounded in actual crawled data."""

    SYSTEM_PROMPT = (
        "You are a senior AI Engine Optimization (AEO) and Generative Engine Optimization (GEO) consultant. "
        "You analyze crawled website data and generate specific, actionable strategic recommendations to improve "
        "that website's visibility in AI-powered search engines (ChatGPT, Claude, Perplexity, Gemini). "
        "Your recommendations must be grounded in the ACTUAL content, structure, and technical signals found on the website. "
        "Never give generic advice — every recommendation must reference specific findings from the crawl data. "
        "You benchmark against what the world's top-performing websites do (like FastAPI docs, Stripe docs, MDN, Cloudflare). "
        "Return a JSON object with a 'recommendations' array. "
        "IMPORTANT: Return ALL applicable recommendations (at least 6-12), covering every area where the website falls short "
        "compared to top performers. Do NOT limit yourself to just 2-3 recommendations."
    )

    def __init__(self, llm_provider: LlmProvider) -> None:
        self._llm = llm_provider

    async def generate_recommendations(
        self,
        brand: str,
        domain: str,
        language: str,
        technical_signals: dict,
        page_summaries: list[dict],
        overall_visibility_score: int,
        overall_opportunity_score: int,
    ) -> list[dict]:
        """Generate website-specific strategic recommendations from crawled data.

        Args:
            brand: The brand/company name
            domain: The website domain
            language: Target language for output (en, ar, zh)
            technical_signals: Dict of boolean flags for detected technical SEO signals
            page_summaries: List of dicts with per-page audit data
            overall_visibility_score: The site-wide visibility score
            overall_opportunity_score: The site-wide opportunity score

        Returns:
            List of recommendation dicts with category, title, impact, description, action_items
        """
        lang_normalized = language.lower().strip()

        # Build a rich context from crawled data
        signal_summary = self._format_signals(technical_signals)
        pages_context = self._format_pages(page_summaries[:8])

        prompt_payload = {
            "task": (
                "Generate a COMPREHENSIVE list of specific, actionable AEO/GEO strategic recommendations "
                "based on the crawled website audit data below. Compare against what top-performing websites do "
                "and suggest ALL improvements needed to match their level."
            ),
            "brand": brand,
            "domain": domain,
            "overallVisibilityScore": overall_visibility_score,
            "overallOpportunityScore": overall_opportunity_score,
            "technicalSignalsDetected": technical_signals,
            "technicalSignalsSummary": signal_summary,
            "crawledPageSummaries": pages_context,
            "targetLanguage": lang_normalized,
            "topWebsiteBenchmarks": {
                "description": "What the top-performing websites in our global leaderboard all do well",
                "common_traits": TOP_WEBSITE_BENCHMARKS["common_traits"],
                "top_performers": TOP_WEBSITE_BENCHMARKS["top_performers"],
            },
            "rules": [
                "Return ALL critical and high-priority recommendations. You MUST generate at least 6-12 recommendations covering EVERY gap found.",
                "Each recommendation MUST reference specific findings from the audit data (e.g. 'Your site is missing Schema.org markup on 4 of 6 pages').",
                "BENCHMARK against top performers: compare the website's signals against what FastAPI (98%), Stripe (97%), MDN (96%) achieve and explain what they do differently.",
                "Cover ALL these categories if applicable: Structured Data, Content Depth, FAQ & Direct Answers, Entity Authority & Brand Identity, Social Meta Tags, Technical SEO, Internal Linking, Content Freshness, Performance, Accessibility, Multilingual Readiness.",
                "Set impact to 'Critical' for blockers (missing Schema, missing meta descriptions, no FAQ content, thin content) and 'High' for important improvements.",
                "Action items must be concrete and implementable (e.g. 'Add JSON-LD Organization schema to the homepage at /' or 'Add 5-8 FAQ Q&A pairs to each of the 6 service pages').",
                f"Write all output natively in the target language: {lang_normalized} (en=English, ar=Arabic, zh=Chinese).",
                "Do NOT give generic SEO advice. Every point must be specific to THIS website's crawl data.",
                "Include recommendations about content strategy: what types of pages to add, what topics to cover, comparison pages, how-to guides, etc.",
                "Include recommendations about authority signals: About page, team expertise, certifications, case studies, testimonials.",
            ],
        }

        user_prompt = json.dumps(prompt_payload, ensure_ascii=False)

        request = LlmRequest(
            prompt=user_prompt,
            system=self.SYSTEM_PROMPT,
            temperature=0.25,
            max_tokens=4000,
        )

        try:
            structured = await self._llm.generate_structured(request, _RecommendationSetSchema)
            if structured.recommendations and len(structured.recommendations) > 0:
                llm_recs = [
                    {
                        "category": r.category,
                        "title": r.title,
                        "impact": r.impact,
                        "description": r.description,
                        "action_items": r.action_items,
                    }
                    for r in structured.recommendations[:15]
                ]
                # Supplement with any signal-based gaps the LLM may have missed
                fallback_recs = self._build_signal_based_fallback(
                    brand, technical_signals, page_summaries, lang_normalized
                )
                # Merge: add fallback recs whose categories aren't already covered by LLM
                llm_categories = {r["category"].lower().strip() for r in llm_recs}
                for fb_rec in fallback_recs:
                    if fb_rec["category"].lower().strip() not in llm_categories:
                        llm_recs.append(fb_rec)
                return llm_recs
            raise ValueError("LLM returned empty recommendations list")
        except Exception:
            # Context-aware fallback based on actual technical signals
            return self._build_signal_based_fallback(
                brand, technical_signals, page_summaries, lang_normalized
            )

    def _format_signals(self, signals: dict) -> str:
        """Format technical signals into a human-readable summary."""
        lines = []
        signal_labels = {
            "has_schema_org": "Schema.org JSON-LD",
            "has_opengraph": "OpenGraph Meta Tags",
            "has_twitter_cards": "Twitter Card Meta Tags",
            "has_meta_description": "Meta Description",
            "has_h1": "H1 Heading",
            "has_heading_hierarchy": "Proper Heading Hierarchy (H1→H2→H3)",
            "has_faq_content": "FAQ / Q&A Structured Content",
            "has_sitemap": "XML Sitemap (sitemap.xml)",
            "has_robots_txt": "Robots.txt",
            "has_canonical": "Canonical URL Tag",
            "has_lang_attr": "HTML lang Attribute",
            "has_viewport": "Mobile Viewport Meta",
            "has_alt_text": "Image Alt Text",
            "brand_in_first_100_chars": "Brand Name in First 100 Characters",
        }
        for key, label in signal_labels.items():
            val = signals.get(key, False)
            coverage = signals.get(key.replace("has_", "") + "_coverage", "")
            status = "✅ Present" if val else "❌ Missing"
            line = f"  {label}: {status}"
            if coverage:
                line += f" ({coverage})"
            lines.append(line)

        # Add score summaries
        for score_key in ["avg_seo_score", "avg_aeo_score", "avg_geo_score", "avg_glmm_score"]:
            val = signals.get(score_key, 0)
            lines.append(f"  {score_key}: {val}%")

        return "\n".join(lines)

    def _format_pages(self, pages: list[dict]) -> str:
        """Format page summaries into context text."""
        lines = []
        for p in pages:
            path = p.get("path", "/")
            vis = p.get("visibility_score", 0)
            chars = p.get("characters_count", 0)
            brand = "✅" if p.get("brand_mentioned") else "❌"
            recs = p.get("recommendations", [])
            lines.append(
                f"  • {path} — Visibility: {vis}%, Chars: {chars}, Brand: {brand}, "
                f"Issues: {'; '.join(recs[:2]) if recs else 'None detected'}"
            )
        return "\n".join(lines)

    def _build_signal_based_fallback(
        self,
        brand: str,
        signals: dict,
        pages: list[dict],
        lang: str,
    ) -> list[dict]:
        """Build comprehensive recommendations from actual technical signals and benchmark gaps."""
        recs: list[dict] = []
        total_pages = len(pages) if pages else 1

        # Helper for trilingual text
        def t(en: str, ar: str, zh: str) -> str:
            if lang.startswith("ar"):
                return ar
            elif lang.startswith("zh"):
                return zh
            return en

        # =====================================================================
        # 1. Missing Schema.org JSON-LD
        # =====================================================================
        if not signals.get("has_schema_org"):
            pages_missing = [p.get("path", "/") for p in pages if not p.get("has_schema_org", False)]
            paths_text = ", ".join(pages_missing[:5]) if pages_missing else "all pages"
            recs.append({
                "category": t("Structured Data", "البيانات المنظمة", "结构化数据"),
                "title": t(
                    f"Add Schema.org JSON-LD markup to: {paths_text}",
                    f"إضافة مخططات Schema.org JSON-LD على: {paths_text}",
                    f"在以下页面添加 Schema.org JSON-LD: {paths_text}",
                ),
                "impact": "Critical",
                "description": t(
                    f"No Schema.org structured data was detected on {brand}'s website. Top-performing sites like FastAPI (schema score: 99%) and Stripe (98%) implement JSON-LD on every page. AI search engines rely heavily on structured data to understand your site's entities.",
                    f"لم يتم اكتشاف أي بيانات منظمة Schema.org على موقع {brand}. المواقع الرائدة مثل FastAPI (99%) و Stripe (98%) تستخدم JSON-LD في كل صفحة.",
                    f"未在 {brand} 网站上检测到 Schema.org 结构化数据。顶级网站如 FastAPI (99%) 和 Stripe (98%) 在每个页面都实施了 JSON-LD。",
                ),
                "action_items": [
                    t(f"Add JSON-LD Organization schema to the homepage with {brand}'s name, address, and contact info",
                      f"إضافة JSON-LD Organization schema على الصفحة الرئيسية تتضمن اسم {brand} والعنوان ومعلومات الاتصال",
                      f"在首页添加 JSON-LD Organization schema，包含 {brand} 名称、地址和联系方式"),
                    t("Add Product or Service JSON-LD to each service/product page",
                      "إضافة JSON-LD لكل صفحة خدمة/منتج مع نوع Product أو Service",
                      "为每个服务/产品页面添加 Product 或 Service 类型的 JSON-LD"),
                    t("Add FAQ Schema to pages that contain Q&A content",
                      "إضافة FAQ Schema للصفحات التي تحتوي على أسئلة وأجوبة",
                      "为包含问答内容的页面添加 FAQ Schema"),
                    t("Add BreadcrumbList schema for navigation breadcrumbs",
                      "إضافة BreadcrumbList schema للتنقل المنظم",
                      "添加 BreadcrumbList schema 用于面包屑导航"),
                ],
            })
        else:
            # Schema exists but check coverage
            coverage = signals.get("schema_coverage", "")
            if coverage and "/" in coverage:
                parts = coverage.split("/")
                try:
                    present, total = int(parts[0]), int(parts[1].split()[0])
                    if present < total:
                        recs.append({
                            "category": t("Structured Data", "البيانات المنظمة", "结构化数据"),
                            "title": t(
                                f"Expand Schema.org coverage from {coverage} to all pages",
                                f"توسيع تغطية Schema.org من {coverage} لتشمل جميع الصفحات",
                                f"将 Schema.org 覆盖范围从 {coverage} 扩展到所有页面",
                            ),
                            "impact": "High",
                            "description": t(
                                f"Schema.org is present on only {coverage}. Top performers like Stripe and FastAPI have structured data on 100% of pages.",
                                f"Schema.org موجود فقط في {coverage}. المواقع الرائدة مثل Stripe و FastAPI لديها بيانات منظمة في 100% من الصفحات.",
                                f"Schema.org 仅存在于 {coverage} 页面上。顶级网站如 Stripe 和 FastAPI 在 100% 的页面上都有结构化数据。",
                            ),
                            "action_items": [
                                t("Add JSON-LD to every page that's currently missing it",
                                  "إضافة JSON-LD لكل صفحة لا تحتويه حالياً",
                                  "为目前缺少的每个页面添加 JSON-LD"),
                                t("Use specific @type values: Organization, Service, Product, FAQ, HowTo",
                                  "استخدم أنواع @type محددة: Organization, Service, Product, FAQ, HowTo",
                                  "使用特定的 @type 值: Organization, Service, Product, FAQ, HowTo"),
                            ],
                        })
                except (ValueError, IndexError):
                    pass

        # =====================================================================
        # 2. Missing OpenGraph Meta Tags
        # =====================================================================
        if not signals.get("has_opengraph"):
            recs.append({
                "category": t("Social Meta Tags", "البيانات الوصفية الاجتماعية", "社交元数据"),
                "title": t(
                    "Add OpenGraph and Twitter Card tags for improved sharing and AI indexing",
                    "إضافة وسوم OpenGraph و Twitter Cards لتحسين المشاركة والفهرسة",
                    "添加 OpenGraph 和 Twitter Cards 以改善分享和 AI 索引",
                ),
                "impact": "High",
                "description": t(
                    f"No OpenGraph or Twitter Card meta tags were found on {brand}'s site. These tags are essential for proper content display when shared and for AI engine content understanding. All top-performing websites implement these on every page.",
                    f"لم يتم العثور على وسوم OpenGraph أو Twitter Cards على موقع {brand}. هذه الوسوم ضرورية للعرض الصحيح عند المشاركة ولفهم محركات الذكاء الاصطناعي.",
                    f"未在 {brand} 网站上发现 OpenGraph 或 Twitter Cards 标签。这些标签对于分享时的正确显示和 AI 引擎的内容理解至关重要。",
                ),
                "action_items": [
                    t("Add og:title, og:description, og:image, og:url to every page",
                      "إضافة og:title و og:description و og:image و og:url لكل صفحة",
                      "为每个页面添加 og:title、og:description、og:image、og:url"),
                    t("Add twitter:card, twitter:title, twitter:description tags",
                      "إضافة twitter:card و twitter:title و twitter:description",
                      "添加 twitter:card、twitter:title、twitter:description"),
                    t("Use unique, compelling images for og:image on each page",
                      "استخدم صوراً فريدة وجذابة لـ og:image في كل صفحة",
                      "为每个页面的 og:image 使用唯一且引人注目的图片"),
                ],
            })

        # =====================================================================
        # 3. Missing FAQ Content
        # =====================================================================
        if not signals.get("has_faq_content"):
            recs.append({
                "category": t("FAQ & Direct Answers", "الأسئلة الشائعة والإجابات المباشرة", "FAQ 常见问题"),
                "title": t(
                    "Add FAQ sections with direct-answer snippets to service pages",
                    "إضافة أقسام أسئلة شائعة (FAQ) مع إجابات مباشرة في صفحات الخدمات",
                    "在服务页面添加 FAQ 常见问题解答部分",
                ),
                "impact": "Critical",
                "description": t(
                    f"No structured FAQ content was detected on {brand}'s website. Top performers like MDN (direct answer score: 95%) and Cloudflare (93%) use structured Q&A extensively. Generative AI engines strongly prefer direct answers structured under clear question headings.",
                    f"لم يتم اكتشاف محتوى FAQ منظم على موقع {brand}. المواقع الرائدة مثل MDN (95%) و Cloudflare (93%) تستخدم الأسئلة والأجوبة المنظمة بكثافة.",
                    f"未在 {brand} 网站上检测到结构化 FAQ 内容。顶级网站如 MDN (95%) 和 Cloudflare (93%) 广泛使用结构化问答。",
                ),
                "action_items": [
                    t("Add 5-8 Q&A pairs to each major service/product page",
                      "إضافة 5-8 أسئلة وأجوبة في كل صفحة خدمة/منتج رئيسية",
                      "在每个主要服务/产品页面添加 5-8 个 FAQ 问答"),
                    t("Use H2/H3 question headings (e.g., 'What is...?', 'How does...work?')",
                      "استخدام عناوين H2/H3 بصيغة سؤال (مثل: 'ما هو...؟'، 'كيف يعمل...؟')",
                      "使用 H2/H3 问题标题（例如：'什么是...？'、'如何...？'）"),
                    t("Write concise 40-60 word direct answers under each question",
                      "كتابة إجابات مباشرة (40-60 كلمة) تحت كل سؤال",
                      "在每个问题下写 40-60 字的直接答案"),
                    t("Add FAQPage JSON-LD schema to pages with FAQ sections",
                      "إضافة FAQPage JSON-LD schema للصفحات التي تحتوي على أقسام FAQ",
                      "为包含 FAQ 部分的页面添加 FAQPage JSON-LD schema"),
                ],
            })

        # =====================================================================
        # 4. Brand Not Mentioned (Entity Identity)
        # =====================================================================
        if not signals.get("brand_in_first_100_chars"):
            pages_missing_brand = [p.get("path", "/") for p in pages if not p.get("brand_mentioned", False)]
            if pages_missing_brand:
                paths_text = ", ".join(pages_missing_brand[:5])
                recs.append({
                    "category": t("Entity Authority & Brand Identity", "هوية الكيان التجاري", "品牌实体权威"),
                    "title": t(
                        f"Add explicit '{brand}' mentions on: {paths_text}",
                        f"ذكر اسم العلامة التجارية '{brand}' صراحةً في: {paths_text}",
                        f"在以下页面明确提及品牌名称 '{brand}': {paths_text}",
                    ),
                    "impact": "High",
                    "description": t(
                        f"The brand name '{brand}' is not mentioned in the opening paragraphs of {len(pages_missing_brand)} pages. AI engines associate content with entities based on early text mentions. Top sites mention their brand within the first sentence of every page.",
                        f"اسم العلامة التجارية '{brand}' غير مذكور في الفقرات الأولى من {len(pages_missing_brand)} صفحات. المواقع الرائدة تذكر علامتها التجارية في أول جملة من كل صفحة.",
                        f"品牌名称 '{brand}' 未出现在 {len(pages_missing_brand)} 个页面的首段中。顶级网站在每个页面的第一句话中都会提及品牌。",
                    ),
                    "action_items": [
                        t(f"Mention '{brand}' within the first 100 characters of each page",
                          f"ذكر '{brand}' في أول 100 حرف من كل صفحة",
                          f"在每个页面的前 100 个字符中提及 '{brand}'"),
                        t(f"Include '{brand}' in H1 and key H2 headings",
                          f"استخدام '{brand}' في عناوين H1 و H2 الرئيسية",
                          f"在 H1 和 H2 标题中使用 '{brand}'"),
                        t("Ensure brand name appears in title tag and meta description",
                          "التأكد من وجود اسم العلامة التجارية في وسم title والوصف meta description",
                          "确保 title 标签和 meta description 中包含品牌名称"),
                    ],
                })

        # =====================================================================
        # 5. Missing Meta Descriptions
        # =====================================================================
        if not signals.get("has_meta_description"):
            recs.append({
                "category": t("Core SEO", "SEO الأساسي", "核心 SEO"),
                "title": t(
                    "Add unique meta descriptions to all pages",
                    "إضافة أوصاف meta فريدة لكل صفحة",
                    "为每个页面添加唯一的 meta description",
                ),
                "impact": "Critical",
                "description": t(
                    f"No meta description tags were found on {brand}'s website. This directly affects how your site appears in search results and how AI engines understand your content. Every top-performing website has unique, compelling meta descriptions.",
                    f"لم يتم العثور على وسم meta description على موقع {brand}. هذا يؤثر مباشرةً على كيفية عرض موقعك في نتائج البحث.",
                    f"未在 {brand} 网站上发现 meta description 标签。这直接影响网站在搜索结果中的显示。",
                ),
                "action_items": [
                    t("Write a unique meta description (150-160 chars) for each page",
                      "كتابة وصف meta فريد (150-160 حرف) لكل صفحة",
                      "为每个页面编写唯一的 meta description（150-160 字符）"),
                    t(f"Include '{brand}' and primary keywords in each description",
                      f"تضمين اسم '{brand}' والكلمات المفتاحية في كل وصف",
                      f"在每个描述中包含 '{brand}' 和主要关键词"),
                    t("Make descriptions action-oriented with clear value propositions",
                      "جعل الأوصاف موجهة نحو الفعل مع عروض قيمة واضحة",
                      "使描述面向行动，具有明确的价值主张"),
                ],
            })
        else:
            coverage = signals.get("meta_desc_coverage", "")
            if coverage and "/" in coverage:
                parts = coverage.split("/")
                try:
                    present, total = int(parts[0]), int(parts[1].split()[0])
                    if present < total:
                        recs.append({
                            "category": t("Core SEO", "SEO الأساسي", "核心 SEO"),
                            "title": t(
                                f"Expand meta description coverage from {coverage} to all pages",
                                f"توسيع تغطية meta description من {coverage} لتشمل جميع الصفحات",
                                f"将 meta description 覆盖范围从 {coverage} 扩展到所有页面",
                            ),
                            "impact": "High",
                            "description": t(
                                f"Meta descriptions are present on only {coverage}. Each page needs a unique, compelling description.",
                                f"أوصاف meta موجودة فقط في {coverage}. كل صفحة تحتاج وصفاً فريداً.",
                                f"Meta description 仅存在于 {coverage} 页面上。每个页面都需要唯一的描述。",
                            ),
                            "action_items": [
                                t("Write unique meta descriptions for all missing pages",
                                  "كتابة أوصاف meta فريدة لجميع الصفحات المفقودة",
                                  "为所有缺少的页面编写唯一的 meta description"),
                            ],
                        })
                except (ValueError, IndexError):
                    pass

        # =====================================================================
        # 6. Missing H1 or Heading Hierarchy
        # =====================================================================
        if not signals.get("has_h1"):
            recs.append({
                "category": t("Content Structure", "هيكل المحتوى", "内容结构"),
                "title": t(
                    "Add H1 headings to all pages",
                    "إضافة عناوين H1 لجميع الصفحات",
                    "为所有页面添加 H1 标题",
                ),
                "impact": "Critical",
                "description": t(
                    f"No H1 heading was found on {brand}'s pages. H1 is the primary signal for AI engines to understand page topic. Every top-performing website uses a single, descriptive H1.",
                    f"لم يتم العثور على عنوان H1 في صفحات {brand}. H1 هو الإشارة الأساسية لمحركات الذكاء الاصطناعي لفهم موضوع الصفحة.",
                    f"未在 {brand} 页面上找到 H1 标题。H1 是 AI 引擎理解页面主题的主要信号。",
                ),
                "action_items": [
                    t("Add a single, clear H1 that describes the page content",
                      "إضافة عنوان H1 واحد واضح يصف محتوى الصفحة",
                      "添加一个清晰描述页面内容的 H1 标题"),
                    t(f"Include '{brand}' in the H1 where appropriate",
                      f"تضمين '{brand}' في H1 عند الاقتضاء",
                      f"在适当的位置在 H1 中包含 '{brand}'"),
                ],
            })

        if not signals.get("has_heading_hierarchy"):
            recs.append({
                "category": t("Content Structure", "هيكل المحتوى", "内容结构"),
                "title": t(
                    "Implement proper heading hierarchy (H1 → H2 → H3) across all pages",
                    "تطبيق تسلسل العناوين الصحيح (H1 → H2 → H3) في جميع الصفحات",
                    "在所有页面实施正确的标题层次结构 (H1 → H2 → H3)",
                ),
                "impact": "High",
                "description": t(
                    f"Proper heading hierarchy was not detected on {brand}'s pages. AI engines use heading structure to understand content organization. Top sites use H2 for main sections and H3 for subsections.",
                    f"لم يتم اكتشاف تسلسل عناوين صحيح في صفحات {brand}. محركات الذكاء الاصطناعي تستخدم هيكل العناوين لفهم تنظيم المحتوى.",
                    f"未在 {brand} 页面上检测到正确的标题层次结构。AI 引擎使用标题结构来理解内容组织。",
                ),
                "action_items": [
                    t("Use H2 for main section titles, H3 for sub-sections",
                      "استخدام H2 للأقسام الرئيسية و H3 للأقسام الفرعية",
                      "使用 H2 作为主要部分标题，H3 作为子部分"),
                    t("Ensure every page has at least H1 → H2 → H3 depth",
                      "التأكد من أن كل صفحة لديها عمق H1 → H2 → H3 على الأقل",
                      "确保每个页面至少有 H1 → H2 → H3 的深度"),
                    t("Use descriptive, keyword-rich headings that AI can parse",
                      "استخدام عناوين وصفية غنية بالكلمات المفتاحية يمكن لـ AI تحليلها",
                      "使用描述性的、关键词丰富的标题，便于 AI 解析"),
                ],
            })

        # =====================================================================
        # 7. Thin Content Pages
        # =====================================================================
        thin_pages = [p for p in pages if p.get("characters_count", 0) < 400]
        if thin_pages:
            paths_text = ", ".join(p.get("path", "/") for p in thin_pages[:5])
            recs.append({
                "category": t("Content Depth", "عمق المحتوى", "内容深度"),
                "title": t(
                    f"Increase content depth on: {paths_text}",
                    f"زيادة عمق المحتوى في: {paths_text}",
                    f"增加以下页面的内容深度: {paths_text}",
                ),
                "impact": "High",
                "description": t(
                    f"Found {len(thin_pages)} thin-content pages (under 400 characters). Top-performing websites average 800-2000+ words per page. AI engines need rich content to extract useful information for citations.",
                    f"تم اكتشاف {len(thin_pages)} صفحات ذات محتوى ضعيف. المواقع الرائدة تحتوي على 800-2000+ كلمة لكل صفحة.",
                    f"检测到 {len(thin_pages)} 个内容稀薄页面。顶级网站每页平均有 800-2000+ 字。",
                ),
                "action_items": [
                    t("Add detailed explanatory paragraphs (500+ words) to each page",
                      "إضافة فقرات توضيحية تفصيلية (500+ كلمة) لكل صفحة",
                      "为每个页面添加详细说明文字（500+ 字）"),
                    t("Include technical specification tables and comparisons",
                      "إضافة جداول مواصفات فنية ومقارنات",
                      "添加技术规格表和对比数据"),
                    t("Add case studies and real-world application examples",
                      "إضافة دراسات حالة وأمثلة عملية",
                      "添加案例研究和实际应用示例"),
                ],
            })

        # =====================================================================
        # 8. Missing Canonical URLs
        # =====================================================================
        if not signals.get("has_canonical"):
            recs.append({
                "category": t("Technical SEO", "SEO التقني", "技术 SEO"),
                "title": t(
                    "Add canonical URL tags to prevent duplicate content",
                    "إضافة وسوم canonical URL لمنع المحتوى المكرر",
                    "添加 canonical URL 标签以防止重复内容",
                ),
                "impact": "High",
                "description": t(
                    f"No canonical URL tags were detected on {brand}'s pages. Without canonicals, AI engines may index duplicate versions of your pages, diluting authority signals.",
                    f"لم يتم اكتشاف وسوم canonical URL على صفحات {brand}. بدون canonicals، قد تفهرس محركات الذكاء الاصطناعي نسخاً مكررة.",
                    f"未在 {brand} 页面上检测到 canonical URL 标签。没有 canonical 标签，AI 引擎可能会索引页面的重复版本。",
                ),
                "action_items": [
                    t("Add <link rel='canonical' href='...'/> to every page",
                      "إضافة <link rel='canonical' href='...'/> لكل صفحة",
                      "为每个页面添加 <link rel='canonical' href='...'/>"),
                    t("Ensure canonical URLs use consistent format (www vs non-www, trailing slash)",
                      "التأكد من أن canonical URLs تستخدم تنسيقاً موحداً",
                      "确保 canonical URL 使用一致的格式"),
                ],
            })

        # =====================================================================
        # 9. Missing Sitemap
        # =====================================================================
        if not signals.get("has_sitemap"):
            recs.append({
                "category": t("Technical SEO", "SEO التقني", "技术 SEO"),
                "title": t(
                    "Create and submit an XML sitemap",
                    "إنشاء وتقديم خريطة موقع XML",
                    "创建并提交 XML 站点地图",
                ),
                "impact": "High",
                "description": t(
                    f"No sitemap.xml was found for {brand}'s website. Sitemaps help AI engines discover and index all your pages efficiently. All top-performing websites maintain up-to-date sitemaps.",
                    f"لم يتم العثور على sitemap.xml لموقع {brand}. خرائط الموقع تساعد محركات الذكاء الاصطناعي على اكتشاف وفهرسة جميع صفحاتك.",
                    f"未找到 {brand} 网站的 sitemap.xml。站点地图帮助 AI 引擎高效地发现和索引所有页面。",
                ),
                "action_items": [
                    t("Generate a sitemap.xml listing all pages with <lastmod> dates",
                      "إنشاء sitemap.xml يحتوي على جميع الصفحات مع تواريخ <lastmod>",
                      "生成包含所有页面和 <lastmod> 日期的 sitemap.xml"),
                    t("Submit sitemap to Google Search Console and Bing Webmaster Tools",
                      "تقديم خريطة الموقع إلى Google Search Console و Bing Webmaster Tools",
                      "将站点地图提交到 Google Search Console 和 Bing Webmaster Tools"),
                    t("Reference sitemap in robots.txt",
                      "إضافة رابط خريطة الموقع في robots.txt",
                      "在 robots.txt 中引用站点地图"),
                ],
            })

        # =====================================================================
        # 10. Missing robots.txt
        # =====================================================================
        if not signals.get("has_robots_txt"):
            recs.append({
                "category": t("Technical SEO", "SEO التقني", "技术 SEO"),
                "title": t(
                    "Add a robots.txt file with proper crawl directives",
                    "إضافة ملف robots.txt مع توجيهات الزحف المناسبة",
                    "添加包含正确爬取指令的 robots.txt 文件",
                ),
                "impact": "High",
                "description": t(
                    f"No robots.txt was found for {brand}'s website. This file tells AI crawlers which pages to index and where to find your sitemap.",
                    f"لم يتم العثور على ملف robots.txt لموقع {brand}. هذا الملف يخبر محركات البحث بالصفحات المسموح بفهرستها.",
                    f"未找到 {brand} 网站的 robots.txt。此文件告诉 AI 爬虫哪些页面可以索引以及在哪里找到站点地图。",
                ),
                "action_items": [
                    t("Create robots.txt with Allow: / and Sitemap directive",
                      "إنشاء robots.txt مع Allow: / و توجيه Sitemap",
                      "创建包含 Allow: / 和 Sitemap 指令的 robots.txt"),
                    t("Block irrelevant paths (admin panels, staging areas)",
                      "حظر المسارات غير ذات الصلة (لوحات الإدارة، مناطق التطوير)",
                      "阻止不相关的路径（管理面板、暂存区域）"),
                ],
            })

        # =====================================================================
        # 11. Missing Alt Text on Images
        # =====================================================================
        if not signals.get("has_alt_text"):
            recs.append({
                "category": t("Accessibility & GLMM", "إمكانية الوصول", "可访问性与 GLMM"),
                "title": t(
                    "Add descriptive alt text to all images",
                    "إضافة نص بديل وصفي لجميع الصور",
                    "为所有图片添加描述性 alt 文本",
                ),
                "impact": "High",
                "description": t(
                    f"Many images on {brand}'s site lack descriptive alt text. Multimodal AI models (GLMM) use alt text to understand visual content. Top sites have alt text on 100% of images.",
                    f"العديد من الصور على موقع {brand} تفتقر إلى نص بديل وصفي. نماذج الذكاء الاصطناعي متعددة الوسائط تستخدم النص البديل لفهم المحتوى المرئي.",
                    f"{brand} 网站上的许多图片缺少描述性 alt 文本。多模态 AI 模型使用 alt 文本来理解视觉内容。",
                ),
                "action_items": [
                    t("Add keyword-rich, descriptive alt text to every image",
                      "إضافة نص بديل وصفي وغني بالكلمات المفتاحية لكل صورة",
                      "为每张图片添加关键词丰富的描述性 alt 文本"),
                    t("Describe what the image shows, not just decorative keywords",
                      "وصف ما تظهره الصورة، وليس مجرد كلمات مفتاحية تزيينية",
                      "描述图片展示的内容，而不仅仅是装饰性关键词"),
                ],
            })

        # =====================================================================
        # 12. Missing lang Attribute
        # =====================================================================
        if not signals.get("has_lang_attr"):
            recs.append({
                "category": t("Accessibility & GLMM", "إمكانية الوصول", "可访问性与 GLMM"),
                "title": t(
                    "Add HTML lang attribute for language identification",
                    "إضافة خاصية lang في HTML لتحديد اللغة",
                    "添加 HTML lang 属性进行语言识别",
                ),
                "impact": "High",
                "description": t(
                    f"The HTML lang attribute is missing on {brand}'s pages. AI engines use this to understand content language and serve appropriate results.",
                    f"خاصية lang في HTML مفقودة على صفحات {brand}. محركات الذكاء الاصطناعي تستخدمها لفهم لغة المحتوى.",
                    f"{brand} 页面上缺少 HTML lang 属性。AI 引擎使用它来理解内容语言。",
                ),
                "action_items": [
                    t("Add lang='en' (or appropriate language code) to the <html> tag",
                      "إضافة lang='ar' (أو رمز اللغة المناسب) لوسم <html>",
                      "在 <html> 标签中添加 lang='zh' (或适当的语言代码)"),
                ],
            })

        # =====================================================================
        # 13. Content Strategy (always recommend)
        # =====================================================================
        word_count = signals.get("total_word_count", 0)
        recs.append({
            "category": t("Content Strategy", "استراتيجية المحتوى", "内容策略"),
            "title": t(
                "Create comparison and how-to content pages to capture AI citations",
                "إنشاء صفحات مقارنة وأدلة إرشادية لجذب اقتباسات الذكاء الاصطناعي",
                "创建比较和操作指南内容页面以获取 AI 引用",
            ),
            "impact": "High",
            "description": t(
                f"Top-performing websites like Cloudflare and MDN create dedicated comparison pages, how-to guides, and glossary pages. These content types are heavily cited by AI engines when users ask comparative or instructional questions. {brand} should create similar content.",
                f"المواقع الرائدة مثل Cloudflare و MDN تنشئ صفحات مقارنة وأدلة إرشادية ومسارد مصطلحات. {brand} يجب أن ينشئ محتوى مشابه.",
                f"顶级网站如 Cloudflare 和 MDN 创建专门的比较页面、操作指南和术语表。{brand} 应该创建类似的内容。",
            ),
            "action_items": [
                t(f"Create '{brand} vs Competitors' comparison pages",
                  f"إنشاء صفحات '{brand} مقابل المنافسين'",
                  f"创建 '{brand} 与竞争对手' 的比较页面"),
                t("Write 'How to' guides for your core services/products",
                  "كتابة أدلة 'كيفية' لخدماتك/منتجاتك الأساسية",
                  "为核心服务/产品编写'如何'指南"),
                t("Create a glossary page defining key industry terms",
                  "إنشاء صفحة مسرد تعريف المصطلحات الصناعية الرئيسية",
                  "创建定义关键行业术语的术语表页面"),
                t("Add detailed case studies with measurable results",
                  "إضافة دراسات حالة مفصلة بنتائج قابلة للقياس",
                  "添加包含可衡量结果的详细案例研究"),
            ],
        })

        # =====================================================================
        # 14. Authority Signals (always recommend)
        # =====================================================================
        recs.append({
            "category": t("Entity Authority", "سلطة الكيان", "实体权威"),
            "title": t(
                "Strengthen entity authority signals for AI engine recognition",
                "تعزيز إشارات سلطة الكيان لتعرف محركات الذكاء الاصطناعي",
                "增强实体权威信号以获得 AI 引擎认可",
            ),
            "impact": "High",
            "description": t(
                f"AI engines like ChatGPT, Claude, and Gemini prioritize citing authoritative sources. {brand} needs to establish stronger authority signals across the site. Top performers like Stripe and AWS include team expertise, certifications, and detailed About pages.",
                f"محركات الذكاء الاصطناعي تفضل الاستشهاد بمصادر موثوقة. {brand} يحتاج إلى تعزيز إشارات السلطة. المواقع الرائدة تتضمن خبرات الفريق والشهادات.",
                f"AI 引擎优先引用权威来源。{brand} 需要建立更强的权威信号。顶级网站如 Stripe 和 AWS 包含团队专业知识和认证。",
            ),
            "action_items": [
                t("Create a detailed About page with company history, mission, and team expertise",
                  "إنشاء صفحة 'عن الشركة' مفصلة بتاريخ الشركة ومهمتها وخبرات الفريق",
                  "创建详细的'关于我们'页面，包含公司历史、使命和团队专业知识"),
                t("Add team member profiles with credentials and certifications",
                  "إضافة ملفات تعريف أعضاء الفريق مع بيانات الاعتماد والشهادات",
                  "添加团队成员资料，包含资质和认证"),
                t("Include client testimonials and trust badges",
                  "تضمين شهادات العملاء وشارات الثقة",
                  "包含客户推荐和信任徽章"),
                t("Add industry certifications, awards, and partnership logos",
                  "إضافة الشهادات الصناعية والجوائز وشعارات الشراكات",
                  "添加行业认证、奖项和合作伙伴标志"),
            ],
        })

        # =====================================================================
        # 15. Internal Linking Strategy (always recommend)
        # =====================================================================
        recs.append({
            "category": t("Internal Linking", "الروابط الداخلية", "内部链接"),
            "title": t(
                "Build a strategic internal linking structure",
                "بناء هيكل روابط داخلية استراتيجي",
                "构建战略性内部链接结构",
            ),
            "impact": "High",
            "description": t(
                f"Top-performing websites like MDN and Stripe use extensive internal linking (5-10+ contextual cross-links per page) to help AI engines understand content relationships. {brand} should implement a similar linking strategy to strengthen topical authority.",
                "المواقع الرائدة مثل MDN و Stripe تستخدم روابط داخلية مكثفة (5-10+ رابط لكل صفحة) لمساعدة محركات الذكاء الاصطناعي على فهم العلاقات بين المحتوى.",
                "顶级网站如 MDN 和 Stripe 使用大量内部链接（每页 5-10+ 个上下文交叉链接）来帮助 AI 引擎理解内容关系。",
            ),
            "action_items": [
                t("Add 5-10 contextual internal links per page to related content",
                  "إضافة 5-10 روابط داخلية سياقية لكل صفحة تربط بالمحتوى ذي الصلة",
                  "每页添加 5-10 个指向相关内容的上下文内部链接"),
                t("Create a pillar page strategy: hub pages linking to detailed sub-pages",
                  "إنشاء استراتيجية صفحات محورية: صفحات رئيسية تربط بصفحات فرعية مفصلة",
                  "创建支柱页面策略：中心页面链接到详细的子页面"),
                t("Use descriptive anchor text (not 'click here' or 'learn more')",
                  "استخدام نص رابط وصفي (ليس 'اضغط هنا' أو 'اعرف المزيد')",
                  "使用描述性锚文本（而不是'点击这里'或'了解更多'）"),
                t("Add 'Related Services/Products' sections at the bottom of each page",
                  "إضافة قسم 'خدمات/منتجات ذات صلة' في أسفل كل صفحة",
                  "在每个页面底部添加'相关服务/产品'部分"),
            ],
        })

        # =====================================================================
        # 16. Twitter Cards (if missing and OG also missing)
        # =====================================================================
        if not signals.get("has_twitter_cards") and signals.get("has_opengraph"):
            recs.append({
                "category": t("Social Meta Tags", "البيانات الوصفية الاجتماعية", "社交元数据"),
                "title": t(
                    "Add Twitter Card meta tags alongside existing OpenGraph",
                    "إضافة وسوم Twitter Cards بجانب OpenGraph الموجود",
                    "在现有 OpenGraph 旁添加 Twitter Card 元标签",
                ),
                "impact": "High",
                "description": t(
                    "OpenGraph tags are present but Twitter Cards are missing. Adding Twitter Cards ensures optimal display when content is shared on X/Twitter and helps AI aggregation engines.",
                    "وسوم OpenGraph موجودة لكن Twitter Cards مفقودة. إضافتها تضمن العرض الأمثل عند المشاركة.",
                    "OpenGraph 标签存在但 Twitter Cards 缺失。添加它们可确保在 X/Twitter 上分享时的最佳显示。",
                ),
                "action_items": [
                    t("Add twitter:card, twitter:title, twitter:description, twitter:image to all pages",
                      "إضافة twitter:card و twitter:title و twitter:description و twitter:image لجميع الصفحات",
                      "为所有页面添加 twitter:card、twitter:title、twitter:description、twitter:image"),
                ],
            })

        # =====================================================================
        # 17. Mobile Viewport (if missing)
        # =====================================================================
        if not signals.get("has_viewport"):
            recs.append({
                "category": t("Technical SEO", "SEO التقني", "技术 SEO"),
                "title": t(
                    "Add mobile viewport meta tag for responsive design",
                    "إضافة وسم viewport للتصميم المتجاوب مع الأجهزة المحمولة",
                    "添加移动端 viewport meta 标签以实现响应式设计",
                ),
                "impact": "Critical",
                "description": t(
                    f"No viewport meta tag was found on {brand}'s pages. Mobile-friendliness is a ranking factor for both search engines and AI engines.",
                    f"لم يتم العثور على وسم viewport على صفحات {brand}. التوافق مع الأجهزة المحمولة هو عامل ترتيب لمحركات البحث والذكاء الاصطناعي.",
                    f"未在 {brand} 页面上找到 viewport meta 标签。移动友好性是搜索引擎和 AI 引擎的排名因素。",
                ),
                "action_items": [
                    t("Add <meta name='viewport' content='width=device-width, initial-scale=1'> to all pages",
                      "إضافة <meta name='viewport' content='width=device-width, initial-scale=1'> لجميع الصفحات",
                      "为所有页面添加 <meta name='viewport' content='width=device-width, initial-scale=1'>"),
                ],
            })

        return recs
