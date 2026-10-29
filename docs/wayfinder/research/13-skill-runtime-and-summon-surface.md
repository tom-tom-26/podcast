# Research 13: Skill runtime, summon surface and Claude-side cost

Ticket: `wayfinder/tickets/13-skill-runtime-and-summon-surface.md`. Researched 2026-10-29.
Tags: **[doc]** means a primary Anthropic or GitHub doc states it (linked). **[inference]** is my reading of several docs together. **[estimate]** is unmeasured arithmetic. **[gap]** means no source states it, so it has to be measured.

## 0. Answer in one screen

- **Runtime: a Claude Code cloud session.** It runs on Anthropic's VMs, so no PC is left on. It is started from the **Code tab of the Claude iPhone app** (or claude.ai/code). The Skill lives in the podcast repo at `.claude/skills/`, which cloud sessions load from the clone. Pushes go through Anthropic's GitHub proxy using the Claude GitHub App, so the session holds **no token**. The environment needs **Full** network access, because the default **Trusted** level blocks journals, news sites and PubMed.
- **Fallback: Claude Code GitHub Action** (`anthropics/claude-code-action`). The owner opens an issue from the GitHub iPhone app with the topic. Claude replies with the proposal as a comment, and the owner comments `@claude go`. It runs on Actions runners (free for a public repo), bills to the owner's subscription through a `CLAUDE_CODE_OAUTH_TOKEN` repo secret, and has open internet. It doesn't depend on the cloud-sessions product.
- **Nicer summon screen (nice-to-have): an iOS Shortcut that fires a cloud scheduled task.** One tap or "Hey Siri", type a topic, and the Shortcut POSTs to the task's `/fire` endpoint. The response contains a session URL, which opens in the Claude app, where the proposal appears and the owner replies "go". It costs nothing extra and needs no PC. Its only secret is a token that can fire that one task and nothing else. A web page on GitHub Pages is **not** recommended (section 6).
- **Claude-side cost:** no extra money on Pro or Max. Every path draws on the plan's 5-hour and weekly limits, which Anthropic doesn't publish as token counts. My estimate is a large share of one Pro 5-hour window per Standard episode, and a comfortable fit on Max. **It has to be measured** in a pilot run (section 7).
- **Time per Standard episode:** an estimated 20-45 min from "go" to pushed Bundle, then the audio pipeline's 10-25 min. The owner only spends about a minute on it (topic, then "go").

## 1. The options considered

| # | Runtime | Start from iPhone | PC on? | Repo write | Web research | Verdict |
|---|---|---|---|---|---|---|
| A | Claude Code on the owner's PC | Only through Remote Control or Dispatch, which need the PC on | Yes | Local git credentials | Full | Fails "no PC left running" |
| B | **Claude Code cloud session** (claude.ai/code, Claude app Code tab, `claude --cloud`) | Yes, Code tab | No | GitHub App via proxy, no token in the VM | Full with **Full** network access | **Recommended** |
| C | Cloud scheduled task (formerly routine), API trigger | Yes, Shortcut POST to `/fire` | No | Same as B | Same as B | **Summon layer on top of B** |
| D | Claude Code GitHub Action | Yes, GitHub app issue or comment | No | Claude GitHub App on the runner | Full (runner internet is open) | **Fallback** |
| E | claude.ai chat or Claude app Project with the GitHub integration | Yes | No | No supported write path [inference] | Good web search | Can't push a Bundle, so rejected as runtime |

## 2. Option B: cloud session (recommended)

