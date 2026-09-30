# 3. Pluggable AI Model and Provider Architecture

Date: 2026-09-15

## Status

Accepted

## Context

The GEO Intelligence Platform requires analyzing website content using multiple AI modalities (Text, Vision, Embeddings) for various tasks: content analysis, entity extraction, structural reasoning, and visual layout evaluation. 

Hardcoding specific LLMs or Cloud Providers (e.g., OpenAI, Gemini, Claude) directly into the business logic (Domain/Application layers) would result in strict coupling, vendor lock-in, and inflexibility. We need the ability to easily swap between:
- Local models (e.g., LFM2.5, Qwen, Llama, BGE embeddings) to optimize for privacy and cost.
- Cloud providers (e.g., OpenAI, Gemini) to handle complex reasoning or large context tasks.
- Different models for different tasks (e.g., a lightweight local model for classification, and a heavy cloud model for deep reasoning).

Furthermore, the core pipeline goes beyond simple LLM wrapping; it involves massive Data Engineering, Feature Extraction, and Competitor Benchmarking.

## Decision

We will design a **Model/Provider Abstraction Layer** using strict Hexagonal Architecture principles. 

1. **Protocol Interfaces**: We will define standard `Protocol` interfaces in the ports layer for each modality, completely decoupled from any specific provider SDK:
   - `TextModel` (for generation and reasoning)
   - `VisionModel` (for image and layout understanding)
   - `EmbeddingModel` (for semantic vectors)

2. **Adapters**: Concrete implementations (Adapters) will wrap specific models/providers (e.g., `GeminiTextModel`, `LocalLFMVisionModel`, `BGEEmbeddingModel`). The Application layer will strictly interact with the Protocols, unaware of the underlying adapter.

3. **Dependency Injection**: Selection of the active model for a given task will be managed via configuration (e.g., `yaml`) and wired via the Composition Root (Dependency Injection). This allows runtime swapping of models (e.g., using Gemini for fallback, or Local for privacy) without modifying business logic.

4. **AI Router**: Future iterations will implement an AI Router to dynamically select the most appropriate registered model based on Task Complexity, Cost, and Privacy constraints.

## Consequences

- **Flexibility**: The engineering team can swap out OpenAI for a local ONNX/llama.cpp model without touching the GEO evaluation logic.
- **Testability**: We can easily mock the `TextModel` or `VisionModel` interfaces for fast, deterministic unit tests.
- **Complexity**: It introduces slight overhead in managing abstractions and standardizing inputs/outputs across fundamentally different provider APIs (e.g., normalizing token usage, streaming, and error handling).
