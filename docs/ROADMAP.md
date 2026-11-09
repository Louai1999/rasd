# Roadmap: build rounds

Rasd is built in **9 rounds**. Each round is one GitHub issue (label `round`)
with the tasks for both people, where their work meets, and when the round
counts as done.

The split is **50/50 by size**: every task has points (1 = a few hours,
5 = several days), and each person has **5 points in every round**, so
**45 points each** in total.

| Person | Who | Leans towards |
|---|---|---|
| A | Louai (@Louai1999) | Backend logic, the LangGraph agent, AI steps |
| B | @rahafsk | Infrastructure, integrations, screens |

Both people touch every layer across the rounds: the database, AI, integrations
and UI. Neither ends up with only "easy" or only "hard" work.

| Round | Theme | Person A (5 pts) | Person B (5 pts) |
|---|---|---|---|
| 1 | Foundation and database | Project structure, core schema and migrations | Docker Compose, settings and price tables, seed data |
| 2 | Tickets and customer intake | Ticket API and state machine | Inbound message endpoint and document storage |
| 3 | AI understanding | LangGraph skeleton, LLM classification and extraction | RAG knowledge base of insurer procedures |
| 4 | Document checks | OCR pipeline and graph integration | Validation rules and missing-document messages |
| 5 | Staff approval (gate 1) | Interrupt, draft request, approval API | Staff approval screen and audit log view |
| 6 | Talking to insurers | Email channel and reading replies | Mock insurer portal and Playwright channel |
| 7 | Timers and reminders | Resume the graph from Temporal, customer reminders | Temporal polling, insurer reminders, escalation |
| 8 | Payment and closing (gate 2) | Payment gate, two-round pricing, closing | Payment link, webhook, price-change detection |
| 9 | Dashboard and demo | Stats API and time-saved figure | Dashboard and settings screens |

## Rules

- A round starts when the previous round's pull requests are merged.
  Inside a round, A and B work in parallel on their own branches.
- **Agree first, then build:** each round names one thing both people must agree
  on before coding (a schema, an interface, a data format). Write it down in the
  issue as a comment.
- Every pull request needs a green CI, the AI review addressed, and one approval
  from the other person.
- Tick the task boxes in the issue as you finish. Close the issue when every
  "Done when" box is ticked.
- To change the split, comment on the issue so both of you agree.
