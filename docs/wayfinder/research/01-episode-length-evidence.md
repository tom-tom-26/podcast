# Research 01: Episode length evidence

Ticket: `wayfinder/tickets/01-episode-length-evidence.md`

Question: what does credible evidence say about the best length for an audio learning episode, how long listeners can focus and retain, what the default should be (owner suggests ~20 min), and when to split into parts.

## Bottom line up front

- No study directly measures retention vs. length for **audio-only learning podcasts**. Everything below is adjacent evidence (video lectures, classroom lectures, one creator's podcast analytics). Confidence in any exact number is low-to-moderate.
- The popular "attention span is 8 seconds / 10-15 minutes" claims are not well supported. Length per se is a weak lever; **structure and active recall** are strong ones.
- ~20 min is defensible as a default. The evidence supports it as long as the episode is built from short coherent segments with built-in recall, not as one continuous lecture.

## Findings

### 1. The "attention span" numbers are mostly myth

- The "8 seconds" figure traces to a 2015 Microsoft Canada marketing report that borrowed it from a commercial statistics website, with no method shown. See the [Wisconsin psych myth-busting handout](https://internet.psych.wisc.edu/wp-content/uploads/532-Master/532-UnitPages/Unit-09/Goldfish_MythBusting.pdf) and [Genetic Literacy Project summary](https://www.geneticliteracyproject.org/2016/07/25/another-modern-myth-shrinking-attention-spans/). (Secondary sources; I did not retrieve the Microsoft report itself.)
- The "attention drops after 10-15 minutes of lecture" claim: Wilson & Korn (2007), ["Attention During Lectures: Beyond Ten Minutes"](https://doi.org/10.1080/00986280701700391) (*Teaching of Psychology*), found the claim rests on thin, mostly non-empirical sources (for example Lloyd 1968) and that note-taking patterns did not show a clear decline. Bradbury (2016), ["Student attention during lectures"](https://journals.physiology.org/doi/full/10.1152/advan.00109.2016) (*Advances in Physiology Education*), traces the claim to a single 1978 manuscript. Caveat: I could not open either full text (HTTP 403 / not retrieved), so these points come from search-result summaries. Verify before quoting.
- Counterpoint: Young, Robinson & Alberts (2009) report a vigilance decrement in standard lectures that impairs learning (seen via search summary only). Attention does vary with time, but there is no clean "cliff" at a fixed minute. It depends on task demand and engagement.

### 2. Shorter segments win engagement (video, not audio)

- Guo, Kim & Rubin (2014), ["How Video Production Affects Student Engagement: An Empirical Study of MOOC Videos"](https://www.cs.rochester.edu/hci/pubs/pdfs/edX-MOOC-video-production-and-engagement_LAS-2014.pdf) (ACM Learning@Scale, [doi:10.1145/2556325.2566239](https://doi.org/10.1145/2556325.2566239)). 6.9M edX video-watching sessions. Verified in the paper text: "Shorter videos are much more engaging... segment videos into chunks shorter than 6 minutes." Also: informal, talking-head-style, fast and enthusiastic delivery engaged more.
- Limits: video, MOOC context, engagement measured as watch time, observational. It argues for chunking, not for a total-length cap. Whether a listener on a commute behaves the same is unproven.

### 3. Segmenting with learner pacing improves learning

- Rey et al. (2019), ["A Meta-analysis of the Segmenting Effect"](https://doi.org/10.1007/s10648-018-9456-4) (*Educational Psychology Review* 31, 389-419): 56 investigations, 88 comparisons; small-to-medium benefits for retention and transfer when multimedia instruction is split into meaningful segments, plus lower cognitive load and longer learning time. Per the abstract, these effects also hold for system-paced segmentation, so learner control is not required. Learners with higher prior knowledge benefited more, for retention only. (Abstract-level reading via [MPI record](https://is.tuebingen.mpg.de/publications/rey2018segmenting). Corrected 2026-10-29, see Amendments.)
- Implication: fixed, clearly bounded segments in a podcast are within the evidence even without the listener pausing. Clear section boundaries help.

### 4. Active recall inside an episode beats length tuning

- Szpunar, Khan & Schacter (2013), ["Interpolated memory tests reduce mind wandering and improve learning of online lectures"](https://pmc.ncbi.nlm.nih.gov/articles/PMC3631699/) (*PNAS*). 80 undergraduates over two experiments (n = 32 and n = 48), 21-min statistics video in four ~5.5-min segments. After each segment: 1 min of arithmetic, then either a 2-min typed quiz of six questions or more arithmetic. Mind-wandering probes (Experiment 2 only): tested 19%, restudy 39%, untested 41%. Final cumulative test, all segments, both experiments combined: tested 90%, restudy 76%, untested 68%. Re-study alone did not help. (Details verified against the PMC full text, 2026-10-29.)
- Follow-ups: Jing, Szpunar & Schacter (2016, *J. Exp. Psychol.: Applied* 22(3), 305-318, [manuscript](https://sites.harvard.edu/schacter-memory/files/2022/08/jing2016-1-1.pdf)) extended the benefit to a 40-min lecture (tested learners learned more and integrated better than restudy). A larger replication, Welhaf et al. (2022, *Cognitive Research: Principles and Implications*, N = 195, [doi:10.1186/s41235-022-00372-y](https://doi.org/10.1186/s41235-022-00372-y)), found only a small, uncertain drop in task-unrelated thought (d about -0.29, BF10 about 1) and no evidence that interpolated tests improved learning. The tests in all three were typed quizzes, a stronger intervention than a spoken prompt to a listener. So this is promising but fragile evidence for periodic recall prompts, and it supports retrieval (question, then answer) rather than recap. The 21- and 40-min lectures bracket the owner's 20 min target. (Corrected 2026-10-29, see Amendments: Jing 2016 was previously described as a mixed replication.)

### 5. Podcast listening data: thin and mostly unreliable

- Best first-party data found: Robert Wiblin, ["Our data suggest people keep listening to podcasts even if they're very long"](https://medium.com/@robertwiblin/our-data-suggests-people-keep-listening-to-podcasts-even-if-theyre-very-long-483dcfc77c02) (Apple Podcasts analytics for one show). Reported (via search summary; page returned 403 on direct fetch): no relationship between length and the share who start, the biggest drop-off is early while listeners decide if the topic interests them, and good content keeps listeners through long episodes. Single show, interview format, not a learning context.
- Edison Research / Triton "Infinite Dial" (2017/2018, self-reported, summarized by [RAIN News](https://rainnews.com/key-insights-from-the-infinite-dial-2017/)): about 40% say they finish episodes, 80% finish most or all. Self-report overstates behavior.
- Unreliable, do not rely on: vendor blogs quoting "18-22 min sweet spot" or "68.4% completion" with no methodology (for example [key-g.com](https://key-g.com/podcast-statistics-2025-global-listener-growth-and-trends), [voxbooster.com](https://www.voxbooster.com/blog/podcast-completion-rate-statistics-2026)). I found no public, length-binned completion dataset from Apple, Spotify, or a research firm.

## Gaps and caveats

- No peer-reviewed study of audio-only learning episode length vs. retention was found. Closest are video lecture studies.
- Several sources were read only through search summaries (Bradbury, Wilson & Korn, Wiblin, Jing et al.). The two I read in full or near full: Guo et al. (text of recommendation), Szpunar et al. (via PMC).
- The tool's content (health/self-improvement, a single voice, no visuals) is closer to audio lecture than to MOOC video, so lean on structure-based findings.

## Recommendation

**Default length: about 20 minutes (range 15-25).**
- Supported by: Szpunar et al. used a 21-min lecture successfully; no evidence of a hard attention cliff at 10-15 min; podcast data suggest listeners stay for long episodes when interested.
- Do not go well under 10 min as a default: the tool's value is a full, sourced explanation of a topic, and the evidence does not penalize 15-25 min.

**Build each episode from 4-5 segments of about 4-6 minutes**, each with a clear spoken signpost (Guo et al.: chunks under 6 min; Rey et al.: coherent segments help). After each segment, include a one- or two-sentence **recall prompt** or recap (Szpunar et al.). Put the hook and the "why this matters / what you'll learn" in the first 60-90 seconds, since early drop-off is where the loss happens (Wiblin).

**When to split into parts:**
1. Script naturally exceeds ~25-30 minutes of speech after trimming. Rough rule: if it needs more than 5-6 segments, split.
2. The topic has two or more independently useful sub-questions (for example "how it works" vs. "how to apply it"), so each part can stand alone.
3. Prefer splitting at a segment boundary, with a recap at the start of part 2 and a one-line teaser at the end of part 1. Aim for 15-22 min per part, 2-3 parts maximum per topic.
4. Do not split just to hit a number below 20 min. Short is not evidenced to be better, and splitting adds friction (more downloads, more feed clutter).

**Treat these as tunable defaults**: log episode length in metadata and let the owner's own feedback (not folklore) adjust the default later. That belongs to the feedback-loop item on the map.

## Amendments (Opus review, 2026-10-29)

Reviewer: opus-agent. Index of all review changes: `research/opus-review-2026-10-29.md`.

**Corrections made in the text above**

1. *Szpunar et al. 2013.* Added the design detail that matters for this project: the "tests" were 2-minute typed quizzes of six questions, and the mind-wandering figures come from Experiment 2 only (n = 48), while the 90/76/68% figures are the combined cumulative test. Verified against the PMC full text. A spoken "pause and recall" prompt is a weaker intervention than what was tested.
2. *Jing et al. 2016* was described as a "mixed" replication. It was positive: tested learners did better in a 40-minute lecture. The weakening result is Welhaf et al. 2022 (N = 195): small, statistically uncertain reduction in mind-wandering and no learning benefit. Both added with citations.
3. *Rey et al. 2019.* The text said the benefit came from "learner-paced" segments and was larger with higher prior knowledge. The abstract says the effects also hold for system-paced segmentation, and the prior-knowledge moderation applies to retention only. Corrected. This strengthens the case for fixed segments in audio.

**Verification of sources that were summary-only**

4. *Bradbury 2016* (*Adv. Physiol. Educ.* 40, 509-513). Now read in full text (PDF via EPALE). Confirms: the 10-15 minute claim traces to Hartley & Davies (1978), a review of note-taking, not attention; Bradbury shows note-taking is not a valid attention proxy and that note-taking declines tracked lecture content, not fatigue. The finding stands, now verified.
5. *Wilson & Korn 2007* (*Teaching of Psychology* 34(2), 85-89). Full text still not retrieved; secondary summaries agree that the cited support was largely indirect or non-empirical and that no specific average span was established. Unchanged, still summary-level.
6. *Wiblin 2020* (Medium). Still 403. Secondary sources confirm Apple Podcasts Analytics as the data source and that the show's average episode was about two hours at the time. Single long-form interview show. Treat as an anecdote, not evidence about learning episodes.

**Reasoning problems**

7. *Segment arithmetic.* The recommendation "4-5 segments of about 4-6 minutes" for a ~20 min episode sums to 16-30 minutes of content before hook, protocol and recap. It cannot be met at the default length. Guo et al.'s "under 6 minutes" is a ceiling. Ticket 05's draft resolves it as 4 content segments of ~3.5 min plus a ~3 min protocol segment, which keeps "4-5 segments". **Recommendation for owner:** reword the map decision line for ticket 01 to match once 05 is signed off. Not a material change to the decision.
8. *"Strongest single piece of evidence" overstated.* With Welhaf 2022 added, the recall-prompt recommendation still stands because it is cheap and low-risk, but it is plausible rather than demonstrated. Ticket 05 designs prompts as real retrieval (question, pause, answer), because restudy did not help in Szpunar.
9. *Missing consideration: playback speed and listening context.* Many podcast listeners use 1.2-2x playback, and comprehension holds up to about 270 wpm (Kuperman et al. 2021, see research/02 amendments), so total length is partly under the listener's control. Divided-attention contexts (walking, gym, driving) are not covered by any lab study cited here. Neither changes the default, but both argue against cramming information into segments.
10. *Missing evidence: measured pace.* The file did not convert minutes to words. Measured Kokoro output runs 159-190 wpm (ticket 05, section 1), so a 20-minute episode is about 3,300 words, not the 3,000 implied elsewhere.

No change to the closed decision (default ~20 min, segments with recall prompts, split above ~25-30 min).
