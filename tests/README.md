# Test Suite for Voice Agent

This directory contains comprehensive tests for the voice agent web application.

## Structure

```
tests/
├── api/              # Backend API tests
│   ├── test_consults.py
│   └── test_voice_api.py
├── e2e/              # End-to-end tests (Playwright)
│   └── voice-agent.spec.js
├── components/       # React component tests
│   ├── ConsultScheduler.test.jsx
│   └── FAQSearch.test.jsx
├── websocket/        # WebSocket/real-time tests
│   └── test_voice_websocket.py
└── README.md         # This file
```

## Running Tests

### API Tests (Python/pytest)

```bash
# Install dependencies
pip install pytest pytest-asyncio httpx websockets

# Run all API tests
pytest tests/api/

# Run specific test file
pytest tests/api/test_consults.py

# Run with coverage
pytest tests/api/ --cov=app --cov-report=html
```

### E2E Tests (Playwright)

```bash
# Install dependencies
npm install -D @playwright/test

# Install browsers
npx playwright install

# Run all E2E tests
npx playwright test

# Run in headed mode (see browser)
npx playwright test --headed

# Run specific test file
npx playwright test tests/e2e/voice-agent.spec.js
```

### Component Tests (React Testing Library)

```bash
# Install dependencies
npm install -D @testing-library/react @testing-library/jest-dom jest

# Run component tests
npm test

# Run with watch mode
npm test -- --watch
```

### WebSocket Tests

```bash
# Run WebSocket tests
pytest tests/websocket/ -v

# Run with async support
pytest tests/websocket/ -v --asyncio-mode=auto
```

## Test Configuration

### Playwright Config

Create `playwright.config.js`:

```javascript
module.exports = {
  testDir: './tests/e2e',
  use: {
    baseURL: 'http://localhost:3000',
    screenshot: 'only-on-failure',
  },
};
```

### Jest Config

Create `jest.config.js`:

```javascript
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/tests/setup.js'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
};
```

## Writing New Tests

### API Test Template

```python
def test_endpoint_name(client):
    response = client.post("/endpoint", json={"key": "value"})
    assert response.status_code == 200
    assert response.json()["field"] == "expected"
```

### E2E Test Template

```javascript
test('user can perform action', async ({ page }) => {
  await page.goto('/page');
  await page.click('[data-testid="button"]');
  await expect(page.locator('[data-testid="result"]')).toBeVisible();
});
```

### Component Test Template

```javascript
test('component renders correctly', () => {
  render(<Component />);
  expect(screen.getByText('Expected Text')).toBeInTheDocument();
});
```

## Best Practices

1. **Test Isolation**: Each test should be independent
2. **Use Test IDs**: Prefer `data-testid` over CSS selectors
3. **Mock External Services**: Don't hit real APIs in tests
4. **Clean Up**: Always clean up test data after tests
5. **Descriptive Names**: Use clear, behavior-focused test names

## CI/CD Integration

Tests run automatically on:
- Pull requests
- Pushes to main branch
- Scheduled nightly runs

See `.github/workflows/tests.yml` for configuration.
