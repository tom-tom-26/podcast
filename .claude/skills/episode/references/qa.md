# Q&A mode

From ticket 11. A Q&A goes deeper on the owner's questions about one published Episode, its parent. It is for more depth, not for corrections. Everything else in this Skill applies unchanged, unless this file says otherwise. Every number here is soft, about ±25%.

## Finding the parent

The summon names the parent by number or by a few title words, then gives one or more questions: "7: does decaf count?", "the tides one: why two a day?".

1. Read `episodes.yaml`. Match a number against `number` (`7`, `4a`, `7q`). Match title words against `title` in `bundles/<bundle_id>/meta.yaml` for each entry.
2. One match: read the parent's `meta.yaml`, `script.md`, `ledger.md` and `show_notes.md` from `bundles/<bundle_id>/`.
3. Several matches: list them in the confirm message, number and title, with the likeliest marked as the default. The owner picks in the "go" reply.
4. The parent isn't in `episodes.yaml` (its Bundle is merged but not yet published, or not merged at all): don't write a Q&A, because its label comes from the parent's number. Say so in one message, and offer to wait until it publishes or to fold the questions into an edit of the parent Bundle. Then stop.

A Q&A on a Q&A is allowed: `parent_episode` is the exact Episode asked about (`ep-007q-...`), and the Pipeline gives it the next letter on the topic number.

## Does each question lead on?

The test: does the answer need the parent's content to make sense? A question that doesn't is recommended in the confirm message as a normal Episode instead. Offer to add it to `config/backlog.md` as well, and add the line only if the owner says yes. The owner may override and keep it in the Q&A.

## Confirm

The same one message as step 1 of `SKILL.md`, opening with "Q&A on Episode 7: <title>". It holds:

- each question as you'll say it, rephrased faithfully into spoken form;
- any question recommended as a normal Episode instead, and the backlog offer;
- the outline: one Segment per question, in the order you'll answer them;
- the Variant and length: about 4-8 minutes per question, so about 10-25 minutes for the typical 3 questions. No fixed cap; propose the Variant like any Episode;
- the voice: the parent's `voice` by default. Propose another only for a clear reason, and say it.

An example:

> Q&A on Episode 7: When to stop drinking coffee. Questions as I'll say them: does decaf still keep you up; and does a nap cancel out a late coffee. Quick, about 12 minutes, voice bm_george as before. Reply go, or adjust.

## Research

- Start from the parent's ledger. Cite its lines as `{p:cN}`, and don't re-check them.
- Fresh research for each question, with at least 2 new sources per question in this Bundle's own `ledger.md`. `references/accuracy.md` applies unchanged: source ladder, raw-text numbers, claim-check, retraction check.
- Set the Higher-risk flag afresh. A question that moves into riskier ground than the parent flags the Q&A even if the parent wasn't flagged.
- Learnings: read and write the parent's field file(s).

If the research shows the parent was wrong or too strong, the Q&A says so plainly, in the Segment where it comes up: "In episode seven we said X. That was too strong. Here's why." Note it in the show notes and flag it at the top of the final message. Whether to correct the parent is Feedback mode's job, not this run's.

## Shape

The Q&A assumes the listener heard the parent, but restates the point it builds on, so it still makes sense weeks later. This overrides "don't assume they heard earlier Episodes" in `references/template.md`, for Q&A only.

```
## Hook
## 1: <the first question, as a short title>     one per question
## Recap
## Sign-off
```

- **Hook** (about 100 words): the question or questions, and a one-line answer to the main one. No Roadmap.
- **One Segment per question**, in this order: a reminder of what the parent said, in one or two sentences with its `{p:cN}` tag; the answer first; then the deeper material (mechanism, evidence, edge cases); then a "so what". Say each question in its faithful spoken rephrasing, never in quotation marks.
- **One Recall prompt** for the whole Q&A, usually in the Recap: a question, `[think]`, its answer. Content Segments don't each need one.
- **Recap**: short.
- **Sign-off**: points back to the parent by its number.

Lint knows this shape. It warns, without blocking, if a Q&A has no `[think]` or if its content Segments don't match its `questions` one for one.

## Show notes and meta.yaml

- The show notes quote each of the owner's questions word for word, before the key points.
- `meta.yaml`: `parent_episode` is the parent's `episode_id` from `episodes.yaml`; `questions` is the list of the owner's questions in their original wording, only the ones this Q&A answers. Lint blocks a Q&A without them, and blocks `questions` on a Bundle with no `parent_episode`.
- `part: null`. A Q&A is never a Part.
- Title: the Q&A's own subject, like any title. Never "Q&A on" or "Follow-up": the Feed calls it `Episode 7q: <title>`.

## Listener profile

After the Bundle is written, append one observation line under `## Observations` in `config/listener_profile.md`, saying what the questions show about the owner's taste: how much detail they wanted, and where their curiosity went. It goes in the same commit as the Bundle (`git add config/listener_profile.md`). The header gives the line format and the size limit, and how to merge old observations when the profile passes it.

When about 3 observations point the same way, propose a default change at the end of the final message, under **Proposed defaults**, such as "go one level deeper on mechanisms in health Episodes". Never apply it yourself. With the owner's OK, a later run writes it under `## Agreed defaults`.

## Final message

As `SKILL.md` step 7, plus:

- **Parent**: "Q&A on Episode 7: <title>", and the questions as the owner asked them.
- **Errors in the parent**, at the top, when the research found any: what the parent said, what the evidence says, and where the Q&A says so.
- **Listener profile**: the observation you added.
- **Proposed defaults**, only when about 3 observations agree.
