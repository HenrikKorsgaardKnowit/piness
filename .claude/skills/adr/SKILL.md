---
name: adr
description: Review and draft Architecture Decision Records. Use when an architectural decision is detected in conversation, when the user explicitly discusses technology choices or design tradeoffs, or when invoked directly.
argument-hint: "[decision description]"
---

# ADR Review and Drafting

You are reviewing a potential architectural decision. This process applies whether triggered by passive detection during conversation or invoked explicitly via `/adr`.

## Input

$ARGUMENTS

If no arguments are provided, infer the decision from the current conversation context.

## Process

### 1. Identify the decision

State the decision clearly in one sentence. If it's ambiguous, ask the user to clarify before proceeding.

### 2. Challenge it

Before formalizing, push back constructively:

- What alternatives exist? List at least 2 other options.
- What are the tradeoffs of the proposed decision vs. alternatives?
- What are the consequences — what becomes easier and what becomes harder?
- Is this decision reversible? If not, flag that explicitly.
- Is this premature? Do we have enough information to decide now?

Present this as a brief summary, not an essay. Ask the user to confirm, revise, or defer the decision.

### 3. Formalize

Once confirmed, draft the ADR in `docs/adrs/` following the project conventions:

- Filename: `ADR<NNN>-<kebab-case-title>.md` where NNN is the next sequential number (check `docs/adrs/` for the current highest)
- Frontmatter: `title`, `status: accepted`, `created: <today>`, `context` (link to related research if applicable), `tags`
- Sections: Status, Context, Decision, Options Considered (with pros/cons/when-to-choose for each), Consequences

Write the ADR file and present it for review. Do not commit unless asked.

### 4. Update references

After the ADR is written:
- Add it to the Key Documents list in `CLAUDE.md` if it represents a significant project decision.
- If it relates to an existing research document, note the connection.
