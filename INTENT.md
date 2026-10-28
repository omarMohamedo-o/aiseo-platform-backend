# INTENT - AISEO / AEO / GEO Platform Vision, Decisions & Policies

> Maintainer & Author: **`@omarMohamedo-o`**  
> Companion Docs: [PLAN.md](PLAN.md) (Execution checklist) · [CLAUDE.md](CLAUDE.md) (Working agreement) · [docs/architecture.md](docs/architecture.md)

---

## 1. Core Mission & Goal

Build an enterprise-grade **Search Visibility Intelligence Platform** that transforms how brands audit, optimize, and dominate modern search across **traditional search engines (Google, Bing)**, **answer engines (Featured Snippets, Siri, Alexa)**, and **generative AI engines (ChatGPT, Google Gemini, Claude, Perplexity)**.

Instead of only checking *"What is my Google keyword ranking?"*, the platform answers:
> *"When a prospective buyer asks an AI engine for solutions in our market, does the AI know us? Does it recommend us? Does it cite our domain? And are its claims grounded and factual, or hallucinated?"*

The system is built on **Clean / Hexagonal Architecture (Domain-Driven Design)**, ensuring total decoupling from commercial LLM providers, database drivers, and frameworks.

---

## 2. Key Architectural Decisions (ADR Summary)

| Area | Decision | Architectural Rationale |
|---|---|---|
| **Core Architecture** | **Clean / Hexagonal Architecture** | Strict dependency inversion: Domain depends on nothing; Application depends only on abstract Ports; Adapters implement Ports. Vendor SDKs never touch business logic. |
| **Provider Independence** | **Open/Closed Generic Registry[T]** | Adding a new LLM provider (e.g. Mistral, DeepSeek) requires adding an adapter and registering it in the composition root. No `if provider == "..."` chains in business code. |
| **ML Inference** | **ONNX Runtime (C++) + MLflow** | Sub-5ms CPU inference for search intent classification. Decoupled from heavy training frameworks. Models trained in MLflow, exported to `.onnx`. |
| **Vector Indexing** | **PostgreSQL + pgvector** | Unifies transactional tenant metadata and high-dimensional vector embeddings in a single database, eliminating the operational overhead of fragmented vector DBs. |
| **Security & Privacy** | **AES-256 Fernet Tenant Vault** | Client API credentials (OpenAI, Gemini, Serper) encrypted at rest with hardware-grade authenticated cryptography. Strict tenant data isolation. |
| **Truth & Grounding** | **Hallucination & Grounding Engine** | Incorporates proven patterns from `HistoryVerse-Chatbot`: Mathematical grounding ratios, citation verification, and RAG faithfulness guardrails. |
| **Retrieval Prediction**| **Hybrid BM25 + Vector + Reranking** | Combines lexical keyword precision and dense semantic vectors with cross-encoder reranking to predict snippet capture with 90%+ accuracy. |
| **Efficiency** | **Tiered Semantic Caching** | Response hashing and semantic cosine similarity thresholding to reduce redundant external LLM invocations and prevent HTTP 429 rate limits. |

---

## 3. Standing Policies

1. **Clean Code & DDD Strictness**:
   - Entities and Value Objects (`TenantId`, `WebsiteId`, `Url`, `Score`) enforce invariants upon construction.
   - Domain errors are mapped into a unified hierarchy (`domain/errors.py`).
2. **Deterministic Fallbacks**:
   - Every external generative feature (summary generation, question generation, answer auditing) must have a deterministic mathematical/rule-based fallback when external APIs are unreachable.
3. **Multi-Tenancy by Design**:
   - Every tenant aggregate carries `TenantId`. Repositories filter strictly by `tenant_id`. No global ambient state.
4. **Test-First Quality Standard**:
   - Every bug gets a reproduction test first. Unit and integration tests must pass cleanly.
5. **No AI Attribution**:
   - The operator (`@omarMohamedo-o`) is the sole author. No assistant trailers or generated watermarks anywhere in the repository.

---

## 4. Operator Commands Glossary

| Operator Command | Meaning & Action |
|---|---|
| `"progress"` / `"table"` | Display the updated stage table from `PLAN.md`. |
| `"next"` / `"continue"` | Proceed to implement the next unchecked stage in `PLAN.md`. |
| `"test"` / `"pytest"` | Run the test suite and verify coverage and type safety. |
| `"solve this"` | Fix the root cause with a failing test first; no workarounds or skips. |
| `"rebuild deck"` | Recompile the 16-page sales pitch and technical architecture PDFs. |
