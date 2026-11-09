# Rasd

AI agent for after-sales motor insurance service tickets in Oman. Read
`docs/spec.md` for the full picture and `docs/ROADMAP.md` for the build rounds.
Each round is a GitHub issue that says who does what.

## Rules that must never break

- Nothing reaches an insurer without the staff approval `interrupt` (gate 1).
- No payment link reaches a customer without the second approval (gate 2).
- No secrets or real customer data in code; use `.env` (see `.env.example`).

## Planned layout

- `app/domain.py`: service types, ticket states, required documents
- `app/db/`: models and migrations
- `app/graph/`: the LangGraph ticket graph and its nodes
- `app/services/`: pure business rules (documents, reminders, prices); keep them I/O-free
- `app/integrations/`: the `InsurerChannel` contract, plus email and portal channels
- `app/workflows/`: Temporal workflows
- `app/api/`: FastAPI
- `ui/`: staff screens and dashboard
- `tests/`: pytest; every new behaviour gets a test

## Commands

```bash
pytest -q
ruff check .
ruff format .
```

## Conventions

- Python 3.12, type hints everywhere, line length 100.
- Graph state holds plain dicts and strings so the checkpointer can store it.
- Inject time (`today_fn`, `now`) instead of calling the clock inside logic.
- LLM calls are mocked in tests so CI never needs an API key.
