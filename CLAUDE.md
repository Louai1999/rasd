# Rasd

AI agent for after-sales motor insurance service tickets in Oman. Read
`docs/spec.md` for the full picture and `docs/WORK_SPLIT.md` for who owns what.

## Rules that must never break

- Nothing reaches an insurer without the staff approval `interrupt` (gate 1).
- No payment link reaches a customer without the second approval (gate 2).
- No secrets or real customer data in code; use `.env` (see `.env.example`).

## Layout

- `app/domain.py`: service types, ticket states, required documents
- `app/graph/`: the LangGraph ticket graph and its nodes
- `app/services/`: pure business rules (documents, reminders); keep them I/O-free
- `app/integrations/channels.py`: the `InsurerChannel` contract; email and portal implement it
- `app/api/`: FastAPI
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
