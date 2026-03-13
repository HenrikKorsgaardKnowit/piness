---
title: In-memory ring buffer for event and message storage
status: accepted
created: 2026-03-13
tags: [storage, architecture]
---

## Status

Accepted

## Context

The service receives events and messages via HTTP and displays them on the e-ink screen. We need to decide how to store this data. The display shows recent data — it is not a historical dashboard.

## Decision

Use in-memory ring buffers (`collections.deque` with `maxlen`) for both events and messages. Data is ephemeral and lost on restart.

## Options Considered

### In-memory ring buffer (chosen)
- **Pros:** Zero dependencies, fast, simple implementation. Fixed memory usage regardless of input volume. Fits the use case — the display only shows recent data, and agents continuously push new events.
- **Cons:** All data lost on restart. Cannot query historical ranges.
- **When to choose:** When data is ephemeral by design and the display is the only consumer.

### SQLite
- **Pros:** Survives restarts, supports time-range queries, enables historical graphing over days/weeks.
- **Cons:** File I/O on the Pi's SD card (wear concern with frequent writes). More complexity for schema, migrations, cleanup. Overkill when the display only shows a rolling window.
- **When to choose:** When historical analysis or data retention is a requirement.

### Flat files (append-only log)
- **Pros:** Simple persistence, human-readable, easy to inspect and debug.
- **Cons:** No random access, needs rotation logic to avoid unbounded growth, SD card wear.
- **When to choose:** When you need a simple audit trail but don't need queries.

## Consequences

- Service starts with empty buffers on every restart — this is expected, not a bug
- Buffer sizes are configurable (default: 100 events, 50 messages)
- If historical data becomes valuable later, this decision is easily reversible — swap the buffer backing store for SQLite without changing the panel rendering code
- Agents must tolerate that their data is transient
