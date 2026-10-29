# Research 05: Episode template and style guide (owner-approved 2026-10-29)

Ticket: `wayfinder/tickets/05-episode-template-and-style-guide.md`. Drafted 2026-10-29 by opus-agent; grilled with the owner the same day.
Status: **decided**. **Section 12 (owner decisions) and section 13 (source profiles) take precedence over everything else in this file.** Sections 1-10 are the original proposal; where they conflict with section 12 (lengths, word budgets, split rule, recall prompts, segment modes, strictness of limits), section 12 wins. Section 0 has been updated to match.

Inputs: research/01 (length), research/02 (host format, 13 style rules), research/03 (TTS), research/04 (feed), ticket 06 (accuracy standard, decided), the voice audition prototype (`prototypes/voice_audition/`), plus new measurements made for this ticket (section 1). The Opus review of 01-04 and 06 (`research/opus-review-2026-10-29.md`) corrected some evidence those files relied on; this file uses the corrected versions.

Tags: **[M]** measured by me on this machine, 2026-10-29; **[P]** primary source; **[S]** secondary; **[R]** my recommendation.

---

## 0. The template in one screen

*Updated to the owner decisions (section 12). All numbers are soft targets with ±25% leniency unless section 12.2 lists them as firm. Ranges are ceilings, not quotas: the skill stops when the honest content runs out and never pads.*

| | Quick | **Standard (default)** | Deep |
|---|---|---|---|
| Duration range | 8-15 min (typ. ~11) | **15-28 min (typ. ~25)** | 28-35 min (typ. ~35); up to ~44 only if the topic will not split cleanly |
| Word ceiling at 165 wpm | ~2,500 | **~4,600** | ~5,800 (absolute ~7,300) |
| Content segments | 2-3 | **4-5** | 5-7 |
| Closing segment | Protocol, or Why it matters / what to watch | same | same |
| Retrieval design (12.6) | opening question + re-ask per segment; spaced recall from segment 2 | same | same |
| Simulated listener questions | 1-2 | **2-4** | 3-5 |
| Chosen by | the skill proposes, owner confirms in one reply (12.4) | | |

Above ~35 minutes and the topic breaks into standalone subtopics: **split into 2-3 Parts** (12.3). No minimum length anywhere.

Skeleton (Standard): **Hook → Roadmap → Segments (each opens with a spoken preview and its main question, closes with "so what" and the re-asked question) → Protocol or Why it matters (ends in "How sure are we") → Recap (retrieval form) → Sign-off.**

---

## 1. Pace: the number every word budget hangs on

research/02 rule 11 guessed 150-180 wpm; research/03 costed at 150 wpm. Neither was measured. I measured the six prototype renders [M] (345-word `sample_script.txt`, kokoro-onnx 0.6.1, int8, speed 1.0, the prototype's 0.3 s / 0.8 s extra silences on top of kokoro-onnx's default punctuation pauses; quiet frames = 10 ms frames 40 dB below peak):

| Voice | Duration | Overall wpm | Quiet share | Speech-only wpm |
|---|---|---|---|---|
| af_heart | 119.1 s | 174 | 24% | 228 |
| af_bella | 121.9 s | 170 | 25% | 226 |
| am_michael | 130.4 s | 159 | 25% | 211 |
| am_adam | 111.7 s | 185 | 23% | 241 |
| bf_emma | 109.0 s | 190 | 25% | 254 |
| bm_george | 125.2 s | 165 | 23% | 215 |

Median overall rate: about 172 wpm. Spread between voices: ±10%. Pauses of 150 ms or more numbered 40-58 per two minutes, median ~0.47 s, max ~1 s.

Supporting evidence on the ceiling: listening comprehension held at 270 wpm and fell steeply at 315 wpm (Kuperman et al. 2021, *JEP: Human Perception and Performance* 47(8), 1103-1112, doi:10.1037/xhp0000932 [S, abstract]). So comprehension is not the limit at 160-190 wpm; naturalness and the listener's working memory are.

**[R] Budget constant: 165 wpm.** It sits inside the measured range and inside the research/02 range, and errs slightly towards a slower voice so episodes run long rather than short. The template's own extra pauses (three 3 s recall pauses, ~6 section breaks of ~1.5 s) add about 20 s to a Standard episode, which is under 2% and is ignored in the budget.

**[R] Calibration rule:** once ticket 09 picks a voice, the pipeline measures real wpm on the first two full episodes and the budget constant is set to that measured value (rounded to 5). The Bundle records `wpm_budget` and the pipeline records the actual duration, so this needs no owner effort. If the chosen voice runs above 180 wpm (bf_emma, am_adam territory), set Kokoro `speed` to bring it to ~165-170 rather than writing fewer words; check by ear that the slower setting does not smear.

Words per minute to duration, for reference: 1,000 words ≈ 6.1 min at 165 wpm; ≈ 5.6 min at 180; ≈ 6.7 min at 150.

---

## 2. Episode skeleton (Standard, 3,300 words, ~20 min)

### 2.1 Segment table

| # | Part | Words | Clock (165 wpm) | Must contain |
|---|---|---|---|---|
| 0 | **Hook (cold open)** | 110-150 (target 130) | 0:00-0:47 | A concrete, sourced surprise, scenario or question; the **promise sentence** (what the listener will be able to do) by word ~100. |
| 1 | **Roadmap** | 60-100 (target 80) | 0:47-1:16 | The organising frame; the number of segments, said aloud and named; "then a plan, then a recap". Higher-risk caution line here only if the whole episode is higher-risk (section 2.5). |
| 2-5 | **Content segments 1-4** | 4 × 520-600 (target 560) | 1:16-14:52 (~3.4 min each) | Numbered signpost, mechanism or idea, one analogy, one concrete example, inline evidence voicing, at most one simulated listener question, a bridge to practice, a **recall prompt** at the end of segments 1-3 (segment 4 optional). |
| 6 | **Protocol / takeaways** | 420-540 (target 480) | 14:52-17:46 | Every action as **what, how much, when, how to adjust, when not to**; targeted cautions next to the action they qualify; ends with **"How sure are we"** (100-140 words). |
| 7 | **Recap** | 170-230 (target 200) | 17:46-18:59 | Cumulative retrieval: ask, pause, answer, in roadmap order. |
| 8 | **Sign-off** | 30-60 (target 50) | ~19:17 | One concrete thing to try, one line. No boilerplate. |

### 2.2 Budget arithmetic

Hook 130 + Roadmap 80 + Content 4 × 560 = 2,240 + Protocol 480 + How sure are we 120 + Recap 200 + Sign-off 50 = **3,300 words = 20.0 min**.

This fixes an inconsistency in research/01 and the map decision. "4-5 segments of ~4-6 min" is 16-30 minutes of content before the hook, protocol and recap, so it cannot fit a 20-minute episode. Guo et al.'s "under 6 minutes" is a ceiling, not a target. **[R] Read the map decision as "4 content segments of ~3.5 min plus a ~3 min protocol segment, so 5 segments in total".** The total stays in the "4-5 segments" range the owner approved.

### 2.3 Two segment modes (the skill picks one per episode)

Huberman's per-tool pattern (mechanism, then instruction, then adjustment; research/02 section 3) suits practical topics. Explanatory topics ("how vaccines train the immune system") have little to dose. **[R]** Two modes, same budgets:

- **Tool-led** (default for health, training, habits and other "better myself" topics): each content segment is one tool. Inside the segment: why it works (mechanism) → exactly what to do (dose, timing) → how to adjust or when not to. The Protocol segment then becomes "Putting it together", a short first-week plan that orders the tools and resolves clashes between them. It does not repeat each tool's detail.
- **Mechanism-led** (explanatory topics, and any topic where the useful actions only make sense after the whole picture): content segments build understanding in order, and the Protocol segment carries all the actions. For non-health topics it is called "Takeaways": two to four things to do or remember, each concrete.

The sample script in the prototype is mechanism-led.

### 2.4 Inside a content segment (target 560 words)

In this order unless the material demands otherwise:

