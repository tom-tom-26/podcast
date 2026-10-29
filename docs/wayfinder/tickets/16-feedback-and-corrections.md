---
title: Feedback loop and published corrections
type: grilling
status: closed
blocked-by: []
claimed-by: owner (this session)
---

## Resolution

Closed 2026-10-29 after three grilling rounds with the owner (Q1-Q17). The owner is the Feed's only listener, so a correction exists for the archive and for replays, not to reach an audience.

**Feedback**
- **Feedback mode of the same Skill** is the documented way in: the owner starts a Code session and says "feedback 7: too long, and it said 'Kokoro' wrong". Episodes are matched by number or title words, as in Q&A mode (ticket 11). Feedback dropped into an Episode summon is still handled, not turned away.
- **Free text only**, no ratings or tags. The Skill sorts each remark and reads it back in one line ("Logged: 7 felt long -> listener profile; 'Kokoro' -> lexicon"). Praise counts as signal.
- **Routing:** taste about defaults (length, depth, pace, recall prompts, tone) -> Listener profile; an avoidable mistake -> Learnings with `source: owner` (ticket 10); mispronunciation -> pronunciation lexicon (format is ticket 14's); voice fit for a topic -> `suits:` in `config/voices.yaml` (ticket 12); banned or overused phrases -> the versioned phrase list (ticket 18); factual error or overstatement -> the correction path below. Anything unclassifiable becomes one Listener profile line.
- **Instructions vs reactions:** an instruction ("make them shorter") changes the tunable at once; the Skill names the tunable and new value ("Standard typical 25 -> 22 min") and bumps `style_guide_version` if the template changed. A reaction ("7 felt long") is logged, and a change is proposed after about 3 similar ones (soft), as in ticket 11. Lexicon entries and owner Learnings apply at once.
- **Listener profile widened** to all owner taste signals (Q&A questions and Episode feedback), same ~300-500 tokens (soft); older observations are merged into summary lines when it outgrows that. Glossary updated.
- **Asking for feedback:** only after something changed (a new voice, a `style_guide_version` bump, a Variant used for the first time). Otherwise never.
- **Auto-merge:** feedback commits may touch the lexicon and the phrase list freely (additive, cheap to undo). Template tunables and `config/voices.yaml` auto-merge only in feedback mode, on commits marked `owner-instructed` whose message quotes the owner's words. Everything else keeps ticket 07's rules.

**Corrections**
- **Who finds errors:** the owner, Q&A episodes (ticket 11), and an overlap check: when a new Episode covers an old one's topic, the Skill compares the new ledger against the old one and flags contradictions. No scheduled re-checks.
- **Tiers** (the Skill proposes, the owner may move it):
  - *Harmful:* a wrong claim that could cause harm if acted on (health, safety, money, law), flagged or not.
  - *Material:* wrong on something central, or a claim much stronger than its evidence.
  - *Minor:* a wrong side detail, slight overstatement, mispronunciation or one garbled chunk.
- **Actions:** Harmful and Material get a `-v2` re-render under the same guid with a minimal edit (the wrong sentences and their neighbours, ledger updated) and a dated line at the top of the show notes ("Corrected 2026-11-03: an earlier version said X. That was wrong; Y (source)."). Harmful also gets a short spoken line near the start ("This version corrects what an earlier one said about X."). Minor gets the show-notes line only; re-render only on request; mispronunciations always also get a lexicon entry. No standalone correction episodes.
- **Approval:** Harmful and Material need the owner's one-reply confirm (claim, tier, new wording, source). A Minor show-notes line applies at once and is reported in the final message; a Minor re-render needs "go".
- **Mechanics:** the correction edits the Bundle (`script.md`, `ledger.md`, `show_notes.md`), bumps `revision` in `meta.yaml` and appends to a `corrections:` list (date, tier, claim, fix, source) on the usual `claude/` branch. Auto-merge sees a published Bundle whose revision rose and dispatches publish-episode in re-render mode; a show-notes-only change dispatches deploy-site. Manual dispatch stays as the fallback. The final message tells the owner to delete and re-download the Episode, since a downloaded copy is not replaced.
- **Episode family:** one correction run also greps the ledgers of the Episode's Q&As (`parent_episode`) and sibling Parts for the same claim and puts every hit into the same confirm.
- **Learnings:** Harmful and Material corrections write a lesson on how the error got through, to the field's file, `source: owner` if the owner reported it, `source: skill` if the overlap check or a Q&A found it. Minor writes a lesson only when the same kind recurs.
- **Episodes outside the Pages window:** Harmful still re-renders into the Release, updating the registry and archive page; the Feed is untouched unless pinned. Material and Minor get the show-notes and archive-page line only, re-render on request.

**Apple behaviour (checked 2026-10-29; hosts' reports, Apple documents nothing):** same guid with a new enclosure reaches anything not yet downloaded once the feed refreshes (hours, up to ~24); downloaded copies stay stale; whether edited show notes refresh for a follow-by-URL feed is unknown. Sources: podcasters.apple.com/support/838 and /823, Buzzsprout help article 51, RSS.com help 44002246497, AntennaPod forum thread 569. The decisions do not depend on the unknowns.

Handed on:
- **07:** `revision` and `corrections:` in `meta.yaml`; auto-merge dispatches re-render on a revision bump of a published Bundle, deploy-site on a show-notes-only change; allow-list adds the lexicon and phrase list, plus template tunables and `config/voices.yaml` for `owner-instructed` feedback-mode commits.
- **14:** owner-reported mispronunciations arrive through feedback mode and become lexicon entries at once; they auto-merge.
- **15:** real-device checks: (1) a re-render of a not-yet-downloaded Episode arrives, and how long it takes; (2) an edited description shows in the app. Lint accepts the correction lines.
- **18:** feedback can add phrases to the versioned phrase list; it auto-merges.
- **Glossary:** Listener profile widened; Feedback mode and Correction added.

## Question

How does the owner tell the system an Episode was good, too long, wrong or mispronounced, with the least effort from an iPhone? Where does that feedback go: the template's tunable defaults (length, wpm budget, recall-prompt count, banned phrases), Learnings (ticket 10), the pronunciation lexicon (ticket 14)? And when an already-published Episode contains a factual error, especially a health claim: is it re-rendered under the same guid (and will Apple Podcasts replace a downloaded copy?), corrected in the show notes only, or followed by a correction or Q&A episode?

Context: research/01 (length is a tunable default to be set by owner feedback), research/05 section 9.4 and `style_guide_version`, research/04 section 9 (guid and enclosure URL never change), ticket 06. Covers the map's "feedback loop" item and adds corrections, which no ticket covered. Proposed by the Opus review, 2026-10-29.

## Notes

- 2026-10-29: ticket 10 closed. Owner feedback about an avoidable mistake becomes a Learnings lesson with `source: owner` (never auto-removed); taste feedback about defaults goes to the template tunables. This ticket still decides how the owner sends it.
- 2026-10-29: ticket 07 closed. Re-render mechanics are fixed: manual publish-episode with an Episode id writes `-v2.m4a` into the same Release, moves the registry entry and enclosure, keeps the guid. This ticket decides when and how the owner asks for it.
- 2026-10-29: ticket 12 closed. Owner reactions to a voice on a topic should update the light `suits:` hints in `config/voices.yaml`.
- 2026-10-29: ticket 11 closed. Q&A episodes are for depth, not corrections, but feed this ticket two ways: `config/listener_profile.md` (auto-appended taste observations; default changes proposed after ~3 Q&As, owner approves), and parent errors a Q&A surfaces, which are said plainly and flagged here for the correction path.
