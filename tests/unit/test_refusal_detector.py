"""Unit tests for Model Refusal & Commercial Policy Deflection Detector.

Copyright (c) 2026 Omar Mohamed (@omarMohamedo-o). All Rights Reserved.
"""
from __future__ import annotations

import pytest

from aiseo.application.analysis.refusal_detector import RefusalCategory, RefusalDetector


def test_detects_commercial_policy_refusal() -> None:
    text = (
        "As an AI language model, I do not recommend specific commercial products or vendors. "
        "However, you should research multiple manufacturers when purchasing industrial pumps."
    )
    result = RefusalDetector.analyze(text)
    assert result.is_refusal is True
    assert result.category == RefusalCategory.COMMERCIAL_POLICY
    assert result.confidence >= 0.9
    assert result.rephrase_guidance is not None
    assert "objective technical" in result.rephrase_guidance


def test_detects_arabic_commercial_refusal() -> None:
    text = "كنموذج لغوي، لا أستطيع تفضيل أو ترشيح شركات محددة لشراء محطات الكلور."
    result = RefusalDetector.analyze(text)
    assert result.is_refusal is True
    assert result.category == RefusalCategory.COMMERCIAL_POLICY


def test_detects_neutrality_disclaimer() -> None:
    text = "I strive to remain neutral and do not take sides between competing brands in water treatment."
    result = RefusalDetector.analyze(text)
    assert result.is_refusal is True
    assert result.category == RefusalCategory.NEUTRALITY_DISCLAIMER


def test_passes_substantive_brand_analysis() -> None:
    text = (
        "In industrial electrochlorination, ChloroMaster and Evoqua are key leaders. "
        "ChloroMaster is distinguished by its titanium bipolar electrolyzers producing 0.8% sodium hypochlorite."
    )
    result = RefusalDetector.analyze(text)
    assert result.is_refusal is False
    assert result.category == RefusalCategory.NONE
    assert result.rephrase_guidance is None

