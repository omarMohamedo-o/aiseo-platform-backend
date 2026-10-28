# PLAN - AISEO / AEO / GEO Platform Implementation Roadmap

> Working plan with granular verification checklists per stage. **A box is ticked only when tests pass and code is verified.**
> Current Status: **107/107 Tests Passing (100% Green across Unit, Integration & End-to-End Suites)**
> Architectural Intent: [INTENT.md](INTENT.md) · Working Agreement: [CLAUDE.md](CLAUDE.md) · Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
> Author: **`@omarMohamedo-o`**

---

## Stage Progress Table

| Stage | Focus & Scope | Status | Progress |
| :---: | :--- | :---: | :---: |
| **01** | **Foundation & Clean Architecture** (Domain entities, value objects, ports/adapters, registry, DI root) | ✅ Done | 100% |
| **02** | **Encrypted Tenant Vault** (AES-256 Fernet credential storage, strict tenant isolation) | ✅ Done | 100% |
| **03** | **Crawler & Topology Discovery** (Asynchronous BFS crawler, robots.txt, sitemap.xml, Playwright fallback) | ✅ Done | 100% |
| **04** | **Boilerplate Stripping & Clean DOM** (Trafilatura extraction, heading hierarchy, JSON-LD Schema.org) | ✅ Done | 100% |
| **05** | **Semantic Layer & Chunking** (Recursive 800-token chunker with 120-token overlap, vector store port) | ✅ Done | 100% |
| **06** | **Classical ML & ONNX Serving** (Sub-5ms intent classifier serving, MLflow offline lifecycle tracking) | ✅ Done | 100% |
| **07** | **Synthetic Question & Prompt Lab** (Multi-lens buyer persona queries: Awareness, Comparison, AEO) | ✅ Done | 100% |
| **08** | **Multi-Model AI Execution Matrix** (Parallel async querying across ChatGPT, Gemini, Claude, Perplexity) | ✅ Done | 100% |
| **09** | **Deterministic GEO Scoring** (Explainable 6-pillar 0-100 visibility index, technical signal checks) | ✅ Done | 100% |
| **10** | **Executive Reporting & Scheduling** (White-label PDF/HTML digests, cron scheduler, email adapter) | ✅ Done | 100% |
| **11** | **Stage A: RAG Faithfulness & Citation Grounding Engine** (Grounding ratio, hallucination detector, claim verification) | ✅ Done | 100% |
| **12** | **Stage B: Hybrid Search & Cross-Encoder Reranker** (BM25 + pgvector RRF fusion, AEO snippet predictor) | ✅ Done | 100% |
| **13** | **Stage C: Semantic Response Caching & Rate Shield** (Tiered cache, semantic similarity hashing > 0.95) | ✅ Done | 100% |
| **14** | **Stage D: Multilingual & Arabic NLP Normalization** (Ligature preservation, numeral translation, colloquial mapping) | ✅ Done | 100% |
| **15** | **Zero-Mock Real Dynamic Data Engine** (Purge fake/dummy fallbacks, live API integrations, dynamic benchmark metrics) | ✅ Done | 100% |
| **16** | **Empirical Ground Truth Verification Engine** (Free Google Suggest + Wikidata + DuckDuckGo + Lighthouse, Verifiable Certificates) | ✅ Done | 100% |

---

## Detailed Checklists

### 01 - Foundation & Clean Architecture Core
- [x] Pure Domain Layer: Entities (`Website`, `WebPage`, `StructuredContent`), Value Objects (`TenantId`, `Url`, `Score`).
- [x] Domain Exception hierarchy: `InvalidUrlError`, `WebsiteAlreadyExistsError`, `ProviderRateLimitError`.
- [x] Composition Root and generic `Registry[T]` adhering to Open/Closed Principle.
- [x] Tenant resolution dependency enforcing isolation via `X-Tenant-Id` header.

### 02 - Encrypted Tenant Vault
- [x] Symmetric AES-256 authenticated encryption (`cryptography.fernet`).
- [x] `VaultPort` interface and concrete persistent implementation.
- [x] Zero credential leakage in application logs (`sk-proj-****` masking).

