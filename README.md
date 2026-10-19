# scientific-research-agents

Specialist AI agents for scientific research repositories, and the protocol they coordinate by: who
does what, how they hand work to each other, which model each starts on, and what it all costs.

All leads and specialist agents search through the configured Scientific Research RAG MCP first, backed by
[`polarizetech/retrieval-augmented-generation`](https://github.com/polarizetech/retrieval-augmented-generation),
unless it is unavailable or the user explicitly opts out. They disclose an unavailable service before using
another search method. For a repository's own current code, the checkout remains authoritative and is
inspected directly after the RAG-first step.

It is used by [scientific-research-scaffold](https://github.com/polarizetech/scientific-research-scaffold),
which installs these agents into every study, sim and tool it makes and keeps them current, but nothing
here depends on the scaffold.

## The agents

Each file in [`agents/`](agents/) is a provider-neutral role brief with Claude Code subagent frontmatter;
`{{placeholders}}` are filled by the installer from the repo and its profile. Claude discovers installed
copies in `.claude/agents/`. ChatGPT, Codex and other repository-aware assistants read the same Markdown
bodies through a section of `AGENTS.md` ([`templates/AGENTS.block.md`](templates/AGENTS.block.md)). If the
environment cannot or must not create a subagent, the lead applies the relevant brief in its current session.

| agent | takes | starts on |
|---|---|---|
| `scout` | finding and summarising, read-only, so other agents don't read everything themselves | haiku, low |
| `computational-engineer` | simulators, models, numerical code, pipelines; language choice, typing, reuse vs duplication | sonnet, high |
| `mathematician` | equations, constants, units and valid ranges; specifies calculators with reference values | sonnet, high |
| `designer` | layout and visual design on the configured component library; how to show a dataset | sonnet, medium |
| `frontend-developer` | zero-build, Python-served apps by default; React when justified, always from the configured design system | sonnet, medium |
| `ios-developer` | native SwiftUI + WKWebView shells around an existing web app; bridge, background audio, simulator and device builds | sonnet, medium |
| `researcher` | literature and evidence, evidence tiers, claims in the research corpus | sonnet, medium |
| `analyst` | data analysis and statistics, preregistered analysis plans | sonnet, high |
| `science-writer` | papers, and blog posts as a separate register | sonnet, medium |
| `auditory-evoked-potentials` | first-priority AEP and exteroceptive-audio pathway research, including ABR, ASSR, FFR, MMN, binaural hearing, neurophonic potentials and neural stimulus design | profile-selected |
| `visual-evoked-potentials` | first-priority ocular-optics, retinal-transduction and visual-pathway research, including ERG, VEP, SSVEP, phase and visual stimulus design | profile-selected |
| `bone-conduction-auditory` | first-priority bilateral bone-conduction delivery, cross-talk, placement, calibration, leakage and device-route research | profile-selected |

**One agent per role, not per discipline.** Research, analysis and writing are different jobs; neuroscience
and cardiology mostly are not. The science roles read discipline briefs from [`disciplines/`](disciplines/):
what is established in each field, its standards and its traps.

Three narrowly scoped sensory-system experts are exceptions:
[`auditory-evoked-potentials`](agents/auditory-evoked-potentials.md),
[`visual-evoked-potentials`](agents/visual-evoked-potentials.md), and
[`bone-conduction-auditory`](agents/bone-conduction-auditory.md). Their pathway tracing and stimulus design
require shared, evidence-addressed knowledge contracts across research, analysis, and simulation work. Each
wins routing ties only for its stated scope and carries explicit negative boundaries. The auditory profile
is associated with the
[`audio-evoked-potentials`](https://github.com/polarizetech/audio-evoked-potentials) simulator project and
the AEP study beneath the configured research corpus.

### Updating specialist grounding

Retrieve the affected passages through the configured scientific-research RAG server, preserve evidence
IDs verbatim, and run its citation checker over the final claim list. The checker validates quotations and
numbers, not entailment, so review the inference yourself. Every row keeps a status and read depth; a new or
unverified claim is `Background` until retrieved. The visual and bone-conduction profiles currently include
web-abstract source seeds because the RAG server was unavailable at creation; replace those seeds with RAG
evidence IDs after retrieval. Update the focused contract tests in `tests/test_agents.py` whenever an
evidence ID, source seed, or required routing example changes.

**The science stays the person's.** Infrastructure is the agent's to decide; equations, parameters and
interpretations come from the person and the research. No agent states a published value from memory.

## How they coordinate

[`COORDINATION.md`](COORDINATION.md): one lead delegates; agents pass handoffs of at most 150 words, never
transcripts; parallel work only for independent tasks; a scientific feature goes researcher, then the
person's decision, then engineer; each agent starts on a cheap model and the lead escalates a task on a
clear signal.

[`references/language-routing.md`](references/language-routing.md) is the evidence behind the engineer's
rule for choosing a language.

[`references/app-architecture.md`](references/app-architecture.md) standardizes interfaces: the configured
design system (Polarize installations use `polarizetech/polarize-ui`), a zero-build browser app and Python
`serve.py` by default, allow-listed shared assets, and an explicit handoff to the computational engineer for
non-trivial APIs.

## What it costs

```bash
bin/agents usage ~/code/*          # tokens and API-equivalent cost per repo, last 7 days
bin/agents usage --all --days 30   # every project with sessions
```

`usage` reads Claude Code's and Codex's local logs, counts each API response once (Claude Code writes one
response as several transcript lines), prices it at [`prices.json`](prices.json), and projects a month. For
Codex it also shows the plan's rate-limit windows. On a subscription the dollar figure is scale, not a bill.

Requirements: Python 3.9+. No other dependencies.

## Licence

Code is MIT; the agent briefs, protocol and documentation are CC BY 4.0. See [`LICENSE`](LICENSE).
