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

    def test_every_brief_is_a_valid_subagent(self):
        briefs = sorted((ROOT / "agents").glob("*.md"))
        self.assertEqual(len(briefs), 9)
        for f in briefs:
            fields = frontmatter(f)
            self.assertEqual(fields["name"], f.stem)
            self.assertNotIn(": ", fields["description"], f"{f.name}: ': ' breaks YAML frontmatter")
            self.assertEqual((fields["model"], fields["effort"]), ("{{model}}", "{{effort}}"), f.name)
            self.assertIn("Handing back" if f.stem != "scout" else "What you hand back", f.read_text())

    def test_aep_expert_routing_and_grounding_contract(self):
        path = ROOT / "agents" / "auditory-evoked-potentials.md"
        text = path.read_text()
        fields = frontmatter(path)
        self.assertEqual(set(fields), {"name", "description", "model", "effort"})
        description = fields["description"].lower()
        for term in ("use first", "abr", "assr", "ffr", "mmn", "p300", "binaural", "cochlear",
                     "neurophonic potentials", "auditory crossover", "wins ties",
                     "not for audio engineering", "music production", "speech-to-text"):
            self.assertIn(term, description)

        positive = (
            "What latency is ABR wave V and where is it generated?",
            "Design a 40 Hz binaural-beat stimulus that produces a cortical ASSR.",
            "Does a 500 Hz carrier reach cortex as a waveform?",
            "Where are ITD and ILD computed, and what survives to IC?",
            "Can a sound reset visual-cortex alpha phase?",
        )
        negative = (
            "Mix this podcast at -16 LUFS.",
            "Master this song for streaming.",
            "Transcribe this interview.",
            "Explain visual steady-state evoked potentials.",
            "Which microphone should I buy for vocals?",
        )
        for example in positive + negative:
            self.assertIn(example, text)

        self.assertRegex(text, r"low carrier near 400 Hz, not a\s+carrier near 3 kHz")
        self.assertIn("does **not** reach cortex as a copied 500 Hz waveform", text)
        self.assertIn("no cortical FFR above about 150 Hz", text)
        self.assertIn("W3132668373#p35.3485f9f5", text)
        self.assertIn("W2005066437#p29.cde118db", text)

        evidence_ids = {
            "W3132093913#p1.84c83136", "W3132093913#p7.1a8911b6",
            "W2018764702#p4.ec23c0f4", "W2019142244#p0.70984e33",
            "W2009521233#p0.f60f0091", "W2921598257#p27.145ec4c4",
            "W2160816201#p14.ec95be9f", "W2005066437#p29.cde118db",
            "W3132668373#p4.8bd4f4d2", "W2982822984#p37.0460d25e",
            "W3132668373#p28.2ec3d6f5", "W3132668373#p35.3485f9f5",
            "W3044911540#p4.29d0d66e", "W2883927487#p29.71aa3661",
            "W1979821264#p3.518a0bd2", "W2168669280#p2.82ea1750",
            "W4387058991#p15.97045a85", "W2790726144#p21.4d896ef5",
            "W2612257546#p1.b12041a6", "W2298343390#p49.8780954d",
            "W4406935723#p3.d01784ce", "W4294203154#p41.d68ac02f",
            "W2074020392#p7.74ef22f2", "W2018663098#p7.c4307836",
            "W2029901428#p17.7133fe3f", "W2029901428#p27.68346ba2",
            "W4377089630#p25.96835910",
        }
        for evidence_id in evidence_ids:
            self.assertIn(evidence_id, text)

        ordered_stages = ("cochlea", "auditory nerve", "cochlear nucleus", "superior olivary complex",
                          "inferior colliculus", "medial geniculate body", "primary auditory cortex",
                          "non-primary auditory cortex", "cross-modal")
        positions = [text.index(stage, text.index("## How to trace a stimulus")) for stage in ordered_stages]
        self.assertEqual(positions, sorted(positions))
        for required in ("Established", "Supported", "Hypothesis", "Derived", "Background",
                         "abstract", "passages", "full", "square-law", "detuned receiver",
                         "medical electrical-safety", "## Limitations that travel with the claims"):
            self.assertIn(required, text)

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