1. **Signpost in** (10-25 words). Number and name, matching the roadmap: "Idea two. Why caffeine lasts longer than it feels." Vary the phrasing between segments (section 5.6).
2. **Way in** (60-120). A concrete case, a question, or a short scene. For novice-level material lead with a small story (research/02: narrative helps novices; Mar et al. 2021, *Psychon. Bull. Rev.* 28, 732-749, doi:10.3758/s13423-020-01853-1 [S, abstract]).
3. **Mechanism or core idea** (180-260), with **one analogy**. One idea per sentence.
4. **Evidence voicing inline** (20-60), at the load-bearing claim, in the fixed vocabulary of section 2.6.
5. **Simulated listener question or misconception** (60-120), if this segment has one: question, then a direct answer ("Not quite." / "Partly." / "Yes, and it goes further."). Section 2.7.
6. **Bridge to practice** (30-60). What this changes for the listener.
7. **Recall prompt** (30-45), section 2.8.

### 2.5 Where ticket 06's cautious framing and show-notes flag go

Ticket 06 decided: never refuse, never stop to ask; conservative framing plus a specific caution; flag the topic as higher-risk in the show notes; disclaimers optional and never repeated.

**[R] Placement rules:**

- **At the action.** A caution sits in the same paragraph as the instruction it qualifies, directly after the dose or timing. It names who, what risk, and what to do instead: "If you take blood pressure medication, don't add this without asking your doctor, because it can lower pressure further." Not "consult a professional".
- **In the roadmap, once, only for a higher-risk episode.** One sentence: "One caution before we start. The fasting part of this episode isn't for anyone with diabetes or a history of eating disorders, and I'll say why when we get there." Never in the hook: the first 60-90 s is where listeners decide to stay (research/01, Wiblin [S]).
- **Nowhere else.** No standing disclaimer at the top or bottom. research/02 rule 5 ("keep a short standing disclaimer") is superseded by ticket 06.
- **In the Bundle:** `risk_flag: higher` plus a one-line `risk_reason`. The show notes open with "Higher-risk topic: <reason>." (interface to 07).
- **Higher-risk** means: the protocol involves medication, supplements with known interactions, fasting, extreme training loads, heat or cold exposure, pregnancy, mental-health crises, or any action where a plausible mistake causes harm. The skill decides; when unsure it flags.

### 2.6 Evidence-strength voicing (links ticket 06's ladder to spoken words)

Every load-bearing claim (a claim the advice depends on) gets one evidence phrase, once, at the claim. Background facts do not need one. Use this vocabulary so the claim-check can compare it to the ledger tier:

| Ledger evidence | Say | Never say |
|---|---|---|
| Tier 1: systematic review or meta-analysis, consistent | "This is well supported. A review pooling twenty-four studies found..." | "Science has proven" |
| Mechanism with textbook consensus (see review amendment to 06) | "This part is textbook. It's been understood for decades." | |
| Tier 2: RCTs, major guidelines | "Good trials show..." / for one small trial: "One small but careful trial found..." | "Studies show" with no qualifier |
| Tier 3: single studies, expert reviews | "Early evidence." / "One study suggests." | "Research confirms" |
| Mixed or conflicting | "The evidence is mixed. On one side... On the other..." | Picking a side without saying so |
| Animal or cell work | "In mice." / "In cells in a dish, not yet in people." Said in the same sentence as the finding. | Putting the species in a later sentence |
| Tier 4: books, commentary | Context only: "The author argues..." Never as evidence. | |
| No source, host's reasoning | "This is my inference, not a finding." | Stating it as fact |

Size and population matter as much as tier: a twelve-person trial is tier 2 but is voiced as small. Say who was studied when it limits the advice ("in young men", "in people with insomnia").

**"How sure are we"** (end of the Protocol segment, 100-140 words): the strongest claim the advice rests on, the weakest link, and what new evidence would change the advice. This is the only place the episode steps back to talk about evidence as a whole.

### 2.7 Simulated listener questions (research/02 rules 7-8)

- 2-4 per Standard episode, at most one per segment. Each must be a real misconception or objection found while researching (the ledger can tag a line `misconception`), not filler.
- Form: a direct question ending in a question mark, without quotation marks. "Now, you might be wondering, if I feel sleepy at bedtime anyway, isn't the caffeine gone?" Then answer at once.
- Vary the lead-in: "You might be thinking...", "A fair question here is...", "If you're like most people, you've heard...", "The obvious objection is...". Never the same lead-in twice in an episode.
- The answer starts with a verdict word or short sentence ("Not quite." "Partly." "Yes.") and then the reason. Real error correction, not "Great question".

### 2.8 Recall prompts

Evidence (corrected in the Opus review of research/01): interpolated tests cut mind-wandering and improved learning in a 21-minute video lecture (Szpunar et al. 2013, *PNAS* [P, full text]), and helped integration in a 40-minute lecture (Jing et al. 2016 [S]). A larger replication (Welhaf et al. 2022, *Cogn. Res.*, N = 195 [S]) found only a small, uncertain drop in mind-wandering and no learning benefit. Szpunar's tests were two-minute typed quizzes; **restudy (seeing the answers again) did not help**. A spoken prompt to a listener on a walk is weaker than either. The prompts are cheap and plausible, not proven.

**[R] Rules that follow from this:**

- A recall prompt is **retrieval, not restatement**. Question first, then a `[think]` pause (~3 s), then the answer. Never give the answer before the pause.
- One question per prompt, answerable in a few words. Answer in at most 25 words.
- Standard: after segments 1, 2 and 3 (segment 4 optional). Quick: one, after segment 2. Deep: after segments 1-4.
- Lead-ins vary: "Quick check before we move on.", "Before I go on, see if you can answer this.", "Pause here for a second." Don't tell the listener to pause the app: the `[think]` pause does that.
- The **Recap** is a cumulative retrieval round: "So, idea one. What does caffeine do to the sleep signal? [think] It hides it..." For each item in roadmap order. In a Quick episode the recap can be plain restatement to save words.
- If the owner finds them annoying, cut to one per episode before cutting them altogether (owner question 7).

### 2.9 Hook rules

- Starts at 0:00 with content. No "Welcome", no show name, no "In today's episode".
- One of: (a) a surprising, sourced fact; (b) a relatable scenario with a twist; (c) the question the listener has probably asked themselves. The fact carries a claim tag like any other.
- Contains the **promise sentence** by word ~100, phrased as a capability: "By the end of this episode, you'll know when your last coffee should be." Vary the wording across episodes.
- No caveats, no disclaimers, no sources by name.

### 2.10 Sign-off rules

30-60 words. One concrete thing to try, ideally with a time frame ("Try it for one week"). Optionally one sentence pointing to a related existing Episode. No "thanks for listening", no "subscribe", no fixed catchphrase in v1 (owner question 10). For Part 1 of a split topic, the sign-off ends with a one-line teaser for Part 2.

---

## 3. Variants

### 3.1 Quick (~11 min, 1,800 words)

Hook 100, Roadmap 50, 3 content segments × 420 = 1,260, Takeaways 220 (with a two-sentence "How sure are we"), Recap 130, Sign-off 40 = 1,800.
Use for narrow topics with two or three core ideas ("Is stretching before running useful?"), or when the owner asks. Not below ~9 minutes: research/01 found nothing that rewards short length, and the tool's value is a full sourced explanation.

### 3.2 Standard (~20 min, 3,300 words)

Section 2. The default.

### 3.3 Deep (~27 min, 4,400 words)

