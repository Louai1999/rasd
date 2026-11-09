# Rasd

An AI agent for after-sales motor insurance service tickets in Oman:
ownership transfer, UAE extension, policy extension, adding a driver and
cancellation.

Rasd classifies each request, checks the customer's documents with OCR, talks
to insurers by email or through their portals, and follows up on replies and
reminders by itself. Staff step in at two points only: before a request goes
to the insurer, and before a payment link goes to the customer.

## Stack

LangGraph · Temporal · OCR · RAG (pgvector) · Playwright · FastAPI · PostgreSQL

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
pytest -q
uvicorn app.api.main:app --reload
```

## Project docs

- [Specification](docs/spec.md)
- [Work split](docs/WORK_SPLIT.md)
- [How we work](CONTRIBUTING.md)
- [AI development log](docs/ai-dev-log.md)

## Status

Early prototype. Insurers, portals and payments are simulated, and all
customer data is fictional.
