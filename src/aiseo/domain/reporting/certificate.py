"""Domain models for verifiable AI Visibility & GEO Compliance Certificates."""
from __future__ import annotations

import hashlib
import uuid
from datetime import UTC, datetime, timedelta

from pydantic import BaseModel, ConfigDict, Field


class GeoComplianceCertificate(BaseModel):
    """An official, cryptographically verifiable GEO Compliance Certificate."""

    model_config = ConfigDict(frozen=True)

    certificate_id: str
    domain: str
    brand_name: str
    issue_date: str
    valid_until: str
    visibility_score: int = Field(ge=0, le=100)
    grounding_score: int = Field(ge=0, le=100)
    schema_score: int = Field(ge=0, le=100)
    certification_tier: str  # "Platinum Enterprise" | "Gold Sovereign" | "Certified AI-Ready"
    verification_hash: str
    issuer: str = "AISEO Platform Global Standards Board"
    lead_architect: str = "Omar Mohamed (@omarMohamedo-o)"
    status: str = "VALID"
    copyright_notice: str = "Copyright © 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved."

    @classmethod
    def create(
        cls,
        domain: str,
        brand_name: str,
        visibility_score: int,
        grounding_score: int = 95,
        schema_score: int = 90,
    ) -> GeoComplianceCertificate:
        """Issue a new official compliance certificate with SHA-256 verification digest."""
        clean_domain = domain.replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0].lower()
        now = datetime.now(UTC)
        issue_date_str = now.strftime("%Y-%m-%d")
        valid_until_str = (now + timedelta(days=365)).strftime("%Y-%m-%d")

        # Determine certification tier based on visibility & grounding
        if visibility_score >= 85 and grounding_score >= 85:
            tier = "Platinum Enterprise"
        elif visibility_score >= 70:
            tier = "Gold Sovereign"
        else:
            tier = "Certified AI-Ready"

        cert_id = f"GEO-CERT-2026-{uuid.uuid4().hex[:8].upper()}"

        # Cryptographic verification digest
        raw_seed = f"{cert_id}:{clean_domain}:{visibility_score}:{grounding_score}:{issue_date_str}:omarMohamedo-o"
        verification_hash = hashlib.sha256(raw_seed.encode("utf-8")).hexdigest()[:32].upper()

        return cls(
            certificate_id=cert_id,
            domain=clean_domain,
            brand_name=brand_name or clean_domain.capitalize(),
            issue_date=issue_date_str,
            valid_until=valid_until_str,
            visibility_score=visibility_score,
            grounding_score=grounding_score,
            schema_score=schema_score,
            certification_tier=tier,
            verification_hash=verification_hash,
            issuer="AISEO Platform Global Standards Board",
            lead_architect="Omar Mohamed (@omarMohamedo-o)",
            status="VALID",
            copyright_notice="Copyright © 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.",
        )

