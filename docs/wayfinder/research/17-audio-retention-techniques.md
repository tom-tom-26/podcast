# Research 17: Techniques for comprehension and retention in passive audio listening

Drafted 2026-10-29. Research only: research/05 and the tickets are not edited. The proposed changes are in the last section.

Question: which script-level techniques have solid evidence for improving comprehension and retention when people learn by listening, which of them a script writer can use, and whether they carry over to a passive listener on an iPhone (TTS voice, no typing, often doing something else).

Already covered elsewhere, and not repeated here: interpolated typed tests (Szpunar 2013, Jing 2016, Welhaf 2022), segmenting (Rey 2019) and the attention-span myths are in research/01. Personalisation and conversational style (Ginns 2013, Mayer), the voice effect with TTS (Craig & Schroeder) and narrative (Mar 2021) are in research/02. This file only adds to those where something new changes the advice.

**How deeply each source was read.** **[F]** full text read (at least methods and results). **[A]** abstract, or abstract plus tables, read at the source. **[S]** secondary only: a citing paper, a review, or search-result summaries. **[K]** cited from background knowledge and not re-checked in this pass. Treat [S] and [K] numbers as leads, not facts.

---

## Bottom line

1. **No technique has been shown to work for the exact case here**: passive, divided-attention listening to a TTS voice, with no way to respond. Everything below is borrowed from reading, video, lecture or lab studies. The one audio-podcast trial found (Weinstock et al. 2020) is small and only abstract-level.
2. **The best-supported technique that fits audio is the prequestion**: ask the question a segment will answer *before* the segment, and invite a guess. Meta-analysis: g = 0.54 on the targeted material, and larger for audiovisual and experimenter-paced material (both describe a podcast). Answering in your head worked as well as typing in the one direct test (Rivers et al. 2026, text). The benefit is **specific**: it helps the question's own content and does essentially nothing for the rest.
3. **Covert after-the-fact retrieval (the current recall prompt) is weak.** The covert-retrieval meta-analysis gives g = 0.23 against restudy, close to nothing after bias correction, and overt retrieval beats covert. The prompts are still cheap. They are more likely to help if they ask about material from **earlier** segments rather than the paragraph just heard, and if the answer is always given afterwards.
4. **Spoken signalling works only if it carries content.** Spoken preview sentences helped TTS listeners. Heading-style labels did not survive the move to audio. "Idea two." is a heading. "Idea two: why caffeine outlasts the buzz, and what that means for your last coffee" is a preview.
5. **Listening costs inference, not literal recall.** Listening and reading come out level on literal comprehension, but reading wins on inferential comprehension (g = 0.36), mainly when the listener cannot control the pace. So the script should **say the inference out loud** rather than leave it for the listener to draw.
6. Pretraining (key terms before the mechanism) has fair support from narrated multimedia, mostly from one lab. Elaborative interrogation, self-explanation, generation and worked examples all depend on the learner producing something or solving problems, so they do not transfer to a passive listener except in weak, host-modelled forms.

---

## 1. What is different about passive TTS listening

These conditions limit how far the findings below transfer.

- **No pacing control.** Clinton-Lisell (2022, *Review of Educational Research*, 46 studies, N = 4,687) [S: abstract figures via search summaries; publisher abstract not opened]: overall reading vs listening difference g = 0.07 (n.s.). Reading was better for inferential comprehension (g = 0.36) and slightly better for general comprehension (g = 0.15), and level for literal comprehension (g = -0.01). Per a secondary summary, the reading advantage came mainly from studies where readers controlled the pace and listeners did not. A podcast listener can rewind, but someone walking or driving mostly won't.
- **More mind wandering.** Varao Sousa, Carriere & Smilek (2013, *Frontiers in Psychology* 4:892, N = 211 in two samples, within-subjects, ~1,800-word Bryson excerpts read by the author) [F via PMC]: mind wandering at 51% of probes when listening vs 36% in silent reading. Listening also gave the worst true/false memory and the least interest. The authors call the findings exploratory. One book, students, a human narrator.
- **Divided attention.** Dividing attention at encoding generally harms later memory [K: e.g. Craik et al. 1996]. Middlebrooks, Kerr & Castel (2017, *Psychological Science*) [S] found that people under divided attention protect memory for items marked as important. That supports explicitly flagging what matters (sections 3 and 4). No study was found that measured memory for spoken educational content while walking or driving.
- **No overt response, no feedback loop.** Any technique that needs the learner to write, type, draw or choose is out, unless it works in a covert form. That is the key test applied to each technique below.