Hook 150, Roadmap 100, 5 content segments × 600 = 3,000, Protocol 480 + How sure are we 120 = 600, plus a **"Where experts disagree"** block of ~250 words placed as the last content segment or inside the protocol, Recap 250, Sign-off 50 = 4,400 (the disagreement block is taken out of segment 5's budget when it stands alone).
Use when the owner asks, or for topics with real controversy, several populations, or edge cases worth covering. Stays under 28 minutes: the conversational-style benefit weakens past ~35 minutes of instruction (Ginns et al. 2013 [S, abstract]) and research/01's split threshold is 25-30 minutes.

### 3.4 Split rule (Parts)

**[R]** After trimming, if the Script would exceed **4,700 words** or **6 content segments**, split it:

1. Split at a segment boundary into **2 Parts (3 at most)**. Each Part is a Standard episode (2,900-3,700 words), or Quick if the remainder is small.
2. Each Part **stands alone**: own hook, own roadmap, own protocol or takeaways (even if partial), own recap. Part 2 onward adds a "Previously" paragraph of at most 120 words inside the roadmap budget. Part 1 (and middle Parts) ends with a one-line teaser in the sign-off.
3. Prefer splits along questions that are useful on their own ("how it works" / "how to use it"), as research/01 recommended.
4. Titles: "<Topic>, part one of two" in the Script; "<Topic> (Part 1 of 2)" in metadata.
5. All Parts of a topic are produced in one skill session and published in one pipeline run, with `pubDate` values one minute apart so the Feed sorts them correctly (interface to 07 and proposed ticket 12).
6. Do not split to get under 20 minutes. Do not pad to reach it.

### 3.5 How the variant is chosen

Ticket 06's zero-input rule stands: the owner gives a topic and nothing else.

- **[R]** The owner may add the word **"quick"** or **"deep"** anywhere in the summon ("deep: zone 2 training"). That wins.
- Otherwise the skill writes **Standard**, with two exceptions it applies itself and reports in the session summary:
  - If honest content runs out below ~2,400 words, it writes **Quick** rather than padding.
  - If the content exceeds 4,700 words after trimming, it **splits into Parts**. It does not upgrade to Deep on its own; Deep is a listening choice, not an overflow.
- The skill never asks about length. If the topic is too broad, ticket 06's single drill-down round already covers it, and that round may offer "or a two-part series" as one of its options.

---

## 4. The host: persona and stance on certainty

**Who the host is.** A well-read friend who has done the reading for you. Curious, plain-spoken, warm, a little dry. Not a doctor, not a coach, not a guru, not a hype man. Talks to one person, "you", singular.

**What the host is not allowed to do:**

- **Invent experience.** The host is synthetic. No "when I tried cold showers", no "my clients". Huberman's personal-anecdote device (research/02, item 6) cannot be used honestly. Use "Say you..." scenarios, or cases reported in the sources.
- **Invent anything else**: numbers, studies, quotes, researcher names, dates.
- Give individual medical advice. Frame as "what the studies did" and "a reasonable starting point", then the caution (section 2.5).

**First person.** "I" is allowed for reasoning and judgement: "Here's how I'd read that.", "My inference, not a finding." "We" is used only for "we, the people who study this": "We don't know yet."

**Stance on certainty: calibrated, and willing to commit.**

- Say plainly what is known, what is likely, and what is unknown. "We don't know" is a complete sentence.
- One hedge per claim, at the claim, in the section 2.6 vocabulary. Not a hedge in every sentence.
- Commit to a recommendation when the evidence is good enough to act on, and say what it rests on: "With evidence this good, here's what I'd do."
- Say when a popular claim is wrong: "You've probably heard that... The evidence doesn't back that up."
- No hype, no fear. Risks are stated with size: absolute numbers over relative ones where the source gives them ("from about two in a hundred to three in a hundred", not "fifty percent higher").
- Separate three things, out loud when it matters: what the study found, what it means for you, and the host's own inference.

**Default listener.** A curious adult with no specialist background, generally healthy, who wants to use what they learn. Explain every technical term the first time. Don't assume the listener heard earlier episodes; a one-line cross-reference to an existing Episode is fine (owner question 11).

---

## 5. Voice and tone rules (research/02's 13 rules, made operational)

Each rule from research/02 is kept, replaced or made testable. "(M)" marks rules the pipeline can check mechanically before rendering; "(J)" needs judgement and is checked by the skill.

| research/02 rule | Operational version in this guide |
|---|---|
| 1. Promise plus map | Hook promise sentence by word ~100 (2.9); roadmap states segment count and names (J, M for the count). |
| 2. One organising frame, numbers said aloud | Roadmap names the frame; each segment's signpost says its number (M: signpost count = roadmap count). |
| 3. Mechanism → dose → adjust | Tool-led mode (2.3); every protocol action has what/how much/when/adjust/when not (J). |
| 4. Signpost transitions, recap every 5-7 min | Signpost at every segment start; recall prompt every ~3.5 min; cumulative recap (2.8). |
| 5. Calibrate confidence; short standing disclaimer | Calibration kept (2.6). Standing disclaimer **removed**, superseded by ticket 06 (2.5). |
| 6. Keep to 20 min | Variants and budgets (sections 0, 3). |
| 7. Voice listener questions and misconceptions | 2.7, 2-4 per Standard episode (M: count of question-lead-ins). |
| 8. Pause for the listener to predict or retrieve | Recall prompts with `[think]` (2.8). |
| 9. Write for the ear | Section 5.1-5.3 and TTS rules (section 6). |
| 10. Stories and analogies; don't narrativise everything | One analogy per content segment, one concrete example per segment (J). |
| 11. ~150-180 wpm; pauses before key numbers | Budget at 165 wpm (section 1). Pauses: `[beat]` before a key number or dose, at most twice per segment. |
| 12. Avoid listicle phrasing and stock phrases | Banned list (5.5); varied transitions (5.6). |
| 13. Mark prosody as the engine allows | Kokoro has no emphasis control; prosody comes from punctuation, sentence shape and markup pauses (section 6). |

### 5.1 Sentences

- Mean sentence length **10-16 words**. Hard maximum **30 words**. Never more than three sentences over 20 words in a row. (The audition script averaged 12.3 words, max 26 [M].)
- One idea per sentence. Main clause first: "Caffeine blocks adenosine, which is why you feel alert", not "Because adenosine, which builds up while you're awake, is blocked by caffeine, you feel alert."
- Vary length on purpose. A three-word sentence after two long ones lands as emphasis.
- Contractions always: "you'll", "doesn't", "it's".
- Paragraphs: at most 5 sentences or ~90 words. Every paragraph break becomes a pause.

### 5.2 Emphasis without markup

Kokoro cannot stress a word on request. Emphasis comes from structure:

- Put the key word last in a short sentence: "What matters is the timing."
- Repeat with contrast: "Not the amount. The timing."
- Put a `[beat]` before a key number or a surprising result.
- Never use capitals, italics or asterisks for stress (capitals risk being spelled out letter by letter).

### 5.3 Spoken lists

- At most three items in a spoken series. More than three becomes separate sentences or a numbered sequence with "First... Second... Third...".
- Announce the count first: "Three things matter here."
- No bullet structures, no "a), b), c)".

### 5.4 Do / don't examples

| Don't | Do | Why |
|---|---|---|
| Studies show that caffeine affects sleep. | A review that pooled twenty-four studies found caffeine cut sleep by about forty-five minutes. | Evidence voicing; concrete number in words. |
| Take 3-5 mg/kg of caffeine 30-60 min pre-workout. | Take about three milligrams of caffeine for every kilogram you weigh. For most people that's two cups of coffee. Have it half an hour to an hour before you train. | Spoken form; one idea per sentence; a translation into everyday units. |
| (In mice, this doubled lifespan.) | In mice, this extended lifespan. We don't know if it does anything in people. | No parentheses; species in the same sentence; no overclaim. |
| When I started doing this, my sleep improved dramatically. | Say you start doing this on Monday. By Friday, you might notice... | No invented experience. |
| Let's dive in! In today's episode we'll explore... | You can drink a coffee at four in the afternoon, fall asleep at eleven, and still lose sleep you never notice. | Hook first; banned phrases. |
| It's important to note that results may vary and you should always consult a healthcare professional before making changes. | If you're pregnant, the timing changes, because your body clears caffeine much more slowly. Ask your midwife what's right for you. | Targeted caution, at the action, once. |
| There are seven key factors: genetics, age, liver health, pregnancy, smoking, medication, and dose. | Three things change how long caffeine lasts in you. Your genes. Whether you're pregnant. And some medications. | Three-item limit; announce the count. |
| The WHO recommends 150 min/week of MVPA. | The World Health Organization recommends at least a hundred and fifty minutes a week of moderate exercise, the kind where you can talk but not sing. | Spoken form; acronyms expanded; concrete anchor. |
| Great question! The answer is complicated. | Not quite. Feeling sleepy and sleeping well are two different things. | Verdict first; no filler. |
| Research confirms that this hack is a total game-changer. | This is early evidence, from one study in forty students. Worth trying, not worth betting on. | Banned words; tier and size voiced. |

### 5.5 Banned phrases

Never: "Let's dive in", "dive deep", "In today's episode", "Welcome back", "without further ado", "In conclusion", "To sum up" (use "So, to recap" once), "game-changer", "hack", "biohack", "secret", "unlock", "supercharge", "life-changing", "science says", "studies show" (unqualified), "research confirms", "it's important to note", "it's worth noting", "at the end of the day", "the truth is", "let that sink in", "buckle up", "journey", "delve", "crucial", "simply" and "just" as minimisers, "consult a healthcare professional" as a generic line, "Great question".
Limit to once per episode: "Here's the thing", "Now,", "So,".

### 5.6 Transitions

Each segment opens with a different signpost form. Pool: "Idea two.", "That's the first piece. The second is...", "Which brings us to number three.", "So far we've covered X. Now, Y.", "Here's where it gets practical.", "Last one, and it's the one people get wrong most." No two segments in an episode open with the same construction.

---

## 6. Writing for TTS (Kokoro via kokoro-onnx)

### 6.1 What the engine actually does

Checked against the installed `kokoro-onnx` 0.6.1 source in the prototype venv and by running its phonemizer on test strings [M]. The engine is Kokoro-82M; text is turned into phonemes by **espeak-ng** (via the `phonemizer` package). Everything below follows from that front end.

- **Punctuation the model knows:** `. ! ? … , ; : — " ( ) “ ”` are tokens in its vocabulary. A plain hyphen is dropped. kokoro-onnx adds a pause after `. ! ? …` (sentence pause, default 0.25 s) and after `, ; :` (clause pause, default 0.1 s), and splits long text into batches of at most 510 phonemes at sentence, then clause, then word boundaries.
- **What breaks** [M, espeak-ng output]:

| Written | Engine says | Write instead |
|---|---|---|
| 5 mg | "five em-gee" | five milligrams |
| 1.5 g/kg | "one. five gee slash kay-gee" (the decimal point becomes a sentence break) | one point five grams per kilogram |
| 7-9 hours | "seven dash nine hours" | seven to nine hours |
| 3:00 p.m. | "three:zero zero pee. em." | three in the afternoon |
| 0.2 s, 150 ms | "zero. two ess", "em-ess" | a fifth of a second, a hundred and fifty milliseconds |
| Dr., e.g., vs. | "doctor." "ee. gee." "vee-ess." with stops | Doctor, for example, versus or compared with |
| WHO | "who" | the World Health Organization, or the W-H-O |
| ATP, alone | "atp" as one word (correct in some contexts, not others) | A-T-P, or say what it is |
| REM sleep | wrong letter reading | rem sleep (as a word) |
| SSRIs | "ess-sree" | S-S-R-Is, or an antidepressant called an S-S-R-I |
| $30 | "dollar thirty" | thirty dollars |
| 2x, 10k | "two ex", "ten kay" | twice, ten thousand |
| 1998 | "nineteen hundred ninety eight" | nineteen ninety-eight |
| omega-3s | "omega three z" | omega-threes |
| Q&A | "queue and uh" | Q and A |
| Zeitgeber | wrong | avoid; or list in `pronunciations` |
| I read it yesterday | "reed" | I went through it yesterday |

- **What works:** 10% → "ten percent"; 1,200 → "one thousand two hundred"; 1st/2nd/3rd; HRV, BDNF, LDL, DNA, UK, VO2 max (spelled as letters); "the ATP molecule" (spelled correctly in that context); common technical words such as hippocampus, suprachiasmatic, adenosine, cortisol, melanopsin, creatine, magnesium glycinate; "A-T-P" and "W-H-O" written with hyphens between capitals give a clean letter reading with no pauses.
- **No emphasis, pitch or rate control** per word. Question marks give some question intonation; exclamation marks some energy.

### 6.2 Rules for the Script

1. **Write everything in spoken form.** No digits at all in spoken text. Numbers, units, times, ranges, money, years and fractions are written as words, exactly as they should be said. This also keeps the Script portable if ticket 09 picks Polly or another engine.
2. **Round numbers for the ear** unless the action depends on the exact value: "about a third", not "thirty-four point two percent". Doses and timings stay exact, are said once in the segment, and are repeated in the recap.
3. **Metric units**, spoken in full ("grams", "kilograms", "degrees Celsius"). Give an everyday translation for doses ("about two cups of coffee"). (Owner question 9.)
4. **No abbreviations with full stops** (e.g., i.e., etc., vs., Dr., approx.).
5. **Acronyms:** prefer the full name. If the acronym is how people say it, use it only if it is on the pipeline's verified list (to be built in proposed ticket 14; today's verified examples: HRV, BDNF, LDL, DNA, VO2 max, UK), or write it as hyphenated capitals (A-T-P). Expand it the first time. List every acronym in the Bundle's `pronunciations` field.
6. **Unusual words and names** (foreign terms, drug names, researcher names, rare anatomy): avoid if the idea survives without them; otherwise list them in `pronunciations` with a plain respelling. Use at most one researcher name per segment. "A twenty twenty-three review of twenty-four studies" carries more than a surname the listener can't spell.
7. **Heteronyms:** avoid ambiguous past-tense "read", and check "lead", "live", "close", "tear", "wind", "minute", "present", "record", "object", "content", "wound", "produce". Rephrase if the context could mislead.
8. **Punctuation allowed:** full stop, comma, question mark; exclamation mark at most once per segment; colon and semicolon at most once per segment (each gives only a 0.1 s clause pause, so they are not a pause tool).
9. **Punctuation banned:** parentheses, brackets (other than the markup in 6.3), em and en dashes, slashes, ampersands, plus signs, percent and currency symbols, ellipses (they read as a full stop; use `[beat]`), quotation marks around simulated questions, emoji, URLs, markdown emphasis, bullets.
10. **No asides.** Anything that would be in parentheses becomes its own sentence or is cut.
11. **No lists that read badly** (5.3).

