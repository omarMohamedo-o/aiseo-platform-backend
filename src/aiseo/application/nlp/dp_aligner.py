"""Dynamic Programming Local Sequence Alignment (Smith-Waterman) for Citation Concordance.

Computes exact mathematical token-level local sequence alignment between AI-generated
factual claims and crawled ground-truth source text chunks using O(m * n) DP matrix.

Provides deterministic mathematical proof of verbatim and semantic citation grounding.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class DpAlignmentResult:
    """Exact mathematical alignment coordinates and concordance score."""
    score: float
    max_possible_score: float
    concordance_ratio: float  # Scale 0.0 - 1.0
    aligned_query: str
    aligned_reference: str
    ref_start_token_idx: int
    ref_end_token_idx: int
    is_grounded: bool


class SmithWatermanAligner:
    """Dynamic programming local sequence aligner for textual claim verification."""

    def __init__(
        self,
        match_score: float = 2.0,
        mismatch_penalty: float = 1.0,
        gap_penalty: float = 1.0,
        grounding_threshold: float = 0.65,
    ) -> None:
        self._match = match_score
        self._mismatch = mismatch_penalty
        self._gap = gap_penalty
        self._threshold = grounding_threshold

    def align(self, query: str, reference: str) -> DpAlignmentResult:
        """Performs Smith-Waterman local alignment between query and reference text."""
        # Tokenize preserving order
        q_tokens = [w.lower() for w in re.findall(r"\b\w+\b", query)]
        r_tokens = [w.lower() for w in re.findall(r"\b\w+\b", reference)]

        m = len(q_tokens)
        n = len(r_tokens)

        if m == 0 or n == 0:
            return DpAlignmentResult(
                score=0.0,
                max_possible_score=max(1.0, float(m * self._match)),
                concordance_ratio=0.0,
                aligned_query="",
                aligned_reference="",
                ref_start_token_idx=-1,
                ref_end_token_idx=-1,
                is_grounded=False,
            )

        max_possible = float(m * self._match)

        # Initialize DP matrix: (m + 1) x (n + 1)
        # H[i][j] stores the best local alignment ending at q_tokens[i-1] and r_tokens[j-1]
        h = [[0.0 for _ in range(n + 1)] for _ in range(m + 1)]

        max_score = 0.0
        max_i, max_j = 0, 0

        for i in range(1, m + 1):
            q_w = q_tokens[i - 1]
            for j in range(1, n + 1):
                r_w = r_tokens[j - 1]

                # Match vs Mismatch
                if q_w == r_w:
                    diag = h[i - 1][j - 1] + self._match
                elif q_w[:4] == r_w[:4] and len(q_w) >= 4:  # Common stem heuristic
                    diag = h[i - 1][j - 1] + (self._match * 0.5)
                else:
                    diag = h[i - 1][j - 1] - self._mismatch

                up = h[i - 1][j] - self._gap
                left = h[i][j - 1] - self._gap

                val = max(0.0, diag, up, left)
                h[i][j] = val

                if val > max_score:
                    max_score = val
                    max_i = i
                    max_j = j

        # Traceback to extract local aligned substring
        aligned_q: list[str] = []
        aligned_r: list[str] = []

        curr_i, curr_j = max_i, max_j
        end_ref_idx = max_j - 1

        while curr_i > 0 and curr_j > 0 and h[curr_i][curr_j] > 0:
            val = h[curr_i][curr_j]
            q_w = q_tokens[curr_i - 1]
            r_w = r_tokens[curr_j - 1]

            score_diag = self._match if q_w == r_w else (-self._mismatch)

            if abs(val - (h[curr_i - 1][curr_j - 1] + score_diag)) < 1e-4:
                aligned_q.append(q_w)
                aligned_r.append(r_w)
                curr_i -= 1
                curr_j -= 1
            elif abs(val - (h[curr_i - 1][curr_j] - self._gap)) < 1e-4:
                aligned_q.append(q_w)
                aligned_r.append("-")
                curr_i -= 1
            else:
                aligned_q.append("-")
                aligned_r.append(r_w)
                curr_j -= 1

        start_ref_idx = curr_j

        aligned_q.reverse()
        aligned_r.reverse()

        concordance = round(min(1.0, max_score / max_possible), 4)

        return DpAlignmentResult(
            score=round(max_score, 2),
            max_possible_score=round(max_possible, 2),
            concordance_ratio=concordance,
            aligned_query=" ".join(aligned_q),
            aligned_reference=" ".join(aligned_r),
            ref_start_token_idx=start_ref_idx,
            ref_end_token_idx=end_ref_idx,
            is_grounded=concordance >= self._threshold,
        )

