---
title: Episode template and style guide
type: grilling
status: closed
blocked-by: []
claimed-by: opus-agent (draft), owner (grilling)
---

## Question

Given the length and host-style evidence, what is the episode skeleton (hook, mechanism, takeaways, recap), default length and the "quick/deep" variants, and the host's voice and tone rules the skill must write to?

## Resolution

Closed 2026-10-29 after grilling with the owner (Q1-Q26). The binding decisions are in `research/05-episode-template-and-style-guide.md` section 12, with source profiles in section 13. They override the draft summary below where they differ. In brief:

- **Any topic with ease** is the tool's defining property: the template is domain-neutral, and evidence standards run through per-field **source profiles**. There are 15 starter profiles from the largest podcast genres, and new fields get a profile on first use, saved to Learnings.
- **Leniency rule:** numeric limits are soft (±25%). Only accuracy, honesty and TTS-safety rules are firm. The owner is asked before any new strict limit is set.
- **Lengths with no minimum and no padding:** Quick 8-15 min, Standard 15-28 (typically ~25), Deep 28-35 (up to ~44 if the topic won't split cleanly). Split above ~35 min into 2-3 standalone subtopic Parts, never cliffhangers.
- **One-round confirm step:** the skill proposes a length and outline (and any drill-down) in one message, and the owner replies "go" or tweaks it.
- **Plain language first:** explain first and name second, an everyday analogy for every hard concept, and a target listener of a bright 15-year-old.
- **Retrieval design:** each segment opens with its main question and re-asks it at the end, with spoken previews, "so what" lines and spaced recall (evidence in research/17).
- **Closing segment:** Protocol, or "Why it matters / what to watch" for topics with nothing to act on. The skill picks tool-led or mechanism-led per topic.
- **Examples:** hypothetical scenarios and real sourced stories are allowed. The host's invented experiences never are.

### Draft summary (2026-10-29, superseded where section 12 differs)

Draft 2026-10-29 by opus-agent. Full proposal in `research/05-episode-template-and-style-guide.md`. Nothing here is decided until the owner signs off; the 13 owner questions with defaults are in section 11 of that file.

- **Pace basis:** word budgets use 165 wpm, taken from the six measured Kokoro renders (159-190 wpm, median ~172), not from the earlier 150 wpm guess. Recalibrated automatically to the chosen voice after two episodes.
- **Variants:** Quick ~11 min / 1,800 words / 3 segments; **Standard ~20 min / 3,300 words / 4 content segments (default)**; Deep ~27 min / 4,400 words / 5 segments. Above 4,700 words or 6 segments, split into 2-3 standalone Parts, published together. Owner picks by adding "quick" or "deep" to the topic; otherwise Standard. The skill may drop to Quick rather than pad, and splits on overflow without asking.
- **Skeleton (Standard):** Hook 130 words (sourced surprise plus promise, no welcome, no caution) → Roadmap 80 (count and frame said aloud) → 4 content segments of ~560 words, each with a numbered signpost, mechanism, one analogy, one example, inline evidence voicing, at most one simulated listener question, and a retrieval-style recall prompt (question, ~3 s `[think]` pause, answer) → Protocol 480 (what, how much, when, adjust, when not; ends with "How sure are we") → Recap 200 in retrieval form → Sign-off 50. This also fixes an arithmetic problem in the 01 decision: "4-5 segments of 4-6 min" can't fit in 20 minutes, so read it as 4 content segments of ~3.5 min plus a protocol segment.
- **Two segment modes:** tool-led (Huberman's mechanism → dose → adjust inside each segment; default for health and training) and mechanism-led (actions gathered in the protocol or "Takeaways" segment).
- **Ticket 06 placement:** each caution sits next to the action it qualifies and is specific; a higher-risk episode adds one caution line in the roadmap (never in the hook) and sets `risk_flag` and a reason for the show notes; no standing disclaimer (overrides research/02 rule 5). Fixed spoken vocabulary maps ledger tiers to words, including size, population and species.
- **Host:** unnamed "well-read friend", calibrated and willing to commit, "I" only for reasoning, never invents experience, numbers, studies or names. All 13 research/02 rules mapped to operational or testable rules, with do/don't pairs and a banned-phrase list.
- **Writing for TTS:** measured against kokoro-onnx's espeak-ng front end. Everything is written in spoken form (no digits, units, symbols, abbreviations, parentheses or dashes), acronyms are expanded or hyphenated and listed in `pronunciations`, sentences average 10-16 words with a maximum of 30, and pauses are named markup (`[beat]`, `[think]`, `##` segment headings, blank lines) whose durations live in pipeline config. Claim tags `{cN}` link sentences to the claim ledger.
- **Checklist:** 23 items, about half mechanical, so ticket 07 can run them as a script lint before TTS.
- **Interfaces flagged, not decided:** Bundle fields for 07; claim tags and two ledger recommendations for 06; a Quick-length answer-first shape for Q&A episodes (11); voice-dependent budget and a harder audition passage (09).
