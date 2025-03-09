import pytest
from app.utils.url import validate_url


@pytest.mark.parametrize(
    "url,expected",
    [
        ("https://example.com", True),
        ("http://example.com", True),
        ("https://www.example.co.uk/path?query=1", True),
        ("example.com", False),
        ("ftp://example.com", False),
        ("", False),
        ("http://", False),
        (None, False),
    ],
)
def test_validate_url(url, expected):
    assert validate_url(url) == expected