---

## 2. Technique-by-technique

Each entry gives: evidence and size, whether it was tested with audio, limits, and transfer to passive TTS listening.

### 2.1 Prequestions (ask before the segment; listener guesses)

- **Meta-analysis.** St. Hilaire, Chan & Ahn (2024), "Guessing as a learning intervention", *Psychonomic Bulletin & Review* 31, 411-441, doi:10.3758/s13423-023-02353-8 [F: abstract, method, moderator tables]. Preregistered. Specific effect (the prequestioned material) **g = 0.54 [0.42, 0.66], k = 97**. General effect (material not asked about) **g = 0.04, k = 91**, i.e. essentially none. No funnel asymmetry; the PET-PEESE adjustment was applied to the specific effect. Moderators for the specific effect: participants guessed g = 0.65 (k = 70) vs only read the questions g = 0.22 [-0.02, 0.45] (k = 29); **audiovisual material g = 0.66 (k = 21)** vs text g = 0.51 (k = 77); **experimenter-paced study g = 0.65** vs self-paced g = 0.42 (p = .049). Factual prequestions g = 0.58 vs conceptual g = 0.28 (marginal, p = .073, few studies). The specific effect was larger when learners knew less beforehand.
- **Covert prequestions.** Rivers, Berdelis, Pan & Tauber (2026), "Does covert prequestioning enhance learning?", *Applied Cognitive Psychology* 40:e70165, doi:10.1002/acp.70165 [F]. Two experiments, N = 165 and N = 315, preregistered (Exp 1). Expository texts of about 4.7 minutes of reading, 10 short-answer prequestions shown for at least 5 s each, a 5-min distractor, then a multiple-choice test. Mentally answering was as good as typing (Exp 1: Bayes factor for the modality effect 0.22, i.e. evidence for no difference). Prequestioned items vs read-only control: covert g_av = 0.75 (Exp 1), 0.71 (Exp 2). **Reading statements of what would be learned ("you will learn: the planet that lacks a magnetic field") worked about as well as prequestions** (g_av = 0.57). The authors read this as support for an attention account. Limits: text, not audio; self-paced reading; a 5-minute retention interval; low prior knowledge; mostly female students at one university.
- **Video.** Carpenter & Toftness (2017) and Pan et al. (2020, "Pretesting reduces mind wandering and enhances learning during online lectures") [S: via St. Hilaire and search summaries]. St. Hilaire & Carpenter (2020), four experiments with 30-minute video lectures [S]: the benefit appeared only when learners noticed the answer during the lecture.
- **Older adjunct-question literature.** Hamaker (1986), *Review of Educational Research* 56(2), 212-242 [S: abstract via search]. Factual prequestions *hurt* unrelated material when study time was fixed. Higher-order questions transferred more broadly than factual ones.
- **The one podcast trial.** Weinstock et al. (2020), "Effect of Interpolated Questions on Podcast Knowledge Acquisition and Retention", *Annals of Emergency Medicine* 76(3), 353-361, doi:10.1016/j.annemergmed.2020.01.021 [A: PubMed abstract and the 2019 WestJEM conference abstract; full text blocked]. Double-blind RCT, 137 emergency-medicine trainees from six programmes. Two versions of a podcast on the history of hypertension, identical except that one had **five interpolated questions to highlight educational points**. 15 multiple-choice items (5 on the highlighted points, 10 unrelated), tested within 48 h and again at 2-3 weeks. Overall: no difference at the immediate test; +5.6 points absolute at 2-3 weeks (95% CI 0.2 to 10.9). Highlighted items: +8.7 points immediately (1.6 to 15.8) and +10.1 points at 2-3 weeks (2.8 to 17.4). Unrelated items: no difference. From the abstracts I could not tell how the questions were voiced, whether there was a pause, or whether they came before or after the material. There was no "highlight only" control, so attention to the key points could explain the result as well as retrieval could.
- **Transfer to passive TTS: good, with one big caveat.** A podcast is experimenter-paced and serial, the conditions in which the effect was largest, and the guess can be covert. The caveat is that the benefit is specific: it boosts the asked-about point and not the rest. Hamaker's warning about fixed study time applies, because a podcast's pace is fixed, so the question has to target the **central idea** of the segment, not a side fact. **Evidence strength: moderate** (a good meta-analysis, but mostly text, short retention intervals, and one small podcast RCT that agrees).