### 6.3 Script markup (proposed; ticket 07 owns the final syntax)

The Script is plain UTF-8 text with only these non-spoken elements. Pause lengths live in pipeline config, not in the Script, so they can be tuned once for every episode.

| Markup | Meaning | Suggested pipeline behaviour |
|---|---|---|
| `## <title>` on its own line | Segment boundary and title (not spoken) | ~1.5 s silence; title kept for metadata and a possible later chapter list |
| Blank line | Paragraph break | ~0.7 s silence (the prototype used 0.8 s) |
| `[beat]` | A deliberate short pause | ~1 s |
| `[think]` | Recall-prompt thinking time | ~3 s |
| `{c7}` or `{c3,c7}` | Claim tag: ledger line(s) this sentence rests on (not spoken) | Stripped before TTS; used by the claim-check |

Segment titles are fixed words so tooling can find parts: `## Hook`, `## Roadmap`, `## <n>: <title>` for content segments, `## Protocol` (or `## Takeaways`), `## Recap`, `## Sign-off`.

The prototype stacked its own 0.3 s and 0.8 s silences on top of kokoro-onnx's own punctuation pauses. Ticket 07 should decide which layer owns which pause so they don't double up; the owner's audition judgement was made on the stacked version.

### 6.4 What the template assumes about voice and music

- **Voice (ticket 09 decides which):** one fixed voice for every episode, English (US `a*` or UK `b*` Kokoro voice), speed set so the voice lands at ~160-175 wpm. Nothing in the Script depends on accent, apart from show-notes spelling (owner question 9). If 09 picks Polly, the markup in 6.3 maps directly to SSML `<break>`, and the spoken-form rules still apply.
- **Music (map "not yet specified", proposed ticket 12):** the Script contains no music cues and never refers to music. The pipeline may add a sting of at most ~5 s before the hook and after the sign-off. The hook must work with or without it. If a standing show line is ever wanted ("This is <show>, where..."), it comes from show config, not from the skill (owner question 6).

---

