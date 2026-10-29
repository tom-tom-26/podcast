---
title: Expressive delivery
type: prototype
status: closed
blocked-by: []
claimed-by:
---

## Resolution

Closed 2026-10-29 after one listening round on the [Expressive delivery page](https://claude.ai/artifact/LSLiEtYuZJoodsnjk2yj2R) (owner verdict in its store at `expressive/verdict`).

- **Keep Kokoro `bm_george` with ticket 09's pacing, unchanged.** The owner picked the baseline as the best take, and said none of the alternatives is worth switching to.
- Owner notes per take: bm_fable prosody graft "a bit clearer but the baseline actually sounds more human like" (about the same); am_puck graft "more quietened" (worse); reworded passage "monotone, very script like" (worse); graft plus rewording had "a weird pause in the wrong place" (worse); Chatterbox built-in voice "very robotic" (worse); Pocket stuart_bell at temperature 0.6 worse than the baseline.
- A/B: the 4.5-minute baseline beat the graft; default stress beat edited stress marks.
- **No engine change**, so no third dependency stack. The owner said no to the slow engine split across about 8 runners, and no to another engine copying George's sound from a Kokoro clip.
- **The pitch-spread number doesn't predict what the owner hears as human.** The graft doubled measured pitch movement and still lost. Don't use it as a quality gate (ticket 15).
- **Pushing intonation through wording backfired** in this test ("script like"). Ticket 07 and the research/05 style guide should treat research/18 A8/A10 wording devices as light-touch, not something to stack up for expressiveness.
- Not tried, and parked rather than queued: Pocket with livelier sample clips (needs the owner to accept Kyutai's gated terms on Hugging Face), non-commercial expressive clips, and post-processing pitch shaping. Reopen only if the owner later finds the baseline flat over a full episode (ticket 15's minute-15 listen).

Handed on:
- **Ticket 07:** no longer blocked by 19. Engine and voice as ticket 09; no Script markup for emphasis or mood.
- **Ticket 15:** don't gate on pitch spread; the minute-15 listen of bm_george is where flatness would show.
- **Ticket 14:** stress-mark editing has no audible use for emphasis; phoneme entries are for pronunciation only.

## Question

How do we make the host sound non-monotone, with pitch rising when the content is exciting and dropping for suspense, using only free, open-source TTS that runs on GitHub Actions? The owner, after the voice audition (ticket 09): "being non-monotone is a big big part."

Baseline to beat: Kokoro `bm_george` with ticket 09's pacing (longer chunks, drawn gaps, speed jitter). It stays the main voice unless something clearly sounds better to the owner on the same passage (`prototypes/voice_audition/audition_script_v2.txt`).

## What to try (candidates to check, nothing verified yet)

1. **Kokoro without new tools:** wording that drives intonation (research/18 A8, A10), punctuation choices, chunk length, the order of sentences in a chunk, and editing stress marks in phoneme input (`is_phonemes=True`; research/18 5.1 says it's untested whether Kokoro follows them).
2. **Pocket TTS:** its delivery follows the sample voice clip, so test more expressive CC0 clips for the roster voices, or a different clip of the same speaker. No cloning of a real person without consent (Pocket licence).
3. **Engines with an emotion or expressiveness control:** research which open-source TTS models have one, their licences, whether they run on a CPU Actions runner inside the time limit, and how stable they are over a 25-minute episode. Check names from current sources, not memory.
4. **Post-processing:** pitch shaping per chunk after rendering. Likely to sound fake; test only if 1-3 fail.

## Constraints

- Free: no paid API (owner rejected Polly in ticket 09). Runs on free Actions runners with no PC left on.
- Licence must allow this use, with any credit recorded (candidate firm rule F7).
- The engine stays swappable (map note), and the Script stays engine-neutral: no engine-specific emotion tags in the Script unless ticket 07 adopts a markup for them.
- Judge minutes, not sentences (research/18 5.3), on the audition page. Owner verdict saved as in ticket 09.

## Feeds

Ticket 07 (engine, any Script markup for emphasis or mood, pacing config) is blocked by this ticket. Ticket 14 if the engine changes the lexicon format.

## Progress (2026-10-29): first round ready for the owner

Findings in `research/19-expressive-delivery.md`. **Listen here:** [Expressive delivery](https://claude.ai/artifact/LSLiEtYuZJoodsnjk2yj2R), verdict saved to its store at `expressive/verdict`. The ticket stays open until the owner scores it.

- Best so far [M]: **graft bm_fable's prosody half onto bm_george** (Kokoro only, no new tools). Phrase-level pitch movement goes from ~1.6 to ~3 semitones at the same intelligibility.
- Chatterbox (MIT, emotion knob) moves pitch most, but at RTF ~17 on 4 threads it needs ~8 parallel runners per episode. Only its American built-in voice is rendered; the George-clip and stuart_bell takes still need rendering.
- Dead ends: exaggerating George's own prosody (flatter), stress-mark edits (no effect), Pocket temperature (no gain). Pocket's livelier clips need the owner to accept Kyutai's gated terms on Hugging Face.
- Owner decisions: research/19 "Owner decisions this needs" (5 items).
