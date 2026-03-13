---
title: Python as implementation language
status: accepted
created: 2026-03-13
tags: [language, foundational]
---

## Status

Accepted

## Context

piness is a display service for the InkyWHAT e-ink display on a Raspberry Pi. We need to choose an implementation language.

## Decision

Use Python as the sole implementation language.

## Options Considered

### Python
- **Pros:** The Pimoroni `inky` library is Python-only and is the official maintained driver. Pillow integrates directly. Large ecosystem for Pi projects.
- **Cons:** Slower runtime than compiled alternatives. Dynamic typing.
- **When to choose:** When using InkyWHAT hardware.

### Go
- **Pros:** Single binary deployment, strong typing, fast.
- **Cons:** No InkyWHAT driver exists. Would need to write SPI communication from scratch or shell out to Python anyway.
- **When to choose:** If the display had a Go driver or we only needed the HTTP API.

### Node.js
- **Pros:** Familiar for web APIs, good async model.
- **Cons:** No InkyWHAT driver. Higher memory footprint on Pi. Image manipulation ecosystem weaker than Pillow.
- **When to choose:** If building a web-only dashboard without e-ink.

## Consequences

- All code is Python 3.11+
- Pi-specific hardware deps (`inky[rpi]`) are isolated behind an optional extra so local dev works without them
- The `inky` library dictates our display interaction model (Pillow Image → set_image → show)
