# AI SEO / AEO / GEO Platform — Project Status & Technology Stack

This document details **what has been built so far**, the **complete suite of tools and dependencies**, and the **explicit architectural rationale for each tool**.

---

## 1. What We Made Until Now

The project is built on **Clean / Hexagonal Architecture** following Domain-Driven Design (DDD) principles. This guarantees that domain logic remains decoupled from third-party frameworks, LLM providers, and databases.

### Key Milestones Completed

#### 1. Core Architecture & Layers
* **Domain Layer (`src/aiseo/domain/`)**:
  * **Entities & Aggregates**:
    * `Website`: Manages registration, crawling state transitions (`PENDING` → `CRAWLING` → `ACTIVE`/`FAILED`), and discovered URLs.
    * `WebPage`: Manages page discovery, scraping state (`DISCOVERED` → `SCRAPING` → `SCRAPED`/`FAILED`), and structured text extraction.
  * **Value Objects (`src/aiseo/domain/value_objects.py`)**: Immutable types with strict validation: `TenantId`, `WebsiteId`, `PageId`, `Url`, and `Score`.
  * **Domain Errors (`src/aiseo/domain/errors.py`)**: Normalized domain exception hierarchy (`InvalidUrlError`, `WebsiteAlreadyExistsError`, `WebsiteNotFoundError`, `ProviderRateLimitError`, `ProviderTimeoutError`, etc.).
* **Ports Layer (`src/aiseo/ports/`)**:
  * Capability interfaces isolating third-party vendors from business logic:
    * `LlmProvider` (`ports/llm`): Generative AI text and structured output calls.
    * `EmbeddingProvider` (`ports/embeddings`): Vector embeddings generation.
    * `ClusteringAlgorithm` (`ports/clustering`): Topic clustering algorithms.
    * `ModelProvider` (`ports/ml`): Machine learning model inference.
    * `WebsiteRepository` (`ports/persistence`): Website data storage.
    * `CrawlerPort` (`ports/crawler`): Page discovery and link traversal.
    * `ScraperPort` (`ports/scraper`): Clean content and DOM extraction.
* **Adapters Layer (`src/aiseo/adapters/`)**:
  * `OnnxModelProvider` (`adapters/ml`): Low-latency model serving via **ONNX Runtime** (tested with `intent_classifier_v1.onnx`).
  * `InMemoryWebsiteRepository` (`adapters/persistence`): In-memory storage with explicit tenant isolation filtering.
  * `HttpxCrawler` (`adapters/crawler`): Asynchronous page discovery within the target domain using `httpx` and `BeautifulSoup4`.
  * `TrafilaturaScraper` (`adapters/scraper`): Web extraction combining `trafilatura` (boilerplate removal) and `BeautifulSoup4` (metadata, title, language, headings).
* **Application Services (`src/aiseo/application/`)**:
  * `RegisterWebsiteService`: Use-case service for validating and persisting new tenant websites.
  * `CrawlAndExtractService`: Use-case orchestrator coordinating page discovery via `CrawlerPort` and structured content extraction via `ScraperPort`.
* **Infrastructure Layer (`src/aiseo/infrastructure/`)**:
  * **Settings (`settings.py`)**: Type-safe configuration via Pydantic (`AISEO_` environment prefix, YAML base overlay at `configs/base.yaml`).
  * **Composition Root (`composition_root.py`)**: Application container managing dependency injection.
  * **Registry (`registry.py`)**: Extensible provider/algorithm container adhering to the Open/Closed Principle.
  * **Observability**: Structured JSON logging via `structlog`.
* **API Layer (`src/aiseo/api/`)**:
  * FastAPI application with lifespan management and global exception handlers.
  * Tenant resolution dependency (`X-Tenant-Id` header).
  * Working REST endpoint: `POST /api/v1/websites`.

#### 2. Verification & Testing
* **24 automated tests** passing across unit and integration suites (`pytest tests`).
* Static type checking with `mypy` (`strict = true`).
* Linting and formatting configured with `ruff`.
* Docker containerization via `Dockerfile`.

---

## 2. Tools & Libraries: Why We Used Each One

