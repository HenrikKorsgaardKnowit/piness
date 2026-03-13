# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**piness** — A Python service for the InkyWHAT e-ink display on a Raspberry Pi. Displays system info (hostname, IP, status), graphs from external events (e.g. agent token consumption), and a tweet-like message feed. Events and messages are ingested via a FastAPI HTTP API.

## Commands

- `make test` — run tests locally
- `make test-cov` — run tests with coverage report
- `make deploy` — rsync code to Pi (reads `.env` for SSH credentials)
- `make run-remote` — SSH into Pi and start the service
- `.venv/bin/pip install -e ".[dev]"` — install for local development
- `.venv/bin/pip install -e ".[dev,rpi]"` — install with Pi hardware deps

## Architecture

- **Display driver abstraction**: `MockDriver` for local dev (saves PNG), `InkyDriver` for real hardware
- **Panels**: sysinfo, graph, messages — each returns a Pillow Image, composited by the renderer
- **API**: FastAPI with POST /events, POST /messages, GET /status
- **Storage**: In-memory ring buffers (ephemeral by design, lost on restart)
- **Deployment**: rsync over SSH to Pi, systemd service

## Architecture Decision Records

Architectural decisions are tracked as ADRs in `docs/adrs/`. Use the `/adr` skill to draft new records.

When the conversation involves choosing a technology, design pattern, API shape, data model, deployment strategy, or any other decision with lasting consequences — proactively suggest running `/adr` to capture it. Don't gate progress on it, but nudge the user so decisions don't go unrecorded.

### Key Decisions

- [ADR001](docs/adrs/ADR001-python-as-implementation-language.md) — Python (driven by InkyWHAT library)
- [ADR002](docs/adrs/ADR002-display-driver-abstraction.md) — Display driver abstraction for local dev
- [ADR003](docs/adrs/ADR003-fastapi-for-event-ingestion.md) — FastAPI for HTTP event ingestion
- [ADR004](docs/adrs/ADR004-rsync-deployment.md) — rsync-based deployment to Pi
- [ADR005](docs/adrs/ADR005-in-memory-ring-buffer.md) — In-memory ring buffer (ephemeral storage)