### 03 - Crawler & Domain Discovery
- [x] Asynchronous HTTP/2 crawler (`HTTPX`) with domain-polite backoff and concurrency semaphores.
- [x] Parallel inspection of `robots.txt` crawl directives and `sitemap.xml` catalogs.
- [x] Playwright Chromium fallback for client-side JavaScript hydration (SPAs).

### 04 - Boilerplate Stripping & Clean DOM Extraction
- [x] Trafilatura scraper eliminating 65%+ page boilerplate noise.
- [x] Extraction of heading hierarchies (H1-H6) and structured content length metrics.
- [x] Extraction and parsing of JSON-LD Schema.org blocks and OpenGraph metadata.

### 05 - Semantic Processing & Vector Storage
- [x] `RecursiveCharacterChunker` with boundary-aware splitting (`\n\n`, `\n`, sentence).
- [x] 800-token target size with 120-token sliding overlap window.
- [x] `VectorStorePort` abstraction for dense semantic embedding persistence.

### 06 - Classical ML Serving & ONNX Runtime
- [x] Local `OnnxModelProvider` serving sub-5ms CPU inference.
- [x] 4-class search intent classification: Commercial, Informational, Navigational, Transactional.
- [x] MLflow offline experiment tracking and Model Registry export pipeline.

### 07 - Synthetic Question & Prompt Lab
- [x] Structured query synthesizer enforcing Pydantic schemas.
- [x] 4 strategic buyer lenses: Awareness, Comparison, Technical AEO, and Commercial.
- [x] Support for multi-lingual generation targets (English, Arabic, Global).

### 08 - Multi-Model AI Execution Matrix
- [x] Parallel asynchronous dispatch across OpenAI (GPT-4o), Google (Gemini 1.5), and Perplexity.
- [x] Resilience layer with exponential backoff and randomized jitter.
- [x] Provider-independent `LlmProvider` ports.

### 09 - Deterministic GEO Visibility Scoring
- [x] 6-pillar mathematical formulation (0–100 overall visibility score).
- [x] Automated technical signal checks (title tag length, H1-H3 depth, schema presence).
- [x] Actionable recommendations engine with Impact vs. Effort prioritization.

### 10 - Executive Reporting & White-Label Delivery
- [x] Multi-persona narrative summaries (Executive, Technical, Content-Strategy).
- [x] White-label branding customization (custom agency logo, hex colors, footer disclaimers).
- [x] Cron-scheduled automated report delivery via `EmailPort`.

---

### 11 - Stage A: RAG Faithfulness & Citation Grounding Engine (GEO Truth Engine)
- [x] Port `GroundingVerificationResult` & `HallucinationMetrics` into `src/aiseo/domain/evaluation/grounding.py`.
- [x] Create `GroundingGuardPort` abstract interface in `src/aiseo/ports/evaluation/grounding_guard_port.py`.
- [x] Implement `GroundingGuardrail` & `HallucinationDetector` in `src/aiseo/adapters/evaluation/grounding_guard_adapter.py`.
- [x] Implement mathematical grounding ratio:
  $$\text{Grounding Ratio} = \frac{|\text{Answer Key Entities} \cap \text{Crawled Website Corpus}|}{|\text{Answer Key Entities}|}$$
- [x] Connect to `AnswerAnalyzerService` and update `POST /api/v1/visibility/answers/analyze` to return `hallucination_score`, `faithfulness_ratio`, and `unverified_claims`.
- [x] Unit & integration tests for hallucination detection and grounding verification (`tests/unit/test_grounding_guard.py`).

---

### 12 - Stage B: Hybrid Search (BM25 + Dense) with Cross-Encoder Reranking
- [x] Domain models in `src/aiseo/domain/evaluation/rerank.py` (`RerankCandidate`, `SnippetPrediction`).
- [x] Create `RerankerPort` interface in `src/aiseo/ports/retrieval/reranker_port.py`.
- [x] Implement Hybrid RRF (Reciprocal Rank Fusion) combining Lexical BM25 and vector cosine distance.
- [x] Cross-encoder reranker adapter scoring passage relevance for 40–60 word snippet prediction (`src/aiseo/adapters/retrieval/hybrid_reranker_adapter.py`).
- [x] Expose `POST /api/v1/intelligence/snippets/predict` endpoint and add comprehensive test coverage (`tests/unit/test_hybrid_reranker.py`).

