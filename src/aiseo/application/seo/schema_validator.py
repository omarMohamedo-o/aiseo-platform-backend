"""Deterministic Schema.org JSON-LD Validator.

Ensures that AI-generated or scraped structured data adheres strictly to Schema.org
specifications and Google Search / AI Overview Rich Result requirements prior to
client delivery.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SchemaValidationResult:
    """Detailed structural validation report for Schema.org JSON-LD markup."""
    is_valid: bool
    schema_type: str | None
    errors: list[str]
    warnings: list[str]
    parsed_schema: dict[str, Any] | None


class SchemaValidator:
    """Deterministic validator for Schema.org JSON-LD structured data."""

    # Supported and recommended Schema.org root types
    _SUPPORTED_TYPES = {
        "Organization",
        "Product",
        "FAQPage",
        "Article",
        "WebSite",
        "LocalBusiness",
        "SoftwareApplication",
    }

    @classmethod
    def validate_jsonld(cls, raw_json_str: str) -> SchemaValidationResult:
        """Validates raw JSON-LD string against Schema.org and Google Rich Snippet standards."""
        if not raw_json_str or not raw_json_str.strip():
            return SchemaValidationResult(
                is_valid=False,
                schema_type=None,
                errors=["Empty or null JSON-LD input."],
                warnings=[],
                parsed_schema=None,
            )

        # 1. Parse JSON syntax
        try:
            data = json.loads(raw_json_str)
        except json.JSONDecodeError as exc:
            return SchemaValidationResult(
                is_valid=False,
                schema_type=None,
                errors=[f"Invalid JSON syntax: {exc.msg} at line {exc.lineno} col {exc.colno}"],
                warnings=[],
                parsed_schema=None,
            )

        if not isinstance(data, dict):
            return SchemaValidationResult(
                is_valid=False,
                schema_type=None,
                errors=["Root of JSON-LD must be a JSON object."],
                warnings=[],
                parsed_schema=None,
            )

        errors: list[str] = []
        warnings: list[str] = []

        # 2. Validate @context
        context = data.get("@context")
        if not context:
            errors.append("Missing '@context' property (expected 'https://schema.org').")
        elif not isinstance(context, str) or "schema.org" not in context.lower():
            errors.append(f"Invalid '@context': '{context}'. Must reference schema.org.")

        # 3. Validate @type
        schema_type = data.get("@type")
        if not schema_type:
            errors.append("Missing '@type' declaration.")
        elif not isinstance(schema_type, str):
            errors.append("'@type' must be a string.")
        elif schema_type not in cls._SUPPORTED_TYPES:
            warnings.append(f"Uncommon Schema.org type '{schema_type}'. Verify Google Rich Result support.")

        # 4. Type-specific requirement checks
        if schema_type == "Organization":
            if "name" not in data or not str(data["name"]).strip():
                errors.append("Organization schema requires a 'name' field.")
            if "url" not in data:
                warnings.append("Recommended 'url' field missing for Organization.")

        elif schema_type == "Product":
            if "name" not in data:
                errors.append("Product schema requires a 'name' field.")
            if "description" not in data:
                warnings.append("Recommended 'description' missing for Product.")
            if "offers" not in data:
                warnings.append("Recommended 'offers' pricing details missing for Product.")

        elif schema_type == "FAQPage":
            main_entity = data.get("mainEntity")
            if not main_entity or not isinstance(main_entity, list):
                errors.append("FAQPage requires a 'mainEntity' list of Question objects.")
            else:
                for idx, q in enumerate(main_entity):
                    if not isinstance(q, dict) or q.get("@type") != "Question":
                        errors.append(f"mainEntity[{idx}] must be of @type 'Question'.")
                        continue
                    if "name" not in q:
                        errors.append(f"Question #{idx+1} is missing the 'name' property (the question text).")
                    ans = q.get("acceptedAnswer")
                    if not ans or not isinstance(ans, dict) or ans.get("@type") != "Answer":
                        errors.append(f"Question #{idx+1} requires an 'acceptedAnswer' object of @type 'Answer'.")
                    elif "text" not in ans:
                        errors.append(f"Answer #{idx+1} is missing the 'text' property.")

        is_valid = len(errors) == 0

        return SchemaValidationResult(
            is_valid=is_valid,
            schema_type=schema_type if isinstance(schema_type, str) else None,
            errors=errors,
            warnings=warnings,
            parsed_schema=data if is_valid else None,
        )

