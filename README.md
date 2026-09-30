# AI SEO / AEO / GEO Platform

Enterprise search-visibility intelligence platform: SEO + AEO (Answer Engine
Optimization) + GEO (Generative Engine Optimization), built on Clean /
Hexagonal Architecture with provider-, algorithm-, and model-independent
interfaces, and MLflow-tracked ML lifecycle.

This repository currently implements **Phase 1 — Foundation** of the roadmap
in `docs/roadmap.md`: project structure, dependency injection / composition
root, configuration, structured logging, error handling, base
domain/port/adapter layers, a first vertical slice (website registration),
and the test infrastructure. See `docs/architecture.md` for the full system
design and `docs/adr/` for architectural decision records.

## Project layout

```
src/aiseo/
  domain/          # entities, value objects, domain errors — no framework imports
  application/      # use-case orchestration, depends only on ports
  ports/             # capability interfaces (llm, embeddings, clustering, ml, persistence)
  adapters/          # concrete implementations of ports (onnx, in-memory, ...)
  infrastructure/    # configuration, composition root, logging, security
  api/                # FastAPI routes, schemas, dependency wiring
tests/
  unit/               # no external services required
  integration/        # exercises the wired FastAPI app
models/               # ONNX model artifacts (see models/README.md)
dataset/               # versioned datasets used for ML training/eval
notebooks/              # exploratory ML notebooks (not part of the shipped app)
configs/                 # environment-specific configuration overlays
outputs/                  # generated reports / build outputs (gitignored)
```

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) for dependency management

## Getting started

```bash
uv sync --all-extras
uv run pytest
uv run main.py            # starts the API on http://localhost:8000
```

Or with Docker:

```bash
docker build -t aiseo-platform .
docker run -p 8000:8000 aiseo-platform
```

## Example request

```bash
curl -X POST http://localhost:8000/api/v1/websites \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: 11111111-1111-1111-1111-111111111111" \
  -d '{"url": "https://example.com"}'
```

## Testing

```bash
uv run pytest                     # unit + integration tests
uv run pytest --cov=aiseo         # with coverage
uv run mypy src                   # static type checking
uv run ruff check src tests       # linting
```

## ML / model serving

Classical ML and lightweight neural models are served via **ONNX Runtime**
through the `ModelProvider` port (`src/aiseo/ports/ml/model_provider.py`),
with `OnnxModelProvider` as the concrete adapter
(`src/aiseo/adapters/ml/onnx_model_provider.py`). Training happens offline
and is tracked in **MLflow** (experiment tracking, model registry); only the
exported `.onnx` artifact and its registered version are loaded at serving
time. `opencv-python-headless` is available for any image/document
preprocessing needed ahead of model inference. A future high-throughput
inference path (ONNX Runtime + OpenCV from C++) can replace the Python
serving adapter without changing the `ModelProvider` port or any business
logic — see `docs/adr/0009-onnx-model-serving.md`.

## Status

Phase 1 (Foundation) only. See `docs/roadmap.md` for the full 15-phase plan.
