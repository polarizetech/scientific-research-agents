# Changelog

## v0.10.0 (2026-10-28)

- Retrieval first, for every question: the rule in `AGENTS.md`, `COORDINATION.md` and the block template now
  covers every question or task in any assistant, including questions about the repository's own code
  (retrieve, then inspect the checkout), instead of applying only before a search. The retrieval tool also
  picks the specialist: the lead calls `pipeline__profile_route` and brings in only the research roles and
  specialist it returns. Building roles are still chosen by the kind of task.

## v0.9.0 (2026-10-22)

- Adds an optional local research checkout setting for private profiles. Each profile receives its own
  `agent-research/<profile>/` Markdown folder, and installed briefs point to it. Folders can be initialized
  without installing a profile into a study; existing notes are preserved.

## v0.8.0 (2026-10-21)

- Narrows the public package to reusable starter roles and adds a specialist brief template and a guide
  for keeping personal profiles in a separate private repository.
- Adds an opt-in, environment-configured installer for private specialist briefs that extend the public
  researcher role and route from a study's `AGENTS.md` outside the scaffold-managed block.
- Removes organisation-specific design-system examples from the starter roles and app architecture guide.

## v0.7.0 (2026-10-19)

- Adds an `ios-developer` role: thin native SwiftUI + `WKWebView` shells around a web app that already works
  in a browser, before any rewrite. The brief covers the narrow JavaScript-to-native bridge, background audio
  (`UIBackgroundModes`, an `.playback` audio session, interruptions) and the rendered-file fallback when live
  Web Audio can't survive the lock screen, plus simulator and personal-device builds. Background behaviour
  counts as verified only on a physical device with the screen locked.

## v0.6.0 (2026-10-18)

- Adds hypothesis-impact ownership to the shared coordination protocol. The agent changing evidence, a finding,
  or scientific implementation propagates it through the corpus reverse index and runs the scaffold's
  hypothesis synchronization in affected studies.
- Researcher, analyst and computational-engineer briefs now carry their specific parts of that workflow.
  Routine synchronization uses a study's standing impact policy; hypothesis meaning and unrecorded scientific
  choices still return to the person.

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
