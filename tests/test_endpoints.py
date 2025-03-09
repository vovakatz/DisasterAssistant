import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.models.assistant_request import QuestionRequest
from app.models.assistant_response import AssistantResponse
from app.models.scrap_request import ScrapeRequest
from app.models.scrape_response import ScrapeResponse

client = TestClient(app)


def test_sample_endpoint():
    response = client.get("/api/v1/sample")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@patch("app.api.v1.endpoints.assistant.AssistantService")
def test_assistant_endpoint(mock_service_class):
    # Setup mock
    mock_service = MagicMock()
    mock_service_class.return_value = mock_service
    mock_service.get_assistant_response.return_value = AssistantResponse(
        thread_id="mock-thread-id",
        message="This is a test response"
    )
    
    # Test request
    request_data = {
        "question": "Test question",
        "thread_id": None
    }
    response = client.post("/api/v1/assistant", json=request_data)
    
    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "thread_id": "mock-thread-id", 
        "message": "This is a test response"
    }
    mock_service.get_assistant_response.assert_called_once()
    call_args = mock_service.get_assistant_response.call_args
    assert call_args[0][0] == "Test question"  # First arg: question
    assert call_args[0][1] is None  # Second arg: thread_id


@patch("app.api.v1.endpoints.admin.scrape.ScrapeService")
def test_scrape_endpoint_authenticated(mock_service_class):
    # This test assumes the authentication is bypassed for testing
    with patch("app.auth.dependencies.verify_api_key", return_value=True):
        # Setup mock
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service
        mock_service.scrape.return_value = ScrapeResponse(
            success=True,
            message="Scraped 3 pages successfully"
        )
        
        # Test request
        request_data = {"url": "https://example.com"}
        response = client.post(
            "/api/v1/admin/scrape",
            json=request_data,
            headers={"X-API-Key": "test-api-key"}
        )
        
        # Assertions
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["success"] is True
        assert "Scraped 3 pages successfully" in response_json["message"]
        mock_service.scrape.assert_called_once()


def test_scrape_endpoint_unauthenticated():
    request_data = {"url": "https://example.com"}
    response = client.post("/api/v1/admin/scrape", json=request_data)
    
    assert response.status_code == 401  # Unauthorized