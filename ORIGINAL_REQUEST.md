# AISEO Platform — Original Charter & Project Definition

> Reference: [docs/project_definition.md](docs/project_definition.md) · [docs/architecture.md](docs/architecture.md)

---

## 1. Project Background

Traditional SEO has been disrupted by Generative AI. With over 65% of user journeys now concluding in zero-click answers on ChatGPT, Google Gemini, and Perplexity, enterprise marketing teams face a critical blind spot:
- *Legacy ranking trackers only monitor 10 blue links on Google.*
- *They have zero visibility into whether generative AI engines recognize, recommend, or cite their brand.*
- *They have no mechanism to detect when AI engines hallucinate outdated pricing or false feature limitations.*

The **AISEO Platform** was commissioned to solve this paradigm shift: creating a unified search intelligence suite for **SEO (Search Engines)**, **AEO (Answer Engines)**, and **GEO (Generative Engines)**.

---

## 2. Core Functional Requirements

### R1. Autonomous Web Crawling & DOM Extraction
- Asynchronously crawl enterprise domains with BFS/DFS link traversal.
- Detect and respect `robots.txt` indexing directives and parse `sitemap.xml` catalogs.
- Strip 65%+ boilerplate noise (navbars, footers, tracking scripts, ads) using high-precision extractors (`Trafilatura`).
- Extract heading trees (H1-H6), structured JSON-LD schemas, and OpenGraph metadata.
- Fallback to headless browser execution (`Playwright`) when dynamic client-side JavaScript hydration (React, Next.js, Vue) is detected.

### R2. High-Speed Classical ML Inference & Intent Classification
- Serve high-accuracy classification models locally via **ONNX Runtime** with sub-5ms CPU latency.
- Categorize search queries and page sections into 4 canonical search intents: *Commercial, Informational, Navigational, Transactional*.
- Track all dataset versions, hyperparameters, and model registry artifacts in **MLflow**.

### R3. Synthetic Buyer Persona & Prompt Simulation Lab
- Synthesize conversational buyer queries across 4 strategic lenses:
  - *Top-of-Funnel (Awareness)*
  - *Middle-of-Funnel (Comparison)*
  - *Bottom-of-Funnel (Decision / Commercial)*
  - *Zero-Click (AEO Direct Answers)*
- Enforce strict Pydantic JSON schemas with multi-lingual support (English, Arabic, Global).

### R4. Multi-Engine AI Execution & Citation Auditing
- Asynchronously dispatch prompt matrices concurrently across OpenAI (GPT-4o), Google (Gemini 1.5), Anthropic (Claude 3.5), and Perplexity (Sonar).
- Parse raw synthesized answers to extract:
  - Brand mention presence (exact and fuzzy NER matching).
  - Ground-truth citation URLs embedded in answers or footnotes.
  - Sentiment analysis (Positive, Neutral, Negative).
  - Competitor co-occurrence and share-of-voice.

### R5. Deterministic GEO Visibility Scoring & Actionable Blueprints
- Compute an explainable, 100% deterministic **0–100 GEO Visibility Score** across 6 weighted sub-pillars:
  - Content Clarity (20%)
  - Entity Coverage (20%)
  - AI Visibility (20%)
  - Citation Readiness (15%)
  - Competitive Share (15%)
  - Technical SEO Signals (10%)
- Generate prioritized remediation tasks (Impact vs. Effort) with copy-paste Schema.org JSON-LD code.

### R6. Enterprise Security, Tenant Vault & Automated Delivery
- AES-256 encrypted credential vault for client API keys (BYOK model).
- Strict multi-tenant data isolation via mandatory `TenantId`.
- Automated cron-scheduled recurring audits with white-label executive PDF digest delivery via email.

---

## 3. High-Fidelity Additions from HistoryVerse-Chatbot

To advance the platform from basic keyword/regex matching into a true **GEO Truth Engine**, the architecture integrates 4 production-grade systems from `omarMohamedo-o/HistoryVerse-Chatbot`:
1. **RAG Faithfulness & Citation Grounding Engine**: Mathematical grounding ratio calculation and hallucination scoring.
2. **Hybrid Search & Cross-Encoder Reranking**: BM25 lexical + dense vector retrieval with cross-encoder scoring to predict exact answer snippet extraction.
3. **Semantic Response Caching**: Similarity-based response hashing reducing external LLM calls by 70%+.
4. **Multilingual & Arabic NLP Normalization**: Ligature protection, numeral translation, and colloquial term mapping for global and MENA enterprise coverage.
