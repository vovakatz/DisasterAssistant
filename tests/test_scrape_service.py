import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import asyncio

from app.models.scrape_response import ScrapeResponse
from app.services.scrape_service import ScrapeService


class MockCrawlerResult:
    def __init__(self, success=True, markdown="Example markdown content"):
        self.success = success
        self.markdown = markdown


@pytest.fixture
def mock_crawler():
    with patch("app.services.scrape_service.AsyncWebCrawler") as mock:
        crawler_instance = AsyncMock()
        mock.return_value.__aenter__.return_value = crawler_instance
        
        # Set up the arun method to return a success result
        result = MockCrawlerResult(success=True, markdown="Example markdown content")
        crawler_instance.arun.return_value = result
        
        yield crawler_instance


@pytest.fixture
def mock_openai_client():
    with patch("app.services.client") as mock_client:
        # Mock file upload
        file_response = MagicMock()
        file_response.id = "file-123"
        mock_client.files.create.return_value = file_response
        
        # Mock batch creation
        batch_response = MagicMock()
        batch_response.id = "batch-123"
        mock_client.beta.vector_stores.file_batches.create.return_value = batch_response
        
        # Mock batch retrieval
        batch_status = MagicMock()
        batch_status.status = "completed"
        mock_client.beta.vector_stores.file_batches.retrieve.return_value = batch_status
        
        yield mock_client


@pytest.mark.asyncio
async def test_get_page_content(mock_crawler):
    service = ScrapeService()
    response = await service.get_page_content("https://example.com")
    
    assert isinstance(response, ScrapeResponse)
    assert response.content == "Example markdown content"
    mock_crawler.arun.assert_called_once_with(url="https://example.com")


def test_add_file_to_assistant():
    # More extensive mocking to prevent actual API calls
    with patch("app.services.client") as mock_client, \
         patch("app.services.scrape_service.settings", MagicMock(VECTOR_STORE_ID="vs-123")), \
         patch("app.services.scrape_service.time.sleep"):  # Skip the sleep calls
        
        # Mock file upload
        file_response = MagicMock()
        file_response.id = "file-123"
        mock_client.files.create.return_value = file_response
        
        # Mock the beta attribute and its full nested structure
        mock_beta = MagicMock()
        mock_client.beta = mock_beta
        
        # Mock vector_stores and its child attributes/methods
        mock_vector_stores = MagicMock()
        mock_beta.vector_stores = mock_vector_stores
        
        # Mock file_batches and its methods
        mock_file_batches = MagicMock()
        mock_vector_stores.file_batches = mock_file_batches
        
        # Mock batch creation response
        batch_response = MagicMock()
        batch_response.id = "batch-123"
        mock_file_batches.create.return_value = batch_response
        
        # Mock batch status response
        batch_status = MagicMock()
        batch_status.status = "completed"
        mock_file_batches.retrieve.return_value = batch_status
        
        # Run the code being tested
        service = ScrapeService()
        service.add_file_to_assistant("Test content", "test.txt")
        
        # Verify file upload
        mock_client.files.create.assert_called_once()
        assert mock_client.files.create.call_args[1]["purpose"] == "assistants"
        
        # Verify batch creation
        mock_file_batches.create.assert_called_once_with(
            vector_store_id="vs-123",
            file_ids=["file-123"]
        )
        
        # Verify batch status check
        mock_file_batches.retrieve.assert_called_once_with(
            vector_store_id="vs-123",
            batch_id="batch-123"
        )