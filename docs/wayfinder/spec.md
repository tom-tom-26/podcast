---
title: "Spec: Plainly Put, the personal podcast tool"
type: spec
status: open
labels: [ready-for-agent]
source: wayfinder/map.md (signed off 2026-10-29), tickets 01-19, research/
---

# Spec: Plainly Put, the personal podcast tool

Terms follow `GLOSSARY.md`. Where this spec and a closed ticket's Resolution or Owner sign-off disagree, the ticket wins and this spec should be fixed. Numeric limits are soft (about ±25%) unless marked **firm**. Firm rules protect accuracy, honesty, the TTS engine or storage, and the owner approved each one.

## Problem Statement

The owner wants to learn about any general-interest topic (sport, science, news, technology, finance, history and more) by listening on their iPhone, in well-built episodes of about 25 minutes. Nothing does that for them today. Existing podcasts don't cover the exact topic they're curious about this week. Reading takes screen time they would rather spend listening. AI audio tools tend to sound robotic, pad their content, make up facts or hide their sources, and many cost a subscription.

The owner's constraints:
- Cost as little as possible: nothing beyond the Claude plan they already pay for, no paid hosting, no paid TTS and no App Store fee.
- No PC left running.
- Starting an episode should take about a minute of their time, from the phone.
- The result must feel human, real and engaging, with no AI slop, at every layer: the content, the audio, the feed text and the code.
- Claims must be traceable to sources, and the episode must say plainly how strong the evidence is.

## Solution

A private-by-obscurity podcast called *Plainly Put*. The owner follows it by URL in Apple Podcasts. It has two halves joined by a file contract:

1. **The Skill**, an `episode` Claude Code skill. The owner starts a Claude Code cloud session from the Code tab of the Claude iPhone app and names a Topic (or says "next" to take the top line of the Topic backlog). The Skill reads its Learnings and the Listener profile, then sends one confirm message with the Variant, the outline, any drill-down options and the proposed voice. The owner replies "go" or tweaks it in that same reply. The Skill then researches against a source ladder, builds a Claim ledger, writes a Script in spoken form in the host's voice, claim-checks it, lints it, and pushes a Bundle on a `claude/` branch. The same Skill also has a Q&A mode (go deeper on a published Episode) and a Feedback mode (reactions, instructions and Corrections).
2. **The Pipeline**, which runs on free GitHub Actions runners in a public repo. It auto-merges safe Bundle branches, renders the Script with open-source neural TTS (Kokoro `bm_george` by default, with Pocket TTS topic voices), normalises loudness, encodes 64 kbps mono AAC, checks the audio against quality gates, uploads it as a GitHub Release, numbers the Episode, and deploys the Feed and an archive page to GitHub Pages. Success is silent. Any failure opens a GitHub issue assigned to the owner, and the last good site stays live.

Apple Podcasts handles offline download and playback speed.

## User Stories

### Summoning an Episode

1. As the owner, I want to start an Episode from the Code tab of the Claude iPhone app, so that I don't need a PC.
2. As the owner, I want to give only a Topic, so that making an Episode costs me about a minute.
3. As the owner, I want to add an angle or hint to the Topic and have it treated as a hint, not a hard rule, so that I can steer without writing a brief.
4. As the owner, I want the Skill to propose the Variant (Quick, Standard or Deep), the outline and the voice in one message, so that I approve everything in one reply.
5. As the owner, I want a Topic that is too broad to come back with a few drill-down options and a recommended default in the same confirm message, so that I never go through more than one round.
6. As the owner, I want to reply "go" or tweak the length, outline or voice in that reply, so that there are no extra round trips.
7. As the owner, I want a Topic that would run over about 35 minutes to be proposed as 2-3 standalone Parts, so that each one stands alone and none ends on a cliffhanger.
8. As the owner, I want to say "next" and have the Skill take the top line of my Topic backlog, still through the confirm step, so that I can queue Topics ahead of time.
9. As the owner, I want to add to the Topic backlog by hand or by saying "add to backlog: X", so that I can capture ideas when they come up.
10. As the owner, I want the Skill never to suggest Topics on its own, so that the show stays driven by my curiosity.
11. As the owner, I want an optional iOS Shortcut that fires a scheduled task's API trigger as a one-tap summon button, so that I can start an Episode from the Home screen or with Siri. v1 can ship without it.
12. As the owner, I want a fallback summon through a GitHub issue labelled `episode`, where I reply `@claude go`, so that I can still make Episodes if cloud sessions are down.
13. As the owner, I want the session's final message to give the Bundle path and branch, the lint warnings kept and why, anything left out and why, "Learned this run", proposed lexicon and phrase-list additions, and an ETA, so that I know what happened without opening files.

### Research and accuracy

