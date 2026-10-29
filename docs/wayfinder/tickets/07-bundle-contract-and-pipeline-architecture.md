---
title: Bundle contract and pipeline architecture
type: grilling
status: closed
blocked-by: [05-episode-template-and-style-guide, 08-audio-storage-and-retention, 10-agent-learnings-repository, 18-human-feel-and-ai-deslop]
claimed-by: owner (session 2026-10-29)
---
## Resolution

Closed 2026-10-29 after three grilling rounds with the owner (answers in the Grilling log below). Not blocked by ticket 14 (owner: no).

- **Bundle (folder per Episode):** `bundles/<date>-<slug>/` holding `script.md` (research/05 6.3 markup, unchanged: `##` headings, blank lines, `[beat]`, `[think]`, `{cN}` tags; no emphasis or mood tags), `meta.yaml` (title, summary, variant, `part: {n, of, series_slug}`, voice, risk_flag/risk_reason, pronunciations, wpm_budget, target/spoken words, style_guide_version, deslop_version, parent_episode), `show_notes.md` (written form), `ledger.md` (one line per claim: id, claim, source, tier, read-depth, tags) and `lint_report.yaml`. Segments are derived from headings.
- **Identity:** the Bundle id (`<date>-<slug>`) is fixed by the Skill and seeds the render. The Pipeline gives the Episode number and Episode id (`ep-007-<slug>`, Parts `4a/4b`) at publish time, in publish order, and records it in the Episode registry (`episodes.yaml`), which only the Pipeline writes.
- **Session to repo:** the Skill rebases on `main` and pushes a `claude/<slug>` branch. An auto-merge Action runs `pipeline lint` and squash-merges only if every changed path is under `bundles/`, `learnings/` or `pinned.txt` and no firm rule fails; otherwise the PR stays open labelled `needs-owner`. Ruleset on `main`: PR only, no force push, owner bypass.
- **Workflows:** auto-merge → **publish-episode** (lint, render, encode 64 kbps mono AAC, Release upload, byte check, registry commit) → **deploy-site** (feed, plain archive page, window from Releases, 900 MB firm ceiling, Pages deploy). Chained by explicit dispatch, because commits made with `GITHUB_TOKEN` don't trigger workflows. One concurrency group for publishing. Manual dispatch covers retries, re-renders and redeploys.
- **Render:** the job installs only the engine the voice needs (`config/voices.yaml`: engine, base speed or stretch, seed, empty `suits:` for ticket 12); models cached with `actions/cache`; one `synthesise(text, voice)` seam. Chunks pack sentences up to ~300 characters (soft) and never cross a paragraph, `[beat]`, `[think]` or heading. The model owns gaps inside a chunk; the Pipeline owns gaps between chunks with research/18 5.4 distributions, ±0.025 speed jitter and trim on, all in `config/pacing.yaml`. Lexicon applied before TTS (format: ticket 14).
- **Parts:** one Bundle per Part, pushed together, published as a group with one number and letters, one registry commit, all or nothing.
- **Re-render:** manual publish-episode with an Episode id writes `-v2.m4a` into the same Release; the registry and enclosure move to it; guid unchanged; old file kept. When to do it is ticket 16.
- **Bring back:** the Skill adds the Episode id to `pinned.txt` on a `claude/` branch, or the owner edits it in the GitHub app. Redeploy only.
- **Show text:** Release text and feed description are generated from `show_notes.md`; CC BY voice credits are appended from `voices.yaml`.
- **Lint:** Python package `pipeline`, ruff. The same `lint` runs in the session before push, on the branch before merge, before TTS and before publish. Blocks only on firm rules, warns otherwise. Reads the last ten Bundles for shared six-word runs (warn only).
- **Failure and noise:** a failed stage opens a GitHub issue assigned to the owner (stage, Bundle, last log lines); Pages keeps the last good site. Success is silent. Style warnings reach the owner only in the session's final message and `lint_report.yaml`. Only network steps retry, at most twice with a short wait. *(Amended by ticket 15 sign-off, 2026-10-29: on an ASR gate fail, the named chunk is re-rendered once before the issue opens.)* Timeouts (owner wanted shorter than 90 min): render job ~45 min, deploy ~15 min, re-set to about twice the measured render time after the first runs.
- **Session final message:** Bundle path and branch, kept lint warnings with reasons, anything left out and why, "Learned this run", proposed lexicon or phrase-list additions, an ETA. No episode number.
- **Fallback:** `anthropics/claude-code-action` on owner issues labelled `episode` or mentioning `@claude`; same branch flow.
- **Repo (name `podcast`, owner may rename):**
  ```
  CLAUDE.md               Agent skills block, repo rules (glossary names, research/18 section 7 build rules)
  GLOSSARY.md
  docs/agents/            issue-tracker.md, domain.md (/setup-matt-pocock-skills; tracker = GitHub Issues)
  docs/adr/               created lazily
  docs/wayfinder/         this map, tickets, research (no prototypes)
  .claude/skills/episode/ SKILL.md + references
  learnings/              INDEX.md, general.md, fields/<field>.md
  bundles/<date>-<slug>/
  config/                 pacing.yaml, voices.yaml, deslop_rules.yaml, show.yaml (ticket 12), lexicon (ticket 14)
  pipeline/               lint.py render.py publish.py site.py (entry points), lib/, tests/
  episodes.yaml, pinned.txt
  .github/workflows/      auto-merge, publish-episode, deploy-site, claude
  README.md
  ```
  import-linter keeps `lib/` private; `pre-commit` runs ruff. Issue labels keep `episode`, `pipeline-failure`, `needs-owner` and wayfinder/triage tickets apart; build tickets never contain `@claude`.

