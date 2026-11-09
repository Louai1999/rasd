# How we work

## Daily flow

1. Pull the latest `main`: `git checkout main && git pull`
2. Create a branch for your task: `git checkout -b r3-a-classification`
   (round number, your letter from the round issue, short name)
3. Write code and tests. Run `pytest -q` and `ruff check .` before pushing.
4. Push and open a pull request: `git push -u origin HEAD`, then `gh pr create`
5. Wait for the checks:
   - **CI** runs lint and all tests. It must be green.
   - **AI code review** reads the change and leaves comments on lines that need work.
6. Fix what the review found, push again. Both checks run again on every push.
7. Your teammate reviews and approves. Then merge.

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
