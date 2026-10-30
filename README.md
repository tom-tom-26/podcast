# Plainly Put

A podcast made for one listener. The owner names a topic from their phone, a Claude Code skill researches it and writes a script with its sources, and GitHub Actions turns the script into audio with open-source text-to-speech and publishes it to an unlisted feed. It costs nothing beyond the owner's Claude plan.

## Where things live

- `pipeline/`: the Python package that lints scripts, renders audio, publishes Episodes and builds the site.
- `learnings/`: lessons the Skill writes after a run goes wrong, with what to do instead, and the Source profile for each field of topics.
- `docs/wayfinder/`: the planning history, including the spec (`spec.md`) and the research behind it.
- `artwork/`: the Cover, drawn as an SVG. `python artwork/render.py` redraws `cover.png` after `pip install -e ".[artwork]"`.
- `GLOSSARY.md`: what the words in this repo mean.

## Making an Episode

Open the Code tab of the Claude iPhone app, start a session on this repo in the `podcast` environment, and name a Topic. The `episode` Skill (`.claude/skills/episode/`) replies with one confirm message; reply "go" or adjust it. It researches, writes the Bundle, lints it, and pushes it on a `claude/` branch with a PR.

Set up once, at claude.ai/code:

- Connect GitHub through the Claude GitHub App. Pushes and the PR go through Anthropic's GitHub proxy, so the session holds no token and the repo has no secret for it.
- Add an environment named `podcast` with **Network access: Full**. The default Trusted level blocks journals, PubMed and news sites, which the research needs.
- Give it this setup script, for reading PDFs as raw text:

  ```
  apt-get update && apt-get install -y poppler-utils || true
  ```

## Running it

```
pip install -e ".[dev,kokoro]"
pytest
pipeline --help
```

The tests need `ffmpeg` and `ffprobe` on the path, and the Kokoro extra for espeak. To hear a Bundle locally, put the Kokoro int8 model and voices file in `models/` (the publish-episode workflow shows where they come from), then:

```
pipeline lint tests/fixtures/bundles/2026-10-30-smoke
pipeline render tests/fixtures/bundles/2026-10-30-smoke --out out/smoke.wav
pipeline publish tests/fixtures/bundles/2026-10-30-smoke --wav out/smoke.wav --dry-run --out-dir out
```

`config/lexicon.yaml` says how each engine should say the terms it gets wrong; a Bundle's `pronunciations` win for that Episode. `pipeline lint <bundle> --pron-check` shows the phonemes Kokoro will get for each entry next to espeak's own reading.

Before anything goes up, `publish` checks the encoded audio: a speech-recognition round trip against the Script, the longest silence, loudness, true peak and format. It needs the ASR extra, `pip install -e ".[asr]"`.

On GitHub, run the publish-episode workflow with a Bundle id (or the Bundle ids of every Part of a topic, space-separated, which go up together or not at all): with `dry_run` you get the `.m4a` and its ASR report as a workflow artifact; without it the Episode goes up as a Release, is added to `episodes.yaml` (the Episode registry), and the deploy-site workflow rebuilds the Pages site from the registry, `config/show.yaml` and the Releases. The site holds only the newest Episodes plus pinned ones (`pinned.txt`), within the budget in `config/site.yaml`; the Archive page links every Episode's Release. To re-render published Episodes by hand, run publish-episode with `rerender` and their Episode ids: each goes up as `-v2.m4a` (then `-v3`) in its own Release under the same guid, and the older files stay. Run deploy-site by hand to redeploy. If any audio can't be fetched or a check fails, nothing is deployed and the last good site stays up.

The Skill pushes each Bundle on a `claude/` branch and opens a PR. The auto-merge workflow lints it and squash-merges it if it only touches Bundles, Learnings, the pin list, the Listener profile, the backlog, the lexicon or the phrase list (the Template tunables and the voice roster too, on a commit with an `Owner-instructed: "..."` line quoting the owner). It then starts publish-episode for a new Bundle (one run for all the Parts of a topic), publish-episode in re-render mode when a published Bundle's `revision` rises, or deploy-site for a pin-list change or a published Bundle's show notes or `meta.yaml` changing alone. A published Script edited without a revision bump stays open for the owner. Anything else stays open, labelled `needs-owner`, with a comment saying why.

A failed run of any of these workflows opens one issue labelled `pipeline-failure`, naming the stage, the Bundle and the last log lines. A run that succeeds says nothing.
