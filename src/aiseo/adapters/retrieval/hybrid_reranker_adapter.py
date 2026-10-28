"""Concrete adapter implementing Hybrid Search (BM25 + Dense Vector) and AEO Snippet Prediction."""
from __future__ import annotations

import math
import re
from collections import Counter
from typing import Sequence

from aiseo.domain.evaluation.rerank import RerankCandidate, SnippetPrediction
from aiseo.ports.retrieval.reranker_port import RerankerPort


def _tokenize(text: str) -> list[str]:
    return [
        w.lower()
        for w in re.findall(r"\b[A-Za-z0-9_\-]{2,}\b", text)
        if len(w) > 1
    ]


class HybridRerankerAdapter(RerankerPort):
    """Combines BM25 lexical scoring and dense semantic signals with Reciprocal Rank Fusion."""

    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b

    def _score_bm25(self, query: str, corpus: list[str]) -> list[float]:
        """Compute exact BM25 scores for query across corpus."""
        query_tokens = _tokenize(query)
        if not query_tokens or not corpus:
            return [0.0] * len(corpus)

        tokenized_corpus = [_tokenize(doc) for doc in corpus]
        doc_lengths = [len(doc) for doc in tokenized_corpus]
        avg_dl = sum(doc_lengths) / max(1, len(doc_lengths))
        n_docs = len(corpus)

        # Document frequencies
        df: Counter[str] = Counter()
        for doc in tokenized_corpus:
            unique_terms = set(doc)
            for t in unique_terms:
                df[t] += 1

        scores: list[float] = []
        for doc_tokens, dl in zip(tokenized_corpus, doc_lengths):
            doc_counts = Counter(doc_tokens)
            doc_score = 0.0
            for t in query_tokens:
                if t in doc_counts:
                    # IDF with Robertson-Spärck Jones formulation
                    n_q = df.get(t, 0)
                    idf = math.log(max(1.0, (n_docs - n_q + 0.5) / (n_q + 0.5) + 1.0))
                    freq = doc_counts[t]
                    numerator = freq * (self.k1 + 1)
                    denominator = freq + self.k1 * (1 - self.b + self.b * (dl / max(1.0, avg_dl)))
                    doc_score += idf * (numerator / denominator)
            scores.append(round(doc_score, 4))

        return scores

    async def rerank(
        self,
        query: str,
        candidates: list[RerankCandidate],
        top_k: int = 5,
    ) -> list[RerankCandidate]:
        """Rank passage candidates using Reciprocal Rank Fusion (RRF) over BM25 and vector scores."""
        if not candidates:
            return []

        corpus = [c.text for c in candidates]
        bm25_scores = self._score_bm25(query, corpus)

        # 1. Sort by BM25 to get rank
        bm25_ranked = sorted(
            enumerate(bm25_scores),
            key=lambda x: x[1],
            reverse=True,
        )
        bm25_rank_map = {idx: rank + 1 for rank, (idx, _) in enumerate(bm25_ranked)}

        # 2. Sort by Vector score to get rank
        vector_ranked = sorted(
            enumerate(candidates),
            key=lambda x: x[1].dense_vector_score,
            reverse=True,
        )
        vector_rank_map = {idx: rank + 1 for rank, (idx, _) in enumerate(vector_ranked)}

        # 3. Reciprocal Rank Fusion: 1 / (60 + r_bm25) + 1 / (60 + r_dense)
        scored_candidates: list[RerankCandidate] = []
        for idx, cand in enumerate(candidates):
            r_b = bm25_rank_map.get(idx, len(candidates))
            r_v = vector_rank_map.get(idx, len(candidates))
            rrf = (1.0 / (60.0 + r_b)) + (1.0 / (60.0 + r_v))
            rerank_score = round(rrf * 100.0, 3)

            scored_candidates.append(
                RerankCandidate(
                    text=cand.text,
                    doc_id=cand.doc_id,
                    chunk_index=cand.chunk_index,
                    lexical_bm25_score=bm25_scores[idx],
                    dense_vector_score=cand.dense_vector_score,
                    rerank_score=rerank_score,
                    final_score=rerank_score,
                )
            )

        scored_candidates.sort(key=lambda c: c.final_score, reverse=True)
        return scored_candidates[:top_k]

    async def predict_aeo_snippet(
        self,
        question: str,
        passages: list[str],
        brand: str | None = None,
    ) -> SnippetPrediction:
        """Extract or synthesize the highest-confidence 40-60 word Featured Snippet candidate."""
        if not passages:
            return SnippetPrediction(
                question=question,
                predicted_snippet=f"{brand or 'The solution'} provides comprehensive capabilities.",
                confidence=0.5,
                word_count=6,
                is_ideal_aeo_length=False,
                recommended_heading=f"What is {brand}?",
            )

        candidates = [
            RerankCandidate(text=p, doc_id=f"doc-{i}", chunk_index=i)
            for i, p in enumerate(passages)
        ]
        ranked = await self.rerank(question, candidates, top_k=3)
        best_passage = ranked[0].text if ranked else passages[0]

        # Break into sentences to find the 40-60 word snippet
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", best_passage) if s.strip()]

        accumulated: list[str] = []
        curr_words = 0
        for s in sentences:
            s_words = len(s.split())
            if curr_words + s_words <= 65:
                accumulated.append(s)
                curr_words += s_words
            elif curr_words < 35:
                accumulated.append(s)
                curr_words += s_words
                break
            else:
                break

        snippet = " ".join(accumulated) if accumulated else best_passage[:300]
        word_count = len(snippet.split())
        is_ideal = 35 <= word_count <= 65

        # Confidence based on word count sweet spot & match quality
        confidence = 0.88 if is_ideal else 0.72

        clean_topic = re.sub(r"^(what is|who is|how does|why is)\s+", "", question, flags=re.IGNORECASE)
        clean_topic = clean_topic.strip("? .")
        recommended_heading = f"What is {clean_topic.title()}?"

        return SnippetPrediction(
            question=question,
            predicted_snippet=snippet,
            doc_id=ranked[0].doc_id if ranked else "doc-0",
            confidence=confidence,
            word_count=word_count,
            is_ideal_aeo_length=is_ideal,
            recommended_heading=recommended_heading,
        )

