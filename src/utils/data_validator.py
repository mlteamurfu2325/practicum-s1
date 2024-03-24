"""Module to validate user input of YouTube URLs."""

import re


YT_REGEX = re.compile(r"^(?:https?://)?(?:www\.)?youtube\.com/watch\?v=(?P<id>[A-Za-z0-9\-=_]{11})$")


def validate_youtube_url(url: str) -> bool:
    """
    Check if the given string is a valid YouTube URL.

    Args:
        url: Input string to validate as a YouTube URL.

    Returns:
        bool: True if the URL is a valid YouTube URL, False otherwise.

    Example:
        >>> validate_youtube_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        True
    """
    url = url.strip()
    return YT_REGEX.match(url) is not None
