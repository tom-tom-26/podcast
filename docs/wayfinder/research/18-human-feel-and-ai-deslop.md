# Research 18: Human feel and AI de-slop across the whole tool

Ticket: `wayfinder/tickets/18-human-feel-and-ai-deslop.md`. Drafted 2026-10-29. Research only: no other file is edited. Proposed changes to research/05 and to later tickets are marked **[R]** and need the owner.

Question: how does every layer of the tool (Content, Audio, Interface, Build) come across as made by a careful person, with no AI slop? What are the tells, how are they caught cheaply, and what replaces them?

**How deeply each source was read.** **[F]** full text read. **[A]** abstract, or the abstract plus figures, read at the source. **[S]** secondary only (search summaries, citing papers, blogs). **[M]** measured by me on this machine today. **[C]** craft opinion from practitioners, not a measured result. **[R]** my recommendation. **[K]** background knowledge, not re-checked.

Terms follow `GLOSSARY.md`. Section numbers in research/05 refer to that file; its section 12 overrides its earlier sections, and ticket 06 overrides style wherever they clash on accuracy.

---

## Bottom line

1. **The written tells are real and measurable, but they move.** Post-ChatGPT papers show a sudden excess of style words ("delves" 28 times its expected rate in 2024 PubMed abstracts) [F: Kobak et al. 2025]. Instruction-tuned models use present-participle clauses 2-5 times as often as people and nominalisations 1.5-2 times as often [F: Reinhart et al. 2025]. But once a tell becomes known, models and writers swap it for another: "delve" fell while "significant" kept rising. A banned-word list catches symptoms and needs refreshing. It does not fix the cause.
2. **The cause is emptiness, not vocabulary.** Slop is what fills the space when there is no specific fact, no stake and no view. The cheapest durable fix is upstream: each segment must carry one sourced surprise, one concrete case and one committed judgement. Without those, scrubbing words produces clean, dull scripts.
3. **The owner is the hardest audience for this.** People who use LLMs heavily for writing spotted AI text almost perfectly (a majority vote of five such annotators misclassified 1 of 300 articles), while non-users did little better than chance [A: Russell et al. 2025]. A heavy Claude user will hear the tells.
4. **Some research/05 rules produce slop themselves**: the "Not X. Y." contrast device (a listed AI tell), the three-item list rule, the fixed lead-in pools for recall prompts and listener questions, the identical internal order of every segment, and the fixed promise sentence. Each needs softening into variety, not removal. Accuracy rules stay as they are.
5. **Audio: the biggest fixable tells are identical pause lengths, pauses that stack, and mispronunciation.** The audition renders put every paragraph gap at 0.90-0.93 s [M]. Human read speech has log-normal pause lengths, peaking near 500-600 ms, and only spontaneous speech has pauses over a second [F: Campione & Véronis 2002]. The Pipeline can draw pauses from a distribution, chunk per sentence, jitter speed slightly per chunk and fix pronunciations through phoneme input. Kokoro has no SSML, no per-word emphasis and, with the shipped model, no timing output, so emphasis has to come from wording.
6. **Breath sounds are a real but small lever with real risks.** Inserted 600 ms inhalations improved verbatim recall slightly in one modern TTS study (0.902 to 0.923 normalised score) and 300 ms ones did not [F: Elmers et al. 2021]. The authors themselves found the 600 ms breath "abnormally long". Treat breaths as an audition A/B test, off by default.
7. **Interface and Build have the same disease in a different form**: template descriptions ("In this episode, we explore..."), bold-bullet show notes with emoji, comments that narrate code, generic names, over-abstraction and commit messages that list files instead of saying why. Apple's own guidance and Git's own contribution rules already describe the human version.
8. **Proposed check:** a mechanical lint (phrase list, cross-episode n-gram repeats, sentence-length spread, list-of-three and paragraph-opener counts) plus a ten-question self-review the Skill answers before emitting the Bundle. Style findings only warn. Blocking stays limited to firm rules, and the new firm candidates in section 8 are questions for the owner, not decisions.

---

## 1. What the evidence on AI writing actually supports

