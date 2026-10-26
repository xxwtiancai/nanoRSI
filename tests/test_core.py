import json
import tempfile
import unittest
from pathlib import Path

from nanorsi import harness, tasks
from nanorsi.config import ConfigError, load_config
from nanorsi.ledger import Ledger, LedgerError
from nanorsi.model import Model, ModelError, parse_reply
from nanorsi.templates import render


class ConfigTests(unittest.TestCase):
    def test_template_config_loads_and_rejects_bad_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "ws"
            render(root, goal="g")
            config = load_config(root / "nanorsi.toml")
            self.assertEqual((config.mode, config.k, config.runner.kind), ("agg", 1, "loopback"))
            text = (root / "nanorsi.toml").read_text().replace('mode = "agg"', 'mode = "tree"')
            (root / "nanorsi.toml").write_text(text)
            with self.assertRaises(ConfigError):
                load_config(root / "nanorsi.toml")


class LedgerTests(unittest.TestCase):
    def test_append_verify_and_tamper_detection(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Ledger(Path(tmp) / "ledger.jsonl")
            ledger.append("configured", x=1)
            ledger.append("reserved", kind="rollout")
            ledger.append("rollout", task="t", usage={"input_tokens": 5, "output_tokens": 1})
            self.assertEqual(ledger.verify(), 3)
            self.assertEqual(ledger.usage()["rollouts"], 1)
            lines = ledger.path.read_text().splitlines()
            lines[0] = lines[0].replace('"x": 1', '"x": 2')
            ledger.path.write_text("\n".join(lines) + "\n")
            with self.assertRaises(LedgerError):
                ledger.verify()


class HarnessTests(unittest.TestCase):
    def test_validate_edit_render(self):
        tree = {"systemprompt.md": "Be careful.\n", "skills/legal/SKILL.md": "description: legal memo structure\n\nUse headings.\n"}
        harness.validate(tree)
        rendered = harness.render_always_on(tree)
        self.assertIn("Be careful.", rendered)
        self.assertIn("`legal`: legal memo structure", rendered)
        updated = harness.apply_edit(tree, "guardrails.md", "- Read twice")
        self.assertEqual(harness.diff_summary(tree, updated)["added"], ["guardrails.md"])
        with self.assertRaises(harness.HarnessError):
            harness.apply_edit(tree, "evaluator/evaluate.py", "x")
        with self.assertRaises(harness.HarnessError):
            harness.validate({"skills/a/SKILL.md": "only\n"})

    def test_write_and_read_tree_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            tree = {"systemprompt.md": "a\n", "scripts/check.py": "print(1)\n"}
            harness.write_tree(tree, Path(tmp) / "h")
            self.assertEqual(harness.read_tree(Path(tmp) / "h"), tree)


class TaskTests(unittest.TestCase):
    def test_manifest_rules(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "m.json").write_text(json.dumps({"schema_version": 1, "tasks": [
                {"task_id": "a", "instruction": "do", "documents": {"d": "docs/d.txt"}, "deliverables": ["out.md"]},
                {"task_id": "a", "instruction": "do", "deliverables": ["out.md"]}]}))
            with self.assertRaises(tasks.TaskError):
                tasks.load_tasks(root, "m.json")
            (root / "m.json").write_text(json.dumps({"schema_version": 1, "tasks": [
                {"task_id": "a", "domain": "x", "instruction": "do", "deliverables": ["out.md"]}]}))
            loaded = tasks.load_tasks(root, "m.json")
            self.assertEqual(tasks.select_tasks(loaded, ["x"], 0)[0]["task_id"], "a")


class ReplyGrammarTests(unittest.TestCase):
    def test_header_and_fences(self):
        header, bodies = parse_reply('{"component": "guardrails.md"}\n```markdown\n- a\n```\n```python\nprint(1)\n```')
        self.assertEqual(header["component"], "guardrails.md")
        self.assertEqual(bodies, ["- a\n", "print(1)\n"])
        with self.assertRaises(ModelError):
            parse_reply("no header here")

    def test_model_retries_and_reports_usage(self):
        calls = {"n": 0}

        def transport(payload):
            calls["n"] += 1
            return {"choices": [{"message": {"content": "OK"}}], "usage": {"prompt_tokens": 3, "completion_tokens": 1}}

        config = load_config(_template_config())
        text, usage = Model(config.model, api_key="k", transport=transport).call([{"role": "user", "content": "hi"}])
        self.assertEqual((text, usage["input_tokens"], calls["n"]), ("OK", 3, 1))


class ComposeTests(unittest.TestCase):
    def _compose(self, reply: str):
        from nanorsi import propose, runner
        config = load_config(_template_config())
        transport = lambda payload: {"choices": [{"message": {"content": reply}}], "usage": {}}
        model = Model(config.model, api_key="k", transport=transport)
        base = {"systemprompt.md": "Be careful.\n"}
        inv = propose.Candidate("INV", "guardrails.md", "verify figures", {**base, "guardrails.md": "- Verify figures.\n"})
        dom = propose.Candidate("DOM", "tool_guidance.md", "cite clauses", {**base, "tool_guidance.md": "- Cite clauses.\n"})
        ref = runner.Rollout("base1", Path("."), True, True, "trace")
        contrasts = {"INV": {"contrast": "mitigates", "observation": "o"}, "DOM": {"contrast": "mitigates", "observation": "o"}}
        return propose.compose(model, {"task_id": "t", "instruction": "do"}, base, [inv, dom], contrasts, ref)

    def test_adopt_takes_the_candidate_tree_without_bodies(self):
        record, tree = self._compose('{"decision": "adopt_dom", "observation": "dom mitigated", "files": ["tool_guidance.md"]}')
        self.assertEqual(record["decision"], "adopt_dom")
        self.assertEqual(tree["tool_guidance.md"], "- Cite clauses.\n")
        self.assertNotIn("guardrails.md", tree)

    def test_adopt_applies_extra_bodies_on_top(self):
        record, tree = self._compose('{"decision": "adopt_inv", "observation": "o", "files": ["memory.md"]}\n```markdown\nLesson: verify.\n```')
        self.assertEqual(tree["guardrails.md"], "- Verify figures.\n")
        self.assertEqual(tree["memory.md"], "Lesson: verify.\n")

    def test_merge_requires_bodies_and_falls_back_to_keep(self):
        record, tree = self._compose('{"decision": "merge", "observation": "o", "files": ["guardrails.md", "tool_guidance.md"]}')
        self.assertEqual(record["decision"], "keep")
        self.assertIn("merge lists 2 files", record["error"])
        self.assertEqual(tree, {"systemprompt.md": "Be careful.\n"})


def _template_config() -> Path:
    tmp = Path(tempfile.mkdtemp()) / "ws"
    render(tmp, goal="g")
    return tmp / "nanorsi.toml"


if __name__ == "__main__":
    unittest.main()