14. As the owner, I want every factual claim traced to a source in the Claim ledger, so that I can check anything I hear.
15. As the owner, I want at least 3 distinct sources (aiming for 5) per Episode, so that one source can't carry an Episode alone.
16. As the owner, I want sources ranked on a ladder (reviews and meta-analyses, then RCTs and guidelines, then single studies and expert reviews, then books and commentary for context only), with blogs, vendors and influencers never counted as evidence, so that weak sources don't get treated as strong ones.
17. As the owner, I want evidence strength said aloud in plain words (strong, early, mixed, textbook), so that I know how much to trust each point.
18. As the owner, I want animal and cell findings labelled as such, with n and population recorded for study sources, so that I don't over-apply results.
19. As the owner, I want every number spoken in the Script to come from a full text, or from an abstract that states that number (**firm**), so that numbers lifted from search summaries never reach the audio.
20. As the owner, I want the two or three load-bearing numbers re-checked against their sources before the Bundle is pushed (**firm**), so that the claims that matter most are right.
21. As the owner, I want a retraction check on any single study behind a protocol (**firm**), so that I'm never told to act on retracted work.
22. As the owner, I want risky topics written with cautious framing, a specific caution next to the action it qualifies, and a Higher-risk flag with a reason in the show notes, never refused and never paused to ask, so that I still get the Episode and stay safe.
23. As the owner, I want no standing disclaimer, so that cautions mean something when they appear.
24. As the owner, I want each field of topics to have a Source profile saying what counts as strong evidence and what triggers the Higher-risk flag, so that one standard adapts to sport, finance, history or health.
25. As the owner, I want a field with no profile to get a draft profile that borrows the strictest neighbouring profile's risk triggers, so that new fields are never treated more loosely.
26. As the owner, I want a cheap claim-check that compares the Script with the Claim ledger without re-reading the sources, so that accuracy doesn't double the cost.
27. As the owner, I want a new Episode that overlaps an old one to have its ledger compared with the old ledger and contradictions flagged, so that errors in old Episodes come to light.

### The Episode itself

28. As the listener, I want each Episode to open on a Hook (about 45 seconds) with a sourced surprise and a promise, not a welcome, so that I'm drawn in at once.
29. As the listener, I want a spoken Roadmap, so that I know where the Episode is going.
30. As the listener, I want each content Segment to open with its main question, invite me to guess, and re-ask it with the answer at the end, so that I remember what I heard.
31. As the listener, I want every hard concept explained first and named second, with an everyday analogy, aimed at a bright 15-year-old, so that I can follow any topic.
32. As the listener, I want each Segment to carry a sourced surprise, a concrete case and a view the host commits to, so that it doesn't sound like a bland summary.
33. As the listener, I want a closing Segment (Protocol, or "Why it matters / what to watch" when there is nothing to act on), then a Recap in retrieval form and a short Sign-off, so that the Episode ends with something I can use.
34. As the listener, I want Episodes to be as long as the topic needs within the Variant's range (Quick 8-15, Standard 15-28 and typically about 25, Deep 28-35 minutes), with no minimum and no padding, so that my time is never wasted.
35. As the listener, I want a single unnamed host who sounds like a well-read friend, uses "I" only for reasoning and never invents experiences, numbers, studies or names (**firm**), so that the voice stays honest.
36. As the listener, I want simulated listener questions in the host's single voice, so that I get the feel of a conversation without a fragile two-host format.
37. As the listener, I want zero to two light moments of humour per Episode, so that it feels human without forced jokes.
38. As the listener, I want no stock AI phrases. The core ten banned phrases block the Bundle (**firm**), and the rest of the versioned phrase list warns, so that the Script doesn't read like slop.
39. As the listener, I want consecutive Episodes not to share long verbatim runs of wording, so that the show doesn't feel templated (warn only).

### Audio

40. As the listener, I want Episodes read by Kokoro `bm_george` by default, so that the voice sounds the most human of the options auditioned.
41. As the owner, I want the Skill to propose a Pocket TTS topic voice (`charles`, `stuart_bell`, `alba`) or the backup `bm_lewis` when it fits the topic, so that some topics get a fitting voice.
42. As the listener, I want gaps between chunks and paragraphs drawn from distributions with per-chunk speed jitter, never fixed, so that the pacing doesn't feel mechanical.
43. As the listener, I want longer chunks (up to about 300 characters, several sentences each) that never cross a paragraph, `[beat]`, `[think]` or heading, so that the model handles the short gaps between sentences naturally.
44. As the listener, I want the pace at about 165 wpm, so that I can fine-tune speed in Apple Podcasts.
45. As the listener, I want numbers, units, times, money and symbols written as words, so that the TTS never reads them wrongly.
46. As the listener, I want terms and names in a pronunciation lexicon applied before TTS (Kokoro as phonemes, Pocket as a respelling), so that they're said right every time.
47. As the listener, I want loudness at -16 LUFS with true peak under control, so that Episodes sit at the same level as other podcasts.
48. As the listener, I want no garbled, truncated or silent stretches, so that I never lose content. An ASR round trip and a silence check catch these before publishing (**firm**).
49. As the owner, I want a re-render of an Episode to sound the same as the first render, so that a re-render doesn't change anything I didn't ask to change. The render is seeded by the Bundle id.

