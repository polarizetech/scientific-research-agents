# Plan: Auditory Evoked Potentials expert profile

## Inventory and placement

Two relevant repositories were found rather than inferred from their names:

- `polarizetech/scientific-research-agents`, this repository, contains eight installable role briefs in
  `agents/`, shared discipline briefs in `disciplines/`, the installer-facing `templates/AGENTS.block.md`,
  and brief validation in `tests/test_agents.py`.
- `polarizetech/audio-evoked-potentials`, at the sibling checkout
  `/Users/joshuaanderton/Sites/audio-evoked-potentials`, contains reusable auditory simulators. Its README
  says that campaigns and results belong to the study that asked the question. It has no `AGENTS.md`,
  `.claude/agents/`, `.agents/`, profile schema, protocol, or preregistration mechanism at its root.
  It points campaign work to `polarizetech/neurophonic-protocol-runner` and its research record is in
  `research/projects/audio-evoked-potentials/`.

The profile will therefore go in this repository as `agents/auditory-evoked-potentials.md`. The existing
`disciplines/auditory-electrophysiology.md` will remain the short shared discipline brief and will point to
the specialist profile for its narrower, evidence-heavy behaviour. This is a deliberate exception to the
current README's “one agent per role, not per discipline” rule: the requested first-priority routing and
specialized answer protocol cannot be expressed by a passive discipline paragraph. The README will document
that narrow exception rather than silently changing the architecture.

Association with the study will be explicit but portable:

- the profile will refer to the AEP project beneath `{{corpus_repo}}`, avoiding a machine-specific path;
- this repository's README will list the profile and link to the public AEP simulator repository;
- `audio-evoked-potentials/README.md` will gain a reciprocal pointer to this profile. That edit is in a
  second repository and will be made only during the approved implementation phase.

No candidate repository will be renamed or moved. No existing profile priority will be changed.

## Existing profile schema and routing

`agents/researcher.md` and `agents/mathematician.md` were read end to end, as were the repository
instructions, coordination protocol, README, template, discipline brief, and tests.

All ordinary briefs use Claude-compatible YAML frontmatter followed by provider-neutral Markdown. The exact
frontmatter mapping for the new file will be:

| Field | Planned value | Purpose |
|---|---|---|
| `name` | `auditory-evoked-potentials` | Must equal the filename stem. |
| `description` | A single line beginning “Use first for…” with positive trigger terms, tie-breaking against general neuroscience, and explicit exclusions | Claude Code's routing metadata; it must not contain `: `. |
| `model` | `{{model}}` | Installer-supplied model, exactly as every ordinary brief uses it. |
| `effort` | `{{effort}}` | Installer-supplied reasoning effort, exactly as every ordinary brief uses it. |

No `priority`, `when_to_consider`, tool, project, or other invented frontmatter field will be added. The
repository has no executable router and no numeric priority schema. “First priority” will be expressed in
the standard `description`, in a visible routing section in the body, in the README roster, and in static
tests. Provider-neutral consumers that read installed briefs through `AGENTS.md` will receive the same rule.

The body will follow existing conventions: direct role instruction, operational sections, the standard
handoff section, only the allowed placeholders, and no organization-specific absolute paths or model
choices.

## Routing boundary

The description and a dedicated **Routing** section will say that this profile wins ties with the general
`researcher`/neuroscience role when the substantive question concerns:

- ABR, MLR, LLR/P1-N1-P2, MMN, P300, ASSR, FFR, or central/binaural-beat responses;
- the external-audio-to-percept pathway, including place, latency, timing, following rate, transformations,
  losses, and newly created components;
- binaural hearing, ITD/ILD, cochlear nonlinearity or DPOAEs;
- audio-stimulus design for a target neural response; or
- auditory-to-other-sense crossover.

It will explicitly decline general audio engineering, music production, speech-to-text, and non-auditory
sensory questions without an auditory crossover. The profile will include these ten examples:

Positive:

1. “What latency is ABR wave V and where is it generated?”
2. “Design a 40 Hz binaural-beat stimulus that produces a cortical ASSR.”
3. “Does a 500 Hz carrier reach cortex as a waveform?”
4. “Where are ITD and ILD computed, and what survives to IC?”
5. “Can a sound reset visual-cortex alpha phase?”

Negative:

1. “Mix this podcast at -16 LUFS.”
2. “Master this song for streaming.”
3. “Transcribe this interview.”
4. “Explain visual steady-state evoked potentials.”
5. “Which microphone should I buy for vocals?”

