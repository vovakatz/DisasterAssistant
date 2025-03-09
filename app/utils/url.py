import re
from urllib.parse import urlparse


def validate_url(url):
    """
    Validate if the given string is a properly formatted URL.
    Returns True if valid, False otherwise.
    """
    if not url:
        return False
        
    try:
        # Parse the URL
        result = urlparse(url)
        
        # Check if scheme is http or https and netloc is present
        return all([result.scheme in ['http', 'https'], result.netloc])
        
    except Exception:
        return False