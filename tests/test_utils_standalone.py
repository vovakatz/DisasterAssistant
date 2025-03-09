import re
from urllib.parse import urlparse

# Copy of the is_valid_url function from app.utils.url for standalone testing
def is_valid_url(url):
    """
    Validates that a given string is a valid URL.
    
    Args:
        url (str): The URL to validate.
        
    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    if not url:
        return False
    
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except:
        return False


def run_standalone_test():
    """Run the URL validation tests without pytest."""
    test_cases = [
        ("https://example.com", True),
        ("http://example.com", True),
        ("https://www.example.co.uk/path?query=1", True),
        ("example.com", False),
        ("ftp://example.com", False),
        ("", False),
        ("http://", False),
        (None, False),
    ]
    
    failures = 0
    
    for url, expected in test_cases:
        result = is_valid_url(url)
        status = result == expected
        print(f"Testing {url!r}: {'✓' if status else '✗'} (got {result}, expected {expected})")
        if not status:
            failures += 1
    
    print(f"Passed {len(test_cases) - failures} of {len(test_cases)} tests")
    return failures == 0


if __name__ == "__main__":
    success = run_standalone_test()
    import sys
    sys.exit(0 if success else 1)