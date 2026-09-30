# ADR-0001: Clean / Hexagonal Architecture

## Context
The platform must support swapping LLM providers, embedding providers,
clustering algorithms, and ML models without touching SEO/AEO/GEO business
logic (the core requirement, section 4 of the spec).

## Decision
Adopt Clean/Hexagonal Architecture with strict dependency direction
(API → Application → Domain; Infrastructure implements Ports). Domain and
Application code depend only on abstract ports; concrete vendor SDKs live
exclusively in `adapters/`.

## Alternatives considered
- Simple layered MVC: rejected — leads to vendor SDK types leaking into
  business logic, violates the Open/Closed requirement.
- Microservices from day one: rejected — see ADR-0010 (modular monolith).

## Consequences
- More upfront interfaces/boilerplate.
- New providers/algorithms are additive (adapter + registration), verified
  by `tests/unit/test_registry.py` and provider/algorithm contract tests.
