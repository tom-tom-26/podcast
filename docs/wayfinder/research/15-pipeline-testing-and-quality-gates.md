# Research 15: Pipeline testing and audio quality gates

Ticket 15. Probe in `prototypes/quality_gates/`: `gates.py` breaks the ticket 09 `bm_george` take (125 s, 345 words) four ways and measures each check; numbers in `results.json`. Tags as in research/18: [M] measured here, [A] primary source read, [R] my recommendation.

## Bottom line

- **The ASR round trip works, but not as a word error rate.** Overall WER barely moved when audio broke: 1.4% clean against 4-8% with a dropped chunk, a garbled chunk or a cut ending [M]. On a 3,300-word Episode one lost sentence would vanish into the average. What separates them is the **longest run of Script words missing from the transcript**: 1-3 clean, 8-24 broken, in every model [M]. That is the gate.
- **`tiny.en` and `base.en` catch everything `small.en` catches**, at a quarter to a third of the time. With 4 threads (a free public-repo runner has 4 vCPUs [A]), `base.en` ran at RTF 0.04-0.06 on the desktop [M]. Assume 2-3x slower on a runner: about 3-5 minutes for a 25-minute Episode, against 10-25 minutes of render. Unmeasured on a runner.
- **ASR can't hear dead air.** Six seconds of silence left the transcript unchanged [M]. A separate longest-silence check catches it: 0.93 s clean, 5.99 s broken [M].
- **Duration against word count is weak.** A dropped 4 s chunk moved pace from 167 to 172 wpm [M]. Keep it as a warning only.
- **Kokoro's raw output is quiet and peaky:** -21.9 LUFS, true peak -4.2 dBTP [M]. Plain gain to -16 LUFS puts the true peak at +1.7 dBTP [M], so normalising needs a true-peak limiter. ffmpeg `loudnorm` falls back from linear to dynamic mode (its limiter) whenever the gain would break the peak ceiling [A, search summary of ffmpeg docs and ffmpeg-user list]. That fallback is expected here and fine for speech.
- **Kokoro and Pocket render at 24 kHz** [M]. Apple asks for 44.1-48 kHz (research/04 constraint 5). Resample to 44.1 kHz before AAC, and check the sample rate after encoding.
- **Apple has no standalone feed validator.** Apple validates only inside Podcasts Connect submission and points to Cast Feed Validator and Podbase [A, Apple support 829]. A followed-by-URL feed is never submitted, so CI checks the feed itself and a third-party validator is a one-off manual check.

## Measurements [M]

faster-whisper 1.2.1, int8, CPU, `cpu_threads=4`, `beam_size=1`, no VAD; desktop (16 logical cores, limited to 4 threads). The faults are applied at the middle of the take.

| Copy | WER tiny / base / small | Longest missing run (all models) | Missing at end | Longest silence | wpm |
|---|---|---|---|---|---|
| clean | 1.4 / 1.1 / 1.4% | 1 / 1 / 3 | 0 | 0.93 s | 167 |
| 4 s dropped | 5.2 / 4.9 / 6.9% | 12 | 0 | 0.93 s | 172 |
| 3 s garbled (reversed audio) | 4.3 / 5.2 / 5.2% | 8 | 0 | 0.93 s | 167 |
| last 8 s cut | 8.3 / 8.0 / 8.3% | 24 | 24 | 0.93 s | 178 |
| 6 s dead air | 2.0 / 2.3 / 0.6% | 1 / 1 / 2 | 0 | 5.99 s | 159 |

RTF: tiny.en 0.02-0.04, base.en 0.04-0.06, small.en 0.14-0.17. Loudness was the same for every copy: -21.9 LUFS, -4.2 dBTP raw, +1.7 dBTP after plain gain.

Limits of the probe: one 2-minute clip, one voice, faults placed by hand. The clean run of 3 under `small.en` came from a name-like phrase. A 25-minute Episode with more names will have longer clean runs, so the threshold below has margin and should be re-set after the first real Episodes.

## Proposed gates [R]

Ticket 07 fixes where checks run (lint in four places, a pre-publish slot) and that only firm rules block. Under the leniency rule, every threshold below is a soft target until the owner signs off, and "fail" means "proposed firm".

### Before TTS (`pipeline lint`, already decided in 07 and 14)

- Firm: ticket 14's spoken-form checks (digits, symbols, URLs, abbreviations, fillers, unverified capitals); research/05 item 11 (every claim tag resolves to a ledger line and a source); Bundle schema (required `meta.yaml` fields, a valid voice in `voices.yaml`, Part info consistent).
- Warn: the other (M) items in research/05 section 8 (word count, structure, sentence length, phrase list).
- Must accept the dated show-notes correction line and the spoken correction line (ticket 16).

### After render, before upload (new step in publish-episode)

Run on the **encoded `.m4a`, decoded again**, so encoding faults are caught too.

| Check | Pass | Proposed fail |
|---|---|---|
| ASR round trip (`base.en`), Script and transcript both normalised (lower case, numbers as words, hyphens split) and aligned with `difflib` | longest missing run under 6 words, nothing missing at the end | 6+ missing words in a row (about 2 s of speech), or 4+ missing at the end. The issue names the chunk and its text |
| Longest silence under -50 dBFS | under ~2 s | over 3 s |
| Integrated loudness (ffmpeg `ebur128`) | -16 ±1 LUFS | outside -16 ±2 |
| True peak | at most -1.0 dBTP | above -0.5 dBTP |
| Format (`ffprobe`) | AAC, mono, 44.1 kHz, ~64 kbps | wrong codec, channel count or sample rate |
| Pace (words / duration) | 165 wpm ±25% | warn only |

