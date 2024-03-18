"""Test src/utils/data_validator.py"""

import pytest

from src.utils.data_validator import validate_youtube_url


@pytest.mark.parametrize(
    "url,expected",
    [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", True),
        ("https://youtu.be/dQw4w9WgXcQ", False),
        ("www.youtube.com/watch?v=dQw4w9WgXcQ", True),
        ("https://google.com", False),
        ("dQw4w9WgXcQ", False),
    ],
)
def test_validate_youtube_url(url, expected):
    """Test validate_youtube_url function"""
    assert validate_youtube_url(url) == expected