## 7. Annotated example (Hook, Roadmap and Segment 1)

Topic: "When should I stop drinking coffee?" Standard variant, tool-led. Claims checked on 2026-10-29: c1 against the Gardiner et al. full text; c2, c3 and c4 against abstracts and bibliographic records. In a real Bundle the ledger read-depth would say so.

### 7.1 Script excerpt (as it would appear in the Bundle)

```
## Hook

You can drink a coffee at four in the afternoon, fall asleep at eleven, and still lose sleep you never notice. {c1}

In one small but careful study, people took a strong dose of caffeine six hours before bed. They slept more than an hour less. And by their own reports, they hadn't noticed. {c2}

That gap, between how you feel and how you actually slept, is the whole problem. Caffeine is the most widely used stimulant in the world. And it's very good at hiding its own effects. {c4}

By the end of this episode, you'll know when your last coffee of the day should be, and how to work it out for your own bedtime.

## Roadmap

Here's the plan. Four ideas, then a simple rule you can use tomorrow, then a quick recap.

First, what caffeine actually does in your brain. Second, why it lasts much longer than it feels. Third, what it does to the sleep you do get. And fourth, why the same cup hits two people differently.

## 1: What caffeine does

Idea one. What caffeine actually does once it's in you. Everything else in this episode follows from it.

From the moment you wake up, a molecule called adenosine builds up in your brain. {c3} Picture sand running into the bottom of an hourglass. The more sand there is, the stronger the pull towards sleep. Sleep turns the hourglass over and starts it again.

Caffeine doesn't take any sand away. It covers the gauge. {c4} It sits on the receptors that adenosine normally presses on, so the signal doesn't get through. Meanwhile, the sand keeps falling.

That's why a strong coffee can make you feel fine after a short night. Nothing about the short night has been fixed. The sand is all still there. You've just stopped feeling it. {c4}

This part is textbook. The blocking action has been understood for decades. {c4} The build-up itself has been measured directly in animals, in cats kept awake for hours. {c3} In people it's measured less directly, but everything we see fits the same picture.

One honest limit. The cat studies show that the build-up happens. They don't tell us how fast it builds in you, or how much one coffee covers. For that we need studies in people, and that's where the next two ideas come from.

Now, you might be thinking, if I feel sleepy at bedtime anyway, the caffeine must be gone. Not quite. Feeling sleepy and sleeping well are two different things. Remember the study from the start. Those people still fell asleep, and they didn't report a worse night. {c2} [beat] The sleep monitor said they lost more than an hour. {c2}

That's the trap with caffeine. How you feel at bedtime isn't a reliable test.

So here's what idea one changes. The question isn't, do I feel wired tonight. It's, how much caffeine is still in me when I go to bed. That depends on how long caffeine lasts, and how much you had. Which is exactly where we're going next.

Quick check before we move on. Does caffeine remove the signal that makes you sleepy, or hide it? [think]

It hides it. The pressure to sleep keeps building underneath, so you can't trust how you feel at bedtime.
```

Ledger lines this excerpt uses (format belongs to tickets 06 and 07; shown for the link only):

```
c1 | Coffee (~107 mg caffeine) should be taken >= 8.8 h before bed to avoid lost total sleep time; caffeine cut total sleep time ~45 min | Gardiner et al. 2023, Sleep Med Rev 69:101764, doi:10.1016/j.smrv.2023.101764 | tier 1 (SR/MA, 24 studies; cutoff is a model estimate) | read: full text
c2 | 400 mg caffeine 6 h before bed reduced objectively measured sleep by >1 h; participants' subjective reports did not reflect it | Drake et al. 2013, J Clin Sleep Med 9(11):1195-1200, doi:10.5664/jcsm.3170 | tier 2 (randomised, placebo-controlled, n=12 healthy sleepers) | read: abstract
c3 | Adenosine rises in the basal forebrain during sustained wakefulness and falls during recovery sleep | Porkka-Heiskanen et al. 1997, Science 276:1265-1268, doi:10.1126/science.276.5316.1265 | tier 3, ANIMAL (cats) | read: abstract
c4 | Caffeine is the most widely consumed CNS stimulant; at usual doses it acts mainly by blocking adenosine receptors, so it masks rather than removes sleep pressure | Fredholm et al. 1999, Pharmacol Rev 51:83-133 | tier 3 (expert review), textbook consensus | read: bibliographic record only; must be upgraded to abstract or full text before real use
```

### 7.2 Annotations

| Where | What it shows |
|---|---|
| Hook, sentence 1 | Scenario with a twist. 4 pm to 11 pm is 7 hours, inside Gardiner's 8.8-hour estimate, so the claim is consistent with c1. Times as words. |
| Hook, paragraph 2 | Sourced surprise. "Small but careful" voices tier 2 and size in four words. No researcher name. "A strong dose" avoids "400 mg"; the exact dose goes in the show notes. |
| Hook, paragraph 3 | Names the problem the episode solves and sets up segment 1. |
| Hook, paragraph 4 | Promise sentence at word ~85 (inside the first ~35 s). No welcome, no show name, no caution. |
| Roadmap | Count said aloud, frame named, "then a rule, then a recap". Four ideas match four content segments. The episode is not higher-risk, so no caution line. |
| Segment 1, paragraph 1 | Signpost with number and name. |
| Paragraph 2-3 | Mechanism in one-idea sentences, one analogy (hourglass) carried through. |
| Paragraph 4 | Concrete everyday example of the mechanism (the short night). |
| Paragraph 5 | Inline evidence voicing in two strengths: "textbook" (consensus, c4) and "measured directly in animals, in cats" (species in the same sentence, c3), plus an honest limit for humans. |
| Paragraph 6 | What the evidence doesn't tell us, said plainly, used as the bridge to the next segments. |
| Paragraph 7 | Simulated listener question from a real misconception; no quote marks; verdict first ("Not quite."); `[beat]` before the key result. |
| Paragraph 8-9 | Bridge to practice and a hand-off to segment 2. |
| Recall prompt | Question, `[think]`, short answer. Retrieval, not restatement. |
| Throughout | No digits, no parentheses, no dashes, no abbreviations; contractions; "you" singular; no invented experience. |

Measured with a throwaway lint [M]: Hook 116 words (promise sentence at word 89), Roadmap 54, Segment 1 363 words, longest sentence 27 words, no banned characters. A full Standard segment is 560 words; this one is shorter to keep the example readable. A real segment would add ~200 words, typically a second worked example (a working day with three coffees) and a fuller evidence passage.

---

## 8. Skill-facing checklist (run before the Bundle is emitted)

(M) items are mechanical. Ticket 07 should implement them as a **script lint** that also runs in the Pipeline and fails the run before TTS. (J) items are self-review by the skill.

**Length and structure**
1. (M) Word count of spoken text is inside the variant's range (Quick 1,500-2,100; Standard 2,900-3,700; Deep 4,000-4,700). Above 4,700: split into Parts.
2. (M) Segment headings present in order: Hook, Roadmap, numbered content segments, Protocol or Takeaways, Recap, Sign-off.
3. (M) Number of content segments matches the variant and the count said in the Roadmap.
4. (M) Hook is 110-150 words (Quick: 80-120) and contains a promise sentence ("By the end" or an equivalent the skill marks).
5. (M) Recall prompts: right count for the variant; each has a `[think]` with the question before it and an answer of at most 25 words after it.
6. (J) Each content segment opens with a numbered signpost, has one analogy and one concrete example, and the signposts use different constructions.
7. (J) 2-4 simulated listener questions (Standard), each a real misconception or objection with a direct verdict-first answer.
8. (J) Every protocol action states what, how much, when, how to adjust, and when not to.
9. (J) "How sure are we" names the strongest claim, the weakest link, and what would change the advice.
10. (J) Recap follows roadmap order, in retrieval form (Standard and Deep).

**Accuracy (ticket 06)**
11. (M) Every sentence with a factual claim carries a claim tag; every tag resolves to a ledger line; every ledger line used in the Script is in the source list.
12. (J) Evidence phrase at each load-bearing claim matches the ledger tier (2.6), including size and population.
13. (J) Animal and cell findings name the species in the same sentence.
14. (J) No invented experience, number, study, quote or name.
15. (J) Every caution is specific and sits next to its action; higher-risk episodes have the roadmap caution line and `risk_flag: higher` with a reason; no standing disclaimer.

