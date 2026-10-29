---
title: Pronunciation lexicon and text normalisation
type: prototype
status: closed
blocked-by: []
claimed-by: owner (this session)
---

## Resolution

Closed 2026-10-29 after a prototype on the 20 worst cases in all five roster voices (`prototypes/pronunciation/`, findings in `research/14-pronunciation-and-text-normalisation.md`). Not yet heard by the owner; the names in cases 16, 19 and 20 need a listen (`prototypes/pronunciation/out/<voice>_before_after_v2.wav`).

- **Spoken form plus a firm lint fixes all the number, unit, time, money and abbreviation cases** in every voice. The lint caught every written-form case and passed the spoken set.
- **Lexicon `config/lexicon.yaml`:** a `verified:` list of capitals words read right as written, and `entries:` of `{term, kokoro, pocket, by, note}`. `kokoro` is `/espeak en-gb phonemes/` or a lower-case respelling; `pocket` is optional text and defaults to the term as written; `note` carries the human version ("owner: KOH-koh-roh"). The Bundle's `pronunciations` uses the same shape and wins for that Episode.
- **One field per engine, because the engines disagree.** Respellings that help Kokoro made Pocket worse ("tsytegayber" came back as "sight agaber"). Pocket reads most terms right as written, and where it needs help, hyphenated chunks of real syllables work (W-H-O, Zeit-gayber).
- **Apply step:** Kokoro phonemizes the whole sentence with a stand-in word for each term, swaps in the entry's phonemes, and calls `create(..., is_phonemes=True)`. Cutting the sentence at a term made a neighbouring "a" read as the letter, and a vowel-final stand-in leaked a linking r. Pocket gets a plain text swap.
- **Lint (firm, TTS safety):** digits, banned symbols, URLs, abbreviations with full stops (including a.m. and p.m.), fillers and stage directions (F5), and capitals words neither verified nor covered by an entry. Text inside an entry is exempt, so CYP1A2 can stay once it has one. Heteronyms only warn. An unknown name can't be linted; the Skill's judgement, the ASR round trip (15) and owner feedback (16) catch those.
- **Who adds entries:** the Skill (Bundle `pronunciations`, plus proposed shared entries in its final message) and the owner through feedback mode, auto-merged. `pron check` shows an entry's phonemes next to espeak's default reading so the Skill can check its own entries.
- **Acronyms in plain capitals, not hyphenated.** espeak en-gb already spells ATP and similar as letters, and Pocket read "A-T-P" as "ITP". The rule "list every acronym in `pronunciations`" goes; the lint guarantees coverage.

Handed on:
- **Ticket 07:** lexicon file and entry shape above; apply step per chunk before `synthesise`; the `pronunciations` field takes the same shape; `pipeline lint` carries the checks above. Port `pron.py` into `pipeline/lib/`.
- **research/05 (style guide):** rule 5 and checklist item 17 change as above; recheck the 6.1 table with `lang="en-gb"`, since some readings there are en-us.
- **Ticket 15:** the ASR round trip is the net for names and for growing the verified list on Pocket; only ATP, REM and CYP1A2 have been checked in Pocket so far.
- **Ticket 16:** an owner remark becomes `{term, kokoro, pocket?, by: owner <date>, note: "<owner's words>"}`.

## Question

How does the Pipeline make sure Kokoro says technical terms, acronyms, names and numbers correctly? Decide: the verified-acronym list, the lexicon format (text respellings, or phonemes substituted before `create(..., is_phonemes=True)`, given that kokoro-onnx has no inline override and misaki's phoneme alphabet differs from espeak-ng's), who adds entries (the Skill via the Bundle's `pronunciations` field, the owner, both), the script lint that rejects digits, symbols and abbreviations before TTS, and how a mispronunciation reported after publishing becomes a lexicon entry. Prototype it on the 20 worst cases from research/03 Amendments item 9.

Context: research/03 Amendments items 1 and 9; research/05 section 6 and checklist items 16-22; ticket 10 (Learnings could hold pronunciation lessons). Covers the map's "pronunciation of technical terms" item. Should block ticket 07. Proposed by the Opus review, 2026-10-29.

## From ticket 09 (2026-10-29)

09 is closed and no longer blocks this ticket. The roster mixes two engines: Kokoro `bm_george` (main, plus `bm_lewis` as backup) and Pocket TTS `charles`, `stuart_bell` and `alba` for some topics. Phoneme entries only work in Kokoro; Pocket takes text, so the lexicon needs a respelling for every entry. Test on the stress lines of `prototypes/voice_audition/audition_script_v2.txt` in each roster voice. If ticket 19 changes the main engine, revisit the format.

## From ticket 07 (2026-10-29)

- 2026-10-29: ticket 07 closed without waiting for this ticket (owner). 07 reserves the lexicon file under `config/`, the Bundle's `pronunciations` field in `meta.yaml`, and a step that applies the lexicon before TTS. This ticket decides the entry format.

## From ticket 16 (2026-10-29)

Mispronunciations the owner reports after publishing arrive through the Skill's feedback mode and become lexicon entries at once (auto-merged). A published Episode is re-rendered for a mispronunciation only if the owner asks (Minor correction tier). The entry format must be writable by the Skill from a one-line owner remark.
