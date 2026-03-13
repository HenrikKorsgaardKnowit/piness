---
name: readme
description: Generate or update a README.md following Gaia README templates. Choose lightweight (quick-start focused) or extended (comprehensive project documentation).
---

# README Generator

Generate a README.md for the current project using Gaia's standardized templates. Two variants exist — pick the one that fits.

## When to Use

- New project needs a README
- Existing README needs to be restructured to follow the standard
- User asks to create or update a README

## Template Selection

| Template | Best For | Focus |
|----------|----------|-------|
| **Lightweight** | New projects, small tools, early-stage repos | Getting a developer running fast |
| **Extended** | Established projects, team-shared codebases | Full project documentation A-Z |

If unclear, ask the user. Default to **lightweight** for repos with < 5 contributors or no CI/CD pipeline.

## Process

1. **Analyze the project** — Read the repo structure, existing configs (`package.json`, `pyproject.toml`, `Dockerfile`, `docker-compose.yml`, `.env.example`, CI configs), and any existing README.
2. **Choose template** — Based on project maturity or user preference.
3. **Fill in sections** — Use actual project data. Never leave placeholder text like "Provide information how to build project." Every section must contain real, actionable content or be omitted.
4. **Omit irrelevant sections** — If a section doesn't apply (e.g., no database, no frontend), drop it entirely. Don't include empty sections.
5. **Write the README** — Output to `README.md` in the project root (or the location the user specifies).

## Lightweight Template

Use for quick-start documentation. Structure:

```markdown
# Project Name

Brief description of what the project does and its purpose.

## Getting Started

### Prerequisites

List required software with install commands.

### Installation

Step-by-step build instructions.

### Usage

How to run the project. Include any required environment variables,
third-party services, or test credentials (if applicable).
```

Rules:
- Every prerequisite must include a version requirement and install command
- Installation steps must be copy-pasteable — a developer should go from clone to running with no guesswork
- If the project has separate frontend/backend/database setup, use sub-sections (`### Database`, `### Frontend`, `### Backend`)

## Extended Template

Use for comprehensive documentation. Structure:

```markdown
# Project Name

Brief description of what the project does and its purpose.

## Table of Contents

Auto-generated from sections included.

## Prerequisites

Software dependencies and access permissions.

## Installation

Build instructions with sub-sections per component
(Database, Frontend, Backend) as needed.

## Usage

How to run. Environment variables, services, test accounts.

## Branching

Branching strategy and workflow.

## Environments

Table of environments:

| | Local | Dev | Test | Preprod | Prod |
|---|---|---|---|---|---|
| FE | | | | | |
| BE | | | | | |
| Hosting | | | | | |
| Branch | | | | | |

## CI/CD

Pipeline links, deployment instructions, approval rules.

## Testing

How to run tests.

## Logging

Where to find logs (Application Insights, local, CMS, etc.).

## Design System

Figma links, Storybook, component library references.

## Helpful Links

Wiki, board, source code, team chat.

## Contact

Product owner, project manager, architect, developers.

## License

License under which the project is distributed.
```

Rules:
- Table of Contents must link to all included sections
- Environments table must reflect actual environments (check CI configs, deployment manifests)
- Contact section should list roles, not just names — the README outlives individual team members
- Helpful Links should include real URLs, not empty markdown links

## Quality Checklist

Before finishing, verify:

- [ ] No placeholder text remains — every sentence is project-specific
- [ ] All commands are copy-pasteable and tested against the actual project
- [ ] Prerequisites list is complete (nothing missing that would block a fresh setup)
- [ ] Environment variables are documented (reference `.env.example` if it exists)
- [ ] Sections that don't apply have been removed, not left empty
