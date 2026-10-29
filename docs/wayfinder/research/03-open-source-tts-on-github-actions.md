# Research 03: Open-source TTS on GitHub Actions

Date: 2026-10-29. Ticket: `tickets/03-open-source-tts-on-github-actions.md`.
Confidence tags: [P] = read on a primary source (repo, model card, official docs); [M] = my own throwaway measurement; [S] = secondary (blog, aggregator), treat as hearsay; [U] = unverified, from memory.

## Short answer

Yes for "runs free on Actions". Probably yes for "good enough", but no primary source can settle quality. **Kokoro-82M** is the only engine that is Apache-2.0, CPU-practical, fixed-voice (stable across a whole episode) and has a mature toolchain. Expect "clean audiobook narrator", not "expressive podcast host". A listening test of a 2-3 minute sample is the one remaining check before committing. Keep the engine swappable and the cheap-API fallback ready (about $0.30 to $0.55 per episode).

## 1. GitHub Actions constraints

- Standard runners in **public repos are free and do not use up the included allowance**. [P] https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-actions/about-billing-for-github-actions
- Public-repo `ubuntu-latest` (x64) and `ubuntu-24.04-arm`: **4 vCPU, 16 GB RAM, 14 GB SSD**. No GPU on standard runners (GPU runners are larger-runner only, Team/Enterprise plans). [P] https://docs.github.com/en/actions/reference/runners/github-hosted-runners
- Job limit **6 hours**; workflow run 35 days; artifacts 500 MB on the Free plan (shared with Packages); cache 10 GB per repo; 20 concurrent jobs on Free. [P] https://docs.github.com/en/actions/reference/limits and the billing page above.
- Private-repo fallback: Free plan gets $12/month of compute (about 2,000 min of 2-core Linux). Not needed if the repo is public. [P] billing page.
- Implication: a 20-min episode only fails the job limit at a real-time factor (RTF) above about 18. Any engine under RTF 1 is comfortably inside limits. Budget is a non-issue; quality is the constraint. 4 vCPU / 16 GB rules out 1B+ parameter GPU models.
- GitHub could change free-for-public terms, hence "engine and runner swappable".

## 2. Candidate engines

| Engine | Licence | Size | CPU on 4 vCPU? | Voices | Markup | Verdict |
|---|---|---|---|---|---|---|
| **Kokoro-82M** | Apache-2.0 (weights and `kokoro`); `kokoro-onnx` MIT [P]; both depend on GPL-3.0 espeak-ng (see Amendments) | 82M | Yes. [M] RTF about 0.36-0.52 (section 3, Amendments) | v1.0: 54 voices, 8 languages incl. American and British English [P]; few English voices are high grade (Amendments) | No SSML. Inline `[word](/phonemes/)` respelling exists only in hexgrad's `kokoro` package (misaki G2P), **not in `kokoro-onnx`** [P, corrected 2026-10-29] | **Recommended** |
| Chatterbox Nano / Turbo | MIT [P] | Nano 110M, Turbo 350M, original 500M | Nano targets CPU, "3x realtime on 8 cores" (vendor claim) [P]; others GPU-oriented | Voice cloning from a short sample | Paralinguistic tags (laugh, cough) on Turbo/Nano; Perth watermark on all output [P] | Shortlist (secondary). Nano quality unverified; one third-party test reported garbled output for the main model [S] |
| Kyutai Pocket TTS | Code MIT; weight licence is listed per voice on HF, not confirmed [P] | about 100M (small variants 1.9-18M) | Yes. 6x realtime on 2 cores of an M4 (vendor) [P] | 26 preset voices, mostly English; cloning from WAV; 7 languages [P] | None documented | Shortlist. "Infinitely long text" claim [P] is attractive; weight licence and naturalness need checking |
| Piper (OHF `piper1-gpl`) | **GPL-3.0**; maintainers wanted [P] | VITS, small | Very fast | Many voices | Limited | Rejected: the most robotic of the set [S] (reason corrected 2026-10-29, owner sign-off: licence does not separate the candidates, see Amendments item 5) |
| Supertonic 3 | Code MIT, model OpenRAIL-M [P] | 99M, ONNX | Yes ("fast on CPU"; RTF 0.3 on an e-reader) [P] | Preset styles, 31 languages, inline tags like `<breath>` [P] | Expression tags | **Repo archived**: "No updates, bug fixes, security patches" [P]. Usable but frozen; not a base |
| NeuTTS Air / Nano | Air Apache-2.0; Nano/2E "NeuTTS Open License 1.0" (terms not read) [P] | 120-360M active | Yes via GGUF Q4 [P] | Cloning from 3 s audio (Air/Nano) | None | Context is 2048 tokens, about 30 s per call [P], so chunking is needed and cloned voices can drift between chunks. Reserve |
| Qwen3-TTS 0.6B/1.7B | Apache-2.0 [P] | 0.6-1.7B | Examples are CUDA only; CPU not addressed [P] | 9 premium voices, VoiceDesign, cloning [P] | Natural-language style control | Promising quality, but likely several times slower than realtime on 4 CPUs (untested). Watch list |
| Orpheus 3B, Dia, F5, Fish Speech | various | 1-3B | GPU needed [S] | | | Out: do not fit a CPU runner. Not re-verified at source |
| XTTS-v2 (Coqui) | Coqui Public Model Licence, non-commercial; Coqui shut down [U] | 0.5B+ | Slow on CPU | Cloning | None | Out on licence and maintenance grounds [U] |