## Profile contents

The knowledge section will reproduce every supplied grounding-table row and every evidence ID verbatim.
Each row will retain its supplied status. Claims not in that table will be marked `Background` unless they
are retrieved and added with evidence. The response protocol will require a read-depth tag (`abstract`,
`passages`, or `full`) alongside `Established`, `Supported`, `Hypothesis`, `Derived`, or `Background`.

The behavioural sections will require:

1. Ordered tracing through cochlea → auditory nerve → cochlear nucleus → superior olivary complex →
   inferior colliculus → medial geniculate body → A1 → non-primary cortex → cross-modal/association/
   hippocampal systems, stating at each stage what survives, is lost, or is created, plus latency and rate
   limits.
2. Separate treatment of carrier/place, envelope or modulation/following rate, and interaural, temporal,
   and spectral differences.
3. Stimulus-design outputs covering carrier, modulation, calibrated level, binaural configuration, expected
   latency and generator, duration, and safety. Every parameter must be sourced or marked
   `UNVERIFIED`/`PLACEHOLDER`.
4. The Neural Trajectories dissociation rule: compare any encoding claim with a gain-matched square-law
   nonlinearity and a detuned receiver; a generic match is leak/correlation, not encoding.
5. A relevant devil's-advocate line, including the supplied 40 Hz SNR caveat and the mixed evidence for
   binaural-beat entrainment.
6. A tools workflow that uses the configured scientific-research retrieval server first, indexes missing
   papers when available, checks citations before documentation, cross-checks research questions with at
   least one web search, and never recalls a constant. Tool names will be described as capability names
   with the supplied aliases in parentheses, because installed MCP namespaces can differ by client.
7. A limitations section covering adult/normal-hearing and stimulus dependence, animal-derived values,
   near-threshold TMS conditions in cross-modal work, mixed binaural-beat evidence, and the fact that the
   citation checker verifies quotations/numbers rather than entailment.

Before implementation, the supplied evidence will be re-verified with the configured Polarize retrieval
server and the final claim list will be passed through its citation checker. If those MCP tools are not
available in the implementation session, no evidence will be invented: the supplied table will be retained
as supplied, clearly marked as requiring re-verification, and the limitation will be reported.

## Documentation and versioning

Implementation will update:

- `README.md`, adding the specialist profile, its first-priority boundary, and instructions for updating its
  grounding table;
- `disciplines/auditory-electrophysiology.md`, with a short pointer and no duplicated evidence table;
- `audio-evoked-potentials/README.md`, with the reciprocal link described above;
- `VERSION`, `CHANGELOG.md`, and `CITATION.cff` together, as required by this repository. The proposed
  release is `0.5.0`, because this adds a new installable role rather than correcting an existing one.

## Tests

`tests/test_agents.py` will be updated to expect the ninth brief and will gain a focused test that checks:

- exact frontmatter schema and allowed placeholders;
- routing metadata includes ABR/ASSR/FFR/MMN/P300, binaural, cochlear, auditory crossover, explicit
  first-priority/tie-breaking language, and the audio-engineering exclusions;
- all five positive and five negative examples are present;
- the 40 Hz control states a low carrier near 400 Hz and rejects approximately 3 kHz;
- the 500 Hz carrier control states that it does not reach cortex as a copied waveform, distinguishes place
  code from following response, gives the cortical FFR limit of approximately 150 Hz, and contains
  `W3132668373#p35.3485f9f5` and `W2005066437#p29.cde118db`;
- all supplied evidence IDs occur verbatim in the profile;
- ordered pathway stages, status/read-depth labels, dissociation controls, safety, limitations, and the
  standard handoff are present.

Because this repository has no runtime classifier, these will be schema/content contract tests rather than
pretending to execute a router that does not exist. The full suite will run with:

```bash
python3 -m unittest discover -v tests
```

## Git and delivery

After approval, create one `codex/aep-expert-profile` branch in this repository, make the planned changes,
run the test suite, and use a concise imperative commit matching the repository's history, for example
`Add auditory evoked potentials expert profile`. The reciprocal pointer in the separate AEP repository
requires its own commit/PR in Git terms; therefore the literal “one branch, one PR” constraint cannot cover
both repositories. The implementation will keep the substantive profile, tests, docs, and release bump in
one branch/PR here and will report the AEP README pointer as a separate cross-repository commit unless the
user chooses to omit that pointer.

The PR description will summarize routing and tests and include the five required limitations verbatim in
substance.
