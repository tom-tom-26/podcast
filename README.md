# Plainly Put

A podcast made for one listener. The owner names a topic from their phone, a Claude Code skill researches it and writes a script with its sources, and GitHub Actions turns the script into audio with open-source text-to-speech and publishes it to an unlisted feed. It costs nothing beyond the owner's Claude plan.

## Where things live

- `pipeline/`: the Python package that lints scripts, renders audio, publishes Episodes and builds the site.
- `docs/wayfinder/`: the planning history, including the spec (`spec.md`) and the research behind it.
- `artwork/`: the Cover, drawn as an SVG. `python artwork/render.py` redraws `cover.png` after `pip install -e ".[artwork]"`.
- `GLOSSARY.md`: what the words in this repo mean.

## Running it

```
pip install -e ".[dev]"
pytest
pipeline --help
```

The tests need `ffmpeg` and `ffprobe` on the path. To hear a Bundle locally, install the engine with `pip install -e ".[kokoro]"`, put the Kokoro int8 model and voices file in `models/` (the publish-episode workflow shows where they come from), then:

```
pipeline lint tests/fixtures/bundles/2026-10-30-smoke
pipeline render tests/fixtures/bundles/2026-10-30-smoke --out out/smoke.wav
pipeline publish tests/fixtures/bundles/2026-10-30-smoke --wav out/smoke.wav --dry-run --out-dir out
```

On GitHub, run the publish-episode workflow with a Bundle id: with `dry_run` you get the `.m4a` as a workflow artifact; without it the Episode goes up as a Release, is added to `episodes.yaml` (the Episode registry), and the deploy-site workflow rebuilds the Pages site from the registry, `config/show.yaml` and the Releases. Run deploy-site by hand to redeploy. If any audio can't be fetched or a check fails, nothing is deployed and the last good site stays up.
