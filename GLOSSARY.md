# Glossary

**Episode**: One finished, listenable piece of audio on a single topic, about 25 minutes by default (see Variant).

**Topic**: The subject the owner names when summoning the skill.

**Skill**: The Claude session entry point. Takes a topic, produces a Bundle.

**Bundle**: The finished input to the tool for one Episode: Script, metadata, and sources.

**Script**: The spoken text of an Episode, written in the host's voice.

**Show notes**: The human-readable summary and source list shown with an Episode.

**Pipeline**: The automated process that turns a Bundle into published audio and an updated Feed.

**Feed**: The podcast RSS feed that Apple Podcasts subscribes to.

**Cover**: The show's one square artwork, used by the Feed for the show and every Episode. Drawn as code in `artwork/`; there is no per-Episode art.

**Host**: The voice presenting the Episode.

**Claim ledger**: The compact record built while researching: one line per claim with its source and evidence tier. Doubles as the Episode's source list.

**Learnings**: Lessons from past runs: a mistake or difficulty the Skill hit and what to do instead, so later Episodes avoid it and spend fewer tokens. Never facts about a topic. Kept per field alongside its Source profile (ticket 10).

**Q&A episode**: An Episode that goes deeper on one or more of the owner's questions about an existing published Episode, its parent. Made by the Skill's Q&A mode and published in the same Feed as `Episode 7q` (ticket 11).

**Listener profile**: The short file (`config/listener_profile.md`) recording the owner's taste, as shown by their Q&A questions and their feedback on Episodes: how much detail they want, where their curiosity goes, and how Episodes land. Read by every run; any default change it suggests needs the owner's OK (tickets 11 and 16).

**Read depth**: How much of a source the Skill actually read for a Claim ledger line: `full text`, `abstract`, or `secondary` (any summary, including a WebFetch result or a search snippet). A number spoken in a Script needs a full text, or an abstract that states it (ticket 06).

**Confirm message**: The Skill's one message before it starts work, with the Variant, outline, voice, and any drill-down options or Part split. The owner answers it in one reply, "go" or a tweak, and is asked nothing else.

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

**Release**: The GitHub Release holding one Episode's audio for good, tagged with its Episode id. Audio lives here, never in git.

**guid**: The Feed's permanent identifier for an Episode, made once at publish time. It never changes, even when the Episode is re-rendered, so podcast apps treat it as the same Episode.

**Episode registry**: The committed list of published Episodes: number, Episode id, Bundle id, guid, voice, file size and duration. The Pipeline is the only writer.

**Window**: The Episodes whose audio the Pages site holds, newest first, within the size budget. The Feed lists only these (unless the Repoint switch is on); the Archive page lists every Episode.

**Site rules**: `config/site.yaml`: the Window's soft budget (about 600 MB of audio), the firm ceiling on the whole site (about 900 MB, over it the deploy is refused), and the Repoint switch.

**Repoint switch**: The Site rules' `repoint` setting. Off, an Episode that leaves the Window leaves the Feed; on, it stays in the Feed with its enclosure on the stable Release download URL. Off until the real-device test shows Apple Podcasts follows that URL (ticket 08).

**Test feed**: `test/feed.xml` on the Pages site, built from the hand-written test registry (`config/test_episodes.yaml`) with its own guids and titles starting `TEST`. For the real-device checks, never for listening. A test entry with `enclosure: release` points at its Release download URL.

**Archive page**: The plain `noindex` page listing every published Episode, newest first, with a download link to its Release. The Feed's `link` points here and nothing else links to it.

**Show config**: `config/show.yaml`, the Feed's channel fields and description.

**Voice roster**: `config/voices.yaml`, each voice's engine and settings, and the credit line a CC BY voice needs. It also names the default voice (`bm_george`), the stretch floor, and each voice's `suits:` hints, the few words the Skill weighs when it proposes a voice.

**Stretch**: A Pocket voice's WSOLA time-stretch, which sets its pace since Pocket has no speed control. Below 1 is slower. A Pocket voice with no stretch is read at Pocket's own pace. The **stretch floor** (about 0.85, soft) is the slowest stretch that still sounded right in the audition.

**Voice seed**: A Pocket voice's roster seed, mixed with the Bundle id into each chunk's seed. Changing it gives every Episode in that voice a different take.

**Lexicon**: `config/lexicon.yaml`, how each engine should say the terms it gets wrong, plus the `verified:` capitals words every roster voice reads right as written. A Bundle's `pronunciations` use the same entry shape and win for that Episode (research/14).

**Chunk**: One stretch of a Script sent to the TTS engine in a single call. A chunk never crosses a paragraph, `[beat]`, `[think]` or Segment heading.

**Pacing config**: `config/pacing.yaml`, how render cuts a Script into chunks and spaces them: the chunk cap, the gap drawn at each kind of boundary, the `[beat]` and `[think]` lengths, speed jitter and trim. Draws are seeded by the Bundle id.

**Chunk map**: The file render writes beside its WAV, naming the voice and each chunk's Segment, text, speed (a Kokoro speed or a Pocket stretch), Pocket seed and place in the WAV, so a later stage can name a chunk or re-render it.

**Gate**: One of publish's firm checks on the encoded Episode, decoded again: the ASR round trip, silence, loudness, true peak and format (research/15). A fail stops the run before the Release; an ASR fail first re-renders the chunk it names, once.

**Failure issue**: The one GitHub issue a failed publish-episode or deploy-site run opens, labelled `pipeline-failure` and assigned to the owner: the stage that failed, the Bundle and the last log lines. A run that succeeds opens nothing.

**ASR report**: `asr_report.yaml`, a Release asset beside the audio, recording for each capitals word and Lexicon term in the Script whether the ASR round trip heard it as written. Weak evidence the Skill weighs before proposing a `verified:` addition.

**Feedback mode**: The Skill mode in which the owner gives free-text reactions or instructions about published Episodes; the Skill routes each one to where it changes future Episodes, or to a Correction (ticket 16).

**Correction**: A fix to a published Episode's content, graded Harmful, Material or Minor. Harmful and Material re-render the Episode under the same guid; every Correction leaves a dated line in the Show notes (ticket 16).

**Topic backlog**: The owner's list of topics for later Episodes (`config/backlog.md`). Only the owner adds to it, by hand or through the Skill; summoning with "next" takes the top line. The Skill never suggests topics on its own.

**Phrase list**: The versioned de-slop list in `config/deslop_rules.yaml`: the core ten phrases that block a Bundle (F9), and the rest, which only warn. Feedback mode may add to it; a Bundle records the `deslop_version` it was written against.

**Pin list**: `pinned.txt`, one Episode id per line, kept in the Window whatever their age and counted against its budget. "Bring back episode X" adds a line (ticket 08).

**Template tunables**: `config/template.yaml`, the Episode template's numbers the owner can change by instruction: Variant ranges, typical Standard length, the wpm budget and the like, versioned by `style_guide_version`.

**Owner-instructed**: A Feedback-mode commit that carries out an instruction the owner gave, marked by a trailer line quoting the owner's words, `Owner-instructed: "make them shorter"`. Only such a commit may auto-merge a change to the Template tunables or the Voice roster.

**Auto-merge**: The workflow that merges a Skill's `claude/` branch PR when every changed path is allowed and lint finds no firm failure, then dispatches the workflow the change needs. Anything else stays open, labelled `needs-owner`.
