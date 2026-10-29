# Research 19: Expressive delivery

Ticket 19. Prototype files are in `prototypes/voice_audition/` (`expr_*.py`, `pitchstats.py`, `asr_check.py`, takes in `expr/`, page in `round4/`). Listening page: [Expressive delivery](https://claude.ai/artifact/LSLiEtYuZJoodsnjk2yj2R), owner verdict saved to its store at `expressive/verdict`.

Tags as in research/18: [M] measured here, [A] primary source read, [S] secondary or search summary, [R] my recommendation.

## Owner verdict (2026-10-29)

The baseline won. No take was worth switching to; the owner said no to cloning and to split renders. Details are in the ticket's Resolution. The analysis below is kept as the record of what was tried.

## Bottom line (before the owner's verdict)

- **Cheapest real gain: graft another Kokoro voice's intonation onto bm_george.** Kokoro's 256-value style vector splits in two: values 0-127 feed the decoder (timbre) and 128-255 feed the prosody predictor (durations, pitch, energy) [A: hexgrad/kokoro `model.py`]. Blending the second half 60% towards bm_fable raised phrase-to-phrase pitch movement from 1.6 to 3.1 semitones on the probe, and from 1.7 to 2.8 over the full 4.5-minute passage, at the same intelligibility [M]. No new engine, no new dependency, same render speed. The voice's median pitch drops ~15 Hz (137 → 122), so it may sound like a slightly deeper George. Only the owner can say whether it still sounds like George.
- **Chatterbox (MIT) is the only tested engine with a real emotion control**, and it moves pitch the most (SD 5.1 st vs George's 2.6) [M]. It is slow: RTF ~17 on 4 threads [M, desktop with 4 threads as a stand-in for a 4-vCPU public-repo runner], so a 25-minute episode is ~7 hours, over the 6-hour job limit [A: GitHub docs]. It only fits if one episode is split across ~8 parallel jobs (free plan allows 20 concurrent) [A]. Only its American built-in voice was rendered; the George-clip and stuart_bell-clip takes were killed twice mid-render and still need doing.
- **Dead ends:** pushing George's own prosody half further from the voice mean makes him *flatter* and slower (SD 2.59 → 2.34 st at ×2.5) [M]. Editing stress marks in phoneme input barely changes the output (duration and pitch extremes within 1-2%) [M]; it's on the page as a 4-second A/B for the owner to confirm by ear.
- **Wording alone helps a little** (SD 2.59 → 2.69 st) [M]. It is free and stacks with the graft, so the research/18 A8/A10 wording rules stay.
- **Pocket TTS:** a higher sampling temperature (0.6) didn't add pitch movement [M]. Livelier clips can't be tested yet: custom-clip cloning needs the gated model, which means the owner accepts Kyutai's terms on Hugging Face and logs in (free, and on Actions an HF token secret).
- Post-processing pitch shaping (candidate 4) was not tried, as the ticket says, because candidate 1 produced a gain.

## Measurements [M]

Pitch spread from `pitchstats.py` (Praat autocorrelation, two-pass speaker-fitted range). It's a ranking aid only. It agrees with ticket 09's ears on the extremes: bf_emma, "too monotonic", is lowest at 2.04 st.

| Take (probe passage, ~1.9 min, unless marked) | SD (st) | 10-90% range (st) | Phrase jump (st) | Notes |
|---|---|---|---|---|
| bm_george baseline (long chunks, drawn gaps, jitter) | 2.59 | 6.51 | 1.60 | WER 0.102 |
| George, prosody ×1.5 / ×2 / ×2.5 from mean | 2.41 / 2.36 / 2.34 | ~6.0 | 1.25 / 1.04 / 0.97 | flatter, slower |
| George, whole vector ×1.5 | 2.49 | 6.28 | 1.25 | |
| George + af_heart prosody 0.5 | 2.76 | 7.16 | 2.39 | median pitch 163 Hz, likely too high |
| George + am_puck prosody 0.5 | 3.21 | 8.32 | 3.05 | WER 0.102; watch for American accent |
| **George + bm_fable prosody 0.6** | **3.30** | **8.85** | **3.11** | WER 0.121 |
| George + af_nicole prosody 0.5 | 2.52 | 6.55 | 1.62 | |
| George, reworded passage | 2.69 | 6.92 | 1.68 | |
| George + bm_fable, reworded | 3.35 | 9.04 | 2.95 | |
| George baseline, full passage (4.5 min) | 2.63 | 6.73 | 1.71 | |
| George + bm_fable, full passage | 3.32 | 8.93 | 2.77 | |
| Chatterbox built-in voice, exag 0.5, cfg 0.5 | 5.13 | 14.15 | 2.97 | RTF 16.9 @ 4 threads; 173 wpm even at the 0.85 stretch floor |
| Pocket stuart_bell, temp 0.6 | 5.10 | 14.21 | 3.84 | RTF 0.52; default temp gave 5.46 |
| Pocket alba, temp 0.6 | 3.46 | 9.19 | 2.87 | |
| Pocket charles, temp 0.6 | 2.22 | 5.37 | 1.87 | |

WER is from faster-whisper `small.en` against the script. ~10% is a floor set by number formatting ("2023" vs "twenty twenty-three", "CYP1A2"), so only differences matter.

## Engines checked on paper (candidate 3)

| Engine | Licence | Expressive control | CPU on a free runner | Verdict |
|---|---|---|---|---|
| Chatterbox (500M) | MIT [A: GitHub] | `exaggeration` (default 0.5; ~0.7+ with `cfg_weight` ~0.3 for dramatic) [A] | RTF ~17 [M] → split over ~8 jobs | Tested; George-clip takes pending. Every output carries Resemble's inaudible Perth watermark [A]. Record that in show notes (F7). |
| Chatterbox Turbo (350M) / Nano (110M) | MIT [A] | Turbo ignores `exaggeration` and has tags like `[laugh]` instead [M: source]; Nano is not in pip 0.1.7 [M] | Nano claimed 3× real time on 8 cores [A] | Tags clash with the engine-neutral Script rule unless 07 adopts markup. Not tested. |
| Zonos v0.1 | Apache 2.0 [A] | 8-way emotion vector, pitch variation, rate [A, S] | "supported but slow", needs a 6 GB+ GPU for normal use [A] | Not tested; likely slower than Chatterbox. |
| IndexTTS-2 | bilibili Model Use License, which defines model *outputs* as derivative works [A: LICENSE.txt] | emotion from a clip or a text description [S] | slow AR model [S] | Rejected: licence and speed. |
| VibeVoice 1.5B | MIT weights, but Microsoft removed the TTS code in Sep 2025 [S] | long-form natural prosody | ~GPU only [S] | Rejected: code pulled for misuse; F7/honesty risk. |
| Fish Audio S2, OmniVoice, XTTS-v2 | non-commercial or restricted [S] | strong | GPU | Rejected on licence (owner could reopen: the show is non-commercial). |
| Dia2 | Apache 2.0 [S] | nonverbal tags, dialogue | unknown | Not tested; tag-based, two-speaker oriented. |

## Owner decisions this needs

1. Which take, if any, beats the baseline (page verdict).
2. Is a George-like voice made by another engine from a Kokoro clip acceptable? It is a synthetic voice, not a real person, so the Pocket "no cloning without consent" rule isn't triggered, but it should be noted.
3. Is splitting each render across ~8 parallel runners acceptable if Chatterbox wins? (This adds complexity to ticket 07's pipeline.)
4. Accept Kyutai's Pocket terms on Hugging Face so livelier Pocket clips can be tried (free).
5. Do CC BY-NC expressive clips (Expresso, EARS) become acceptable, given the show is non-commercial? Ticket 09 said avoid them.

## Still to do in this ticket

- Render Chatterbox with `clips/george_ref.wav` and `clips/stuart_bell.wav` (exag 0.5/cfg 0.5 and 0.8/0.3) and add them to the page: `expr_chatterbox.py REF EXAG CFG`, started as its own background job, since child processes of a finished shell call get killed.
- If the graft wins: tune the blend weight (0.4-0.7) by ear, and record per-voice base speed (graft lands at 0.96-0.98 against George's 1.07).
- A minute-15 listen of the winner on a full Standard episode (ticket 15 already has this).

## Feeds

- **Ticket 07:** if the graft wins, the voice becomes a recipe (`bm_george` timbre + `bm_fable` prosody at w), stored in the pacing config; no Script markup needed. If Chatterbox wins: a third dependency stack, split-render jobs, and a watermark note.
- **Ticket 14:** stress-mark editing is not a route to emphasis; phoneme entries stay for pronunciation only.
- **Ticket 12:** credit lines if Chatterbox (watermark) or a CC BY clip is used.

## Sources

- hexgrad/kokoro `kokoro/model.py` (style vector split), github.com/hexgrad/kokoro
- Chatterbox README and Nano card: github.com/resemble-ai/chatterbox, huggingface.co/ResembleAI/chatterbox-nano
- Zonos README: github.com/Zyphra/Zonos
- IndexTTS-2 licence: huggingface.co/IndexTeam/IndexTTS-2/blob/main/LICENSE.txt
- Kyutai voice catalogue and licences: huggingface.co/kyutai/tts-voices
- GitHub Actions limits and runner specs: docs.github.com/en/actions/reference/limits, docs.github.com/en/actions/reference/runners/github-hosted-runners
- Survey articles (secondary): bentoml.com/blog/exploring-the-world-of-open-source-text-to-speech-models; VibeVoice removal reports, e.g. windowsnews.ai
