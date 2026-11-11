"""Shared pytest fixtures.

Put fixtures both people need here: a test database session, a fake LLM,
a fake insurer channel, and a fixed clock. Unit tests go in tests/unit
(no database, no network); tests that need Postgres or Temporal go in
tests/integration.
"""
