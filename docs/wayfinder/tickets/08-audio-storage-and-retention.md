---
title: Audio storage and retention
type: grilling
status: closed
blocked-by: []
claimed-by: owner (this session)
---

## Question

Committing audio to git grows the repo permanently, and every Pages deploy re-uploads the whole site, against a 1 GB site cap (about 70-100 episodes). Where do episode audio files live (in the repo, GitHub Releases, a separate store), and what is the retention policy when the cap approaches (archive, prune oldest, lower bitrate)? Context: see `research/04-rss-github-pages-apple-podcasts.md`.

## Resolution

Closed 2026-10-29. Decided with the owner:

- **Architecture: hybrid (option C).** Audio never goes in git. Each episode's `.m4a` is uploaded as a GitHub Release file, which is the permanent archive (no total size or bandwidth limit; under 2 GiB per file, checked on docs.github.com 2026-10-29). At deploy time, Actions downloads the episodes in the window into the Pages site, and the feed points at those Pages URLs, which already serve HEAD and range requests and the correct MIME type.
- **Layout:** one Release per episode. Show notes go in the release text.
- **Encoding:** mono AAC in `.m4a`, 44.1 kHz, 64 kbps soft default (~12 MB per 25 min). Ticket 09 may raise it if 64 sounds worse on the iPhone. Published files are never re-encoded to save space.
- **What is kept:** every Bundle is committed to git permanently. No WAV masters; any episode can be re-rendered from its Bundle.
- **Public archive is accepted.** It adds no exposure beyond the public feed agreed in 04.
- **Window:** the Pages site holds the newest episodes up to about **600 MB of audio (soft, ±25%)**. **Firm ceiling: the site never exceeds ~900 MB.** A deploy that would go over is refused. The owner approved this as a firm limit.
- **Leaving the window:** by default the feed item is removed at the same time (no 404s) and the audio stays in Releases. **If the Apple Release-URL test passes, switch to keeping the item and repointing its enclosure to the stable `github.com/.../releases/download/...` URL** (never the signed one). The owner asked firmly for this switch, so every episode stays in the app.
- **Restoring:** an archive page on Pages lists every episode with show notes and a Release download link. A pin list (`pinned.txt`) keeps chosen episodes in the window, counted against the budget. "Bring back episode X" from the skill adds the ID and pushes.
- **Naming (owner):** the listener sees `Episode 1: Why bridges sway?`. Numbers start at 1, count up in publish order and are never reused. **Parts of a split topic share the number with a letter: `Episode 4a: ...`, `Episode 4b: ...`.** Internal names follow the number: Release tag and file `ep-001-why-bridges-sway(.m4a)`, `ep-004a-...`. Because Parts are not integers and the number is already in the title, `itunes:episode` is **omitted**. This also avoids Apple showing the number twice. The owner's title format overrides Apple's advice to keep numbers out of titles; nothing enforces that advice for a feed followed by URL.
- **Parts move together:** a split topic is archived or restored as a group (soft budget absorbs the overshoot).
- **Published audio is never overwritten in place.** A corrected episode gets a new file (`-v2`); its guid is unchanged. When and how corrections happen is ticket 16.
- **Storage failure rules (firm):** a new file is uploaded and its byte size checked against the encoded file **before** the feed is touched. If a deploy cannot fetch any file in the window, it fails loudly and Pages keeps serving the last good site. Never publish a feed item whose audio is unverified; never exceed the ceiling. Soft: every deploy logs site size, and over budget it warns and drops the oldest unpinned episodes.

Handed on:
- **Real-device check (ticket 15):** (1) a throwaway test feed whose enclosure is a Release URL. Does Apple follow the 302, accept `application/octet-stream`, seek and download offline? A pass turns on the repoint rule above. (2) Check how `Episode N: Title` displays.
- **Ticket 12:** episode numbering and Part labels are settled here. Q&A episode labelling, seasons and `itunes:type` stay with 12.
- **Ticket 07:** pipeline order (upload, verify, deploy), repo layout, `pinned.txt` and archive page generation.
- **New ticket 18** (human feel and AI de-slop across content, audio, interface and build) was raised by the owner here and now blocks 07.

## Notes

- 2026-10-29: ticket 12 closed. Q&A episodes extend this numbering: parent number plus a letter from `q` (`7q`, `7r`; `4q` for a split topic), Episode id `ep-007q-<slug>`.