### 2.2 Covert retrieval after learning (the current recall prompt)

- **Meta-analysis.** Yu, Zhao, Li, Shanks, Hu, Luo & Yang (2025), "Is Covert Retrieval an Effective Learning Strategy? Is It as Effective as Overt Retrieval?", *Educational Psychology Review* 37:52, doi:10.1007/s10648-025-10024-4 [S: the figures as cited in Rivers et al. 2026 [F] plus a teacher-blog summary; the abstract itself was not reached]. 18 studies, N = 2,560. Covert retrieval vs restudy **g = 0.23**, and per the blog summary **negligible after correcting for publication bias**, with large heterogeneity. Overt beat covert by **g = 0.17**. Suggested mechanism: covert searches stop early. Per the blog summary (not verified): covert retrieval works when it requires actually thinking of the answer, not when learners only judge a given answer; it helped longer-term rather than immediate retention; and feedback increased the benefit.
- **Primary studies.** Smith, Roediger & Karpicke (2013, *JEP: LMC*) [S]: covert retrieval was as good as overt, with word lists. Tauber et al. (2018) [S]: overt was better for complex material such as definitions. An earlier meta-analysis (Sundqvist et al. 2017) [S] found only a d = 0.07 overt advantage.
- **General testing effect, for scale.** Rowland (2014, *Psychological Bulletin*) g = 0.50 [0.42, 0.58]; Adesope, Trevisan & Sundararajan (2017, *RER*), testing beat restudy and all other comparisons [S for both]. These are mostly overt tests, so they set an upper bound for what a spoken prompt can achieve.
- **Delay and effort.** Karpicke & Roediger (2007, *JEP: LMC* 33(4), 704-719) [A via search]: delaying the first retrieval improved long-term retention. Pyc & Rawson (2009, *JML* 60, 437-447) [S]: harder successful retrievals, for example after longer gaps, gave better final recall. Spaced vs massed retrieval: Latimier, Peyre & Ramus (2021) g = 0.74 [S, secondary summary only]. A question about something said 20 seconds ago is answered from working memory and is the weakest form of retrieval.
- **Pause length.** No evidence was found for any particular pause length in audio. Rivers et al. used at least 5 s per prequestion for text. Classroom "wait time" research (Rowe) recommends 3 s or more, but it is about spoken answers in class [K]. 3 s is a guess. Longer may help for conceptual questions, at the cost of dead air.
- **Transfer to passive TTS: weak.** The listener can't be made to retrieve. Some won't, and those doing something else may not be able to. **Evidence strength: weak for covert prompts as such; moderate for the design rules** (delay the question, always give the answer).

### 2.3 Signalling (previews, signposts, connectives, flagging what matters)

- **Meta-analysis.** Schneider, Beege, Nebel & Rey (2018), "A meta-analysis of how signaling affects learning with media", *Educational Research Review* 23, 1-24 [S: figures from two independent summaries]. Retention g = 0.53 (139 comparisons), transfer g = 0.33 (70), cognitive load g = 0.25. Mostly visual cues (colour, arrows, highlighting); no spoken-only breakdown was found. Alpizar et al. (2020) [S]: d = 0.38.
- **Spoken signalling.** Mautone & Mayer (2001), *J. Educational Psychology* 93(2), 377-389 [S: abstract via search]. A lesson on aircraft lift with preview summary, headings and connectives ("because", "as a result"). Signalling improved transfer for printed text (Exp 1), **spoken text (Exp 2)** and narrated animation (Exp 3). Small lab samples [K].
- **TTS specifically.** Lorch, Chen & Lemarié (2012), *JEP: Applied* 18(3), 265-276, doi:10.1037/a0029547 [S: abstract fragments]: **preview sentences** improved listeners' outlines of TTS-rendered text vs no signals. **Headings worked in print but poorly in TTS audio**, because the visual cues headings carry (spacing, size) are lost. Chen (2015, Kentucky dissertation) [A]: audio headings helped note-taking; effects on cued recall and transfer were unclear.
- **Transfer to passive TTS: good, if the signal says what is coming.** This is the cheapest technique on the list. **Evidence strength: moderate** (meta-analysis mostly visual; two audio or TTS studies agree; outcomes in the TTS study were outlining, not long-term memory).

