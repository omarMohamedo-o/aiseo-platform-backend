"""Multilingual & Arabic NLP normalization service.

Adopts production-tested Arabic NLP patterns from HistoryVerse-Chatbot:
- Lam-Alef ligature protection and normalization
- Arabic-Indic numeral translation (٠-٩ -> 0-9)
- Tashkeel diacritic and Tatweel/Kashida stripping
- Alef/Yaa/Taa-Marbuta normalization
- Egyptian Colloquial (Amiya) to Modern Standard Arabic (MSA) term mapping
- High-accuracy language detection for MENA / bilingual GEO audits
"""
from __future__ import annotations

import re
import unicodedata

# Arabic-Indic and Eastern Arabic-Indic numerals mapping
_NUMERAL_MAP = {
    # Standard Arabic-Indic (Mashriq / Egypt / Levant / Gulf)
    "٠": "0", "١": "1", "٢": "2", "٣": "3", "٤": "4",
    "٥": "5", "٦": "6", "٧": "7", "٨": "8", "٩": "9",
    # Eastern Arabic-Indic (Persian / Urdu)
    "۰": "0", "۱": "1", "۲": "2", "۳": "3", "۴": "4",
    "۵": "5", "۶": "6", "۷": "7", "۸": "8", "۹": "9",
}

_NUMERAL_TRANS = str.maketrans(_NUMERAL_MAP)

# Tashkeel diacritics & Kashida regex
_TASHKEEL_REGEX = re.compile(
    r"[\u064B-\u0652\u0670\u0640]"  # Fathatan, Dammatan, Kasratan, Fatha, Damma, Kasra, Shadda, Sukun, Superscript Alef, Tatweel
)

# Lam-Alef Presentation Forms to Standard Sequence
_LIGATURE_MAP = {
    "\uFEFB": "لا",  # Isolated Lam with Alef
    "\uFEFC": "لا",  # Final Lam with Alef
    "\uFEF7": "لأ",  # Isolated Lam with Alef with Hamza Above
    "\uFEF8": "لأ",  # Final Lam with Alef with Hamza Above
    "\uFEF9": "لإ",  # Isolated Lam with Alef with Hamza Below
    "\uFEFA": "لإ",  # Final Lam with Alef with Hamza Below
    "\uFEF5": "لآ",  # Isolated Lam with Alef with Madda Above
    "\uFEF6": "لآ",  # Final Lam with Alef with Madda Above
}

# Egyptian Colloquial (Amiya) token mapping to Modern Standard Arabic (MSA)
_COLLOQUIAL_MAP: dict[str, str] = {
    "عايز": "اريد",
    "عايزة": "اريد",
    "عاوز": "اريد",
    "عاوزة": "اريد",
    "ازاي": "كيف",
    "ازاى": "كيف",
    "ليه": "لماذا",
    "كده": "هكذا",
    "كدا": "هكذا",
    "دلوقتي": "الان",
    "دلوقتى": "الان",
    "برضه": "ايضا",
    "برضو": "ايضا",
    "مش": "ليس",
    "علشان": "من اجل",
    "عشان": "من اجل",
    "ايه": "ماذا",
    "مين": "من",
    "فين": "اين",
    "شغال": "يعمل",
    "بكام": "كم سعر",
    "حاجة": "شيء",
    "شوية": "قليلا",
}

# Pre-compiled word regex for colloquial replacement
_WORD_REGEX = re.compile(r"[\u0600-\u06FF\w]+")


class ArabicNormalizer:
    """Normalizes Arabic text for token-efficient and accurate LLM/GEO evaluation."""

    @staticmethod
    def is_arabic(text: str) -> bool:
        """Return True if text contains Arabic characters."""
        return bool(re.search(r"[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]", text))

    @staticmethod
    def normalize_numerals(text: str) -> str:
        """Convert Eastern & Arabic-Indic numerals (٠-٩, ۰-۹) to Western standard (0-9)."""
        return text.translate(_NUMERAL_TRANS)

    @staticmethod
    def strip_tashkeel(text: str) -> str:
        """Remove harakat (fatha, damma, kasra, sukun, shadda, tatweel)."""
        return _TASHKEEL_REGEX.sub("", text)

    @staticmethod
    def normalize_ligatures(text: str) -> str:
        """Decompose Lam-Alef unicode presentation forms into canonical Arabic sequences."""
        res = text
        for lig, repl in _LIGATURE_MAP.items():
            res = res.replace(lig, repl)
        return res

    @staticmethod
    def normalize_alef_and_letters(text: str) -> str:
        """Unify Alef forms [إأآا] to ا, Alef Maksura [ى] to ي, and Taa Marbuta [ة] to ه."""
        # Unify Alef with Hamza / Madda
        res = re.sub(r"[إأآٱ]", "ا", text)
        # Unify Alef Maksura to Yaa
        res = re.sub(r"ى\b", "ي", res)
        # Normalize Taa Marbuta
        res = re.sub(r"ة\b", "ه", res)
        return res

    @staticmethod
    def map_colloquial(text: str) -> str:
        """Map common Egyptian Amiya tokens to Modern Standard Arabic for intent accuracy."""
        def _replace_token(match: re.Match[str]) -> str:
            token = match.group(0)
            return _COLLOQUIAL_MAP.get(token, token)

        return _WORD_REGEX.sub(_replace_token, text)

    @classmethod
    def normalize(
        cls,
        text: str,
        strip_diacritics: bool = True,
        convert_numerals: bool = True,
        normalize_letters: bool = True,
        map_colloquial_terms: bool = True,
    ) -> str:
        """Full normalization pipeline for Arabic search queries and scraped text."""
        if not text:
            return ""

        # Step 1: Unicode NFC normalization
        normalized = unicodedata.normalize("NFC", text)

        # Step 2: Ligature protection and decomposition
        normalized = cls.normalize_ligatures(normalized)

        # Step 3: Tashkeel stripping
        if strip_diacritics:
            normalized = cls.strip_tashkeel(normalized)

        # Step 4: Numeral standardization (٠-٩ -> 0-9)
        if convert_numerals:
            normalized = cls.normalize_numerals(normalized)

        # Step 5: Letter normalization (Alef, Yaa, Taa-Marbuta)
        if normalize_letters:
            normalized = cls.normalize_alef_and_letters(normalized)

        # Step 6: Colloquial term mapping
        if map_colloquial_terms:
            normalized = cls.map_colloquial(normalized)

        # Step 7: Collapse whitespace
        normalized = re.sub(r"\s+", " ", normalized).strip()

        return normalized

