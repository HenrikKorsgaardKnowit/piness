---
title: rsync-based deployment to Raspberry Pi
status: accepted
created: 2026-03-13
tags: [deployment, workflow]
---

## Status

Accepted

## Context

We need a way to get code from the development machine onto the Raspberry Pi during development. SSH credentials are stored in `.env`.

## Decision

Use `rsync` over SSH to sync source code to the Pi. Wrapped in a `make deploy` target and `scripts/deploy.sh`.

## Options Considered

### rsync over SSH (chosen)
- **Pros:** Fast incremental sync (only changed files). Simple. Works with any Pi setup. No extra software on Pi beyond SSH.
- **Cons:** Requires `sshpass` for password-based auth (or SSH keys). Not idempotent for dependency installation.

### Git pull on Pi
- **Pros:** Familiar workflow, Pi always has a clean checkout.
- **Cons:** Requires git on Pi, pushing to remote before every test, slower iteration loop.

### Docker
- **Pros:** Reproducible environment, easy dependency management.
- **Cons:** Docker on Pi is resource-heavy. InkyWHAT hardware access from containers requires privileged mode and device mapping. Overkill for a single-device deploy.

### Ansible
- **Pros:** Declarative, handles deps and service management.
- **Cons:** Heavy tooling for a single target device. Slower iteration than rsync.

## Consequences

- `make deploy` is the primary deployment command
- SSH key auth is recommended over `sshpass` for security
- `deploy.sh` also handles `pip install` on the Pi when `pyproject.toml` changes
- `.env` must never be committed (contains PI_HOST, PI_USER, PI_PASSWORD)
