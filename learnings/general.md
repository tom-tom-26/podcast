# General lessons

Lessons that hold in every field. Line format and rules: `.claude/skills/episode/references/learnings.md`.

## Lessons

- `2026-10-29 · planning · stage: research` **What happened:** numbers taken from search summaries proved wrong three times in the planning research: Mayer's personalisation effect quoted from the 2005 edition (d about 1.3) instead of the 2014 one (d = 0.79), a positive study (Jing 2016) reported as a mixed replication, and a DOI that led to a different paper. **Do instead:** speak a number only from a full text or an abstract that states it, and open a DOI to check its title before citing it. **Saves:** a correction pass after the Episode is written. `seen: 1` `source: owner`
- `2026-10-29 · planning · stage: research` **What happened:** the Trusted network level blocks journals, news sites and PubMed, so `curl` and WebFetch get `403 host_not_allowed`. **Do instead:** run in the `podcast` environment with Full network access; if fetches to those hosts still return `403 host_not_allowed`, the environment is wrong, so say so at the top of the final message. **Saves:** a whole run of failed fetches. `seen: 1` `source: owner`
