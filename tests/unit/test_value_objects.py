import pytest

from aiseo.domain.errors import InvalidUrlError
from aiseo.domain.value_objects import Keyword, LanguageCode, Score, Url


def test_url_accepts_valid_http_url() -> None:
    url = Url(value="https://example.com/page")
    assert url.domain == "example.com"


@pytest.mark.parametrize("raw", ["not-a-url", "ftp://example.com", ""])
def test_url_rejects_invalid_url(raw: str) -> None:
    with pytest.raises(InvalidUrlError):
        Url(value=raw)


def test_score_clamps_to_two_decimals() -> None:
    assert Score(value=64.567).value == 64.57


@pytest.mark.parametrize("value", [-1, 101])
def test_score_rejects_out_of_range(value: float) -> None:
    with pytest.raises(ValueError):
        Score(value=value)


def test_keyword_is_normalized() -> None:
    assert Keyword(text="  Best  SEO Tool ").text == "best  seo tool"


def test_language_code_rejects_invalid() -> None:
    with pytest.raises(ValueError):
        LanguageCode(value="english")


from pydantic import ValidationError


def test_value_objects_are_frozen() -> None:
    url = Url(value="https://example.com")
    with pytest.raises(ValidationError):
        url.value = "https://other.com"
