# DisasterAssistant Tests

This directory contains tests for the DisasterAssistant application.

## Test Structure

The tests are organized as follows:

- **Regular Tests**: These tests are designed to be run with pytest and may require all dependencies to be installed
  - `test_sample.py`: Tests for the sample endpoint
  - `test_utils.py`: Tests for utility functions like URL validation
  - `test_assistant_service.py`: Tests for the AssistantService with mocked OpenAI (uses async calls)
  - `test_scrape_service.py`: Tests for the ScrapeService
  - `test_endpoints.py`: Tests for API endpoints
  - `test_auth.py`: Tests for authentication

- **Standalone Tests**: These tests can be run directly with Python without requiring all dependencies
  - `test_utils_standalone.py`: Standalone tests for URL validation
  - `test_mock_assistant_standalone.py`: Standalone tests for AssistantService with mocked responses (handles async)
  - `test_endpoint_standalone.py`: Standalone tests for API endpoints using mock clients
  - `run_standalone_tests.py`: Script to run all standalone tests in one go

## Running Tests

### Recommended: Use the Test Runner Script

The easiest way to run tests is using the provided test runner script:

```bash
# Run all working tests (standalone + utils tests)
python run_tests.py

# Run only standalone tests (no dependencies required)
python run_tests.py --standalone

# Run only utils tests
python run_tests.py --utils
```

### Running Standalone Tests

The standalone tests are designed to work without requiring all dependencies. Run them using:

```bash
# Run all standalone tests
python tests/run_standalone_tests.py

# Run a specific standalone test
python tests/test_utils_standalone.py
```

### Running with pytest

Due to dependency issues, not all tests can be run with pytest. Currently, only the utility tests are guaranteed to work:

```bash
# Run utils tests
python -m pytest tests/test_utils.py -v
```

Other tests require additional dependencies:
- Scrape service tests require `pytest-asyncio` and active OpenAI API keys
- Assistant service tests require `pytest-asyncio` and active OpenAI API keys
- Authentication tests require `authlib` and other authentication dependencies
- Endpoint tests require additional dependencies like `itsdangerous`

## Setting Up Test Environment

Make sure to install the required dependencies:

```bash
pip install -r requirements.txt
```

For testing, you might want to set up environment variables in a `.env.test` file:

```
API_KEY=test-api-key
OPENAI_API_KEY=test-openai-key
```

## Dependency Issues

If you encounter dependency issues when running the tests with pytest, you can:

1. Use the standalone tests instead, which don't require all dependencies
2. Create a virtual environment and install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Writing New Tests

When writing new tests:

1. Follow the existing pattern of test files
2. Use pytest fixtures for common setup
3. Use mocks for external services (OpenAI, web requests)
4. Create standalone versions for critical functionality with a `run_standalone_test()` function
5. Add the new test to this README file
6. Make sure tests can run without all dependencies installed