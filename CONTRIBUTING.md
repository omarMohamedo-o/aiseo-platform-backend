# Contributing to AISEO Platform

> Maintainer & Author: **`@omarMohamedo-o`**  
> Operating Agreement: [CLAUDE.md](CLAUDE.md) · Intent & Policies: [INTENT.md](INTENT.md) · Working Plan: [PLAN.md](PLAN.md)

---

## 1. Branch & Development Flow

- Work on feature/fix branches: `feat/<short-name>` or `fix/<short-name>`.
- Every change is reviewed and merged into `main` by the operator.
- Never push directly to `main`. Never force-push.

---

## 2. Commit Standards

- **Commit Message Format**: `<type>: <summary in present tense>`
  - Accepted types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`.
- **Atomic Commits**: One finished logical change per commit = the code + its tests + its doc updates together.
- **Strict Prohibition on AI Attribution**:
  - **Zero AI tool attribution anywhere:** No "Claude", "Gemini", "ChatGPT", "Copilot", "Co-Authored-By", or "Generated with..." in commits, commit trailers, PR titles/bodies, code comments, docstrings, docs, contributor lists, or release notes.
  - The operator (`@omarMohamedo-o`) is the sole author and contributor of this codebase.
- **Explicit Staging Only**:
  - Use `git add <explicit-file-path>`, never `git add -A` or `git add .`.
  - Scratch scripts and debug experiments never enter the repository.
- **Zero Secrets**:
  - Never commit raw API keys or tokens. All credentials must use the AES-256 encrypted tenant vault.

---

## 3. Bug Fix Protocol

1. **Test-First**: Write a failing unit or integration test reproducing the exact issue before touching code.
2. **Preserve the Test**: Do not alter, weaken, or skip the test assertion to pass.
3. **Fix the Root Cause**: Fix the underlying domain/adapter issue and confirm the test turns green.

---

## 4. Code Quality & Architectural Integrity

- **Clean / Hexagonal Architecture**:
  - Domain layer must never import frameworks (FastAPI, SQLAlchemy, Redis, OpenAI, ONNX).
  - Business logic depends strictly on abstract Ports.
- **Strict Typing**:
  - Enforce `mypy` with `strict = true`. No untyped functions or unannotated parameters.
- **Linting & Formatting**:
  - Code must pass `ruff check src tests` with zero errors.