Independent quality ranking: I could not obtain a current TTS Arena or Artificial Analysis leaderboard (the TTS Arena space did not render under fetch). Secondary roundups consistently call Kokoro the best CPU-only quality/accuracy option and say the larger cloning models need a GPU [S]: https://picovoice.ai/blog/on-device-tts/ (vendor-run, biased), https://pinggy.io/blog/best_open_source_self_hosted_text_to_speech_models/. Directional only.

Sources: Kokoro https://huggingface.co/hexgrad/Kokoro-82M and https://github.com/hexgrad/kokoro; ONNX port https://github.com/thewh1teagle/kokoro-onnx; Chatterbox https://github.com/resemble-ai/chatterbox; Pocket TTS https://github.com/kyutai-labs/pocket-tts; Piper https://github.com/OHF-Voice/piper1-gpl; Supertonic https://github.com/supertone-inc/supertonic; NeuTTS https://github.com/neuphonic/neutts; Qwen3-TTS https://github.com/QwenLM/Qwen3-TTS.

## 3. Runtime per 20-min episode (Kokoro)

Throwaway check [M]: `kokoro-onnx`, int8 model (92 MB) plus voices file (28 MB), voice `af_heart`, CPU only, on my 16-thread Windows desktop:
- Default threads: 66.6 s of audio generated in 28.3 s (RTF 0.43).
- `intra_op_num_threads=4`: 46.1 s of audio in 16.5 s (RTF 0.36).

Extrapolation for 20 min of audio: about 7-9 min on this desktop at 4 threads. A shared Actions vCPU is likely slower, so plan on **roughly 10-25 min per episode** including install and the roughly 120 MB model download (cacheable with Actions cache). Free on a public repo. Caveats: one machine, one voice, int8 only (fp32 not tested), short run.

Secondary data point: a Reddit-linked benchmark reports Kokoro PyTorch RTF around 0.43 on its hardware [S].

## 4. Long-form stability, pacing, markup

- Kokoro handles at most 510 phoneme tokens per call (about one to three sentences, roughly 30 s of audio); the reference code truncates or errors beyond that. [S] https://code.amethyst.name/public-mirrors/Kokoro-FastAPI/raw/commit/7f15ba8fed1d69b4902f390bcead918bf8742960/README.md . The official `kokoro` package splits text via `split_pattern` [P]. In my run, `kokoro-onnx` accepted a 1,068-char paragraph and returned one continuous clip [M].
- Each chunk resets prosody at its boundary. A fixed voicepack means the voice itself does not drift between chunks, an advantage over cloning engines (NeuTTS, Chatterbox, Pocket TTS clone mode).
- Pacing and pauses: no SSML. Practical approach: the pipeline splits the script into sentences, synthesises each, and inserts **explicit silence** (for example 250 ms between sentences, 600-900 ms between paragraphs, longer at section breaks) when concatenating. Speed parameter is available [M].
- "Rushed" artifacts appear near the 510-token ceiling [S]; keep chunks around 150-300 characters.
- Pronunciation of technical terms: hexgrad's `kokoro` package accepts inline `[term](/phonemes/)` overrides through its misaki G2P [P]. The recommended `kokoro-onnx` runtime does not: it phonemizes with espeak-ng and would need the pipeline to substitute phonemes itself and call `create(..., is_phonemes=True)`, or a text-level respelling lexicon [P: installed kokoro-onnx 0.6.1 source; corrected 2026-10-29]. Either way, a pre-processing dictionary in the pipeline (acronyms, units, numbers) is needed.
- Expressiveness: flatter than a human host. Paralinguistic tags exist only on Chatterbox Turbo/Nano and Supertonic [P] and add little to a single-host educational show.

## 5. Voices

Kokoro v1.0: 54 voices across 8 languages [P]; `af_heart` is the voice in the project's own examples [P]. Other English voices (`bf_*`, `am_*`, `bm_*`) exist per its VOICES.md (not opened). For a male read, audition the `am_*` and `bm_*` voices. Voice selection is already an open item on the map; this ticket only needs "enough options exist".

