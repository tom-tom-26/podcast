# Episode template and style guide

research/05 as the owner signed it off: section 12 with the 12.11 softenings applied, plus the parts of sections 2-5 that section 12 left standing. `style_guide_version: 1`. Every number here is soft, about ±25%, unless marked **firm**.

## Variants and length

| | Quick | Standard (default) | Deep |
|---|---|---|---|
| Length | 8-15 min, typically about 11 | 15-28 min, typically about 25 | 28-35 min |
| Words at 165 wpm | up to about 2,500 | up to about 4,600 | up to about 5,800 |
| Content Segments | 2-3 | 4-5 | 5-7 |
| Simulated listener questions | 1-2 | 2-4 | 3-5 |

- The ranges are ceilings. There is no minimum. **Firm:** no padding to reach a length; if the honest content runs out, propose the shorter Variant.
- Deep is a listening choice, not an overflow. A Deep Episode may also hold a "Where experts disagree" passage.
- **Parts:** split only when the estimate passes about 35 minutes *and* the Topic breaks into subtopics that each stand alone. Otherwise a single Deep Episode may run to about 44 minutes, and anything longer is trimmed.
  - **Firm:** at most 3 Parts, and no cliffhanger endings.
  - Each Part has its own Hook, Roadmap, closing Segment and Recap, and makes sense heard alone or out of order. Part 2 on may open the Roadmap with a short "previously" of a few sentences.
  - The Sign-off may name the other Part's subtopic in one line, nothing more.
  - Prefer splits along questions useful on their own: how it works, then how to use it.
  - Titles: "<Topic> (Part 1 of 2)" in `meta.yaml`; the Script says "part one of two" if it says anything.

## Segments

Headings are fixed words so tooling can find them:

```
## Hook
## Roadmap
## 1: <title>          one per content Segment, numbered from 1
## Protocol            or ## Why it matters, for a Topic with nothing to act on
## Recap
## Sign-off
```

**Hook** (about 130 words; Quick about 100). Starts on content at second zero: a sourced surprise, a scenario with a twist, or the question the listener has probably asked. No welcome, no show name, no caution, no source by name. By about word 100 it makes the promise, phrased as something the listener will be able to do or understand. Vary the promise's wording; "By the end of this episode, you'll know..." is one form among many, and lint warns when it repeats a recent Bundle.

**Roadmap** (about 80 words). The organising frame and how many content Segments, said aloud, then what comes after them. A Higher-risk Episode puts its one caution line here.

**Content Segments.** Each one carries, in an order you vary between Segments:

- a spoken preview of what it explains and why, said with "because" and "so", never a bare "Idea two";
- its Recall prompt: the main question near the start, re-asked with its answer at the end. Inviting a guess is optional; sometimes the question just hangs with a `[think]`;
- the mechanism or core idea, one idea per sentence, with one everyday analogy carried through (and where it breaks, if it does);
- one sourced surprise, one concrete case, and one view the host commits to (research/18);
- the evidence phrase at the load-bearing claim (`accuracy.md`);
- at most one simulated listener question;
- one "so what" sentence per mechanism, in fresh words;
- the re-asked question may fold into the "so what";
- from Segment 2 on, a brief spaced-recall question about an earlier Segment.

Open one Segment with the case, another with the question, another with the surprising number. Don't give two Segments the same internal order. If research finds nothing surprising for a Segment, merge it or cut it.

Two ways to arrange the actions, picked per Topic:

- **Tool-led:** each content Segment is one tool: why it works, exactly what to do, how to adjust or when not to. The Protocol becomes a short first-week plan that orders the tools.
- **Mechanism-led:** the Segments build understanding in order, and the Protocol (or "Takeaways" for non-health Topics) carries the actions.

**Protocol** (about 480 words). Each action as what, how much, when, how to adjust, and when not to, with its caution beside it. For a Topic with nothing to act on (concepts, news, history), **Why it matters** instead: the implications, what to watch next, where the uncertainty lies. Both end with **"How sure are we"** (about 120 words): the strongest claim the Episode rests on, the weakest link, and what new evidence would change the advice.

**Recap** (about 200 words). Retrieval, not restatement: for each content Segment in Roadmap order, ask its question, `[think]`, answer. A Quick Episode may restate plainly.

**Sign-off** (about 50 words). One concrete thing to try, ideally with a time frame, or one thing to watch. Optionally one line pointing to a related Episode already in the Feed. No thanks for listening, no subscribe, no catchphrase, no "see you next week".

## Retrieval

Ranked by strength of evidence (research/17):

