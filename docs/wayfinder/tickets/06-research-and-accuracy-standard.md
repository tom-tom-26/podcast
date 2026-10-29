---
title: Research and accuracy standard
type: grilling
status: closed
blocked-by: []
claimed-by: owner (this session)
---

## Question

How should the skill research a topic and what standard of sourcing does a script have to meet, especially for health and training claims? Decide: source types allowed, minimum number of sources, how uncertainty and conflicting evidence are voiced, disclaimers, and what the skill refuses or flags.

## Resolution

Closed 2026-10-29. Decided with the owner:

- **Source ladder:** systematic reviews and meta-analyses, then RCTs and major guidelines, then single peer-reviewed studies and expert reviews, then books and commentary for context only. Blogs, vendors and influencer claims never count as evidence. Tier 3 and below is voiced as weaker evidence.
- **Minimum sourcing:** at least 3 distinct sources, aiming for 5. Fewer only when extra sources add very little. Every factual claim traces to a source; unsourced claims are cut or voiced as the host's inference.
- **Uncertainty:** evidence strength stated in plain spoken words (strong, early, mixed); conflicts presented as both sides; animal and cell findings labelled as such.
- **Disclaimers:** optional, left to the skill's judgment. No mandatory line, no repetition. Targeted cautions where the content is risky.
- **Risky topics:** never refuse and never stop to ask. Write the episode with conservative framing and a specific caution, and flag the topic as higher-risk in the show notes.
- **Non-health topics:** one standard for everything, disclaimers adapted to the topic.
- **Claim-check:** a second pass, kept cheap. While researching, the skill builds a compact ledger (one line per claim: claim, source, evidence tier). The claim-check compares the script to the ledger without re-reading sources, and the ledger doubles as the bundle's source list. Research effort scales with topic breadth.
- **Zero-input rule:** the owner gives only a topic. If the topic is genuinely too broad, the skill asks one short drill-down round (a few options with a recommended default, answerable in a single reply) and no more. Narrow topics go straight to the script. Any angle the owner includes is a hint.

## Amendments (Opus review, 2026-10-29)

Reviewer: opus-agent. This is a closed, owner-decided ticket. Nothing below changes the decision; items 1-5 are **recommendations for the owner** and need sign-off. Index: `research/opus-review-2026-10-29.md`.

1. **Add a read-depth field to every ledger line** (full text / abstract / secondary). The earlier research tickets (01, 02, 03) failed in exactly this way: several numbers were taken from search summaries and some turned out wrong (an edition mix-up for Mayer's effect size, a positive study reported as a mixed replication, a misattributed DOI). Proposed rule: a specific number spoken in a Script must come from a full text, or from an abstract that states that number. A summary-only source may support context, never a number. Cost: one word per ledger line.
2. **Spot-check load-bearing numbers against the source.** The cheap claim-check compares Script to ledger, so it cannot catch a ledger line that misread its source. Proposed: re-open the source for the two or three numbers the protocol depends on (doses, timings, thresholds) and confirm them. Small cost, and it targets the claims where a mistake does harm.
3. **Voice size and population along with tier.** The ladder ranks study designs, so a 12-person trial counts as tier 2 next to a 5,000-person trial. Ticket 05's draft voices both ("one small but careful trial"). Recommend the ledger line records n and population.
4. **Allow a "textbook consensus" marker for mechanisms.** Long-established mechanisms (for example, caffeine blocking adenosine receptors) are usually sourced from expert reviews or textbooks, which are tier 3 and would be voiced as "early evidence". That understates them. Proposed: a `consensus` marker for mechanism claims supported by an authoritative review and not contested, voiced as "textbook".
5. **Missing source-quality checks:** source age (prefer the last ~10 years unless a classic; say when a finding is old), retraction status for any single study that carries a protocol (Crossref now carries the Retraction Watch data), industry funding or conflicts for supplement and product claims, and absolute rather than relative risk where the source allows.

Notes, no decision needed:

6. *Contradiction resolved:* research/02 rule 5 called for a short standing disclaimer; this ticket decided there is none. This ticket wins (marked in research/02).
7. *"Never refuse" has a boundary the skill does not control.* The model running the skill may decline some content regardless of this standard (for example, instructions that facilitate serious harm). The spec should say what happens then: the skill writes the safest useful version, and says in the session output what it left out and why. Suggested for ticket 07 or the skill spec.
8. *Copyright.* Scripts and show notes are published in a public repo. Paraphrase sources; quote at most a sentence, attributed.
9. *Interface with ticket 05:* claim tags `{cN}` in the Script make the claim-check mechanical (research/05 section 9.2).

## Amendments approved by owner via ticket 05 (2026-10-29)

These are owner-approved and binding. (Recommendations 1-5 above were signed off on 2026-10-29; see the end of this file.)

- **Any-topic scope:** the source ladder above is the Health profile. Every topic uses the source profile for its field (research/05 section 13: 15 starter profiles). A field with no profile gets one drafted during research and saved to Learnings (ticket 10). The general standard here (3-5 sources, the ledger, traceability) applies to all fields.
- **News and current events:** the primary document plus at least 2 independent reputable outlets for each key claim. The Script says the date aloud. Reported fact, open dispute and the host's analysis are labelled as such. Contested political claims get both sides fairly.
- **Zero-input rule replaced:** the skill sends one confirm message (proposed length and outline, plus any drill-down question) and the owner replies "go" or tweaks it. Still one round only (research/05 12.4).
- **Evidence voicing generalised:** the spoken strength phrases fit any field, not only study tiers. Checks that only make sense for studies, such as naming animal or cell findings, apply to science and health only.

## Owner sign-off of recommendations 1-5 (2026-10-29)

All five accepted:
1. Every ledger line carries a read depth (full text / abstract / secondary). **Firm:** a number spoken in the Script comes from a full text, or from an abstract that states that number.
2. **Firm:** the two or three load-bearing numbers are re-checked against the source before the Bundle is emitted.
3. Ledger lines for study sources record n and population.
4. A `consensus` marker for uncontested mechanisms backed by an authoritative review, voiced as "textbook" (research/05 2.6).
5. Soft checks for source age, conflicts of interest and absolute rather than relative risk. **Firm:** a retraction check (Crossref / Retraction Watch) on any single study that carries a protocol.
