# Research and accuracy standard

From ticket 06 with recommendations 1-5 signed off, research/05 sections 2.5, 2.6 and 13, and research/13 section 2. **Firm** marks the rules with no leniency. Everything else is soft.

## Source profiles

Each field of topics has a Source profile: what counts as strong evidence, what to watch for, and what triggers the Higher-risk flag. Each one is at the top of its field file in `learnings/fields/`; `learnings/INDEX.md` matches a Topic to its field.

- **Overlap rule:** a Topic can draw on two profiles (sport training uses Sport and Health). The stricter flag rule applies.
- **No profile fits:** draft one with the same three bullets during research, borrowing the risk triggers of the strictest neighbouring profile, use it, and save it as a `draft` field file (`references/learnings.md`).

## The ladder

Health's ladder is the model; a profile changes which sources sit at the top.

1. Systematic reviews and meta-analyses.
2. RCTs and major guidelines.
3. Single peer-reviewed studies and expert reviews.
4. Books and commentary, for context only.

Blogs, vendors, press releases and influencers never count as evidence. Tier 3 and below is voiced as weaker evidence.

- At least 3 distinct sources, aiming for 5. Fewer only when extra sources add very little.
- Every factual claim traces to a ledger line. **Firm.** An unsourced claim is cut, or voiced as the host's inference.
- Paraphrase sources. Quote at most a sentence, attributed. The Bundle is public.
- **News and current events:** the primary document plus at least 2 independent reputable outlets for each key claim. Say the date aloud. Label reported fact, open dispute and the host's analysis as such. Contested political claims get both sides fairly.
- **Soft checks:** source age (prefer the last ten years unless it's a classic, and say when a finding is old); industry funding or conflicts behind supplement and product claims; absolute rather than relative risk where the source gives it.

## Reading raw text

WebFetch hands back a small model's summary of the page, so a number read through it is secondary at best. Search snippets are worse. **Firm:** a number that carries weight is read from the raw text.

```
# A web page: fetch it, then search it for the number
curl -sL "<url>" -o /tmp/src.html && grep -o -i ".\{0,200\}<keyword>.\{0,200\}" /tmp/src.html

# A PDF
curl -sL "<pdf url>" -o /tmp/src.pdf && pdftotext -layout /tmp/src.pdf - | grep -n -i "<keyword>"

# A PubMed abstract, as plain text
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=<PMID>&rettype=abstract&retmode=text"
```

If `pdftotext` is missing, `apt-get install -y poppler-utils`. WebSearch and WebFetch are fine for finding sources and for context.

A source behind a paywall or a bot wall is read as far as you can: its abstract, or a secondary account. Record the read depth honestly and voice it accordingly.

## The Claim ledger

`ledger.md`, one line per claim, written while researching, with no header line. Seven fields, separated by ` | `:

```
id | claim | source | tier | read depth | n and population | tags
```

- **id**: `c1`, `c2`, ... in the order you find them. A Claim tag `{c7}` in the Script points here.
- **claim**: what the source says, in your own words, with any number exactly as the source states it.
- **source**: author and year, title or venue, and a DOI or URL.
- **tier**: `1` to `4` on the profile's ladder.
- **read depth**: `full text`, `abstract` or `secondary` (anything summarised: WebFetch, a search snippet, a news story about a study).
- **n and population**: for a study, the sample size and who was studied (`n=12 healthy young sleepers`); `-` for anything that isn't a study.
- **tags**: comma-separated, or `-`:
  - `consensus`: an uncontested mechanism backed by an authoritative review, voiced as textbook.
  - `animal` or `cell`: the finding is in animals or cells, not people.
  - `load_bearing`: the advice or the Episode's main point depends on it.
  - `surprise`: a fact the default listener probably gets wrong; a Segment can open on it.
  - `misconception`: a common belief this line corrects; it can carry a simulated listener question.
  - `rechecked`: a load-bearing number confirmed against the raw text in step 4.
  - `retraction_checked`: the retraction check ran and found nothing.

An example:

```
c2 | 400 mg caffeine 6 h before bed cut objectively measured sleep by more than 1 h; participants did not report worse sleep | Drake et al. 2013, J Clin Sleep Med 9(11):1195-1200, doi:10.5664/jcsm.3170 | 2 | abstract | n=12 healthy sleepers | load_bearing, surprise
```

`pipeline lint` warns on a line that isn't in this shape.

## Firm number and retraction checks

These run in step 4, before lint.

- **Spoken numbers.** Every number in the Script comes from a `full text` line, or an `abstract` line whose abstract states that number. A `secondary` line may support context, never a number.
- **Load-bearing numbers.** Pick the two or three numbers the advice or main point rests on (doses, timings, thresholds, the headline figure). Re-open each source's raw text and confirm the number and what it measured. Tag the line `rechecked`.
- **Retractions.** For each single study a protocol action rests on:

  ```
  curl -s "https://api.crossref.org/works?filter=updates:<DOI>&rows=20" | jq '[.message.items[] | .["update-to"][]? | {type, DOI: .DOI}]'
  ```

  Crossref lists the notices that update a DOI, and carries the Retraction Watch data. A `retraction` or `withdrawal` against the study's DOI means it comes out. Report an `expression_of_concern` in the final message. For a PubMed record, its publication types also say "Retracted Publication". Tag the line `retraction_checked`.

## Voicing the evidence

Every load-bearing claim gets one evidence phrase, once, at the claim. The tier decides the meaning; the wording rotates between phrasings of the same strength. Never upgrade a tier for variety.

| Ledger | Say, for example | Never |
|---|---|---|
| Tier 1, consistent | "This is well supported. A review pooling twenty-four studies found..." / "The evidence here is strong." | "Science has proven" |
| `consensus` | "This part is textbook." / "This has been understood for decades." | |
| Tier 2 | "Good trials show..." / for one small trial, "One small but careful trial found..." | "Studies show" with nothing after it |
| Tier 3 | "Early evidence." / "One study suggests..." | "Research confirms" |
| Mixed | "The evidence is mixed. On one side... On the other..." | Picking a side without saying so |
| `animal`, `cell` | "In mice..." / "In cells in a dish, not yet in people." In the same sentence as the finding. | The species in a later sentence |
| Tier 4 | Context only: "The author argues..." | As evidence |
| No source | "This is my inference, not a finding." | Stated as fact |

Other fields get phrasings that fit them at the same strengths: "the official figures show", "historians mostly agree", "two independent outlets report".

Size and population count as much as tier: a twelve-person trial is voiced as small, and who was studied is said when it limits the advice ("in young men"). The animal and cell labels apply to science and health Topics only.

## Risky Topics

**Firm:** never refuse a Topic, and never stop to ask about risk.

- Write it with cautious framing. Each caution is specific and sits in the same paragraph as the action it qualifies, right after the dose or timing. It says who, what risk, and what to do instead: "If you take blood pressure medication, don't add this without asking your doctor, because it can lower pressure further." Never "consult a professional".
- A Higher-risk Episode adds one caution line in the Roadmap, never in the Hook.
- **Firm:** no standing disclaimer anywhere.
- In `meta.yaml`, `risk_flag: true` and a one-line `risk_reason`. The show notes open with `Higher-risk topic: <reason>.`
- Higher-risk means the profile's trigger fires: medication, supplements with known interactions, fasting, extreme training loads, heat or cold exposure, pregnancy, mental-health crises, investing, debt or tax, or any action where a plausible mistake causes harm. When unsure, flag.

The model running this Skill may still decline some content, for example instructions that would help someone cause serious harm. Then write the safest useful version and say in the final message what you left out and why.

## The claim-check

A second pass, kept cheap: compare the Script with the ledger, without re-reading the sources (step 4's number checks are the exception).

- Each tagged sentence: the ledger line supports it, at the strength the sentence voices it.
- Each untagged sentence: it makes no factual claim. Fix it if it does.
- Each spoken number: its line passes the firm number rule above.
- Each content Segment carries at least one Claim tag (lint blocks otherwise).
- Every ledger line the Script uses is in the show notes' source list.