### 2.4 Pretraining (names and characteristics of key terms first)

- Mayer's pretraining principle: 5 of 5 tests with median d = 0.85 (2009 edition); 13 of 16 tests with median d = 0.75 (*Cambridge Handbook*, 2nd ed., ch. 13) [S]. A separate review lists d = 0.46 and notes the effect is stronger for low-knowledge learners [S]. Key study: Mayer, Mathias & Wetzell (2002, *JEP: Applied* 8, 147-154) [K]. The lessons were short, fast narrated animations, which makes the procedure close to a podcast; but the tests were done mostly by one lab, with small samples and immediate tests.
- **Transfer to passive TTS: plausible.** A listener can't glance back at a term's definition, so introducing two or three terms with a one-line characteristic before the mechanism lowers the load when they come up. **Evidence strength: moderate-to-weak** (the median-d tallies are not proper meta-analyses).

### 2.5 Advance organisers

- Luiten, Ames & Ackerson (1980, *AERJ* 17, 211-218) and Stone (1983) [S]: small positive average effects, with the 1960s-70s studies inconsistent; no breakdown for spoken organisers was found. The "organiser" is often hard to tell apart from a preview or signalling.
- **Transfer:** the episode roadmap already does this. **Evidence strength: weak, old.** No change beyond 2.3.

### 2.6 Spaced repetition (within and across episodes)

- Cepeda et al. (2006, *Psychological Bulletin* 132, 354-380) [A]: 839 assessments in 317 experiments; spaced beats massed study in verbal recall. Spaced retrieval: Latimier et al. (2021) g = 0.74 [S]. Very robust in general, but mostly word lists and facts, and the gaps that matter for long-term retention are days, not minutes.
- **Within an episode**, a 20-minute episode only allows minute-scale spacing. The useful lever is to ask about earlier segments later (2.2). **Across episodes**, re-asking a key point from a related earlier episode is the form with real spacing. But the listener may not have heard that episode, and there is no record of what they heard.
- **Transfer:** partial. **Evidence strength: strong in general, untested for podcasts.**

### 2.7 Concrete examples and analogies

- Concrete examples: Rawson, Thomas & Jacoby (2015, *Educational Psychology Review* 27(3), 483-504) [S]: concrete examples improved learning of declarative concepts, replicated by Micallef & Newton (2022) [S]. A related line of work suggests one example can tie the concept to that case, so varied examples are better for transfer [S]. Dunlosky et al. (2013) list concrete examples as supported [K].
- Analogies: no high-quality meta-analysis found. Alfieri, Nokes-Malach & Schunn (2013) on comparing cases, about d = 0.50 [S]. A Turkish science-education meta-analysis reports g = 1.03 [S, quality unknown; treat as unreliable]. The classroom literature says analogies help when the source is familiar and the mapping is made explicit, and can mislead otherwise [K].
- **Transfer: good.** Both are things the host says, so nothing is asked of the listener. **Evidence strength: moderate for examples, weak for analogies.** research/05 already requires one of each per segment. The only refinement is to make an analogy's mapping explicit and say where it breaks.

### 2.8 Elaborative interrogation, self-explanation, generation

- Dunlosky et al. (2013, *Psychological Science in the Public Interest*) [S]: elaborative interrogation and self-explanation rated "moderate utility". The learner generates the explanation; educational evidence is thin. Generation effect: Bertsch et al. (2007, *Memory & Cognition* 35, 201-210) [S], 86 studies, about d = 0.40, mostly word-level generation in lab tasks.
- **Transfer: poor.** All three need the learner to produce something. A podcast can only ask a "why" question and pause, which makes it a form of covert retrieval (2.2) with the same weak evidence. A host asking and answering their own "why" question is just an explanation, not elaborative interrogation. **Evidence strength for passive audio: very weak.** Do not add new prompt types for these.

