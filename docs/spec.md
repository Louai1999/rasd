# Rasd: specification

## Problem

After a motor policy is issued, customers ask for changes: ownership transfer,
UAE extension, policy extension, adding a driver, cancellation. Staff handle
each ticket by hand: read the message, find the policy, chase missing
documents, email or use the insurer's portal, follow up, send a payment link,
and deliver the endorsement. Tickets run late and some are forgotten.

## Goal

An AI agent that does the repetitive work and the follow-ups, so staff only
make decisions. It must reduce staff time per ticket while keeping a human in
control of anything that leaves the company.

## Hard rules

1. **Nothing reaches an insurer without staff approval** (gate 1).
2. **No payment link reaches a customer without staff approval** (gate 2).
3. Reminders to insurers and customers use fixed templates and may be sent automatically.
4. A document read with low confidence never passes automatically.
5. Every action is written to the audit log: who, what, when.
6. Prices in the price table change only with staff approval; history is kept.

## Services and required documents

See `REQUIRED_DOCUMENTS` in `app/domain.py`. Insurer-specific extras come from
the RAG knowledge base.

## Insurer channels

- **Email:** request and reply matched by `[T-xxxx]` in the subject.
- **Portal:** driven by Playwright, with a screenshot of each step.
- Per insurer: channel, whether the insurer needs its own approval, and whether
  pricing takes one round or two.

## Timing (per service, editable)

See `DEFAULT_POLICIES` in `app/services/reminders.py`. Example: ownership
transfer is polled every 20 minutes, the insurer is reminded after 24 hours,
up to 3 reminders, and the ticket is escalated after 3 days.

## Ticket states

`new → awaiting_documents → in_review → sent_to_insurer → awaiting_insurer →
in_review_payment → awaiting_payment → issuing → closed`, plus `escalated`
and `rejected` from any state.

## Stack

LangGraph (decisions), Temporal (timers and long waits), OCR (documents), RAG
on pgvector (insurer procedures), Playwright (portals), FastAPI, PostgreSQL.

## Out of scope for the prototype

Real insurer connections, real payments and real customer data. Insurers,
portals and payments are simulated.
