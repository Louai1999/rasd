# Work split

The work is split **50/50 by size, not by count**. Each task has points
(1 = a few hours, 5 = several days). Both halves add up to **27 points**.

The split is by area, so each person owns their part end to end and the two
of you rarely edit the same files:

- **Person A: the brain.** Everything the agent *thinks*: the graph,
  classification, documents, approvals and the staff screen.
- **Person B: the hands and the clock.** Everything the agent *does* in the
  outside world and *when*: email, portals, Temporal timers, payments,
  settings and the dashboard.

The two halves meet at one contract,
[`app/integrations/channels.py`](../app/integrations/channels.py): A's graph
calls `InsurerChannel.submit(...)`, and B implements it for email and portals.
Until B's channels are ready, A uses `FakeChannel` in tests.

| Person | GitHub | Area |
|---|---|---|
| A | Louai (`@<louai-username>`) | The brain |
| B | Teammate (`@<teammate-username>`) | The hands and the clock |

## Person A: the brain (27 points)

| # | Task | Points | Main files | Done |
|---|---|---|---|---|
| A1 | Database schema and models: customers, policies, tickets, messages, approvals, audit log | 3 | `app/db/` | [ ] |
| A2 | Complete the LangGraph ticket graph: second half (insurer reply, payment gate, issuing), checkpointer on Postgres | 5 | `app/graph/` | [ ] |
| A3 | Classification and data extraction with the LLM (structured output), replacing the keyword stub | 3 | `app/graph/nodes.py` | [ ] |
| A4 | OCR for images and PDFs, feeding `check_documents` | 5 | `app/services/ocr.py` | [ ] |
| A5 | Approval API: list waiting tickets, approve, edit, reject (resumes the graph) | 3 | `app/api/` | [ ] |
| A6 | Staff approval screen | 3 | `ui/approvals` | [ ] |
| A7 | Read insurer replies: approved or not, price, and price-change detection against the price table | 3 | `app/services/replies.py` | [ ] |
| A8 | End-to-end demo of scenario 3 (missing and expired documents) | 2 | `tests/e2e/` | [ ] |

## Person B: the hands and the clock (27 points)

| # | Task | Points | Main files | Done |
|---|---|---|---|---|
| B1 | Docker Compose (Postgres with pgvector, Temporal, Mailpit) and seed data for 4 mock insurers | 3 | `docker-compose.yml`, `scripts/seed.py` | [ ] |
| B2 | RAG knowledge base of insurer procedures and required documents | 3 | `app/services/rag.py`, `knowledge/` | [ ] |
| B3 | Email channel: send, read the inbox, match replies to tickets by `[T-xxxx]` in the subject | 5 | `app/integrations/email.py` | [ ] |
| B4 | Mock insurer portal and the Playwright channel (submit, check status, screenshot every step) | 5 | `mock_portal/`, `app/integrations/portal.py` | [ ] |
| B5 | Temporal workflows: polling, insurer and customer reminders, escalation (uses `next_insurer_action`) | 5 | `app/workflows/` | [ ] |
| B6 | Test-mode payment link, and the price table with change history | 3 | `app/services/payments.py`, `app/services/prices.py` | [ ] |
| B7 | Settings screen and stats dashboard (open, in review, closed, emails sent, reminders) | 3 | `ui/settings`, `ui/dashboard` | [ ] |

## Shared (both of you)

- Review each other's pull requests. Every PR needs one approval from the other person.
- Keep `docs/spec.md` up to date when a decision changes.
- Log important AI prompts in `docs/ai-dev-log.md`.
- Run all three scenarios end to end before the final demo, and prepare the presentation together.

## Order of work

1. **Week 1:** A1 and B1 first, because everything else needs the database and Docker.
2. **Then in parallel:** A2–A5 alongside B2–B5. Agree on any change to `channels.py` before making it.
3. **Last:** A6–A8 and B6–B7, then the joint end-to-end run.

To change the split, edit this file in a pull request so both of you agree on it.
