"""Unit tests for recursive text chunker."""
from __future__ import annotations

from aiseo.adapters.semantic.recursive_chunker import RecursiveChunker


def test_chunker_empty_or_whitespace_text() -> None:
    chunker = RecursiveChunker()
    assert chunker.chunk("doc1", "") == []
    assert chunker.chunk("doc1", "   \n\n   ") == []


def test_chunker_short_text_single_chunk() -> None:
    chunker = RecursiveChunker()
    chunks = chunker.chunk("doc1", "This is a brief text within limits.", chunk_size=100)
    assert len(chunks) == 1
    assert chunks[0].id == "doc1:0"
    assert chunks[0].text == "This is a brief text within limits."
    assert chunks[0].sequence == 0


def test_chunker_splits_by_paragraphs() -> None:
    chunker = RecursiveChunker()
    p1 = "Paragraph one with some interesting background information."
    p2 = "Paragraph two diving deeper into specific technical details."
    text = f"{p1}\n\n{p2}"

    chunks = chunker.chunk("doc1", text, chunk_size=len(p1) + 5, chunk_overlap=0)
    assert len(chunks) == 2
    assert chunks[0].text == p1
    assert chunks[1].text == p2


def test_chunker_splits_by_sentences_when_paragraphs_too_large() -> None:
    chunker = RecursiveChunker()
    s1 = "First sentence is clear."
    s2 = "Second sentence is concise."
    text = f"{s1} {s2}"

    chunks = chunker.chunk(
        "doc1", text, chunk_size=max(len(s1), len(s2)) + 2, chunk_overlap=0
    )
    assert len(chunks) == 2
    assert s1 in chunks[0].text
    assert s2 in chunks[1].text


def test_chunker_preserves_metadata_and_sequences() -> None:
    chunker = RecursiveChunker()
    long_text = " ".join([f"Word{i}" for i in range(100)])
    meta = {"source": "test_url", "tenant": "111"}
    chunks = chunker.chunk("doc42", long_text, chunk_size=50, chunk_overlap=10, metadata=meta)

    assert len(chunks) > 1
    for idx, c in enumerate(chunks):
        assert c.document_id == "doc42"
        assert c.sequence == idx
        assert c.metadata["source"] == "test_url"
        assert c.metadata["tenant"] == "111"
        assert c.metadata["sequence"] == str(idx)
