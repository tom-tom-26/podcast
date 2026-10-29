---
title: Show identity and feed metadata
type: grilling
status: closed
blocked-by: []
claimed-by: owner (this session)
---

## Question

What is the show itself: its title, description, author, Apple category, language, explicit flag and cover artwork (1400-3000 px square, no alpha; who makes it, and how, at no cost)? How are Episodes titled and numbered in the Feed (`itunes:episode`, `itunes:season`, `itunes:type` episodic or serial, how Parts of a split topic and Q&A episodes are labelled and ordered)? Is there audio branding (an intro or outro sting, music and its licence, any standing show line) or none? What does the public repo and Pages site expose, and which obscurity measures are worth it (no index page, `robots.txt`, whether `itunes:block` still allows Follow-by-URL)?

Context: research/04 constraints 2-3 and its Opus amendments 4-5; research/05 sections 3.4, 6.4 and owner questions 6 and 8. Absorbs the map's "series/ordering ... numbered or themed" and "intro/outro, music" items. Proposed by the Opus review, 2026-10-29: Apple requires artwork, and no ticket owned it.

## Resolution

Closed 2026-10-29. Decided with the owner (three grilling rounds, Q1-Q18):

- **Show:** *Plainly Put*. `itunes:author` is the show name; no `itunes:owner` email; `copyright` reads `© 2026 Plainly Put`. Nothing in the Feed names the owner.
- **Channel fields** (`config/show.yaml`): `language` `en-GB`; one category, `Education`; `itunes:explicit` `false`; `itunes:type` `episodic`; no seasons; `link` is the archive page.
- **Channel description** (the only place show-level text lives, research/18 I6):
  > One topic per episode, anything from bridge engineering to sleep, explained plainly in about twenty-five minutes. Claude researches and writes each episode from a handful of sources, all listed in the show notes, and a synthetic voice reads it. Where the evidence is thin, the episode says so.
- **AI disclosure:** stated once, in the channel description above. Nothing about voices or AI is said in the audio.
- **Artwork:** typographic, drawn as code. An SVG in the repo is rendered by a small script to a 3000x3000 RGB PNG with no alpha. Deep ink-blue background, cream serif "Plainly Put" (free OFL font, licence file committed) and one thin rule under it; nothing else. The owner approves the PNG before it is committed. The Pipeline checks size, squareness and no alpha before publishing. No per-episode art.
- **Audio branding:** none in v1. Episodes open on the hook and end on the sign-off. The Pipeline keeps a hook for a sting of at most ~5 s (CC0 or self-made, licence recorded per F7), to be A/B tested later like breaths. No music under speech.
- **Standing show line:** none (research/05 12.9 stands). **Host stays unnamed.**
- **Voice credits:** CC BY voices (Pocket `alba`, `charles`) get one plain line at the end of the show notes, e.g. `Voice: alba, Kyutai Pocket TTS voices, CC BY 4.0 (link)`, appended from `voices.yaml`. Kokoro voices and CC0 voices (`stuart_bell`) carry no credit line.
- **`suits:` in `voices.yaml`:** light hints only. `bm_george` is the default for everything; the other roster voices carry a word or two each, filled in from the owner's reactions to real episodes (via ticket 16). The Skill still proposes the voice in the confirm step.
- **Q&A labelling** (default, assuming Q&A episodes share the Feed; ticket 11 may override if it moves them elsewhere): a Q&A takes its parent's number plus a letter from `q`: `Episode 7q`, then `7r`, `7s` ... `7z`, then `7z2` (a safety rule only; the owner expects it never to be needed). Parts use only `a`-`c`, so the ranges never collide. A Q&A on one Part attaches to the topic number (`Episode 4q`); its title names the Part if needed, and `parent_episode` in `meta.yaml` points at the exact Part. Titles carry no "follow-up" wording (the `q` says it), e.g. `Episode 7q: Do longer bridges sway more?`. Feed: `itunes:episodeType` `bonus`, `pubDate` is the real publish date. Episode id `ep-007q-<slug>`; the registry's `number` field is text.
- **Obscurity:** `<itunes:block>Yes</itunes:block>` and `<podcast:block>yes</podcast:block>` in the channel; `robots.txt` with `Disallow: /`; archive page carries `noindex` and is linked only from the Feed's `link`; the README never links the Feed. The owner accepts that the public repo history shows every topic asked about. Evidence that block still allows Follow-by-URL: Apple says followers get a show directly from the hosting provider ([Apple 5108](https://podcasters.apple.com/support/5108-how-apple-podcasts-distributes-your-shows-to-listeners)), and private-feed hosts pair the block tag with Follow-by-URL ([Acast](https://learn.acast.com/en/articles/4619103-hiding-your-show-itunes-block-tags), [Hello Audio](https://help.helloaudio.fm/en/articles/12261382-how-do-i-use-apple-podcasts-to-listen-to-private-podcasts)). One 2019 report of a blocked feed failing Apple validation ([Apple Community](https://discussions.apple.com/thread/250474156)) is old and anecdotal; the device test settles it.
- **Archive page:** one sentence at the top, *"Every episode of Plainly Put so far, newest first."*, then a plain generated list (title, date, one-line summary, duration, link), per research/18 I9.

Handed on:
- **Ticket 11:** the Q&A labelling default above; 11 owns whether Q&A episodes share the Feed.
- **Ticket 15:** the first-episode iPhone check adds "feed with block tags still follows by URL and validates"; the Pipeline's artwork check (size, square, no alpha).
- **Ticket 16:** owner reactions feed the `suits:` hints.
- **Tickets 07 and 08:** Q&A Episode ids (`ep-007q-...`) extend 08's numbering; `episodes.yaml` `number` is text; `config/show.yaml` now has its contents.

## Notes

- Settled in ticket 08 (owner, 2026-10-29): titles read `Episode N: Title`, numbered from 1 in publish order and never reused; Parts share a number with a letter (`Episode 4a`, `4b`); `itunes:episode` is omitted. Still open here: Q&A episode labelling, seasons, `itunes:type`.
- 2026-10-29: ticket 07 closed. Channel metadata and artwork path go in `config/show.yaml`; which topics each voice suits goes in the `suits:` field of `config/voices.yaml`; CC BY credit lines are appended from `voices.yaml` automatically, so 12 sets their wording.
