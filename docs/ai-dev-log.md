# AI development log

Rasd is built with AI-driven development: we write the spec, an AI coding
assistant writes code and tests under our direction, and we review everything.
Record each significant prompt here, newest first.

## Template

```
### YYYY-MM-DD · <your name> · <task id, e.g. A3>
**Tool:** Claude Code / Cursor
**Prompt:** what you asked for (short)
**Result:** what it produced
**What we changed and why:** your corrections
**Lesson:** what to ask differently next time
```

---

### 2026-11-09 · Louai · setup
**Tool:** Claude Code
**Prompt:** Set up the repo with CI on every push, an AI reviewer that
comments on pull requests, and a build plan in rounds split 50/50 between two
people, one GitHub issue per round.
**Result:** CI and AI review workflows, spec, roadmap and nine round issues.
**What we changed and why:** The AI first wrote starter code. We removed it so
we build every part ourselves, round by round.
**Lesson:** Say up front whether you want code or only a plan.
