# Backlog and bring back

From ticket 08 and the map's backlog decision. Three summons change a list instead of writing an Episode: "next" takes a Topic from the Topic backlog, "add to backlog: X" adds one, and "bring back episode X" puts an old Episode back in the Window. Read `config/backlog.md`, `pinned.txt` and `episodes.yaml` from `origin/main`.

Never suggest Topics, for the backlog or anything else. A line goes on the backlog only in the owner's words: from "add to backlog", or an unlinked Q&A question the owner said yes to (`references/qa.md`).

## "next"

1. The Topic is the top `- ` line of `config/backlog.md`. If there is none, say the backlog is empty and stop.
2. Run Episode mode from step 1 with that Topic. The confirm message opens with "Next from the backlog: <the line>", and the owner's reply works as for any Topic.
3. At step 6, delete that line from `config/backlog.md` and add the file to the Bundle's commit. Nowhere else: a run that stops before the push, or can't make the Bundle pass lint, leaves the line where it was. Auto-merge refuses a backlog line removed without a new Bundle, or more than one with it.
4. If the rebase stops on a conflict in `config/backlog.md` (the owner edited it meanwhile), take `origin/main`'s version and delete only your line from it. The same goes for `pinned.txt`: take `origin/main`'s and add only your ids.

## "add to backlog: X"

No confirm message. Add each Topic the owner gave as a `- ` line at the bottom of `config/backlog.md`, in their words, trimmed. Skip one already on the list and say so. With nothing new to add, stop without a push.

Alone, it goes on a branch of its own:

```
git checkout -b claude/backlog-<date>-<slug> origin/main
git add config/backlog.md
git commit -m "Add <Topic> to the Topic backlog"
git fetch origin main && git rebase origin/main
git push -u origin claude/backlog-<date>-<slug>
```

Open the PR with `gh api` as in step 6 of `SKILL.md`. Auto-merge merges it and starts nothing. The final message is the line or lines added, the PR link, and how many Topics the backlog now holds.

When it comes with another summon ("caffeine and sleep; add to backlog: how tides work"), add the line in that run's commit instead.

## "bring back episode X"

1. Find the Episode in `episodes.yaml` as Q&A mode finds a parent: by `number` (`7`, `4a`, `7q`) or by title words in its Bundle's `meta.yaml`. Several matches: take the likeliest and name it in the final message; that's cheaper for the owner than a question. No match: say so and stop.
2. Add its `episode_id` (`ep-007-...`) to `pinned.txt`, one line each. For a Part, add the id of every Part of the topic (`ep-004a-...`, `ep-004b-...`), since Parts come and go together; Q&As on it stand alone and are only added when named. Skip ids already pinned. With nothing new to pin, say it's already pinned and stop.
3. Commit "Bring back Episode <number>" on `claude/bring-back-<date>-<number>`, rebase and push as for the backlog, and open the PR. A rebase conflict in `pinned.txt` is resolved as under "next". Auto-merge merges it and starts deploy-site, which puts the audio back in the Feed.

When it comes with another summon, add the ids in that run's commit instead. Publish-episode then starts the deploy.

The final message names each Episode pinned, with its title, the PR link, and that it reaches the app a few minutes after the deploy. Pinned Episodes count against the Window's budget, so add that older unpinned Episodes may drop out of the Feed.