**TTS (section 6)**
16. (M) No digits in spoken text; none of the banned characters `( ) [ ] — – / & + % $ € £ … * _ #` outside the markup; no URLs; no emoji.
17. (M) No abbreviations with full stops; no all-capitals words other than acronyms on the verified list or hyphenated (A-T-P); every acronym also in `pronunciations`.
18. (M) Mean sentence length 10-16 words; no sentence over 30 words; no run of more than three sentences over 20 words.
19. (M) Paragraphs at most 5 sentences or 90 words.
20. (M) No banned phrase (5.5); limited phrases at most once.
21. (J) No spoken series longer than three items; counts announced.
22. (J) Heteronyms checked (6.2 rule 7).

**Bundle completeness**
23. (M) Title, summary, show notes, variant, part info if any, risk flag, `pronunciations`, `wpm_budget`, `style_guide_version`, ledger and sources all present (section 9).

---

## 9. Interfaces with other tickets (flagged, not decided)

### 9.1 Bundle fields this template implies (for ticket 07)

| Field | Content |
|---|---|
| `script` | The Script with the 6.3 markup |
| `variant` | `quick`, `standard` or `deep` |
| `part` | null, or `{n, of, series_slug}` |
| `segments` | Derived list: id, heading, kind (hook, roadmap, content, protocol, recap, signoff), word count |
| `wpm_budget`, `target_words`, `spoken_words` | For duration estimates and the section 1 calibration |
| `risk_flag`, `risk_reason` | `none` or `higher`, plus one line |
| `pronunciations` | List of `{term, say_as}`: every acronym, name and unusual term; format owned by 07 and proposed ticket 14 |
| `title` | Plain, at most ~60 characters, says what the listener gets ("When to stop drinking coffee") |
| `summary` | Two or three sentences for the feed description |
| `show_notes` | Written form, not spoken form: digits and units allowed. Opens with the risk line if flagged; summary; the protocol with exact numbers; the source list from the ledger with evidence tiers |
| `claim_ledger` | Ticket 06 lines, with stable ids matching the claim tags |
| `parent_episode` | null; set by Q&A episodes (ticket 11) |
| `style_guide_version` | So feedback can be tied to the template version that produced the episode |

Show notes are a separate piece of writing from the Script. The skill writes both: the Script in spoken form, the show notes in normal written form with exact numbers.

### 9.2 Claim ledger link (for ticket 06)

The `{cN}` tags make ticket 06's cheap claim-check mechanical: for each tagged sentence, check that the ledger line supports it at the strength voiced; for each untagged sentence, confirm it makes no factual claim. Two recommendations from the Opus review affect the ledger: a read-depth field (full text, abstract, secondary) and a "consensus" marker for textbook mechanisms (section 2.6). Both need owner sign-off on 06.

### 9.3 Shape a Q&A episode would reuse (for ticket 11)

Proposed shape, for 11 to accept or change:

- **Length:** the Quick budget (~1,300-2,000 words, 8-12 min).
- **Hook (≤100 words):** the question in the listener's words, why it's a good question, and the answer in one sentence (answer first, since the listener asked).
- **Link back (1-2 sentences):** "In the episode on caffeine and sleep, we said..." Uses the parent's claim ids.
- **Two or three content segments:** the evidence on the question; nuance or edge cases; what to do.
- **One recall prompt**, plain recap, sign-off pointing back to the parent episode.
- **Ledger:** reuse parent lines by reference (for example `{p:c3}`), add new lines for new claims. New research only for what the parent's ledger doesn't cover.
- All TTS, voice and accuracy rules apply unchanged.

### 9.4 Other links

- **Ticket 09 (voice):** budget constant set from the chosen voice (section 1). The audition script avoided numbers, acronyms and technical terms, so it doesn't test section 6. Recommend adding the example in 7.1 to the audition.
- **Ticket 10 (Learnings):** add a learnings category for "TTS pronunciation problems found" so lexicon fixes and Script habits carry forward.
- **Proposed ticket 12 (show identity):** episode title conventions, part numbering in the Feed, music sting, any standing show line.
- **Proposed ticket 14 (pronunciation and normalisation):** the verified-acronym list, lexicon format, and the lint for section 6.
- **Proposed ticket 15 (testing):** the (M) checklist items are the first automated quality gate.
- **Proposed ticket 16 (feedback):** how owner reactions tune budgets, recall-prompt count and banned phrases.

---

## 10. Proposed glossary additions (owner to accept)

- **Variant**: The length format of an Episode: Quick (~11 min), Standard (~20 min, default) or Deep (~27 min).
- **Segment**: A titled section of a Script: Hook, Roadmap, a content segment, Protocol or Takeaways, Recap, Sign-off.
- **Hook**: The opening of an Episode (first ~45 s) that earns attention and states the promise.
- **Recall prompt**: A question to the listener, followed by a thinking pause and then the answer.
- **Part**: One Episode of a topic that was split because it would run over ~28 minutes.
- **Claim tag**: A non-spoken marker in the Script linking a sentence to its Claim ledger line.
- **Spoken form**: Text written exactly as it should be said: numbers, units and symbols as words.
- **Higher-risk flag**: The Bundle marker, with a reason, for topics whose advice could cause harm if misapplied.

---

## 11. Open questions for owner (answered 2026-10-29, see section 12)

Kept for the record. The owner's answers, and the follow-up rounds they triggered (Q14-Q26), are in section 12.

1. **Lengths.** Quick ~11 min, Standard ~20 min, Deep ~27 min, split into Parts above ~28 min? *Default: yes.*
2. **Pace basis.** Budget at 165 wpm, recalibrated automatically to the chosen voice after two episodes, slowing the voice with the speed setting if it runs above ~180 wpm? *Default: yes.*
3. **Choosing a variant.** Owner adds "quick" or "deep" to the topic; otherwise Standard, with the skill allowed to drop to Quick when honest content runs out and to split into Parts when it overflows, telling you afterwards? *Default: yes.*
4. **Splits without asking.** Should the skill split into Parts on its own (max 3, all published together), or ask first? *Default: split on its own; asking would break ticket 06's zero-input rule.*
5. **Segment mode.** Skill picks tool-led or mechanism-led per topic, tool-led by default for health and training? *Default: yes.*
6. **Standing show line.** A fixed one-sentence show introduction after the hook? *Default: none in v1; revisit with show identity (proposed ticket 12).*
7. **Recall prompts.** Three per Standard episode with a ~3 s pause, retrieval-style? *Default: yes; if they annoy you after three episodes, cut to one before dropping them.*
8. **Host persona.** Unnamed host, "a well-read friend", first person only for reasoning, never claims personal experience? *Default: yes. Naming the host belongs with show identity.*
9. **Units and spelling.** Metric units in the Script; British spelling in show notes? *Default: yes (the project docs are in British English). Say if you want imperial alongside.*
10. **Sign-off.** Varied closing with one concrete thing to try, no catchphrase? *Default: yes.*
11. **Cross-references.** May an Episode mention one earlier Episode by topic ("in the episode on sleep...")? *Default: yes, at most one, and only to Episodes that exist in the Feed.*
12. **Disclaimer conflict.** Confirm ticket 06 (no standing disclaimer) overrides research/02 rule 5? *Default: yes.*
13. **Show notes.** Summary, the protocol with exact numbers, and sources with tiers, but not the full transcript (the Script is already in the public repo)? *Default: yes.*

---

## 12. Owner decisions (grilling, 2026-10-29)

These override sections 1-11 wherever they differ. Question numbers refer to the grilling rounds: Q1-Q13 are from section 11, and Q14-Q26 are the follow-ups.

