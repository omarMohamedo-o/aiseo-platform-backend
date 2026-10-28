"""Concrete adapter implementing factual grounding verification and hallucination detection.

Modeled after the grounding guardrail and hallucination detector patterns from HistoryVerse-Chatbot.
"""
from __future__ import annotations

import re
from typing import Sequence

from aiseo.domain.evaluation.grounding import GroundingStatus, HallucinationMetrics
from aiseo.ports.evaluation.grounding_guard_port import GroundingGuardPort

# Factual claim regex patterns (pricing, percentages, stats, compliance, citations)
_PRICING_PATTERN = re.compile(
    r"(?:\$|€|£|USD\s*)\d+(?:,\d{3})*(?:\.\d{1,2})?(?:\s*(?:\/mo|\/month|\/year|\/user|per month|per year|monthly|annually))?",
    re.IGNORECASE,
)
_PERCENTAGE_PATTERN = re.compile(r"\b\d+(?:\.\d+)?%\b")
_NUMERIC_STAT_PATTERN = re.compile(
    r"\b\d+(?:,\d{3})*(?:\+)?\s*(?:users|customers|clients|integrations|languages|countries|uptime|employees|servers|nodes)\b",
    re.IGNORECASE,
)
_COMPLIANCE_PATTERN = re.compile(
    r"\b(?:SOC\s*2(?:\s*Type\s*(?:I|II))?|HIPAA|GDPR|ISO\s*27001|PCI-DSS|FedRAMP|CCPA|FERPA)\b",
    re.IGNORECASE,
)
_BRACKETED_CITATION_PATTERN = re.compile(
    r"\[(?:Source|Ref|Reference|Link|Citation):\s*([^\]]+)\]",
    re.IGNORECASE,
)
_URL_PATTERN = re.compile(r"https?://[^\s)\]}>,]+")


class GroundingGuardAdapter(GroundingGuardPort):
    """Evaluates factual consistency between generated AI answers and crawled website text."""

    def extract_claims(self, text: str) -> list[str]:
        """Extract high-entropy verifiable factual claims from text."""
        if not text:
            return []

        claims: list[str] = []

        # 1. Pricing assertions
        for m in _PRICING_PATTERN.finditer(text):
            val = m.group(0).strip()
            if val and val not in claims:
                claims.append(val)

        # 2. Percentage and growth stats
        for m in _PERCENTAGE_PATTERN.finditer(text):
            val = m.group(0).strip()
            if val and val not in claims:
                claims.append(val)

        # 3. Numeric statistics
        for m in _NUMERIC_STAT_PATTERN.finditer(text):
            val = m.group(0).strip()
            if val and val not in claims:
                claims.append(val)

        # 4. Compliance and security assertions
        for m in _COMPLIANCE_PATTERN.finditer(text):
            val = m.group(0).strip()
            if val and val not in claims:
                claims.append(val)

        # 5. Bracketed citation tags
        for m in _BRACKETED_CITATION_PATTERN.finditer(text):
            val = m.group(0).strip()
            if val and val not in claims:
                claims.append(val)

        return claims

    def extract_references(self, text: str) -> list[str]:
        """Extract explicit domain references and citation URLs."""
        if not text:
            return []

        refs: list[str] = []
        for m in _URL_PATTERN.finditer(text):
            cleaned = re.sub(r"[.,;:]+$", "", m.group(0).strip())
            if cleaned and cleaned not in refs:
                refs.append(cleaned)

        for m in _BRACKETED_CITATION_PATTERN.finditer(text):
            val = m.group(1).strip()
            if val and val not in refs:
                refs.append(val)

        return refs

    def verify_grounding(
        self,
        answer: str,
        source_context: str | Sequence[str],
        brand: str,
        threshold: float = 0.45,
    ) -> HallucinationMetrics:
        """Evaluate factual grounding and return calibrated hallucination metrics."""
        if not answer or len(answer.strip()) == 0:
            return HallucinationMetrics(
                grounding_ratio=1.0,
                hallucination_score=0.0,
                is_hallucinated=False,
                status="GROUNDED",
                verified_claims=[],
                unverified_claims=[],
                cited_references=[],
            )

        # Build unified source context string
        if isinstance(source_context, (list, tuple)):
            context_corpus = " ".join(source_context).strip()
        else:
            context_corpus = str(source_context or "").strip()

        cited_refs = self.extract_references(answer)
        claims = self.extract_claims(answer)

        # If no source context was provided at all, return UNVERIFIED
        if not context_corpus:
            return HallucinationMetrics(
                grounding_ratio=0.85,
                hallucination_score=0.15,
                is_hallucinated=False,
                status="UNVERIFIED",
                verified_claims=[],
                unverified_claims=claims,
                cited_references=cited_refs,
            )

        context_lower = context_corpus.lower()

        # Step 1: Claim-level validation
        verified_claims: list[str] = []
        unverified_claims: list[str] = []

        for claim in claims:
            claim_norm = claim.strip().lower()
            # Clean punctuation for robust matching
            claim_simple = re.sub(r"[^\w\s]", "", claim_norm)
            if claim_norm in context_lower or (claim_simple and claim_simple in context_lower):
                verified_claims.append(claim)
            else:
                unverified_claims.append(claim)

        # Step 2: Content entity lexical overlap (HistoryVerse grounding ratio)
        answer_words = [
            w.strip(".,!?:;'\"()[]{}")
            for w in answer.lower().split()
            if len(w.strip(".,!?:;'\"()[]{}")) > 3
        ]

        if not answer_words:
            content_ratio = 1.0
        else:
            context_words = {
                w.strip(".,!?:;'\"()[]{}")
                for w in context_lower.split()
                if len(w.strip(".,!?:;'\"()[]{}")) > 3
            }
            matched_words = sum(1 for w in answer_words if w in context_words)
            content_ratio = matched_words / len(answer_words)

        # Step 3: Combined weighted score
        if claims:
            claim_ratio = len(verified_claims) / len(claims)
            # 60% claim precision, 40% lexical corpus overlap
            grounding_ratio = round((claim_ratio * 0.6) + (content_ratio * 0.4), 3)
        else:
            grounding_ratio = round(content_ratio, 3)

        grounding_ratio = max(0.0, min(1.0, grounding_ratio))
        hallucination_score = round(1.0 - grounding_ratio, 3)
        is_hallucinated = hallucination_score > threshold

        status: GroundingStatus
        if grounding_ratio >= 0.75:
            status = "GROUNDED"
        elif grounding_ratio >= 0.40:
            status = "PARTIALLY_GROUNDED"
        else:
            status = "HALLUCINATED"

        return HallucinationMetrics(
            grounding_ratio=grounding_ratio,
            hallucination_score=hallucination_score,
            is_hallucinated=is_hallucinated,
            status=status,
            verified_claims=verified_claims,
            unverified_claims=unverified_claims,
            cited_references=cited_refs,
        )
