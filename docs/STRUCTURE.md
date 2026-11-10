# Project structure

Every placeholder file says at the top what it is for, who owns it, and in
which round it gets built. Open the file, read the docstring, and start there.

**A** = @Louai1999 · **B** = @rahafsk · **A+B** = agree together before coding

```
rasd/
├── app/
│   ├── config.py                  B  R1  settings from .env
│   ├── domain.py                  A+B R1 enums shared by everything
│   ├── db/
│   │   ├── session.py             A  R1
│   │   └── models/
│   │       ├── core.py            A  R1  customers, policies, tickets…
│   │       └── settings.py        B  R1  services, reminders, prices, knowledge
│   ├── api/
│   │   ├── main.py                A  R1  FastAPI app, /health
│   │   └── routes/
│   │       ├── tickets.py         A  R2
│   │       ├── inbound.py         B  R2  simulated WhatsApp
│   │       ├── approvals.py       A  R5  gate 1 and gate 2
│   │       ├── payments.py        B  R8  webhook
│   │       ├── settings.py        B  R9
│   │       └── stats.py           A  R9
│   ├── services/                  business logic; keep the rule modules I/O-free
│   │   ├── tickets.py             A  R2  state machine
│   │   ├── storage.py             B  R2  uploaded files
│   │   ├── llm.py                 A  R3  LLM wrapper, mocked in tests
│   │   ├── rag.py                 B  R3  knowledge base lookup
│   │   ├── ocr.py                 A  R4
│   │   ├── documents.py           B  R4  validation rules
│   │   ├── customer_messages.py   B  R4
│   │   ├── replies.py             A  R6  read insurer replies
│   │   ├── reminders.py           B  R7  poll / remind / escalate rules
│   │   ├── prices.py              B  R8  price changes and history
│   │   └── stats.py               A  R9
│   ├── graph/                     the LangGraph agent
│   │   ├── state.py               A  R3
│   │   ├── graph.py               A  R3
│   │   └── nodes/
│   │       ├── classify.py        A  R3
│   │       ├── documents.py       A  R4
│   │       ├── approval.py        A  R5  interrupt, gate 1
│   │       ├── insurer.py         A  R6
│   │       └── payment.py         A  R8  interrupt, gate 2
│   ├── integrations/
│   │   ├── channels.py            A+B R6 InsurerChannel interface
│   │   ├── email.py               A  R6
│   │   ├── portal.py              B  R6  Playwright
│   │   └── payments.py            B  R8
│   └── workflows/                 Temporal
│       ├── ticket_workflow.py     B  R7
│       ├── signals.py             A  R7
│       └── worker.py              B  R7
├── ui/                            staff screens
│   ├── app.py                     B  R5
│   └── pages/
│       ├── approvals.py           B  R5
│       ├── dashboard.py           B  R9
│       └── settings.py            B  R9
├── mock_portal/app.py             B  R6  fake insurer portal
├── knowledge/                     B  R3  fictional insurer procedures
├── migrations/                    A  R1  Alembic
├── scripts/seed.py                B  R1  fictional data
├── tests/
│   ├── conftest.py                shared fixtures
│   ├── unit/                      no database, no network
│   └── integration/               needs Postgres or Temporal
└── docs/                          spec, ERD, roadmap, this file
```

`docker-compose.yml` is not here yet: it is Person B's first task in Round 1.

## Why the split rarely collides

- Database models are two files: `core.py` (A) and `settings.py` (B).
- Each route, service and graph node is its own file with one owner.
- The two shared files, `domain.py` and `channels.py`, are agreed in the round
  issue before either person changes them.
