# Plainly Put

A personal podcast tool. The `episode` Skill writes Bundles; the `pipeline` package turns them into published Episodes and the Feed. The plan behind every decision is in `docs/wayfinder/` (start with `spec.md`). Where the spec and a closed ticket disagree, the ticket wins.

## Agent skills

### Issue tracker

Build tickets live in GitHub Issues on this repo. See `docs/agents/issue-tracker.md`.

### Triage labels

The five default triage labels, plus `episode`, `pipeline-failure` and `needs-owner`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `GLOSSARY.md` and `docs/adr/` at the root. See `docs/agents/domain.md`.

## Build rules

From `docs/wayfinder/research/18-human-feel-and-ai-deslop.md` section 7.

1. Names come from `GLOSSARY.md`. A new domain word goes into the glossary first.
2. Comments explain why; no comment restates code.
3. No abstraction until the second real use. The one exception is the `synthesise(text, voice)` seam, because swapping TTS engines is a stated requirement.
4. Commit messages: imperative subject, a body that says why when the change isn't obvious, no file lists, no emoji, attribution lines as the repo requires.
5. Logs: one line per stage with counts and timings; errors say what failed and on which input (chunk index, Episode id).
6. Docs: one README a person could read in two minutes. Spec decisions live in `docs/wayfinder/`, not repeated in code docs.
7. The phrase lint (research/18 section 9) runs over READMEs, commit messages and log message strings, warning only.

Also:

- Say only what was run. Don't write "all tests pass" or "verified" unless you ran it.
- The public entry points are `pipeline.lint`, `render`, `publish` and `site`; `pipeline/cli.py` only dispatches to them. Everything else goes under `pipeline/_lib/`. import-linter fails the build if a listed root package outside `pipeline` imports `_lib`, so a new top-level package must be added to the contract in `pyproject.toml`.
- Tests drive the public entry points with fixture Bundles and a fake GitHub client (spec, Testing Decisions). Don't test private helpers.
- Audio never goes in git.
- Build tickets never contain `@claude`.
- Never link the Feed from the README or any other page a search engine might index.

## Commands

```
pip install -e ".[dev]"
pre-commit install
ruff check . && ruff format --check .
lint-imports
pytest
```