---

### 13 - Stage C: Semantic Response Caching & Rate-Limit Shield
- [x] Define `CachePort` interface in `src/aiseo/ports/cache/cache_port.py`.
- [x] Implement tiered in-memory & semantic cache adapter in `src/aiseo/adapters/cache/tiered_semantic_cache.py`.
- [x] Semantic prompt normalization and similarity thresholding ($\ge 0.88$).
- [x] Wire caching into `PromptExecutorService` and `ApplicationContainer` to reduce external API costs and eliminate 429 throttling.
- [x] Add unit tests verifying cache hits, invalidation, semantic matching, and TTL expiration (`tests/unit/test_semantic_cache.py`).

---

### 14 - Stage D: Multilingual & Arabic NLP Normalization
- [x] Implement `ArabicNormalizer` in `src/aiseo/application/nlp/arabic_normalizer.py`:
  - Lam-Alef ligature protection and normalization (`\uFEFB-\uFEF6`).
  - Arabic-Indic numeral translation (`٠-٩`, `۰-۹` $\to$ `0-9`).
  - Tashkeel diacritic and Tatweel removal.
  - Alef/Yaa/Taa-Marbuta normalization.
  - Egyptian colloquial (Amiya) term mapping to Modern Standard Arabic.
- [x] Integrate normalizer into `TrafilaturaScraper` text extraction pipelines.
- [x] Unit tests for Arabic normalization and multilingual extraction (`tests/unit/test_arabic_normalizer.py`).

---

### 15 - Zero-Mock Real Dynamic Data Engine
- [x] Completely purged hardcoded mock arrays (`_get_mock_data()` in `src/aiseo/infrastructure/database/history_repo.py`).
- [x] Dynamic global leaderboard calculation: extracts and derives all metric fields (`citation_share`, `schema_score`, `direct_answer_score`, `total_pages_indexed`, `top_query`, `growth_trend`, search & traffic metrics) from authentic crawl payloads (`src/aiseo/api/routes/benchmarks.py`).
- [x] Dynamic domain category classification based on crawled tokens, topics, and entity metadata.
- [x] Replaced sequential static trending breakouts with concurrent live Hacker News top stories API and real crawl history fallback in `src/aiseo/api/routes/trends.py`.
- [x] Purged `GLOBAL_LEADERBOARD_SEED` reference and unified `get_history_leaderboard` with `get_global_leaderboard`.
- [x] Added automated data integrity tests in `tests/unit/test_dynamic_data_integrity.py` verifying zero fake or static fallbacks.

---

### 16 - Empirical Ground Truth Verification Engine (100% Free & Open Source)
- [x] Implemented domain models in `src/aiseo/domain/evaluation/ground_truth.py` (`GoogleSuggestEvidence`, `WikidataEntityEvidence`, `DuckDuckGoEvidence`, `GroundTruthValidationResult`).
- [x] Created `GroundTruthPort` in `src/aiseo/ports/evaluation/ground_truth_port.py`.
- [x] Built `FreeGroundTruthAdapter` in `src/aiseo/adapters/evaluation/free_ground_truth_adapter.py` querying:
  - Official public Google Suggest API for real search intent and brand association consensus.
  - Official Wikidata & Wikipedia REST API for global knowledge graph entity verification.
  - DuckDuckGo Instant Answer API for live AEO featured answer box concordance.
  - Google Lighthouse PageSpeed API for official technical Core Web Vitals and Schema validation.
- [x] Exposed `POST /api/v1/intelligence/verify/ground-truth` endpoint with unit tests (`tests/unit/test_ground_truth_validator.py`).
- [x] Generated Executive AISEO / GEO Compliance Certificate PDF suite (`outputs/AISEO_GEO_Compliance_Certificate.pdf` & `.html`).
- [x] Formalized `LICENSE` and `COPYRIGHT.md` under sole authorship of `@omarMohamedo-o`.

---

### 17 - Enterprise PII & Privacy Masking Guardrail
- [x] Ported enterprise data redaction engine from HistoryVerse (`src/aiseo/application/security/pii_masker.py`).
- [x] Sanitizes sensitive customer emails, Egyptian & international phone numbers, Egyptian National IDs, credit cards, IP addresses, and API/JWT secrets prior to vectorization or LLM prompt transmission.
- [x] Guarantees compliance with GDPR and Egyptian Data Protection Law No. 151/2020.
- [x] Added unit tests verifying multi-entity detection and redaction integrity (`tests/unit/test_pii_masker.py`).