### Publishing and the Feed

50. As the owner, I want to follow the Feed by URL in Apple Podcasts and download Episodes for offline listening, so that it works like any podcast.
51. As the owner, I want Episodes titled `Episode N: Title`, numbered in publish order and never reused, with Parts as `4a`, `4b` and Q&A episodes as `7q`, `7r`, so that the list reads in order.
52. As the owner, I want the Feed kept out of directories and search (`itunes:block`, `podcast:block`, `robots.txt` disallow, a `noindex` archive page, README never linking the Feed), so that the show stays obscure.
53. As the owner, I want nothing in the Feed to name me, so that the public repo doesn't expose me.
54. As the owner, I want the channel description to say once that Claude writes the episodes and a synthetic voice reads them, and nothing about AI in the audio, so that the show is honest without nagging.
55. As the owner, I want show notes with a summary, the source list, any Higher-risk flag and its reason, and a one-line credit for CC BY voices, so that every Episode is documented and licences are respected.
56. As the owner, I want a typographic cover drawn from code (ink blue, cream serif "Plainly Put", 3000x3000 RGB with no alpha) that I approve before it's committed, so that the show looks clean with no stock art.
57. As the owner, I want every Episode's audio kept permanently as a GitHub Release and never in git, so that the repo stays small and nothing is lost.
58. As the owner, I want the Pages site to hold the newest Episodes up to about 600 MB of audio, and never more than about 900 MB (**firm**), so that the site stays under GitHub's 1 GB cap.
59. As the owner, I want Episodes that leave the window dropped from the Feed by default, or repointed to their stable Release URL if the Apple Release-URL test passes, so that I never hit a 404 and, ideally, keep every Episode in the app.
60. As the owner, I want an archive page listing every Episode with a Release download link, so that I can get any Episode back.
61. As the owner, I want to say "bring back episode X" and have it pinned in the window, so that I can re-listen to old favourites in the app.
62. As the owner, I want Parts of a split topic to publish, archive and restore as a group, so that I never get half a series.
63. As the owner, I want a new audio file uploaded and its byte size verified before the Feed is touched (**firm**), so that the Feed never points at missing audio.
64. As the owner, I want a failed deploy to leave the last good site live, so that a bug never breaks my subscription.

### Q&A mode

65. As the owner, I want to name a published Episode by number or title words plus one or more questions, so that I can go deeper on something I heard.
66. As the owner, I want the confirm step to say "Q&A on Episode 7", show my questions rephrased in spoken form, and list possible parents when the match is ambiguous, so that a wrong guess is caught before work starts.
67. As the owner, I want a question that doesn't lead on from the parent recommended as a normal Episode instead, while I can still override, so that Q&As stay focused.
68. As the listener, I want each question to get its own Segment: a short reminder of what the parent said, the answer first, then mechanism, evidence and edge cases, then a "so what", so that the answer makes sense weeks later.
69. As the owner, I want the Q&A to cite the parent's ledger by reference and add at least 2 new sources per question, so that the depth is real.
70. As the listener, I want the Q&A to say plainly if the parent was wrong or too strong, so that errors aren't hidden.
71. As the owner, I want a Q&A about an unpublished parent to be refused with an offer to wait or to edit the parent Bundle, so that labels stay consistent.
72. As the listener, I want a Q&A in its parent's voice by default, so that the show stays consistent.

### Feedback mode and Corrections

