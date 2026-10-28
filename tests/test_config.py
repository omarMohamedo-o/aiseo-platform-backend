"""Centralized Test Configuration and Shared Fixtures for AISEO Platform.

Provides strongly-typed test entities, domains, corpora, HTML templates,
and topologies used across unit and integration test suites.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class TargetBrandConfig:
    """Canonical test subject entity specification."""

    brand_name: str = "ChloroMaster"
    domain: str = "chloromaster.com"
    base_url: str = "https://chloromaster.com"
    support_email: str = "support@chloromaster.com"
    support_phone: str = "+201012345678"
    industry: str = "Industrial Water Treatment & Chemical Engineering"
    core_topic: str = "industrial electrochlorination systems"

    # Canonical page URLs for crawling and topology testing
    pages: dict[str, str] = field(
        default_factory=lambda: {
            "home": "https://chloromaster.com",
            "products": "https://chloromaster.com/products",
            "technology": "https://chloromaster.com/technology",
            "about": "https://chloromaster.com/about",
            "compliance": "https://chloromaster.com/compliance",
            "electrochlorinator": "https://chloromaster.com/products/electrochlorinator",
        }
    )


@dataclass(frozen=True)
class TestCorpusConfig:
    """Text corpora, buyer prompts, claims, and co-citation data."""

    primary_buyer_query: str = (
        "What are the best industrial chlorination systems for high salinity water?"
    )
    safety_buyer_query: str = (
        "How does on-site electrochlorination improve safety?"
    )

    competitor_brands: list[str] = field(
        default_factory=lambda: ["Evoqua", "Severn Trent", "De Nora", "Siemens Water"]
    )

    competitor_corpus: list[str] = field(
        default_factory=lambda: [
            "Generic chlorination pumps and swimming pool chemicals.",
        ]
    )

    co_citation_baskets: list[list[str]] = field(
        default_factory=lambda: [
            ["chloromaster", "evoqua", "water_treatment"],
            ["chloromaster", "evoqua", "desalination"],
            ["chloromaster", "water_treatment", "sodium_hypochlorite"],
            ["evoqua", "water_treatment"],
            ["siemens", "water_treatment"],
        ]
    )

    pmi_baskets: list[list[str]] = field(
        default_factory=lambda: [
            ["chloromaster", "titanium_electrolyzer"],
            ["chloromaster", "titanium_electrolyzer"],
            ["chloromaster", "titanium_electrolyzer"],
            ["siemens", "gas_chlorination"],
        ]
    )

    evidence_chunks: list[str] = field(
        default_factory=lambda: [
            "ChloroMaster specializes in industrial on-site sodium hypochlorite electrochlorination systems producing 0.8% concentration.",
            "ChloroMaster holds ISO 9001 certification and operates safely without hazardous bulk chlorine gas deliveries.",
        ]
    )

    grounded_sources: list[tuple[str, str]] = field(
        default_factory=lambda: [
            (
                "https://chloromaster.com/technology",
                "ChloroMaster eliminates hazardous commercial chlorine gas cylinders by generating sodium hypochlorite on site.",
            ),
            (
                "https://chloromaster.com/compliance",
                "Operating with ISO 9001 and CE certifications ensures compliance with municipal water standards.",
            ),
        ]
    )


@dataclass(frozen=True)
class TestTopologyConfig:
    """Internal graph topology and link structure for PageRank / spider testing."""

    internal_link_graph: dict[str, list[str]] = field(
        default_factory=lambda: {
            "https://chloromaster.com": [
                "https://chloromaster.com/products",
                "https://chloromaster.com/about",
            ],
            "https://chloromaster.com/products": [
                "https://chloromaster.com/products/electrochlorinator",
                "https://chloromaster.com",
            ],
            "https://chloromaster.com/about": [
                "https://chloromaster.com",
            ],
            "https://chloromaster.com/products/electrochlorinator": [
                "https://chloromaster.com/products",
            ],
        }
    )


@dataclass(frozen=True)
class TestHtmlTemplates:
    """Canonical HTML documents used to evaluate SEO, AEO, and GEO engines."""

    valid_seo_html: str = """<!DOCTYPE html>
