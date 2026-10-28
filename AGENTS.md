# scientific-research-agents

The specialist role briefs (`agents/`), the coordination protocol (`COORDINATION.md`), discipline briefs
(`disciplines/`), and `bin/agents` (usage and cost).

## Retrieval first, for every question

Every question or task handled by the lead or any specialist agent, in any assistant (Claude, Codex or
another), starts with the configured Scientific Research RAG MCP backed by
[`polarizetech/retrieval-augmented-generation`](https://github.com/polarizetech/retrieval-augmented-generation)
before answering and before any literature, web, corpus, or other search. Client namespaces may expose it as
`scientific_research_rag` or `research-rag`. Ground answers in the passages it returns rather than memory or
an ungrounded search summary. A reply that only approves or answers the agent's own question continues the
earlier request.

The only exceptions are when the RAG service is unavailable or the user explicitly says not to use it for
the request or session. If it is unavailable, say so before using another search method. A question about a
repository's own code is no exception: retrieve first, then inspect the checkout directly, because local
filesystem inspection remains the source of truth for its current code and files, and say when no passage
applies. Do not index private or user-supplied material into a shared corpus without authorization.

**The tool picks the specialist.** Before bringing in a research role or specialist, call the tool's
`pipeline__profile_route` with the question, and use only the research roles and the specialist it
returns, following its guidance. When it names no specialist, the lead answers without one. Building roles
are chosen by the kind of task, and the user can always name a role.

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
- The retrieval-first rule is inherited by every installed agent and is not repeated in each brief.
- Bump `VERSION`, `CHANGELOG.md` and `CITATION.cff` together; the scaffold pins a tag.

Tests: `python3 -m unittest discover -v tests`
