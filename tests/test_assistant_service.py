import pytest
from unittest.mock import MagicMock, patch

from app.models.assistant_request import QuestionRequest
from app.models.assistant_response import AssistantResponse
from app.services.assistant_service import AssistantService


@pytest.fixture
def mock_openai_client():
    with patch("app.services.client") as mock_client:
        # Mock the beta.threads APIs
        threads_mock = MagicMock()
        mock_client.beta.threads = threads_mock
        
        # Mock thread creation
        thread = MagicMock()
        thread.id = "mock-thread-id"
        threads_mock.create.return_value = thread
        
        # Mock messages
        messages_mock = MagicMock()
        threads_mock.messages = messages_mock
        
        # Mock runs
        runs_mock = MagicMock()
        threads_mock.runs = runs_mock
        run = MagicMock()
        run.status = "completed"
        runs_mock.create_and_poll.return_value = run
        
        # Mock message listing
        message_data_mock = MagicMock()
        message_data_mock.model_dump_json.return_value = '''
        {
            "data": [
                {
                    "content": [
                        {
                            "text": {
                                "value": "This is a mock response from the AI assistant."
                            }
                        }
                    ]
                }
            ]
        }
        '''
        messages_mock.list.return_value = message_data_mock
        
        yield mock_client


@pytest.fixture
def mock_assistant_store():
    with patch("app.store.assistant.AssistantStore") as mock_store_class:
        mock_store = MagicMock()
        mock_store_class.return_value = mock_store
        mock_store.save_q_and_a.return_value = None
        yield mock_store


@pytest.mark.asyncio
async def test_get_assistant_response(mock_openai_client, mock_assistant_store):
    service = AssistantService()
    question = "Test question"
    thread_id = None
    
    response = await service.get_assistant_response(question, thread_id)
    
    assert isinstance(response, AssistantResponse)
    assert response.message == "This is a mock response from the AI assistant."
    assert response.thread_id == "mock-thread-id"
    
    # Verify thread creation
    mock_openai_client.beta.threads.create.assert_called_once()
    
    # Verify run creation
    mock_openai_client.beta.threads.runs.create_and_poll.assert_called_once_with(
        thread_id="mock-thread-id",
        assistant_id="asst_sh3cHFY9moqlcjt8wvW5ZqMa"
    )
    
    # Verify store was called to save Q&A
    mock_assistant_store.save_q_and_a.assert_called_once_with(
        "mock-thread-id", 
        "Test question",
        "This is a mock response from the AI assistant."
    )


@pytest.mark.asyncio
async def test_get_assistant_response_with_existing_thread(mock_openai_client, mock_assistant_store):
    service = AssistantService()
    question = "Follow-up question"
    thread_id = "existing-thread-id"
    
    response = await service.get_assistant_response(question, thread_id)
    
    assert isinstance(response, AssistantResponse)
    assert response.message == "This is a mock response from the AI assistant."
    assert response.thread_id == "existing-thread-id"
    
    # Verify message creation on existing thread
    mock_openai_client.beta.threads.messages.create.assert_called_once_with(
        thread_id="existing-thread-id",
        role="user",
        content="Follow-up question"
    )
    
    # Verify thread creation was not called
    mock_openai_client.beta.threads.create.assert_not_called()