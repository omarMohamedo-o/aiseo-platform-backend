"""Enterprise PII and Privacy Redaction Guardrail.

Protects crawled customer data, corporate secrets, and personally identifiable
information (PII) before vectorization or LLM prompt transmission.

Ensures compliance with GDPR, Egyptian Data Protection Law No. 151/2020, and HIPAA.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class PiiDetectionResult:
    """Detailed summary of redacted PII entities."""
    original_text: str
    sanitized_text: str
    redacted_count: int
    entity_counts: dict[str, int]
    has_pii: bool


class PiiMasker:
    """Enterprise PII sanitizer supporting global and regional (MENA/Egyptian) identifiers."""

    # Regex definitions for PII categories
    _PATTERNS: ClassVar[list[tuple[str, re.Pattern[str], str]]] = [
        # 1. API Keys & JWT Tokens (High Security)
        (
            "api_key_jwt",
            re.compile(r"\b(?:sk-[a-zA-Z0-9_-]{20,}|ghp_[a-zA-Z0-9]{30,}|eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+)\b"),
            "[REDACTED_API_SECRET]",
        ),
        # 2. Credit / Payment Cards (16 digits with optional spaces/hyphens)
        (
            "credit_card",
            re.compile(r"\b(?:\d{4}[ -]?){3}\d{4}\b"),
            "[REDACTED_PAYMENT_CARD]",
        ),
        # 3. Egyptian National ID (14 digits starting with 2 or 3)
        (
            "national_id",
            re.compile(r"\b[23]\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{7}\b"),
            "[REDACTED_NATIONAL_ID]",
        ),
        # 4. Email Addresses
        (
            "email",
            re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"),
            "[REDACTED_EMAIL]",
        ),
        # 5. Mobile & International Phone Numbers (+20, +1, +44, etc.)
        (
            "phone_number",
            re.compile(r"(?:\+?\d{1,3}[ -]?)?(?:\(?\d{2,4}\)?[ -]?)?\d{3,4}[ -]?\d{3,4}\b"),
            "[REDACTED_PHONE]",
        ),
        # 6. IPv4 Addresses (prevent corporate server leaks)
        (
            "ip_address",
            re.compile(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"),
            "[REDACTED_IP_ADDRESS]",
        ),
    ]

    @classmethod
    def sanitize(cls, text: str) -> str:
        """Sanitizes text by replacing sensitive PII with standardized redaction tokens."""
        if not text:
            return ""

        sanitized = text
        for _, pattern, replacement in cls._PATTERNS:
            sanitized = pattern.sub(replacement, sanitized)

        return sanitized

    @classmethod
    def inspect(cls, text: str) -> PiiDetectionResult:
        """Inspects text, calculates entity frequency counts, and returns a detailed report."""
        if not text:
            return PiiDetectionResult(
                original_text="",
                sanitized_text="",
                redacted_count=0,
                entity_counts={},
                has_pii=False,
            )

        sanitized = text
        counts: dict[str, int] = {}
        total = 0

        for entity_type, pattern, replacement in cls._PATTERNS:
            matches = pattern.findall(sanitized)
            if matches:
                count = len(matches)
                counts[entity_type] = count
                total += count
                sanitized = pattern.sub(replacement, sanitized)

        return PiiDetectionResult(
            original_text=text,
            sanitized_text=sanitized,
            redacted_count=total,
            entity_counts=counts,
            has_pii=total > 0,
        )

    @classmethod
    def contains_pii(cls, text: str) -> bool:
        """Fast-path check whether the text contains any confidential PII patterns."""
        if not text:
            return False
        return any(pattern.search(text) is not None for _, pattern, _ in cls._PATTERNS)

