# Install private researcher extensions

The public `agents/` directory holds general roles. Put narrow, project-specific source briefs in a
separate private repository under `agents/`. Start from [`templates/specialist.example.md`](../templates/specialist.example.md).
Each private brief declares `extends: researcher` in its source frontmatter. The installer combines the
study's installed public `researcher` brief with the specialist's body into one installed role, so the
retrieval, evidence, and handoff rules are inherited rather than copied and allowed to drift.

## Configure a local source

Clone the private repository **outside this public checkout**. Do not add it as a submodule of this repo:
a private submodule URL would be committed publicly, and outsiders could not fetch it. The local path is
configured per machine in an ignored environment file, or passed as `--source`.

```sh
cp .agent-extensions.env.example .agent-extensions.env
# Edit the local path and corpus setting in .agent-extensions.env.
python3 bin/install-agent-extensions --env-file .agent-extensions.env \
  --target /path/to/private-study --profile honeybee-communications-analyst
```

Set `SCIENTIFIC_RESEARCH_AGENT_CORPUS_REPO` to the repository identifier used in briefs, such as
`owner/research`. Set `SCIENTIFIC_RESEARCH_AGENT_RESEARCH_REPO` to an existing local Git checkout of that
repository. The setting stays in the ignored `.agent-extensions.env`; installed study briefs also contain
the resolved local path so the agent can open its folder. Review generated briefs before publishing a study.
`--research-repo` overrides that path for one invocation. When configured, installation creates
`agent-research/<profile>/README.md` in the research checkout and embeds that profile's absolute research
folder in its installed brief. A profile can read Markdown the person adds there and write new notes there.
Existing notes are never overwritten.

To create folders for every private profile before installing any into a study, run:

```sh
python3 bin/install-agent-extensions --env-file .agent-extensions.env --all --init-research
```

Use `--profile NAME --init-research` to create only one folder. Research notes stay in the selected
research repository; this public package contains neither those notes nor the private path. When the
profile is used directly from its source brief, point it at the same folder convention.

The target must already contain `.claude/agents/researcher.md`, installed by the public scaffold or copied
from this package with its placeholders filled. Repeat `--profile` to install several specialists, or use
`--all` for every source brief. `--name`, `--corpus-repo`, `--model`, `--effort`, and `--agents-ref` override
values in the env file. Model and effort default to the target researcher's values; name defaults to the
target folder name. All placeholders used by a private brief must resolve, or installation fails.

The installer writes `.claude/agents/<specialist>.md` and a bounded routing section in the target's
`AGENTS.md`. That section sits outside `<!-- scaffold:start -->` and `<!-- scaffold:end -->`, so a normal
`scaffold update` leaves it in place. Run the installer again after changing a private source brief or
updating the public researcher brief. It refuses to overwrite a profile file it did not install.

For a new specialist, give the file and frontmatter the same unique kebab-case name, keep
`extends: researcher`, state positive and negative routing boundaries, and separate retrieved evidence
from inference. The source brief is an extension, so it can focus on the specialty while the public
researcher brief supplies shared research rules.

## Publishing checks

Run `python3 -m unittest discover -v tests` for changes to this starter set. Check `git status --short`
and `git ls-files agents disciplines` before committing here. The private checkout path and any unpublished
source brief should never be committed to this public repository. Removing a file from a public branch
does not erase it from that repository's public history; use a new clean public repository if historical
copies must no longer be accessible.
