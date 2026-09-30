"""RAG prompt builder: formats retrieved context and prompts for LLM consumption."""
from __future__ import annotations

from aiseo.domain.semantic.chunk import SearchResult


class RagPromptBuilder:
    """Builds context-augmented prompts with source citations and token limits."""

    DEFAULT_SYSTEM_TEMPLATE: str = (
        "You are an expert AI assistant specializing in search visibility, content auditing, and factual analysis. "
        "Use the provided context to answer accurately. If the context does not contain the answer, state that clearly."
    )

    def __init__(self, system_template: str | None = None) -> None:
        self.system_template = system_template or self.DEFAULT_SYSTEM_TEMPLATE

    def build_context_block(
        self, search_results: list[SearchResult], max_chars: int = 4000
    ) -> str:
        """Format search results into a clean markdown context block with source tags."""
        if not search_results:
            return ""

        context_parts: list[str] = ["### Relevant Reference Context:"]
        current_length = len(context_parts[0])

        for idx, result in enumerate(search_results, start=1):
            source_tag = f"Source {idx} (Doc: {result.document_id})"
            snippet = f"\n\n[{source_tag}]:\n{result.text.strip()}"
            if current_length + len(snippet) > max_chars:
                break
            context_parts.append(snippet)
            current_length += len(snippet)

        return "".join(context_parts)

    def build_prompt(
        self,
        query: str,
        search_results: list[SearchResult] | None = None,
        max_context_chars: int = 4000,
    ) -> str:
        """Compose user query and retrieved context into the final LLM prompt."""
        if not search_results:
            return query

        context_block = self.build_context_block(search_results, max_chars=max_context_chars)
        if not context_block:
            return query

        return f"{context_block}\n\n### User Question:\n{query}\n\n### Answer:"
