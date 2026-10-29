---
title: Q&A episode skill
type: grilling
status: closed
blocked-by: []
claimed-by: owner (this session)
---

## Resolution

Closed 2026-10-29 after two grilling rounds with the owner (Q1-Q15). The owner's framing: a Q&A is for **more depth**, not for corrections, and the questions asked are a signal of how much detail the owner wants and where their curiosity goes.

- **One Skill, Q&A mode.** No second skill. When the summon names a published Episode plus one or more questions ("7: does decaf count?"), the `episode` Skill switches to Q&A mode. It shares every reference (template, accuracy, TTS, lint, Learnings) and adds one short Q&A section. The confirm message says "Q&A on Episode 7", so a wrong guess is redirected there.
- **Same Feed.** Ticket 12's labelling stands: `Episode 7q`, then `7r`...; `4q` for a split topic; `itunes:episodeType` `bonus`; Episode id `ep-007q-<slug>`.
- **Finding the parent:** the owner gives a number or a few title words; the Skill matches them against `episodes.yaml` and Bundle titles, then reads the parent's `script.md`, `ledger.md`, `show_notes.md` and `meta.yaml` from the Bundle folder the registry names. Several matches are listed in the confirm step and the owner picks in the "go" reply.
- **Several questions per Q&A** (expected to be the norm; about 3, soft ±25%). Each question becomes one segment.
- **Must lead on from the parent.** Test: does the answer need the parent's content to make sense? A question with no real link is recommended as a normal Episode in the confirm step; the owner may override.
- **Errors in the parent:** not the purpose, but if research shows the parent was wrong or too strong, the Q&A says so plainly ("In episode 7 we said X. That was too strong. Here's why."), notes it in the show notes, and flags it in the session's final message. Whether to re-render the parent is ticket 16's.
- **Q&A about a Q&A:** allowed. `parent_episode` points at the exact Episode (`7q`); the label takes the next letter on the root number (`7r`).
- **Parent must be published** (in `episodes.yaml`), since the label comes from its number. Otherwise the Skill says so and offers to wait or to fold the question into an edit of the unpublished parent Bundle.
- **Shape** (adapts research/05 section 9.3): Hook with the question(s) and a one-line answer to the main one, then one segment per question (a one- or two-sentence reminder of what the parent said, the answer first, then deeper material such as mechanism, evidence and edge cases, then a "so what"), then one recall prompt, a short recap, and a sign-off pointing back to the parent. About 4-8 min per question (soft), so ~10-25 min for three. The Variant is proposed in the confirm step like any Episode; no fixed Quick cap.
- **Assumes the parent was heard**, but restates the relevant point before building on it, so it still makes sense weeks later. Overrides research/05's "don't assume earlier episodes" for Q&A only.
- **Research:** start from the parent's ledger and sources, cited by reference (`{p:c3}`) and not re-checked; fresh research for each question with at least 2 new sources per question (soft, owner-approved). Ticket 06 applies unchanged: source ladder, claim-check against the ledger, and a new Higher-risk flag if a question moves into riskier ground than the parent.
- **Learnings:** as ticket 10, read and write the parent's field file(s).
- **The owner's wording:** each question is spoken in a faithful spoken-form rephrasing; the show notes quote the original verbatim. The confirm step shows the rephrasing.
- **Voice:** the parent's voice by default; another only if the confirm step proposes it for a clear reason.
- **Confirm message** (one reply, as ticket 05): matched parent, the questions as rephrased, any to split off into a normal Episode, the outline (one segment per question), proposed length and voice. The owner replies "go" or tweaks.
- **Listener profile (new):** `config/listener_profile.md`, about 300-500 tokens (soft), read by every run, normal or Q&A. After each Q&A the Skill auto-appends a one-line observation with the episode reference (e.g. `7q: asked for the mechanism under the dose numbers; wants the why behind doses`). When a pattern recurs across about 3 Q&As (soft), the Skill *proposes* a default change in its final message (e.g. "go one level deeper on mechanisms in health episodes"); it lands in the profile or the template tunables only with the owner's OK. Taste, so not Learnings (ticket 10).
- **Bundle fields:** `meta.yaml` gains `questions` (the owner's original wording, list) alongside `parent_episode` (the parent's Episode id).

Handed on:
- **07:** `config/listener_profile.md` in the repo layout and in the auto-merge allow-list (observations are written in the Bundle commit); `questions` in `meta.yaml`; lint accepts `{p:cN}` tags, resolving them against the parent's ledger.
- **10:** owner taste signals from Q&As go to the listener profile, never to Learnings.
- **16:** the listener profile is one input to the feedback loop; parent errors surfaced by a Q&A are flagged for 16's correction path.
- **Glossary:** Listener profile added; Q&A episode reworded.

## Question

The owner wants a step beyond a normal podcast: point at an existing episode, drop a question, and get a Q&A episode answering it. Decide whether this is a second skill (and its contract with the first), what it takes as input (episode id plus question, how it finds the episode's script, sources and ledger), its episode shape and length, how its research differs from a fresh episode, and how it appears in the feed (linked to the parent episode, separate series, or same feed). Context: the Episode template, the accuracy standard, and the pipeline architecture.

## Notes

- 2026-10-29: ticket 10 closed. Q&A episodes follow the same Learnings rules, reading and writing the parent episode's field file(s).
- 2026-10-29: ticket 07 closed. A Q&A episode is an ordinary Bundle with `parent_episode` set in `meta.yaml`, using the same branch, lint and publish flow.
- 2026-10-29: ticket 12 closed. Default Q&A labelling if Q&A shares the Feed: parent number plus a letter from `q` (`Episode 7q`, then `7r` ... `7z`, `7z2`); a Q&A on a Part attaches to the topic number (`4q`); `itunes:episodeType` `bonus`; Episode id `ep-007q-<slug>`. 11 may override only if it moves Q&A out of the Feed.

## From the final sign-off session (2026-10-29)

When the owner's question isn't linked to a published Episode, the Skill offers to add it to `config/backlog.md` as well as recommending it as a normal Episode. It adds the line only if the owner says yes.