73. As the owner, I want to give free-text feedback such as "feedback 7: too long, and it said 'Kokoro' wrong", so that reacting takes seconds.
74. As the owner, I want each remark read back in one line with where it went, so that I can trust it was understood.
75. As the owner, I want taste feedback routed to the Listener profile, avoidable mistakes to Learnings, mispronunciations to the lexicon, voice fit to `suits:` hints and banned phrases to the phrase list, so that each kind of feedback changes the right thing.
76. As the owner, I want an instruction ("make them shorter") applied at once, with the tunable and its new value named, so that I see the effect next time.
77. As the owner, I want a reaction ("7 felt long") logged, and a change proposed only after about 3 similar ones, so that one mood doesn't shift the defaults.
78. As the owner, I want to be asked for feedback only after something changed (a new voice, a style guide bump, a first use of a Variant), so that I'm never nagged.
79. As the owner, I want a Correction graded Harmful, Material or Minor, with the Skill proposing a grade I can change, so that the response matches how serious the error is.
80. As the owner, I want Harmful and Material errors re-rendered as `-v2` under the same guid, with a minimal edit and a dated show-notes line, after my one-reply confirm, so that the Feed carries the right version.
81. As the listener, I want a Harmful Correction to add a short spoken line near the start, so that a replay doesn't mislead me.
82. As the owner, I want a Minor error to get a show-notes line at once and a re-render only when I say "go", so that small slips cost nothing.
83. As the owner, I want one Correction to check the parent's Q&As and sibling Parts for the same claim and put every hit in the same confirm, so that the whole Episode family is fixed together.
84. As the owner, I want to be told to delete and re-download a corrected Episode, because Apple won't replace a copy I've already downloaded.
85. As the owner, I want Harmful errors in Episodes outside the Pages window still re-rendered into their Release and noted on the archive page, so that the archive stays right.

### Learnings and the Listener profile

86. As the owner, I want the Skill to record lessons (what went wrong and what to do instead) and never topic facts, so that later runs avoid known mistakes and spend fewer tokens.
87. As the owner, I want a smooth run to write nothing, so that Learnings don't fill with noise.
88. As the owner, I want every run to read only about 3-5k tokens of Learnings (the index, general lessons and one or two field files), so that the cost stays low.
89. As the owner, I want lessons I give never removed by self-correction or compaction, so that my input sticks.
90. As the owner, I want the Skill only able to tighten higher-risk triggers on its own, and any loosening proposed for my OK (**firm**), so that safety only ratchets up.
91. As the owner, I want outlets named only for a concrete observed error, never for reputation or political lean, so that Learnings stay fair.
92. As the owner, I want a Listener profile of about 300-500 tokens, read by every run, that records my taste from Q&A questions and feedback, so that Episodes fit me better over time.

### Running and maintaining the system

93. As the owner, I want Bundle branches auto-merged only when every changed path is in the allow-list and no firm rule fails, and anything else left open labelled `needs-owner`, so that the Skill can't change code or config unseen.
94. As the owner, I want a failed stage to open one GitHub issue assigned to me with the stage, the Bundle and the last log lines, and success to be silent, so that I only hear about problems.
95. As the owner, I want an ASR gate failure to re-render the named chunk once before an issue opens, so that one-off TTS glitches fix themselves.
96. As the owner, I want manual workflow dispatch for retries, re-renders and redeploys, so that I can recover from the GitHub app.
97. As the owner, I want a `dry_run` mode and a test feed, so that changes can be tried without publishing.
98. As the owner, I want a one-off real-device checklist on my iPhone before the first real Episode, so that the Apple-specific unknowns get settled.
99. As the owner, I want the plan-usage pilot measured on the first real Episode, with a cheaper model for research subagents as the first lever if usage is heavy, so that I know what an Episode costs.
100. As a maintainer (the owner or an agent), I want code, comments, commits and logs that read like a careful person wrote them, using glossary names, so that the build itself has no slop.
101. As a maintainer, I want one shared lint run in the session, on the branch, before TTS and before publish, so that the rules can't drift between places.

## Implementation Decisions

### System shape

- Two halves joined by one contract, the **Bundle**. The Skill writes Bundles and never touches audio, the Feed or the Episode registry. The Pipeline reads Bundles and never writes them, except the registry and generated site output.
- One public GitHub repo (working name `podcast`) holds the Skill, Learnings, config, Bundles, the Pipeline, the registry and the planning history. Audio never goes in git.
- The repo follows the Matt Pocock skills conventions: a `CLAUDE.md` with the agent skills block and build rules (glossary names, research/18 section 7 build rules), a root glossary, `docs/agents/` with GitHub Issues as the build tracker, a lazily created `docs/adr/`, and the wayfinder planning history under `docs/wayfinder/` (without prototypes).
- Issue labels keep `episode` summons, `pipeline-failure`, `needs-owner` and build or triage tickets apart. Build tickets never contain `@claude`.

### The Skill (`episode`)

- A Claude Code skill committed in the repo, with a SKILL.md plus reference files for the episode template and style guide (research/05 section 12 as signed off, 12.11 softenings applied), the research and accuracy standard (ticket 06 plus recommendations 1-5), writing for TTS (ticket 14), and the de-slop checklist (research/18 section 9 and firm rules F1-F9).
- **Runtime:** a Claude Code cloud session in a dedicated environment with **Full** network access, since the Trusted level blocks journals, news sites and PubMed. It pushes through the Claude GitHub App proxy, so there is no token in the session. Numbers that carry weight are read as raw text (curl or pdftotext), not through summarised fetches.
- **Modes, all in one Skill:**
  - *Episode* (a Topic, or "next").
  - *Q&A* (a published Episode plus questions).
  - *Feedback* (`feedback N: ...`; feedback dropped into an Episode summon is still handled).
  - *Backlog* ("add to backlog: X").
  - *Bring back* ("bring back episode X" adds the Episode id to the pin list).
