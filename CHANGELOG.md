# Changelog

## v0.2.0 (2026-10-01)

- Adds repository-level `AGENTS.md` instructions with `CLAUDE.md` as an import adapter, describes the role
  briefs as provider-neutral Markdown with Claude frontmatter, and lets ChatGPT/Codex apply a role in the
  current session when subagents are unavailable or not authorized.

## v0.1.2 (2026-10-01)

- The coordination protocol points at the kit's scope protocol, part of `prereg` since kit 0.6.0 (`tool-scope`
  is retired), and says a tool's override experiments are preregistered in the research corpus.

## v0.1.1 (2026-09-30)

- Briefs follow the scaffold's work types: a dataset is referenced in `datasets/<slug>/DATASET.toml`, and
  preregistrations live in the unit they test (`<unit>/preregistrations/<EID>/`).
- Briefs cite protocol sections by name, not number, so renumbering can't break them.

## v0.1.0 (2026-09-30)

First release, split out of scientific-research-scaffold.

- Eight agent briefs: scout, computational-engineer, mathematician, designer, frontend-developer,
  researcher, analyst, science-writer, each with a starting model and effort.
- The coordination protocol, discipline briefs for neuroscience, cardiology, auditory electrophysiology and
  bioelectricity, and the language-routing reference.
- The `AGENTS.md` section template for Codex and other assistants.
- `bin/agents usage`: tokens and API-equivalent cost per repo from Claude Code and Codex logs.