### 12.1 Any topic, not a niche (Q18, Q24): the tool's defining property
This is the owner's biggest requirement. The tool must handle **any general-interest topic with ease**: sport, science, news, technology, finance, history and anything else. It must not stick to one area the way a typical podcast does. Consequences:
- The template (structure, plain-language rules, retrieval design) is domain-neutral. Health is one profile among many, not the default.
- What counts as good evidence varies by field, so the research standard runs through **source profiles** (section 13). A topic outside the starter profiles gets a profile worked out on first use and saved to Learnings (ticket 10).
- The spoken evidence-strength phrases (2.6) are generalised to fit any field ("the official figures show", "historians mostly agree", "two independent outlets report"), not only study tiers. Science-only checks (checklist item 13, naming the species) apply only to science and health topics.
- The map's destination is rewritten from "learn something / better myself" to any general-interest topic.

### 12.2 Leniency rule (Q17, Q23)
Every numeric limit is a **soft target with about ±25% leniency** unless it is listed as firm below. The owner is asked before any new strict limit is introduced anywhere in the spec.

**Firm (no leniency).** These protect accuracy, honesty or the TTS engine, not style:
- Never invent experiences, studies, numbers, quotes or names.
- Every factual claim traces to the claim ledger.
- No digits or symbols in spoken text (spoken form, section 6).
- No padding to reach a length, and no cliffhanger Part endings.
- At most 3 Parts.
- No standing disclaimer (ticket 06 overrides research/02 rule 5).
- Firm rules F1-F9 from research/18 section 8a (owner sign-off, 2026-10-29; see 12.11).
- Ticket 06 sign-off (2026-10-29): a spoken number comes from a full text, or from an abstract that states it; the two or three load-bearing numbers are re-checked against the source; a single study that carries a protocol is checked for retraction.
- "Explain first, name second" and an everyday analogy for every hard concept are firm *defaults*. The skill may break them only with a reason, which it states in the session output.

**Soft (±25%):** word ranges, segment counts, hook length, sentence and paragraph lengths, the number of simulated listener questions and retrieval prompts, pause lengths, technical terms per episode, anecdotes per segment, cross-references per episode, and the "bright 15-year-old" reading target.

**Lint behaviour (for tickets 07 and 15):** the script check fails a run only when a firm rule is broken. A soft limit exceeded by more than 25% raises a warning. The skill either fixes it or justifies it in one line in the Bundle.

### 12.3 Lengths, splitting and Parts (Q1, Q14, Q15, Q22)
- Lengths are topic-dependent ranges with **no minimum**:
  - Quick: 8-15 min.
  - Standard: 15-28 min, typically about 25.
  - Deep: 28-35 min, typically about 35.

  The owner: "no need for fillers to get us to time."
- The owner knowingly extends Standard and Deep beyond research/01's suggested split point (25-30 min). That evidence was indirect, since no study tested audio alone. The segment structure and retrieval design carry the longer episodes.
- **Split** only when the estimate exceeds ~35 min *and* the topic breaks into subtopics that each stand alone. If it doesn't break cleanly, a single Deep episode may run to ~44 min (35 + 25%), and anything longer must be trimmed.
- **Parts are distinct subtopics, never a serial.**
  - Each Part has its own hook, closing segment and recap.
  - Each Part makes sense heard alone or out of order.
  - No teaser endings. At most, one closing line names the other Part's subtopic.
  - At most 3 Parts, published together.
  - The skill splits on its own and shows the split in the confirm step (12.4).

### 12.4 The confirm step (Q3, Q16)
The owner doesn't add "quick" or "deep". The skill proposes and the owner confirms, in **one round**:
> "Standard, about 24 min, 4 segments: A, B, C, D. Reply go, or adjust." (or "2 Parts: X / Y.")

The owner replies "go" or with a short tweak. If the topic is too broad, the drill-down question comes in the same message, so there is still only one round. This replaces ticket 06's zero-input rule with exactly one confirmation reply. The skill still drops to a shorter length rather than pad. Padding is a firm no.

### 12.5 Segment styles and the closing segment (Q5, Q19)
- The skill picks **tool-led** or **mechanism-led** freely for each topic. There is no default by domain.
- Topics with nothing to act on afterwards (concepts, news, history) replace the Protocol with **"Why it matters / what to watch"**. It covers the implications, what to watch next, and where the uncertainty lies. It still ends with "How sure are we".

### 12.6 Retrieval design (Q7, Q21; evidence in research/17)
This replaces the "three recall pauses" of 2.8. The items are ranked by strength of evidence:
1. **Open each segment with its main question** and invite a guess ("have a guess before I explain"), then **re-ask it at the end** with the answer. (Moderate evidence.)
2. **Signposts become spoken previews**: what the segment explains and why, not "Idea two". Reasons are said with "because" and "so". (Moderate.)
3. **Each mechanism ends with an explicit "so what" sentence.** (A moderate gap in listening comprehension; the fix itself is untested.)
4. **From segment 2 on, ask a brief spaced-recall question** about an earlier segment. (Moderate in general, weak for silent prompts.)
5. **Introduce 2-3 key terms**, each with a one-line description, before the mechanism. This fits 12.7. (Moderate to weak.)
6. **Pauses** are about 3 s for one-fact answers and 4-5 s for "why" questions, always followed by the answer. (Weak evidence; a soft limit.)
7. **An optional callback question** to a related earlier Episode, using the one allowed cross-reference (12.9).
8. **No prompts that need the listener to produce or explain something** (elaborative interrogation, generation, self-explanation).

This adds about 100-150 words to a Standard episode, partly taken from each segment's opening. The owner is open to better-evidenced methods later. Revisit if research/17's unchecked sources (the Weinstock 2020 full text and the covert-retrieval meta-analysis) change the picture.

### 12.7 Plain language (Q5, Q17): a top priority for the owner
Anyone must be able to understand hard or technical ideas. No textbook register and no undefined jargon.
- **Explain first, name second** (firm default): give the idea in everyday words, then the term, if it's needed at all.
- About 3-4 technical terms per episode (soft), each defined in one plain sentence on first use.
- Every hard concept gets an everyday analogy (firm default).
- Target listener: a bright 15-year-old with no background in the subject (soft).
- Checklist addition, mechanical where possible: flag any term used before its plain explanation.

### 12.8 Host, examples and anecdotes (Q8, Q20)
- The host is unnamed, "a well-read friend". The host says "I" only for reasoning and never claims personal experience. Naming the host belongs to ticket 12.
- Allowed:
  - (a) Clearly hypothetical "imagine you…" scenarios.
  - (b) Real, sourced stories (historical cases, documented people, study participants), logged in the claim ledger.
- Never allowed: (c) the host's own invented experiences.
- About one example per segment (soft), used to unlock a hard concept. Never corny or stacked.

### 12.9 Smaller decisions (Q2, Q6, Q9-Q13, Q25, Q26)
- **Pace:** 165 wpm, recalibrated to the chosen voice after two episodes. Slow the voice if it runs above ~180 wpm.
- **Show line:** none in v1. Revisit in ticket 12.
- **Units and spelling:** metric only in Scripts. British spelling in show notes.
- **Sign-off:** varied, with one concrete thing to try (or one thing to watch, for topics with nothing to act on). No catchphrase.
- **Cross-references:** at most one earlier Episode per Episode (soft), and only Episodes already in the Feed.
- **Disclaimer:** ticket 06 wins, so there is no standing disclaimer.
- **Show notes:** the summary, the protocol or key points with exact numbers, and sources with tiers. No transcript.
- **Summon front end:** the owner would like a nicer, branded interface than the standard Claude app or CLI. Added to ticket 13 as a nice-to-have.
- **Glossary:** the section 10 terms are accepted, updated to these decisions, plus **Source profile**.

### 12.10 Sections superseded
- 2.1-2.2 word budgets: now the ranges in 12.3.
- 2.3 segment-mode default: now 12.5.
- 2.8 recall prompts: now 12.6.
- 3.1-3.5 variants and split rule: now 12.3 and 12.4.
- Checklist items 1, 3, 5 and 6: the numbers and recall form now follow 12.3 and 12.6, as soft limits.
- Section 11: answered.
- 2.4 fixed order, 2.6 single phrasing per tier, 2.7 lead-ins and verdict words, 2.9 promise wording, 5.2 "Repeat with contrast", 5.3 count announcing, 5.5 "So," limit and blocking, 5.6 transition pool, and 12.6 items 1 and 3 wording: softened by 12.11.

