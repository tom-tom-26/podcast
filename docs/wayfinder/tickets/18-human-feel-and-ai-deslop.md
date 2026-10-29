---
title: Human feel and AI de-slop across the whole tool
type: research
status: closed
blocked-by: []
claimed-by: research-agent (session 2026-10-29)
---

## Resolution

Closed 2026-10-29. Findings in `research/18-human-feel-and-ai-deslop.md`. The tells are named per layer: content C1-C21, audio A1-A12, interface I1-I10 and build B1-B11, each with a way to detect it and a fix. AI writing tells are measurable but they drift ("delve" fell once it became notorious), so a banned list must be versioned and refreshed. The main fix is upstream: each segment carries a sourced surprise, a concrete case and a judgement the host commits to. Several devices in research/05 produce slop themselves (negative parallelism, the cap of three on lists, fixed lead-ins, identical segment order); the proposed softenings are marked [R] in section 4 and await the owner. Audio: the audition's paragraph gaps are all 0.90-0.93 s. kokoro-onnx 0.6.1 allows only one speed per call, takes phoneme input, and has no timing output or SSML (this corrects research/05 6.1). Soft defaults are sentence gap ~0.38 s, paragraph ~0.75 s, segment 1.3-1.7 s, speed jitter ±0.025 per chunk, and breaths off pending an A/B test in ticket 09. Apple's advice against episode numbers in titles conflicts with ticket 08's `Episode N: Title`; this is flagged for ticket 12. A cheap three-point lint (Skill, pre-TTS, pre-publish) plus a ten-question self-review is in section 9; nothing blocks on style alone. **Signed off 2026-10-29:** F1-F9 are firm (F4 Skill-checked; F6's silence bound replaced by ticket 15's 3 s gate), the F9 core ten block, and the [R] softenings are applied in research/05 12.11 (research/18 8a and 10.1). Gaps: no usable BBC guidance was found, the NPR points are partly secondary, and no study tests AI tells in spoken scripts.

## Question

How do we make every part of the tool feel human, real and very engaging, with no AI "slop" anywhere? The owner rates this as very important (raised during ticket 08, 2026-10-29). Research it thoroughly against primary sources where they exist, and end with a concrete checklist that every later ticket and the build must apply.

Cover all four layers:

- **Content:** scripts and show notes. The known AI-writing tells (stock phrases, hedging, symmetric lists, "let's dive in", summary-for-the-sake-of-it, fake enthusiasm, over-signposting) and how to detect and remove them. Also the human qualities that make spoken explanation gripping: specificity, real stakes, surprise, a point of view, uneven rhythm, natural asides, and earned humour. Check how these fit with the template and rules from tickets 02, 05 and 06, which win where they conflict on accuracy.
- **Audio:** what makes TTS sound robotic (flat prosody, uniform pacing, identical pause lengths, no breaths, mispronounced terms, the same intonation on every sentence) and which of these the pipeline can fix. Candidates: script markup for emphasis and pauses, varied pause lengths, breath insertion, chunking at natural phrase boundaries, sentence-length variety. Feeds ticket 09 (voice choice), ticket 14 (pronunciation) and the script markup in ticket 07.
- **Interface:** feed and episode titles, descriptions, show notes and the archive page. They should read like a person wrote them, not a template.
- **Build:** code, comments, commit messages, logs and docs. Code should read like a careful human wrote it, with no boilerplate comments, no over-abstraction, and no generic names.

Output: a research file `research/18-human-feel-and-ai-deslop.md` with findings, a named list of tells per layer, and a checklist split into firm rules (ask the owner before making any rule firm, per the leniency rule) and soft guidance. It should also include a proposed lint or review step that the skill and the pipeline can run cheaply.

Context: the owner's existing de-slop voice profile for their dissertation (`OneDrive/Desktop/final_project/uni_plan/drafts/voice_profile.md`) may be a useful reference for written tells, but this tool's voice is the podcast host's, not the owner's. Research/02 style rules, research/05 template, research/17 retention techniques.

Blocks ticket 07 (the bundle contract and script markup must carry whatever this finds). Also feeds 09, 12, 14 and 15.

## From ticket 16 (2026-10-29)

The owner can add banned or overused phrases to the versioned phrase list through the Skill's feedback mode; such commits auto-merge.
