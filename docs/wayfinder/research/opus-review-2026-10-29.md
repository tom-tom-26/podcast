# Opus review, 2026-10-29: index of changes

Reviewer: opus-agent. Scope: tickets and research 01, 02, 03, 04, 06, the voice audition prototype (ticket 09), map.md and GLOSSARY.md, plus drafting ticket 05. Each amended file has its own dated "Amendments (Opus review, 2026-10-29)" section with the reasons; this file is the index.

Method: primary sources fetched where possible (PMC full text, a Bradbury full-text PDF, Gardiner et al. full text, Kokoro VOICES.md, the Pocket TTS model card, AWS Polly pricing, Apple 823 and 825, GitHub runner docs, Crossref for DOIs). I read the installed `kokoro-onnx` 0.6.1 source and ran its espeak-ng phonemizer on test strings, measured pace and pauses in the six prototype WAVs, and curl-tested a GitHub Release asset. Throwaway scripts lived in the session scratchpad; nothing was built in the project.

## Findings ranked by importance

1. **Pronunciation override doesn't exist in the chosen runtime** (research/03, ticket 03). `[word](/phonemes/)` is a misaki feature of hexgrad's `kokoro`, not of `kokoro-onnx`. Fixing technical terms needs a lexicon or a phoneme-substitution step. Factual error, corrected. Drives proposed ticket 14.
2. **espeak-ng text normalisation breaks common health-script forms** (new finding). Units, decimals, ranges, times, abbreviations and several acronyms come out wrong; the decimal point even becomes a sentence break. The only defence is writing in spoken form plus a lint and a lexicon (research/05 section 6; tickets 14, 15).
3. **Word budgets were based on an unmeasured 150 wpm.** Measured Kokoro output is 159-190 wpm (median ~172), so 20 minutes is ~3,300 words. Affects ticket 05 budgets, Polly cost and render-time estimates.
4. **Recall-prompt evidence was overstated and partly misreported** (research/01). Jing 2016 was positive, not mixed; the larger Welhaf 2022 replication (N = 195) found no learning benefit; Szpunar's "tests" were typed quizzes. The recommendation survives as cheap and plausible, redesigned as true retrieval.
5. **The ticket 01 decision's segment arithmetic doesn't fit 20 minutes.** 4-5 segments of 4-6 min is 16-30 min of content alone. Resolved in the 05 draft; map wording should follow.
6. **Ticket 06 lacks a read-depth rule**, which is the exact failure behind items 1 and 4 and the citation errors below. Recommendation for owner.
7. **Voice audition is incomplete and too easy.** No Pocket TTS or Polly render. The script has no numbers, acronyms or terms. The lowest-graded voice was auditioned and better-graded male voices were not. Pause settings are stacked on engine defaults.
8. **Citation errors in research/02.** Mayer's d ≈ 1.3 is the 2005 figure (2014: d = 0.79); the "modern TTS closes the gap" link went to an unrelated paper (the right ones, Craig & Schroeder 2017/2019, support TTS). Corrected.
9. **Polly free tier changed** for AWS accounts created after 15 July 2025 (credits and a 6-month plan instead of 12 months free). Corrected.
10. **Gaps no ticket owned:** cover artwork and show metadata (Apple requires them), where the skill runs and what it costs on the Claude side, corrections to published episodes. Proposed tickets 12, 13 and 16.
11. **Contradictions between files:** research/02 rule 5 (standing disclaimer) vs ticket 06 (none), resolved in favour of 06; Piper rejected for GPL-3.0 while the Kokoro stack depends on GPL-3.0 espeak-ng and phonemizer; research/02 rule 4 (recap every 5-7 min) vs research/01 (prompt after each segment), harmonised in 05.
12. **Smaller additions:** Release assets redirect to signed URLs but support HEAD and range (input for 08); Git LFS can't serve Pages; obscurity leaks via indexing and repo history; Kokoro voice grades; Pocket TTS is CC-BY-4.0 and gated; kokoro-onnx 0.6.1 has built-in punctuation pauses and a `continuous` mode.

