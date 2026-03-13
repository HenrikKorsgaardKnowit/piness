---
title: FastAPI for HTTP event ingestion
status: accepted
created: 2026-03-13
tags: [api, framework]
---

## Status

Accepted

## Context

The service needs an HTTP API to receive external events (e.g. token consumption from agents) and text messages for display. We need to choose an HTTP framework.

## Decision

Use FastAPI with uvicorn as the HTTP server.

## Options Considered

### FastAPI + uvicorn (chosen)
- **Pros:** Async support, automatic request validation via Pydantic, auto-generated API docs at `/docs`, excellent `TestClient` for testing. Already proving its value — Pydantic catches malformed payloads, TestClient enables clean test setup.
- **Cons:** Heavier dependency chain than minimal alternatives. Arguably overkill for 3 endpoints.
- **When to choose:** When you want validation, docs, and testability out of the box.

### Flask
- **Pros:** Simpler, lighter, widely known.
- **Cons:** No async, no built-in validation, separate test client setup.
- **When to choose:** When simplicity matters more than auto-validation and the endpoint count stays very low.

### Bare `http.server`
- **Pros:** Zero dependencies, part of stdlib.
- **Cons:** Manual JSON parsing, no validation, no routing framework, painful to maintain and test.
- **When to choose:** When you truly cannot add any dependencies.

### MQTT (e.g. with mosquitto broker)
- **Pros:** IoT-native, pub/sub fits the event model well, very low per-message overhead.
- **Cons:** Requires running a broker, different paradigm from request/response, harder to test, agents would need MQTT clients.
- **When to choose:** When multiple Pi devices need to communicate or when agents already speak MQTT.

## Consequences

- FastAPI + uvicorn + Pydantic are core dependencies
- API docs are available at `/docs` on the running service (useful for debugging on the Pi)
- Tests use `httpx` via FastAPI's `TestClient`
- If resource usage becomes a concern on the Pi, monitor uvicorn's memory footprint — fall back to single-worker mode or Flask if needed
