# Research 04: RSS feed on GitHub Pages, followed in Apple Podcasts

Ticket: `wayfinder/tickets/04-rss-github-pages-apple-podcasts.md`. Researched 2026-10-29.
Claims are tagged **[doc]** (stated in a primary doc, linked), **[tested]** (I observed it with curl) or **[gap]** (no primary source states it).

## 1. Following a feed by URL on iPhone

- Path on iOS: Podcasts app, Library, Edit (upper right), add a show by URL, paste the RSS URL, tap Follow. [doc: [Test your podcast RSS feed](https://podcasters.apple.com/support/828-test-your-podcast)]
- The menu label varies by app version ("Add a Show by URL" / "Follow a Show by URL"). Apple's own pages disagree on the label, so the spec should not hard-code it. [doc: same page; label variance reported in search results over [Apple creator docs](https://podcasters.apple.com/support/897-submit-a-show)]
- It does **not** publish the show to the Apple Podcasts directory. Apple frames it as a way to preview artwork and confirm episodes download and stream. [doc: [828](https://podcasters.apple.com/support/828-test-your-podcast)]
- Shows added this way are not in Search, Siri, or recommendations, and are not eligible for editorial featuring. That is fine for a personal feed. [doc: Apple creator docs, as summarised by search; the 828 page confirms the non-publishing part]
- Feed refresh interval after following: **[gap]**. Apple does not document it. The spec should assume refresh is not instant and not controllable.
- "Private" feeds: Apple's requirements page says the feed must be "publicly addressable (not password-protected)". [doc: [Podcast RSS feed requirements](https://podcasters.apple.com/support/823-podcast-requirements)] So the feed is **obscure, not private**. Anyone with the URL can read it. Apple's token-style private RSS URLs apply to subscription shows, which are out of scope.

## 2. RSS requirements

Source: [Podcast RSS feed requirements](https://podcasters.apple.com/support/823-podcast-requirements) and [Validate your podcast RSS feed](https://podcasters.apple.com/support/829-validate-your-podcast), and the [RSS feed sample](https://help.apple.com/itc/podcasts_connect/en.lproj/itcbaf351599.html). Apple's separate "required tags" page (help.apple.com `itcb54353390`) needs JavaScript and could not be fetched. The list below is the union of what the fetchable pages state.

**Feed-level**
- RSS 2.0, publicly addressable, with this declaration: `<?xml version="1.0" encoding="UTF-8"?><rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:content="http://purl.org/rss/1.0/modules/content/">`. [doc: 823]
- At least one episode and show artwork. [doc: 823]
- Hosting must support HTTP HEAD and byte-range requests, for artwork and episodes. [doc: 823, 829]
- UTF-8. Use `&apos;` and `&quot;`, not HTML entities like `&rsquo;`. Escape `&` as `&amp;`. Filenames and URLs ASCII only (a-z, A-Z, 0-9). XML tags are case sensitive. [doc: 823]

**Channel (show) tags the validator checks** [doc: 829]
- `<title>` non-empty.
- `<description>` non-empty.
- `<language>` valid ISO value.
- `<itunes:category>` at least one, exact Apple spelling (e.g. `Society &amp; Culture`). Apple's list: [Apple Podcasts categories](https://podcasters.apple.com/support/1691-apple-podcasts-categories).
- `<itunes:explicit>` with `true` or `false`.
- `<itunes:image href="...">` show cover.
- Appear in Apple's sample and are worth including: `link`, `itunes:author`, `itunes:type`, `copyright`. [doc: sample feed structure]. Whether `link` is mandatory is **[gap]**: 829 does not mention it.

**Item (episode) tags**
- `<enclosure url="..." length="BYTES" type="audio/mpeg">` with all three attributes. Duplicate enclosure URLs are ignored by Apple. [doc: 823]
- `<guid>` globally unique and **never changes**, even if the title or enclosure URL changes. [doc: 823, plus the search summary of the same page]
- `<pubDate>` RFC 2822, 24-hour, with zone offset, e.g. `Wed, 6 Jul 2014 13:00:00 -0700`. [doc: 823]
- `<title>` (or `itunes:title`). [doc: sample]
- In Apple's sample items: `description`, `itunes:duration`, `itunes:explicit`, `itunes:episodeType`, and optionally `itunes:episode`, `itunes:season`, `itunes:image`, `link`. Which of these are strictly required is **[gap]** (blocked by the JS-only required-tags page). Include all of them and treat the sample as the safe superset.
- Validation tools Apple points to: Cast Feed Validator and Podbase Podcast Validator ([sample page](https://help.apple.com/itc/podcasts_connect/en.lproj/itcbaf351599.html)). Apple's own validator flow is described at [829](https://podcasters.apple.com/support/829-validate-your-podcast).

## 3. Audio

Source: [Audio requirements](https://podcasters.apple.com/support/893-audio-requirements).
- RSS feed audio must be **MP3 or AAC**. AAC is "strongly recommended" over MP3 at equal bitrate; use the MP4 (`.m4a`) container, not ADTS, for efficient streaming and accurate seeking.
- Recommended bitrates:

| Channels | 22.05/24 kHz | 44.1/48 kHz |
|---|---|---|
| Mono | 40-80 kbps | 64-128 kbps |
| Stereo | 80-160 kbps | 128-256 kbps |

- Loudness: about -16 LKFS (+/- 1 dB), true peak no higher than -1 dBFS, measured per ITU-R BS.1770-5, applied before encoding. Embed loudness metadata in ID3 or MP4 headers for Sound Check.
- **Maximum file size: not specified** by Apple (checked 893 and 823). Apple only says to compress to the smallest acceptable size. **[gap]**
- Enclosure `type` for `.m4a` is `audio/x-m4a` (Apple's sample uses `audio/mpeg` for MP3); the exact type string for AAC is not on the fetched pages. **[gap]**, verify at implementation.

Sizing for this project (my arithmetic, not a source claim): 20 min of mono speech at 64 kbps is about 9.6 MB; at 96 kbps about 14.4 MB; at 128 kbps about 19.2 MB.

## 4. Artwork

- Show cover: 3000x3000 px ideal; for RSS the accepted range is 1400x1400 to 3000x3000, PNG or JPG, **no alpha channel**. File size and colour space not specified. [doc: [Show cover template](https://podcasters.apple.com/support/5514-show-cover-template); alpha rule also in [Troubleshoot artwork](https://podcasters.apple.com/support/902-troubleshooting-artwork-issues)]
- Artwork must be served from a host supporting HEAD and byte-range requests. [doc: 829]
- Episode art (`itunes:image` on an item) is optional. [doc: [artwork requirements](https://podcasters.apple.com/support/artwork-requirements)]

## 5. GitHub Pages limits and rules

Source: [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits).
- Published site: **1 GB max**. Source repo: 1 GB recommended.
- Bandwidth: **soft 100 GB/month**. Over quota, GitHub may stop serving or suggest a CDN. Rate-limited requests get HTTP 429.
- Builds: soft 10 per hour, which does **not** apply when publishing with a custom GitHub Actions workflow. Deployments time out after 10 minutes.
- Content: not to be used primarily for commercial transactions, e-commerce or commercial SaaS. No sensitive transactions. No explicit rule against audio or streaming is stated; a personal podcast feed is not covered by any listed prohibition.
- **Public repo requirement:** On GitHub Free, "the repository must be public". Private-repo Pages needs a plan that allows it, and the resulting site is **still publicly accessible**. [doc: [Creating a GitHub Pages site](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)] So a public repo is the free path, and the audio and scripts in it are world-readable.
- Publishing: branch/folder (Jekyll by default; add `.nojekyll` to skip it) or a GitHub Actions workflow. Actions deploy uses `actions/configure-pages`, `actions/upload-pages-artifact`, `actions/deploy-pages`, with `pages: write` and `id-token: write` permissions; artifact tar must be under 10 GB and contain no symlinks or hard links. [doc: [Custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)] Standard runners are free for public repos. [doc: creating-a-site page]

## 6. Observed Pages behaviour (curl, 2026-10-29)

Tested against an existing public Pages site (`primer.github.io`), since the docs say nothing about this. **[tested]**
- `HEAD` returns `200`, with `Accept-Ranges: bytes`.
- `Range: bytes=0-99` returns `206 Partial Content` with a correct `Content-Range`.
- Responses carry `Cache-Control: max-age=600` (10 minutes). This is not in GitHub's docs; treat as observed and subject to change. It implies a freshly published feed can be stale for about 10 minutes at the edge.
- A 404 is served as `text/html`; a wrong enclosure URL will fail visibly.
This satisfies Apple's HEAD and byte-range requirement. I did not test with a large audio file or with the iOS client itself.

## 7. Offline downloads from Pages

- Apple Podcasts' offline download is the app's job once it can fetch the enclosure; nothing in Apple's docs ties it to a specific host. The only host-side prerequisites Apple states are HEAD and byte-range support, which Pages passed in section 6. Whether the iOS app downloads or streams a given episode, and its auto-download and retention rules, are **[gap]** (not in the creator docs; they are listener-side settings).
- The "Follow by URL" page lists "episodes download and stream correctly" as the success test, so the spec's acceptance check should be a real follow-and-download on the owner's iPhone.

## 8. Capacity maths (my arithmetic)

- 1 GB site cap at about 14 MB per episode (mono 96 kbps AAC, 20 min) is roughly 70 episodes. At 9.6 MB (64 kbps) roughly 100. Weekly episodes fill the cap in under 2 years.
- Bandwidth 100 GB/month is about 7,000 downloads of a 14 MB episode; a single listener is nowhere near it. Downloads that are repeated (re-downloads, multiple devices) still stay far below.
- Because each Actions deploy publishes the **whole** site, each deploy re-uploads all audio; the artifact must stay under 10 GB and the site under 1 GB.
- Git history keeps every committed binary forever, so repo size (1 GB recommended) grows even if old files are deleted from the tip. Binary audio committed to git is the main long-run risk. Alternative: build the site in the Actions run from a smaller store (for example GitHub Releases assets) so audio is never committed. Not researched here; flag for the architecture ticket.

## 9. Naming and storage over time (design guidance derived from the constraints above)

- Filenames and URLs: ASCII a-z, A-Z, 0-9 only [doc: 823]. Practical form: `episodes/2026-10-29-topic-slug.m4a`, lowercase, hyphens (hyphens are not in Apple's literal a-z/0-9 list, so the safest strictly-compliant form is letters and digits only, or confirm hyphens are fine in the validator; **[gap]** on hyphens and underscores).
- Never rename or move a published file: the enclosure URL and guid identify the episode. Changing the guid makes Apple treat it as a new episode. Changing the URL only is tolerated, but old followers' downloads break.
- guid: use a stable ID (for example the date-slug or a UUID) stored in the bundle and never regenerated.
- `length` must be the real byte size of the final file; compute it from the encoded file, not the pre-encode one.
- Retention: delete old episodes only when approaching the caps, and remove their `<item>` at the same time or the feed will point at 404s. Keep the feed itself small (episodes are text only; feed size limits are **[gap]**, not documented in the pages read).

## 10. Constraints the spec must respect

1. Feed is RSS 2.0 with the exact XML declaration and `itunes` and `content` namespaces, UTF-8, ASCII-only URLs and filenames, escaped `&` and `'`/`"`.
2. Channel must have non-empty `title`, `description`, `language`, at least one valid `itunes:category`, `itunes:explicit` (`true`/`false`), and `itunes:image` (PNG/JPG, 1400-3000 px square, no alpha). Also include `link`, `itunes:author`, `itunes:type`, `copyright` to match Apple's sample.
3. Every item must have `title`, `description`, `enclosure` (url, true byte `length`, `type`), permanent unique `guid`, RFC 2822 `pubDate`, `itunes:duration`, `itunes:explicit`, `itunes:episodeType`. `itunes:episode` and `itunes:season` are omitted (tickets 08 and 12); `itunes:episodeType` is `full`, or `bonus` for Q&A episodes (ticket 12).
4. Enclosure URLs are unique; a guid never changes; published file paths never move.
5. Audio is MP3 or AAC; prefer AAC in an `.m4a` (MP4) container. Mono speech at 64-128 kbps / 44.1-48 kHz; loudness about -16 LKFS, true peak <= -1 dBFS, applied before encoding. Apple sets no max file size. Budget about 10-15 MB per 20 min episode.
6. Host must answer HEAD and range requests (GitHub Pages does, observed). The pipeline's acceptance test should repeat the check against the real enclosure URL.
7. Pages hard and soft limits: site 1 GB, bandwidth 100 GB/month, deploy under 10 min, artifact under 10 GB. The retention policy must keep the whole published site under 1 GB (about 70-100 episodes at the sizes above).
8. Free plan means a public repo and public site. The feed is unlisted but not private: no secrets, no source material the owner wants hidden, and the feed URL is the only "key". Apple requires the feed be publicly addressable, so no auth layer is possible.
9. Publish with a GitHub Actions workflow (exempt from the 10 builds/hour soft limit, handles non-Jekyll output) or a branch with `.nojekyll`. Allow roughly 10 minutes of edge caching (`max-age=600`, observed) before a new episode appears.
10. Following by URL does not list the show in Apple's directory and has no discovery. Acceptance is a real follow, download and offline play on the owner's iPhone.
11. Avoid committing audio to git history unless the size cap is acceptable; decide the storage strategy in the architecture ticket.

## Gaps to close at implementation time
- Apple's required-tags page (`help.apple.com/itc/podcasts_connect/#/itcb54353390`) is JS-only; confirm per-item required tags with Apple's validator or an external one (Cast Feed Validator, Podbase).
- Exact enclosure MIME type for AAC in `.m4a`.
- Whether hyphens and underscores are acceptable in filenames despite the "a-z, A-Z, 0-9" wording.
- Feed refresh cadence in the Podcasts app after Follow by URL, and its auto-download/retention behaviour.
- Feed size limits.
- Large-audio-file range-request behaviour on Pages (only a small file was tested).

## Amendments (Opus review, 2026-10-29)

Reviewer: opus-agent. Index of all review changes: `research/opus-review-2026-10-29.md`. No factual errors found; this file was the most carefully tagged of the set. Additions:

1. *Formats and MIME type.* Apple's [Content setup page (825)](https://podcasters.apple.com/support/825-how-to-create-an-episode) lists M4A, MP3, MOV, MP4 and M4V as supported episode formats for RSS-hosted shows. The `audio/x-m4a` type string is consistent across third-party guides but still not on a fetched Apple page. Re-checked 823 on 2026-10-29: it does not mention file formats, HTTPS, redirects, file size or item-level `itunes:explicit`. Gap narrowed, not closed; the validator settles it.
2. *GitHub Release assets as an enclosure host (input for ticket 08)* [tested, curl, 2026-10-29, on a public release asset of `thewh1teagle/kokoro-onnx`]: the `github.com/.../releases/download/...` URL answers `302` to a signed `release-assets.githubusercontent.com` URL that expires after about an hour; the final URL answers `HEAD` with `200`, `Accept-Ranges: bytes` and the true `Content-Length`, and a `Range` request with `206`. It is served as `application/octet-stream` with `Content-Disposition: attachment`. So the enclosure must be the stable `github.com` URL, never the signed one. Whether Apple Podcasts follows the redirect and accepts `octet-stream` is **[gap]**: add it to the real-device check.
3. *Git LFS.* GitHub's docs (an Enterprise Server page, via search) state Git LFS cannot be used with GitHub Pages sites; branch-published Pages serve the pointer file, not the audio. An Actions-built deploy could fetch LFS objects before uploading the Pages artifact (my inference, untested), but LFS has its own storage and bandwidth quota. Input for ticket 08.
4. *Obscurity has more leaks than the feed URL.* A public repo and Pages site can be indexed by search engines and crawled by podcast indexes, and the repo history shows every topic the owner has asked about (including health interests). Mitigations to consider in the show-identity ticket (proposed 12): no index page linking the feed, a `robots.txt` disallow, and testing whether `<itunes:block>Yes</itunes:block>` still lets Follow-by-URL work **[gap]**. The owner accepted a public repo; this is about knowing what that exposes.
5. *Show artwork is a hard requirement with no owner.* Constraint 2 needs a 1400-3000 px square cover with no alpha channel, but no ticket decides who makes it or how. Added to the proposed show-identity ticket (12).
6. *Item-level `itunes:explicit`.* Constraint 3 lists it as required per item. Apple's fetched pages require it at channel level only; at item level it is harmless to include. No change.
7. *Capacity maths unchanged* by the measured speech rate: file size depends on duration and bitrate, not words.

No change to the closed decision.