| Finding | Source | Strength |
|---|---|---|
| Sudden excess of style words in 2024 biomedical abstracts: "delves" r = 28.0, "underscores" 13.8, "showcasing" 10.7; common words in excess include "potential", "findings", "crucial". 66% of the 379 excess style words were verbs, 14% adjectives. At least 13.5% of 2024 abstracts processed with an LLM. | Kobak, González-Márquez, Horvát & Lause, *Science Advances* 11(27), 2025, doi:10.1126/sciadv.adt3813; [arXiv html](https://arxiv.org/html/2406.07016v5) [F, figures read from the html] | Strong for the vocabulary shift in scientific abstracts. Says nothing about speech scripts. |
| Later revision: "delve" dropped once it became notorious; "significant" kept rising. | Same paper, later arXiv versions, [abstract page](https://arxiv.org/abs/2406.07016v5) [S, via search summary] | Moderate. It is the key reason a fixed word list goes stale. |
| Instruction-tuned models differ from human text in grammar: GPT-4o uses present-participle clauses 5.3 times the human rate (d = 1.38), nominalisations 2.1 times (d = 1.23), phrasal coordination 1.9 times, agentless passive about half as often. Overused words include "camaraderie", "tapestry", "intricate", "underscore", "palpable", "unease". Differences are larger for instruction-tuned than base models. | Reinhart et al., "Do LLMs write like humans?", *PNAS* 2025, doi:10.1073/pnas.2422455122; [arXiv html](https://arxiv.org/html/2410.16107v2) [F, results read] | Strong for written prose across several genres. The grammar finding matters more than the word list because it is harder to scrub. |
| Human news text has more varied sentence lengths and vocabulary than LLM news text; LLMs use more numbers, auxiliaries and pronouns and less negative emotion. | Muñoz-Ortiz, Gómez-Rodríguez & Vilares, *Artificial Intelligence Review* 2024, doi:10.1007/s10462-024-10903-2; [arXiv](https://arxiv.org/abs/2308.09067) [A] | Moderate, one genre. A non-peer-reviewed matched-pair analysis found sentence-length spread on its own a weak detector ([opace.agency](https://opace.agency/tools/ai/content-verification-integrity/research/ai-writing-myths-measured/), [S]). Use it as one signal among several, not a verdict. |
| RLHF may contribute to the overuse of words like "delve"; architecture and training data do not explain it. Evidence mixed. | Juzek & Ward, COLING 2025, [arXiv](https://arxiv.org/abs/2412.11385v1) [A] | Weak to moderate. Useful mainly for "why it keeps happening". |
| Heavy LLM users detect AI-written non-fiction very accurately (5-annotator majority vote: 1 error in 300), beating most automatic detectors, including on paraphrased or "humanised" text. They cite vocabulary, but also formality, originality and clarity. | Russell, Karpinska & Iyyer, ACL 2025, [arXiv 2501.15654](https://arxiv.org/abs/2501.15654) [A] | Moderate. The relevant point: tells are noticed by exactly this owner's kind of reader, and they are not only lexical. |
| An editor-maintained catalogue of signs: significance inflation ("a pivotal moment", "a testament to"), trailing "-ing" analysis ("highlighting...", "ensuring..."), promotional words ("vibrant", "nestled", "boasts"), vague attribution ("experts argue"), "despite these challenges" sections, copula avoidance ("serves as", "stands as"), negative parallelism ("not just X, but Y"), the rule of three, title case and bold overuse, emoji as formatting, chatbot phrases ("I hope this helps", "Certainly!"). It dates its vocabulary lists by era and now lists em-dash overuse as a historical sign (2022 to September 2026). | [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) [F for the first ~200k characters; the tail was not read] | Practitioner catalogue, not a study. High value because it is maintained against current models and is explicit about its limits: "descriptive, not prescriptive", "not proof of AI use", and "fixing surface signs alone" leaves the real problems (sourcing, neutrality) in place. |
| Automatic detectors have non-trivial error rates. | Same Wikipedia page, citing GPTZero and Pangram [S] | Moderate. Do not buy or run a detector; the lint below targets this project's own tells. |

**What I could not verify.** No study measures AI tells in *spoken* scripts or podcast audio. Everything about scripts below is extrapolated from written prose plus radio craft.

---

## 2. Content layer: named tells

Each tell: what it looks like, why it reads as machine-made, how to catch it (**M** mechanical, **J** judgement in the Skill's self-review), and the fix. Phrase lists for the M checks are in section 9.

| Id | Tell | Looks like | Why it reads as machine-made | Detect | Fix |
|---|---|---|---|---|---|
| C1 | Stock openers and closers | "Let's dive in." "In today's episode..." "Ever wondered why...?" "So, to wrap up..." "Thanks for listening." | Openers that fit any topic carry no information. They are the most quoted LLM tells and already on research/05's ban list. | M | Start on the fact, scene or question itself (research/05 2.9). End on the one thing to try. |
| C2 | LLM vocabulary | delve, tapestry, intricate, underscore, pivotal, crucial, landscape, realm, testament, showcase, foster, navigate (figurative), leverage, robust, seamless, multifaceted, vibrant, palpable | Measured excess in LLM text (section 1). Also bookish: nobody says "tapestry" to a friend. | M (count and list) | Plain word, or cut. "Crucial" becomes "the part that matters" or nothing. |
| C3 | Copula avoidance | "Adenosine serves as a signal." "The hippocampus acts as a hub." | Avoiding "is" is a catalogued tell, and it adds syllables for the ear with no meaning. | M | "Adenosine is a signal." |
| C4 | Negative parallelism | "It's not about the amount, it's about the timing." "Not just a stimulant, but a mask." "Caffeine doesn't take any sand away. It covers the gauge." | One of the strongest current tells (Wikipedia; also the owner's own dissertation profile, rule 2). It manufactures a contrast nobody proposed. | M (regex for "not X, (it's) Y", "not just... but") | State the positive claim. Keep a contrast only when a real misconception is being corrected, and then once per episode (section 4, row 5). |
| C5 | Reflexive rule of three | "faster, sharper and more focused"; three adjectives, three short clauses, three examples, every time | LLMs use triples to look comprehensive (Wikipedia). Repeated, the rhythm is audible and predictable. | M (count "X, Y and Z" per 1,000 words; count "three things" announcements) | Use the real number of items. Two is fine. One strong example beats three thin ones. |
| C6 | Trailing participle analysis | "...which fell by a third, highlighting the importance of sleep." "..., underscoring how little we know." | 5.3 times the human rate for GPT-4o [F: Reinhart]. It tacks a vague judgement on to a fact. | M (", highlighting/underscoring/showcasing/emphasising/reflecting/ensuring") | Either cut the tail, or make it a sentence that says the actual inference: "So the sleep loss is real even when you can't feel it." |
| C7 | Significance inflation | "a pivotal moment", "changed everything", "plays a crucial role", "a testament to" | Asserts importance instead of showing it. Catalogued tell. | M | Show the size: a number, a before-and-after, a consequence. |
| C8 | Vague attribution | "Studies show", "experts say", "scientists agree", "some argue" | Catalogued tell, and an accuracy fault under ticket 06: no traceable source. | M (also checks the sentence carries a claim tag) | Name the evidence in research/05 2.6 terms, with the tag. This is the one content tell where accuracy rules already decide the answer. |
| C9 | Hedge stacking | "This may potentially suggest that it could possibly help." | LLMs hedge per sentence, not per claim. Sounds evasive. | M (three or more hedge words in a sentence) | One hedge per claim, at the claim, in the 2.6 vocabulary (research/05 section 4). |
| C10 | Empty signposting and meta-talk | "Now let's turn to...", "In this section we'll look at...", "As we discussed earlier..." with nothing after it | Talks about the episode instead of the subject. research/17 found heading-style signals fail in TTS audio; only content-bearing previews help. | M (phrase list) + J | Every signpost says what the segment explains and why (research/05 12.6 item 2). |
| C11 | Summary for its own sake | A paragraph that ends by restating itself; "In summary", "To sum up"; a recap after every point | Fills space. LLMs close every unit with a summary sentence. | M ("in summary", "to sum up", "in short", "overall,") + J | Keep the planned retrieval recap (research/05 12.6). Cut every other restatement. |
| C12 | Fake enthusiasm and sycophancy | "Great question!" "Fascinating!" "This is amazing." Exclamation marks | Chatbot register. Also, on TTS, exclamations make Kokoro push energy in a way that sounds performed. | M | Let the fact do the work. A dry line after a surprising number lands harder. |
| C13 | Uniform rhythm | Sentence after sentence of 12-16 words; every paragraph four sentences; every paragraph ends with a takeaway | Lower spread of sentence length is measured in LLM text (Muñoz-Ortiz). On the ear it becomes a drone, and TTS exaggerates it (section 5, A4). | M (spread of sentence length; runs of similar-length sentences; paragraph-closer pattern) | Mix very short sentences with longer ones; allow one-sentence paragraphs; end some paragraphs mid-thought and pick it up in the next. |
| C14 | Repeated paragraph openers and template transitions | "So,", "Now,", "Here's", "This" opening paragraph after paragraph; the same transition phrases every episode | Template feel. Across episodes it turns the show into a mail-merge. | M (first-word counts in the episode; n-gram overlap with recent Bundles) | Vary openers. Treat research/05 5.6 as examples, not a menu. |
| C15 | Generic examples | "Imagine a busy professional named Sarah..."; "Picture a student cramming for exams" with no detail that could only belong to this topic | Interchangeable cases are the opposite of specificity. (That models default to particular stock names is folklore I could not verify; the fault is the genericness, whatever the name.) | J | Use a real, sourced case (research/05 12.8 b): the study's participants, a documented event, a named place and year. If hypothetical, give it one detail that is specific to the topic. |
| C16 | Moral endings and grand closers | "And that, in the end, is what makes sleep so remarkable." "The future looks bright." "Despite these challenges..." | Catalogued "challenges and future outlook" pattern; relentless positivity (owner's profile, rule 5). | M (phrase list) + J | End on a concrete thing to try or watch (research/05 2.10). |
| C17 | Verdict-free balance | "Ultimately, it depends." "There are pros and cons." | LLMs avoid commitment. research/05 section 4 asks the host to commit when the evidence allows. | M ("it depends", "pros and cons") + J | Say what you would do and what it rests on; say what would change your mind. On contested values (news, politics), present both sides fairly (ticket 06) and commit only on questions of evidence. |
| C18 | Invented intimacy or experience | "When I first tried this..." "I remember..." "My listeners often tell me..." | Dishonest for a synthetic host. Already firm (research/05 12.2). | M ("when I (first )?tried", "I remember", "my (clients|listeners|friends)") + J | "Say you..." scenarios or sourced cases. |
| C19 | Elegant variation | "caffeine... the stimulant... the compound... this popular molecule" | Synonym cycling is a catalogued (now historical) tell, and harmful in audio: a listener who can't re-read thinks a new thing has arrived. | J | Repeat the same noun. Repetition is a feature on the ear. |
| C20 | Nominalisation-heavy abstraction | "the facilitation of memory consolidation", "the optimisation of sleep timing" | 1.5-2 times the human rate in instruction-tuned models [F: Reinhart]. Hard to follow by ear. | M (rough: share of words ending -tion/-ment/-ness/-ity per sentence) + J | Verbs: "sleep helps you keep what you learned". |
| C21 | Bookish show-notes formatting | Bold-led bullets, "Key Takeaways", emoji, title-case headings, a "Conclusion" heading | Catalogued formatting tells (Wikipedia, style section). | M | Short plain paragraphs, then the protocol, then sources (section 6). |

**What the tells have in common.** C1, C7, C10, C11, C12 and C16 are all filler that stands in for content. That is why the human qualities in section 3 come first in the fix, and the lint second.

---

## 3. Human qualities that make spoken explanation gripping, as Skill actions

Most of this section is craft opinion [C]. Where a study supports it, that is said.

| Quality | What practitioners say | What the Skill does |
|---|---|---|
| **Specificity** | Radio writing advice converges on concrete nouns, active verbs and one thought per sentence ([UBC workshop drawing on NPR's *Sound Reporting*](https://wiki.ubc.ca/Course:LFS400/Workshops/Writing_For_the_Ear), [S]; [JEA summary of Kern](https://jea.org/?p=1953), [S]). Concrete examples have moderate learning evidence (research/17 2.7). | Each content segment contains at least one detail that could only belong to this topic: a figure, a place, a year, a study population, an object. During research, mark ledger lines that carry such a detail. In self-review, swap any sentence that would fit three other topics. |
| **Real stakes** | Glass: a story needs "an interesting idea about how the world works", and both the action and the conclusions must be interesting ([Transom 2004](https://transom.org/2004/ira-glass/), [C]). | The Hook names what the listener stands to lose or gain, in their own life, in concrete terms. Each segment's "so what" (research/05 12.6 item 3) states a consequence for the listener, not a moral. |
| **Surprise** | Glass: "If it's not surprising, it's not a story" (same source, [C]). Prequestions work best when the listener's guess is likely wrong (research/17 2.1, moderate evidence, larger for low prior knowledge). | Each segment is built around one sourced fact the default listener (research/05 section 4) probably gets wrong. That fact becomes the segment's opening question. Ledger lines can carry a `surprise` tag next to the existing `misconception` tag. If research finds nothing surprising for a segment, merge or cut the segment rather than inflate it (no padding is firm). |
| **A point of view** | Glass on Alex Chadwick: "he sounds like a real guy telling you something he's interested in, not a news-robot" (Transom, [C]). NPR Training: the goal is to "sound like yourself", and trying to sound like the house style holds reporters back ([NPR Training 2016](https://training.npr.org/2016/03/23/reporter-two-ways-improvisation-within-a-structure/), [C]). | The host commits at least once per episode, using research/05's "I" for reasoning: "Here's how I'd read that." "If it were my bedtime, I'd stop at noon." It also says once where it is unsure and why. Opinions about evidence and practical choices only; contested values get both sides (ticket 06). Inference is labelled as inference. |
| **Uneven rhythm** | Writing for the ear means writing the way you speak, in short units, read aloud before it airs (UBC, JEA, [S]). Shorter sentences were recalled better from TTS (0.959 vs 0.860 normalised score, 8.5 vs 16.2 words) [F: Elmers et al. 2021]. | Mix lengths on purpose: a three-to-five-word sentence at least every hundred or so words, a longer explanatory sentence where the logic needs it. Some paragraphs one sentence long. The lint measures spread, not just the mean (section 9). |
| **Natural asides** | Asides are how a person shows they are thinking, not reciting [C]. research/05 6.2 rule 10 bans parenthetical asides for TTS reasons. | Allow asides as their own short sentences, never in brackets or dashes: "A small detour, because it matters later." "Odd detail, but true." At most one or two an episode (soft), and each must carry a fact or a judgement. |
| **Earned humour** | Glass: build in moments that amuse you, "no pleasure, no sense of discovery, no humor" is how stories fail; and over-performing emotional material "can sound cheesy really fast" (Transom, [C]). | Humour comes only from the material: an absurd true detail, a dry understatement after a big number, the gap between what people believe and what the data say. No inserted jokes, puns or "fun fact" framing. None near a higher-risk caution. TTS cannot time a punchline, so the only timing tool is a `[beat]` before the dry line. Soft target: zero to two light moments an episode; zero is fine. |

---

## 4. Reconciliation with research/02, research/05 (sections 5 and 12) and ticket 06

Accuracy and honesty rules win every conflict. The host never invents experiences. "Agree" means this ticket adds nothing; "Extend" adds a de-slop angle; "Conflict" means the existing rule, applied literally, produces a tell, with a proposed softening **[R]**.

| # | Existing rule | Relation | Note and proposed softening |
|---|---|---|---|
| 1 | 02 rule 1 / 05 2.9: promise sentence by word ~100, "By the end of this episode, you'll know..." | **Conflict (mild)** | The example wording, reused every episode, becomes a catchphrase. Keep the promise as a function. [R] Vary its form; the lint flags any promise sentence sharing six or more consecutive words with one in the last ten Bundles. |
| 2 | 02 rule 4 / 05 2.4 step 1: signpost every transition | **Extend** | Already sharpened by research/17: previews must carry content. A content-free signpost is C10. |
| 3 | 02 rule 7 / 05 2.7: simulated listener questions with varied lead-ins ("You might be thinking...") | **Conflict (mild)** | The pool is small and fixed, so across episodes the lead-ins repeat. [R] Allow questions with no lead-in at all ("So is the caffeine gone by bedtime? Not quite."). Cross-episode n-gram check applies. |
| 4 | 05 2.7: answer starts with a verdict word ("Not quite." "Partly.") | **Conflict (mild)** | Fine once; formulaic three times. [R] No verdict word twice in an episode; some answers may start with the reason. |
| 5 | 05 5.2: "Repeat with contrast: Not the amount. The timing." | **Conflict** | This is negative parallelism (C4), one of the strongest tells. [R] Keep as one emphasis tool among several, at most once per episode (soft), and only when it corrects a belief the listener actually holds. Prefer end-focus ("What matters is the timing.") and the short-sentence-after-long device. |
| 6 | 05 5.3: at most three items in a spoken series; announce the count | **Conflict (mild)** | The cap protects the listener's memory and should stay. Applied everywhere, it makes every list a triple (C5). [R] The cap is a maximum, not a target: two items are often better. Announce the count only when there are three or more and the listener needs to hold them. Lint warns on more than two "three things" announcements per episode. |
| 7 | 05 5.1 and checklist 18: mean sentence length 10-16 words, maximum 30 | **Extend** | A mean alone rewards uniform 13-word sentences. The research/05 example itself averages 9.8 [M], inside the ±25% band. [R] Add a spread check (section 9). Keep the 30-word maximum as the TTS-facing limit it is. |
| 8 | 05 5.1: paragraphs at most 5 sentences / 90 words | **Extend** | Fine as a maximum. [R] Say explicitly that one-sentence paragraphs are welcome. |
| 9 | 05 5.5: banned phrases, including "Now," "So," and "Here's the thing" at most once per episode | **Conflict (small)** | research/17 and 05 12.6 item 2 want "so" and "because" at causal joints. [R] The once-per-episode limit applies to "So," as a paragraph-opening discourse marker, not to causal "so" mid-sentence. Extend the list with C2 vocabulary and the C3/C4/C6 constructions. |
| 10 | 05 5.6: transition pool | **Conflict (mild)** | A fixed pool reused across episodes is a template. [R] Mark the pool as examples; the cross-episode check catches reuse. |
| 11 | 05 2.4: fixed internal order of a content segment | **Conflict (mild)** | Five segments with the same shape (signpost, way in, mechanism, evidence, question, bridge, recall) is structural slop the listener notices by segment three. research/05 already says "unless the material demands otherwise". [R] Vary the order across segments: open one with the case, another with the question, another with the surprising number. Keep the retrieval bookends (12.6 item 1). |
| 12 | 05 12.6 items 1 and 4: open each segment with its question and invite a guess; re-ask at the end; spaced recall from segment 2 | **Conflict (mild)** | The evidence supports the device (research/17, moderate). Said the same way five times ("Have a guess before I explain"), it becomes a quiz-show formula. [R] The question is mandatory; the invitation phrase is not. Sometimes the question simply hangs ("So why would a three o'clock coffee cost you sleep at eleven?") with `[think]`. Vary the re-ask: sometimes folded into the "so what" sentence. No lead-in repeated within an episode. |
| 13 | 05 12.6 item 3 / research/17: each mechanism ends with an explicit "so what" | **Extend, with a risk** | Saying the inference is good for listeners (research/17 2.12). Every paragraph ending in a takeaway is C16/C13. [R] One "so what" per mechanism, not per paragraph, and not always in the same words ("So here's what that means for you" at most once an episode). |
| 14 | 05 2.6: fixed evidence vocabulary so the claim-check can compare with the ledger tier | **Accuracy wins; soften the wording only** | Identical phrases at every claim ("Early evidence." x6) sound canned. [R] Keep the tier meaning fixed and add two or three equivalent phrasings per tier, all mapped in the lint, so the claim-check still works. Never upgrade a tier for variety. |
| 15 | 05 6.2 rule 10: no asides (TTS) | **Agree for TTS; extend** | Asides as standalone sentences are TTS-safe (section 3). |
| 16 | 05 12.7: an everyday analogy for every hard concept (firm default) | **Agree, with a risk** | Stacked or corny analogies are a tell. 12.8 already says "never corny or stacked". [R] One analogy per concept, carried through (the hourglass in research/05 7.1 is the model), and say where it breaks (research/17 2.7). |
| 17 | 05 12.2 firm: no padding | **Agree** | Padding is the root of C1, C10, C11 and C16. This firm rule is the most important de-slop rule already in the spec. |
| 18 | 05 section 4 / 12.8: no invented experience; "I" only for reasoning | **Agree (firm)** | C18 is caught mechanically too. |
| 19 | 05 2.10 / 12.9: sign-off with one thing to try, no catchphrase | **Agree** | Extend the cross-episode check to the sign-off. |
| 20 | 02 rule 5 superseded / ticket 06: no standing disclaimer, targeted cautions at the action | **Agree** | Boilerplate disclaimers are slop. The specific caution ("If you take blood pressure medication...") is the human version. |
| 21 | Ticket 06: no vague attribution, every claim traceable | **Agree; strengthens C8** | Candidate firm rule F2 (section 8) simply makes the existing accuracy rule mechanical. |
| 22 | Ticket 06: news topics label reported fact, dispute and analysis; contested political claims get both sides | **Agree; bounds C17** | Point of view applies to evidence and practical choices, not to contested values. |
| 23 | Ticket 06 amendment 8: paraphrase, quote at most a sentence | **Agree** | Also helps the voice: long quotes read by TTS sound like someone else's prose. |
| 24 | Ticket 08: titles read `Episode N: Title` | **Conflict with Apple guidance (not a slop issue)** | Apple asks creators not to put episode numbers in titles and to use RSS tags instead ([Apple, Present your podcast](https://podcasters.apple.com/support/867-featured-present-your-podcast), [F]). 08 is owner-decided and omits `itunes:episode`, so the prefix is the only numbering. The practical cost is that a truncated title on the iPhone shows "Episode 12: When to sto..." Flag for ticket 12; no change proposed here. |

---

## 5. Audio layer

### 5.1 What the engine actually allows

Checked against the installed `kokoro-onnx` 0.6.1 source in `prototypes/voice_audition/.venv` and by inspecting the shipped model file [M]:

- `create(text, voice, speed=1.0, lang, is_phonemes=False, trim=True, sentence_pause=0.25, clause_pause=0.1, continuous=False)`. `speed` must be between 0.5 and 2.0 and is **one scalar per call**, so speed can vary per chunk and never inside one.
- `is_phonemes=True` accepts a phoneme string instead of text. This is the route to a pronunciation lexicon (ticket 14) and, in principle, to moving stress marks (`ˈ`, `ˌ`) for emphasis. Whether Kokoro audibly follows edited stress marks is **untested**.
- The shipped `kokoro-v1.0.int8.onnx` has inputs `tokens`, `style`, `speed` and a single output `audio`: **no duration output**. So `continuous=True` raises an error, and the timing-based pause placement in `pauses.py` cannot run. With this model, `sentence_pause` and `clause_pause` are only added at the joins between the library's own 510-phoneme batches. Inside a chunk, the gap after a full stop is whatever the model produces, which the library's own docstring puts at "around 0.1s" in dialogue. This refines research/05 6.1, which reads as if the 0.25 s were added after every sentence.
- `trim=True` strips leading and trailing silence from each batch, so silence the Pipeline adds between chunks is the real gap.
- No SSML, no emphasis, no pitch control, no breath tokens. Punctuation shapes intonation: espeak keeps `.`, `,`, `?`, `!` and `...` in the phoneme string [M: "Wait... what?" → `wˈeɪt... wˌɒt?`].
- Filler words are phonemised as ordinary words [M: "um" → `ˈʌm`, "Hmm" → `həm`, "Huh" → `hˈʌ`]. Whether they sound natural is unheard.

### 5.2 Named audio tells

| Id | Tell | Why it sounds robotic | Fixable by the Pipeline? | How |
|---|---|---|---|---|
| A1 | Identical pause lengths | Human pauses vary on a log-normal curve (section 5.3). In the audition renders every paragraph gap sits at 0.90-0.93 s and nothing exceeds 0.93 s [M: af_heart 45 pauses ≥150 ms, median 460 ms, p90 906 ms; bm_george 57 pauses, median 380 ms]. The repeated value is audible as a metronome. | **Yes** | Draw each gap from a distribution per pause class (5.4). |
| A2 | Stacked or doubled pauses | Prototype silences sat on top of the model's own punctuation gaps (research/05 6.3; ticket 09 issue 3). Dead air reads as a glitch. | **Yes** | One layer owns each pause: chunk per sentence, `trim=True`, Pipeline adds all inter-chunk silence. |
| A3 | Uniform pace | The same rate for a dose as for a throwaway line. Humans slow for what matters [C]. | **Partly** | Per-chunk speed: slightly slower for sentences carrying numbers, doses or the segment's key claim; tiny random jitter elsewhere (5.4). |
| A4 | Same intonation every sentence | Each chunk is synthesised fresh, so each starts with a fresh contour [S: research/03 "each chunk resets prosody"]. Sentence-per-chunk makes this worse; long chunks rush (A9). | **Mostly by wording** | Vary sentence types in the Script: questions, short declaratives, fronted phrases ("By bedtime, ..."), the occasional two-sentence chunk. Ticket 09 compares sentence-per-chunk with pairing short sentences. |
| A5 | Joins between chunks | Level or timbre jump, clicks at hard cuts [K]. | **Yes** | 5-10 ms fades at chunk edges; loudness normalisation over the whole episode (ticket 15 already has -16 LKFS). |
| A6 | Mispronunciation | One wrong reading of a key term breaks the illusion faster than any prosody issue [C]. research/05 6.1 lists many espeak failures. | **Yes** | Spoken-form rules (firm), plus a lexicon applied by phoneme substitution (ticket 14), plus a speech-to-text round trip (ticket 15). |
| A7 | No breath at all, or fake repetitive breath | Twenty minutes of breathless speech is unlike any person [C]; one looped breath sample is worse. | **Optional** | Breath samples before some paragraph starts, A/B tested (5.5). Off by default. |
| A8 | Wrong or no emphasis | Default stress falls on the last content word; contrastive stress is impossible on request. | **By wording only** | End-focus, short sentence after a long one, cleft sentences ("What matters is the timing."), `[beat]` before the key word or number. Stress-mark editing via phonemes is a low-priority experiment. |
| A9 | Rushed long chunks | Artefacts near the 510-phoneme ceiling (research/03 [S]). | **Yes** | Chunk per sentence; the 30-word sentence maximum keeps chunks well under the limit. |
| A10 | Over-performance | Exclamation marks and rhetorical questions push energy; Glass: "it's fantastically easy to over-perform" [C]. | **By wording** | Exclamation at most once per segment (05 6.2 rule 8); question density check (section 9). |
| A11 | List contour | Three items in a row each get the same contour, which sounds like a machine reading a list [C]. | **By wording** | Split lists into separate sentences with different shapes (05 5.3 already). |
| A12 | Scripted disfluency | "Um", "uh", "[laughs]", "haha" rendered literally by TTS. | **Ban in Script** | No fillers or stage directions in the Script (candidate firm rule F5). Evidence on fillers is mixed anyway: Fraundorf & Watson (2011, *JML* 65(2), 161-175) found human-recorded "uh/um" improved recall of plot points [S]; a partial replication found no effect in English and a fluent advantage in German ([Muhlack et al. 2021](https://www.coli.uni-saarland.de/~trouvain/docs/Muhlack_et_al_2021.pdf), [S]). |

### 5.3 Evidence behind the pause and phrasing defaults

- **Pause durations.** Campione & Véronis (2002, Speech Prosody, 199-202, [PDF](https://mail.sprosig.org/sp2002/pdf/campione-veronis.pdf)) [F]: about 6,000 silent pauses in 5.5 hours, read speech in five languages plus French interviews. Pause durations are log-normal overall. Read speech has two peaks: brief pauses around 100-150 ms (4-23% of pauses) and medium pauses around 500-600 ms (77-96%). English read speech: arithmetic mean 487 ms, median 493 ms. Spontaneous speech adds a third class around 1.6 s (14% of pauses), and 2.8% of its pauses exceed 2 s; read speech had none over 2 s. Proposed categories: brief under 200 ms, medium 200-1000 ms, long over 1000 ms. *Strength: moderate.* Large corpus, but the spontaneous part is French only, it is 2002, and a scripted podcast sits somewhere between read and spontaneous speech.
- **Phrase breaks matter to listeners.** Japanese TTS with predicted phrase breaks scored 4.39 on prosody naturalness against 4.37 for ground-truth breaks ([Futamata et al., Interspeech 2021](https://www.isca-archive.org/interspeech_2021/futamata21_interspeech.html)) [A]. English Tacotron2 listeners clearly preferred text synthesised with predicted phrase breaks, and the author reports better comprehension ([Vadapalli, *SN Computer Science* 2025, arXiv 2304.04157](https://arxiv.org/abs/2304.04157)) [A]. *Strength: moderate that pause placement at phrase boundaries matters; neither tests Kokoro.*
- **Breath groups.** Studies of read speech put breath groups at roughly 2-3.5 s and 15-20 syllables, with inhalations at major syntactic boundaries (Korean read speech mean 3.06 s, 17.95 syllables; German spontaneous ~3.5 s) [S: search summaries only, papers not opened]. At 165 wpm that is about one sentence. *Strength: weak as cited here.*
- **Long-form judging.** Sentence-level ratings of TTS, paragraph ratings and in-context ratings gave different results that did not necessarily correlate ([Clark et al., SSW 2019](https://www.isca-archive.org/ssw_2019/clark19_ssw.html); [Google blog](https://research.google/blog/assessing-the-quality-of-long-form-synthesized-speech/)) [A]. *Strength: moderate.* It is the main reason ticket 09 must judge minutes, not sentences.

### 5.4 Soft starting values for the Pipeline

**Amended by ticket 09 (owner, 2026-10-29):** the owner preferred longer chunks (several sentences, up to ~300 characters) to one chunk per sentence, and drawn gaps to fixed ones. The values below now apply at chunk, paragraph and segment boundaries. Inside a chunk, the model sets the gap between sentences.

All values are soft defaults to be tuned by ear in ticket 09, with ±25% leniency. They assumed one chunk per sentence, `trim=True`, and the Pipeline owning every gap between chunks. Random draws use a seed derived from the Episode id, so a re-render is identical.

| Pause class | Distribution | Clip range | Notes |
|---|---|---|---|
| Between sentences, same paragraph | log-normal, median 0.38 s, geometric SD factor 1.3 | 0.22-0.65 s | Near Campione's medium peak, slightly short because a TTS voice has no hesitation inside sentences. Subtract 0.08 s when the next sentence starts with "And", "But", "So" or "Because" (tight link). Add 0.10 s after a question. |
| Paragraph break | log-normal, median 0.75 s, factor 1.25 | 0.55-1.10 s | Replaces the fixed 0.8 s. |
| Segment boundary (`## heading`) | uniform 1.3-1.7 s | 1.2-1.9 s | The one place a "long" pause over a second is natural. |
| `[beat]` | uniform 0.8-1.1 s | fixed range | Before a key number or a dry line. |
| `[think]` | 3 s for one-fact questions, 4.5 s for "why" questions (research/17), ± 0.3 s jitter | 2.5-5.5 s | Functional pause, so only slight jitter. |
| Commas, colons, semicolons | model's own | n/a | Not touched. |

| Speed | Value | Notes |
|---|---|---|
| Base | set so the chosen voice lands at ~165 wpm (research/05 section 1) | Per voice, from ticket 09. |
| Jitter per chunk | uniform ±0.025 around base | Small enough to be felt, not heard as a lurch. Cap the step between adjacent chunks at 0.04. Untested [R]. |
| Key-information chunks | base × 0.95 | Sentences with number words, doses, or a claim tag the Skill marks as load-bearing. |
| Bounds | 0.90-1.10 × base | Outside this, Kokoro may smear or rush (research/05 section 1 warns about smearing). Candidate firm rule F6 for engine safety. |

Sentence-length variety is set by the Script, not the Pipeline: section 9's spread check is the audio fix for A4 as much as a writing rule.

### 5.5 Breath insertion: options and risks

| Option | For | Against |
|---|---|---|
| None (default) | Zero risk of uncanny breaths; nothing to license; current audition state. | Long stretches can feel airless. |
| Recorded breath samples, inserted by the Pipeline | The one measured benefit: 600 ms inhalations improved recall slightly (0.902 → 0.923, p < 0.01); 300 ms ones did not [F: Elmers et al. 2021, Polly standard voices, 63 listeners, single sentences]. Whalen et al. (1995, *JASA* 97(5)) found a similar effect with formant synthesis [S, via Elmers]. | Elmers' first author found the effective 600 ms breath "abnormally long", so the benefit may come from extra processing time, not naturalness. A breath recorded from a different person has a different timbre; a small sample set repeats audibly; samples need a clear licence; single-sentence lab results may not carry to 25-minute episodes. |
| Neural breath generation | Natural in research systems (Székely et al., ICASSP 2020, [PDF](https://www.speech.kth.se/tts-demos/szekely2020breathing.pdf)) [A]. | Not available in Kokoro. |

**[R] Soft defaults if the A/B test is run:** a pool of at least 8 inhalations from one CC0 or self-recorded source, 350-550 ms long, never the same sample twice in a row; placed only at paragraph starts (about one in three) and after sentences over ~22 words; never before a `[think]` or a segment heading; level roughly 18-24 dB below average speech (my guess, set by ear); a 100-150 ms gap between breath and speech onset (Elmers used ~150 ms, from natural phrase-initial breaths). The breath replaces part of the paragraph pause, so total gap length stays the same.

### 5.6 What feeds later tickets

- **Ticket 09 (voice audition), what to listen for:**
  1. Judge passages of at least two to three minutes, ideally a full segment of research/05 7.1, never single sentences (Clark et al.).
  2. A/B: fixed pauses (prototype) vs the 5.4 distributions. Does the paragraph gap still sound like a metronome?
  3. A/B: sentence-per-chunk vs pairing very short sentences into one chunk. Which has less repeated contour (A4)?
  4. A/B: speed jitter on vs off; key-information slowdown audible or not?
  5. A/B: no breaths vs breath samples (5.5). Count how often the breath is noticed as a breath.
  6. Listen at minute 15 of a long render, not only the start: fatigue makes uniformity worse [C].
  7. Mispronunciations per minute in the harder passage (numbers, acronyms, terms), as already asked in 09's amendments.
  8. Questions and exclamations: does Kokoro's question intonation sound natural, and does "!" sound performed?
  9. Record all pause, speed and breath settings with the verdict, as 09's amendment 3 already asks.
- **Ticket 14 (pronunciation):** phoneme substitution via `is_phonemes=True` is the confirmed route; the lexicon entry format should allow an espeak phoneme string as well as a respelling. Add a low-priority experiment: whether editing stress marks in phonemes changes emphasis audibly. Mispronunciation found in feedback feeds the lexicon (ticket 16).
- **Ticket 07 (Bundle and markup):** see section 10. The Script markup needs nothing new for v1: pause classes are derived from punctuation, paragraphs, headings and the existing `[beat]` and `[think]`. What 07 must carry is the pacing config (pipeline side), a way to mark load-bearing sentences (the claim tags already do this if the ledger marks load-bearing lines), and the lint report.

---

## 6. Interface layer: Feed, titles, descriptions, show notes, archive page

### 6.1 Named interface tells

| Id | Tell | Looks like | Fix |
|---|---|---|---|
| I1 | Hype or clickbait titles | "The Shocking Truth About Coffee", "Unlocking Better Sleep", "Everything You Need to Know About..." | Say what the listener gets, plainly: "When to stop drinking coffee" (research/05 9.1). Apple: titles brief, specific and unique ([Apple](https://podcasters.apple.com/support/867-featured-present-your-podcast), [F]). |
| I2 | Formula titles | "Caffeine: Myths, Facts, and the Science of Sleep" (colon subtitle plus a title-case triple) | One clause, sentence case. With 08's `Episode N:` prefix, never a second colon. |
| I3 | Template descriptions | "In this episode, we explore...", "Join us as we dive into...", "Discover how..." | Lead with the most interesting specific claim (Apple: "Lead with your most eye-catching, important information"). Two or three sentences, research/05 9.1. |
| I4 | Description that repeats the title | Title "When to stop drinking coffee"; description "This episode is about when to stop drinking coffee." | The description adds the surprise and the promise. |
| I5 | Listicle show notes | Bold-led bullets, emoji, "Key Takeaways", "Conclusion", title-case headings | Plain short paragraphs; the protocol as a short numbered list only where order matters; sources with tiers. |
| I6 | Boilerplate repeated in every episode | Identical opening sentence across show notes; identical "About this show" paragraph in each episode | Show-level text lives once, in the Feed's channel description (ticket 12). The cross-episode n-gram check covers summaries and show notes. |
| I7 | Over-claiming metadata | A title promising a cure, a description promising what the episode does not deliver | Apple's content guidelines require metadata to "accurately represent" the content and forbid influencing search with inaccurate terms ([Apple guidelines](https://podcasters.apple.com/support/891-content-and-subscription-guidelines), [S: wording via search summary]). Candidate firm rule F4. |
| I8 | Fake engagement | "Don't forget to subscribe!", "Let us know in the comments", "See you next week" | There are no comments and no schedule. Never write a call to action that isn't true. Candidate firm rule F3. |
| I9 | Marketing archive page | "Welcome to our podcast!", "Discover fascinating stories", hero banner text, "Stay tuned for more" | A plain list: Episode title, date, one-line summary, duration, link. One short sentence at the top that says what the show is. |
| I10 | Uniform evidence boilerplate | Every source line ending "This study highlights the importance of..." | Sources are references, not commentary: author, year, title, venue, link, tier, read depth. |

### 6.2 Do and don't

| Don't | Do | Why |
|---|---|---|
| Episode 12: Unlocking the Secrets of Caffeine and Sleep | Episode 12: When to stop drinking coffee | I1, I2; says what the listener gets. |
| In this episode, we dive deep into the fascinating world of caffeine and explore how it affects your sleep. | A coffee at four can cost you sleep at eleven, even if you fall asleep fine. Here's how long caffeine really lasts, and how to pick your own cut-off time. | I3; leads with the surprise. |
| **Key Takeaways** ✨ / - **Timing matters:** Caffeine has a long half-life... | Stop caffeine about 8-9 hours before bed. That's the estimate from a 2023 review of 24 studies (Gardiner et al.). If you're pregnant or on certain medicines, the cut-off is earlier, so ask your doctor or midwife. | I5; written form with exact numbers (research/05 9.1). |
| Thanks for listening! Don't forget to subscribe and leave a review. | (nothing) | I8; there is nowhere to leave one, and the owner already follows the show. |
| Welcome to our podcast, where curiosity meets science! | Plainly explained episodes on whatever I'm curious about, researched and sourced. Written and voiced by software. | I9. The second sentence is a disclosure the owner may or may not want (owner question 6). |

### 6.3 Rules

1. Titles: sentence case, one clause, no colon after the `Episode N:` prefix, no hype words (the C2 list plus "secret", "shocking", "ultimate", "everything you need to know"), soft target under ~60 characters (research/05 9.1).
2. Summary: two or three sentences, the first carrying a specific sourced claim, no "In this episode".
3. Show notes: risk line first if flagged (research/05 2.5); then the summary; then the protocol or key points with exact numbers; then sources. No bold, no emoji, no headings beyond `Sources`. Spelling British (research/05 12.9). Show notes may use digits and units, so the Script's TTS lint does not apply, but the phrase lint does.
4. Archive page: generated list, no marketing copy, one plain sentence of description.
5. Parts: titles state each Part's subtopic, never "Part 2: The Shocking Conclusion" (no cliffhangers is firm already).

---

## 7. Build layer: code, comments, names, commit messages, logs and docs

### 7.1 Named build tells

| Id | Tell | Looks like | Fix | Source |
|---|---|---|---|---|
| B1 | Comments that narrate | `# Loop over the chunks` above a loop | Comment only why: a reason, a constraint, a measured fact ("# kokoro-onnx 0.6.1 only pauses at batch joins with this model, so we add our own"). | Google: comments should "explain why some code exists", not "what some code is doing" ([eng-practices](https://google.github.io/eng-practices/review/reviewer/looking-for.html)) [F] |
| B2 | Docstrings everywhere | Every function with a docstring restating its name and arguments; banner comments | Docstrings for public entry points and anything surprising. | Same |
| B3 | Generic names | `data`, `result`, `process_data`, `handler`, `manager`, `utils.py`, `helpers.py` | Domain names from `GLOSSARY.md`: `render_chunk`, `pause_after`, `bundle`, `claim_ledger`. | Google: a good name is "long enough to fully communicate what the item is or does" [F] |
| B4 | Over-abstraction | An abstract `TTSEngine` base class with one implementation, factories, plugin registries, config for values that never change | One small `synthesise(text, voice) -> audio` seam (research/03 already asks for that), nothing more until a second engine exists. | Google: over-engineering is code "more generic than it needs to be"; solve the future problem "once it arrives" [F] |
| B5 | Defensive bloat | `try/except Exception: pass`, retries around pure functions, validating states that cannot occur | Fail loudly in CI; catch only errors you can act on. | [K] |
| B6 | Duplicated blocks | Near-identical functions for each segment kind | Extract when the third copy appears. GitClear reports copy-pasted lines rising and moved (refactored) lines falling as AI assistants spread ([2024 report summary](https://visualstudiomagazine.com/articles/2024/01/25/copilot-research.aspx)) [S]. GitClear sells analytics, the data is correlational, and Google's DORA 2024 reached a different conclusion, so treat it as weak. | [S] |
| B7 | Commit messages that list instead of explain | "Update files", "Refactor code for better readability and maintainability", a bullet per changed file, emoji, "This commit adds..." | Short imperative subject (soft ~50 characters, `area: ` prefix optional), body explaining the problem and why this fix. | Git: "Describe your changes in imperative mood"; the body should "explain the problem the change tries to solve" and "justify the way the change solves the problem" ([SubmittingPatches](https://git-scm.com/docs/SubmittingPatches)) [F] |
| B8 | Chatty logs | "🚀 Starting the amazing render process...", "✅ Successfully completed!" | Terse, factual, with numbers: `render: 214 chunks, 1,412 s audio, RTF 0.48`. | [C] |
| B9 | Brochure docs | README with badges, "✨ Features", "seamlessly", "comprehensive", empty "Contributing" for a one-person repo | Say what it does, how to run it, where things live. Short. | [C]; Wikipedia's formatting tells apply to Markdown docs too |
| B10 | Leftovers | Commented-out code, unused parameters, TODOs with no owner, dead config keys | Delete; git keeps history. | Git: no commented-out debugging code in patches [F] |
| B11 | Claims nobody checked | Commit body "All tests pass", log "verified", docs "fully tested" when they weren't run | Say only what was run. Candidate firm rule F9 (honesty). | [R] |

### 7.2 Rules

1. Names come from the glossary. A new domain word goes into `GLOSSARY.md` first.
2. Comments explain why; no comment restates code.
3. No abstraction until the second real use. The TTS seam is the one exception, because swapping engines is a stated requirement.
4. Commit messages: imperative subject, a body that says why when the change isn't obvious, no file lists, no emoji, attribution lines as the repo requires.
5. Logs: one line per stage with counts and timings; errors say what failed and on which input (chunk index, Episode id).
6. Docs: one README that a person could read in two minutes; spec decisions live in `wayfinder/`, not repeated in code docs.
7. The phrase lint (section 9) runs over READMEs, commit messages in CI (optional) and log message strings, warning only.

---

## 8. Checklist

### 8a. Firm rules (owner sign-off, 2026-10-29)

**Signed off 2026-10-29: all of F1-F9 are firm**, with two adjustments. F4 is checked by the Skill, not the Pipeline. F6 keeps the speed bounds and pause clip ranges, but its 6 s silence bound is replaced by ticket 15's firm 3 s silence gate.

Limited to accuracy, honesty and TTS safety, plus one slop ban I judge essential. Rules already firm in research/05 12.2 are not repeated (no invented experience, every claim traceable, no digits or symbols in spoken text, no padding, no cliffhangers, no standing disclaimer). None of the following is firm until the owner says so.

| Id | Firm rule | Protects | Status |
|---|---|---|---|
| F1 | No unattributed evidence claims: "studies show", "research shows/confirms", "experts/scientists say/agree", "some argue" are blocked unless the same sentence names the kind of evidence and carries a claim tag. | Accuracy (ticket 06) | Signed off 2026-10-29 |
| F2 | No first-person memory or experience phrases in the Script ("when I tried", "I remember", "my clients/listeners/friends"), checked mechanically, with a one-line override in the Bundle for a genuine reasoning use ("I remember the study said..." is not allowed; "Here's how I'd read that" is). | Honesty (makes an existing firm rule mechanical) | Signed off 2026-10-29 |
| F3 | No false calls to action or interface claims in Script, show notes or Feed: subscribe, review, comment, "link in the description" unless true, "see you next week" or any promised schedule. | Honesty | Signed off 2026-10-29 |
| F4 | Titles and summaries never promise more than the Episode delivers, and never state a claim the ledger does not support. Checked by the Skill (J); the Pipeline only checks the banned hype words. | Honesty, Apple metadata rules | Signed off 2026-10-29 |
| F5 | No scripted fillers, laughter or stage directions in spoken text ("um", "uh", "haha", "[laughs]", "*sighs*"). | TTS safety (rendered literally) | Signed off 2026-10-29 |
| F6 | Pipeline safety bounds: per-chunk speed within 0.90-1.10 of the voice's base speed; no silence longer than 6 s anywhere; no pause class outside its clip range. | TTS engine safety; no "broken file" dead air | Signed off 2026-10-29 |
| F7 | Any breath or audio sample used has a recorded licence (CC0 or self-recorded) in the repo. | Honesty and licensing | Signed off 2026-10-29 |
| F8 | Commit messages, logs and docs do not claim a test, check or verification that was not run. | Honesty | Signed off 2026-10-29 |
| F9 | (Essential slop ban, my judgement.) Should research/05 5.5's existing "Never" list block the run, or only warn? I suggest blocking only this core of ten that are both empty and unmistakable: "let's dive in", "dive deep", "delve", "in today's episode", "welcome back", "without further ado", "buckle up", "great question", "it's important to note", "it's worth noting". | Human feel (the owner's top priority for this ticket) | Signed off 2026-10-29 |

### 8b. Soft guidance (±25% leniency on every number)

Content
1. Each segment carries one sourced surprise, one specific detail, and one consequence for the listener (section 3).
2. The host commits to a view at least once per episode and says once where it is unsure.
3. Sentence-length spread: coefficient of variation per segment around 0.45 or more; warn below 0.35 (section 9).
4. At least one sentence of five words or fewer per ~150 words; one-sentence paragraphs allowed.
5. "X, Y and Z" triples: at most about 4 per 1,000 words; "three things" announced at most twice per episode.
6. No paragraph-opening word used for more than ~15% of paragraphs; never the same opener twice in a row.
7. Contrast device ("Not X. Y.") at most once per episode.
8. Same lead-in never twice in an episode, for recall prompts, listener questions and signposts.
9. No six-word run shared with the last ten Bundles in the Hook, Roadmap, signposts, prompts or Sign-off.
10. Asides as their own sentence, one or two an episode.
11. Humour only from the material; zero to two light moments.
12. Hedges: one per claim; never three hedge words in one sentence.
13. Evidence phrases: the tier is fixed; the wording rotates within the tier's mapped pool.
14. Vary the internal order of content segments; keep the question bookends.

Audio
15. Pauses drawn per class from 5.4; seeded by Episode id.
16. One chunk per sentence; Pipeline owns all inter-chunk silence; 5-10 ms edge fades.
17. Speed jitter ±0.025 per chunk, 0.95 for key-information chunks.
18. Breaths off until ticket 09's A/B says otherwise.

Interface
19. Titles in sentence case, one clause, under ~60 characters, no hype words.
20. Summary leads with the specific claim, two or three sentences.
21. Show notes without bold, emoji or "Key takeaways".
22. Archive page plain.

Build
23. Glossary names; why-comments; no abstraction before the second use; imperative commit subjects around 50 characters with a why-body; terse numeric logs; short README.

---

## 9. Proposed cheap lint and review step

### 9.1 Where it runs and what it may do

| Stage | Runs | Blocks on | Warns on | Cost |
|---|---|---|---|---|
| Skill, before emitting the Bundle | Mechanical pass on Script, summary, title and show notes; then the self-review rubric (9.5) | Only rules already firm (research/05 12.2) and any section 8a rule the owner makes firm | Everything else | Mechanical: milliseconds. Rubric: one extra read of a ~4,000-word Script inside the Skill session; cost belongs to ticket 13. |
| Pipeline, before TTS | Mechanical pass on the Script only (same code, versioned) | Firm rules (TTS safety, claim tags, plus approved 8a items) | Style warnings copied into the run log | Milliseconds; no LLM. |
| Pipeline, before publish | Interface pass on title, summary, show notes; the F6 audio bounds on the render plan | Firm rules only | Style warnings | Milliseconds. |

Per research/05 12.2, a soft warning exceeded by more than 25% asks the Skill to fix it or justify it in one line. The justifications go into the Bundle's `lint_report` so the owner can see them and ticket 16 can tune the lists.

### 9.2 Starter phrase lists (case-insensitive regex; warn unless marked)

**Banned openers** (first sentence of the Hook, and the first sentence of any segment):
```
^(have you ever|ever wondered|imagine a world|in a world where|picture this|what if i told you|did you know|hello and welcome|welcome( back)?( to)?|hey there|today,? we|in today'?s|let'?s (start|begin|dive|get))
```

**P1 Openers, closers and fake engagement** (F9 core and F3 candidates marked):
```
let'?s dive in [F9] | dive (deep|into) [F9] | in today'?s episode [F9] | welcome back [F9] | without further ado [F9] | buckle up [F9]
in conclusion | to sum up | in summary | in short, | that'?s a wrap | until next time | stay tuned
thanks for (listening|tuning in) | (don'?t forget to |please )?(subscribe|leave a review|rate (us|the show)) [F3] | let (us|me) know in the comments [F3] | see you next (week|time) [F3] | link in the (description|show notes) [F3, allowed if true]
```

**P2 Vocabulary** (each hit listed; warn harder at three or more distinct words per episode):
```
delv(e|es|ed|ing) [F9] | tapestry | intricac(y|ies) | intricate | underscor(e|es|ed|ing) | pivotal | crucial | paramount | realm
landscape (figurative) | testament | showcas(e|es|ed|ing) | foster(s|ed|ing)? | leverag(e|es|ed|ing) | navigat(e|es|ing) (figurative)
robust | seamless(ly)? | multifaceted | nuanced | vibrant | embark | unlock | unleash | supercharge | game[- ]?changer | groundbreaking
revolutioni[sz]e | meticulous(ly)? | palpable | camaraderie | interplay | holistic | synergy | elevate | empower | boasts? | nestled
ever[- ]evolving | in the heart of | plethora | myriad | hack | biohack | secret | life[- ]changing | treasure trove | beacon
```
"Landscape" and "navigate" are literal in some topics (geology, sailing); the warning lists them for the Skill to judge.

**P3 Constructions:**
```
(serves|stands|acts) as (a|an|the)                                  # C3
plays an? (crucial|key|pivotal|vital|significant|important) role     # C7
a (testament|reminder) (to|of)                                       # C7
it'?s (important|worth) (to note|noting|mentioning|remembering) [F9] # filler
\bnot (just|only|merely) [^.]{1,60}\bbut( also)?\b                   # C4
\bit'?s not [^.]{1,50}[,.] it'?s\b                                   # C4
, (highlighting|underscoring|emphasi[sz]ing|showcasing|reflecting|ensuring|fostering|illustrating) # C6
the (truth|reality) is | at the end of the day | let that sink in | make no mistake | the bottom line is | here'?s the (kicker|catch)
when it comes to | despite (these|the) challenges | the future (looks|is) bright | only time will tell     # C16
(studies|research|experts|scientists) (show|shows|say|suggest|agree|confirm)  [F1 if no claim tag in the sentence]
some (people|experts|critics|researchers) (say|argue|believe|claim)          [F1 if no claim tag]
(great|good|excellent|fantastic) question [F9 for "great question"] | (fascinating|amazing|incredible|mind-blowing)!?
(ultimately,? )?it (all )?depends | pros and cons                                                     # C17
\b(may|might|could|possibly|potentially|perhaps|arguably|seemingly)\b  (three or more in one sentence) # C9
when i (first )?(tried|started|did)|i remember (when|the first)|my (clients|listeners|patients|friends) [F2]
\b(um|uh|erm|haha)\b | \[(laughs?|sighs?|pause|music)\] | \*[a-z ]+\*                                 [F5]
```

**P4 Meta-talk:**
```
in this (section|segment|part|episode),? (we|i)('ll| will) | as (we|i) (mentioned|discussed|said|saw) (earlier|before|above)
now,? let'?s (turn|move|look|talk|shift) | let'?s (take a (closer )?look|explore|unpack|break (it|this) down) | first and foremost
```

**P5 Show notes and docs only:**
```
[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]          # emoji
^\s*[-*]\s*\*\*[^*]+\*\*:?                       # bold-led bullets
key takeaways? | ^#+ .*conclusion | ^#+ (\w+ ){1,}\w+$ with every word capitalised   # title-case headings
```

### 9.3 Structure checks (soft thresholds)

Spoken text is the Script with headings, claim tags and markup stripped. Thresholds were sanity-checked on the two scripts in this repo [M]: research/05 7.1 (54 sentences, mean 9.8 words, SD 5.0, CV 0.51, ten sentences of five words or fewer, three runs of four similar-length sentences, about 3.8 triples per 1,000 words) and the audition sample (28 sentences, mean 12.3, SD 7.3, CV 0.59). Both pass every threshold below, which is the intent: they are the hand-written baseline.

| Check | Measure | Warn when |
|---|---|---|
| S1 Sentence-length spread | CV (SD / mean of words per sentence) per segment | below 0.35 |
| S2 Flat runs | consecutive sentences each within ±3 words of the previous | five or more in a row |
| S3 Short sentences | sentences of five words or fewer | none in a content segment |
| S4 Triples | "X, Y(,) and Z" with items of one to four words | over ~4 per 1,000 words, or two in one paragraph |
| S5 Count announcements | "three (things|ways|reasons|ideas)" | more than two per episode |
| S6 Paragraph openers | first word of each paragraph | one word opens over ~15% of paragraphs, or the same opener twice in a row |
| S7 Paragraph closers | last sentence starts "So", "That's why", "Which means", "And that's" | over ~40% of paragraphs |
| S8 Colons | Script: per segment (research/05 6.2 rule 8 already); show notes: per 100 words outside the source list | Script over one per segment; notes over one per 100 words |
| S9 Dashes | em and en dashes | Script: already blocked (TTS firm rule); show notes and docs over one per 200 words |
| S10 Questions | question marks per segment | over one per ~40 words in a segment, or none in the whole episode |
| S11 Exclamations | per segment | over one (research/05 already) |
| S12 Lead-in repetition | first three words of recall prompts, listener questions and signposts | any repeat inside the episode |
| S13 Cross-episode repetition | 6-word shingles of Hook, Roadmap, signposts, prompts, Sign-off, summary and show-notes opening, against the last ten Bundles in git | any shared 6-word run, excluding segment headings, evidence-tier phrases and quoted titles |
| S14 Nominal density | words ending -tion, -ment, -ness, -ity, -ance, -ence per sentence | three or more in one sentence |
| S15 Intensifiers | very, really, incredibly, truly, deeply, highly, extremely | over ~6 per 1,000 words |

S13 costs nothing extra: Bundles are kept in git (ticket 08). It is the only check that sees the template creeping in across episodes, which is the tell the owner is most likely to notice by Episode 10.

### 9.4 Versioning

The phrase lists and thresholds live in one versioned file (for example `deslop_rules.yaml`) with a `deslop_version` recorded in each Bundle next to `style_guide_version`. Because tells drift (Kobak; Wikipedia's dated lists), the owner or a Learnings entry (ticket 10) can add words, and ticket 16 can retire warnings that keep being justified away.

### 9.5 Self-review rubric for the Skill (one pass, before emitting)

The Skill answers each question about its own draft, fixes what it finds, and records any warning it keeps with a one-line reason in `lint_report`.

1. Read the Hook cold. Could its first two sentences open an episode on a different topic? If yes, rewrite around this topic's specific fact.
2. For each segment, name the one surprising, sourced fact. If you can't, merge or cut the segment.
3. Where does the host commit to a view, and where does it say it is unsure? If neither appears, add them, labelled as inference where they are.
4. Find every sentence that only announces what is coming or restates what was said, outside the planned recap. Cut it or give it content.
5. Is any example generic enough to fit three other topics? Replace it with a sourced case or add a topic-specific detail.
6. Do two segments share the same internal order? Change one.
7. Read three random paragraphs as if aloud. Does any sound like a press release, a textbook or a chatbot reply? Rewrite in plain speech.
8. Is there a joke, pun or "fun fact" frame that the material didn't earn? Cut it.
9. Check honesty: any invented experience, number, quote or name; any evidence phrase stronger than its ledger tier; any call to action that isn't true.
10. Is the same noun used for the same thing throughout, with no synonym cycling?

---

## 10. Open questions and interfaces

### 10.1 Questions for the owner

**Answered 2026-10-29.** 1: all of F1-F9 firm (see 8a). 2: block on the ten-phrase core only, warn on the rest. 3: breaths off in v1, revisit by A/B once a licensed set exists. 4: settled by ticket 09 (drawn gaps and jitter on). 5: zero to two light moments, from the material. 6: settled by ticket 12. 7: as proposed. 8: yes, the softenings are applied in research/05 12.11. 9: settled by ticket 12 (`Episode N: Title` kept). 10 and 11: settled by ticket 07. 12: settled by ticket 07 (Python, ruff).

1. Which of the section 8a candidates (F1-F9) should become firm? Each is independent.
2. F9: should research/05 5.5's "Never" list block a run, or warn? If block, is the ten-phrase core right, or should the whole list block?
3. Do you want to hear breath samples in the voice audition (ticket 09), knowing the measured benefit is small and the risk of sounding fake is real?
4. After hearing it, should varied pauses and speed jitter be on by default?
5. Humour: zero to two light moments an episode, from the material only. Too much, too little, or none at all?
6. Should the show's channel description say plainly that the episodes are researched, written and voiced by software? It is honest and reads as human; it is also optional for a private-ish feed (ticket 12).
7. How strong may the host's point of view be? The proposal is: commit on evidence and practical choices, stay balanced on contested values and politics (ticket 06).
8. Should research/05's own example devices be softened as in section 4 (rows 1, 3-6, 9-14)? That is an edit to an owner-approved file, so it needs your yes.
9. Ticket 08's `Episode N: Title` conflicts with Apple's advice to keep numbers out of titles. Keep it, or revisit in ticket 12?
10. May the lint read the last ten Bundles from git for the cross-episode repetition check (S13)?
11. Where should lint warnings reach you: only in the Bundle, in the confirm message, or in a short post-publish line?
12. Build: which language and formatter for the Pipeline (for example Python with one formatter and linter), so the build rules in section 7 have a concrete home?

### 10.2 What each later ticket must pick up

| Ticket | Must pick up |
|---|---|
| **07** Bundle contract and pipeline | Bundle fields: `lint_report` (warnings, justifications, `deslop_version`); ledger tags `surprise` and `load_bearing` alongside `misconception`. Pipeline config block `pacing` (pause classes, distributions, clip ranges, speed jitter, key-information slowdown, breath on/off and sample pool), seeded by Episode id. Pause ownership: chunk per sentence, `trim=True`, Pipeline adds all inter-chunk silence, so nothing stacks. No new Script markup in v1 beyond research/05 6.3. Lint runs at the three points in 9.1. |
| **09** Voice audition | The listening list in 5.6: long passages, A/B of pause distributions, chunk pairing, speed jitter and breaths; listen at minute 15; record settings with the verdict. |
| **12** Show identity | Interface rules in section 6; channel description wording (owner question 6); the `Episode N:` vs Apple question (owner question 9); archive page copy. |
| **14** Pronunciation | Phoneme substitution through `is_phonemes=True`; lexicon entries that accept espeak phonemes; optional stress-mark emphasis experiment; F5 (no fillers or stage directions) in the TTS lint. |
| **15** Testing and quality gates | The mechanical lint (9.2-9.3) as the first automated gate, firm items blocking and the rest warning; F6 bounds on the render plan; the speech-to-text round trip also catches literal "um" or bracket text reaching the audio. |
| **16** Feedback | How owner reactions add or retire phrases and thresholds (`deslop_version`); "this sounded robotic at 12:40" as a feedback type that points to a chunk and its pause and speed values. |

---

## Gaps and limits

- No study tests AI-writing tells in spoken scripts, or listener reactions to them in a podcast. Section 2 extrapolates from written prose.
- The pause defaults rest on one 2002 corpus study, plus TTS phrase-break studies on other engines. None of it is Kokoro. Ticket 09's ears decide.
- Breath-group figures (section 5.3) are search-summary level.
- Fraundorf & Watson 2011 was not read at source; its claim is reported via citing papers.
- Apple's content-guideline wording on accurate metadata came through a search summary; the "Present your podcast" page was read directly.
- The Wikipedia guide was read for about the first 200,000 of 250,000 characters.
- NPR's own writing guide ("The Journey from Print to Radio Storytelling") was not found at source; the NPR points here come from one NPR Training page and secondary summaries of Kern's *Sound Reporting*. I found no BBC Academy page on writing for the ear, so no BBC guidance is cited.
- The soft thresholds in 9.3 were checked only against two hand-written samples in this repo. They should be recalibrated on the first five real Bundles.

## Sources

- Kobak, González-Márquez, Horvát & Lause (2025), *Science Advances* 11(27), doi:10.1126/sciadv.adt3813. [arXiv html v5](https://arxiv.org/html/2406.07016v5) [F, results]; [abstract](https://arxiv.org/abs/2406.07016v5)
- Reinhart et al. (2025), "Do LLMs write like humans?", *PNAS*, doi:10.1073/pnas.2422455122. [arXiv html](https://arxiv.org/html/2410.16107v2) [F, results]
- Muñoz-Ortiz, Gómez-Rodríguez & Vilares (2024), *Artificial Intelligence Review*, doi:10.1007/s10462-024-10903-2. [arXiv](https://arxiv.org/abs/2308.09067) [A]
- Juzek & Ward (2025), COLING. [arXiv](https://arxiv.org/abs/2412.11385v1) [A]
- Russell, Karpinska & Iyyer (2025), ACL. [arXiv](https://arxiv.org/abs/2501.15654) [A]
- Liang et al. (2024/2025), mapping LLM use in scientific papers. [arXiv](https://arxiv.org/abs/2404.01268v1) [S; not used for any number here]
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) [F, most of the page]
- Campione & Véronis (2002), "A large-scale multilingual study of silent pause duration", Speech Prosody, 199-202. [PDF](https://mail.sprosig.org/sp2002/pdf/campione-veronis.pdf) [F]
- Elmers, Werner, Muhlack, Möbius & Trouvain (2021), "Take a breath", Interspeech, 3196-3200, doi:10.21437/Interspeech.2021-1496. [PDF](https://www.coli.uni-saarland.de/~trouvain/docs/Elmers_et_al_2021b.pdf) [F]
- Whalen, Hoequist & Sheffert (1995), *JASA* 97(5), 3147-3153, doi:10.1121/1.411875 [S, via Elmers]
- Székely, Henter, Beskow & Gustafson (2020), "Breathing and speech planning in spontaneous speech synthesis", ICASSP. [PDF](https://www.speech.kth.se/tts-demos/szekely2020breathing.pdf) [A]
- Futamata et al. (2021), Interspeech. [ISCA](https://www.isca-archive.org/interspeech_2021/futamata21_interspeech.html) [A]
- Vadapalli (2025), *SN Computer Science* 6(2):91. [arXiv 2304.04157](https://arxiv.org/abs/2304.04157) [A]
- Clark, Silen, Kenter & Leith (2019), "Evaluating long-form text-to-speech", SSW. [ISCA](https://www.isca-archive.org/ssw_2019/clark19_ssw.html) [A]; [Google blog](https://research.google/blog/assessing-the-quality-of-long-form-synthesized-speech/) [S]
- Fraundorf & Watson (2011), *JML* 65(2), 161-175, doi:10.1016/j.jml.2011.03.004 [S]; Muhlack et al. (2021), [PDF](https://www.coli.uni-saarland.de/~trouvain/docs/Muhlack_et_al_2021.pdf) [S]
- Breath-group figures: [Yoo & Shin 2020 (Korean)](https://koreascience.kr/article/JAKO202010163509326.pdf), [German spontaneous speech summary](https://reading.readthedocs.io/ja/latest/LanguageAcquisition/TheInterplayOfLinguisticStructureAndBreathingInGermanSpontaneousSpeech/main.html) [S]
- kokoro-onnx 0.6.1 source (`__init__.py`, `chunker.py`, `pauses.py`) and model inputs/outputs, inspected locally [M]; [repo](https://github.com/thewh1teagle/kokoro-onnx)
- Ira Glass, Transom manifesto (2004). [Transom](https://transom.org/2004/ira-glass/) [F, first part of the page] [C]
- NPR Training (2016), "Reporter two-ways: how to sound natural, even with a script". [NPR Training](https://training.npr.org/2016/03/23/reporter-two-ways-improvisation-within-a-structure/) [S] [C]
- Writing for the ear summaries: [UBC workshop](https://wiki.ubc.ca/Course:LFS400/Workshops/Writing_For_the_Ear), [JEA on Kern's *Sound Reporting*](https://jea.org/?p=1953) [S] [C]
- Apple Podcasts for Creators: [Present your podcast](https://podcasters.apple.com/support/867-featured-present-your-podcast) [F]; [Content guidelines](https://podcasters.apple.com/support/891-content-and-subscription-guidelines) [S]; [Search](https://podcasters.apple.com/support/3686-search-on-apple-podcasts) [S]
- Git, [SubmittingPatches](https://git-scm.com/docs/SubmittingPatches) [F]
- Google engineering practices, [What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html) [F]
- GitClear 2024 report, via [Visual Studio Magazine](https://visualstudiomagazine.com/articles/2024/01/25/copilot-research.aspx) [S]
- Owner's dissertation voice profile, `OneDrive/Desktop/final_project/uni_plan/drafts/voice_profile.md` (written tells only; the host's voice is not the owner's)