### 2.9 Worked examples

- Strong for problem-solving domains (algebra, physics) [K]. A content segment explaining a mechanism is not that kind of task. The nearest use is in the Protocol segment: work through the plan for one concrete person ("Say you wake at seven and train at six in the evening..."). research/05 already does this in its do/don't table.
- **Transfer: limited to procedures. Evidence strength for this use: weak (by analogy only).**

### 2.10 Narrative, personalisation, conversational style

- Covered in research/02 (Ginns et al. 2013: retention d = 0.30, transfer d = 0.54, fading beyond about 35 minutes of instruction; Mar et al. 2021 on narrative). Nothing found in this pass changes that advice. The Ginns boundary at about 35 minutes is consistent with the episode lengths here.

### 2.11 Recaps and redundancy

- Mayer's "redundancy principle" is about adding on-screen text to narration, not about verbal recaps. It doesn't apply here.
- A restatement recap is restudy. In Szpunar et al. (2013, research/01), restudy did not beat no-test. Radio news: Burkum (1997, Michigan State dissertation) [S: abstract via search]: repeating information within a story improved recall of that information. A 1987 *Communication Research* study [S] reported better auditory recall with redundancy between audio and visuals. Both are modest, old and not about learning episodes.
- **Transfer:** a plain recap probably helps a little, especially for listeners who drifted (section 1). A retrieval-form recap adds a (weak) retrieval chance on top. **Evidence strength: weak** either way. research/05's design (retrieval form, plain restatement allowed in Quick) is reasonable.

### 2.12 Stating inferences (added)

- Following from Clinton-Lisell (2022), section 1: listeners lose more on inference than on literal content, mainly when they can't control the pace. A script can turn inferences into literal content by saying the "so what" out loud ("So the caffeine is still working at bedtime, even though you can't feel it").
- **Evidence strength: moderate for the listening gap; the fix is my inference** and has not been tested.

### 2.13 Saying the answer aloud (added; production effect)

- Producing a word aloud improves memory for it compared with reading it silently [K: MacLeod et al. 2010; the production effect]. Varao Sousa et al. (2013) [F] found reading aloud had the least mind wandering. A listener alone in a car could say the answer to a recall prompt aloud. That is a bigger change in what the listener does than covert recall, and the evidence on it is mostly single words. **Weak; optional.**

---

## 3. Summary table

| Technique | Best evidence | Tested with audio? | Passive TTS transfer | Strength |
|---|---|---|---|---|
| Prequestion before segment (guess) | Meta g = 0.54 specific, ~0 general; AV g = 0.66 | Video yes; one podcast RCT (abstract) | Good, specific to the asked point | **Moderate** |
| Spoken preview sentences, connectives | Signalling meta g = 0.53 (mostly visual) | Yes (Mautone & Mayer Exp 2; Lorch TTS) | Good | **Moderate** |
| Saying the inference explicitly | Listening inferential gap g = 0.36 | Yes (listening vs reading) | Good | Moderate (gap); fix untested |
| Pretraining key terms | Median d 0.75-0.85 (tallies) | Narrated animation | Plausible | Moderate-weak |
| Lagged covert recall | Covert g = 0.23 (≈0 bias-corrected); delay helps | No | Weak | **Weak** |
| Concrete examples | Rawson 2015, replication | No | Good | Moderate |
| Analogies | No good meta-analysis | No | Good | Weak |
| Spacing across episodes | Cepeda 2006, very robust | Lists, not podcasts | Partial | Strong in general, untested here |
| Recap (restatement) | Restudy ≈ no gain; radio redundancy | Radio (dissertation) | Fine | Weak |
| Advance organisers | 1980s meta-analyses, small | Not found | Already in roadmap | Weak |
| Elaborative interrogation / self-explanation / generation | Moderate utility, needs output | No | Poor | Very weak here |
| Worked examples | Strong for problem solving | No | Protocol segment only | Weak here |
| Personalisation, narrative | research/02 | research/02 | research/02 | research/02 |

---

## 4. Ranked changes to research/05 section 2.8 (recall prompts) and segment design (2.4)

Proposed for the owner. Not applied. Ranked by evidence strength times how cheaply it fits the existing word budget.

