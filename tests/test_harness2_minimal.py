"""Offline contract tests for the harness2-minimal study (no network, no pandoc)."""
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "harness2_minimal"


def _load(name):
    spec = importlib.util.spec_from_file_location(f"h2m_{name}", EXAMPLE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


agent = _load("agent")
run = _load("run")
lab = _load("lab")


def scripted_chat(replies):
    state = {"i": 0}

    def fake(messages, max_tokens=None):
        reply = replies[min(state["i"], len(replies) - 1)]
        state["i"] += 1
        return reply, {"input_tokens": 10, "output_tokens": 5}
    return fake


class ParseReplyTest(unittest.TestCase):
    def test_header_only(self):
        head, body = agent.parse_reply('{"contrast": "neutral", "observation": "same"}')
        self.assertEqual(head["contrast"], "neutral")
        self.assertEqual(body, "")

    def test_header_with_fence(self):
        text = '{"action": "write_deliverable", "filename": "memo.docx"}\n```markdown\n# Memo\nBody\n```'
        head, body = agent.parse_reply(text)
        self.assertEqual(head["action"], "write_deliverable")
        self.assertEqual(body.strip(), "# Memo\nBody")

    def test_bad_header_raises(self):
        with self.assertRaises(agent.ModelError):
            agent.parse_reply("no json at all")


class SystemPromptTest(unittest.TestCase):
    def test_expected_deliverables_and_skill_index(self):
        task = {"deliverables": ["memo.docx"], "documents": {}}
        files = {"systemprompt.md": "be careful", "skills/legal/SKILL.md": "Legal memo structure guidance"}
        system = agent.harness_system_prompt(files, task)
        self.assertIn("memo.docx", system)
        self.assertIn("skills/legal/SKILL.md", system)
        self.assertIn("be careful", system)


TASK = {"name": "t/one", "title": "T", "instructions": "Do it.", "deliverables": ["out.docx"],
        "documents": {"a.txt": Path("/tmp/a.txt")}, "criteria": []}


class ExecuteTaskTest(unittest.TestCase):
    def test_full_tool_loop(self):
        replies = [
            '{"action": "list_documents"}',
            '{"action": "read_document", "name": "a.txt"}',
            '{"action": "write_deliverable", "filename": "out.docx"}\n```markdown\n# Out\nDone\n```',
            '{"action": "done", "summary": "written"}',
        ]
        execution = agent.execute_task(None, TASK, {}, convert=lambda name: f"text of {name}",
                                       chat_fn=scripted_chat(replies))
        self.assertTrue(execution.ok)
        self.assertEqual(execution.deliverables["out.docx"].strip(), "# Out\nDone")
        self.assertIn("[READ] a.txt", execution.trajectory)
        self.assertIn("[WRITE] out.docx", execution.trajectory)
        self.assertEqual(execution.usage["model_calls"], 4)

    def test_wrong_deliverable_name_is_refused_then_done_reports_missing(self):
        replies = [
            '{"action": "write_deliverable", "filename": "wrong.docx"}\n```markdown\nx\n```',
            '{"action": "done", "summary": "gave up"}',
        ]
        execution = agent.execute_task(None, TASK, {}, convert=lambda name: "",
                                       chat_fn=scripted_chat(replies))
        self.assertFalse(execution.ok)
        self.assertIn("missing deliverables: ['out.docx']", execution.error)


class ProposeComposeTest(unittest.TestCase):
    def test_propose_parses_component_and_content(self):
        reply = ('{"component": "tool_guidance.md", "note": "read twice"}\n'
                 '```markdown\nAlways read documents twice.\n```')
        with mock.patch.object(run, "chat") as fake:
            fake.return_value = (reply, {"input_tokens": 1, "output_tokens": 1})
            cand = run.propose(run.AgentConfig(), "key", "INV", TASK, {}, {"trajectory": "", "deliverable_text": ""})
        self.assertEqual(cand["component"], "tool_guidance.md")
        self.assertIn("read documents twice", cand["content"])

    def test_compose_keep(self):
        with mock.patch.object(run, "chat") as fake:
            fake.return_value = ('{"decision": "keep", "observation": "both neutral", "files": []}', {"input_tokens": 1, "output_tokens": 1})
            decision = run.compose(run.AgentConfig(), "key", TASK, {}, [], {}, {"trajectory": ""})
        self.assertEqual(decision["decision"], "keep")
        self.assertEqual(decision["files"], {})

    def test_compose_merge_extracts_file_blocks(self):
        reply = ('{"decision": "merge", "observation": "both mitigate", "files": ["systemprompt.md"]}\n'
                 '===FILE systemprompt.md===\n```markdown\nMerged prompt.\n```')
        with mock.patch.object(run, "chat") as fake:
            fake.return_value = (reply, {"input_tokens": 1, "output_tokens": 1})
            decision = run.compose(run.AgentConfig(), "key", TASK, {}, [], {}, {"trajectory": ""})
        self.assertEqual(decision["files"]["systemprompt.md"].strip(), "Merged prompt.")

    def test_contrast_rejects_unknown_verdict(self):
        empty_run = {"trajectory": "", "deliverable_text": ""}
        with mock.patch.object(run, "chat") as fake:
            fake.return_value = ('{"contrast": "better"}', {"input_tokens": 1, "output_tokens": 1})
            with self.assertRaises(run.ModelError):
                run.contrast(run.AgentConfig(), "key", TASK, empty_run, empty_run,
                             {"dim": "INV", "component": "x", "note": "", "content": ""})


class LabAccessTest(unittest.TestCase):
    def test_task_fixture_roundtrip(self):
        lab_module = lab
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task_dir = root / "tasks" / "area" / "task-one"
            (task_dir / "documents").mkdir(parents=True)
            (task_dir / "documents" / "note.txt").write_text("hello", encoding="utf-8")
            (task_dir / "task.json").write_text(json.dumps({
                "title": "T", "instructions": "Do.",
                "deliverables": {"out.docx": "out.docx"},
                "criteria": [{"id": "C1", "title": "c", "match_criteria": "PASS if x"}],
            }), encoding="utf-8")
            task = lab_module.load_task(root, "area/task-one")
            self.assertEqual(task["deliverables"], ["out.docx"])
            self.assertIn("note.txt", task["documents"])
            bind, convert = lab_module.document_reader(root, sys.executable)
            bind(task)
            self.assertEqual(convert("note.txt"), "hello")
            self.assertEqual(lab_module.list_tasks(root), ["area/task-one"])


class BaseHarnessTest(unittest.TestCase):
    def test_base_harness_has_always_on_components(self):
        files = run.load_base_harness()
        for name in run.EDITABLE:
            self.assertIn(name, files, f"missing {name}")
            self.assertTrue(files[name].strip())


if __name__ == "__main__":
    unittest.main()