1. Each Segment opens with its main question and re-asks it with the answer at the end.
2. Previews say what is coming and why.
3. Each mechanism ends with a "so what".
4. Spaced-recall questions from Segment 2 on.
5. Two or three key terms each get a one-line description before the mechanism uses them.
6. A `[think]` after each question, then the answer, always. The pause lengths live in `config/pacing.yaml`, not in the Script.
7. One optional callback to a related earlier Episode, as the one cross-reference.

Never ask the listener to produce or explain something aloud. Never tell them to pause the app. Lead-ins don't repeat within an Episode.

## Plain language

The owner's top priority.

- **Explain first, name second** (a firm default): the idea in everyday words, then the term, if it's needed at all.
- An everyday analogy for every hard concept (a firm default). Never corny, never stacked: one per concept.
- About 3-4 technical terms per Episode, each defined in one plain sentence on first use.
- The target listener is a bright 15-year-old with no background in the subject, healthy, wanting to use what they learn. Don't assume they heard earlier Episodes.

You may break either firm default only with a reason, and you give the reason in the final message.

## The host

- An unnamed well-read friend who has done the reading. Curious, plain-spoken, warm, a little dry. Talks to one person, "you".
- **Firm:** never invents experiences, numbers, studies, quotes, researcher names or dates. No "when I tried", no "my clients".
- "I" only for reasoning and judgement: "Here's how I'd read that." "If it were my bedtime, I'd stop at noon." "We" only for "we, the people who study this": "We don't know yet."
- Examples: clearly hypothetical "say you..." scenarios, or real sourced stories logged in the ledger. About one per Segment, where it makes a hard idea click.
- Calibrated and willing to commit. Say what's known, likely and unknown. One hedge per claim, at the claim. Commit to a view at least once and say what it rests on; say once where you're unsure and why. Say when a popular claim is wrong.
- Risks with size: absolute numbers over relative ones ("from about two in a hundred to three in a hundred").
- Balanced on contested values and politics; commit only on questions of evidence and practical choice.
- Humour: zero to two light moments, only from the material, never near a caution.
- At most one cross-reference to an earlier Episode, and only one already in the Feed.

## Sentences and lists

- Contractions always. Main clause first. One idea per sentence.
- Sentence length varies on purpose: mean about 10-16 words, hard maximum 30, a very short sentence every hundred words or so. Not more than three long sentences in a row.
- Paragraphs up to 5 sentences or about 90 words. One-sentence paragraphs are welcome. Every paragraph break is a pause.
- Emphasis comes from structure: the key word last in a short sentence, a short sentence after a long one, a `[beat]` before a key number. "Not X. Y." at most once per Episode, and only to correct a belief the listener holds.
- Spoken lists: three items is a maximum, not a target; two is often better. Announce the count only for three or more items the listener must hold.
- Simulated listener questions: a real misconception or objection from research (a `misconception` ledger line), asked directly, with or without a lead-in, never in quotation marks, answered at once. No verdict word ("Not quite.", "Partly.") twice in an Episode; some answers start with the reason.
- The same noun for the same thing throughout. A listener can't re-read, so a synonym sounds like a new thing.

## Show notes

`show_notes.md` is written form, not spoken form: digits and units are fine. British spelling.

1. `Higher-risk topic: <reason>.` first, if flagged.
2. A short summary that adds to the title, leading with the most interesting specific claim.
3. The protocol or key points with exact numbers, as short plain paragraphs, or a short numbered list only where order matters.
4. `Sources`, then one line per source: author, year, title, venue, link, tier and read depth. References, not commentary.

No bold, no emoji, no headings beyond `Sources`, no "Key takeaways", no "In this episode", no calls to action. CC BY voice credits are added by the Pipeline.

## meta.yaml

```
title: When to stop drinking coffee     # sentence case, one clause, no colon, under about 60 characters
summary: >-                             # two or three sentences for the Feed; the first carries a specific sourced claim
  ...
variant: Standard                       # Quick, Standard or Deep
part: null                              # or {n: 1, of: 2, series_slug: caffeine}
voice: bm_george                        # a roster voice
risk_flag: false                        # true for a Higher-risk Episode
risk_reason: null                       # one line when flagged
pronunciations: []                      # Lexicon entries for this Episode only (tts.md)
wpm_budget: 165
target_words: 4100                      # what you aimed for
spoken_words: 3980                      # what the Script has, markup excluded
style_guide_version: 1
deslop_version: 1                       # the version in config/deslop_rules.yaml
parent_episode: null
questions: []
revision: 1
corrections: []
```

**Firm (F4):** the title and summary never promise more than the Episode delivers, and never state a claim the ledger doesn't support. No hype words in either.
