# Learnings

From ticket 10. **Firm** marks the rules with no leniency. Everything else is soft (about ±25%).

A lesson is a mistake or difficulty this run hit, written with what to do instead, so a later run doesn't repeat it or spend tokens finding it out again. It is never a fact about a Topic, and never generic advice you would follow anyway.

## Layout

- `learnings/INDEX.md`: each field file and its Topic keywords.
- `learnings/general.md`: lessons that hold in every field.
- `learnings/fields/<field>.md`: one per field. Frontmatter `status: settled` or `draft`, the Source profile on top, then `## Lessons`.

## Reading

Every run reads `INDEX.md`, `general.md` and the one or two field files the index matches to the Topic (two when it overlaps, as sport training uses Sport and Health). That is about 3-5k tokens. Don't read the other field files.

Follow each lesson that applies. Note the ones that helped again, and any that turned out wrong or unnecessary.

## What counts

A difficulty in a stage this Skill runs: confirm, research, write, check, lint or push. For example a search dead end, a host that times out, a source whose number didn't match its abstract, a lint rule you tripped twice, a rebase that went wrong. In a field file, also outlets found wrong and access difficulties with that field's sources.

Not lessons, so never written here:

- Facts about the Topic.
- A pronunciation rule: propose a Lexicon entry instead. A lesson may say "proposed X for the Lexicon".
- An AI-tell phrase: propose a phrase-list addition instead.
- The owner's taste (length, depth, pace): that goes to the Listener profile or the Template tunables.
- Pipeline or Actions failures after the session ends: those open a Failure issue.

## A lesson line

One line, appended under `## Lessons` of the field file it belongs to, or of `general.md` when it holds in every field:

```
- `<date> · <Bundle id> · stage: <stage>` **What happened:** ... **Do instead:** ... **Saves:** ... `seen: 1` `source: skill`
```

- **Do instead** is always something to do, not a warning.
- **Saves** is optional: what following it saves, such as "~4 fetches".
- Use the Bundle id, because the Episode id doesn't exist until the Pipeline publishes.
- `source: owner` marks a lesson the owner gave. Feedback mode writes those; a normal run writes `source: skill`.

An example:

```
- `2026-11-03 · 2026-11-03-creatine-and-memory · stage: research` **What happened:** PubMed full-text links timed out three times. **Do instead:** go straight to the PMC mirror URL. **Saves:** ~4 fetches. `seen: 1` `source: skill`
```

## Writing

- **A smooth run writes nothing.** There is no minimum.
- About 3 new lessons per run at most. Keep the ones that would have saved the most.
- Learnings changes go in the same commit as the Bundle (SKILL.md step 6).
- When a lesson helped again, raise its `seen` by one. Keep its date.
- When a lesson you followed turned out wrong or unnecessary, rewrite or delete it in this run. **Firm:** never a `source: owner` lesson; propose the change in the final message instead.

### Naming outlets

**Firm:** name an outlet only for a concrete error you observed, written as a fact with the Bundle id: "misstated n in 2026-11-03-creatine-and-memory". Never a verdict, and never for its reputation or political lean.

After about 3 logged errors by one outlet in one field, add it to that field's **Watch for** as context only: "<outlet>: context only (3 logged errors)". From then on it never counts as evidence in that field.

## Source profiles

**Firm:**

- You may append to a profile's **Watch for**, and you may add a stricter **Higher-risk flag when** trigger on your own.
- Changing **Strongest evidence**, or removing or loosening any Higher-risk trigger, is only a proposal in the final message. The owner makes it.

### A new field

When no field file fits the Topic, draft a profile during research, with the same three bullets, and use it:

- Its **Higher-risk flag when** are the strictest neighbouring profile's triggers, plus any of its own. Beekeeping borrows Health's.
- Save it as `learnings/fields/<field>.md` with `status: draft` and `drafted: <Bundle id>` in the frontmatter, the Apple categories line if one fits, and an empty `## Lessons`.
- Add its row to `INDEX.md` with keywords.

A later run in that field that needed no change to the draft makes it `settled`: change the status and say so in "Learned this run". The owner's OK settles it too. Settling never loosens the borrowed triggers; that stays a proposal.

## Compaction

A file over its size is compacted in the same run: `INDEX.md` at about 300 tokens, `general.md` and each field file at about 1,500. With `wc -w`, that is about 220 and 1,100 words.

- Merge duplicates into one line, adding their `seen` counts.
- Drop dead lessons: about a host or tool that no longer behaves that way, or no longer needed.
- Then drop lessons older than about 12 months with `seen: 1`, oldest first.
- **Firm:** never remove or merge away a `source: owner` lesson. Only the owner removes those.
- Never delete a file; auto-merge refuses a deleted path.
- Compaction is the only rewrite of Learnings. Skip it in any run that meets a conflict at push.

## Push conflicts

Learnings lines are append-only, so parallel sessions can each add theirs. If the rebase in step 6 stops on a conflict in a `learnings/` file:

```
git checkout origin/main -- <file>
```

Then re-append this run's own lines to that file (new lessons, a new field file's INDEX row), redo any `seen` raise on top of main's version, drop this run's compaction of it, `git add` it and `git rebase --continue`. Say in "Learned this run" that compaction was skipped.

## Learned this run

Every final message has this block. List each change, one line each, with its file:

```
Learned this run:
- added (fields/health.md): PubMed full-text links time out; use the PMC mirror
- seen 2 (general.md): numbers only from full text or abstract
- drafted fields/beekeeping.md (triggers borrowed from Health)
- compacted fields/health.md: merged 2 duplicates
- proposed: loosen Leisure's "outdoor activities" trigger to ..., because ...
```

Or, for a smooth run, `Learned this run: nothing new.`