1. **Add a prequestion to the start of every content segment, and close it at the end.** After the signpost (2.4 step 1), the host asks the one question the segment will answer and invites a guess: "Here's what this part answers. If caffeine wears off in a few hours, why can a three o'clock coffee still cost you sleep? Take a guess. [think]" The question targets the segment's **central idea**, never a side fact, because the effect is specific and a factual prequestion may draw attention away from the rest at fixed pace. Then the segment's end-of-segment recall prompt **re-asks the same question** after the explanation, so the listener gets answer, feedback and closure. Cost: about 20-30 words per segment, about 100 words in a Standard episode; take it from the 60-120-word "way in" (step 2), which the prequestion partly replaces. *Evidence: moderate* (St. Hilaire 2024 [F]; Rivers 2026 covert = overt [F]; Weinstock 2020 podcast RCT, targeted items only [A]).
2. **Make every signpost a spoken preview sentence, not a label, and use explicit causal connectives.** "Idea two." on its own is a heading, and headings failed in TTS audio. Require: number + what the segment explains + why it matters, in one or two sentences, plus "because", "so", "which means" at the causal joints of the mechanism. Lint check (M): each signpost contains more than its label. *Evidence: moderate* (Lorch 2012 TTS [S]; Mautone & Mayer 2001 spoken [S]; Schneider 2018 [S]).
3. **Say the inference.** Add to 2.4 step 3 or step 6: every mechanism ends with one explicit "so what" sentence that states the conclusion the listener would otherwise have to infer. *Evidence: moderate for the listening deficit (Clinton-Lisell 2022 [S]); the fix itself is untested.*
4. **Lag the recall prompts.** Change 2.8 from "a recall prompt at the end of segments 1-3, about that segment" to: the end of segment *n* closes segment *n*'s prequestion (change 1), and from segment 2 on, **adds one recall question about an earlier segment** in place of a second question on the current one. The cumulative recap keeps its retrieval form. This keeps the prompt count the same and turns near-immediate repetition into delayed retrieval. *Evidence: moderate for the principle (Karpicke & Roediger 2007 [A]; Pyc & Rawson 2009 [S]), weak for covert prompts as such (Yu 2025 [S]).*
5. **Pretrain two or three key terms.** In the Roadmap or right after a segment's preview, name each term the mechanism depends on with a one-line characteristic ("Adenosine, the chemical that builds up the longer you're awake"). Only for terms used again later. *Evidence: moderate-to-weak* (Mayer pretraining tallies [S]).
6. **Pause rule for prompts: 3 s for one-fact answers, 4-5 s for "why" questions, answer always given after.** Never skip the answer: feedback carries much of the retrieval benefit, and listeners who didn't retrieve still get the content. Drop any wording implying the prompt is proven. In 2.8, replace "cheap and plausible, not proven" evidence text with the Yu 2025 figures. *Evidence: weak* (no audio pause-length data found).
7. **Optional cross-episode callback.** When an episode builds on an earlier one, open the first content segment with one retrieval question from that episode, answered at once (it also works as a recap for new listeners). *Evidence: strong for spacing in general, untested for podcasts.*
8. **Do not add** elaborative-interrogation, self-explanation or "generate it yourself" prompts as separate devices, and do not lengthen the recap. They would add dead air or words for effects that depend on output the listener can't give. Keep one analogy and one concrete example per segment, but state the analogy's mapping and where it breaks. *Evidence: very weak for passive audio.*

Net word cost of 1-5: roughly +100 to +150 words in a Standard episode, offset by shortening the "way in" step. The 3,300-word budget holds within its 2,900-3,700 range. Owner question 7 in research/05 (cut prompts to one per episode if annoying) still applies. Under this design, the prequestions are the last thing to cut, not the first.

---

## 5. Gaps

- No study found tests any of these with **TTS audio in a divided-attention setting**, or measures retention beyond a few weeks.
- Weinstock et al. 2020 full text (question placement, wording, pauses) was not retrieved. It's worth reading before finalising change 1.
- Yu et al. 2025 abstract and moderator tables were not reached. The g = 0.23 and g = 0.17 come from Rivers et al. 2026 [F], and the bias-corrected "negligible" from a blog summary.
- Schneider et al. 2018, Mautone & Mayer 2001, Lorch et al. 2012 and Clinton-Lisell 2022 were read only at abstract or summary level. None gave a spoken-only effect size.
- Prequestion effects are mostly measured with tests that match the prequestions, after minutes. Real-world value for a health listener a week later is unknown.

