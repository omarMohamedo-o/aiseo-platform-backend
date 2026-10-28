"""Unit tests for Deterministic Schema.org JSON-LD Validator.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import pytest

from aiseo.application.seo.schema_validator import SchemaValidator
from tests.test_config import TARGET_BASE_URL, TARGET_BRAND


def test_validate_valid_faq_schema() -> None:
    valid_faq = """
    {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "How does on-site electrochlorination eliminate bulk chlorine gas risk?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "By generating sodium hypochlorite directly from salt and electricity on demand."
                }
            }
        ]
    }
    """
    res = SchemaValidator.validate_jsonld(valid_faq)
    assert res.is_valid is True
    assert res.schema_type == "FAQPage"
    assert len(res.errors) == 0
    assert res.parsed_schema is not None


def test_validate_invalid_syntax() -> None:
    broken_json = '{"@context": "https://schema.org", "@type": "Product", name: missing quotes}'
    res = SchemaValidator.validate_jsonld(broken_json)
    assert res.is_valid is False
    assert any("Invalid JSON syntax" in err for err in res.errors)


def test_validate_missing_context_and_type() -> None:
    bad_data = f'{{"name": "{TARGET_BRAND}"}}'
    res = SchemaValidator.validate_jsonld(bad_data)
    assert res.is_valid is False
    assert any("@context" in err for err in res.errors)
    assert any("@type" in err for err in res.errors)


def test_validate_organization_missing_name() -> None:
    bad_org = f'{{"@context": "https://schema.org", "@type": "Organization", "url": "{TARGET_BASE_URL}"}}'
    res = SchemaValidator.validate_jsonld(bad_org)
    assert res.is_valid is False
    assert any("requires a 'name' field" in err for err in res.errors)