## Recommended decision changes needing owner sign-off

**All signed off by the owner on 2026-10-29 and applied** (tickets 06, 01 and 03 carry an "Owner sign-off" section; ticket 07's blocked-by change was made when 07 was worked).

- **Ticket 06:** add a read-depth field to ledger lines and the rule that spoken numbers need full text or an abstract that states them; spot-check the two or three load-bearing numbers against the source; record n and population; add a "textbook consensus" marker for mechanisms; add checks for source age, retractions, conflicts of interest, and absolute risk.
- **Ticket 01 / map decision line:** reword "4-5 segments of ~4-6 min" to "4 content segments of ~3.5 min plus a protocol segment (5 in total)" once 05 is signed off.
- **Ticket 03:** base Piper's rejection on quality, not licence (the decision itself doesn't change).
- **Ticket 07:** add 13 (runtime) and 14 (pronunciation) to `blocked-by`.

## Change log

| File | Change |
|---|---|
| `research/05-episode-template-and-style-guide.md` | **New.** Full ticket 05 proposal. |
| `tickets/05-episode-template-and-style-guide.md` | `claimed-by: opus-agent`; added "Resolution (proposed, awaiting owner)". Status left open. |
| `map.md` | Notes: one line saying the 05 draft awaits review. "Not yet specified": one line listing the new gaps and proposed tickets 12-16. "Decisions so far" untouched. |
| `research/01-episode-length-evidence.md` | Corrected in place: Szpunar design and figures, Jing 2016 (positive), Welhaf 2022 added, Rey 2019 system-paced. Amendments section: 10 items (includes Bradbury verified in full text, segment arithmetic). |
| `tickets/01-episode-length-evidence.md` | Amendments pointer, plus a recommendation to reword the map line. |
| `research/02-host-format-and-engagement.md` | Corrected in place: Mayer edition figures, TTS voice-effect citations (wrong DOI replaced), Kuperman and Mar citations, rule 5 marked superseded. Amendments section: 12 items. |
| `tickets/02-host-format-and-engagement.md` | Amendments pointer. |
| `research/03-open-source-tts-on-github-actions.md` | Corrected in place: phoneme override (table and section 4), Polly free tier, 510-limit confirmation, RTF range. Amendments section: 11 items. |
| `tickets/03-open-source-tts-on-github-actions.md` | Resolution text corrected (inline override) and Amendments added. |
| `research/04-rss-github-pages-apple-podcasts.md` | Amendments section: 7 items (no factual errors found). |
| `tickets/04-rss-github-pages-apple-podcasts.md` | Amendments pointer. |
| `tickets/06-research-and-accuracy-standard.md` | Amendments: 5 recommendations for owner, 4 notes. Decision untouched. |
| `tickets/09-voice-audition.md` | Amendments: prototype state, measurements, 7 issues. Still open. |
| `tickets/12-show-identity-and-feed-metadata.md` | **New**, open, grilling. |
| `tickets/13-skill-runtime-and-summon-surface.md` | **New**, open, research. |
| `tickets/14-pronunciation-and-text-normalisation.md` | **New**, open, prototype, blocked by 09. |
| `tickets/15-pipeline-testing-and-quality-gates.md` | **New**, open, research, blocked by 07. |
| `tickets/16-feedback-and-corrections.md` | **New**, open, grilling, blocked by 07. |
| `GLOSSARY.md` | Not changed. Eight proposed terms are in research/05 section 10 for the owner to accept. |
| `prototypes/voice_audition/` | Not changed. Reviewed in ticket 09's Amendments. |

## Not verified (still open)

- Wiblin 2020 and Wilson & Korn 2007 full texts (both blocked); Mayer 2014 chapter full text; Ginns 2013 moderator tables.
- Apple-domain confirmation of the `audio/x-m4a` string; whether Apple follows Release-asset redirects or accepts `octet-stream`; the effect of `itunes:block` on Follow-by-URL.
- Kokoro render speed on a real Actions runner; a full 20-minute render's stability.
