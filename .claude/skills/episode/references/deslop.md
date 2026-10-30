# De-slop checklist

From research/18 sections 2, 3, 8 and 9, signed off 2026-10-29. Slop is what fills the space when there's no specific fact, no stake and no view, so the fix starts upstream: each Segment carries a sourced surprise, a concrete case and a committed view. Scrubbing words comes second.

The phrase list is `config/deslop_rules.yaml`, and `pipeline lint` runs it over the Script, title, summary and show notes. Its `block` list is the core ten (F9); everything else only warns.

## Firm rules

| | Rule | Checked by |
|---|---|---|
| F1 | No unattributed evidence: "studies show", "research shows" or "confirms", "experts say" or "agree", "some argue", unless the same sentence names the kind of evidence and carries a Claim tag. | you; lint warns on the phrases |
| F2 | No first-person memory or experience: "when I tried", "I remember", "my clients", "my listeners". "Here's how I'd read that" is fine. | you; lint warns |
| F3 | No false calls to action or claims about the interface, anywhere: subscribe, review, comment, "link in the description", "see you next week" or any schedule. | you; lint warns on the phrases |
| F4 | The title and summary never promise more than the Episode delivers, and never state a claim the ledger doesn't support. | you |
| F5 | No fillers, laughter or stage directions in spoken text. | lint blocks |
| F6 | Speed and pause bounds in the render. | the Pipeline |
| F7 | Any breath or audio sample has a recorded licence. | the Pipeline (breaths are off) |
| F8 | No claim of a check that wasn't run, in commit messages, logs, docs, the PR or the final message. | you |
| F9 | The core ten never appear: "let's dive in", "dive deep", "delve", "in today's episode", "welcome back", "without further ado", "buckle up", "great question", "it's important to note", "it's worth noting". | lint blocks |

## The tells to look for

The phrase list catches the words. These need your judgement too:

- **Openers and closers that fit any Topic:** "Have you ever...", "Imagine a world...", "So, to wrap up...". Start on the fact; end on the thing to try.
- **Bookish vocabulary:** tapestry, pivotal, crucial, landscape, realm, robust, seamless, navigate, foster, leverage. Use the plain word, or cut.
- **"Serves as", "acts as", "stands as":** say "is".
- **Negative parallelism:** "It's not about X, it's about Y." "Not just X, but Y." State the positive claim. A real misconception may get one contrast an Episode.
- **Reflexive threes:** three adjectives, three clauses, three examples, every time. Use the real number; two is fine.
- **Trailing participle verdicts:** "..., highlighting the importance of sleep." Cut the tail, or make it a sentence that says the actual inference.
- **Significance inflation:** "changed everything", "plays a crucial role", "a testament to". Show the size instead.
- **Hedge stacking:** "may potentially suggest it could help". One hedge, at the claim.
- **Meta-talk:** "In this section we'll look at...", "Now let's turn to...". Every signpost says what and why.
- **Summary for its own sake:** a paragraph that ends by restating itself. Keep the planned Recap; cut the rest.
- **Fake enthusiasm:** "Fascinating!", "This is amazing." Let the fact do it; a dry line after a big number lands harder.
- **Uniform rhythm:** sentence after sentence of the same length, every paragraph ending on a takeaway.
- **Repeated paragraph openers:** "So,", "Now,", "Here's", "This". Vary them; "So," opens at most one paragraph an Episode.
- **Generic examples:** "a busy professional named Sarah". Use a sourced case, or give a hypothetical one detail only this Topic has.
- **Grand closers:** "The future looks bright." "Despite these challenges..."
- **Verdict-free balance:** "Ultimately, it depends." Say what you'd do and what would change your mind.
- **Synonym cycling:** "caffeine... the stimulant... the compound". Repeat the noun.
- **Nominalisations:** "the facilitation of memory consolidation". Use verbs: "sleep helps you keep what you learned".
- **Show-notes formatting:** bold-led bullets, emoji, "Key takeaways", title-case headings.

## Soft targets

About ±25% on every number.

1. Each Segment: one sourced surprise, one detail that could only belong to this Topic, one consequence for the listener.
2. The host commits to a view at least once and says once where it's unsure.
3. Sentence lengths spread out; at least one sentence of five words or fewer every 150 words or so.
4. No more than about 4 "X, Y and Z" triples per 1,000 words; "three things" announced at most twice.
5. No paragraph opener used for more than about 15% of paragraphs, and never twice in a row.
6. "Not X. Y." at most once.
7. No lead-in twice in an Episode, across Recall prompts, listener questions and signposts.
8. No six-word run shared with the last ten Bundles in the Hook, Roadmap, signposts, prompts, Sign-off, summary or show-notes opening. Lint warns on these.
9. One or two asides an Episode, each its own sentence, each carrying a fact or a judgement.
10. Zero to two light moments, from the material.
11. Titles in sentence case, one clause, under about 60 characters, no hype ("secret", "shocking", "ultimate", "everything you need to know").

## Self-review

Answer each question about the draft, fix what you find, and keep any warning you decide to keep in `lint_report.yaml` with its reason.

1. Read the Hook cold. Could its first two sentences open an Episode on another Topic? If so, rewrite it around this Topic's fact.
2. Name each Segment's surprising, sourced fact. If you can't, merge or cut the Segment.
3. Where does the host commit to a view, and where does it say it's unsure? If neither appears, add them, labelled as inference where they are.
4. Find every sentence that only announces what's coming or restates what was said, outside the Recap. Cut it or give it content.
5. Is any example generic enough to fit three other Topics? Replace it with a sourced case or give it a Topic-specific detail.
6. Do two Segments share the same internal order? Change one.
7. Read three paragraphs as if aloud. Does any sound like a press release, a textbook or a chatbot? Rewrite it as speech.
8. Is there a joke, pun or "fun fact" frame the material didn't earn? Cut it.
9. Honesty: any invented experience, number, quote or name; any evidence phrase stronger than its ledger tier; any call to action that isn't true?
10. Is each thing called by the same noun throughout?
