---
title: Skill runtime, summon surface and Claude-side cost
type: research
status: closed
blocked-by: []
claimed-by: research-agent (session 2026-10-29)
---

## Resolution

Closed 2026-10-29. Findings in `research/13-skill-runtime-and-summon-surface.md`. Owner sign-off is still needed on the two choices marked ❓ below.

- **Runtime: a Claude Code cloud session.** It runs on Anthropic's VMs, so no PC stays on. It is started from the Code tab of the Claude iPhone app (or claude.ai/code). The Skill is committed in the podcast repo under `.claude/skills/`, which cloud sessions load. The confirm step and "go" happen in the session itself.
- **Repo write:** through the Claude GitHub App and Anthropic's GitHub proxy. There is no token in the session and no repo secret. Ticket 07 chooses between pushing to `main` and a `claude/` branch with auto-merge.
- **Network:** a dedicated environment set to **Full** network access. The default Trusted level blocks journals, news sites and PubMed. WebFetch is summarised by a small model, so numbers that carry weight should be read as raw text (`curl`, `pdftotext`). Input for ticket 06 recommendation 1.
- **Fallback: Claude Code GitHub Action.** The owner opens an issue from the GitHub app, Claude comments the proposal, and the owner replies `@claude go`. It uses a `CLAUDE_CODE_OAUTH_TOKEN` subscription secret and free public-repo runners.
- ❓ **Summon front end (nice-to-have): an iOS Shortcut that fires a cloud scheduled task's API trigger.** One Home-screen tap or Siri phrase, type the topic, and the session opens in the Claude app. It costs nothing, needs no PC, and its only token can fire that one task. The feature is in research preview, and the Code tab is the manual fallback. A GitHub Pages page or PWA is not recommended.
- **Cost:** no money beyond the existing plan (cloud VM, runners and Shortcut are all free). Plan usage is not published as tokens. Estimated at a large share of one Pro 5-hour window per Standard episode, and comfortable on Max. ❓ **A measured pilot is needed:** read the Settings → Usage bars before and after one real episode. If it's heavy, the first lever is a cheaper model for research subagents.
- **Time:** an estimated 20-45 min from "go" to a pushed Bundle, plus 10-25 min of audio render. About one minute of the owner's time.

## Question

Where does the Skill run, and from where does the owner summon it? Options include Claude Code on the owner's PC, Claude Code on the web, and claude.ai or the Claude mobile app with a GitHub connection. For each: can the owner start an episode from an iPhone, does the session have web search and fetch good enough for ticket 06's standard (including reading full-text papers), how does it get write access to the repo (and what secret or token that needs), how long does one Standard episode take, and how much of the owner's Claude plan usage does one episode consume (research plus Script plus claim-check)? Recommend one runtime and a fallback.

Context: the map's constraints ("as cheap as possible, no PC left running"), ticket 06 (research effort), ticket 10 (Learnings read cost). Should block ticket 07, which owns the push mechanics but needs to know where the session runs. Proposed by the Opus review, 2026-10-29: Claude-side cost and the summon surface were in no ticket, and the cost is likely the largest per-episode cost in the system.

## Added from ticket 05 (owner, 2026-10-29)

**Nice-to-have: a nicer summon front end.** The owner would like something better looking than the stock Claude app or CLI: a clean, branded screen to type a topic, see the skill's one-message proposal (research/05 12.4) and reply "go". Not required. Evaluate it alongside the runtime choice. Options range from cheapest to most work:
- a Claude app Project with custom instructions;
- a small web page hosted next to the Feed on GitHub Pages;
- a home-screen web app.

Note the cost, the secrets it would need, and whether it still fits "no PC left running".

## Owner sign-off (2026-10-29)

- The iOS Shortcut summon front end is accepted as an optional extra. The Code tab stays the primary way in, and v1 can ship without the Shortcut.
- The plan-usage pilot runs on the first real Episode as a v1 acceptance step (Settings, Usage, before and after). If usage is heavy, the agreed first lever is a cheaper model for research subagents.
- Summon "next" takes the top topic from `config/backlog.md` (see the map's topic backlog decision); it still goes through the confirm step.
