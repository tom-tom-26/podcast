# Plainly Put

A podcast made for one listener. The owner names a topic from their phone, a Claude Code skill researches it and writes a script with its sources, and GitHub Actions turns the script into audio with open-source text-to-speech and publishes it to an unlisted feed. It costs nothing beyond the owner's Claude plan.

## Where things live

- `pipeline/`: the Python package that lints scripts, renders audio, publishes Episodes and builds the site.
- `docs/wayfinder/`: the planning history, including the spec (`spec.md`) and the research behind it.
- `GLOSSARY.md`: what the words in this repo mean.

## Running it

```
pip install -e ".[dev]"
pytest
pipeline --help
```

The entry points are placeholders for now and exit with "not built yet".
