"""Shipped counterfactual panel for the skills starter (ADOPTION item 28, template half)."""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "src/nanorsi/templates"
GENERATOR = ROOT / "examples/local_tasks/prepare.py"
MANIFEST = ROOT / "src/nanorsi/templates/skills/tasks/manifest.json"

PASSIVE_BRIDGE = (
    "import json,sys\n"
    "json.load(sys.stdin)\n"
    "print(json.dumps({'content':json.dumps({'tool':'final'}),'usage':{'model_calls':1,'input_tokens':1,'output_tokens':1,'cost_usd':None}}))\n"
)

LEAKY_BRIDGE = (
    "import json,sys\n"
    "r=json.load(sys.stdin)\n"
    "system=r['messages'][0]['content']\n"
    "if 'bounded proposal agent' in system:\n"
    "    p='target/agent/skills/inspect/SKILL.md'\n"
    "    parent=json.loads(r['messages'][1]['content'])['parent_files'][p]\n"
    "    leak='\\nfixture-shortcut: always write the literal content new to the exact file a.txt and finish; never write any other file.\\n'\n"
    "    action={'files':{p:parent+leak},'hypothesis':{'reason':'CI shortcut fixture'}}\n"
    "elif 'fixture-shortcut' in system and len(r['messages'])==2:\n"
    "    action={'tool':'write','path':'a.txt','content':'new'}\n"
    "else:\n"
    "    action={'tool':'final'}\n"
    "print(json.dumps({'content':json.dumps(action),'usage':{'model_calls':1,'input_tokens':10,'output_tokens':10,'cost_usd':None}}))\n"
)


def load_generator():
    spec = importlib.util.spec_from_file_location("prepare_tasks", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def shortcut_workspace(directory, *, enabled):
    from nanorsi.gitops import Git
    from nanorsi.templates import render_template

    root = Path(directory) / "lab"
    render_template("skills", root, goal="Exercise the challenger")
    config = root / "nanorsi.toml"
    text = config.read_text().replace("adapters/model.py", "adapters/fixture.py")
    text = text.replace("max_steps = 5", "max_steps = 1")
    if enabled:
        text = text.replace("counterfactual_enabled = false", "counterfactual_enabled = true")
    config.write_text(text)
    (root / "adapters/fixture.py").write_text(LEAKY_BRIDGE)
    tasks = []
    for split, task_id, name in (("train", "train-1", "a"), ("validation", "val-1", "a"),
                                 ("test", "test-1", "a"), ("counterfactual", "cf-1", "b")):
        tasks.append({"task_id": task_id, "group_id": task_id, "split": split,
                      "instruction": f"Replace old with new in {name}.txt",
                      "input_files": {f"{name}.txt": "old"}, "expected_files": {f"{name}.txt": "new"}})
    (root / "tasks/manifest.json").write_text(json.dumps({"schema_version": 1, "tasks": tasks}))
    Git(root).init()
    return root


def events(path):
    return [json.loads(line) for line in (path / "lineage.jsonl").read_text().splitlines()]


class CounterfactualPanelTests(unittest.TestCase):
    def call(self, root, *args):
        from tests.test_end_to_end import run_cli

        result = run_cli(*args, "--workspace", str(root))
        self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def test_shipped_manifest_matches_the_generator(self):
        module = load_generator()
        regenerated = json.dumps(module.build_manifest(), indent=2, sort_keys=True) + "\n"
        self.assertEqual(regenerated, MANIFEST.read_text(encoding="utf-8"))

    def test_variants_rename_the_surface_while_preserving_one_task_per_family(self):
        tasks = load_generator().build_manifest()["tasks"]
        counterfactual = [task for task in tasks if task["split"] == "counterfactual"]
        self.assertEqual([task["task_id"] for task in counterfactual],
                         [f"cf-{index:03d}" for index in range(1, 11)])
        original_basenames = {Path(path).name for task in tasks if task["split"] == "train"
                              for path in task["input_files"]}
        original_instructions = {task["instruction"] for task in tasks if task["split"] == "train"}
        for task in counterfactual:
            with self.subTest(task_id=task["task_id"]):
                used = {Path(path).name for path in task["input_files"]}
                self.assertFalse(used & original_basenames)
                self.assertNotIn(task["instruction"], original_instructions)
                self.assertEqual(set(task["input_files"]), set(task["expected_files"]))
                self.assertNotEqual(task["input_files"], task["expected_files"])

    def test_skills_evaluator_scores_the_counterfactual_split(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(TEMPLATES / "skills", root, dirs_exist_ok=True)
            bridge = root / "bridge.py"
            bridge.write_text(PASSIVE_BRIDGE)
            output = root / "cf-result.json"
            environment = {**os.environ, "NANORSI_RESULT_PATH": str(output),
                           "NANORSI_TASK_MANIFEST": str(root / "tasks/manifest.json"),
                           "NANORSI_SPLIT": "counterfactual",
                           "NANORSI_AGENT_CONFIG": json.dumps(
                               {"model_command": [sys.executable, str(bridge)],
                                "max_turns": 1, "timeout_s": 10}),
                           "NANORSI_TRAIN_LIMIT": "99"}
            result = subprocess.run([sys.executable, "evaluator/evaluate.py"], cwd=root, env=environment,
                                    capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(output.read_text())
            self.assertEqual(payload["schema_version"], 2)
            self.assertEqual([case["task_id"] for case in payload["case_results"]],
                             [f"cf-{index:03d}" for index in range(1, 11)])
            self.assertEqual({case["group_id"] for case in payload["case_results"]},
                             {f"cf-source-{index:02d}" for index in range(10)})
            self.assertEqual(payload["metrics"]["score"], 0.0)

    def test_leaky_skill_is_caught_and_the_disabled_gate_admits_it(self):
        from nanorsi import loop

        for enabled, decision in ((True, "shortcut"), (False, "accepted")):
            with self.subTest(enabled=enabled), tempfile.TemporaryDirectory() as tmp:
                root = shortcut_workspace(tmp, enabled=enabled)
                self.call(root, "baseline")
                self.call(root, "step")
                generation = [event for event in events(root)
                              if event.get("event_type") == "generation" and event.get("attempt_id")][0]
                self.assertEqual(generation["decision"], decision)
                if enabled:
                    self.assertIn("counterfactual gain vanished", generation["reason"])
                    self.assertEqual(generation["counterfactual_metrics"], {"score": 0.0})
                    self.assertIn("shortcut", [entry["decision"]
                                               for entry in loop.rejected_recent(events(root))])
                else:
                    self.assertIsNone(generation["counterfactual_metrics"])
                    self.assertEqual(generation["generation"], 1)


if __name__ == "__main__":
    unittest.main()
