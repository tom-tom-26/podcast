---
title: RSS, GitHub Pages and Apple Podcasts
type: research
status: closed
blocked-by: []
claimed-by: research-agent
---

## Question

What are the exact requirements and limits for a private-ish podcast feed hosted on GitHub Pages and followed in Apple Podcasts on iPhone via "Follow a Show by URL"? Cover required RSS/iTunes tags, audio format and size, GitHub Pages size and bandwidth limits, public-repo requirement, whether Apple Podcasts offline downloads and range requests work from Pages, and how episodes should be named and stored over time.

## Resolution

Closed 2026-10-29. Findings in `research/04-rss-github-pages-apple-podcasts.md` (ends with 11 numbered constraints). Follow-by-URL works on iPhone and does not list the show in Apple's directory; feed must be publicly addressable (obscure, not private). Audio: MP3 or AAC (.m4a recommended), mono 64-128 kbps, about -16 LKFS, ~10-15 MB per 20 min. Artwork 1400-3000 px square, no alpha. Pages limits: 1 GB site, soft 100 GB/month bandwidth, so roughly 70-100 episodes before storage pressure. Pages served HEAD and byte-range requests correctly in a small curl test, but iOS offline download is unverified and needs a real-device check. Gaps: strictly required episode tags, AAC MIME type, feed refresh cadence; validate with Apple's validator at build time.

## Amendments (Opus review, 2026-10-29)

- No factual errors found. Added to research/04: a GitHub Release asset test (302 to a signed URL, HEAD and range work, `octet-stream`; Apple behaviour unverified), Git LFS cannot serve Pages, the obscurity leaks (search indexing, topic history), and show artwork having no owner. Decision unchanged.
