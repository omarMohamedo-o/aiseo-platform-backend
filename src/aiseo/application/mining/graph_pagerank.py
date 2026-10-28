"""Domain Link Topology and Internal PageRank Graph Mining Engine.

Calculates internal link equity distribution across crawled domain pages using
iterative power-convergence PageRank. Identifies crawl hubs and orphan pages.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PageRankResult:
    """PageRank scores and topological classifications for a crawled domain."""
    total_pages: int
    scores: dict[str, float]
    crawl_hubs: list[tuple[str, float]]
    orphan_pages: list[str]
    authority_sinks: list[str]
    iterations_to_converge: int


class DomainPageRankMiner:
    """Graph mining engine computing PageRank on internal website hyperlinks."""

    def __init__(self, damping_factor: float = 0.85, max_iterations: int = 100, tolerance: float = 1e-6) -> None:
        self._damping = damping_factor
        self._max_iter = max_iterations
        self._tolerance = tolerance

    def compute_pagerank(self, link_graph: dict[str, list[str]]) -> PageRankResult:
        """Computes PageRank over an adjacency list representation of internal links.
        
        Args:
            link_graph: dict mapping source_url -> list of target_urls linked from it.
        """
        # Collect all unique nodes in the graph
        all_nodes: set[str] = set(link_graph.keys())
        for targets in link_graph.values():
            all_nodes.update(targets)

        nodes = sorted(list(all_nodes))
        n = len(nodes)
        if n == 0:
            return PageRankResult(0, {}, [], [], [], 0)

        # Build in-links and out-degree maps
        in_links: dict[str, list[str]] = {u: [] for u in nodes}
        out_degree: dict[str, int] = {u: 0 for u in nodes}

        for src, targets in link_graph.items():
            valid_targets = [t for t in set(targets) if t in all_nodes]
            out_degree[src] = len(valid_targets)
            for tgt in valid_targets:
                in_links[tgt].append(src)

        # Identify orphan pages (0 incoming links from internal pages, excluding root if self-linked)
        orphan_pages = [u for u in nodes if len(in_links[u]) == 0]

        # Identify authority sinks (has in-links but 0 out-links)
        authority_sinks = [u for u in nodes if len(in_links[u]) > 0 and out_degree[u] == 0]

        # Initialize uniform PageRank vector
        initial_val = 1.0 / n
        rank = {u: initial_val for u in nodes}

        iterations = 0
        base_teleport = (1.0 - self._damping) / n

        for it in range(self._max_iter):
            iterations += 1
            new_rank: dict[str, float] = {}

            # Calculate dangling sum (mass from nodes with out_degree == 0)
            dangling_sum = sum(rank[u] for u in nodes if out_degree[u] == 0)
            dangling_contrib = self._damping * (dangling_sum / n)

            for u in nodes:
                in_flow = sum(rank[v] / out_degree[v] for v in in_links[u] if out_degree[v] > 0)
                new_rank[u] = base_teleport + dangling_contrib + (self._damping * in_flow)

            # Check convergence using L1 norm
            diff = sum(abs(new_rank[u] - rank[u]) for u in nodes)
            rank = new_rank
            if diff < self._tolerance:
                break

        # Normalize so sum(rank) == 1.0
        total_mass = sum(rank.values())
        if total_mass > 0:
            rank = {u: round(v / total_mass, 6) for u, v in rank.items()}

        # Sort crawl hubs descending by PageRank
        sorted_hubs = sorted(rank.items(), key=lambda kv: kv[1], reverse=True)

        return PageRankResult(
            total_pages=n,
            scores=rank,
            crawl_hubs=sorted_hubs,
            orphan_pages=orphan_pages,
            authority_sinks=authority_sinks,
            iterations_to_converge=iterations,
        )

