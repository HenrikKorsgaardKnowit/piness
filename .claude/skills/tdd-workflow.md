---
name: tdd-workflow
description: Use this skill when writing new features, fixing bugs, or refactoring code. Enforces test-driven development with 80%+ coverage including unit and integration tests.
---

# Test-Driven Development Workflow

This skill ensures all code development follows TDD principles with comprehensive test coverage.

## When to Activate

- Writing new features or functionality
- Fixing bugs or issues
- Refactoring existing code
- Adding API endpoints or event handlers
- Integrating new external services

## Core Principles

### 1. Tests BEFORE Code
ALWAYS write tests first, then implement code to make tests pass.

### 2. Coverage Requirements
- Minimum 80% coverage (unit + integration)
- All edge cases covered
- Error scenarios tested
- Boundary conditions verified

### 3. Test Types

#### Unit Tests
- Individual functions and utilities
- Command handlers and routing logic
- Data transformation and formatting
- Pure functions and helpers

#### Integration Tests
- Slack event handling with mocked client
- LLM calls with mocked responses
- External API interactions (Jira, GitHub)
- End-to-end message flow (event → response)

## TDD Workflow Steps

### Step 1: Write Failing Test (RED)
```python
def test_status_command_queries_jira():
    """The status command should fetch active sprint issues."""
    result = handle_command("@bot status", [])
    assert "sprint" in result.lower()
```

### Step 2: Run Test (Verify it FAILS)
```bash
pytest -x
# Test should fail - we haven't implemented yet
```

### Step 3: Write Minimal Implementation (GREEN)
```python
def handle_command(mention_text: str, thread_messages: list) -> str:
    if "status" in mention_text.lower():
        issues = fetch_sprint_issues()
        return format_status(issues)
    return "I don't understand that command."
```

### Step 4: Run Test (Verify it PASSES)
```bash
pytest -x
# Test should now pass
```

### Step 5: Refactor (IMPROVE)
- Remove duplication
- Improve naming
- Optimize performance
- Enhance readability

### Step 6: Verify Coverage
```bash
pytest --cov --cov-report=term-missing
# Verify 80%+ coverage achieved
```

## Mocking External Dependencies

### Mock Slack Client
```python
from unittest.mock import MagicMock, patch

def test_handle_mention_reads_thread():
    client = MagicMock()
    client.conversations_replies.return_value = {
        "messages": [{"text": "hello"}, {"text": "world"}]
    }
    event = {"channel": "C123", "ts": "1.0", "thread_ts": "1.0", "text": "@bot status"}
    say = MagicMock()

    handle_mention(event, say, client)

    client.conversations_replies.assert_called_once()
    say.assert_called_once()
```

### Mock LLM Calls
```python
@patch("app.anthropic_client")
def test_agent_response_uses_claude(mock_client):
    mock_client.messages.create.return_value = MockResponse(
        content=[{"type": "text", "text": "Sprint is on track."}]
    )
    result = get_agent_response("What's the status?", [])
    assert "on track" in result
```

### Mock Jira/GitHub APIs
```python
@patch("integrations.jira.fetch_sprint_issues")
def test_status_formats_jira_issues(mock_fetch):
    mock_fetch.return_value = [
        {"key": "PROJ-1", "summary": "Fix bug", "status": "In Progress"},
    ]
    result = handle_command("@bot status", [])
    assert "PROJ-1" in result
```

## Test File Organization

```
agents/slack-bot/
├── app.py
├── pyproject.toml
├── tests/
│   ├── conftest.py            # Shared fixtures
│   ├── test_app.py            # Unit tests for app.py
│   ├── test_commands.py       # Command handler tests
│   └── test_integrations.py   # Integration tests with mocked APIs
└── prompts/
    └── ...
```

## Common Testing Mistakes to Avoid

### Testing Implementation Details
```python
# DON'T test internal state
assert handler._internal_cache == {"key": "value"}

# DO test observable behavior
result = handler.process("input")
assert result == "expected output"
```

### Tests Depend on Each Other
```python
# DON'T rely on previous test state
# DO setup data in each test using fixtures
```

### No Test Isolation
```python
# DON'T use real Slack/Jira/LLM connections in tests
# DO mock all external dependencies
```

## Best Practices

1. **Write Tests First** — always TDD
2. **One Assert Per Test** — focus on single behavior
3. **Descriptive Test Names** — explain what's tested
4. **Arrange-Act-Assert** — clear test structure
5. **Mock External Dependencies** — isolate unit tests
6. **Test Edge Cases** — empty, None, malformed input
7. **Test Error Paths** — not just happy paths
8. **Keep Tests Fast** — unit tests < 50ms each
9. **Clean Up After Tests** — no side effects
10. **Review Coverage Reports** — identify gaps
