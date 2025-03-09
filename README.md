# DisasterAssistant Service

This is a sample FastAPI service with a sample endpoint, tests, and a good enterprise-level project structure.

## Getting Started

### Prerequisites

- Python 3.9
- Docker (optional)

### Installation

1. Clone the repository.
2. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Testing

The application includes a comprehensive test suite. For detailed information on running tests, see [tests/README.md](tests/README.md).

### Recommended: Use the Test Runner Script

The simplest way to run tests is using the provided test runner script:

```bash
# Run all working tests (standalone tests + utils tests)
python run_tests.py

# Run only standalone tests (no dependencies required)
python run_tests.py --standalone

# Run only utils tests with pytest
python run_tests.py --utils
```

### Alternative: Run Tests Directly

Run all standalone tests at once (no additional dependencies required):

```bash
python tests/run_standalone_tests.py
```

Or run individual standalone tests:

```bash
# Run URL validation standalone tests
python tests/test_utils_standalone.py

# Run mock assistant service standalone tests
python tests/test_mock_assistant_standalone.py

# Run endpoint standalone tests
python tests/test_endpoint_standalone.py
```

### Test Coverage

The tests cover:
- URL validation utilities
- Assistant service functionality (mocked)
- API endpoints
- Basic authentication flows

Several integration tests require external dependencies and API access and are skipped by default.

If you encounter dependency issues, refer to the [dependency troubleshooting section](tests/README.md#dependency-issues) in the testing documentation.