Everything else stands.

### 12.11 De-slop softenings and host stance (owner sign-off, 2026-10-29)
From research/18 section 4 (rows 1, 3-6 and 9-14) and owner questions 5, 7 and 8 of research/18 10.1. These override the sections named. Every number here is soft (±25%) unless marked firm.
- **Promise sentence (2.9):** the promise stays as a function, by word ~100. "By the end of this episode, you'll know..." is one form among many, not a template. The lint warns when a promise sentence shares six or more consecutive words with one in the last ten Bundles.
- **Listener questions (2.7):** a lead-in is optional. A question may stand with none ("So is the caffeine gone by bedtime? Not quite."). The lead-ins listed in 2.7 are examples, not a pool.
- **Verdict words (2.7):** no verdict word ("Not quite.", "Partly.") twice in an episode. Some answers start with the reason instead.
- **"Not X. Y." (5.2):** at most once per episode, and only to correct a belief the listener actually holds. Prefer end-focus ("What matters is the timing.") and a short sentence after a long one.
- **Lists (5.3):** three items is a maximum, not a target; two is often better. Announce the count only for three or more items the listener needs to hold. The lint warns on more than two "three things" announcements per episode.
- **Banned phrases (5.5):** the once-per-episode limit on "So," applies to it as a paragraph-opening marker, not to causal "so" mid-sentence. The list is extended with research/18's C2 vocabulary and the C3, C4 and C6 constructions (research/18 9.2) and is versioned. **Firm (F9):** only the core ten block a run: "let's dive in", "dive deep", "delve", "in today's episode", "welcome back", "without further ado", "buckle up", "great question", "it's important to note", "it's worth noting". The rest warn.
- **Transitions (5.6):** the pool is examples only. The cross-episode check catches reuse.
- **Segment order (2.4):** vary the internal order across segments: open one with the case, another with the question, another with the surprising number. The retrieval bookends (12.6 item 1) stay.
- **Segment question (12.6 item 1):** the main question is mandatory; the invitation phrase is not. Sometimes the question simply hangs, with `[think]`. The re-ask may fold into the "so what" sentence. No lead-in is repeated within an episode.
- **"So what" (12.6 item 3):** one per mechanism, not per paragraph, in varied words. "So here's what that means for you" at most once an episode.
- **Evidence phrasing (2.6):** the tier meaning is fixed. Each tier gets two or three equivalent phrasings, all mapped in the lint so the claim-check still works. Never upgrade a tier for variety.
- **Humour:** zero to two light moments an episode, from the material only, never forced.
- **Point of view:** the host commits to a view on evidence and practical choices, and stays balanced on contested values and politics (ticket 06's news rules).
- **Breaths:** off in v1. Revisit only through an A/B test, once a breath set whose licence meets F7 exists.

---

## 13. Source profiles (starter set)

**Why these:** the starter set covers the largest podcast genres, so the tool is strong across general-interest topics from day one.

- **Top five:** Edison Research ranks US podcast genres by weekly reach, using each show's primary Apple Podcasts category. Its most recent full public ranking (Q1 2024) was Comedy, Society & Culture, News, True Crime, Sports. [S, via press coverage; the Edison page couldn't be fetched.]
- **Since then:** a September 2026 secondary report says True Crime has passed Comedy. [S, unverified.]
- **The rest:** Apple's other top-level categories fill out the list: Business, Health & Fitness, Education, History, Science, Technology, Religion & Spirituality, Arts, Music, TV & Film, Leisure, Kids & Family, Government and Fiction. Their reach order beyond the top five isn't public, so the table below is grouped by kind, not ranked.
- **Not covered:** Comedy and Fiction are formats, not knowledge domains, so they get no profile. The host may be lightly funny on any topic.

Each profile gives three things: what counts as strong evidence, what to watch for, and what triggers the higher-risk flag. Ticket 06's general standard applies to all of them: 3-5 sources, the claim ledger, every claim traceable, and read-depth once approved. A profile changes only *which* sources sit at the top of the ladder and how strength is voiced.

| # | Profile (Apple categories) | Strongest evidence | Watch for | Higher-risk flag when |
|---|---|---|---|---|
| 1 | **News and current events** (News) | Primary document (statement, ruling, filing, dataset) plus 2 independent reputable outlets per key claim | Single-source scoops and fast-moving facts. Say the date aloud ("as of the twenty-ninth of October"). Keep reported fact, open dispute and analysis clearly separate | Ongoing legal cases; unconfirmed casualty figures |
| 2 | **Politics and government** (Government, News) | Legislation, official records, election data and polls from established pollsters, nonpartisan analysts | Partisan framing. Give contested claims both sides fairly. Polls are snapshots with margins of error | Elections in progress; always label analysis versus fact |
| 3 | **True crime and law** (True Crime) | Court records, judgments, official inquiry reports, established long-form journalism | Presumption of innocence, living people and victims. Never speculate on guilt beyond the record. Defamation | Unresolved cases; named living suspects |
| 4 | **Society, culture and psychology** (Society & Culture) | Peer-reviewed social science; large surveys from official statistics or established research bodies | The replication crisis in psychology, correlation versus cause, one-country samples. Say who was studied | Mental-health advice, which is handled as health |
| 5 | **Sport** (Sports) | Governing-body statistics and rules, established stats providers, sports-science studies for training claims | Stat definitions differ between sources. Small-sample "hot streaks". Transfer and injury rumours are not facts | Training or injury advice, which is handled as health |
| 6 | **Business, finance and economics** (Business) | Company filings, central-bank and official statistics, peer-reviewed economics, regulator publications | General explanation only, **never personal financial advice**. Past returns, survivorship bias, nominal versus real figures | Any investing, debt or tax content |
| 7 | **Health, fitness and nutrition** (Health & Fitness) | Ticket 06's original ladder: systematic reviews and meta-analyses, RCTs, major guidelines | Name animal and cell studies as such. Absolute versus relative risk. Supplement-industry funding | Doses, fasting, drugs, supplements, medical conditions |
| 8 | **Science, space and nature** (Science) | Reviews and meta-analyses, major scientific bodies, mission and agency data | Preprints, single striking studies, press-release hype. Say when something is a hypothesis | Rarely; environmental-health claims are handled as health |
| 9 | **Technology** (Technology) | Official documentation and specs, standards bodies, peer-reviewed computing research, independent testing | Vendor benchmarks and marketing. Claims age fast, so date them. Hype cycles | Security how-tos; financial claims about crypto, which are handled as finance |
| 10 | **History** (History) | Scholarly books and journal articles, primary sources, reputable reference works | Popular myths and misquotes. Say where historians disagree and why. Dates and the spelling of names | Topics prone to denial: atrocity and genocide denial is never treated as a legitimate side |
| 11 | **Learning, careers and self-improvement** (Education) | Learning-science and organisational research; reviews ahead of popular books | Self-help claims without evidence; success stories offered as proof | Rarely |
| 12 | **Religion, spirituality and philosophy** (Religion & Spirituality) | Primary texts, academic religious studies, philosophy reference works | Describe traditions in their own terms. Never judge whose belief is true. Note the diversity within each tradition | Rarely; respect over provocation |
| 13 | **Arts, music, film and books** (Arts, Music, TV & Film) | The works themselves, artist interviews, reputable criticism and scholarship, industry data | Separate fact (dates, sales, history) from taste. Critics disagree. Warn about spoilers up front | Rarely |
| 14 | **Leisure, food, travel and hobbies** (Leisure) | Official and expert bodies (food safety, travel advisories), reputable guides, manufacturer documentation for equipment | Regional variation. Prices and rules change, so date them | Food safety; outdoor and physically risky activities |
| 15 | **Parenting and family** (Kids & Family) | Paediatric and developmental guidelines, reviews | Strong opinions presented as evidence; cultural variation | Child health and safety, which is handled as health |

**Overlap rule:** a topic can draw on two profiles. Sport training, for example, uses Sport and Health. The stricter flag rule applies.
**New field:** if no profile fits, the skill drafts one with the same columns during research, uses it, and saves it to Learnings (ticket 10). The next topic in that field is then cheaper.
