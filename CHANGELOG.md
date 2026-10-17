# Changelog

## v0.5.0 (2026-10-17)

- Adds a first-priority Auditory Evoked Potentials specialist profile with explicit routing boundaries,
  stage-by-stage tracing, stimulus-design and dissociation protocols, a supplied evidence-addressed
  grounding table, safety and interpretation limits, and positive/negative routing controls.
- Documents how to update the AEP grounding table and links the profile to the reusable AEP simulator
  project. The existing auditory-electrophysiology discipline brief now routes narrow AEP work to it.
- Adds first-priority visual-system and bone-conduction expert profiles. The visual profile separates ocular
  optics, phototransduction, retinal coding, ascending pathways and cortical phase; the bone-conduction
  profile centers bilateral/dual-transducer transfer, cross-talk, calibration, leakage and tactile controls.
  Both start with web-abstract source seeds clearly marked for replacement by RAG evidence.
- Makes the `polarizetech/retrieval-augmented-generation` MCP the first search path for every request handled
  by the lead or any specialist, with only service-unavailable and explicit user opt-out exceptions. Local
  checkout inspection remains authoritative for current repository contents.
- Standardizes design and small-app delivery around the configured design system—
  `polarizetech/polarize-ui` in Polarize installations—and a zero-build browser app served by Python
  `serve.py`. Designer, frontend developer, and computational engineer briefs now share the same component,
  server, API-ownership, and exception rules.

## v0.4.0 (2026-10-15)

- The `designer` brief gains an *Originality* section (never copy another organisation's layout, buttons,
  type treatment or palette; treat a named reference as a negative reference; differ on every identifying
  axis; record provenance) and an *Audit mode* (inventory, compare, redesign, report).

## v0.3.0 (2026-10-11)

- Adds `templates/local-models/model-roles.example.json`: named roles for local models served by Ollama (a
  research model, a fast default, a slow reasoning one, an embedding model), in the fields Open WebUI's
  workspace models take. The coordination protocol's section on local models points to it. Nothing installs
  it; it is a file to copy.

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