Loudness chain: two-pass `loudnorm=I=-16:TP=-1.5:LRA=11`, accepting the dynamic fallback, then resample to 44.1 kHz and encode. Aim at -1.5 to leave room for AAC overshoot, and gate on the encoded file. Sound Check metadata (research/04) is optional: Apple's players measure loudness themselves.

ASR on a failed gate: no automatic re-render, in line with 07 (only network steps retry). The run opens a `pipeline-failure` issue with the gate, the numbers and the chunk. Owner question 2 below.

ASR also feeds the lexicon (ticket 14). For each capitals word or lexicon term in the Script, record whether the transcript matched, in `asr_report.yaml`, uploaded as a Release asset (not in git, success stays silent). The Skill reads the last few reports and proposes `verified:` additions for Pocket. A match is weak evidence (research/14), so a proposal, never an automatic entry.

### Upload and deploy (from 08 and 12)

- Release asset byte size equals the local file before the registry or feed is touched (firm, 08).
- Every file in the window can be fetched, and the site stays under the ~900 MB ceiling (firm, 08).
- Feed check in Python, before deploy: well-formed XML; research/04 constraints 1-4 (namespaces, required channel tags, unique and unchanged guids, ASCII URLs); each enclosure `length` equals its byte size; `itunes:duration` from `ffprobe`; cover 3000x3000, square, RGB, no alpha (12). Firm: an invalid feed can stop the app from updating.
- After deploy, wait ~10 minutes for the edge cache (research/04 constraint 9), then check the feed URL returns 200 and contains the new guid, and the new enclosure answers `HEAD` 200 with the right `Content-Length` and `Range: bytes=0-1` with 206 (research/04 constraint 6). A failure here opens an issue; the site is already live.
- Third-party validator (Cast Feed Validator or Podbase): by hand, once at setup and after any change to the feed template. Not in CI.

## Testing without publishing [R]

- **Unit tests** in `pipeline/tests/` (pytest), run on every PR that touches `pipeline/`, `config/` or workflows: lint rules on fixture Bundles (good and bad); chunker boundaries; the ASR alignment gate on synthetic transcripts (drop, garble, cut end, as in the probe); a feed golden file; registry numbering for Parts and Q&A letters.
- **Smoke Bundle**: a ~1-minute Quick Bundle in `pipeline/tests/fixtures/`, rendered end to end in **dry-run** mode on PRs that touch render or encode code, and by manual dispatch.
- **Dry run** (`dry_run: true` input on publish-episode): lint, render, encode, every audio gate; audio and reports go up as a workflow artifact; no Release, no registry commit, no dispatch to deploy. The first real Episode goes through it first, and the measured render time sets the timeouts (07: about twice the measured time).
- **Test feed**: deploy-site can write `test/feed.xml` with its own guids, title prefix "TEST", `itunes:block`. The same Pages site, so it costs nothing. Used for the real-device checks below, never followed for listening.

## Real-device acceptance (one-off, owner, on the iPhone)

Collected from tickets 04, 07, 08, 12, 14 and 16 and research/03:

1. Follow the test feed by URL with `itunes:block` and `podcast:block` set; it follows (12).
2. Download an Episode, switch to flight mode, play, seek (04).
3. Throwaway item whose enclosure is a GitHub Release URL (302 to a signed URL, `application/octet-stream`): plays, seeks, downloads offline. A pass turns on 08's repoint rule.
4. `Episode N: Title`, `Episode 4a: ...` and `Episode 7q: ...` display and sort sensibly (08, 12).
5. Re-render a not-yet-downloaded item (same guid, `-v2` enclosure) and time how long the new audio takes to arrive; edit an item description and see whether the app shows it (16).
6. Listen to one full-length render past minute 15 for drift or degradation (research/03 item 10, 07).
7. Listen to the names flagged in ticket 14 (cases 16, 19, 20).

## Owner questions

**Answered 2026-10-29:** (1) yes, all six fails are firm; (2) yes, re-render the named chunk once (Pocket new seed, Kokoro new speed draw) before opening an issue, which amends ticket 07's retry rule; (3) `base.en`.

1. Make the six proposed fails firm (ASR missing run, missing end, silence, loudness, true peak, format)? They protect the TTS output, so they fit the leniency rule's exception, but the rule says to ask.
2. On an ASR fail, re-render the named chunk once (Pocket with a new seed, Kokoro with a new speed draw) before opening an issue? It saves a manual re-run, but 07 said only network steps retry.
3. ASR model: `base.en` (recommended) or `tiny.en` (half the time, caught the same faults here)?

## Sources

- [GitHub-hosted runners reference](https://docs.github.com/en/actions/reference/runners/github-hosted-runners): public repos get 4 CPU / 16 GB / 14 GB SSD Linux runners; private 2 / 8 / 14. Read 2026-10-29.
- [Apple: Validate your podcast RSS feed](https://podcasters.apple.com/support/829-validate-your-podcast): validation is part of submission; recommends Cast Feed Validator and Podbase. Read 2026-10-29.
- ffmpeg `loudnorm`: linear mode falls back to dynamic when the target LRA is below the source's or the gain would exceed the true-peak ceiling; dynamic mode upsamples to 192 kHz for true-peak detection. From a search summary of [ffmpeg-user, March 2022](https://ffmpeg.org/pipermail/ffmpeg-user/2022-March/054425.html), the [loudnorm docs (7.0)](https://ayosec.github.io/ffmpeg-filters-docs/7.0/Filters/Audio/loudnorm.html) and [ffmpeg-normalize options](https://slhck.info/ffmpeg-normalize/usage/normalization-options/); check the warning on real files.
- research/04 constraints 5, 6, 9 and 10; research/03 Amendments 10-11; research/05 section 8; research/14 Measurements; tickets 07, 08, 12, 16.
