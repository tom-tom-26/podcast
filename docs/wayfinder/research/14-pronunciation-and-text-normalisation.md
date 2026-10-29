# Research 14: Pronunciation lexicon and text normalisation

Ticket 14. Prototype files are in `prototypes/pronunciation/`: `pron.py` (lint, Kokoro apply step, Pocket respell), `lexicon.yaml` (the proposed `config/lexicon.yaml`, format v2), `bundle_meta.yaml` (a Bundle `pronunciations` example), `raw_cases.txt` and `cases_spoken.txt` (the 20 cases as written and in spoken form), `render_cases.py`, `asr_cases.py`, `pocket_probe.py`. Takes are in `prototypes/pronunciation/out/`; `<voice>_before_after_v2.wav` plays each case as written, then fixed.

Tags as in research/18: [M] measured here, [A] primary source read, [R] my recommendation.

## Bottom line

- **Spoken form does most of the work, and the lint enforces it.** All 20 written-form cases failed somewhere as written. Written in spoken form ("five milligrams", "seven to nine hours", "three in the afternoon"), the number, unit, time, money and abbreviation cases read correctly in all five roster voices [M, faster-whisper transcripts]. The lint caught every written-form case in the raw set (digits, `/ $ &`, `Dr. e.g. vs.`, unverified capitals) and passed the spoken set [M].
- **The lexicon is for what spoken form can't fix:** acronyms espeak misreads (WHO, REM, SSRIs, IVF, ETF, IMF, ECB), names and foreign words (Zeitgeber, Porkka-Heiskanen, Kokoro), heteronyms in context ("read it yesterday"), and a lone letter A, which espeak always turns into a schwa ("Q and A", "CYP1A2") [M].
- **The two engines need different fixes, so each entry has one field per engine.** Kokoro takes phonemes. Pocket takes text. Respellings that help Kokoro made Pocket worse: run-together "tsytegayber" came back as "sight agaber" and "Cy Gay Bear", and "porka hay-ska-nen" as "pork a heist gun" [M]. As written, Pocket read ATP, REM, CYP1A2, Kokoro and 5 mg correctly by itself [M]. Where Pocket did need help, hyphenated chunks of real syllables worked in all three voices: W-H-O, S-S-R-I's, Zeit-gayber, Porka Hayskanen [M].
- **Hyphenated capitals (A-T-P) should no longer be the Script's default.** espeak en-gb already spells ATP, HRV, BDNF and similar as letters, and Pocket charles read "A-T-P" as "ITP" [M]. The Script writes acronyms in plain capitals; the verified list and the lexicon decide how each engine says them.

## Measurements [M]

espeak-ng en-gb phonemes via kokoro-onnx 0.6.1's own tokenizer (`pron.py check`); takes from Kokoro `bm_george` and `bm_lewis` (int8, `lang="en-gb"`) and Pocket TTS 4.0.1 `charles`, `stuart_bell`, `alba` (seed 9); transcripts from faster-whisper `small.en`. Whisper writes numbers as digits and guesses spellings from context, so a transcript shows a reading went wrong more reliably than it proves a reading is right. Names need a listen.

### As written (raw) vs spoken form plus lexicon (fix)

| # | Case as written | Kokoro as written | Pocket as written | Fixed, all 5 voices |
|---|---|---|---|---|
| 1 | 5 mg | "em-gee" | right | right |
| 2 | 1.5 g/kg | "one. five gee slash kay-gee" | "G-KG", "Gg" | right |
| 3 | 7-9 hours | "dash" | "seven nine" in 2 of 3 | right |
| 4 | 3:00 p.m. | "three zero zero pee em" | garbled ("3x", "3's hour") | right |
| 5 | 0.2 s, 150 ms | "zero point two ess", "em-ess" | "millilitres", "millibars" | right |
| 6 | Dr. e.g. vs. | stops read, "ee-gee", "vee-ess" | unclear (ASR echoes the abbreviations) | right |
| 7 | WHO | "who" | "WA" in stuart_bell | right (entry) |
| 8 | ATP | letters, right (en-gb) | right | right |
| 9 | REM | letters "ar-ee-em" | right | right (entry) |
| 10 | SSRIs | "ess-sree" | "SSR is a" in 2 of 3 | right (entry) |
| 11 | $30 | "dollar thirty" | probably right | right |
| 12 | 2x, 10k | "two ex", "ten kay" | "two ex", "ten kay" | right |
| 13 | 1998 | "nineteen hundred ninety eight" | unclear (ASR writes digits) | right |
| 14 | Omega-3s | "omega three z" | right | right |
| 15 | Q&A | "Q and uh" | right | right (entry) |
| 16 | Zeitgeber | "zite-jebber" | "Zitegiver", "Zygiber" | close to TSITE-gay-ber (entry; needs a listen) |
| 17 | read (past) | "reed" | can't tell from ASR | "red" (phrase entry) |
| 18 | CYP1A2 | "sip one A two", A as schwa | right | right (entry) |
| 19 | Porkka-Heiskanen | "high-skay-nen" | garbled | "Porka Hayskanen" (entry; needs a listen) |
| 20 | Kokoro | "kuh-KOR-oh" | right | KOH-koh-roh (entry) |

### What espeak en-gb gets right and wrong with capitals

