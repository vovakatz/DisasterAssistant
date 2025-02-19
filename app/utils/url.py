import re
from urllib.parse import urlparse


def validate_url(url):
    """
    Validate if the given string is a properly formatted URL.
    Returns True if valid, False otherwise.
    """
    try:
        # Check if basic URL structure is valid
        result = urlparse(url)

        # Check if scheme and netloc are present
        if not all([result.scheme, result.netloc]):
            return False

        # Additional validation using regex
        # This pattern checks for common URL formats
        url_pattern = re.compile(
            r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$'
        )

        return bool(url_pattern.match(url))

    except Exception:
        return False