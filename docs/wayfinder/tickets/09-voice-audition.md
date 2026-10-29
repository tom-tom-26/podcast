---
title: Voice audition
type: prototype
status: closed
blocked-by: []
claimed-by:
---

## Question

Is any open-source voice good enough that the owner would happily listen to it for 20 minutes? Render the same ~2-minute excerpt (written to the host style rules in `research/02-host-format-and-engagement.md`) with several Kokoro voices, Kyutai Pocket TTS, and Amazon Polly Neural/Generative as the paid reference. The owner listens and picks, or rejects open-source and takes the cheap API. Context: `research/03-open-source-tts-on-github-actions.md`. Link the audio samples as assets.

## Resolution

Closed 2026-10-29 after three listening rounds on the [audition page](https://claude.ai/artifact/MdSATNX5Cm8xCtRY4NpZga) (owner verdicts in its store at `audition/verdict` and `audition/verdict3`).

- **Main voice: Kokoro `bm_george`** (UK male). `bm_lewis` (UK male) was also marked main-host quality and is the backup main voice.
- **Shape: one main voice plus others for some topics** (owner's idea). Topic voices: **Pocket TTS `charles`, `stuart_bell` and `alba`**. Which topics each one suits is not yet set (ticket 12 for show identity, ticket 07 for the topic-to-voice map). Owner reference for the quality wanted: Chris Williamson's delivery. It's a reference only, never a clone (Pocket licence bars cloning without consent).
- **Who picks: Claude proposes the voice in the confirm message**, together with length and outline (research/05 12.4), and the owner can change it in the same reply. No extra round trip.
- **Engines: Kokoro and Pocket TTS both in the Pipeline**, since the roster mixes them. Costs carried to 07: two dependency stacks on Actions (Pocket needs PyTorch), Pocket render speed on Actions unmeasured, Pocket seeded for repeatable renders. Licences: Pocket model CC BY 4.0; alba and charles (VCTK) CC BY 4.0, so credit them in show notes or feed; stuart_bell (voice-zero) CC0.
- **Polly: not wanted.** Open-source only, so the cost-cap question (amendment 7) is moot.
- **Pacing (owner A/B, rounds 2 and 3):** varied speed per chunk is in. **Longer chunks beat one sentence per chunk**: up to ~300 characters, several sentences per chunk, so the model owns the short gaps between sentences inside a chunk. Owner: "I don't like the long distinct pauses between sentences." **Gaps between chunks and paragraphs are drawn from distributions, never fixed** ("if they are not varied it's annoying"). This replaces research/18 5.4's "one chunk per sentence" assumption; its pause-class values still apply at chunk, paragraph and segment boundaries. Breaths were not tested and stay off.
- **Pace: keep ~165 wpm** (research/05 section 1, soft). The owner found the voices a touch slow at 1× and 1.25× too fast. Apple Podcasts on iOS 26 has 0.1× speed steps and remembers speed per show ([MacRumors](https://www.macrumors.com/how-to/ios-fine-tune-podcast-playback-speeds/)), so the owner tunes speed in the player. Pocket voices reach the target by WSOLA time-stretch per chunk. The owner heard something wrong with marius at 0.76×, so keep stretches mild (soft floor ~0.85, voices needing more are out).
- **Per-voice base speeds** (Kokoro, at 165 wpm with sentence chunks): bm_george 1.07-1.2 (re-calibrate for long chunks), bm_lewis 1.12. Pocket stretch: charles 0.905, alba 0.907, stuart_bell none. All recorded in `prototypes/voice_audition/settings_v2.json`.
- **Audio quality differences heard between voices are real, not only the test setup.** Pocket copies the recording quality of its sample clip (VCTK clips are older studio recordings), and time-stretching adds artefacts. Test MP3s were ~57 kbps; ticket 08's 64 kbps AAC is close. Ticket 15 should check each roster voice at the final encoding.

Handed on:
- **New ticket 19 (expressive delivery)**, accepted by the owner: "being non-monotone is a big big part", meaning pitch rising with excitement and dropping for suspense. Kokoro has no pitch or emotion control. 19 blocks 07, because it may change the engine for the main voice.
- **Ticket 07:** pacing config (long chunks, drawn gaps, jitter), the roster and topic-to-voice map, two engines, Pocket seeding and stretch, the voice field in the Bundle and in the confirm step.
- **Ticket 14:** lexicon must cover both engines. Phoneme entries work only for Kokoro; Pocket needs respellings.
- **Ticket 12:** which topics each roster voice suits, how the show presents more than one voice, and credit lines for CC BY voices.
- **Ticket 15:** a minute-15 listen of a full Standard episode in bm_george before the first real episode (not done here: auditions were ~4.5 min), and audio-quality checks per roster voice.

## Amendments (Opus review, 2026-10-29)

Reviewer: opus-agent. Review of `prototypes/voice_audition/` as it stands. The ticket stays open with the owner. Index: `research/opus-review-2026-10-29.md`.

**State of the prototype**

- Rendered: six Kokoro voices (af_heart, af_bella, am_michael, am_adam, bf_emma, bm_george), 24 kHz mono 16-bit WAV, about 2 minutes each.
- **Not rendered:** Kyutai Pocket TTS (the `.venv_pocket` environment has torch and other dependencies but no `pocket-tts` package, so the install appears to have stopped) and the Amazon Polly reference (needs an AWS account). The ticket's comparison against a paid reference has not happened.
- Audio is not yet linked as assets, which the ticket asks for.

**Measurements from the renders** [M, details in research/05 section 1]: overall pace 159-190 wpm, quiet share 23-25%, render RTF 0.50-0.52 on the desktop.

**Issues**

1. *Voice selection.* Kokoro's own grades: af_heart A, af_bella A-, bf_emma B-, am_michael C+, bm_george C, **am_adam F+**. Unrendered voices graded as high or higher than some auditioned ones: am_fenrir and am_puck (C+, American male), af_nicole (B-). If the owner wants a male host, render am_fenrir and am_puck before deciding.
2. *The script is too easy to judge a real episode.* `sample_script.txt` has no digits, acronyms, units, technical terms, doses, recall pause or long sentences. Real Scripts will have most of these, so the audition may overrate every voice. Recommend adding a ~45-second stress passage: the example in research/05 section 7.1 with its markup turned into silences, plus one dose sentence and one acronym.
3. *Pause settings are part of what's being judged.* `render_kokoro.py` adds 0.3 s between chunks and 0.8 s after paragraphs on top of kokoro-onnx 0.6.1's own punctuation pauses (0.25 s after sentences, 0.1 s after clauses). Record these settings with the owner's verdict, because ticket 07 will set them.
4. *Pace differs between voices by up to 20%* (bf_emma 190 wpm vs am_michael 159). Judge voices at matched pace, or note which felt rushed; the `speed` parameter can bring a fast voice down to ~165 wpm.
5. *Content caveat.* The sample's claims are unsourced (for example, that a long lie-in two days later doesn't repair a lost night, and the invented Spanish-vocabulary comparison stated as an outcome). Fine for a voice test; do not reuse it as episode content or as a model of the ticket 06 standard.
6. `render_kokoro.py` chooses `en-us` for `a*` voices and `en-gb` otherwise through a convoluted expression. It is correct for the six voices used.
7. *Cost-cap policy* (map "not yet specified") only matters if this ticket picks Polly; decide it here if so.

## Round 2 (2026-10-29): ready for the owner to listen

Prepared by Claude to clear the amendments above. The ticket stays open until the owner gives a verdict.

**Listen here:** [Voice audition, round 2](https://claude.ai/artifact/MdSATNX5Cm8xCtRY4NpZga) (private page; works on iPhone). It plays blind by default and saves the owner's scores to its store at `audition/verdict`, which the next session reads with ArtifactData.

**What changed from round 1** (files in `prototypes/voice_audition/`):

- *Harder passage* (amendment issue 2): `audition_script_v2.txt` is the research/05 7.1 excerpt in full (Hook, Roadmap, Segment 1 with its `[beat]` and `[think]`), plus a ~45 s stress segment with a dose, a decimal, an enzyme code (C-Y-P-one-A-two), an acronym (H-R-V), a Finnish surname and one exclamation. About 4.3 min, 710 words. The stress segment's half-life, smoking and pregnancy lines and the sleep-tracker line are textbook-level and unsourced: audition only, not episode content (same caveat as issue 5).
- *Stacked pauses fixed* (issue 3, research/18 A2): `render_v2.py` renders one sentence per chunk with `trim=True`, and the script adds every gap. Gaps are drawn from the research/18 section 5.4 distributions, seeded (seed 9), so re-renders are identical. Speed jitter ±0.025 with a 0.04 step cap, and ×0.95 on sentences with number words. 8 ms fades at chunk edges.
- *Matched pace* (issue 4): each Kokoro voice is calibrated to ~165 wpm overall (base speed clamped to 0.8-1.2).
- *More voices* (issue 1): added am_fenrir, am_puck and af_nicole; dropped am_adam (F+).
- *Pocket TTS rendered*: install finished (`pocket-tts` 4.0.1 in `.venv_pocket`, plus `soundfile`). Voices alba, marius and javert. It has no speed control, so pace isn't matched. It's fast on CPU (RTF ~0.3 against Kokoro's ~0.5 at sentence-per-chunk; desktop numbers, not Actions). Output is stochastic: no seed, so a re-render differs.
- *A/B on af_heart* (research/18 5.6 items 2-4): fixed round-1 pacing vs varied; speed jitter off vs on; very short sentences paired vs alone.
- *Assets linked* (ticket ask): MP3s published with the page. Local WAV and MP3 copies are in `round2/`.

**Measured** [M, `settings_v2.json`]:

| Take | wpm | Base speed | Length |
|---|---|---|---|
| Kokoro af_heart | 163 | 1.014 | 4:21 |
| Kokoro af_bella | 162 | 1.037 | 4:23 |
| Kokoro af_nicole | **129** | 1.2 (cap) | 5:29 |
| Kokoro bf_emma | 164 | 0.984 | 4:19 |
| Kokoro am_michael | 157 | 1.149 | 4:32 |
| Kokoro am_fenrir | 163 | 0.999 | 4:20 |
| Kokoro am_puck | 162 | 1.028 | 4:22 |
| Kokoro bm_george | 157 | 1.198 | 4:31 |
| Pocket alba | 178 | n/a | 3:59 |
| Pocket marius | **207** | n/a | 3:26 |
| Pocket javert | 148 | n/a | 4:48 |

af_nicole stays slow even at the speed cap. Pocket marius is a fast speaker (~260 wpm while talking); a per-sentence check found no dropped passages, though one short line may be clipped. Pace for Kokoro isn't linear in `speed`, so two voices landed at 157; inside the ±25% soft range.

**Not done (owner action needed):**

- *Amazon Polly reference*: needs an AWS account. The page asks whether the owner wants it before deciding.
- *Breath A/B* (research/18 5.5): skipped. It waits on research/18 owner question 3, and there's no CC0 or self-recorded breath set yet (candidate firm rule F7).
- *Minute-15 fatigue listen* (research/18 5.6 item 6): the passage is 4-5 min. If a voice survives, render a full Standard episode in that voice before signing off.

**Settings to carry into ticket 07 with the verdict** (issue 3): sentence-per-chunk, `trim=True`, pause classes and clip ranges as research/18 5.4, seed per Episode, jitter ±0.025, key-info ×0.95, bounds 0.90-1.10 × base, per-voice base speed as in the table.

## Round 2 verdict (owner, 2026-10-29, read from the page's store)

- No voice is a "yes". Maybes: **Kokoro bm_george** ("I like this"), **Pocket marius** (preferred over af_heart, but too fast), **Pocket alba** (would be nice if more British).
- Nos: af_heart ("too robotic"), af_bella, am_michael, am_puck, am_fenrir ("sounds like a TikTok AI voice"), bf_emma ("too monotonic"), Pocket javert ("too groggy"), af_nicole (too ASMR for most content, "but mysteries would be cool").
- Polly: not wanted; decide from open-source voices.
- **Accent: owner prefers a non-American accent.** Reference for a good podcast voice: Chris Williamson (Modern Wisdom). A reference for the quality we're after only: we do not clone or imitate a real person's voice (honesty rule; candidate firm rule F7 territory).
- A/B: **varied speed preferred** (jitter on). **Every sentence alone preferred** over pairing short sentences. **Round-1 pacing preferred** over the new varied pauses. That last result is confounded: round-1 also used longer chunks (up to 300 characters), so it may be the chunking, not the fixed gaps. Round 3 separates them on bm_george (`fixed` vs `longvaried`: same long chunks, fixed vs drawn gaps).

### New idea from the owner: a roster of voices, chosen per topic

The owner asks whether episodes could use different voices, because some voices suit some subjects (for example a soft voice for mysteries).

Feasibility [M/R]: **feasible and cheap.** The voice is one Pipeline setting per Episode; all Kokoro voices sit in one `voices-v1.0.bin`; Pocket voices are a short reference clip each. What it costs:

1. *Vetting per voice*: each roster voice needs its own audition, base speed, and pronunciation check. Soft roster size: about 2-4 voices (±25%, owner to confirm).
2. *Two engines, if the roster mixes Kokoro and Pocket*: two dependency stacks on Actions (Pocket needs PyTorch, a much larger install; cacheable). Pocket's render speed on Actions runners is unmeasured.
3. *Pronunciation (ticket 14)*: phoneme-level lexicon entries only work for Kokoro (`is_phonemes=True`); Pocket takes text only, so it needs respellings. The lexicon must hold both forms, or the roster stays on one engine.
4. *Pocket specifics*: no speed control (round 3 tests WSOLA time-stretch to ~165 wpm); output is stochastic unless seeded (round 3 seeds torch). Licences checked 2026-10-29 [A: huggingface.co/kyutai/pocket-tts and /kyutai/tts-voices]: model **CC BY 4.0**, which bars cloning a voice without explicit consent; alba and VCTK voices **CC BY 4.0** (credit in show notes or feed); voice-donations (marius, javert) and voice-zero **CC0**; expresso (cosette) and EARS (jean) **CC BY-NC 4.0**, so avoid them. The package code is MIT.
5. *Show identity (ticket 12)*: one feed can carry several voices, but the show's feel changes from episode to episode. Option: one main host plus "guest voices" for given topic types.
6. *Selection*: fits the existing confirm step (research/05 12.4). The Skill proposes length, outline **and voice** in one message, from a topic-to-voice default map, and the owner can override in the same reply. No extra round trip.

Owner decisions this needs (not yet asked formally): one main voice or an equal roster; who picks (Skill proposes, owner overrides in the confirm reply, is the recommendation); whether mixing engines is acceptable.

### Round 3 (ready for the owner, 2026-10-29)

British-accent candidates: Pocket charles, paul, anna, vera, fantine (VCTK speakers, believed English accents, unverified), peter_yearsley, stuart_bell, caro_davy, bill_boerst (accents unknown); Kokoro bm_fable, bm_lewis, bm_daniel, bf_isabella (Kokoro grades C, D+, D, C). Pocket marius and alba re-rendered, time-stretched to ~165 wpm. Pocket now seeded. Pacing A/B on bm_george as above.

Round 3 is on the same page (version 3) and saves to `audition/verdict3`; round 2's verdict stays at `audition/verdict`. Each voice is scored Main host / Some topics / No, with a "which topics" note. The verdict asks one voice vs main-plus-others vs roster, and who picks per episode. All Pocket takes land at 158-169 wpm (WSOLA stretch 0.76-0.98, none for stuart_bell and caro_davy); Kokoro British voices at 156-161 wpm. Accents of the voice-zero speakers are unconfirmed; VCTK accents are from memory of the corpus notes, so the page doesn't claim them. Pacing pairs on bm_george: long chunks with fixed vs varied gaps, and sentence-per-chunk vs long chunks (both with varied gaps).
