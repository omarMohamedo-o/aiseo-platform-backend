"""Unit tests for Enterprise PII Redaction Guardrail.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import pytest

from aiseo.application.security.pii_masker import PiiMasker
from tests.test_config import (
    TARGET_BRAND,
    TARGET_EMAIL,
    TARGET_PHONE,
)


def test_sanitize_emails_and_phones() -> None:
    text = f"Contact our lead engineer at {TARGET_EMAIL} or call {TARGET_PHONE} immediately."
    clean = PiiMasker.sanitize(text)
    assert TARGET_EMAIL not in clean
    assert "[REDACTED_EMAIL]" in clean
    assert "[REDACTED_PHONE]" in clean


def test_sanitize_national_id() -> None:
    # Egyptian National ID: 29805121234567 (born 1998-05-12)
    text = "Client representative ID is 29805121234567 for enterprise compliance check."
    clean = PiiMasker.sanitize(text)
    assert "29805121234567" not in clean
    assert "[REDACTED_NATIONAL_ID]" in clean


def test_sanitize_credit_card() -> None:
    text = "Billing card on file: 4111 2222 3333 4444."
    clean = PiiMasker.sanitize(text)
    assert "4111 2222 3333 4444" not in clean
    assert "[REDACTED_PAYMENT_CARD]" in clean


def test_sanitize_api_keys() -> None:
    text = "Our backend environment has sk-proj-1234567890abcdef1234567890 for OpenAI connections."
    clean = PiiMasker.sanitize(text)
    assert "sk-proj-1234567890abcdef1234567890" not in clean
    assert "[REDACTED_API_SECRET]" in clean


def test_inspect_details() -> None:
    raw = "Reach out to ceo@enterprise.com with server IP 192.168.1.100."
    res = PiiMasker.inspect(raw)
    assert res.has_pii is True
    assert res.redacted_count == 2
    assert "email" in res.entity_counts
    assert "ip_address" in res.entity_counts
    assert "[REDACTED_EMAIL]" in res.sanitized_text
    assert "[REDACTED_IP_ADDRESS]" in res.sanitized_text


def test_contains_pii() -> None:
    clean_text = f"{TARGET_BRAND} provides industrial electrochlorination systems worldwide."
    dirty_text = "Server ip 10.0.0.1 failed."
    assert PiiMasker.contains_pii(clean_text) is False
    assert PiiMasker.contains_pii(dirty_text) is True