## 6. Cheap-API fallback: cost per roughly 20-min episode

Assumption: 150 wpm, so 3,000 words, about 18,000 characters, about 20 min audio.

| Service | Price (source) | Per 20-min episode |
|---|---|---|
| Amazon Polly Standard | $4.00/1M chars; 5M chars/month free [P] https://aws.amazon.com/polly/pricing/ | $0.07 (free within allowance) |
| Amazon Polly Neural | $16/1M; 1M chars/month free for first 12 months on accounts created before 15 July 2025; newer accounts get credits instead (Amendments) [P] | $0.29 (about $0.30 at measured pace) |
| Amazon Polly Generative | $30/1M; 100k chars/month free for 12 months, same caveat [P] | $0.54 (about $0.57 at measured pace) |
| Google Cloud Chirp 3 HD | $30/1M [S, official page snippets] https://cloud.google.com/text-to-speech/pricing | $0.54 (1M free chars/month reported [S]; verify) |
| Google Cloud Neural2 / WaveNet | $16/1M; Standard $4/1M [S] | $0.29 |
| OpenAI gpt-4o-mini-tts | $0.60/1M text tokens plus $12/1M audio tokens [P], about $0.015/min [S]; 2,000-token input cap [P]; model page marks it deprecated https://developers.openai.com/api/docs/models/gpt-4o-mini-tts | about $0.30; needs chunking |
| ElevenLabs API | $0.04/1k chars (Flash/Turbo), $0.08/1k (v2/v3/v4) [P] https://elevenlabs.io/pricing/api | $0.72 / $1.44 |

OpenAI's pricing page returned 403 and Google's did not render prices in fetch, so those figures are not first-party confirmed. Polly and ElevenLabs are first-party.

## 7. Shortlist, recommendation, fallback

**Shortlist (in order):**
1. Kokoro-82M via `kokoro-onnx` (int8, CPU).
2. Kyutai Pocket TTS (check weight licence and sample quality; strongest long-text claim).
3. Chatterbox Nano/Turbo (MIT; only if Kokoro sounds too flat; Perth watermark noted).
Watch: Qwen3-TTS 0.6B (if a CPU benchmark appears), NeuTTS.

**Recommended engine: Kokoro-82M.** Apache-2.0, fits 4 vCPU / 16 GB easily, RTF about 0.4 so roughly 10-25 min of Actions time per episode at zero cost on a public repo, stable fixed voices, pronunciation override, no GPU. The pipeline should own chunking (sentence level, 150-300 chars) and silence insertion, behind a small "synthesise(text, voice) to wav" interface so the engine can be swapped.

**Cheap-API fallback:** Amazon Polly Neural or Generative, **$0.29-0.54 per 20-min episode** (often $0 inside free tiers). Premium upgrade: ElevenLabs at $0.72-1.44 per episode.

## 8. Open items and unverified points

- No blind listening comparison done. Cheapest next step: render the same 2-minute excerpt with 2-3 Kokoro voices, Pocket TTS and Polly Neural, and let the owner pick.
- Actions-runner RTF not measured on a real runner (my figure is a desktop proxy).
- Pocket TTS weight licence, NeuTTS Open License 1.0 terms, first-party Google/OpenAI prices, Polly SSML support and XTTS/Orpheus status were not verified at source.
- Kokoro's 510-token limit comes from third-party code and README, not the official model card. *(Now confirmed in kokoro-onnx 0.6.1 source: `MAX_PHONEME_LENGTH = 510`, with automatic splitting. 2026-10-29.)*

## Amendments (Opus review, 2026-10-29)

Reviewer: opus-agent. Index of all review changes: `research/opus-review-2026-10-29.md`. Evidence for items 1-4 and 8 is the `kokoro-onnx` 0.6.1 package installed in `prototypes/voice_audition/.venv` (read directly; it is primary for the version the prototype used) and phonemizer runs in that venv [M].

**Corrections made in the text above**