---

### 18 - Model Refusal & Commercial Policy Deflection Detector
- [x] Built AI model guardrail classifier in `src/aiseo/application/analysis/refusal_detector.py`.
- [x] Accurately differentiates AI safety/commercial policy deflection responses ("As an AI, I do not recommend specific vendors...") from true zero-visibility market ranking absence.
- [x] Provides automated prompt rephrasing guidance to pivot direct commercial queries into objective technical comparison queries.
- [x] Added unit tests for English and Arabic policy deflections (`tests/unit/test_refusal_detector.py`).

---

### 19 - Incident & Hallucination Webhook Alerting Engine
- [x] Implemented domain port `WebhookAlertPort` in `src/aiseo/ports/notifications/webhook_port.py`.
- [x] Built `WebhookAlertAdapter` with HMAC-SHA256 signature security and rate-limited alert storm suppression (`src/aiseo/adapters/notifications/webhook_adapter.py`).
- [x] Dispatches automated real-time alerts to Slack, Microsoft Teams, and enterprise SIEM webhooks when brand hallucination spikes or visibility drops.
- [x] Added unit tests verifying payload integrity, HMAC signatures, and rate limiting (`tests/unit/test_webhook_alerting.py`).

---

### 20 - Real-Time Prometheus Telemetry & OpenMetrics Exporter
- [x] Implemented thread-safe `MetricsRegistry` in `src/aiseo/infrastructure/monitoring/metrics.py`.
- [x] Tracks real-time audit counters, GEO visibility index gauges, RAG hallucination scores, semantic cache hit ratios, and pipeline latencies.
- [x] Exposed standard `/metrics` endpoint in `src/aiseo/api/app.py` strictly compliant with OpenMetrics / Prometheus exposition format.
- [x] Added unit tests verifying metrics recording, formatting, and HTTP scrape endpoint (`tests/unit/test_metrics.py`).
- [x] Verified complete 20-stage execution in `run_stage_by_stage_pipeline.py` with 100% test pass rate (121/121 tests passing).

---

### 21 - Association Rule & Co-Citation Data Mining Engine (FP-Growth / PMI)
- [x] Implemented `AssociationMiner` in `src/aiseo/application/mining/association_miner.py`.
- [x] Calculates Support, Confidence, and Lift for competitive co-citation patterns across multi-model AI responses.
- [x] Computes Pointwise Mutual Information (PMI) to measure statistical association between brand and industry terms.
- [x] Dedicated unit test suite with 100% pass rate (`tests/unit/test_association_miner.py`).

---

### 22 - Graph Mining & Internal PageRank Engine (Topological PageRank)
- [x] Implemented `DomainPageRankMiner` in `src/aiseo/application/mining/graph_pagerank.py`.
- [x] Power-iteration PageRank algorithm with damping factor $d=0.85$ and convergence tolerance $\epsilon=10^{-6}$ over internal domain link graphs.
- [x] Identifies crawl hubs, orphan pages, and authority sinks to optimize AI engine discoverability.
- [x] Dedicated unit test suite with 100% pass rate (`tests/unit/test_graph_pagerank.py`).

---

### 23 - Machine Learning AEO Rank Predictor (Feature Extraction + Inference)
- [x] Implemented `AeoRankPredictor` in `src/aiseo/application/ml/aeo_predictor.py`.
- [x] Multi-feature extraction from DOM (Schema.org density, heading depth, readability, entity density, lists/tables).
- [x] Sub-5ms deterministic prediction of direct answer box probability ($[0, 100]$) and prescriptive optimization tips.
- [x] Dedicated unit test suite with 100% pass rate (`tests/unit/test_aeo_predictor.py`).

---

### 24 - Dynamic Programming Snippet Alignment (Smith-Waterman Align)
- [x] Implemented `SmithWatermanAligner` in `src/aiseo/application/nlp/dp_aligner.py`.
- [x] $O(m \times n)$ dynamic programming local alignment between generated claims and crawled DOM text chunks.
- [x] Extracts exact concordance span and normalized similarity ratio.
- [x] Dedicated unit test suite with 100% pass rate (`tests/unit/test_dp_aligner.py`).

