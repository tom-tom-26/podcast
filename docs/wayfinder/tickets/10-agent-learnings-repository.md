---
title: Agent learnings repository
type: grilling
status: closed
blocked-by: []
claimed-by: owner (this session)
---

## Question

The owner wants a learnings store that agents read and add to: anything that proved really useful for researching a class of topics (good approaches, places to look, sources that were reliable or poor). Decide what belongs in it, how it is organised by generalised topic area, where it lives (in the podcast repo or separate), how the skill reads it cheaply (token cost) and when and how it writes to it, and how stale or wrong entries are kept out. Context: the accuracy standard in `ticket 06` and its claim ledger.

## Input from ticket 05 (2026-10-29)

Learnings must hold **source profiles** per field of topics (research/05 section 13: strongest evidence, watch-outs, higher-risk triggers). The 15 starter profiles seed it. When the skill meets a field with no profile, it drafts one during research and writes it here. Decide how profiles are stored, read cheaply, and kept up to date alongside the other learnings.

## Resolution

Closed 2026-10-29. Decided with the owner:

- **What a learning is (owner's reframe):** a **lesson**, meaning a mistake or difficulty that happened in a run, written down with what to do instead, so it isn't repeated and later runs spend fewer tokens finding out again. **Never facts about a topic**, and never generic advice the model already knows. A smooth run writes nothing; there is no minimum.
- **Entry format:** one line, appended. `date · episode ID · stage: <stage>` **What happened:** ... **Do instead:** ... (always actionable). Optional **Saves:** (e.g. "~4 wasted fetches"), plus `seen: N` and `source: skill|owner`.
  Example: `2026-11-03 · ep-007 · stage: research` What happened: PubMed full-text links timed out three times. Do instead: go straight to the PMC mirror URL. Saves: ~4 fetches. `seen: 1`.
- **Stages covered:** every stage the skill itself runs: research, confirm step, script writing, claim-check and push. Pipeline or Actions failures after the session belong to tickets 15 and 16. Pronunciation rules live in ticket 14's lexicon and AI-tell phrases in `deslop_rules` (research/18). A lesson may say "added X to the lexicon" but never holds the rule itself; additions to those files are proposed in the session output.
- **Location:** the podcast repo (forced by ticket 13: cloud sessions load only the clone), so Learnings are public like the feed.
- **Layout:** `learnings/INDEX.md` (fields and topic keywords), `learnings/general.md` (cross-field lessons), and `learnings/fields/<field>.md`, one per source profile: the profile at the top, then its lessons (field-specific mistakes, outlets found wrong, access difficulties, search dead ends).
- **Read budget (soft, ±25%):** every run reads INDEX (~300 tokens), `general.md` (~1,500) and the 1-2 field files the overlap rule picks (~1,500 each), so about 3-5k tokens in total. A file over its size is compacted in the same run (duplicates merged, dead lessons dropped). Re-tune after research/13's usage pilot.
- **Writing:** auto-write in the same commit as the Bundle. The session output always carries a short **"Learned this run"** block listing every Learnings change, or "nothing new". The owner reverts anything unwanted. Soft cap of about 3 new lessons per run (±25%).
- **Source profiles (firm, owner-approved because it protects accuracy):** the skill may append to "watch for" and to lessons freely, and may *add* a stricter higher-risk trigger on its own. Changing "strongest evidence", or removing or loosening any higher-risk trigger, is only a proposal in the session output that the owner approves.
- **New fields:** the skill drafts a profile during research and saves it with `status: draft`. While it is a draft, its higher-risk triggers are those of the strictest neighbouring profile (beekeeping borrows Health's). It becomes `settled` after a second clean use or the owner's OK.
- **Naming outlets:** allowed only for a concrete observed error, written as a fact ("misstated n in ep-007"), never as a verdict, and never based on reputation or political lean. After about 3 logged errors (soft) in one field, the skill demotes that outlet to context-only for that field.
- **Staleness:** self-correcting. If a lesson the skill follows turns out wrong or unnecessary, it is rewritten or deleted in that run and noted in "Learned this run". `seen` rises each time a lesson helps again. Compaction drops lessons older than about 12 months with `seen: 1` first.
- **Owner feedback (link to 16):** feedback about an avoidable mistake becomes a lesson with `source: owner`. Owner lessons are never removed by self-correction or compaction; only the owner removes them. Taste feedback about defaults (length, pace) goes to the template's tunables, not Learnings. Ticket 16 owns how the feedback is sent.
- **Parallel sessions:** lessons are append-only lines. Compaction is the only rewrite and is skipped if the push meets a conflict. On a conflict the skill rebases and re-appends its own lines. Ticket 07 owns the git mechanics.
- **Q&A episodes (ticket 11):** same rules. They read the parent episode's field file(s) and write lessons there.
- **Seeding on day one:** 15 field files from research/05 section 13 (profile, empty lessons), INDEX with keywords, and `general.md` seeded with real mistakes from this planning work: numbers taken from search summaries proved wrong in tickets 01-03 (Mayer effect-size edition mix-up, a positive study reported as a mixed replication, a misattributed DOI; do instead: speak a number only from a full text or an abstract that states it), and the Trusted network level blocking journals, news sites and PubMed (research/13; do instead: run in the Full-network environment).

Handed on:
- **07:** the `learnings/` layout in the repo, the "Learned this run" block in session output, and the append/rebase rule on push conflicts.
- **16:** owner feedback about mistakes lands in Learnings as `source: owner` lessons; taste feedback goes to the tunables.
- **11:** Q&A episodes read and write the parent's field file(s).
- **14 and research/18:** the skill proposes lexicon and phrase-list additions in its output; it never stores them in Learnings.

## Notes

- 2026-10-29: ticket 11 closed. Owner taste signals drawn from Q&A questions go to `config/listener_profile.md`, never to Learnings.
