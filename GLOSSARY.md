# Glossary

**Episode**: One finished, listenable piece of audio on a single topic, about 25 minutes by default (see Variant).

**Topic**: The subject the owner names when summoning the skill.

**Skill**: The Claude session entry point. Takes a topic, produces a Bundle.

**Bundle**: The finished input to the tool for one Episode: Script, metadata, and sources.

**Script**: The spoken text of an Episode, written in the host's voice.

**Show notes**: The human-readable summary and source list shown with an Episode.

**Pipeline**: The automated process that turns a Bundle into published audio and an updated Feed.

**Feed**: The podcast RSS feed that Apple Podcasts subscribes to.

**Host**: The voice presenting the Episode.

**Claim ledger**: The compact record built while researching: one line per claim with its source and evidence tier. Doubles as the Episode's source list.

**Learnings**: Lessons from past runs: a mistake or difficulty the Skill hit and what to do instead, so later Episodes avoid it and spend fewer tokens. Never facts about a topic. Kept per field alongside its Source profile (ticket 10).

**Q&A episode**: An Episode that goes deeper on one or more of the owner's questions about an existing published Episode, its parent. Made by the Skill's Q&A mode and published in the same Feed as `Episode 7q` (ticket 11).

**Listener profile**: The short file (`config/listener_profile.md`) recording the owner's taste, as shown by their Q&A questions and their feedback on Episodes: how much detail they want, where their curiosity goes, and how Episodes land. Read by every run; any default change it suggests needs the owner's OK (tickets 11 and 16).

**Variant**: The length format of an Episode, proposed by the Skill and confirmed by the owner: Quick (8-15 min), Standard (15-28 min, default, typically ~25) or Deep (28-35 min). Ranges are ceilings; there is no minimum.

**Segment**: A titled section of a Script: Hook, Roadmap, a content segment, the closing segment (Protocol, or Why it matters / what to watch), Recap, Sign-off.

**Hook**: The opening of an Episode (first ~45 s) that earns attention and states the promise.

**Recall prompt**: A segment's main question, asked at its start with an invitation to guess, and re-asked with its answer at the end.

**Part**: One of 2-3 Episodes made from a topic that would run over ~35 minutes and splits into standalone subtopics. Each Part stands alone; none ends on a cliffhanger.

**Claim tag**: A non-spoken marker in the Script linking a sentence to its Claim ledger line.

**Spoken form**: Text written exactly as it should be said: numbers, units and symbols as words.

**Higher-risk flag**: The Bundle marker, with a reason, for topics whose content could cause harm if misapplied.

**Source profile**: For one field of topics, what counts as strong evidence, what to watch for, and what triggers the Higher-risk flag. Starter set in research/05 section 13; new ones are saved to Learnings.

**Bundle id**: The name of a Bundle's folder, `<date>-<slug>`, fixed when the Skill writes it. Seeds the render's random pauses, so a re-render sounds the same.

**Episode id**: The published name of an Episode, `ep-007-<slug>` (Parts `ep-004a-...`), given by the Pipeline at publish time in publish order. Used for the Release tag and file name.

**Episode registry**: The committed list of published Episodes: number, Episode id, Bundle id, guid, voice, file size and duration. The Pipeline is the only writer.

**Feedback mode**: The Skill mode in which the owner gives free-text reactions or instructions about published Episodes; the Skill routes each one to where it changes future Episodes, or to a Correction (ticket 16).

**Correction**: A fix to a published Episode's content, graded Harmful, Material or Minor. Harmful and Material re-render the Episode under the same guid; every Correction leaves a dated line in the Show notes (ticket 16).

**Topic backlog**: The owner's list of topics for later Episodes (`config/backlog.md`). Only the owner adds to it, by hand or through the Skill; summoning with "next" takes the top line. The Skill never suggests topics on its own.
