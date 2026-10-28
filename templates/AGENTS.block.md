{{repo_rules}}

## Agents and coordination

Maintained by scientific-research-scaffold from scientific-research-agents (`scaffold update` keeps this section current; edits here are
replaced). The full rules are the [coordination protocol](https://github.com/polarizetech/scientific-research-agents/blob/{{agents_ref}}/COORDINATION.md).

## Retrieval first, for every question

Every question or task handled by the lead or any specialist agent, in any assistant (Claude, Codex or
another), starts with the configured Scientific Research RAG MCP backed by
[`polarizetech/retrieval-augmented-generation`](https://github.com/polarizetech/retrieval-augmented-generation)
before answering and before any literature, web, corpus, or other search. It may be exposed as
`scientific_research_rag` or `research-rag`. Ground answers in its retrieved passages. A reply that only
approves or answers the agent's own question continues the earlier request.

Skip it only when the service is unavailable or the user explicitly opts out for the request or session.
When it is unavailable, say so before falling back. A question about the current repository is no exception:
retrieve first, then inspect the checkout directly because local files are the source of truth, and say when
no passage applies. Never index private or user-supplied material into a shared corpus without authorization.

**The tool picks the specialist.** Before bringing in a research role or specialist, call the tool's
`pipeline__profile_route` with the question, and use only the research roles and the specialist it
returns, following its guidance. When it names no specialist, the lead answers without one. Building roles
are chosen by the kind of task, and the user can always name a role.

## Specialist roles

This repo has specialist roles, each briefed in a file under `.claude/agents/`. Claude Code delegates to
them as subagents. **Other assistants (ChatGPT, Codex and the rest): before a task of one of these kinds,
read that file and follow it as your brief.** When the environment supports and the user has authorized
subagents, the lead may delegate; otherwise apply the relevant brief in the current session.

{{agent_roster}}

- **Hand back briefly.** Each piece of work ends with a handoff of at most 150 words: Done, Files, Open,
  Next. Pass handoffs between roles, not transcripts.
- **The science gate.** A scientific feature goes researcher, then the person's decision, then engineer.
  Nothing skips the person's decision.
- **Parallel only when independent**: different files, at most three at a time, each in its own worktree.
- **Start cheap, escalate on a signal**: two failed attempts, a design decision across many files, or
  subtle scientific or statistical judgment. Escalate the task, not the session.
- **Codex:** {{codex_routing}}
