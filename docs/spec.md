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

| Service | Customer documents |
|---|---|
| Ownership transfer | Vehicle registration, new owner's ID card, new owner's driving licence |
| UAE extension | None beyond the policy on file |
| Policy extension | Vehicle registration, driving licence |
| Add a driver | Driver's ID card, driver's driving licence |
| Cancellation and refund | Reason, plus proof of sale if sold |

Insurer-specific extras come from the RAG knowledge base.

## Insurer channels

- **Email:** request and reply matched by `[T-xxxx]` in the subject.
- **Portal:** driven by Playwright, with a screenshot of each step.
- Per insurer: channel, whether the insurer needs its own approval, and whether
  pricing takes one round or two.

## Timing (per service, editable)

| Service | Poll | Remind insurer after | Max reminders | Remind customer after | Escalate after |
|---|---|---|---|---|---|
| Ownership transfer | 20 min | 24 h | 3 | 24 h | 3 days |
| UAE extension | 30 min | 4 h | 3 | 6 h | 12 h |
| Policy extension | 60 min | 24 h | 2 | 24 h | 48 h |
| Add a driver | 60 min | 24 h | 2 | 24 h | 48 h |
| Cancellation and refund | 2 h | 48 h | 2 | 48 h | 5 days |

Example defaults; staff edit them from the settings screen.

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