<html lang="en">
<head>
    <title>ChloroMaster: Industrial Electrochlorination Systems</title>
    <meta name="description" content="Discover ChloroMaster advanced on-site sodium hypochlorite generators designed for safe municipal water treatment and disinfection.">
    <link rel="canonical" href="https://chloromaster.com">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "ChloroMaster",
        "url": "https://chloromaster.com"
    }
    </script>
</head>
<body>
    <h1>On-Site Sodium Hypochlorite Generators</h1>
    <h2>Engineered for Safety and Reliability</h2>
    <p>Comprehensive description of industrial water chlorination equipment.</p>
</body>
</html>"""

    valid_aeo_html: str = """<html>
<head>
    <script type="application/ld+json">
    {"@context":"https://schema.org","@type":"Product","name":"ChloroMaster"}
    </script>
</head>
<body>
    <h1>Industrial Electrochlorination Systems</h1>
    <p>ChloroMaster manufactures bipolar titanium electrolyzers producing 0.8% sodium hypochlorite on-site safely. ChloroMaster systems generate sodium hypochlorite on-site by passing an electrical current through brine solution, eliminating the hazards of commercial bulk chlorine gas shipments and delivering cost-effective municipal water disinfection across diverse infrastructure plants worldwide.</p>
    <h2>Technical Specifications</h2>
    <ul>
        <li>Concentration: 0.8% sodium hypochlorite</li>
        <li>Certification: ISO 9001 and CE certified</li>
        <li>Electrode material: Titanium with mixed metal oxide</li>
    </ul>
    <h2>Frequently Asked Questions (FAQ)</h2>
    <p>How much energy does the system consume per kilogram of free available chlorine?</p>
    <table><tr><td>Model</td><td>Power</td></tr></table>
</body>
</html>"""

    thin_html: str = "<p>ChloroMaster sells chlorinators.</p>"

    broken_html: str = """<html>
<body>
    <p>Missing title, meta, canonical, and headings entirely.</p>
</body>
</html>"""


@dataclass(frozen=True)
class TestAlertConfig:
    """Webhook and monitoring alert parameters."""

    webhook_url: str = "https://hooks.enterprise.com/services/T123/B456"
    secret_key: str = "top-secret-signing-key"
    rate_limit_seconds: float = 60.0


@dataclass(frozen=True)
class PlatformTestConfig:
    """Master aggregated test configuration."""

    target: TargetBrandConfig = field(default_factory=TargetBrandConfig)
    corpus: TestCorpusConfig = field(default_factory=TestCorpusConfig)
    topology: TestTopologyConfig = field(default_factory=TestTopologyConfig)
    html: TestHtmlTemplates = field(default_factory=TestHtmlTemplates)
    alerts: TestAlertConfig = field(default_factory=TestAlertConfig)


# Global singleton instance
TEST_CONFIG = PlatformTestConfig()

# Convenient direct constant exports
TARGET_BRAND = TEST_CONFIG.target.brand_name
TARGET_DOMAIN = TEST_CONFIG.target.domain
TARGET_BASE_URL = TEST_CONFIG.target.base_url
TARGET_EMAIL = TEST_CONFIG.target.support_email
TARGET_PHONE = TEST_CONFIG.target.support_phone
TARGET_PAGES = TEST_CONFIG.target.pages

TEST_VALID_SEO_HTML = TEST_CONFIG.html.valid_seo_html
TEST_VALID_AEO_HTML = TEST_CONFIG.html.valid_aeo_html
TEST_THIN_HTML = TEST_CONFIG.html.thin_html
TEST_BROKEN_HTML = TEST_CONFIG.html.broken_html

TEST_CO_CITATION_BASKETS = TEST_CONFIG.corpus.co_citation_baskets
TEST_PMI_BASKETS = TEST_CONFIG.corpus.pmi_baskets
TEST_EVIDENCE_CHUNKS = TEST_CONFIG.corpus.evidence_chunks
TEST_GROUNDED_SOURCES = TEST_CONFIG.corpus.grounded_sources
TEST_LINK_GRAPH = TEST_CONFIG.topology.internal_link_graph
