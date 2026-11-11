# Rasd

An AI agent for after-sales motor insurance service tickets in Oman:
ownership transfer, UAE extension, policy extension, adding a driver and
cancellation.

Rasd classifies each request, checks the customer's documents with OCR, talks
to insurers by email or through their portals, and follows up on replies and
reminders by itself. Staff step in at two points only: before a request goes
to the insurer, and before a payment link goes to the customer.

## Stack

LangGraph · Temporal · OCR · RAG (pgvector) · Playwright · FastAPI · PostgreSQL · uv

## Quick start

```bash
uv sync
uv run pytest -q
```

Full setup in [CONTRIBUTING.md](CONTRIBUTING.md).

## Project docs

- [Vision (PDF)](docs/Rasd-vision.pdf)
- [Specification](docs/spec.md)
- [Roadmap: build rounds](docs/ROADMAP.md)
- [Database design (ERD)](docs/erd.md)
- [Project structure](docs/STRUCTURE.md)
- [How we work](CONTRIBUTING.md)
- [AI development log](docs/ai-dev-log.md)

## Status

Planning done; building starts with Round 1. Insurers, portals and payments
will be simulated, and all customer data is fictional.
