# ADR-0002: Provider abstraction via capability-specific ports

## Context
The platform must integrate multiple LLM, embedding, reranking, search, and
clustering vendors without `if provider == "..."` chains in business logic.

## Decision
Define one narrow interface per capability (`LlmProvider`,
`EmbeddingProvider`, `ClusteringAlgorithm`, `ModelProvider`, ...) rather than
one monolithic `AiProvider`. Resolve concrete implementations through an
injectable `Registry[T]` keyed by configuration, built once in the
composition root.

## Alternatives considered
- Single `AiProvider` interface: rejected — forces every implementation to
  support every capability, violates Interface Segregation.
- Conditional dispatch (`if/elif` on provider name) in services: rejected —
  violates Open/Closed, explicitly forbidden by the spec (section 14).

## Consequences
- Adding a provider is additive: implement port → register → configure.
- Capability mismatches (e.g. Anthropic has no embeddings) are explicit and
  caught at registration time, not by a runtime crash deep in business logic.
