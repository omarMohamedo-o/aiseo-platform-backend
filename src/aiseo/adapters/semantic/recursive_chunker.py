"""Recursive structure-aware text chunker adapter."""
from __future__ import annotations

from typing import Any, ClassVar

from aiseo.domain.semantic.chunk import TextChunk
from aiseo.ports.semantic.chunker_port import ChunkerPort


class RecursiveChunker(ChunkerPort):
    """Splits text recursively across structural boundaries (paragraphs, sentences, words)."""

    DEFAULT_SEPARATORS: ClassVar[list[str]] = [
        "\n\n",
        "\n",
        ". ",
        "! ",
        "? ",
        "; ",
        ", ",
        " ",
        "",
    ]

    def __init__(self, separators: list[str] | None = None) -> None:
        self.separators = separators or self.DEFAULT_SEPARATORS

    def chunk(
        self,
        document_id: str,
        text: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        metadata: dict[str, Any] | None = None,
    ) -> list[TextChunk]:
        clean_text = text.strip()
        if not clean_text:
            return []

        chunk_size = max(10, chunk_size)
        chunk_overlap = max(0, min(chunk_overlap, chunk_size - 1))

        leaves = self._split_recursive(clean_text, 0, chunk_size)
        packed_chunks = self._pack_leaves(leaves, chunk_size, chunk_overlap)

        return [
            TextChunk.create(
                document_id=document_id,
                text=chunk_str,
                sequence=idx,
                metadata=metadata,
            )
            for idx, chunk_str in enumerate(packed_chunks)
            if chunk_str.strip()
        ]

    def _split_recursive(self, text: str, separator_idx: int, max_size: int) -> list[str]:
        if len(text) <= max_size:
            return [text]

        if separator_idx >= len(self.separators):
            # Hard split as final fallback
            return [text[i : i + max_size] for i in range(0, len(text), max_size)]

        separator = self.separators[separator_idx]
        if not separator:
            # Empty string means character-level split
            return [text[i : i + max_size] for i in range(0, len(text), max_size)]

        parts = text.split(separator)
        result: list[str] = []

        for i, part in enumerate(parts):
            # Reattach separator to preserve punctuation/formatting (except on last piece if trailing)
            piece = part if i == len(parts) - 1 else part + separator
            if not piece:
                continue

            if len(piece) <= max_size:
                result.append(piece)
            else:
                result.extend(
                    self._split_recursive(piece, separator_idx + 1, max_size)
                )

        return result

    def _pack_leaves(
        self, leaves: list[str], chunk_size: int, chunk_overlap: int
    ) -> list[str]:
        if not leaves:
            return []

        chunks: list[str] = []
        current_chunk: list[str] = []
        current_length = 0

        for leaf in leaves:
            leaf_len = len(leaf)
            if current_length + leaf_len > chunk_size and current_chunk:
                merged = "".join(current_chunk).strip()
                if merged:
                    chunks.append(merged)

                # Compute overlap for the next rolling window
                if chunk_overlap > 0:
                    overlap_acc: list[str] = []
                    overlap_len = 0
                    for prev_leaf in reversed(current_chunk):
                        if overlap_len + len(prev_leaf) <= chunk_overlap:
                            overlap_acc.insert(0, prev_leaf)
                            overlap_len += len(prev_leaf)
                        else:
                            break
                    current_chunk = overlap_acc
                    current_length = overlap_len
                else:
                    current_chunk = []
                    current_length = 0

            current_chunk.append(leaf)
            current_length += leaf_len

        if current_chunk:
            final_merged = "".join(current_chunk).strip()
            if final_merged:
                chunks.append(final_merged)

        return chunks
