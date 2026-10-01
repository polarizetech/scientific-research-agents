# scientific-research-agents

The specialist role briefs (`agents/`), the coordination protocol (`COORDINATION.md`), discipline briefs
(`disciplines/`), and `bin/agents` (usage and cost).

**This repo is read and forked by people outside the organisation that wrote it.** Keep it generic: an
organisation's choices (which disciplines, which models, code conventions, its design system) come in as
placeholders filled by the installer from that organisation's profile, never written into a brief.

- `bin/agents` is stdlib only and runs on Python 3.9+.
- Briefs use `{{placeholders}}`: `name`, `corpus_repo`, `design_system`, `conventions`, `model`, `effort`,
  `agents_ref`. An installer must fill every one; `tests/` lists the allowed set.
- A brief's frontmatter `description` never contains ": " (it breaks YAML).
- Claude-specific frontmatter is an adapter for `.claude/agents/`; the Markdown body must remain usable as
  a provider-neutral role brief when another assistant reads it through `AGENTS.md`.
- A claim in a discipline brief that wasn't verified in a session is marked [BK].
- Bump `VERSION`, `CHANGELOG.md` and `CITATION.cff` together; the scaffold pins a tag.

Tests: `python3 -m unittest discover -v tests`
