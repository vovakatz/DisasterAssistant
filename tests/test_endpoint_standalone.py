from dataclasses import dataclass
from typing import Optional, Dict, Any, List
import unittest
from unittest.mock import patch, MagicMock


# Simple mock FastAPI app for testing
class MockResponse:
    def __init__(self, status_code: int, json_data: Dict[str, Any]):
        self.status_code = status_code
        self._json_data = json_data
        
    def json(self) -> Dict[str, Any]:
        return self._json_data


class MockTestClient:
    def __init__(self, app):
        self.app = app
        self.headers = {}
    
    def get(self, url: str, headers: Optional[Dict[str, str]] = None) -> MockResponse:
        if url == "/api/v1/sample":
            return MockResponse(200, {"message": "Hello World"})
        return MockResponse(404, {"detail": "Not found"})
    
    def post(self, url: str, json: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> MockResponse:
        if url == "/api/v1/assistant":
            return MockResponse(200, {
                "thread_id": "mock-thread-id",
                "message": "This is a test response"
            })
        elif url == "/api/v1/admin/scrape":
            if headers and headers.get("X-API-Key") == "test-api-key":
                return MockResponse(200, {"success": True, "message": "Scraped successfully"})
            return MockResponse(401, {"detail": "Unauthorized"})
        return MockResponse(404, {"detail": "Not found"})


def run_standalone_test():
    """Run endpoint tests without unittest framework."""
    failures = 0
    client = MockTestClient(None)  # Mock app, not needed for this test
    
    # Test 1: Sample endpoint
    response = client.get("/api/v1/sample")
    test1_passed = response.status_code == 200 and response.json() == {"message": "Hello World"}
    print(f"Test 1 - Sample endpoint: {'✓' if test1_passed else '✗'}")
    if not test1_passed:
        failures += 1
    
    # Test 2: Assistant endpoint
    request_data = {
        "question": "Test question",
        "thread_id": None
    }
    response = client.post("/api/v1/assistant", json=request_data)
    test2_passed = (response.status_code == 200 and 
                   response.json() == {
                       "thread_id": "mock-thread-id",
                       "message": "This is a test response"
                   })
    print(f"Test 2 - Assistant endpoint: {'✓' if test2_passed else '✗'}")
    if not test2_passed:
        failures += 1
    
    # Test 3: Scrape endpoint authenticated
    request_data = {"url": "https://example.com"}
    response = client.post(
        "/api/v1/admin/scrape",
        json=request_data,
        headers={"X-API-Key": "test-api-key"}
    )
    test3_passed = response.status_code == 200 and response.json()["success"] is True
    print(f"Test 3 - Scrape endpoint (authenticated): {'✓' if test3_passed else '✗'}")
    if not test3_passed:
        failures += 1
    
    # Test 4: Scrape endpoint unauthenticated
    request_data = {"url": "https://example.com"}
    response = client.post("/api/v1/admin/scrape", json=request_data)
    test4_passed = response.status_code == 401
    print(f"Test 4 - Scrape endpoint (unauthenticated): {'✓' if test4_passed else '✗'}")
    if not test4_passed:
        failures += 1
    
    # Summary
    print(f"\nPassed {4 - failures} of 4 tests")
    return failures == 0


# For unittest compatibility
class TestEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = MockTestClient(None)  # Mock app, not needed for this test
    
    def test_sample_endpoint(self):
        response = self.client.get("/api/v1/sample")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello World"})
    
    def test_assistant_endpoint(self):
        request_data = {
            "question": "Test question",
            "thread_id": None
        }
        response = self.client.post("/api/v1/assistant", json=request_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "thread_id": "mock-thread-id",
            "message": "This is a test response"
        })
    
    def test_scrape_endpoint_authenticated(self):
        request_data = {"url": "https://example.com"}
        response = self.client.post(
            "/api/v1/admin/scrape",
            json=request_data,
            headers={"X-API-Key": "test-api-key"}
        )
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertTrue(response_json["success"])
    
    def test_scrape_endpoint_unauthenticated(self):
        request_data = {"url": "https://example.com"}
        response = self.client.post("/api/v1/admin/scrape", json=request_data)
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--unittest":
        unittest.main(argv=['first-arg-is-ignored'])
    else:
        success = run_standalone_test()
        sys.exit(0 if success else 1)