Handed on:
- **11:** Q&A episodes are ordinary Bundles with `parent_episode` set; same branch and publish flow.
- **12:** `config/show.yaml` (channel metadata, artwork path), `suits:` in `voices.yaml`, credit wording.
- **14:** lexicon file under `config/`, the `pronunciations` field, the pre-TTS apply step; Kokoro phonemes and Pocket respellings.
- **15:** which checks fill the lint and pre-publish slots; timeouts set from measured render time; real-device and minute-15 listens.
- **16:** how the owner asks for a re-render or correction; the `-v2` mechanics are fixed here.


## Question

What exactly does the skill hand the tool (bundle format, script markup for pacing, metadata, sources), and how does the pipeline run end to end (how the session pushes a bundle, what triggers Actions, TTS step, audio post-processing, feed update, failure handling, repo layout)?

## Notes

- 2026-10-29: 09 closed (voice roster, pacing, two engines; see its Resolution). Now blocked by new ticket 19 (expressive delivery), which may change the main engine.
- 2026-10-29: blocked by 18 (owner, during ticket 08). The script markup and bundle contract must carry the de-slop findings. Storage decisions to build on are in ticket 08's Resolution.
- 2026-10-29: ticket 13 closed. The session runs as a Claude Code cloud session and pushes through the Claude GitHub App proxy, so it needs no token. The Skill, its references and Learnings must be committed in this repo. Ticket 07 still decides between pushing to `main` and a `claude/` branch with auto-merge, and specifies the fallback Action workflow (research/13 section 8).
- 2026-10-29: ticket 10 closed. The repo needs `learnings/` (INDEX.md, general.md, fields/<field>.md); session output carries a "Learned this run" block; Learnings lines are append-only, and on a push conflict the skill rebases and re-appends (compaction skipped). See its Resolution.
- 2026-10-29: ticket 11 closed. Q&A is a mode of the same Skill in the same Feed. Adds `config/listener_profile.md` (auto-appended observations in the Bundle commit, so it joins the auto-merge allow-list), `questions` in `meta.yaml`, and `{p:cN}` ledger tags that lint resolves against the parent's ledger.

## Grilling log (session 2026-10-29)

Round 1, owner answers (all recommendations accepted unless noted):
1. Not blocked by ticket 14: 07 reserves the `pronunciations` field, a lexicon file slot and a pre-TTS apply step; 14 owns the entry format.
2. Session pushes a `claude/<slug>` branch; an Action auto-merges only if every changed path is under `bundles/`, `learnings/` or `pinned.txt`; anything else waits for owner review. Session rebases on `main` before pushing.
3. Pipeline assigns the episode number at publish time; Bundle folders are `bundles/<date>-<slug>/`; an Episode registry (`episodes.yaml`) holds number, slug, release tag, guid, voice, bytes, duration.
4. Bundle is a folder: `script.md`, `meta.yaml`, `show_notes.md`, `ledger.md`, `lint_report.yaml`. Segment list is derived from headings, not stored.
5. Two workflows: publish-episode (lint, render, encode, Release upload, byte check, registry commit) and deploy-site (feed, archive page, window, Pages deploy, 900 MB firm ceiling).
6. Render job installs only the engine the voice needs (`config/voices.yaml`); models cached; one `synthesise(text, voice)` seam.
7. Any failed stage opens a GitHub issue assigned to the owner (stage, Bundle, last log lines); success is silent.
8. Chunks of sentences up to ~300 chars (soft), never crossing paragraph, `[beat]`, `[think]` or heading; model owns gaps inside a chunk, Pipeline owns gaps between chunks (research/18 5.4 distributions, ±0.025 jitter, seeded by Bundle id, trim on); values in `config/pacing.yaml`; markup unchanged from research/05 6.3.
9. No topic-to-voice map in v1; `voices.yaml` roster with empty `suits:` for ticket 12; Skill proposes, default `bm_george`.
10. Python + ruff; one `pipeline` package whose `lint` runs in the session and in the Pipeline; blocks only on firm rules.
11. Layout accepted; owner asked to align it with the Matt Pocock skills' repo conventions (checked, see round 2).
12. Fallback: `anthropics/claude-code-action` on owner issues/comments, same branch flow.
13. Final session message: Bundle path and branch, kept lint warnings, what was left out, Learned this run, lexicon/phrase proposals, ETA. No episode number.

