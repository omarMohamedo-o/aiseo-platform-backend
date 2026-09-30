# Architecture

## 1. System purpose

An **Enterprise Search Visibility Intelligence Platform** covering SEO,
AEO (Answer Engine Optimization), and GEO (Generative Engine Optimization).
Not an LLM wrapper, not an MLflow app, not a crawler — those are
implementation details behind ports.

## 2. Bounded contexts

| Context | Responsibility |
|---|---|
| Websites | Registration, lifecycle status of a tenant's site |
| Crawling | Fetching pages, respecting robots.txt, extracting links |
| Content Intelligence | Page/content extraction, chunking |
| Semantic | Embeddings, vector search, similarity |
| ML | Feature engineering, model inference, MLflow-tracked lifecycle |
| Topics | Clustering, topic labeling |
| Entities | Extraction, knowledge graph, consistency checks |
| Questions / AEO | Question discovery, retrieval, reranking, answer evaluation |
| GEO | Entity/topical authority, evidence, citation, retrievability |
| Competitors | Competitor discovery and gap analysis |
| Recommendations | Prioritized, evidence-linked action items |
| Scoring | Deterministic, versioned, explainable SEO/AEO/GEO scores |
| Reporting | JSON/HTML/PDF report generation |

## 3. Dependency direction

```
API → Application → Domain
Infrastructure/Adapters → implement → Ports (used by Application/Domain)
```

Domain never imports SQLAlchemy, FastAPI, OpenAI SDK, MLflow SDK, Playwright,
Redis, or onnxruntime directly. Only `adapters/*` and `infrastructure/*` may.

## 4. Module structure

```
src/aiseo/
  domain/            entities, value objects, domain errors
  application/        use-case orchestration (depends only on ports)
  ports/               capability interfaces: llm, embeddings, clustering, ml, persistence
  adapters/             concrete port implementations: onnx, in-memory, (future: openai, hdbscan, sqlalchemy, mlflow)
  infrastructure/        configuration, composition root, logging, security, database, observability
  api/                    FastAPI routes, DTOs, dependency wiring
```

## 5. Ports implemented in Phase 1

- `LlmProvider` (`ports/llm`) — generate / generate_structured, no concrete adapter yet
- `EmbeddingProvider` (`ports/embeddings`) — no concrete adapter yet
- `ClusteringAlgorithm` (`ports/clustering`) — no concrete adapter yet
- `ModelProvider` (`ports/ml`) — **implemented**: `OnnxModelProvider` (ONNX Runtime)
- `WebsiteRepository` (`ports/persistence`) — **implemented**: `InMemoryWebsiteRepository`
  (a SQLAlchemy/PostgreSQL adapter is a drop-in replacement in Phase 2/3)

## 6. Provider / algorithm independence (Open/Closed)

Selection is configuration-driven (`infrastructure/configuration/settings.py`)
and resolved through an injectable `Registry[T]`
(`infrastructure/configuration/registry.py`) owned by the composition root
(`infrastructure/configuration/composition_root.py`). No `if provider == "..."`
chains appear in business logic — see `tests/unit/test_registry.py` for the
open/closed contract test.

Adding a new LLM/embedding/clustering/ranking provider or algorithm means:
add adapter → register in composition root → add config value → add contract
test. No existing SEO/AEO/GEO/orchestration logic changes.

## 7. Multi-tenancy

Every domain aggregate that is tenant-owned carries a `TenantId` value
object. The API layer resolves the tenant from the request
(`api/dependencies/tenant.py`) and passes it explicitly into every
application service call — there is no ambient/global tenant context.
Repositories filter by tenant explicitly (see
`InMemoryWebsiteRepository.list_for_tenant` /
`test_register_website_enforces_tenant_isolation`).

## 8. ML / MLflow architecture (target — see ADR-0003, ADR-0009)

```
Dataset → Feature Set → Experiment (MLflow) → Training Run → Metrics/Artifacts
  → Model → Model Registry → Evaluation → Staging → Production → Monitoring
```

Training and evaluation are tracked in MLflow through an `ExperimentTracker`
/ `ModelRegistry` abstraction (not yet implemented — Phase 7). Only the
**exported ONNX artifact** and its registered version are loaded at serving
time through `ModelProvider` → `OnnxModelProvider`. Business code never
depends on `mlflow`, `sklearn`, or `onnxruntime` types directly — only on
`Prediction` / `FeatureVector` (`ports/ml/model_provider.py`).

## 9. Error handling

All provider/framework exceptions are normalized into the hierarchy in
`domain/errors.py` (`ProviderRateLimitError`, `ProviderTimeoutError`,
`InvalidModelOutputError`, ...). Business code only ever catches these.

## 10. Roadmap

See `docs/roadmap.md` for the full 15-phase implementation plan. This
repository currently implements **Phase 1 — Foundation** plus a first
vertical slice (`POST /api/v1/websites`) to prove the architecture end to
end: API → application service → domain aggregate → repository port →
in-memory adapter, fully tested.
