# scientific-research-agents

Specialist AI agents for scientific research repositories, and the protocol they coordinate by: who
does what, how they hand work to each other, which model each starts on, and what it all costs.

It is used by [scientific-research-scaffold](https://github.com/polarizetech/scientific-research-scaffold),
which installs these agents into every study, sim and tool it makes and keeps them current, but nothing
here depends on the scaffold.

## The agents

Each file in [`agents/`](agents/) is a Claude Code subagent brief, with `{{placeholders}}` the installer
fills from the repo and its profile. Codex and other assistants read the same briefs through a section of
`AGENTS.md` ([`templates/AGENTS.block.md`](templates/AGENTS.block.md)).

| agent | takes | starts on |
|---|---|---|
| `scout` | finding and summarising, read-only, so other agents don't read everything themselves | haiku, low |
| `computational-engineer` | simulators, models, numerical code, pipelines; language choice, typing, reuse vs duplication | sonnet, high |
| `mathematician` | equations, constants, units and valid ranges; specifies calculators with reference values | sonnet, high |
| `designer` | layout and visual design on the design system; how to show a dataset | sonnet, medium |
| `frontend-developer` | React and shadcn/ui interfaces built from the designer's mockups | sonnet, medium |
| `researcher` | literature and evidence, evidence tiers, claims in the research corpus | sonnet, medium |
| `analyst` | data analysis and statistics, preregistered analysis plans | sonnet, high |
| `science-writer` | papers, and blog posts as a separate register | sonnet, medium |

**One agent per role, not per discipline.** Research, analysis and writing are different jobs; neuroscience
and cardiology mostly are not. The science roles read discipline briefs from [`disciplines/`](disciplines/):
what is established in each field, its standards and its traps.

**The science stays the person's.** Infrastructure is the agent's to decide; equations, parameters and
interpretations come from the person and the research. No agent states a published value from memory.

## How they coordinate

[`COORDINATION.md`](COORDINATION.md): one lead delegates; agents pass handoffs of at most 150 words, never
transcripts; parallel work only for independent tasks; a scientific feature goes researcher, then the
person's decision, then engineer; each agent starts on a cheap model and the lead escalates a task on a
clear signal.

[`references/language-routing.md`](references/language-routing.md) is the evidence behind the engineer's
rule for choosing a language.

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
