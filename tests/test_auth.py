import pytest
from unittest.mock import patch
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.auth.dependencies import verify_api_key
from app.auth.middleware import APIKeyMiddleware
from app.main import app

client = TestClient(app)


def test_verify_api_key_valid():
    with patch("app.auth.dependencies.os.environ", {"API_KEY": "valid-key"}):
        result = verify_api_key("valid-key")
        assert result is True


def test_verify_api_key_invalid():
    with patch("app.auth.dependencies.os.environ", {"API_KEY": "valid-key"}):
        with pytest.raises(HTTPException) as excinfo:
            verify_api_key("invalid-key")
        assert excinfo.value.status_code == 401
        assert "Invalid API key" in str(excinfo.value.detail)


def test_verify_api_key_missing():
    with patch("app.auth.dependencies.os.environ", {"API_KEY": "valid-key"}):
        with pytest.raises(HTTPException) as excinfo:
            verify_api_key(None)
        assert excinfo.value.status_code == 401
        assert "API key required" in str(excinfo.value.detail)


def test_middleware_bypass_public_endpoint():
    response = client.get("/api/v1/sample")
    assert response.status_code == 200


@patch("app.auth.middleware.os.environ", {"API_KEY": "test-api-key"})
def test_middleware_protected_endpoint_with_valid_key():
    with patch("app.services.scrape_service.ScrapeService.scrape") as mock_scrape:
        mock_scrape.return_value.success = True
        mock_scrape.return_value.message = "Success"
        
        response = client.post(
            "/api/v1/admin/scrape",
            json={"url": "https://example.com"},
            headers={"X-API-Key": "test-api-key"}
        )
        assert response.status_code == 200


@patch("app.auth.middleware.os.environ", {"API_KEY": "test-api-key"})
def test_middleware_protected_endpoint_with_invalid_key():
    response = client.post(
        "/api/v1/admin/scrape",
        json={"url": "https://example.com"},
        headers={"X-API-Key": "wrong-key"}
    )
    assert response.status_code == 401