# ADR-0004: Adopt Lean Modular Microservices (5 Deployable Services)

Status: Accepted
Lead Architect: Omar Mohamed Abdelsalam (@omarMohamedo-o)
Platform: EsooAI Enterprise Platform

## Context & Decision

Adopt a modular architecture with clear domain boundaries and independently scalable deployment units without introducing premature distributed-system complexity.

## Initial 5 Deployable Services

1. **API Layer (`esoo-api`)**
   - API Gateway
   - Customer API
   - Admin API
   - Authentication and tenant management

2. **Engine Service (`esoo-engine`)**
   - Website crawler
   - Technical SEO analysis
   - AEO analysis
   - GEO analysis
   - GLLM visibility analysis
   - Visibility scoring

3. **Intelligence Service (`esoo-intelligence`)**
   - Search trends
   - Intent classification
   - Buyer persona query synthesis
   - Knowledge graph analysis
   - Competitor intelligence

4. **Recommendation Service (`esoo-recommendation`)**
   - Recommendation generation
   - Impact-versus-effort prioritization
   - Remediation plans
   - CMS integrations
   - Evidence and recommendation verification

5. **Worker Service (`esoo-worker`)**
   - Asynchronous task execution
   - Scheduled audits
   - Background processing
   - Report generation
   - Webhook notifications

## Shared Packages & Infrastructure

- Shared Core: domain contracts, common models, validation and utilities.
- PostgreSQL and pgvector.
- Redis and Celery.
- Object storage for audit artifacts and evidence.
- Centralized logging, metrics and tracing.

## Mandatory Engineering Principles

- Strict modular boundaries.
- Tenant isolation and RBAC.
- Versioned API and event contracts.
- Idempotent background processing.
- No uncontrolled cross-service database writes.
- Independent deployment capability.
- Evidence-based SEO/GEO scoring: Zero fake, dummy, or mock data.
- Reproducible validation and audit trails.
- No brand names in variable identifiers.
- Single-letter variables strictly banned.
- No unnecessary microservice fragmentation.

## Future Extraction Strategy

Services such as the crawler, GEO visibility engine, AI inference engine and CMS execution engine may become independent deployments when actual scaling, reliability or ownership requirements justify the separation.

Final principle: Build for independent scalability without introducing unnecessary distributed-system complexity.