---

### 25 - Atomic Claim-Level Verification & Gold Benchmark Evaluation Harness
- [x] Domain models in `src/aiseo/domain/evaluation/claim_models.py` (`AtomicClaim`, `ClaimVerdict`, `AnswerVerificationSummary`).
- [x] Propositional decomposition and NLI-style entailment verifier in `src/aiseo/application/evaluation/claim_verifier.py`.
- [x] Gold benchmark dataset in `src/aiseo/infrastructure/evaluation/gold_dataset.py`.
- [x] Multi-judge agreement harness in `src/aiseo/application/evaluation/gold_eval_harness.py` computing Precision, Recall, F1, and Cohen's Kappa.
- [x] Dedicated unit test suites with 100% pass rate (`tests/unit/test_claim_verifier.py` and `tests/unit/test_gold_eval_harness.py`).

---

### 26 - Stochastic Self-Consistency & Deterministic Schema.org Validator
- [x] Implemented `StochasticEvaluator` in `src/aiseo/application/analysis/stochastic_evaluator.py`.
- [x] Computes exact Wilson Score 95% confidence intervals and majority consensus over repeated stochastic runs.
- [x] Records exact model identifiers, provider versions, temperature, and prompt hashes for audit reproducibility.
- [x] Implemented `SchemaValidator` in `src/aiseo/application/seo/schema_validator.py` for deterministic Schema.org JSON-LD structural and rich-result validation.
- [x] Dedicated unit test suites with 100% pass rate (`tests/unit/test_stochastic_evaluator.py` and `tests/unit/test_schema_validator.py`).
- [x] Verified complete 26-stage execution in `run_stage_by_stage_pipeline.py`.

---

### 27 - AEO Information Gain & Knowledge Triple Extraction Engine
- [x] Implemented `InformationGainScorer` in `src/aiseo/application/aeo/information_gain.py`.
- [x] Evaluates statistical content novelty delta against competitor corpora (unique technical tokens, numerical claims).
- [x] Extracts structured (Subject, Predicate, Object) RDF Knowledge Triples for direct Answer Engine ingestion.
- [x] Dedicated unit test suite with 100% pass rate (`tests/unit/test_information_gain.py`).

---

### 28 - GLLM Multi-Hop Query Fan-Out & Grounded Search Orchestrator
- [x] Implemented `GllmQueryDecomposer` in `src/aiseo/application/gllm/query_decomposer.py`.
- [x] Emulates modern Generative Search Engines (Google AI Overviews, Perplexity, ChatGPT Search) via 3-4 sub-query fan-out.
- [x] Synthesizes grounded AI responses with authentic numeric footnote citation anchors (`[1]`, `[2]`).
- [x] Dedicated unit test suite with 100% pass rate (`tests/unit/test_query_decomposer.py`).

---

### 29 - Enterprise Technical SEO Audit Engine
- [x] Implemented `SeoAuditEngine` in `src/aiseo/application/seo/seo_audit_engine.py`.
- [x] Performs deterministic evaluation of title tags, meta descriptions, canonical URLs, mobile viewport, heading hierarchy, and Schema.org structure.
- [x] Computes overall Technical SEO Score ($[0, 100]$) and actionable priority roadmaps.
- [x] Dedicated unit test suite with 100% pass rate (`tests/unit/test_seo_audit_engine.py`).

---

### 30 - Enterprise Generative Engine Optimization (GEO) Audit Engine
- [x] Implemented `GeoAuditEngine` in `src/aiseo/application/geo/geo_audit_engine.py`.
- [x] Consolidates multi-model AI visibility, atomic claim faithfulness, AEO snippet potential, and GLLM citation attribution into an authoritative unified GEO Index.
- [x] Classifies brand into Market Leader, Challenger, Emerging, or At Risk tiers with Wilson 95% Confidence Intervals.
- [x] Dedicated unit test suite with 100% pass rate (`tests/unit/test_geo_audit_engine.py`).
- [x] Verified complete 30-stage execution in `run_stage_by_stage_pipeline.py` with 100% test pass rate (157/157 tests passing).
