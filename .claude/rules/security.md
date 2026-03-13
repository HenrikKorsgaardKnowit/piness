# Security Guidelines for Agent Development

## Secrets Management

NEVER hardcode secrets:

```python
# WRONG
api_key = "sk-ant-xxxxx"

# CORRECT
api_key = os.environ["ANTHROPIC_API_KEY"]
```

- One service account per agent per integration, scoped to minimum permissions
- Secrets loaded from environment variables or a vault, never from code
- Per-agent secret namespacing (each agent only accesses its own secrets)
- No shared API keys between agents

## Before Any Commit

- [ ] No hardcoded secrets (API keys, tokens, passwords)
- [ ] No secrets in log output
- [ ] .env files are in .gitignore
- [ ] API keys are scoped to minimum required permissions

## Agent-Specific Security

### Prompt Injection
- Validate and sanitize all external input before including in prompts
- Never pass raw user input (Slack messages, GitHub data) directly into system prompts
- Use structured tool outputs, not free-form text injection

### LLM Output Handling
- Never execute LLM output as code without validation
- Treat LLM responses as untrusted input when they drive actions (API calls, file writes)
- Validate LLM output structure before passing to integrations

### API Key Scoping
- Read-only keys where the agent only reads (e.g., Slack bot reading channels)
- Write keys scoped to specific resources (e.g., GitHub issues in one repo, not org-wide)
- LLM gateway mediates all model access — agents never hold provider API keys directly

### Rate Limiting
- Respect external API rate limits
- Implement backoff on 429 responses
- LLM gateway enforces per-agent token budgets

## Security Response

If a security issue is found:
1. Stop and fix before continuing
2. Check if similar patterns exist elsewhere in the codebase
3. Rotate any exposed secrets immediately
4. Document the fix