**Where it runs and what it costs.** "A cloud session is a Claude Code session that runs on cloud infrastructure instead of on your machine… The session keeps running after you close your laptop… It counts toward your plan's usage limits alongside the rest of your Claude and Claude Code usage, and there's no separate charge for the cloud VM." It is available on Pro, Max and Team. [doc: [Use Claude Code in the cloud](https://code.claude.com/docs/en/claude-code-on-the-web)]

**Start from the iPhone.** The Claude iOS app's Code tab is "a client for Claude Code sessions". From it the owner can "select a repository and branch, describe the task, and submit it", then open the session to "check progress, answer Claude's questions, or steer it". Permission modes in the app are Accept edits, Plan and Auto. [doc: [Claude Code on mobile](https://code.claude.com/docs/en/mobile)] That covers the confirm step in research/05 12.4: the Skill posts its one-message proposal and the owner replies "go" in the same session.

**Waiting for "go".** "If Claude asks a question and the session sits idle, you can still answer when you come back, up to environment expiry." After expiry, reopening restores the conversation history on a fresh VM. [doc: cloud page, "Environment expired"] At the confirm step nothing is running in the background, so a late "go" loses nothing. The exact idle expiry time isn't published. **[gap]**

**The Skill gets there by committing it.** Cloud sessions start from a fresh clone, and the repo's `CLAUDE.md`, `.claude/skills/`, `.claude/agents/` and `.claude/settings.json` all load. User-level `~/.claude/skills/` does **not**. [doc: [Configure cloud environments](https://code.claude.com/docs/en/cloud-environments), "What carries over"] Consequence for ticket 07: the Skill, its references (template, source profiles) and the Learnings (ticket 10) all live in the podcast repo.

**Repo write access with no token.** The owner connects GitHub once, either by authorising the Claude GitHub App during web onboarding or with `/web-setup` from a PC. "Your GitHub credentials stay encrypted on Anthropic's servers and never enter a session's VM. GitHub operations from the VM go through the GitHub proxy." [doc: cloud page, "GitHub authentication options"] So the runtime needs no PAT and no repo secret.

**Branch rules (input for ticket 07).** Claude works on `claude/`-prefixed branches by default. For scheduled tasks the docs say it "pushes its work to a branch prefixed with `claude/` unless your prompt directs it to push to another branch", and branch protection is what actually restricts it. [doc: [Scheduled tasks](https://code.claude.com/docs/en/routines), "Repositories and branch permissions"] Ticket 07 picks between:
  1. the Skill pushes the Bundle straight to `main`, which is simplest, or
  2. the Skill pushes a `claude/episode-N` branch and a small Action auto-merges PRs that only touch `bundles/`, which is safer because a bad session can't touch pipeline code.

**Network: the one setting that must change.** Environments have four levels: None, **Trusted** (the default: "package registries, GitHub, cloud SDKs"), **Full** ("Any domain") and Custom. Under Trusted, requests to other hosts "fail with `403` and `x-deny-reason: host_not_allowed`". [doc: cloud environments, "Access levels"; scheduled tasks, "Environments and network access"]
  - **WebSearch** runs on "Anthropic's web search backend". [doc: [Tools reference](https://code.claude.com/docs/en/tools-reference)] So I expect it to work at any level. [inference]
  - **WebFetch and `curl`** run from the VM, so under Trusted they can't reach journals, PubMed, news outlets or government sites. Ticket 06's standard needs those. **Use a dedicated "podcast" environment set to Full.** A Custom allowlist isn't practical for an any-topic show. [inference from the two docs; confirm in the pilot]
  - Every outbound request passes Anthropic's security proxy, which does "rate limiting and abuse prevention". [doc] A few paywalled or bot-blocking sites will refuse it. That happens on any runtime.

**Research quality versus ticket 06.**
  - WebFetch "reads up to 100,000 characters of a page's content per call". It then runs an extraction prompt through a separate small model and returns only that result, which makes it "lossy by design". For the raw page the docs say to use `curl` via Bash. [doc: tools reference] **This bears on ticket 06 recommendation 1 (read depth).** A number taken from a WebFetch summary is effectively summary-depth. For load-bearing numbers the Skill should `curl` the full text, or the PDF through `pdftotext`, and quote the exact sentence into the ledger. With Full network access, the VM can do this. [inference]
  - Interactive sessions are limited to 200 WebSearch calls. [doc] One episode needs roughly 15-40, so the limit doesn't bind. [estimate]
  - Subagents work in cloud sessions [doc: cloud page], so the Skill can fan research out in parallel. That speeds it up but uses more of the plan (section 7).

**VM and time limits.** About 4 vCPU, 16 GB RAM and 30 GB disk. Foreground commands get 2 min by default, up to 10. [doc: cloud environments] The Skill only writes text and calls git, so neither limit matters.

## 3. Option C: scheduled task with an API trigger (summon layer)

A scheduled task saves a prompt, a repository and an environment. One of its trigger types is **API**: "POSTing to the endpoint with the task's bearer token starts a new session and returns a session URL." Available on Pro, Max, Team and Enterprise. Runs "draw down subscription usage the same way interactive sessions do". [doc: [Scheduled tasks](https://code.claude.com/docs/en/routines)]

- **Payload:** the request body carries an optional `text` field. It "arrives wrapped in a `<routine-fire-payload>` block that labels it as untrusted data", so the task's saved prompt has to opt in, for example: "The topic is in the routine-fire-payload block; run the podcast Skill on it." [doc] For this use that's a feature. A leaked token can only suggest a topic. It can't give the agent orders.
- **Token scope:** "Each scheduled task has its own token, scoped to triggering that task only." It can be regenerated or deleted from the web UI. [doc]
- **Limits:** 30 fires an hour per task, with no overage. [doc] That's far above what the show needs.
- **Session behaviour:** a fired run is an ordinary cloud session, so the owner can "continue the conversation manually". Runs start in auto mode. [doc] The confirm step works as in B.
- **Status:** "in research preview", and the `/fire` endpoint sits behind a dated beta header (`experimental-cc-routine-2026-04-01`) that "may change". [doc] So it stays a convenience layer. If it breaks, the owner starts the same session by hand from the Code tab.

**The iOS Shortcut (my design, built from the doc's curl example):**
1. "Ask for Input" (Text): "What should the episode be about?"
2. "Get Contents of URL": POST `https://api.anthropic.com/v1/claude_code/routines/<trig_id>/fire`, with headers `Authorization: Bearer <token>`, `anthropic-beta: experimental-cc-routine-2026-04-01`, `anthropic-version: 2023-06-01` and `Content-Type: application/json`, and JSON body `{"text": <input>}`.
3. "Get Dictionary Value" `claude_code_session_url`, then "Open URLs". The session opens in the Claude app, assuming the app claims claude.ai links (**[gap]**; otherwise it opens in Safari, which also works).
4. Add the Shortcut to the Home Screen with a custom icon and name, or run it with "Hey Siri, new episode".

The token lives inside the Shortcut, which syncs through iCloud. It isn't stored in the repo. Shortcuts doesn't enforce CORS, which a browser page would. [inference]

## 4. Option D: GitHub Action (fallback)

- **Trigger from the iPhone:** "Claude waits for the trigger phrase, `@claude` by default, in an issue or pull request comment… or in the body or title of a newly opened issue". [doc: [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)] The GitHub iPhone app can open issues and comment, and an issue template can prefill `@claude episode:`.
- **Confirm step:** the first run posts the proposal as an issue comment and stops. The owner's `@claude go` starts a second run, which reads the proposal back from the thread. That makes two cold starts, so the proposal comment has to carry everything the second run needs. [inference]
- **Auth:** the `CLAUDE_CODE_OAUTH_TOKEN` repo secret is "an OAuth token that authenticates with your Claude subscription, available on Pro, Max, Team, and Enterprise plans", generated once with `claude setup-token` on a PC. "If you authenticate with an OAuth token, runs use your Claude subscription instead of API billing." [doc] An API key also works but bills per token, which goes against "as cheap as possible".
- **Write access:** the Claude GitHub App needs Contents, Issues and Pull requests read/write. [doc] Only users with write access can trigger runs [doc], so strangers on the public repo can't spend the owner's plan.
- **Web access:** GitHub-hosted runners have open internet [inference; ticket 03 already relies on runners downloading models], so WebSearch, WebFetch and `curl` all work. Tools have to be allowed explicitly in `claude_args --allowedTools` or in the Skill's `allowed-tools` frontmatter. [doc]
- **Runner minutes:** standard runners are free on public repos (ticket 03). A research run takes about 20-45 runner minutes. [estimate]
- **Downsides compared with B:** comments are a poorer conversation surface, each reply costs a cold start, and the long-lived OAuth token sits in a repo secret. It's a sound fallback and a poor primary.

## 5. Option E: claude.ai chat or a Project

A Claude app Project with custom instructions has good web search and is the cheapest front end. But the claude.ai GitHub integration adds repo files as context. It doesn't commit. [inference; no doc states a write path] Pushing a Bundle would need a third-party GitHub MCP connector with a write token, which is more secrets and more fragile than B. **Rejected as runtime.** As a front end it isn't needed, because the Code tab is already in the same app.

## 6. The nicer summon front end (owner's nice-to-have)

| Option | Looks | Cost | Secrets | PC on? | Verdict |
|---|---|---|---|---|---|
| Claude app Code tab (stock) | Stock | 0 | None | No | Baseline, always available |
| Claude app Project with instructions | Stock, but named | 0 | None | No | Can't push (section 5) |
| **iOS Shortcut → `/fire`** | Home-screen icon, Siri, one text box | 0 | Fire token in the Shortcut | No | **Recommended** |
| Web page on GitHub Pages → `/fire` | Fully branded | 0 | Fire token in browser storage on a public site | No | Not recommended: CORS to `api.anthropic.com` is unverified **[gap]**, and the token would sit in a public-site page |
| Home-screen web app (PWA) with own backend | Fully branded, proposal shown in-page | A serverless function plus its upkeep | Fire token, plus a session-read API that doesn't exist publicly **[gap]** | No | Too much build for a nice-to-have |

Being honest about the limit: the proposal and the "go" reply happen inside the Claude app session on every option. A fully branded screen that shows the proposal would need a way to read the session that isn't publicly documented. The Shortcut gives a branded start (icon, name, Siri phrase) and hands over to the Claude app for the conversation. That's the most polish available without building a backend.

## 7. Claude-side cost per episode

**What's documented.** Pro and Max have a rolling 5-hour session limit plus a weekly limit. Claude, Claude Code and cloud sessions share one pool. Max 5x and 20x give 5x and 20x Pro's per-session allowance. Anthropic doubled Claude Code's 5-hour limits on 2026-05-06. Usage "depends on the length and complexity of your conversations, the model you choose, and the features you use", and no token counts are published. Usage credits allow pay-as-you-go beyond the limit, and without them you wait for the reset. [doc: [Usage limits](https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work), [Pro/Max with Claude Code](https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan), [higher limits](https://www.anthropic.com/news/higher-limits-spacex)]

**Estimate for one Standard episode [estimate].** Research is 15-40 searches and 10-25 fetches or curls. Then come Learnings and source-profile reads (ticket 10: keep these small), the ledger, a script of about 3,300-4,400 words with claim tags, show notes, the claim-check and the push. As an agentic session, that's on the order of 1-3 M cumulative input tokens, mostly cache reads, and 40-90 k output tokens. Parallel research subagents push the top of the range up.

What that means for the plan, still an estimate:
- **Pro:** likely a large share of one 5-hour window. One episode a day is plausible. Several back to back may hit the limit.
- **Max:** comfortable.
- **Model choice is the biggest lever.** A cheaper model for search and fetch subagents, with the main model kept for the script and claim-check, should cut usage noticeably without touching accuracy rules.

**Measure it, don't trust the estimate.** Pilot: note Settings → Usage (5-hour and weekly bars) before and after one real Standard episode. Run `/context` and `/cost` (if available in cloud) at the end. Write the result into this file and into ticket 10's read-cost budget. If one episode takes more than about 50% of a Pro window, use the cheaper research model first. Usage credits are the last resort.

**The other costs:** the cloud VM is free [doc]. Actions minutes are free on a public repo. The Shortcut is free. The **only money** in the system remains the plan the owner already pays for.

## 8. What this hands to other tickets

- **07:** the runtime is a cloud session with GitHub access through the Claude GitHub App proxy, so no push token is needed. Choose main-push or a `claude/` branch with auto-merge (section 2). The Skill, its references and Learnings must be committed in the podcast repo. Document the "podcast" environment (Full network). The fallback Action workflow takes topic and "go" from issues. Also the "model refused part of it" note from the ticket 06 review: the session output is where the Skill says what it left out.
- **06:** WebFetch is summarised by a small model. Read-depth "full text" should mean raw text (`curl` or `pdftotext`), not a WebFetch summary. That supports recommendation 1, signed off by the owner on 2026-10-29.
- **10:** Learnings are read from the clone on every run, so the read-cost budget is real plan usage. Size it from the section 7 pilot.
- **15:** the pilot measurements (time, usage) belong in the quality gates too.

## Gaps to close at implementation time

- Confirm in the first real session that WebFetch and `curl` reach journal, PubMed and news hosts under Full, and fail under Trusted.
- Idle expiry time of a cloud session waiting for "go".
- Whether `claude.ai/code/session_…` links open in the Claude iOS app from Shortcuts.
- Measured plan usage and wall-clock time for one Standard episode (section 7 pilot).
- Whether `/cost` works in cloud sessions on a subscription.
- The `/fire` beta header will change. The Shortcut needs updating when it does, and the Code tab is the manual fallback.
