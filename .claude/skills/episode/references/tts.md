# Writing for TTS

From research/05 section 6 as ticket 14 changed it, and research/14. The engines read the Script literally: Kokoro through espeak-ng's en-gb front end, Pocket through its own. `pipeline lint` blocks every mechanical case below, so these rules mostly save you a lint round.

## Spoken form (firm)

Write everything exactly as it should be said. No digits anywhere in spoken text.

| Don't write | Write |
|---|---|
| 5 mg | five milligrams |
| 1.5 g/kg | one point five grams per kilogram |
| 7-9 hours | seven to nine hours |
| 3:00 p.m. | three in the afternoon |
| 150 ms | a hundred and fifty milliseconds |
| $30 | thirty dollars |
| 2x, 10k | twice, ten thousand |
| 1998 | nineteen ninety-eight |
| 50% | fifty percent, or half |
| omega-3s | omega-threes |
| Q&A | Q and A |

- Round for the ear unless the action depends on the exact value: "about a third", not "thirty-four point two percent". Doses and timings stay exact, are said once in their Segment, and come back in the Recap.
- Metric units, said in full, with an everyday translation for a dose: "about three milligrams for every kilogram you weigh. For most people that's two cups of coffee."
- No abbreviations with full stops: write "for example", "versus", "Doctor", "and so on". No a.m. or p.m.
- No URLs.

## Capitals and the Lexicon

- An all-capitals word must be on the `verified:` list in `config/lexicon.yaml` or have a Lexicon entry, or lint blocks it. Write acronyms in plain capitals, not hyphenated: espeak already spells most of them as letters.
- Prefer the full name the first time: "the World Health Organization".
- An unusual word or name (a foreign term, a drug, a researcher, rare anatomy): leave it out if the idea survives without it. If it stays, give it a Bundle entry. At most one researcher name per Segment; "a twenty twenty-three review of twenty-four studies" carries more than a surname the listener can't spell.
- A Bundle entry goes in `meta.yaml` `pronunciations`, the same shape as a shared one, and wins for this Episode:

  ```
  pronunciations:
    - {term: Zeitgeber, kokoro: /tsˈaɪtɡeɪbə/, pocket: Zeit-gayber, by: skill 2026-10-30, note: TSITE-gay-ber}
  ```

  `kokoro` is espeak en-gb phonemes in slashes, or a lower-case respelling espeak reads. `pocket` is optional: Pocket reads most terms right as written. Where it needs help, write hyphenated chunks of real syllables (W-H-O), never a run-together respelling, which it garbles.
- `pipeline lint bundles/<Bundle id> --pron-check` prints what Kokoro will get for each entry beside espeak's own reading of the term. It needs espeak: `pip install -e ".[kokoro]"`.
- A term that will come back in later Episodes belongs in the shared Lexicon: propose it in the final message, don't write it.

## Heteronyms

Rephrase where context could mislead: past-tense "read" ("I went through it yesterday"), and "lead", "live", "close", "tear", "wind", "minute", "present", "record", "object", "content", "wound", "produce", "bass", "row", "bow", "refuse", "desert". Lint warns on each; a reason to keep one is fine ("'minute' as time").

## Punctuation

- Allowed: full stop, comma, question mark. An exclamation mark at most once per Segment. A colon or semicolon at most once per Segment; each gives only a short clause pause, so neither is a pause tool.
- **Banned (firm):** parentheses, square brackets other than `[beat]` and `[think]`, em and en dashes, slashes, `&`, `+`, `%`, currency symbols, `…`, `*`, `_`, `#` outside headings, `@`, emoji.
- No quotation marks around simulated questions.
- No asides in brackets or dashes. An aside becomes its own short sentence: "A small detour, because it matters later."
- No markdown emphasis, no bullets, no "a), b), c)".

## Fillers and stage directions (F5, firm)

Never "um", "uh", "erm", "haha", "[laughs]", "[sighs]", "*sighs*", "[pause]" or "[music]". The engine reads them out loud.

## Markup

The only non-spoken text in `script.md`:

| Markup | Meaning |
|---|---|
| `## <title>` on its own line | Segment boundary (headings in `template.md`) |
| A blank line | Paragraph break, and a pause |
| `[beat]` | A short deliberate pause, before a key number or a dry line. At most twice a Segment. |
| `[think]` | Thinking time after a recall question |
| `{c7}` or `{c3,c7}` | Claim tag after the sentence it supports; not spoken |

There is no emphasis or mood markup. Kokoro can't stress a word on request, so emphasis comes from wording (`template.md`, Sentences and lists).
