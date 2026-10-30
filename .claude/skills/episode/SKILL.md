---
name: episode
description: Make a Plainly Put Episode. Use when the owner names a Topic to make an Episode about ("caffeine and sleep", "how tides work, deep"). Researches the Topic, writes the Script, Claim ledger and show notes as a Bundle, lints it and pushes it on a claude/ branch for the Pipeline to publish.
---

# Episode

The owner names a Topic from their phone. This Skill turns it into a Bundle on a `claude/` branch; auto-merge and the Pipeline do the rest. Words follow `GLOSSARY.md`.

The owner spends about a minute on an Episode: the Topic, then one reply to the confirm message. Never ask them anything else. When something is unclear after their reply, make the most reasonable call and say what you chose in the final message.

Only Episode mode is built so far. If the owner asks for a Q&A on an Episode, gives feedback (`feedback 7: ...`), says "next", "add to backlog: X" or "bring back episode X", say that mode isn't built yet and stop. Never suggest Topics.

## References

Read each one when its step comes up, not all at the start.

| File | What it holds | Read at |
|---|---|---|
| `references/accuracy.md` | Source ladder, Claim ledger, the firm number and retraction checks, risky topics, the claim-check | step 2, again at step 4 |
| `references/template.md` | Variants, Segments, the host, retrieval design, show notes, metadata | step 1 (Variants), step 3 |
| `references/tts.md` | Spoken form, capitals and the Lexicon, punctuation, markup | step 3 |
| `references/deslop.md` | Firm rules F1-F9, the soft checklist, the ten-question self-review | step 3, again at step 4 |
| `references/learnings.md` | What a lesson is, the line format, Source profile rules, compaction, push conflicts, "Learned this run" | before step 1, again at step 6 |

## Before step 1

1. `pip install -e .` from the repo root, so `pipeline lint` runs.
2. `git fetch origin main` and work from `origin/main`.
3. Read `learnings/INDEX.md`, `learnings/general.md` and the one or two field files the index matches to the Topic (`references/learnings.md`), and follow the lessons that apply. Read `config/listener_profile.md` if it exists. The Listener profile shapes depth and angle; it never overrides the owner's words in this summon.
4. Read `config/voices.yaml` for the roster and each voice's `suits:` hints.

## 1. Confirm

Send exactly one message, then wait. It holds:

- **Variant and length**: "Standard, about 24 minutes". See `references/template.md` for the ranges. Never pad to reach a length; if the honest content is shorter, propose the shorter Variant.
- **Outline**: the content Segments by name, in order, and whether the closing Segment is a Protocol or "Why it matters / what to watch".
- **Voice**: `bm_george` unless another roster voice's `suits:` hints fit the Topic clearly. Name the voice and, if it isn't the default, why in a few words.
- **Drill-down**, only if the Topic is too broad for one Episode: two to four narrower options, one marked as the default. The default is what you write if the reply is "go".
- **Parts**, only if the Topic would run over about 35 minutes and breaks into 2 or 3 subtopics that each stand alone: "2 Parts: X / Y." Never more than 3.

End with "Reply go, or adjust." Keep it short enough to read on a phone. An example:

> Standard, about 24 minutes, voice bm_george. Four Segments: what caffeine does; why it lasts longer than it feels; what it does to the sleep you get; why the same cup hits two people differently. Closing: a Protocol for your last coffee of the day. Reply go, or adjust.

Any angle or hint in the summon is a hint, not a rule. A risky Topic is never refused and never paused on: it gets the Higher-risk flag (step 2), not a question.

The owner's reply is final. A tweak ("make it quick", "drop the genetics one", "option 2") is applied without another confirm. That reply is the only drill-down round.

## 2. Research

Follow `references/accuracy.md`. In short:

- Use the Source profile in the matched field file (the overlap rule applies), or draft one if none fits (`references/learnings.md`), and climb its source ladder. At least 3 distinct sources, aiming for 5.
- Write `ledger.md` as you go, one line per claim. Don't write the Script first and source it afterwards.
- Every number that carries weight is read from raw text (`curl`, `pdftotext`, PubMed's abstract text), never from a WebFetch summary or a search snippet.
- Decide the Higher-risk flag here, from the profile's triggers. When unsure, flag.

Fix the Bundle id now: `<today's date>-<slug>`, the slug a few lower-case words joined by hyphens. Write into `bundles/<Bundle id>/`. For Parts, one Bundle per Part, each with `part: {n, of, series_slug}` and the same `series_slug`.

## 3. Write

Write the Script in spoken form, to `references/template.md`, `references/tts.md` and `references/deslop.md`. Then write `show_notes.md` (written form, exact numbers), `meta.yaml` (fields in `references/template.md`), and `lint_report.yaml` holding just `warnings: []`. Lint blocks a Bundle without that file, and fills it in itself.

Write as you go to the Bundle folder, so a lost session leaves the work on disk. When a stage hits a difficulty worth a lesson, note it then; the lessons are written at step 6.

## 4. Check

In this order, fixing as you go:

1. **Claim-check** the Script against the ledger (`references/accuracy.md`). Don't re-read sources for this, except as the next item says.
2. **Firm number checks**: every spoken number traces to a `full text` line, or an `abstract` line whose abstract states that number. Re-open the source for the two or three `load_bearing` numbers and confirm each one against the raw text; tag those lines `rechecked`.
3. **Retraction check** on every single study a protocol action rests on; tag those lines `retraction_checked`. A retracted study comes out of the Script.
4. **Self-review**: the ten questions in `references/deslop.md`.

## 5. Lint

```
pipeline lint bundles/<Bundle id>
```

It must exit 0. A blocking line is a firm rule: fix the Script, never the rule. Every warning goes into `lint_report.yaml`; fix it, or keep it with a one-line `reason`. A warning on an F1, F2 or F3 phrase (`references/deslop.md`) is a firm rule lint can only warn on: keep it only when the sentence really meets the rule, such as "studies show" with the evidence named and a Claim tag, and say so in the reason. Lint keeps the reasons you gave when you run it again, so run it until it exits 0 and each kept warning has a reason.

If you can't make a Bundle pass, don't push. Say what blocks in the final message.

## 6. Push

One commit holds the whole run: the Bundle (every Part, for a split Topic), this run's Learnings changes, and nothing outside the auto-merge allow-list. A path outside it leaves the PR for the owner.

First write this run's lessons, `seen` raises and any compaction, to `references/learnings.md`. A smooth run changes nothing in `learnings/`.

```
git checkout -b claude/<slug> origin/main
git add bundles/<Bundle id> learnings
git commit -m "Add the <title> Episode"
git fetch origin main && git rebase origin/main
pipeline lint bundles/<Bundle id>
git push -u origin claude/<slug>
```

If the rebase stops on a conflict in `learnings/`, follow "Push conflicts" in `references/learnings.md`. Lint again after the rebase, since the last ten Bundles on `main` may have moved. For Parts, use the `series_slug` for the branch and add every Part's folder.

Then open the PR. `gh pr create` fails in a cloud session, because the GitHub proxy blocks GraphQL; the REST API works:

```
gh api repos/{owner}/{repo}/pulls -f head=claude/<slug> -f base=main -f title="<title>" -f body="<one or two plain sentences: the Topic and the Variant>"
```

If the PR call fails, the branch is still pushed: say so at the top of the final message, with the branch name, so the owner can open the PR from the GitHub app. Without a PR nothing publishes.

Auto-merge takes it from there: lint on the branch, a squash merge, publish-episode, deploy-site. Don't merge it yourself.

## 7. Final message

Plain text, short sections, readable on a phone:

- **Bundle**: `bundles/<Bundle id>` on `claude/<slug>`, and the PR link.
- **Kept warnings**: each one with its reason, or "none".
- **Choices**: any call you made on an unclear reply, any Source profile you drafted, and any firm default (explain first, an analogy per hard concept) you broke, with the reason.
- **Left out**: anything the research found but the Episode doesn't say, and why: too weak to voice, off the outline, a source behind a paywall, or something you would not write. When you wrote a safer version than the Topic asked for, say what you left out and why.
- **Learned this run**: the block in `references/learnings.md`, or "nothing new". Proposed Source profile changes go here too.
- **Proposed additions**: shared Lexicon entries (each `{term, kokoro, pocket?, by: skill <date>, note}`) and phrase-list additions, for the owner to accept. Don't write them to `config/` yourself.
- **ETA**: about 10-25 minutes of render after the merge, Pocket voices slower.

Never give an Episode number: the Pipeline picks it at publish time.
