# Feedback mode and Corrections

From ticket 16. The owner is the Feed's only listener, so a Correction exists for the archive and for replays, not to reach an audience. **Firm** marks the rules with no leniency. Everything else is soft (about ±25%).

## The summon

Free text, no ratings or tags: "feedback 7: too long, and it said 'Kokoro' wrong". The Episode is named by number or title words, matched as in "Finding the parent" in `references/qa.md`. Feedback with no Episode ("they've all felt slow lately") applies to the show as a whole. Praise counts as signal: "7 was perfect" is a reaction like any other.

Feedback dropped into an Episode or Q&A summon ("caffeine and sleep; also 7 was too long") is still handled, never turned away: route it as below in the same run, and put any Correction confirm into the run's one confirm message. A Correction that re-renders goes on a branch and PR of its own (see "Push"), since auto-merge refuses a PR that holds a new Bundle and a re-render together.

## Sorting each remark

Split the feedback into remarks, and send each one to the place where it changes future Episodes:

| The remark is about | It goes to | Applies |
|---|---|---|
| Taste: length, depth, pace, Recall prompts, tone, praise | `config/listener_profile.md`, or a Template tunable for an instruction | see below |
| An avoidable mistake the Skill made (an outline that missed the point, a confusing analogy, a promise the Hook didn't keep) | a lesson in the Episode's field file or `learnings/general.md`, `source: owner` (`references/learnings.md`) | at once |
| A word said wrong | a `config/lexicon.yaml` entry, `by: owner <date>` (`references/tts.md`), plus a Minor Correction | at once |
| How a voice fit the Topic | that voice's `suits:` hints in `config/voices.yaml` | at once, Owner-instructed |
| A phrase that grates or is overused | `config/deslop_rules.yaml`, with `version` raised by one: `block:` when the owner bans it outright ("never say X"), `warn:` otherwise | at once |
| A wrong fact, or a claim stated more strongly than its evidence | a Correction (below) | after the confirm, for Harmful and Material |
| Anything you can't place | one Listener profile observation | at once |

A lexicon entry from the owner needs both engines' readings worked out as `references/tts.md` says. The owner's spelling ("KOH-koh-roh") goes in `note`. Never take a phrase off the phrase list or reword one: auto-merge refuses a phrase list that loses a line.

### Instructions and reactions

- **An instruction** ("make them shorter", "use alba for history") is applied at once. Change the tunable in `config/template.yaml` and raise its `style_guide_version` by one, or change `default:` or a voice's `suits:` in `config/voices.yaml`. Name the tunable and its new value in the read-back: "Standard typical 25 -> 22 min". Choose a modest step that fits the owner's words, and keep a typical length inside its Variant's range. An instruction with no number behind it ("more analogies") goes under `## Agreed defaults` in the Listener profile, in the owner's words, since the instruction is their OK.
- **A reaction** ("7 felt long") is one observation line under `## Observations`. Nothing else changes. When about 3 observations point the same way, propose the change under **Proposed defaults** in the final message, such as "Standard typical 25 -> 22 min". Never apply it yourself. With the owner's OK, a later run applies it as an instruction.

When you can't tell which it is, treat it as a reaction and say so in the read-back.

Lexicon entries, owner lessons and phrase-list additions apply at once whichever it is.

### The Listener profile line

`- <date> · feedback on <number>: <what it shows>`, or `feedback on the show` with no Episode. Write what the remark shows about taste, not the remark again: "wanted a shorter Standard; 24 min felt long for a sleep topic". The header in `config/listener_profile.md` gives the size limit and how to merge.

## Corrections

### Grade

Propose a grade; the owner may move it in their reply.

- **Harmful:** a wrong claim that could cause harm if acted on (health, safety, money, law), whether the Episode was flagged Higher-risk or not.
- **Material:** wrong on something central, or a claim much stronger than its evidence.
- **Minor:** a wrong side detail, a slight overstatement, a mispronunciation or one garbled chunk.

### Research the fix

1. Find what the Episode said: the Script sentences and the ledger line their Claim tags point to.
2. Check it as `references/accuracy.md` says, numbers from raw text. If the Episode was right, say so with the source and change nothing.
3. **Episode family.** Read `episodes.yaml` and each listed Bundle's `meta.yaml`. The family is the Episode, its sibling Parts (the same `part.series_slug`) and every Q&A whose `parent_episode` is any of them, and Q&As on those. Grep each one's `ledger.md` and `script.md` for the same claim. Every hit goes into the same confirm, each with its own grade.
4. **The Window.** Episodes outside the Pages Window have no copy on Pages, and leave the Feed unless `repoint` is on in `config/site.yaml`; the Archive page and their Release keep them either way. Start with the newest Episode and every Episode in `pinned.txt`, adding up their `bytes` from `episodes.yaml`. Then add the others newest first until the sum reaches `budget_mb` in `config/site.yaml` (in megabytes of 1,000,000 bytes). The one that crosses the line is still in. A topic's Parts (4a, 4b) always go in or out together, and a pin on one keeps them all. Anything not added is outside.

### Confirm

Harmful and Material need the owner's one-reply confirm. It's the run's one confirm message, so keep it short enough to read on a phone. For each hit it gives what the Episode said, the grade, the new wording and the source:

> Correction for Episode 7: When to stop drinking coffee. It said caffeine's half-life is about 2 hours; it's about 5 (FDA, full text). Grade: Material. New wording: "Half of it is still in you about five hours later." Also in 7q, same claim, Material. Both re-render. Reply go, or adjust.

A Minor show-notes line needs no confirm: write it at once and report it in the final message, offering a re-render. A Minor re-render needs the owner's "go".

### What happens for each grade

| | Show-notes line | Re-render | Spoken line | Lesson |
|---|---|---|---|---|
| Harmful | yes | yes, also outside the Window | yes | yes |
| Material | yes | yes inside the Window; outside it only on request | no | yes |
| Minor | yes | only on "go" | no | only when the same kind recurs |

Every Correction also gets the Archive page line: the Pipeline copies it from the show notes.

### Edit the Bundle

Work on the published Bundle in `bundles/<Bundle id>/`. **Firm:** the edit is minimal.

- **`script.md`**, only for a re-render: change the wrong sentences and their neighbours, nothing else, still in spoken form with Claim tags. A Harmful Correction also puts this line in the Hook, in these exact words, which lint knows: "This version corrects what an earlier one said about <the subject>."
- **`ledger.md`**: fix the line the claim rested on (same id), or add a new line for a new source.
- **`show_notes.md`**: a dated line first, above everything else: "Corrected 2026-11-03: an earlier version said X. That was wrong; Y (source)." For an overstatement, "That was too strong" instead of "That was wrong". One line per Correction, newest first. Fix the wrong text below it too.
- **`meta.yaml`**: append to `corrections:` an entry with `date`, `tier`, `claim` (what was said), `fix` and `source`. Raise `revision` by one only for a re-render. A Minor show-notes-only Correction leaves `revision` and `script.md` alone, because auto-merge refuses a published Script that changes without a bump.

Then `pipeline lint bundles/<Bundle id>`, as step 5 of `SKILL.md`. A firm rule added since the Episode published may now block old text: fix only what blocks, and list it in the final message.

A mispronunciation is a Minor Correction whose fix is the lexicon entry: the show-notes line says the Episode said the word wrong, and a re-render on "go" uses the new entry without editing `script.md`. So that re-render only raises `revision`.

### Lesson

Harmful and Material Corrections write a lesson on how the error got through, such as a number taken from a summary, a tier misjudged or a retraction missed, with **Do instead** naming the check that would have caught it. It goes to the Episode's field file, `source: owner` when the owner reported it, `source: skill` when a Q&A or the overlap check found it. A Minor one writes a lesson only when the field file already has one of the same kind: raise its `seen` instead of adding a line.

## Push

One commit per branch. A feedback run's branch is `claude/feedback-<date>-<number or show>`, from `origin/main` as step 6 of `SKILL.md`. It adds only what the run changed: `config/listener_profile.md`, `config/template.yaml`, `config/voices.yaml`, `config/lexicon.yaml`, `config/deslop_rules.yaml`, `learnings/` and the corrected Bundles.

- **Firm:** a commit that changes `config/template.yaml` or `config/voices.yaml` ends with a trailer quoting the owner's words exactly as they gave them, on one line, before the attribution lines:

  ```
  Owner-instructed: "make them shorter, and use alba for history"
  ```

  Without it auto-merge leaves the PR for the owner. Never add the trailer to a commit the owner didn't instruct, such as a proposed default.
- A Correction that re-renders gets a branch and PR of its own, separate from any new Bundle in the same run. Every Bundle in the family can go on that one branch, since one re-render run takes them all.
- Subject lines: "Log feedback on Episode 7", "Correct Episode 7: caffeine half-life".

Open the PR with `gh api` as in step 6 of `SKILL.md`. Auto-merge then re-renders each Bundle whose `revision` rose, or redeploys the site for a show-notes-only change.

## Final message

Plain text, readable on a phone:

- **Read-back**: one line per remark, saying where it went: "Logged: 7 felt long -> listener profile; 'Kokoro' -> lexicon (KOH-koh-roh); Standard typical 25 -> 22 min (style guide 2)."
- **Corrections**: each one's Episode, grade, what changed and whether it re-renders. For a re-render: "When the new version reaches your Feed, in about 10-25 minutes of render plus up to a day for the app, delete the downloaded Episode and download it again: Apple won't replace a copy you already have." For a show-notes-only line, say that edited notes may not show in the app.
- **Offers**: a Minor re-render, "reply go to re-render".
- **Branch and PR** for each branch, as in step 7 of `SKILL.md`.
- **Learned this run** (`references/learnings.md`) and **Proposed defaults**, when about 3 reactions agree.
