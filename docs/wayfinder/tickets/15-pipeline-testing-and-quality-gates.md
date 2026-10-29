---
title: Pipeline testing and audio quality gates
type: research
status: closed
blocked-by: []
claimed-by: owner (this session)
---

## Resolution

Closed 2026-10-29 after a probe on the ticket 09 `bm_george` take with four deliberate faults (`prototypes/quality_gates/`, findings in `research/15-pipeline-testing-and-quality-gates.md`). Thresholds are soft until the owner answers the three questions in research/15.

- **ASR round trip gates on the longest run of missing Script words, not WER.** WER went from 1.4% clean to only 4-8% broken; the longest missing run went from 1-3 to 8-24 in every model. Proposed fail: 6+ missing words in a row, or 4+ missing at the end. The issue names the chunk.
- **Model `base.en`** (int8, CPU, 4 threads): RTF 0.04-0.06 on the desktop, about 3-5 min per Episode on a runner (assumed, unmeasured). `tiny.en` caught the same faults.
- **Separate silence check** (ASR can't hear dead air): fail over ~3 s. Pace against word count is a warning only.
- **Loudness:** raw Kokoro is -21.9 LUFS, -4.2 dBTP, and plain gain overshoots to +1.7 dBTP, so two-pass `loudnorm` I=-16, TP=-1.5 with its limiter, resample 24 to 44.1 kHz, encode, then gate the encoded file (-16 ±2 LUFS, true peak at most -0.5 dBTP to fail; ±1 and -1.0 to pass cleanly).
- **All audio gates run on the decoded `.m4a`** after encoding, before the Release upload. Format check by `ffprobe`.
- **Feed checks in Python before deploy** (research/04 constraints 1-4, enclosure lengths, duration, artwork), a post-deploy HEAD/range/guid smoke check after the cache window, and a third-party validator by hand only. Apple has no standalone validator.
- **Testing without publishing:** pytest unit tests (including synthetic ASR faults), a ~1-minute smoke Bundle, a `dry_run` input on publish-episode (artifact only, no Release, registry or deploy), and a `test/feed.xml` on the same Pages site.
- **Real-device acceptance:** one checklist of seven items gathered from 04, 07, 08, 12, 14, 16 and research/03 (research/15).
- **Lexicon feed:** `asr_report.yaml` as a Release asset records which capitals words and lexicon terms transcribed right; the Skill proposes Pocket `verified:` additions from it, never adds them itself.

Handed on:
- **Spec / implementation:** gate step in publish-episode, `pipeline/tests/`, smoke fixture, `dry_run` input, `test/feed.xml` target in deploy-site; faster-whisper and the `base.en` model cached with `actions/cache`.
- **Ticket 07's layout:** `asr_report.yaml` joins the Release assets; timeouts re-set from the dry-run render time.
- **Owner:** questions 1-3 in research/15, and the real-device checklist.

## Question

What must pass before an Episode is published, and what happens when a check fails? Candidates: the script lint (research/05 checklist (M) items), Bundle schema validation, a speech-to-text round trip on CPU compared with the Script to catch garbled or truncated chunks (which engine, what error threshold, how long it adds to a run), duration against word count, loudness (-16 LKFS, true peak at or below -1 dBFS), enclosure byte length, Feed validation against Apple's rules, a HEAD and range check on the live enclosure URL, and the one-off real-device acceptance test (follow, download, offline play on the owner's iPhone). Also: how the Pipeline is tested without publishing (dry-run mode, a test feed).

Context: research/03 Amendments 10-11, research/04 constraints 6 and 10, research/05 section 8. Covers the map's "testing strategy for the pipeline and audio quality gates" item. Proposed by the Opus review, 2026-10-29.

## Notes

- From ticket 08 (2026-10-29), add to the real-device test: a throwaway feed whose enclosure is a GitHub Release URL (302 to signed URL, `application/octet-stream`). Check that it plays, seeks and downloads offline; a pass turns on 08's repoint rule. Also check how `Episode N: Title` and `Episode 4a: ...` display in Apple Podcasts.
- Storage gates from 08: verify the Release file's byte size before touching the feed; fail the deploy if any file in the window can't be fetched; refuse a deploy over the ~900 MB site ceiling.
- 2026-10-29: ticket 07 closed. Lint runs in four places (session, branch before merge, before TTS, before publish) and blocks only on firm rules. Job timeouts start at ~45 min render and ~15 min deploy (owner wanted them short); re-set them to about twice the measured render time. Network steps retry at most twice.
- 2026-10-29: ticket 12 closed. Add to the gates: cover artwork is 3000x3000, square, RGB with no alpha. Add to the real-device check: the Feed with `itunes:block` and `podcast:block` still follows by URL and passes validation.
- 2026-10-29: ticket 16 closed. Add to the real-device check: (1) re-render a not-yet-downloaded Episode (same guid, `-v2` enclosure) and time how long the new audio takes to arrive; (2) edit an item description and see whether the app shows the change. Lint must accept the dated show-notes correction line and the spoken correction line for Harmful corrections.

## From ticket 14 (2026-10-29)

- The ASR round trip is the only net for names and unusual words the lint can't see. Use it to grow the lexicon's `verified:` list on Pocket: so far only ATP, REM and CYP1A2 have been checked in a Pocket render; the rest are checked in espeak only.
- Whisper writes numbers as digits and guesses spellings from context, so compare after normalising both sides, and treat a name that transcribes right as weak evidence (research/14, Measurements).
- `pipeline lint` carries ticket 14's firm spoken-form checks; heteronyms warn only.

## Owner sign-off (2026-10-29)

- The six audio and format fails are firm: ASR missing run of 6+ words, 4+ missing at the end, silence over 3 s, loudness outside -16 ±2 LUFS, true peak above -0.5 dBTP, wrong format.
- On an ASR fail the Pipeline re-renders the named chunk once (Pocket with a new seed, Kokoro with a new speed draw) and re-runs the gates; a second fail opens the `pipeline-failure` issue. This amends ticket 07's "only network steps retry".
- ASR model: `base.en`.