Round 2, owner answers (all recommendations accepted):
1. Build tracker is GitHub Issues (Matt Pocock setup); labels keep `episode` summons, `pipeline-failure` and wayfinder/triage tickets apart; build tickets never contain `@claude`.
2. Layout adds `CLAUDE.md` (Agent skills block, build rules), root `GLOSSARY.md`, `docs/agents/`, lazy `docs/adr/`, `docs/wayfinder/` (planning history, no prototypes); `pipeline/` has entry points `lint.py render.py publish.py site.py`, private `lib/`, `tests/`; import-linter enforces entry points; `pre-commit` with ruff (not Husky).
3. GITHUB_TOKEN merges/commits don't trigger workflows, so auto-merge → publish-episode → deploy-site chain by explicit dispatch; one concurrency group for publishing.
4. Ruleset on `main`: PR only, no force push, owner bypass. Auto-merge runs `pipeline lint` on the branch first; on a disallowed path or firm failure it leaves the PR open labelled `needs-owner`. Squash merge.
5. Parts: one Bundle each with `part: {n, of, series_slug}`, pushed together, published as a group (`4a`, `4b`), one registry commit, all or nothing.
6. Re-render: manual publish-episode with an Episode id renders `-v2.m4a` into the same Release; registry and enclosure move; guid unchanged; old file kept. When is ticket 16.
7. Bring back: Skill edits `pinned.txt` on a `claude/` branch or owner edits it in the GitHub app; redeploy only.
8. Release text and feed description generated from `show_notes.md`; CC BY voice credits appended from `voices.yaml`.
9. Lint reads the last ten Bundles for shared six-word runs; warn only.
10. Lint warnings: session final message and `lint_report.yaml`; Pipeline style warnings only in run log; firm failures open an issue.

Round 3, owner answers: timeouts shorter than proposed (render ~45 min, deploy ~15 min); network-only retries, at most two.
- 2026-10-29: ticket 12 closed. `config/show.yaml` contents, cover SVG with render script and font licence, `robots.txt`, `noindex` archive page, block tags and the voice credit line are set in its Resolution. Q&A Episode ids are `ep-007q-<slug>`, so the registry `number` field is text.
- 2026-10-29: ticket 16 closed. Add `revision` and a `corrections:` list to `meta.yaml`. Auto-merge dispatches publish-episode in re-render mode when a published Bundle's `revision` rises, and deploy-site when only `show_notes.md` changed (manual dispatch stays as fallback). Allow-list adds the pronunciation lexicon and the phrase list, plus template tunables and `config/voices.yaml` only for feedback-mode commits marked `owner-instructed` that quote the owner. See its Resolution.
- 2026-10-29: ticket 14 closed. Lexicon is `config/lexicon.yaml` (`verified:` capitals list, `entries:` of `{term, kokoro, pocket, by, note}`); `pronunciations` in `meta.yaml` takes the same entry shape and wins for that Episode. The pre-TTS step works per chunk: Kokoro gets phonemes spliced in through a stand-in word and `is_phonemes=True`, Pocket a text swap. `pipeline lint` adds the firm spoken-form checks in its Resolution. Port `prototypes/pronunciation/pron.py` into `pipeline/lib/`.

## From the final sign-off session (2026-10-29)

- Repo layout gains `config/backlog.md`: the topic backlog (map decision). Owner-added only; a Skill commit that only adds a backlog line auto-merges like `learnings/`.
- ASR fail: one re-render of the named chunk before the issue (ticket 15 sign-off).
