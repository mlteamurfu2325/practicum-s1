import re

import streamlit as st


YT_REGEX = r"^(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})$"


def validate_youtube_url(url: str) -> bool:
    """Check if given string is valid YouTube URL.

    :param url: Input string to validate as YouTube URL
    :type url: str
    :return: True if valid YouTube URL, False otherwise
    :rtype: bool

    :Example:

    >>> validate_youtube_url("https://youtu.be/dQw4w9WgXcQ")
    True
    """
    url = url.strip()
    return re.match(YT_REGEX, url) is not None
