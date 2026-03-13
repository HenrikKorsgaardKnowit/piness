# README Maintenance

When working in a project that has a README.md, keep it accurate.

## When to check

After making changes that affect any of these, verify the README still matches reality:

- **Prerequisites** — new dependencies added (`package.json`, `pyproject.toml`, `Dockerfile`, etc.)
- **Installation/setup steps** — build process changed, new env vars required, database migrations added
- **Usage/run commands** — entrypoints changed, new CLI flags, different ports
- **Environments** — new environment added or removed
- **CI/CD** — pipeline config changed

## What to do

- If the README is out of date, flag it to the user: describe what's stale and suggest the fix.
- Do not silently update the README — always tell the user what changed and why.
- If the project has no README and the changes are non-trivial, suggest creating one using the `/readme` skill.

## What NOT to do

- Don't rewrite the entire README for a minor change. Surgical edits only.
- Don't add sections that weren't there before without asking.
- Don't block the user's work — this is a nudge, not a gate.
