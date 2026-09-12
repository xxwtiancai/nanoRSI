"""Offline engineering checks; fake bridges are not model-improvement evidence."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

TEMPLATES = Path(__file__).resolve().parents[1] / "src/nanorsi/templates"


def _render(root, name):
    shutil.copytree(TEMPLATES / "skills", root, dirs_exist_ok=True)
    shutil.copyfile(root / "evaluator/evaluate.py", root / "evaluator/_skills.py")
    if name == "agent":
        shutil.copyfile(root / "target/agent/run.py", root / "target/agent/_skills.py")
    overlay = TEMPLATES / name
    if overlay.exists():
        shutil.copytree(overlay, root, dirs_exist_ok=True)


def _evaluate(root, split="train"):
    output = root / f"{split}-result.json"
    environment = {**os.environ, "NANORSI_RESULT_PATH": str(output), "NANORSI_TASK_MANIFEST": str(root / "tasks/manifest.json"), "NANORSI_SPLIT": split, "NANORSI_AGENT_CONFIG": "{}", "NANORSI_TRAIN_LIMIT": "99"}
    result = subprocess.run([sys.executable, "evaluator/evaluate.py"], cwd=root, env=environment, capture_output=True, text=True, timeout=20)
    if result.returncode:
        raise AssertionError(result.stderr)
    return json.loads(output.read_text())


def _runner(root, request):
    result = subprocess.run([sys.executable, "target/agent/run.py"], cwd=root, input=json.dumps(request), capture_output=True, text=True, timeout=10)
    if result.returncode:
        raise AssertionError(result.stderr)
    return json.loads(result.stdout)


class LiveTemplateTests(unittest.TestCase):
    def test_program_executes_mutable_source_and_only_train_exposes_feedback(self):
        self.assertTrue((TEMPLATES / "program/target/program.py").is_file())
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _render(root, "program")
            baseline = _evaluate(root)
            self.assertGreater(baseline["metrics"]["score"], 0)
            self.assertLess(baseline["metrics"]["score"], 1)
            self.assertEqual(len(baseline["case_results"]), 4)
            self.assertIn("expected_files", baseline["case_results"][0]["feedback"])
            source = root / "target/program.py"
            old_hash = hashlib.sha256(source.read_bytes()).hexdigest()
            # A test-only source mutation proves the evaluator executes the target.
            source.write_text("import json, sys\njson.load(sys.stdin)\nprint('{}')\n")
            changed = _evaluate(root)
            self.assertEqual(changed["metrics"]["score"], 0)
            self.assertNotEqual(old_hash, changed["case_results"][0]["trace"][0]["sha256"])
            for split in ("validation", "test"):
                heldout = _evaluate(root, split)
                self.assertEqual(len(heldout["case_results"]), 4)
                self.assertTrue(all("task" not in case and "feedback" not in case for case in heldout["case_results"]))

    def test_agent_executes_plans_and_reloads_mutated_source_for_proposal(self):
        self.assertTrue((TEMPLATES / "agent/target/agent/run.py").is_file())
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _render(root, "agent")
            baseline = _evaluate(root)
            self.assertGreater(baseline["metrics"]["score"], 0)
            self.assertLess(baseline["metrics"]["score"], 1)
            source = root / "target/agent/run.py"
            original = source.read_text()
            old_hash = hashlib.sha256(source.read_bytes()).hexdigest()
            # Exercise a generic dependency scheduler as an offline patch fixture.
            replacement = '''    pending = list(steps)
    ordered = []
    available = set()
    while pending:
        ready = [step for step in pending if set(step.get("depends_on", [])) <= available]
        if not ready:
            raise _skills.RunnerError("cyclic or missing dependency")
        for step in ready:
            ordered.append(step)
            available.add(step["id"])
            pending.remove(step)
    return ordered'''
            self.assertIn("    return list(steps)", original)
            source.write_text(original.replace("    return list(steps)", replacement))
            improved = _evaluate(root)
            self.assertEqual(improved["metrics"]["score"], 1)
            new_hash = hashlib.sha256(source.read_bytes()).hexdigest()
            self.assertNotEqual(new_hash, old_hash)
            self.assertTrue(all(case["trace"][0]["sha256"] == new_hash for case in improved["case_results"]))
            bridge = root / "bridge.py"
            bridge.write_text("import json,sys\njson.load(sys.stdin)\nprint(json.dumps({'content':json.dumps({'diff':'', 'hypothesis':{'reason':'offline fixture'}}),'usage':{}}))\n")
            request = {"mode":"propose", "context":{"goal":"improve", "parent_files":{}}, "agent":{"model_command":[sys.executable,str(bridge)]}}
            result = _runner(root, request)
            self.assertEqual(result["status"], "ok")
            self.assertEqual(result["trace"][0]["sha256"], new_hash)
            self.assertEqual(result["trace"][0]["event"], "runner_loaded")

    def test_source_context_includes_program_and_excludes_denied_protected_large_binary_and_symlinks(self):
        proposer = runpy.run_path(str(TEMPLATES / "skills/proposer/propose.py"))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "target/private").mkdir(parents=True)
            (root / "target/program.py").write_text("def solve(x): return x\n")
            (root / "target/private/secret.txt").write_text("private")
            (root / "target/binary.bin").write_bytes(b"\x00\xff")
            (root / "target/huge.txt").write_text("x" * 300000)
            (root / "tasks").mkdir()
            (root / "tasks/manifest.json").write_text("heldout-secret")
            (root / "target/symlink").symlink_to(root / "tasks", target_is_directory=True)
            (root / "target/.env").write_text("credential")
            (root / "target/nanorsi.toml").write_text("private-config")
            (root / "target/tasks").mkdir()
            (root / "target/tasks/manifest.json").write_text("nested-heldout")
            with patch("os.getcwd", return_value=str(root)):
                files = proposer["_gather_parent_files"]({"surface":{"allow":["**"], "deny":["target/private/**"]}})
            self.assertEqual(files, {"target/program.py":"def solve(x): return x\n"})

    def test_proposal_prompt_forwards_operator_parents_thinking_and_only_train_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _render(root, "skills")
            bridge = root / "bridge.py"
            capture = root / "capture.json"
            bridge.write_text("import json,sys\nfrom pathlib import Path\nr=json.load(sys.stdin)\nPath(" + repr(str(capture)) + ").write_text(json.dumps(r))\nprint(json.dumps({'content':json.dumps({'diff':'', 'hypothesis':{}}),'usage':{}}))\n")
            context = {"goal":"improve", "parent_files":{"target/program.py":"print(1)"}, "train_results":[{"task_id":"train-one"}], "operator":"crossover", "extra_parents":[{"candidate_id":"parent-b", "source":{"target/program.py":"print(2)"}}], "validation_results":"hidden-validation", "test_results":"hidden-test"}
            request = {"mode":"propose", "context":context, "agent":{"model_command":[sys.executable,str(bridge)], "thinking":{"type":"disabled"}}}
            result = _runner(root, request)
            self.assertEqual(result["status"], "ok")
            seen = json.loads(capture.read_text())
            self.assertEqual(seen["thinking"], {"type":"disabled"})
            prompt = json.loads(seen["messages"][1]["content"])
            self.assertEqual(prompt["operator"], "crossover")
            self.assertEqual(prompt["extra_parents"], context["extra_parents"])
            self.assertNotIn("hidden-validation", json.dumps(seen))
            self.assertNotIn("hidden-test", json.dumps(seen))
            self.assertEqual(result["trace"][0]["sha256"], hashlib.sha256((root / "target/agent/run.py").read_bytes()).hexdigest())

    def test_live_driver_passes_program_source_and_filtered_crossover_parent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _render(root, "program")
            bridge = root / "bridge.py"
            capture = root / "capture.json"
            bridge.write_text("import json,sys\nfrom pathlib import Path\nr=json.load(sys.stdin)\nPath(" + repr(str(capture)) + ").write_text(json.dumps(r))\nprint(json.dumps({'content':json.dumps({'diff':'', 'hypothesis':{}}),'usage':{}}))\n")
            context = {"goal":"improve", "surface":{"allow":["target/program.py"]}, "agent":{"model_command":[sys.executable,str(bridge)]}, "train_results":[_evaluate(root)], "operator":"crossover", "extra_parents":[{"candidate_id":"other", "candidate_commit":"abc", "parent_files":{"target/program.py":"print(2)", "tasks/manifest.json":"hidden-test-source"}}], "validation_results":"hidden-validation", "test_results":"hidden-test"}
            context_path = root / "context.json"
            context_path.write_text(json.dumps(context))
            environment = {**os.environ, "NANORSI_CONTEXT_PATH":str(context_path), "NANORSI_PROPOSAL_DIR":str(root / "proposal"), "NANORSI_PROPOSER_HARNESS":str(root)}
            result = subprocess.run([sys.executable,"proposer/propose.py"], cwd=root, env=environment, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["status"], "ok")
            payload = json.loads(capture.read_text())
            visible = json.loads(payload["messages"][1]["content"])
            self.assertEqual(visible["parent_files"], {"target/program.py":(root / "target/program.py").read_text()})
            self.assertEqual(visible["extra_parents"][0]["parent_files"], {"target/program.py":"print(2)"})
            self.assertEqual(visible["extra_parents"][0]["candidate_id"], "other")
            self.assertNotIn("hidden-test", json.dumps(payload))
            self.assertNotIn("hidden-validation", json.dumps(payload))
            self.assertIn("expected_files", json.dumps(visible["train_results"]))

    def test_model_source_replacements_generate_applicable_git_diff(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _render(root, "skills")
            program = root / "target/program.py"
            program.write_text("value = 1")
            replacements = {"target/program.py":"value = 2\nprint(value)", "target/agent/skills/edit/run.py":"import json\nprint(json.dumps({'done': True}))\n", "target/empty.txt":""}
            bridge = root / "bridge.py"
            response = {"files":replacements, "hypothesis":{"reason":"offline source fixture"}}
            bridge.write_text("import json,sys\njson.load(sys.stdin)\nprint(json.dumps({'content':" + repr(json.dumps(response)) + ",'usage':{}}))\n")
            result = _runner(root, {"mode":"propose", "context":{"parent_files":{"target/program.py":"value = 1"}, "surface":{"allow":["target/**"]}}, "agent":{"model_command":[sys.executable,str(bridge)]}})
            self.assertEqual(result["status"], "ok", result)
            self.assertIn("--- /dev/null", result["diff"])
            self.assertIn("No newline at end of file", result["diff"])
            subprocess.run(["git","init","-q"], cwd=root, check=True)
            check = subprocess.run(["git","apply","--check","-"], cwd=root, input=result["diff"], text=True, capture_output=True)
            self.assertEqual(check.returncode, 0, check.stderr)
            subprocess.run(["git","apply","-"], cwd=root, input=result["diff"], text=True, check=True)
            for path, source in replacements.items():
                self.assertEqual((root / path).read_text(), source)

    def test_source_replacements_reject_invalid_paths_types_and_private_files(self):
        runtime = runpy.run_path(str(TEMPLATES / "skills/target/agent/run.py"))
        self.assertIn("_replacement_diff", runtime)
        context = {"surface":{"allow":["**"], "deny":["target/private/**"]}, "parent_files":{}}
        for path in ("../outside.py", "/tmp/outside.py", "target/../outside.py", "target/./x.py", "target/private/key.txt", "target/.env", "target/.env.secret", "target/tasks/manifest.json", "tasks/manifest.json", "target/key.pem", "target/credentials", "target/a\\b.py"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                runtime["_replacement_diff"]({path:"secret"}, context)
        for files in ([], {"target/a.py":None}, {"target/a.py":7}, {"target/a.py":"\x00binary"}):
            with self.subTest(files=files), self.assertRaises(ValueError):
                runtime["_replacement_diff"](files, context)
        self.assertEqual(runtime["_replacement_diff"]({}, context), "")

    def test_parent_source_budget_bounds_all_files_together(self):
        proposer = runpy.run_path(str(TEMPLATES / "skills/proposer/propose.py"))
        source = {f"target/part{index}.py":"x" * 50000 for index in range(12)}
        bounded = proposer["_bounded_source"](source, {"surface":["target/**"]})
        self.assertLessEqual(sum(len(value.encode()) for value in bounded.values()), 192000)
        self.assertEqual(len(bounded), 3)

    def test_declared_skill_script_executes_with_arguments_and_actual_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _render(root, "skills")
            script = root / "target/agent/skills/edit/run.py"
            script.write_text("import json,sys\nfrom pathlib import Path\nr=json.load(sys.stdin)\n(Path(r['workspace'])/'note.txt').write_text(r['arguments']['text'])\nprint(json.dumps({'written':'note.txt'}))\n")
            bridge = root / "bridge.py"
            bridge.write_text("import json,sys\nr=json.load(sys.stdin)\na={'tool':'final'} if any(m['role']=='assistant' for m in r['messages']) else {'tool':'skill','name':'edit','arguments':{'text':'updated'}}\nprint(json.dumps({'content':json.dumps(a),'usage':{}}))\n")
            result = _runner(root, {"mode":"task", "task":{"instruction":"edit note", "input_files":{"note.txt":"before"}}, "agent":{"skills":["edit"], "model_command":[sys.executable,str(bridge)]}})
            self.assertEqual(result["status"], "ok")
            self.assertEqual(result["output_files"]["note.txt"], "updated")
            digest = hashlib.sha256(script.read_bytes()).hexdigest()
            calls = [item for item in result["trace"] if item.get("event") == "skill_script_invoked"]
            self.assertEqual(calls[0]["sha256"], digest)
            self.assertEqual(result["skill_hashes"]["edit/run.py"], digest)

    def test_skill_action_rejects_undeclared_names_and_script_output_overflow(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _render(root, "skills")
            script = root / "target/agent/skills/edit/run.py"
            script.write_text("print('x' * 2000000)\n")
            bridge = root / "bridge.py"
            request = {"mode":"task", "task":{"instruction":"edit", "input_files":{}}, "agent":{"skills":["edit"], "model_command":[sys.executable,str(bridge)]}}
            for name, code in (("../edit", "undeclared"), ("verify", "undeclared"), ("edit", "output limit")):
                bridge.write_text("import json,sys\njson.load(sys.stdin)\nprint(json.dumps({'content':json.dumps({'tool':'skill','name':" + repr(name) + ",'arguments':{}}),'usage':{}}))\n")
                result = _runner(root, request)
                self.assertEqual(result["status"], "error")
                self.assertIn(code, json.dumps(result["trace"]))

    def test_self_use_executes_learned_planner_while_building_next_proposal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _render(root, "agent")
            source = root / "target/agent/run.py"
            original = source.read_text()
            manifest = json.loads((root / "tasks/manifest.json").read_text())
            task = next(task for task in manifest["tasks"] if task["task_id"] == "train-reverse")
            case = {"task_id":task["task_id"], "task":{"input_files":task["input_files"]}, "feedback":{"expected_files":task["expected_files"]}}
            capture = root / "capture.json"
            bridge = root / "bridge.py"
            bridge.write_text("import json,sys\nfrom pathlib import Path\nr=json.load(sys.stdin)\nPath(" + repr(str(capture)) + ").write_text(json.dumps(r))\nprint(json.dumps({'content':json.dumps({'files':{},'hypothesis':{}}),'usage':{}}))\n")
            context = {"parent_files":{"target/agent/run.py":original}, "train_results":[case], "validation_results":"private-validation-workflow", "test_results":"private-test-workflow"}
            request = {"mode":"propose", "context":context, "agent":{"model_command":[sys.executable,str(bridge)]}}
            before = _runner(root, request)
            before_prompt = json.loads(json.loads(capture.read_text())["messages"][1]["content"])
            self.assertIn("proposal_planning", before_prompt["train_results"][0]["feedback"])
            before_plan = before_prompt["train_results"][0]["feedback"]["proposal_planning"]
            source.write_text(original.replace("    return list(steps)", "    return list(reversed(steps))"))
            after = _runner(root, request)
            after_prompt = json.loads(json.loads(capture.read_text())["messages"][1]["content"])
            after_plan = after_prompt["train_results"][0]["feedback"]["proposal_planning"]
            self.assertEqual(before["status"], "ok")
            self.assertEqual(after["status"], "ok")
            self.assertEqual(after_plan["planned_step_ids"], list(reversed(before_plan["planned_step_ids"])))
            self.assertFalse(before_plan["dependency_order_valid"])
            self.assertTrue(after_plan["dependency_order_valid"])
            self.assertEqual(before_prompt["parent_files"], after_prompt["parent_files"])
            for result, prompt in ((before, before_prompt), (after, after_prompt)):
                self.assertTrue(any(item.get("event") == "proposal_planner_used" for item in result["trace"]))
                self.assertNotIn("private-validation-workflow", json.dumps(prompt))
                self.assertNotIn("private-test-workflow", json.dumps(prompt))
            self.assertNotIn("proposal_planning", case["feedback"])

    def test_program_grading_accepts_equivalent_numeric_json_and_rejects_boolean_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _render(root, "program")
            program = root / "target/program.py"
            original = program.read_text()
            baseline = _evaluate(root)
            program.write_text(original.replace('"count": count', '"count": float(count)'))
            self.assertEqual(_evaluate(root)["metrics"]["score"], baseline["metrics"]["score"])
            program.write_text("import json,sys\njson.load(sys.stdin)\nprint(json.dumps({'count':True,'totals':{'uncategorized':'18.01'}}))\n")
            self.assertEqual(_evaluate(root, "validation")["metrics"]["score"], 0)
            precise = '{"count":2.00000000000000001,"totals":{"travel":"15.50"}}'
            program.write_text("import sys\nsys.stdout.write(" + repr(precise) + ")\n")
            self.assertEqual(_evaluate(root)["metrics"]["score"], 0)

    def test_program_grading_does_not_import_target_agent_as_helper(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _render(root, "program")
            (root / "target/agent/run.py").write_text("raise RuntimeError('mutable helper imported by evaluator')\n")
            result = _evaluate(root)
            self.assertEqual(result["status"], "ok")
            self.assertGreater(result["metrics"]["score"], 0)

    def test_task_prompt_exposes_configured_turn_budget(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _render(root, "skills")
            bridge = root / "bridge.py"
            capture = root / "capture.json"
            bridge.write_text("import json,sys\nfrom pathlib import Path\nr=json.load(sys.stdin)\nPath(" + repr(str(capture)) + ").write_text(json.dumps(r))\nprint(json.dumps({'content':json.dumps({'tool':'final'}),'usage':{}}))\n")
            result = _runner(root, {"mode":"task", "task":{"instruction":"finish", "input_files":{}}, "agent":{"max_turns":4,"model_command":[sys.executable,str(bridge)]}})
            self.assertEqual(result["status"], "ok")
            messages = json.loads(capture.read_text())["messages"]
            self.assertEqual(json.loads(messages[1]["content"]).get("max_turns"), 4)
            self.assertIn("including final", messages[0]["content"])

    def test_agent_default_comparison_uses_baseline_and_candidate(self):
        import tomllib
        config = tomllib.loads((TEMPLATES / "agent/nanorsi.toml").read_text())
        self.assertEqual(config["experiment"].get("final_conditions"), ["baseline", "candidate"])

    def test_task_splits_have_disjoint_groups_and_inputs(self):
        for name in ("program", "agent"):
            manifest = TEMPLATES / name / "tasks/manifest.json"
            self.assertTrue(manifest.is_file())
            tasks = json.loads(manifest.read_text())["tasks"]
            self.assertEqual(len(tasks), 12)
            groups = {split:{task["group_id"] for task in tasks if task["split"] == split} for split in ("train","validation","test")}
            self.assertFalse(groups["train"] & (groups["validation"] | groups["test"]))
            self.assertFalse(groups["validation"] & groups["test"])
            self.assertEqual(len({json.dumps(task["input_files"], sort_keys=True) for task in tasks}), 12)


if __name__ == "__main__":
    unittest.main()
