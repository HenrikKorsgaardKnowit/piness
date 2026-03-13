---
title: Display driver abstraction for local development
status: accepted
created: 2026-03-13
tags: [architecture, testing, display]
---

## Status

Accepted

## Context

The InkyWHAT hardware is only available on the Raspberry Pi. We need to develop and test display rendering logic on a local machine without the hardware.

## Decision

Define a `DisplayDriver` ABC with two implementations: `InkyDriver` (wraps real hardware) and `MockDriver` (saves PNG to disk).

## Options Considered

### Driver abstraction (chosen)
- **Pros:** Full local development loop. Tests run without hardware. Mock output is visually inspectable.
- **Cons:** Thin abstraction layer to maintain.

### No abstraction (always require Pi)
- **Pros:** No indirection, code directly calls `inky`.
- **Cons:** Cannot run or test locally. Every change requires deploy-to-Pi cycle. CI cannot run display tests.

### Headless rendering only (no driver, just save PNG)
- **Pros:** Simpler than an ABC.
- **Cons:** No clean path to swap in real hardware. Production code would need its own integration.

## Consequences

- `InkyDriver` import of `inky` is guarded with try/except — missing on non-Pi machines is expected
- `MockDriver` writes to `/tmp/piness_display.png` for visual inspection
- All panel and renderer tests use `MockDriver`
- The driver is selected based on `config.mock_display` setting