- **Every run reads** the Learnings index, general lessons, the one or two matching field files (by the overlap rule) and the Listener profile.
- **Confirm step:** exactly one message, answered in one reply. It holds the Variant, outline, drill-down options if needed, voice, Part split if needed and, for Q&A, the matched parent and the questions rephrased. Corrections use the same one-reply confirm (claim, grade, new wording, source).
- **Research:** builds the Claim ledger as it goes. Ledger line fields: id, claim, source, tier, read depth (full text / abstract / secondary), n and population for study sources, tags including `consensus`. A Q&A cites parent lines as `{p:cN}`.
- **Script writing:** spoken form throughout. Markup is exactly research/05 6.3: `##` Segment headings, blank-line paragraphs, `[beat]`, `[think]`, and `{cN}` Claim tags. There is no emphasis or mood markup (ticket 19), and the research/18 A8/A10 wording devices stay light-touch.
- **Before pushing:** claim-check against the ledger, the firm number and retraction checks, `pipeline lint`, and the ten-question self-review.
- **Push:** rebase on `main`, push a `claude/<slug>` branch. Parts are pushed together. On a conflict in Learnings, rebase and re-append its own lines (compaction is skipped that run).
- **Writes in the same commit as the Bundle:** Learnings changes (soft cap of about 3 new lessons), Listener profile observations (Q&A and feedback), and pin-list or backlog edits.
- **Proposes but never writes on its own:** shared lexicon entries (except owner-reported ones from feedback mode), Pocket `verified:` additions drawn from the ASR report, Source profile loosening, default changes after about 3 reactions.

### Bundle contract

A Bundle is one folder per Episode, named by its Bundle id `<date>-<slug>`, which the Skill fixes. It holds:

