# How we work

## Daily flow

1. Pull the latest `main`: `git checkout main && git pull`
2. Create a branch for your task: `git checkout -b r3-a-classification`
   (round number, your letter from the round issue, short name)
3. Write code and tests. Run `pytest -q` and `ruff check .` before pushing.
4. Push and open a pull request: `git push -u origin HEAD`, then `gh pr create`
5. Wait for **CI**: it runs lint and all tests on every push. It must be green.
6. Ask for an **AI review** (see below), fix what it finds, and push again.
7. Your teammate reviews and approves. Then merge.

## AI review in Claude Code

Open this project in Claude Code (desktop app or terminal) and ask:

> Review PR #12 and post your comments on GitHub.

Claude reads the change, checks it against `CLAUDE.md` and `docs/spec.md`, and
can leave comments on the lines that need work. It uses your normal Claude
subscription, so no API key or token is needed. Whoever opens the pull
request asks for the review.

`main` is protected: nobody pushes to it directly, and a pull request needs a
green CI and one approval before it can be merged.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt -r requirements-dev.txt
pytest -q
```

Copy `.env.example` to `.env` and fill in your own keys. Never commit `.env`.