1. *Pronunciation override (factual error).* The file said Kokoro has "inline phoneme overrides" and listed `[word](/phonemes/)` as the engine's markup. That syntax belongs to **misaki**, the G2P inside hexgrad's PyTorch `kokoro` package. The recommended runtime, `kokoro-onnx`, phonemizes with espeak-ng through the `phonemizer` package and contains no parser for it. Overrides with kokoro-onnx need either a text respelling lexicon or the pipeline producing phonemes itself and passing `is_phonemes=True`. misaki and espeak-ng also use different phoneme alphabets, so a lexicon written for one does not port to the other. Corrected in the table, section 4 and ticket 03's resolution. This affects tickets 07 and the proposed pronunciation ticket 14.
2. *510-token limit.* Now confirmed at source: `MAX_PHONEME_LENGTH = 510` in kokoro-onnx, which splits long input into balanced batches at sentence, then clause, then word boundaries, so it does not error on long text.
3. *Polly free tier.* AWS replaced the 12-month free tier for accounts created after 15 July 2025 with up to $200 of credits and a 6-month free plan ([AWS announcement](https://aws.amazon.com/about-aws/whats-new/2025/07/aws-free-tier-credits-month-free-plan/); [Polly pricing](https://aws.amazon.com/polly/pricing/), checked 2026-10-29). Per-character prices are unchanged and confirmed: Standard $4, Neural $16, Generative $30, Long-Form $100 per million characters. A new account cannot count on "free for about 55 episodes a month in year 1".

**Things the file missed or got thin**

4. *Pausing is richer than "no SSML, so explicit silence".* kokoro-onnx 0.6.1 `create()` has `sentence_pause` (default 0.25 s, after `. ! ? …`), `clause_pause` (0.1 s, after `, ; :`), trims silence at batch edges, uses the model's phoneme durations to top up gaps after punctuation, and has `continuous=True` (overlapping windows that keep prosody across joins, at about 1.4x compute). The prototype added its own 0.3 s / 0.8 s silences on top of these defaults, so the owner's audition hears stacked pauses. Ticket 07 should decide which layer owns which pause. Pin the kokoro-onnx version: 0.6.1 behaves differently from the versions most third-party write-ups describe.
5. *Licence reasoning is inconsistent.* Piper was "rejected: GPL-3 is awkward", but the recommended stack also depends on GPL-3.0 code: `phonemizer` declares GPL-3.0 in its installed metadata, and espeak-ng is GPL-3.0; hexgrad's `kokoro` uses espeak-ng as its out-of-vocabulary fallback. For a personal tool that runs in CI and is not distributed as software, GPL obligations are not triggered by running it (my reading, not legal advice), so licence does not separate the candidates. Piper's rejection should rest on quality ([S] reports it as the most robotic). Recommendation only; the decision is unchanged.
6. *Voice quality grades.* Kokoro's own [VOICES.md](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md) grades voices by training data. Only af_heart (A) and af_bella (A-) are A-grade, both American female. Best British: bf_emma (B-). Best American male: am_fenrir, am_michael, am_puck (C+). bm_george C, am_adam F+. "54 voices" overstates usable choice: if the owner wants a male host, the quality ceiling is lower. Relevant to ticket 09, which auditioned am_adam (F+) but not am_fenrir, am_puck or af_nicole (B-).
7. *Pocket TTS licence, now checked.* The [Hugging Face model card](https://huggingface.co/kyutai/pocket-tts) lists CC-BY-4.0, gated access (accept terms with a Hugging Face account), 26 voices (21 English), per-voice licences in `kyutai/tts-voices`. Using it in Actions needs a Hugging Face token secret and attribution in the show or feed.
8. *Measured render speed and pace.* The prototype rendered six voices at RTF 0.50-0.52 (default threads, same desktop), slower than the 0.36-0.43 quoted here. A 20-minute episode is about 10 minutes of desktop compute; the 10-25 minute runner estimate stands but is still unmeasured on a runner. Measured pace was 159-190 wpm, so a 20-minute Script is about 3,300 words and 19,000 characters (5.6 characters per word in the sample), not 3,000 words and 18,000 characters. Polly costs scale accordingly (about $0.30 Neural, $0.57 Generative).
9. *Text normalisation was not examined.* espeak-ng mishandles many written forms common in health scripts [M]: "5 mg" → "five em-gee"; "1.5" → "one. five" (the decimal point becomes a sentence break and gets a pause); "7-9" → "seven dash nine"; "3:00 p.m." garbled; "Dr.", "e.g.", "vs." read with full stops; "WHO" → "who"; "ATP" read as a word in some contexts; "REM" mis-read; "$30" → "dollar thirty"; "1998" → "nineteen hundred ninety eight"; heteronyms like past-tense "read" wrong. Writing the Script in spoken form avoids most of it (ticket 05 section 6); the rest needs a lexicon and a lint (proposed tickets 14 and 15).
10. *Long-form stability is asserted, not tested.* No full 20-minute render has been made. Fixed voicepacks prevent voice drift, but kokoro-onnx selects the style vector by batch length (`voice[len(tokens) - 1]`), which is one reason it balances batch sizes. Worth one full-length test render before the spec is final.
11. *ASR round-trip check missing from the stability plan.* A cheap CPU speech-to-text pass over the rendered audio, compared with the Script, would catch garbled or truncated chunks automatically. Suggested for the testing ticket (15), not verified here.

No change to the closed decision (Kokoro via kokoro-onnx on free runners, Polly fallback). Item 1 changes how pronunciation fixes will be built, not the engine choice.
