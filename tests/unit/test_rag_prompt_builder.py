"""Unit tests for RAG prompt builder."""
from __future__ import annotations

from aiseo.application.rag.prompt_builder import RagPromptBuilder
from aiseo.domain.semantic.chunk import SearchResult


def test_rag_prompt_builder_without_search_results() -> None:
    builder = RagPromptBuilder()
    prompt = builder.build_prompt("What is SEO?")
    assert prompt == "What is SEO?"


def test_rag_prompt_builder_with_results() -> None:
    builder = RagPromptBuilder()
    results = [
        SearchResult(
            chunk_id="doc1:0",
            document_id="https://example.com/about",
            text="Acme provides the premier AI SEO automation engine.",
            similarity=0.95,
        ),
        SearchResult(
            chunk_id="doc2:0",
            document_id="https://example.com/pricing",
            text="Plans start at $49/mo with unlimited scans.",
            similarity=0.88,
        ),
    ]

    prompt = builder.build_prompt("How much does Acme cost?", search_results=results)
    assert "### Relevant Reference Context:" in prompt
    assert "https://example.com/about" in prompt
    assert "https://example.com/pricing" in prompt
    assert "### User Question:\nHow much does Acme cost?" in prompt
    assert "### Answer:" in prompt
