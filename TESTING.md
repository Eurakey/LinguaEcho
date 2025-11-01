# Testing Documentation

## Overview

LinguaEcho has comprehensive test coverage for both backend and frontend:
- **Backend**: 19 tests covering API endpoints and business logic (70% coverage)
- **Frontend**: 18 tests covering Pinia stores and state management
- **CI/CD**: Automated testing on every push via GitHub Actions

---

## Backend Testing

### Setup

```bash
cd backend
source venv/bin/activate  # Or: venv\Scripts\activate on Windows
pip install pytest pytest-asyncio pytest-cov pytest-mock
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=app --cov=main --cov-report=term-missing

# Run specific test file
pytest tests/test_api_chat.py -v

# Run specific test
pytest tests/test_api_chat.py::TestChatEndpoint::test_chat_endpoint_success -v
```

### Test Structure

```
backend/tests/
├── __init__.py
├── conftest.py              # Pytest configuration and fixtures
├── test_api_chat.py         # Tests for /api/chat endpoint (9 tests)
└── test_api_report.py       # Tests for /api/report/generate endpoint (10 tests)
```

### Test Coverage

- **API Endpoints**: 100% coverage
- **Models/Schemas**: 100% coverage
- **Overall**: 70% coverage
- All tests passing ✅

### What's Tested

#### `/api/chat` Endpoint
- ✅ Successful chat requests
- ✅ Request validation (missing fields, invalid enums)
- ✅ Error handling (LLM service failures)
- ✅ All 10 scenarios (restaurant, hotel, supermarket, etc.)
- ✅ Both languages (Japanese, English)
- ✅ Conversation history handling

#### `/api/report/generate` Endpoint
- ✅ Successful report generation
- ✅ Reports with grammar errors
- ✅ Reports with vocabulary issues
- ✅ Reports with naturalness feedback
- ✅ Perfect conversations (no errors)
- ✅ Long conversation handling
- ✅ Error handling

---

## Frontend Testing

### Setup

```bash
cd frontend
npm install
```

### Running Tests

```bash
# Run tests once
npm test

# Run tests in watch mode (for development)
npm test -- --watch

# Run with UI
npm run test:ui

# Run with coverage
npm run test:coverage
```

### Test Structure

```
frontend/src/stores/__tests__/
└── conversation.spec.js     # Pinia store tests (18 tests)
```

### Test Coverage

- **Conversation Store**: Comprehensive coverage
- All 18 tests passing ✅
- Fast execution: <500ms

### What's Tested

#### Conversation Store
- ✅ Initial state validation
- ✅ `startNewConversation()` action
- ✅ `addMessage()` action
- ✅ Computed properties:
  - `turnCount` calculation
  - `hasConversation` flag
  - `userMessages` filtering
- ✅ `setLoading()` action
- ✅ `resetConversation()` action
- ✅ `getConversationData()` getter

---

## CI/CD Pipeline

### GitHub Actions Workflows

#### Backend Tests
- **Trigger**: Push or PR to `main` branch (when backend files change)
- **Runs**: Python 3.10 on Ubuntu
- **Steps**:
  1. Install dependencies
  2. Run pytest with coverage
  3. Upload coverage to Codecov (optional)

#### Frontend Tests
- **Trigger**: Push or PR to `main` branch (when frontend files change)
- **Runs**: Node.js 20 on Ubuntu
- **Steps**:
  1. Install dependencies
  2. Run vitest tests
  3. Generate coverage report
  4. Upload coverage to Codecov (optional)

### Status Badges

Add these to README.md once CI is set up:

```markdown
![Backend Tests](https://github.com/YOUR_USERNAME/LinguaEcho/workflows/Backend%20Tests/badge.svg)
![Frontend Tests](https://github.com/YOUR_USERNAME/LinguaEcho/workflows/Frontend%20Tests/badge.svg)
```

---

## Writing New Tests

### Backend Test Example

```python
# tests/test_new_feature.py
import pytest
from unittest.mock import patch, AsyncMock

def test_new_endpoint(client):
    """Test description"""
    with patch('app.services.llm_service.llm_service.method_name', new_callable=AsyncMock) as mock:
        mock.return_value = "Expected response"

        response = client.post("/api/endpoint", json={"key": "value"})

        assert response.status_code == 200
        assert response.json()["key"] == "expected_value"
```

### Frontend Test Example

```javascript
// src/stores/__tests__/new_store.spec.js
import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useNewStore } from '../new_store'

describe('New Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should initialize correctly', () => {
    const store = useNewStore()
    expect(store.someState).toBe(initialValue)
  })

  it('should update state on action', () => {
    const store = useNewStore()
    store.someAction(newValue)
    expect(store.someState).toBe(newValue)
  })
})
```

---

## Best Practices

### Backend Testing
1. **Mock External Services**: Always mock LLM API calls to avoid real API usage
2. **Test Happy Path First**: Ensure normal flow works before edge cases
3. **Test Error Handling**: Verify proper error responses (400, 422, 500)
4. **Use Fixtures**: Leverage `conftest.py` for reusable test data
5. **Keep Tests Fast**: Aim for <1 second per test

### Frontend Testing
1. **Test User Behavior**: Focus on what users actually do
2. **Isolate Store Logic**: Test stores independently from components
3. **Mock API Calls**: Use Vitest's `vi.mock()` for API services
4. **Test Computed Properties**: Verify reactive calculations
5. **Keep It Simple**: One test = one behavior

### General
- **Run Tests Before Committing**: `pytest && npm test`
- **Maintain Coverage**: Keep above 70% for both backend and frontend
- **Update Tests With Code**: Don't let tests fall behind
- **Clear Test Names**: Use descriptive names that explain what's being tested
- **One Assertion Per Test**: Makes failures easier to debug

---

## Troubleshooting

### Backend Tests Failing

**Problem**: `ModuleNotFoundError: No module named 'app'`
```bash
# Solution: Ensure you're in the backend directory and venv is activated
cd backend
source venv/bin/activate
pytest
```

**Problem**: Mock not working
```python
# Make sure you're mocking the right path
# ❌ Wrong: patch('app.services.llm_service.LLMService.get_instance')
# ✅ Right: patch('app.services.llm_service.llm_service.method_name')
```

### Frontend Tests Failing

**Problem**: `Cannot find module 'pinia'`
```bash
# Solution: Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Problem**: Tests timeout
```javascript
// Add timeout to specific tests
it('slow test', async () => {
  // test code
}, 10000) // 10 second timeout
```

---

## Coverage Goals

### Current Status
- ✅ Backend: 70% (19 tests passing)
- ✅ Frontend: Store tests complete (18 tests passing)
- ⚠️ Frontend Components: Not yet covered

### Next Steps
1. Add component tests for critical views (Home, Conversation, Report)
2. Add API service layer tests with mocked HTTP calls
3. Add localStorage utility tests
4. Increase backend coverage to 80%+

### Coverage Targets
- **Critical Paths**: 100% (auth, payment, data integrity)
- **Business Logic**: 90%+ (stores, services, utils)
- **UI Components**: 70%+ (critical components)
- **Config/Setup**: 50%+ (less critical)

---

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Vitest Documentation](https://vitest.dev/)
- [Vue Test Utils](https://test-utils.vuejs.org/)
- [Pinia Testing](https://pinia.vuejs.org/cookbook/testing.html)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

---

**Last Updated**: 2025-11-01