| Category | Tool / Library | Why We Used It (Architectural Justification) |
|---|---|---|
| **Package Management** | **uv** | Ultra-fast Python package and project manager written in Rust. Replaces `pip`, `poetry`, and `virtualenv`, providing reproducible builds with `uv.lock` in milliseconds. |
| **API Framework** | **FastAPI** | High-performance, asynchronous web framework based on Starlette and Pydantic. Provides native `async/await`, automatic OpenAPI / Swagger documentation, and dependency injection for clean routing. |
| **ASGI Server** | **Uvicorn** | Lightning-fast ASGI web server implementation for Python based on `uvloop` and `httptools`. |
| **Configuration** | **Pydantic & Pydantic-Settings** | Type-safe environment variable parsing (`SettingsConfigDict`), deep nested configuration (e.g. `AISEO_LLM__MODEL`), and data validation for API schemas. |
| **Observability** | **Structlog** | Enterprise structured JSON logging. Allows contextual logging (attaching `tenant_id`, `request_id`, execution duration) essential for distributed tracing and production debugging. |
| **Database & ORM** | **SQLAlchemy (2.0)** | The standard Python SQL toolkit and ORM. Uses modern 2.0 type-safe syntax and async sessions (`AsyncSession`) for clean interaction with PostgreSQL. |
| **Database Migrations** | **Alembic** | Lightweight database migration tool for SQLAlchemy. Tracks and manages schema changes version-by-version across environments. |
| **Database Drivers** | **Psycopg 3 & Asyncpg** | Modern, high-performance PostgreSQL drivers. Supports asynchronous database queries, connection pooling, and binary vector operations with `pgvector`. |
| **Vector Storage** | **PostgreSQL + pgvector** | Integrates relational data and high-dimensional vector embeddings in a single database, eliminating the operational overhead of a separate vector database in early phases. |
| **Task Queue & Cache** | **Redis** | In-memory key-value store used as the broker for background task queues, response caching, and API rate limiting. |
| **Distributed Jobs** | **Celery** | Asynchronous task queue for long-running jobs (crawling entire websites, generating bulk embeddings, running GEO scans) without blocking HTTP endpoints. |
| **HTTP Client** | **HTTPX** | Fully featured async HTTP client with HTTP/2 support, used for crawling web pages, sitemaps, robots.txt, and calling external AI APIs. |
| **Web Scraping** | **Trafilatura** | Specialized library for web text discovery and extraction. Accurately extracts main article content while filtering out boilerplate (navigation bars, ads, footers, sidebars). |
| **HTML Parsing** | **BeautifulSoup4 & Lxml** | Fast, forgiving HTML and XML parsing for extracting specific DOM tags, structured metadata, OpenGraph tags, JSON-LD schemas, and heading hierarchies. |
| **Headless Browser** | **Playwright** *(planned)* | Automated browser execution to render dynamic, client-side JavaScript sites (React/Vue/Angular) that basic HTTP scrapers cannot extract. |
| **Natural Language Processing** | **spaCy** | Industrial-strength NLP library for Named Entity Recognition (NER), part-of-speech tagging, and linguistic analysis to detect company names, products, competitors, and key claims. |
| **ML Inference** | **ONNX Runtime** | High-performance, cross-platform inference engine. Serves lightweight neural models and classifiers with low memory overhead, decoupling inference from heavy training frameworks. |
| **Classical ML & Math** | **Scikit-learn & NumPy** | Fast vector operations, cosine similarity calculations, TF-IDF analysis, and topic clustering algorithms (`KMeans`, `HDBSCAN`). |
| **Computer Vision** | **OpenCV (Headless)** | Image preprocessing for visual SEO, screenshot rendering analysis, and document layout parsing without GUI overhead. |
| **MLOps & Lifecycle** | **MLflow** | Full machine learning lifecycle tracking: experiment logging, hyperparameter tracking, model evaluation, and model registry before exporting to ONNX. |
| **Testing** | **Pytest & Pytest-Asyncio** | Standard Python testing framework with native support for asynchronous test cases and dependency fixtures. |
| **Code Quality** | **Mypy** | Static type checker enforcing strict type safety (`strict = true`) to prevent runtime type errors. |
| **Linting & Formatting** | **Ruff** | Extremely fast Python linter and code formatter written in Rust, replacing flake8, black, and isort. |
| **Containerization** | **Docker** | Ensures consistent runtime environments and multi-stage container deployment across local dev, CI/CD, and production. |

---

## 3. What Needs to Be Done Next

The full 15-phase roadmap is defined in [`docs/roadmap.md`](./roadmap.md). The immediate next development priorities are:

1. **Phase 2: Multi-Tenancy & Authentication**:
   - User entity, tenant organization models, password hashing, and JWT/OAuth2 authentication.
   - Role-Based Access Control (RBAC) and API Key generation.
2. **Phase 3: Database Persistence (PostgreSQL + Alembic)**:
   - Implement `SqlAlchemyWebsiteRepository` and `SqlAlchemyPageRepository`.
   - Setup Alembic database migrations and PostgreSQL connection pools.
3. **Phase 4: Crawler & Scraper Productionization**:
   - Add Celery background task wiring for `CrawlAndExtractService`.
   - Add `robots.txt` and `sitemap.xml` parsing, plus Playwright fallback for JS-heavy websites.
4. **Phase 5 & 6: Semantic Layer & Embeddings**:
   - Content chunking and `pgvector` storage.
   - Adapters for OpenAI embeddings (`text-embedding-3-small`) and open-source models (`sentence-transformers`).
5. **Phase 10 & 11: AEO & GEO Scanners**:
   - Question generation and LLM query simulation (testing brand presence in ChatGPT, Claude, Gemini, and Perplexity).
   - Unified GEO Visibility Score computation and actionable recommendation engine.
