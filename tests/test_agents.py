# SPDX-License-Identifier: MIT
"""The briefs are valid subagents with only known placeholders; usage counts each response once."""
import datetime as dt
import importlib.machinery
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_loader = importlib.machinery.SourceFileLoader("agents", str(ROOT / "bin" / "agents"))
_spec = importlib.util.spec_from_loader("agents", _loader)
agents = importlib.util.module_from_spec(_spec)
_loader.exec_module(agents)

PLACEHOLDERS = {"name", "corpus_repo", "design_system", "conventions", "model", "effort", "agents_ref"}
BLOCK_PLACEHOLDERS = {"agents_ref", "repo_rules", "agent_roster", "codex_routing"}


def frontmatter(path):
    head = path.read_text().split("---\n")[1]
    return dict(line.split(": ", 1) for line in head.strip().splitlines())


class Briefs(unittest.TestCase):
    def test_repo_instructions_are_shared_without_dropping_claude(self):
        self.assertEqual((ROOT / "CLAUDE.md").read_text(), "@AGENTS.md\n")
        instructions = (ROOT / "AGENTS.md").read_text()
        self.assertIn("provider-neutral role brief", instructions)
        self.assertIn("Python 3.9+", instructions)

    def test_every_agent_inherits_retrieval_before_search(self):
        expected = (
            "polarizetech/retrieval-augmented-generation",
            "before any literature, web, corpus, or other search",
            "service is unavailable",
            "user explicitly",
            "Local filesystem" ,
        )
        instructions = (ROOT / "AGENTS.md").read_text()
        for phrase in expected:
            self.assertIn(phrase, instructions)

        template = (ROOT / "templates" / "AGENTS.block.md").read_text()
        coordination = (ROOT / "COORDINATION.md").read_text()
        for text in (template, coordination):
            self.assertIn("polarizetech/retrieval-augmented-generation", text)
            self.assertIn("scientific_research_rag", text)
            self.assertIn("research-rag", text)
            self.assertIn("unavailable", text)
            self.assertIn("explicitly opts out", text)
            self.assertIn("checkout", text)
            self.assertIn("without authorization", text)

    def test_interface_profiles_share_design_and_app_architecture(self):
        designer = (ROOT / "agents" / "designer.md").read_text()
        frontend = (ROOT / "agents" / "frontend-developer.md").read_text()
        reference = (ROOT / "references" / "app-architecture.md").read_text()

        for text in (designer, frontend, reference):
            self.assertIn("{{design_system}}", text)
        for text in (designer, frontend):
            self.assertIn("app-architecture.md", text)

        for text in (designer, frontend, reference):
            self.assertIn("pinned release", text)
            self.assertIn("design-system", text)

        for text in (frontend, reference):
            self.assertIn("serve.py", text)
            self.assertIn("ThreadingHTTPServer", text)
            self.assertIn("index.html", text)
            self.assertIn("app.js", text)
            self.assertIn("app.css", text)
            self.assertIn("/api/", text)

        self.assertIn("allow-list", frontend)
        self.assertIn("never mount", frontend)
        self.assertIn("FastAPI", frontend)
        self.assertIn("Record that reason", reference)

    def test_every_brief_is_a_valid_subagent(self):
        briefs = sorted((ROOT / "agents").glob("*.md"))
        self.assertEqual({f.stem for f in briefs}, {"scout", "computational-engineer", "mathematician",
                          "designer", "frontend-developer", "ios-developer", "researcher", "analyst",
                          "science-writer"})
        for f in briefs:
            fields = frontmatter(f)
            self.assertEqual(fields["name"], f.stem)
            self.assertNotIn(": ", fields["description"], f"{f.name}: ': ' breaks YAML frontmatter")
            self.assertEqual((fields["model"], fields["effort"]), ("{{model}}", "{{effort}}"), f.name)
            self.assertIn("Handing back" if f.stem != "scout" else "What you hand back", f.read_text())

    def test_only_known_placeholders(self):
        for f in (ROOT / "agents").glob("*.md"):
            self.assertLessEqual(set(re.findall(r"\{\{(\w+)\}\}", f.read_text())), PLACEHOLDERS, f.name)
        block = (ROOT / "templates" / "AGENTS.block.md").read_text()
        self.assertLessEqual(set(re.findall(r"\{\{(\w+)\}\}", block)), BLOCK_PLACEHOLDERS)

    def test_local_model_roles_template(self):
        roles = json.loads((ROOT / "templates" / "local-models" / "model-roles.example.json").read_text())
        ids = [m["id"] for m in roles["models"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn(roles["default_model_id"], ids)
        self.assertLessEqual(set(roles["pinned_model_ids"]), set(ids))
        for m in roles["models"]:
            self.assertTrue(m["base_model_id"] and m["name"] and m["description"], m["id"])
            self.assertIn(m["base_model_id"], roles["hide_base_ids"])  # only the named roles show

    def test_version_agrees(self):
        version = (ROOT / "VERSION").read_text().strip()
        self.assertIn(f"version: {version}\n", (ROOT / "CITATION.cff").read_text())
        self.assertEqual(re.search(r"^## v(\S+)", (ROOT / "CHANGELOG.md").read_text(), re.M).group(1), version)

    def test_prices(self):
        table = json.loads((ROOT / "prices.json").read_text())
        for m in table["models"]:
            self.assertEqual(set(m), {"id", "input", "output", "cache_read"}, m)


class Extensions(unittest.TestCase):
    def test_private_extension_inherits_researcher_and_routes_outside_scaffold_block(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "private"
            (source / "agents").mkdir(parents=True)
            (source / "agents" / "bee.md").write_text(
                "---\nname: bee\ndescription: Use first for bee evidence in {{name}}.\n"
                "extends: researcher\nmodel: {{model}}\neffort: {{effort}}\n---\n\n"
                "Find bee evidence in {{corpus_repo}} at {{agents_ref}}.\n")
            target = root / "study"
            (target / ".claude/agents").mkdir(parents=True)
            (target / ".claude/agents/researcher.md").write_text(
                "---\nname: researcher\ndescription: General research.\nmodel: sonnet\n"
                "effort: medium\n---\n\nVerify evidence first.\n")
            managed = "<!-- scaffold:start -->\nPublic roles\n<!-- scaffold:end -->\n"
            (target / "AGENTS.md").write_text(managed)
            env_file = root / "private.env"
            env_file.write_text("SCIENTIFIC_RESEARCH_AGENT_EXTENSIONS={}\n"
                                "SCIENTIFIC_RESEARCH_AGENT_CORPUS_REPO=org/research\n"
                                "SCIENTIFIC_RESEARCH_AGENT_AGENTS_REF=v0.8.0\n".format(source))
            command = ["python3", str(ROOT / "bin/install-agent-extensions"), "--env-file", str(env_file),
                       "--target", str(target), "--profile", "bee"]
            for _ in range(2):
                result = subprocess.run(command, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
            installed = (target / ".claude/agents/bee.md").read_text()
            self.assertIn("Verify evidence first.", installed)
            self.assertIn("Find bee evidence in org/research at v0.8.0.", installed)
            self.assertNotIn("extends: researcher", installed.split("---", 2)[1])
            routing = (target / "AGENTS.md").read_text()
            self.assertIn(managed, routing)
            self.assertEqual(routing.count("<!-- scientific-research-agent-extensions:start -->"), 1)
            self.assertIn("`.claude/agents/bee.md`", routing)

    def test_profile_research_folders_are_created_and_existing_notes_are_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "private"
            (source / "agents").mkdir(parents=True)
            (source / "agents" / "translator.md").write_text(
                "---\nname: translator\ndescription: Translate sources in {{name}}.\n"
                "extends: researcher\nmodel: {{model}}\neffort: {{effort}}\n---\n\n"
                "Use {{corpus_repo}}.\n")
            research = root / "research"
            (research / ".git").mkdir(parents=True)
            folder = research / "agent-research" / "translator"
            folder.mkdir(parents=True)
            (folder / "user-note.md").write_text("My research\n")
            env_file = root / "private.env"
            env_file.write_text("SCIENTIFIC_RESEARCH_AGENT_EXTENSIONS={}\n"
                                "SCIENTIFIC_RESEARCH_AGENT_CORPUS_REPO=org/research\n"
                                "SCIENTIFIC_RESEARCH_AGENT_RESEARCH_REPO={}\n"
                                "SCIENTIFIC_RESEARCH_AGENT_AGENTS_REF=v0.9.0\n".format(source, research))
            command = ["python3", str(ROOT / "bin/install-agent-extensions"), "--env-file", str(env_file),
                       "--profile", "translator"]
            result = subprocess.run(command + ["--init-research"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((folder / "README.md").is_file())
            (folder / "README.md").write_text("My index\n")
            target = root / "study"
            (target / ".claude/agents").mkdir(parents=True)
            (target / ".claude/agents/researcher.md").write_text(
                "---\nname: researcher\ndescription: General research.\nmodel: sonnet\n"
                "effort: medium\n---\n\nVerify evidence first.\n")
            result = subprocess.run(command + ["--target", str(target)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            installed = (target / ".claude/agents/translator.md").read_text()
            self.assertIn(str(folder), installed)
            self.assertIn("org/research", installed)
            self.assertEqual((folder / "README.md").read_text(), "My index\n")
            self.assertEqual((folder / "user-note.md").read_text(), "My research\n")


class Usage(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.env = {k: os.environ.get(k) for k in ("CLAUDE_CONFIG_DIR", "CODEX_HOME")}
        os.environ["CLAUDE_CONFIG_DIR"], os.environ["CODEX_HOME"] = str(self.tmp / "claude"), str(self.tmp / "codex")
        self.repo = self.tmp / "colony"
        self.repo.mkdir()
        now = dt.datetime.now(dt.timezone.utc)
        recent, old = (now - dt.timedelta(days=1)).isoformat(), (now - dt.timedelta(days=30)).isoformat()

        def line(msg_id, ts, cwd, model="claude-opus-5-5"):
            return json.dumps({"timestamp": ts, "cwd": cwd, "requestId": "r" + msg_id, "message": {
                "id": msg_id, "model": model, "usage": {
                    "input_tokens": 0, "output_tokens": 1_000_000, "cache_read_input_tokens": 1_000_000,
                    "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 1_000_000}}}})
        (self.tmp / "claude" / "projects" / "p").mkdir(parents=True)
        (self.tmp / "claude" / "projects" / "p" / "s.jsonl").write_text("\n".join([
            line("a", recent, str(self.repo)), line("a", recent, str(self.repo)), line("a", recent, str(self.repo)),
            line("b", old, str(self.repo)),
            line("c", recent, str(self.repo / ".claude" / "worktrees" / "wt"), model="claude-haiku-4-5"),
            line("d", recent, "/elsewhere"),
        ]) + "\n")
        (self.tmp / "codex" / "sessions").mkdir(parents=True)
        rl = {"primary": {"used_percent": 26.0, "window_minutes": 300},
              "secondary": {"used_percent": 65.0, "window_minutes": 10080}}
        (self.tmp / "codex" / "sessions" / "s.jsonl").write_text("\n".join(json.dumps(r) for r in [
            {"timestamp": recent, "type": "turn_context", "payload": {"cwd": str(self.repo), "model": "gpt-x"}},
            {"timestamp": recent, "type": "token_usage_record", "payload": {"response_id": "x1", "usage": {
                "input_tokens": 1000, "cached_input_tokens": 800, "output_tokens": 50}}},
            {"timestamp": recent, "type": "token_usage_record", "payload": {"response_id": "x2", "usage": {
                "input_tokens": 2000, "cached_input_tokens": 1500, "output_tokens": 70}}},
            {"timestamp": recent, "type": "event_msg", "payload": {"type": "token_count", "rate_limits": rl}},
        ]) + "\n")
        self.week = (now - dt.timedelta(days=7)).isoformat()

    def tearDown(self):
        shutil.rmtree(self.tmp)
        for k, v in self.env.items():
            os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)

    def test_claude_counts_each_response_once(self):
        self.assertEqual(len(list(agents.claude_usage("2000"))), 4)
        per, total, _ = agents.tally(agents.claude_usage(self.week), [os.path.realpath(self.repo)])
        e = per[os.path.realpath(self.repo)]
        self.assertEqual(e["n"], 2)  # "a" once, and the worktree's "c"; "b" is too old, "d" elsewhere
        self.assertAlmostEqual(e["cost"], 20 + 0.2 + 8 + 5 + 0.1 + 2)
        self.assertEqual(total["n"], 3)

    def test_codex_and_its_plan(self):
        rows, limits = agents.codex_usage("2000")
        rows = list(rows)
        self.assertEqual(sum(t["cache_read"] for _, _, t in rows), 2300)
        self.assertEqual(sum(t["input"] for _, _, t in rows), 700)
        self.assertEqual(limits["secondary"][1], 65.0)
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(agents.main(["usage", str(self.repo)]), 0)
        self.assertIn("weekly window (10080 min): 65% used", out.getvalue())
        self.assertRegex(out.getvalue(), r"colony\s+2\s")


if __name__ == "__main__":
    unittest.main()
