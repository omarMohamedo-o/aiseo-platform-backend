# Implementation roadmap

| Phase | Scope | Status |
|---|---|---|
| 1 | Foundation: structure, DI/composition root, config, logging, errors, base ports, test infra | **Done (this repo)** |
| 2 | Tenancy: tenants, users, RBAC, tenant isolation | Not started |
| 3 | Website: registration, URL validation, configuration | Partial (registration slice done) |
| 4 | Crawler: robots.txt, URL normalization, crawling, extraction, links | Not started |
| 5 | SEO: technical analyzers, SEO score, findings | Not started |
| 6 | Semantic layer: chunking, embeddings, vector search, similarity | Not started |
| 7 | ML: datasets, features, intent classifier, MLflow tracking, model registry | Ports/ONNX serving adapter scaffolded |
| 8 | Topics: clustering, topic labeling, semantic coverage | Port scaffolded, no algorithm yet |
| 9 | Entities: extraction, normalization, graph, consistency | Not started |
| 10 | AEO: questions, retrieval, reranking, answer evaluation, AEO score | Not started |
| 11 | GEO: entity/topical authority, evidence, citation, retrievability, GEO score | Not started |
| 12 | Competitors: discovery, analysis, content/semantic gaps | Not started |
| 13 | Recommendations: impact, effort, confidence, priority | Not started |
| 14 | Reporting: dashboard, JSON/HTML/PDF | Not started |
| 15 | Enterprise: observability, billing, quotas, audit, provider routing, model lifecycle, scaling | Logging done; rest not started |

Each phase follows: domain models → ports → application services → adapters
→ persistence → API → tests, then run tests/type-checker/linter and validate
dependency direction, tenant isolation, and open/closed compliance before
moving on (see `docs/architecture.md`).