## Sources

- St. Hilaire, Chan & Ahn (2024), *Psychon. Bull. Rev.* 31, 411-441. [PDF via NSF PAR](https://par.nsf.gov/servlets/purl/10511812) [F]
- Rivers, Berdelis, Pan & Tauber (2026), *Appl. Cogn. Psychol.* 40:e70165. [PDF](https://sc-pan.github.io/pdf/RBPT_2026.pdf) [F]
- Weinstock et al. (2020), *Ann. Emerg. Med.* 76(3), 353-361. [PubMed](https://pubmed.ncbi.nlm.nih.gov/32317122/) [A]; [WestJEM 2019 abstract](https://journalpub.escholarship.org/westjem/article/13052/galley/6839/download) [A]
- Yu et al. (2025), *Educ. Psychol. Rev.* 37:52, [doi:10.1007/s10648-025-10024-4](https://doi.org/10.1007/s10648-025-10024-4) [S]; [blog summary](https://tipsforteachers.substack.com/p/research-bite-33-is-covert-retrieval) [S]
- Smith, Roediger & Karpicke (2013), *JEP: LMC*. [PDF](https://pcllab.github.io/downloads/2013/2013_Smith_Roediger_Karpicke_JEPLMC.pdf) [S, not opened]
- Varao Sousa, Carriere & Smilek (2013), *Front. Psychol.* 4:892. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3842750/) [F]
- Clinton-Lisell (2022), *Rev. Educ. Res.*, [doi:10.3102/00346543211060871](https://doi.org/10.3102/00346543211060871) [S]
- Schneider, Beege, Nebel & Rey (2018), *Educ. Res. Rev.* 23, 1-24 [S]; [QIC summary](https://www.qic-wd.org/sites/default/files/Umbrella%20Summary%20-%20Signaling%20in%20Training%20111021.pdf)
- Mautone & Mayer (2001), *J. Educ. Psychol.* 93(2), 377-389 [S]
- Lorch, Chen & Lemarié (2012), *JEP: Applied* 18(3), 265-276, [doi:10.1037/a0029547](https://doi.org/10.1037/a0029547) [S]; Chen (2015), [dissertation](https://uknowledge.uky.edu/psychology_etds/60) [A]
- Mayer pretraining: *Cambridge Handbook of Multimedia Learning*, [chapter](https://www.cambridge.org/core/books/cambridge-handbook-of-multimedia-learning/principles-for-managing-essential-processing-in-multimedia-learning-segmenting-pretraining-and-modality-principles/DD24C2F48B9B1277CE59F78276110258) [S]
- Karpicke & Roediger (2007), *JEP: LMC* 33(4), 704-719 [A]; Pyc & Rawson (2009), *JML* 60, 437-447 [S]
- Cepeda et al. (2006), *Psychol. Bull.* 132, 354-380, [PubMed](https://pubmed.ncbi.nlm.nih.gov/16719566/) [A]; Latimier, Peyre & Ramus (2021) [S]
- Rowland (2014), *Psychol. Bull.* [S]; Adesope, Trevisan & Sundararajan (2017), *RER* 87(3), 659-701 [S]
- Hamaker (1986), *RER* 56(2), 212-242 [S]
- Luiten, Ames & Ackerson (1980), *AERJ* 17, 211-218 [S]
- Rawson, Thomas & Jacoby (2015), *Educ. Psychol. Rev.* 27(3), 483-504 [S]; Alfieri et al. (2013) [S]
- Dunlosky et al. (2013), *PSPI*, doi:10.1177/1529100612453266 [S]; Bertsch et al. (2007), *Mem. Cognit.* 35, 201-210, [PubMed](https://pubmed.ncbi.nlm.nih.gov/17645161/) [S]
- Burkum (1997), radio news redundancy, [MSU dissertation](https://d.lib.msu.edu/etd/26385/FULL_TEXT/view) [S]
- Middlebrooks, Kerr & Castel (2017), *Psychol. Sci.*, [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5546942) [S]
