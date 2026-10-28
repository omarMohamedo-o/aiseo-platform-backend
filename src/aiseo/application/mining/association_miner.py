"""Association Rule and Co-Citation Data Mining Engine.

Mines co-citation patterns, competitive entity associations, and Pointwise Mutual
Information (PMI) from authentic crawled text and multi-model AI responses.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass, field


@dataclass(frozen=True)
class AssociationRule:
    """Discovered association rule: Antecedent -> Consequent."""
    antecedent: str
    consequent: str
    support: float
    confidence: float
    lift: float


@dataclass(frozen=True)
class PmiScore:
    """Pointwise Mutual Information (PMI) association between two terms."""
    term_a: str
    term_b: str
    pmi: float
    co_occurrence_count: int


@dataclass(frozen=True)
class MiningResult:
    """Aggregated data mining report."""
    total_transactions: int
    frequent_items: dict[str, int]
    rules: list[AssociationRule]
    pmi_scores: list[PmiScore]


class AssociationMiner:
    """Data mining engine computing Support, Confidence, Lift, and PMI."""

    @classmethod
    def mine_co_citations(
        cls,
        transactions: list[list[str]],
        min_support: float = 0.1,
        min_confidence: float = 0.5,
    ) -> MiningResult:
        """Discovers association rules (A -> B) across citation transactions."""
        n_transactions = len(transactions)
        if n_transactions == 0:
            return MiningResult(0, {}, [], [])

        # 1. Count individual item frequencies
        item_counts: Counter[str] = Counter()
        pair_counts: Counter[tuple[str, str]] = Counter()

        for basket in transactions:
            unique_items = sorted(list({item.strip().lower() for item in basket if item.strip()}))
            for item in unique_items:
                item_counts[item] += 1
            
            # Count distinct ordered pairs for directed association rules
            for i in range(len(unique_items)):
                for j in range(len(unique_items)):
                    if i != j:
                        pair_counts[(unique_items[i], unique_items[j])] += 1

        # 2. Filter frequent items by min_support
        frequent_items = {
            item: count
            for item, count in item_counts.items()
            if (count / n_transactions) >= min_support
        }

        # 3. Generate Association Rules & compute Support, Confidence, Lift
        discovered_rules: list[AssociationRule] = []
        for (item_a, item_b), co_count in pair_counts.items():
            support_ab = co_count / n_transactions
            if support_ab < min_support:
                continue

            support_a = item_counts[item_a] / n_transactions
            support_b = item_counts[item_b] / n_transactions

            if support_a == 0 or support_b == 0:
                continue

            confidence = support_ab / support_a
            if confidence >= min_confidence:
                lift = confidence / support_b
                discovered_rules.append(
                    AssociationRule(
                        antecedent=item_a,
                        consequent=item_b,
                        support=round(support_ab, 4),
                        confidence=round(confidence, 4),
                        lift=round(lift, 4),
                    )
                )

        # Sort rules descending by Lift, then Confidence
        discovered_rules.sort(key=lambda r: (r.lift, r.confidence), reverse=True)

        # 4. Compute Pointwise Mutual Information (PMI)
        pmi_scores: list[PmiScore] = []
        seen_unordered_pairs: set[tuple[str, str]] = set()

        for (item_a, item_b), co_count in pair_counts.items():
            canonical_pair = tuple(sorted([item_a, item_b]))
            if canonical_pair in seen_unordered_pairs:
                continue
            seen_unordered_pairs.add(canonical_pair)

            p_ab = co_count / n_transactions
            p_a = item_counts[item_a] / n_transactions
            p_b = item_counts[item_b] / n_transactions

            if p_a > 0 and p_b > 0 and p_ab > 0:
                # PMI = log2( P(A, B) / (P(A) * P(B)) )
                pmi_val = math.log2(p_ab / (p_a * p_b))
                pmi_scores.append(
                    PmiScore(
                        term_a=canonical_pair[0],
                        term_b=canonical_pair[1],
                        pmi=round(pmi_val, 4),
                        co_occurrence_count=co_count,
                    )
                )

        pmi_scores.sort(key=lambda s: s.pmi, reverse=True)

        return MiningResult(
            total_transactions=n_transactions,
            frequent_items=dict(item_counts.most_common()),
            rules=discovered_rules,
            pmi_scores=pmi_scores,
        )
