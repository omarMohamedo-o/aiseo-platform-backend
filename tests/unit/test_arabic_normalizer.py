import pytest

from aiseo.application.nlp.arabic_normalizer import ArabicNormalizer


def test_is_arabic():
    assert ArabicNormalizer.is_arabic("شركة حلول الذكاء الاصطناعي") is True
    assert ArabicNormalizer.is_arabic("Enterprise GEO Search Platform") is False
    assert ArabicNormalizer.is_arabic("Bilingual text with عربي inside") is True


def test_numeral_standardization():
    raw_indic = "السعر هو ٤٥٠٠ دولار في عام ٢٠٢٦"
    normalized = ArabicNormalizer.normalize_numerals(raw_indic)
    assert normalized == "السعر هو 4500 دولار في عام 2026"

    # Eastern numerals (Persian / Urdu style)
    raw_eastern = "کد ۵۶۷"
    assert ArabicNormalizer.normalize_numerals(raw_eastern) == "کد 567"


def test_tashkeel_and_tatweel_stripping():
    vocalized = "المُـنَـصَّـةُ الرَّقْمِـيَّةُ"
    clean = ArabicNormalizer.strip_tashkeel(vocalized)
    assert clean == "المنصة الرقمية"
    assert "ّ" not in clean
    assert "ـ" not in clean


def test_ligature_normalization():
    # \uFEFB is isolated Lam-Alef
    ligature_str = "\uFEFB شريك موثوق"
    normalized = ArabicNormalizer.normalize_ligatures(ligature_str)
    assert normalized == "لا شريك موثوق"


def test_alef_and_letter_normalization():
    text = "إدارة الأعمال والذكاء الإنتاجي فى الشركة"
    normalized = ArabicNormalizer.normalize_alef_and_letters(text)
    # إ and أ -> ا; فى -> في; الشركة -> الشركه
    assert "اداره" in normalized
    assert "الاعمال" in normalized
    assert "الشركه" in normalized


def test_egyptian_colloquial_mapping():
    amiya_text = "عايز اعرف ازاي الموقع شغال دلوقتي علشان نحسن الترتيب"
    msa_text = ArabicNormalizer.map_colloquial(amiya_text)
    assert "اريد" in msa_text
    assert "كيف" in msa_text
    assert "يعمل" in msa_text
    assert "الان" in msa_text
    assert "من اجل" in msa_text


def test_end_to_end_arabic_pipeline():
    noisy = "شَرِكَةُ \uFEFB للتجارة! عايز اعرف بكام الباقة؟ السعر ٢٥٠٠ ج.م فى الشهر."
    result = ArabicNormalizer.normalize(noisy)
    # Check that tashkeel removed, ligature resolved, numerals standardized, colloquial mapped
    assert "2500" in result
    assert "لا" in result
    assert "اريد" in result
    assert "كم سعر" in result
    assert "شركه" in result

