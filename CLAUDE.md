# AISEO Platform — Project Context & Working Agreement

> Auto-loaded every session. **This project is strictly documented — use the docs, keep them current.**
> Project: **Enterprise Search & Generative Engine Optimization (AISEO / AEO / GEO) Platform**
> Architecture: **Clean / Hexagonal Architecture (Domain-Driven Design)**
> Maintainer / Author: **`@omarMohamedo-o`**

---

## 1. What This Project Is

An **Enterprise Search Visibility Intelligence Platform** unifying:
1. **SEO (Search Engine Optimization)**: Traditional web indexing, title tags, heading hierarchies, crawlability.
2. **AEO (Answer Engine Optimization)**: Direct answer snippet capture, Google Featured Snippets, Siri/voice assistant matching.
3. **GEO (Generative Engine Optimization)**: Citations, brand mentions, and favorable recommendations across LLMs (ChatGPT, Gemini, Claude, Perplexity).

Built on **Clean / Hexagonal Architecture** with provider-, algorithm-, and model-independent interfaces, sub-5ms ONNX model serving, and MLflow-tracked ML lifecycle.

---

## 2. Standing Rules & Working Agreement

1. **Clean Hexagonal Architecture is Law**:
   - `domain/`: Pure domain logic, entities, value objects, domain errors. **Zero imports of FastAPI, SQLAlchemy, OpenAI, Redis, or ONNX.**
   - `ports/`: Capability interfaces defining contracts (`LlmProvider`, `CrawlerPort`, `ScraperPort`, `ModelProvider`, `GroundingGuardPort`, `RerankerPort`, `VaultPort`).
   - `adapters/`: Concrete implementations of ports. All third-party vendor SDKs live strictly here.
   - `application/`: Use-case orchestration depending only on ports.
   - `infrastructure/`: Composition root, dependency injection, settings, logging, encryption.
   - `api/`: FastAPI routes, request/response DTO schemas, and dependency wiring.
2. **Author Attribution**:
   - The operator (`@omarMohamedo-o`) is the maintainer and author.
   - No assistant names, "Co-Authored-By", or tool-generated footers in commits, code comments, docs, or release notes.
3. **Test-First & Regression Prevention**:
   - Every bug must have a failing unit test reproducing it before fixing.
   - Never skip, allowlist, or weaken an assertion to turn a test green.
   - Target 100% type safety with `mypy` (`strict = true`) and clean linting via `ruff`.
4. **Docs Ship With Code in the Same Pass**:
   - When a step or domain feature is added or modified, update `PLAN.md`, `docs/architecture.md`, and relevant module docs in the same turn.
5. **Secrets & Tenant Privacy**:
   - Secrets and external API keys never enter git or logs. All credentials are encrypted via AES-256 in the tenant vault.
   - Every request and repository query enforces explicit `TenantId` isolation.

---

## 3. Project Directory Map

```
src/aiseo/
  domain/            # pure business entities, value objects, domain errors
  application/       # use-case orchestration (analysis, rag, reporting, websites, evaluation)
  ports/             # capability interfaces (crawler, scraper, semantic, llm, ml, evaluation, cache)
  adapters/          # concrete implementations (httpx, trafilatura, pgvector, onnx, openai, gemini)
  infrastructure/    # configuration, composition root, settings, logging, vault
  api/               # FastAPI endpoints, routes, dependencies, DTO schemas
tests/
  unit/              # isolated fast unit tests
  integration/       # end-to-end multi-stage pipeline tests
models/              # ONNX model computational graphs (e.g. intent_classifier_v1.onnx)
configs/             # environment overlays (base.yaml, etc.)
outputs/             # generated executive slide decks, reports, PDFs
docs/                # architectural specifications, ADRs, roadmaps
```

---

## 4. Key Developer Commands

```bash
uv sync --all-extras                    # Sync dependencies via uv
uv run pytest                           # Run test suite
uv run mypy src                         # Static type checking (strict mode)
uv run ruff check src tests             # Linting
python main.py                          # Start local API server on http://localhost:8000
python generate_sales_pitch_deck.py     # Recompile Client Sales Pitch PDF
python generate_technical_architecture_deck.py # Recompile Technical Deep-Dive PDF
```
