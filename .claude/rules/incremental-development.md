# Incremental Development

Work in small, verified steps. Never stack untested changes.

## One change at a time

- Make a single functional change (one new dependency, one new function, one config change)
- Verify it works before moving to the next change
- If a change touches multiple files, verify after each file edit when possible

## Verify before progressing

After every code change, prove it works:

- **New dependency added**: run `pip install` and confirm import works
- **New env var or config**: run a minimal script or test that reads it
- **New function**: write a test or run it interactively
- **Changed event handler**: run the app and trigger the event
- **Bug fix**: reproduce the bug first, then verify the fix

Do not assume something works. Run it.

## Ask before assuming

If a change could fail for reasons outside the code (missing env var, wrong API scope, network issue), stop and ask the user to verify rather than silently moving on.

## No batching unrelated changes

- Don't edit 3 files in one shot unless they're trivially coupled (e.g., adding a dependency to pyproject.toml and importing it)
- Don't add a feature and refactor at the same time
- Don't fix a bug and add a new capability in the same step

## Checkpoint with the user

After verifying a change works, briefly state what was done and what the next step is. Let the user confirm direction before continuing. Don't auto-chain into the next feature.