- Read as letters, correctly: HRV, BDNF, LDL, DNA, UK, NHS, BBC, GDP, ADHD, PTSD, MRI, HIV, CEO, EU, ATP. Read as words, correctly: NASA, NATO, UNESCO, FIFA, NICE.
- Read as one syllable, wrongly: IVF ("ivf"), ETF, IMF, ECB. Read as a word, wrongly: WHO. Read as letters, wrongly: REM. Garbled: SSRIs.
- So en-gb is not the en-us behaviour research/05 section 6.1 recorded for ATP ("as one word"); 6.1 was probed partly in en-us. Recheck the 6.1 table with `lang="en-gb"` when ticket 07 copies it into the style guide.
- A lone capital A is a schwa (ɐ) in every context tried: "Q and A", "C-Y-P-one-A-two", "one A two". "ay" gives "eye". Only a phoneme entry fixes it.

### How the apply step was made to work

- **Splitting the sentence at a term breaks its neighbours.** The first version phonemized the text around each term separately. "and a Q and A" then read "and AY Q and A": a lone "a" at a cut is read as the letter [M]. The working version phonemizes the whole sentence with a stand-in word ("jukebox") in place of each term, then swaps the stand-in's phonemes for the entry's.
- The first stand-in, "zebra", ended in a vowel, and British linking r leaked into the next word ("zebra advises" gave "...ər advises") [M]. The stand-in must end in a consonant.
- Possessives work: "Kokoro's", "the WHO's", "the Zeitgeber's" get z, s or ɪz from the entry's last phoneme [M].
- Phoneme entries go through `create(..., is_phonemes=True)` unchanged, within the 510-phoneme batch limit, which kokoro-onnx splits on its own (research/03 Amendments item 2).

### What the lint catches and what it can't

- Caught (firm): digits, the research/05 banned characters, URLs, abbreviations with full stops (including a.m. and p.m., missed in the first run), fillers and stage directions (F5), and any all-capitals word that is neither on the verified list nor a lexicon or Bundle term. Text covered by an entry is exempt, so CYP1A2 can stay in the Script once it has an entry [M].
- Warned: heteronyms from research/05 rule 7, unless a phrase entry covers them [M].
- **Not catchable by lint:** an unusual word or name with no entry (Zeitgeber, Porkka-Heiskanen). Nothing cheap tells a mispronounced name from a correct one before rendering. The Skill's judgement (research/05 rule 6), the ASR round trip (ticket 15) and the owner's feedback (ticket 16) are the three nets.

## Decisions [R]

1. **Lexicon file `config/lexicon.yaml`**: a `verified:` list of capitals words every roster voice reads right as written, and `entries:` with `term` (as written; whole word, case-sensitive; may be a phrase), `kokoro` (`/espeak en-gb phonemes/` in slashes, or a lower-case respelling espeak reads), `pocket` (optional text; omitted means as written), `by` (skill, owner or review, with a date) and `note` (the human version, such as "owner: KOH-koh-roh", and why). A Bundle's `pronunciations` in `meta.yaml` uses the same entry shape and wins over the shared lexicon for that Episode; it is for one-off terms and context phrases. Recurring terms go to the shared lexicon.
2. **Apply step, before TTS, per chunk.** Kokoro: placeholder phonemization as above, then `is_phonemes=True`. Pocket: plain text swap where `pocket` is set. Any future engine gets a field of its own; an entry with no field for an engine leaves the term as written for it.
3. **Lint (in `pipeline lint`, firm because it protects the TTS):** the checks above. A firm failure blocks auto-merge, but the Skill runs the same lint before pushing and fixes the Script, so this should rarely reach the owner.
4. **Who adds entries:** the Skill, in the Bundle's `pronunciations` and as proposed shared-lexicon additions in its final message (as ticket 07 already has); the owner, through feedback mode (ticket 16), as one-line remarks the Skill turns into an entry with the owner's words in `note`, auto-merged. The Skill writes the `kokoro` phonemes and runs `pron check` to see them next to espeak's default reading; it writes a `pocket` text only for terms that Pocket is known to garble or that are listed as hard (names, foreign words, letter acronyms that read as words).
5. **Style guide changes (research/05 6.2 rule 5, checklist 17):** acronyms in plain capitals, not hyphenated. Each must be on the verified list or have an entry. Drop "list every acronym in `pronunciations`": the lint already guarantees coverage, and repeating verified acronyms per Bundle adds nothing. Keep rule 6 (avoid unusual names; list the ones that stay).
6. **Verified list growth:** an acronym joins it only after `pron check` shows espeak reading it as intended and a roster-voice listen or ASR round trip confirms Pocket. The starter list above was checked in espeak en-gb; in Pocket only ATP, REM and CYP1A2 were checked here. Treat the rest as Kokoro-verified until ticket 15's ASR round trip has seen them in a Pocket render.
7. **Heteronyms stay a warning**, fixed by rephrasing or a phrase entry. Context can't be resolved reliably by a rule.

## Not tried or still open

- The owner hasn't listened. The ASR evidence is strong for numbers and acronyms and weak for names: Zeitgeber, Porkka-Heiskanen and Kokoro need the owner's ear (`out/<voice>_before_after_v2.wav`, cases 16, 19 and 20).
- bm_lewis's "Kokoro" came back as "Cocro" once; the phonemes may need a fuller middle vowel. Only matters if a Script says the engine's name.
- Stress-mark editing for emphasis: settled by ticket 19 (no audible use), so not repeated.
- An auto-verify step that classifies a new capitals word by comparing espeak's reading with its letter-by-letter reading is possible, but it covers Kokoro only, so it was left out.