- **`script.md`**: the Script with the markup above. Segments come from the headings and are not stored separately.
- **`meta.yaml`**: title, summary, variant, `part: {n, of, series_slug}`, voice, `risk_flag` / `risk_reason`, `pronunciations` (same entry shape as the lexicon; wins for this Episode), `wpm_budget`, target and spoken words, `style_guide_version`, `deslop_version`, `parent_episode` (an Episode id, for Q&A), `questions` (the owner's verbatim wording, for Q&A), `revision` (starts at 1), and `corrections:` (a list of date, tier, claim, fix, source).
- **`show_notes.md`**: written form. A dated correction line goes at the top when one applies. The Release text and the Feed item description are generated from it, and CC BY voice credits are appended from the voice roster.
- **`ledger.md`**: one line per claim, in the shape above.
- **`lint_report.yaml`**: the warnings kept, with reasons.

### Identity and the Episode registry

- The Bundle id seeds the render (pause draws, jitter, Pocket seed), so a re-render sounds the same.
- The Pipeline gives the Episode number and Episode id at publish time, in publish order: `ep-007-<slug>`, Parts `ep-004a-…` (letters `a`-`c`), Q&As `ep-007q-…`. Q&A letters run `q` to `z`, then `z2`. A Q&A on a Part takes the topic number (`4q`).
- The **Episode registry** (`episodes.yaml`) records: number (as text), Episode id, Bundle id, guid, voice, file name, bytes and duration. Only the Pipeline writes it. A guid never changes.
- Listener-facing titles are `Episode N: Title`, with no follow-up wording for Q&As. There is no `itunes:episode`. Q&As are `itunes:episodeType` `bonus`.

### Config files (contract with the owner)

- **Voice roster:** for each voice, its engine, base speed or stretch factor, seed and light `suits:` hints.
  - `bm_george`: the default for everything.
  - `bm_lewis`: backup, base speed about 1.12.
  - Pocket `charles` (stretch 0.905) and `alba` (0.907), both CC BY with a credit line; `stuart_bell` (no stretch), CC0.
  - Stretch floor about 0.85 (soft).
  - Re-calibrate `bm_george`'s base speed for long chunks.
- **Pacing:** chunk cap about 300 characters (soft). Gap distributions at chunk, paragraph and Segment boundaries per research/18 5.4 (sentence about 0.38 s, paragraph about 0.75 s, Segment 1.3-1.7 s), plus `[beat]` and `[think]` lengths (`[think]` about 1 s, owner 2026-10-30, replacing research/18's 3-4.5 s). Speed jitter ±0.025 per chunk. Trim on. Breaths off in v1.
- **Lexicon:** a `verified:` list of capitals words read right as written, and `entries:` of `{term, kokoro, pocket, by, note}`. `kokoro` is an espeak en-gb phoneme string in slashes or a lower-case respelling. `pocket` is optional (it defaults to the term as written). `note` holds the human version.
- **De-slop rules:** the versioned phrase list. The core ten block; the rest warn.
- **Show:** channel fields (title *Plainly Put*, author = show name, no owner email, `© 2026 Plainly Put`, `en-GB`, Education, not explicit, episodic, no seasons, link = archive page), the channel description text from ticket 12, block tags and the artwork path.
- **Listener profile:** about 300-500 tokens (soft). Older observations are merged into summary lines when it grows past that.
- **Topic backlog:** a plain list. Only the owner adds to it.
- **Pin list:** Episode ids kept in the Pages window.
- **Template tunables:** Variant ranges, typical Standard length, wpm budget (165, re-calibrated to the voice after two Episodes) and similar, versioned by `style_guide_version`.

### Pipeline package (Python, ruff, pytest)

- **Four public entry points: `lint`, `render`, `publish`, `site`.** Each takes Bundle folders or the repo state and is runnable from the command line and from Actions. Everything else is private and kept that way by import-linter. pre-commit runs ruff.
- **`lint`** is one module with one rule set, run in four places: the session, the branch before merge, before TTS and before publish. It blocks only on firm rules and warns otherwise.
  - *Firm (TTS safety):* digits, banned symbols, URLs, abbreviations with full stops (including a.m. and p.m.), fillers and stage directions (F5), and capitals words neither `verified:` nor covered by an entry. Text inside an entry is exempt.
  - *Firm (contract):* Bundle schema validity, every Claim tag resolving to a ledger line (`{p:cN}` against the parent's ledger), every content Segment carrying a Claim tag, the core ten phrases, and `meta.yaml` versions present.
  - *Warn:* heteronyms; rest of the phrase list; six-word runs shared with any of the last ten Bundles; sentence length; segment balance and the other soft research/05 checklist items; pace against word count.
  - Accepts the dated correction line and the spoken Harmful correction line.
- **`render`** turns a Bundle into a 24 kHz WAV timeline.
  - *Chunking:* sentences packed up to the chunk cap, never crossing a paragraph, `[beat]`, `[think]` or heading.
  - *Lexicon:* applied per chunk before synthesis. For Kokoro, the whole chunk is phonemized with a stand-in word for each term, the entry's phonemes are spliced in, and the call uses `is_phonemes=True`. Pocket gets a plain text swap. Bundle `pronunciations` override the shared lexicon.
  - *Engine seam:* `synthesise(text, voice, speed) → audio`. The voice roster picks the engine.
  - *Speed:* Kokoro gets a per-call speed (base plus jitter). Pocket gets a WSOLA stretch.
  - *Gaps:* between chunks, drawn from the pacing distributions with an RNG seeded by the Bundle id. The model owns the gaps inside a chunk.
  - *Re-render one chunk:* supported, for the ASR retry (Pocket with a new seed, Kokoro with a new speed draw).
- **`publish`** makes an Episode from a Bundle.
  - Two-pass `loudnorm` to I -16, TP -1.5 with its limiter, resampled 24 to 44.1 kHz, then encoded to 64 kbps mono AAC `.m4a`.
  - Gates run on the decoded `.m4a`. **Firm fails:** an ASR (`faster-whisper` `base.en`, int8, CPU) longest run of missing Script words of 6 or more, or 4 or more missing at the end, comparing after normalising both sides; silence over 3 s; integrated loudness outside -16 ±2 LUFS; true peak above -0.5 dBTP; wrong format (`ffprobe`). On an ASR fail it re-renders the named chunk once and re-gates. Pitch spread is never a gate.
  - Then: number the Episode, upload the Release (tag = Episode id, text from the show notes, assets the `.m4a` and `asr_report.yaml`), verify the uploaded byte size against the local file (**firm**, before anything else changes), and commit the registry.
  - Parts publish as a group with one registry commit, all or nothing.
  - *Re-render mode* (given an Episode id): writes `-v2.m4a` (then `-v3`…) into the same Release, moves the registry entry and the enclosure, keeps the guid and keeps the old file.
  - *`dry_run`:* produces the encoded file as a workflow artifact only, with no Release, registry change or deploy.
- **`site`** builds the Pages site.
  - Builds the Feed (RSS 2.0 plus the iTunes and podcast namespaces, research/04's 11 constraints, block tags), the plain `noindex` archive page (one top sentence, then title, date, one-line summary, duration and link, newest first), `robots.txt`, and the artwork.
  - *Window:* newest Episodes up to about 600 MB (soft) plus pinned ones, with Parts kept as a group. Over budget, it warns and drops the oldest unpinned. If the window still exceeds the 900 MB firm ceiling, the deploy is refused.
  - *Leaving the window:* the item is dropped, or repointed to the stable Release download URL once the Apple test passes. A config switch, off by default.
  - *Checks before deploy:* Feed checks in Python, enclosure lengths match bytes, durations, artwork 3000x3000 square RGB with no alpha, and every window file fetched (any fetch failure fails the deploy).
  - *After deploy:* a HEAD, range and guid smoke check once the cache window has passed.
  - Also builds a test feed on the same site from a test registry.
- **GitHub access** (Releases, dispatch, issues, registry commits) goes through one thin client inside the package, so the four entry points can be tested with a fake.
- **Artwork:** an SVG in the repo, rendered to PNG by a small script, with the font licence (OFL) committed. The owner approves the PNG before it's committed.

### Workflows (GitHub Actions)

- **auto-merge** (on a `claude/` branch PR): runs `lint`, then squash-merges only if every changed path is allowed and no firm rule fails. Otherwise it leaves the PR open labelled `needs-owner`.
  - Always allowed: Bundles, Learnings, the pin list, the Listener profile, a backlog-only change, the lexicon and the phrase list.
  - Also allowed for feedback-mode commits marked `owner-instructed` that quote the owner: template tunables and the voice roster.
  - After merging, it dispatches publish-episode for a new Bundle, re-render mode when a published Bundle's `revision` rises, and deploy-site for a show-notes-only change or a pin-list change.
- **publish-episode** (dispatch, with inputs Bundle or Episode id, `dry_run`, re-render): installs only the engine the voice needs; caches models (Kokoro int8 ONNX, Pocket, `base.en`) with `actions/cache`; runs lint, render, gates, encode, Release, byte check and registry commit; then dispatches deploy-site.
- **deploy-site:** runs `site`, then deploys to Pages.
- **claude:** the fallback, `anthropics/claude-code-action` on owner issues labelled `episode` or comments mentioning `@claude`. It uses the `CLAUDE_CODE_OAUTH_TOKEN` secret and the same branch flow.
- **Chaining and failure handling:**
  - Workflows chain by explicit dispatch, because commits made with `GITHUB_TOKEN` don't trigger workflows.
  - One concurrency group for publishing and deploying.
  - Timeouts: render job about 45 min, deploy about 15 min, re-set to about twice the measured render time after the first runs.
  - Only network steps retry, at most twice with a short wait, plus the one ASR chunk re-render.
  - A failure opens a `pipeline-failure` issue assigned to the owner. Pages keeps the last good site.
- **Ruleset on `main`:** PR only, no force push, owner bypass.

### Content rules carried as reference, not code

- Template: Hook, Roadmap, content Segments (Recall prompt opens and re-asks; surprise, concrete case, committed view), closing Segment (Protocol or Why it matters / what to watch, tool-led or mechanism-led per topic), Recap, Sign-off. Segment count follows the topic. No sting, music or show line in v1, and the host stays unnamed.
- Q&A shape per ticket 11: about 4-8 min per question (soft), about 3 questions typical.
- Firm rules F1-F9 from research/18 (F4 checked by the Skill; F6's silence bound replaced by the 3 s gate). Humour zero to two light moments. Breaths off.

### Day-one seeding

- 15 field files from research/05 section 13: each has its profile at the top and an empty lessons section.
- The Learnings index with keywords.
- `general.md` seeded with the planning-era lessons from ticket 10 (numbers from search summaries proved wrong; the Trusted network blocked journals).
- The lexicon, seeded from `prototypes/pronunciation/lexicon.yaml`, with the prototype's pronunciation logic ported into the package.
- An empty registry, pin list and backlog. The cover SVG and show config.

## Testing Decisions

- **What a good test is:** it drives a public entry point with a Bundle or repo-state fixture and checks external output: the lint verdict and messages, the gate verdict and the chunk it names, the Feed XML and archive HTML, the window chosen, the registry entry written, and the calls made to the GitHub client. Tests never assert private helpers, chunk-packing internals or exact random draws. Determinism is tested as "the same Bundle id gives byte-identical timing", not as specific values.
- **Seam 1: the `pipeline` entry points on fixture Bundles, with GitHub faked.** The highest seam, and where most tests live.
  - `lint`: one good fixture plus one fixture per firm rule that must block, and per warning that must only warn; `{p:cN}` resolution against a parent fixture; correction lines accepted; the shared six-word run check against fake history.
  - `publish`: gates on synthetic audio with deliberate faults (dropped words, truncated end, 4 s silence, too quiet, clipped peak, wrong format), matching research/15's probe; the ASR chunk retry happens once, then an issue opens; the byte check runs before the registry commit; Parts are all or nothing; re-render mode keeps the guid and writes `-v2`; `dry_run` touches nothing.
  - `site`: the Feed passes the Python checks; block tags are present; Q&A items are `bonus`; there is no `itunes:episode`; window selection under budget, over budget and over the firm ceiling; pinned and grouped Parts; the repoint switch; a fetch failure fails the deploy; artwork checks.
  - auto-merge path rules: the allow-list, `owner-instructed`, and which workflow a merge dispatches. Test these as a pure function over a changed-path list and a commit message, called from the workflow.
- **Seam 2: `synthesise(text, voice, speed)` with a fake engine.** It returns tone or silence of a length proportional to the text, so render and pacing tests (chunk boundaries respected, gaps drawn and seeded, lexicon applied per engine, Pocket stretch called) run in seconds without Kokoro or Pocket. The real engines run only on the smoke Bundle (about 1 minute of Script that uses every markup element, a lexicon term and a number in spoken form), through publish-episode with `dry_run`, on demand and before the first real Episode.
- **Seam 3: the Skill, tested only through what it produces.** There are no unit tests of the prompt. A Skill Bundle must pass `pipeline lint` in the session and on the branch. Acceptance is one pilot Episode run end to end with `dry_run`, then the first real Episode with the plan-usage reading before and after.
- **Prior art:** the repo has no tests yet. Reuse the prototype probes as fixtures and expectations:
  - research/15's four-fault probe on the `bm_george` take, for gate thresholds (clean missing run 1-3 words, broken 8-24);
  - research/14's 20 worst pronunciation cases and their before/after results, for lint and the lexicon apply step;
  - the voice audition settings, for roster values.
- **Manual acceptance (one-off, owner):**
  - The real-device checklist of seven items from research/15: follow by URL with block tags; download and offline play; seek; how `Episode N: Title`, `4a` and `7q` titles display; the Release-URL enclosure test (302, `application/octet-stream`, seek, offline), which turns on the repoint switch; a re-render of a not-yet-downloaded Episode arrives (time it); whether an edited description refreshes.
  - The minute-15 listen of a full Standard Episode in `bm_george`.
  - A per-voice check at the final encoding.
  - Approval of the cover PNG.
  - Listening to the names in pronunciation cases 16, 19 and 20.

## Out of Scope

- A native iOS app, or any paid App Store presence.
- Paid hosting, or paid TTS as the default path (Polly is dropped, so there's no cost cap to build).
- Auto-suggested Topics, daily briefs and chapters.
- A summon web page or PWA on GitHub Pages (the iOS Shortcut is the optional extra; the Code tab is primary).
- Two-host format, voice cloning, a prosody graft, emphasis or mood markup, split renders across runners, a third TTS engine (ticket 19).
- Breaths, a sting, music and per-episode artwork in v1. The sting has a hook (at most ~5 s, licence recorded) and is A/B tested later.
- Standalone correction Episodes and scheduled re-checks of old Episodes.
- Re-encoding published audio to save space, and WAV masters.
- Ratings or tags in feedback.
- Pitch spread as a quality gate.
- Parked, not queued: Pocket with livelier sample clips (gated licence terms), non-commercial expressive clips, and post-processing pitch shaping. Reopen only if the minute-15 listen finds the baseline flat.

## Further Notes

- **Unknowns the build doesn't depend on, settled by the device test:** whether Apple follows a Release URL enclosure (decides the repoint switch); whether edited show notes refresh for a feed followed by URL; how fast a same-guid re-render arrives (reports say hours, up to about 24).
- **Unmeasured numbers to re-set after the first runs:** Kokoro render time on a runner (estimated 10-25 min per Episode), Pocket render time, ASR time (estimated 3-5 min), job timeouts, `bm_george`'s base speed with long chunks, and the Learnings read budget after the usage pilot.
- **Per-episode cost:** estimated as a large share of one Pro 5-hour window per Standard Episode, comfortable on Max. Measured in the pilot.
- **Time from "go" to audio:** about 20-45 min to a pushed Bundle, plus 10-25 min of render.
- **Public repo:** the history shows every topic asked about, Learnings and the Listener profile. The owner accepted this.
- **Build order suggestion:**
  1. Repo skeleton and conventions.
  2. `lint` (unblocks the Skill).
  3. `render` with the fake engine, then the real engines.
  4. `publish` gates.
  5. `site`.
  6. Workflows.
  7. The Skill.
  8. Smoke Bundle and `dry_run` pilot.
  9. Device checklist.
  10. First real Episode with the usage pilot.
- Research files under `wayfinder/research/` hold the full detail behind each decision. research/05 section 12 (template), research/18 sections 7-9 (de-slop rules and lint), research/04 (Feed constraints) and research/15 (gates) are the ones an implementer will need open.
