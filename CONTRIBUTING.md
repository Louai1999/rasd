# How we work

## Daily flow

1. Pull the latest `main`: `git checkout main && git pull`
2. Create a branch for your task: `git checkout -b r3-a-classification`
   (round number, your letter from the round issue, short name)
3. Write code and tests. Run `uv run pytest -q` and `uv run ruff check .` before pushing.
4. Push and open a pull request: `git push -u origin HEAD`, then `gh pr create`
5. Wait for **CI**: it runs lint and all tests on every push. It must be green.
6. Ask for an **AI review** (see below), fix what it finds, and push again.
7. **@Louai1999 reviews and approves** every pull request (see Code review below). Then merge.

## AI review in Claude Code

Open this project in Claude Code (desktop app or terminal) and ask:

> Review PR #12 and post your comments on GitHub.

Claude reads the change, checks it against `docs/spec.md`, and
can leave comments on the lines that need work. It uses your normal Claude
subscription, so no API key or token is needed. Whoever opens the pull
request asks for the review.

`main` is protected: nobody pushes to it directly, and a pull request needs a
green CI and an approval from the code owner before it can be merged.

## Code review

@Louai1999 is the code owner (see `.github/CODEOWNERS`) and reviews every
pull request. GitHub requests the review automatically when a PR opens.

- **@rahafsk's pull requests** need @Louai1999's approval to merge.
- **@Louai1999's own pull requests:** GitHub does not let anyone approve their
  own PR, so after CI is green and the AI review is done, @Louai1999 merges
  them as the repository admin.

## Setup

The project uses [uv](https://docs.astral.sh/uv/) for Python and packages.
Install it once:

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"   # Windows
curl -LsSf https://astral.sh/uv/install.sh | sh                                       # macOS / Linux
```

Then, in the project folder:

```bash
uv sync                 # installs Python 3.12 and every package from uv.lock
uv run pytest -q        # tests
uv run ruff check .     # lint
uv run ruff format .    # format
```

- Add a library: `uv add <name>` (or `uv add --dev <name>` for test tools).
  Commit both `pyproject.toml` and `uv.lock`.
- Never use `pip install`; it bypasses the lock file.
- After pulling someone else's changes, run `uv sync` again.

Copy `.env.example` to `.env` and fill in your own keys. Never commit `.env`.
