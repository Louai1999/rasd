## What this changes

<!-- One or two sentences. Name the round issue: Part of #3 -->

## How I tested it

- [ ] `uv run pytest -q` passes locally
- [ ] `uv run ruff check .` and `uv run ruff format --check .` pass
- [ ] If I added a library, I used `uv add` and committed `uv.lock`
- [ ] Added or updated tests for the new behaviour
- [ ] Asked Claude Code to review this PR and fixed what it found

## Checklist

- [ ] Nothing reaches an insurer or a customer payment link without a staff approval
- [ ] No API keys, passwords or real customer data in the code
- [ ] Logged any important AI prompt in `docs/ai-dev-log.md`
