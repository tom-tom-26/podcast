---
title: Open-source TTS on GitHub Actions
type: research
status: closed
blocked-by: []
claimed-by: research-agent
---

## Question

Can an open-source neural TTS (e.g. Kokoro, Piper, XTTS, Chatterbox, others current as of today) produce a natural, non-robotic ~20 min single-host episode while running on a free GitHub Actions CPU runner? Compare quality, licence, runtime per episode, long-form stability (chunking, pacing, pauses), markup/SSML support, voices, and Actions minute limits. Give a shortlist and a fallback if none are good enough (cheap API cost per episode).

## Resolution

Closed 2026-10-29. Findings in `research/03-open-source-tts-on-github-actions.md`. Recommended engine Kokoro-82M via kokoro-onnx int8 on CPU (Apache-2.0, 54 voices, stable long-form); shortlist Kyutai Pocket TTS, Chatterbox Nano/Turbo; Piper rejected (most robotic of the set; reason corrected 2026-10-29, see Owner sign-off). Free public-repo runners (4 vCPU, 16 GB, no GPU, 6 h job limit) are enough: estimated 10-25 min render per 20-min episode (desktop proxy, not measured on a runner). Kokoro needs sentence-sized chunks (~150-300 chars), has no SSML so pauses come from punctuation plus inserted silence. *(Corrected 2026-10-29: inline phoneme overrides exist only in hexgrad's `kokoro`/misaki, not in `kokoro-onnx`; see research Amendments.)* Cheap fallback: Amazon Polly Neural/Generative at about $0.29-0.54 per 20-min episode. Quality is unverified: no listening test done, which is the real open risk (see the voice audition ticket). Pocket TTS and NeuTTS licences and Polly SSML support not checked at source.

## Amendments (Opus review, 2026-10-29)

- Corrected the resolution text: kokoro-onnx has no inline phoneme override; fixes need a lexicon or a phoneme-substitution step (research/03 Amendments item 1).
- Added to research/03: Polly free-tier change for new AWS accounts, measured RTF 0.50-0.52 and pace 159-190 wpm, Kokoro voice grades, Pocket TTS licence (CC-BY-4.0, gated), GPL-3.0 dependency inconsistency in the Piper rejection, espeak-ng text-normalisation failures. Decision unchanged.

## Owner sign-off (2026-10-29)

Piper's rejection rests on sound quality (the most robotic of the set), not its licence: the Kokoro stack also depends on GPL-3.0 code, so licence does not separate the candidates. The decision is unchanged.
