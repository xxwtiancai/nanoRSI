import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import runpy
import subprocess
import sys
import tempfile
import textwrap
import threading
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "src" / "nanorsi" / "templates" / "skills"
RUNNER = TEMPLATE / "target" / "agent" / "run.py"
EVALUATOR = TEMPLATE / "evaluator" / "evaluate.py"
PROPOSER = TEMPLATE / "proposer" / "propose.py"
ADAPTER = TEMPLATE / "adapters" / "model.py"


def _write_fake_bridge(directory: Path, *, proposal: bool = False) -> Path:
    script = directory / "fake_bridge.py"
    if proposal:
        body = """
import json, sys
request = json.load(sys.stdin)
assert request["messages"][0]["role"] == "system"
print(json.dumps({"content": json.dumps({"diff": "patch", "hypothesis": {"reason": "fixture"}}), "usage": {"model_calls": 1, "input_tokens": 5, "output_tokens": 3, "cost_usd": None}}))
"""
    else:
        body = """
import json, sys
request = json.load(sys.stdin)
messages = request["messages"]
assistants = [item for item in messages if item.get("role") == "assistant"]
if not assistants:
    action = {"tool": "list"}
elif len(assistants) == 1:
    action = {"tool": "read", "path": "note.txt"}
elif len(assistants) == 2:
    action = {"tool": "write", "path": "note.txt", "content": "edited"}
else:
    action = {"tool": "final"}
print(json.dumps({"content": json.dumps(action), "usage": {"model_calls": 1, "input_tokens": 10, "output_tokens": 2, "cost_usd": None}}))
"""
    script.write_text(textwrap.dedent(body), encoding="utf-8")
    return script


def _run(request, *, cwd: Path):
    result = subprocess.run(
        [sys.executable, str(RUNNER)],
        input=json.dumps(request),
        capture_output=True,
        text=True,
        cwd=cwd,
        check=False,
    )
    if result.returncode:
        raise AssertionError(f"runner failed: {result.stderr}\n{result.stdout}")
    return json.loads(result.stdout)


class SkillsRunnerTests(unittest.TestCase):
    def test_task_loads_skills_and_runs_isolated_read_write_episode(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bridge = _write_fake_bridge(root)
            result = _run(
                {
                    "mode": "task",
                    "task": {"task_id": "one", "instruction": "edit note", "input_files": {"note.txt": "original"}},
                    "agent": {"model_command": [sys.executable, str(bridge)], "model": "fixture", "skills": ["inspect", "edit", "verify"]},
                },
                cwd=root,
            )
            self.assertEqual(result["status"], "ok")
            self.assertEqual(result["output_files"]["note.txt"], "edited")
            self.assertEqual(set(result["skill_hashes"]), {"inspect", "edit", "verify"})
            for name, digest in result["skill_hashes"].items():
                content = (TEMPLATE / "target" / "agent" / "skills" / name / "SKILL.md").read_bytes()
                self.assertEqual(digest, hashlib.sha256(content).hexdigest())
            self.assertGreaterEqual(result["usage"]["model_calls"], 4)
            self.assertTrue(any(item.get("event") == "skills_loaded" for item in result["trace"]))

    def test_task_rejects_path_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outside = root.parent / "nanorsi-runner-secret.txt"
            outside.write_text("secret", encoding="utf-8")
            bridge = root / "bad_bridge.py"
            bridge.write_text(
                "import json,sys\njson.load(sys.stdin)\nprint(json.dumps({'content': json.dumps({'tool':'read','path':'../nanorsi-runner-secret.txt'}), 'usage': {'model_calls': 1}}))\n",
                encoding="utf-8",
            )
            result = _run(
                {"mode": "task", "task": {"task_id": "bad", "instruction": "read", "input_files": {}}, "agent": {"model_command": [sys.executable, str(bridge)], "model": "fixture", "skills": []}},
                cwd=root,
            )
            self.assertEqual(result["status"], "error")
            self.assertIn("path", json.dumps(result["trace"]).lower())
            self.assertEqual(outside.read_text(encoding="utf-8"), "secret")

    def test_runner_rejects_nonfinite_timeout_and_turns_above_cap(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = _run({"mode": "task", "task": {"task_id": "bad", "instruction": "x", "input_files": {}}, "agent": {"model_command": [sys.executable, "missing.py"], "skills": [], "timeout_s": float("inf")}}, cwd=root)
            self.assertEqual(result["status"], "error")
            self.assertEqual(result["usage"]["model_calls"], 0)
            result = _run({"mode": "task", "task": {"task_id": "bad", "instruction": "x", "input_files": {}}, "agent": {"model_command": [sys.executable, "missing.py"], "skills": [], "max_turns": 9}}, cwd=root)
            self.assertEqual(result["status"], "error")
            self.assertIn("max_turns", json.dumps(result["trace"]))

    def test_bridge_timeout_and_output_overflow_are_bounded_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            overflow = root / "overflow.py"
            overflow.write_text("import sys\nsys.stdout.write('x' * 2000000)\nsys.stdout.flush()\n", encoding="utf-8")
            result = _run({"mode": "task", "task": {"task_id": "overflow", "instruction": "x", "input_files": {}}, "agent": {"model_command": [sys.executable, str(overflow)], "skills": [], "timeout_s": 5}}, cwd=root)
            self.assertEqual(result["status"], "error")
            self.assertEqual(result["usage"]["model_calls"], 1)
            self.assertIn("model_output_limit", result["usage"]["errors"])
            timeout = root / "timeout.py"
            timeout.write_text("import time\ntime.sleep(2)\n", encoding="utf-8")
            result = _run({"mode": "task", "task": {"task_id": "timeout", "instruction": "x", "input_files": {}}, "agent": {"model_command": [sys.executable, str(timeout)], "skills": [], "timeout_s": 0.1}}, cwd=root)
            self.assertEqual(result["status"], "error")
            self.assertEqual(result["usage"]["model_calls"], 1)
            self.assertIn("model_timeout", result["usage"]["errors"])

    def test_propose_returns_model_diff_and_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bridge = _write_fake_bridge(root, proposal=True)
            result = _run(
                {"mode": "propose", "context": {"goal": "improve", "parent_files": {"target/agent/a.txt": "x"}}, "agent": {"model_command": [sys.executable, str(bridge)], "model": "fixture", "skills": ["inspect"]}},
                cwd=root,
            )
            self.assertEqual(result["diff"], "patch")
            self.assertEqual(result["hypothesis"]["reason"], "fixture")
            self.assertEqual(result["usage"]["model_calls"], 1)

    def test_proposer_driver_gathers_parent_surface_and_writes_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "target" / "agent").mkdir(parents=True)
            (root / "target" / "agent" / "policy.txt").write_text("parent", encoding="utf-8")
            bridge = _write_fake_bridge(root, proposal=True)
            context_path = root / "context.json"
            context_path.write_text(json.dumps({"goal": "improve", "surface": {"allow": ["target/**"]}, "agent": {"model_command": [sys.executable, str(bridge)], "model": "fixture", "skills": ["inspect"]}, "train_results": [{"score": 1.0}], "parent_commit": "p", "proposer_harness_commit": "h"}), encoding="utf-8")
            proposal_dir = root / "proposal"
            env = os.environ.copy()
            env.update({"NANORSI_CONTEXT_PATH": str(context_path), "NANORSI_PROPOSAL_DIR": str(proposal_dir), "NANORSI_PROPOSER_HARNESS": str(TEMPLATE)})
            completed = subprocess.run([sys.executable, str(PROPOSER)], cwd=root, env=env, capture_output=True, text=True, check=False)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual((proposal_dir / "proposal.diff").read_text(encoding="utf-8"), "patch")
            self.assertTrue((proposal_dir / "hypothesis.json").is_file())
            self.assertTrue((proposal_dir / "usage.json").is_file())
            self.assertTrue((proposal_dir / "trace.json").is_file())

    def test_proposer_rejects_nonzero_runner_and_removes_stale_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            harness = root / "harness"
            (harness / "target" / "agent").mkdir(parents=True)
            (harness / "target" / "agent" / "run.py").write_text("import json,sys\nprint(json.dumps({'status':'ok','diff':'new','hypothesis':{}}))\nsys.exit(1)\n", encoding="utf-8")
            context_path = root / "context.json"
            context_path.write_text(json.dumps({"goal": "improve", "surface": ["target/**"], "agent": {"model": "fixture", "model_command": [sys.executable, "missing.py"], "skills": []}}), encoding="utf-8")
            proposal_dir = root / "proposal"
            proposal_dir.mkdir()
            (proposal_dir / "proposal.diff").write_text("stale", encoding="utf-8")
            (proposal_dir / "hypothesis.json").write_text("{}", encoding="utf-8")
            env = os.environ.copy()
            env.update({"NANORSI_CONTEXT_PATH": str(context_path), "NANORSI_PROPOSAL_DIR": str(proposal_dir), "NANORSI_PROPOSER_HARNESS": str(harness)})
            completed = subprocess.run([sys.executable, str(PROPOSER)], cwd=root, env=env, capture_output=True, text=True, check=False)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertFalse((proposal_dir / "proposal.diff").exists())
            self.assertFalse((proposal_dir / "hypothesis.json").exists())
            self.assertEqual(json.loads((proposal_dir / "usage.json").read_text(encoding="utf-8"))["model_calls"], 0)
            self.assertIn("exit", (proposal_dir / "trace.json").read_text(encoding="utf-8"))

    def test_finite_platform_max_timeout_writes_structured_failure_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "target" / "agent").mkdir(parents=True)
            (root / "target" / "agent" / "run.py").write_bytes(RUNNER.read_bytes())
            bridge = _write_fake_bridge(root)
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({"schema_version": 1, "tasks": [{"task_id": "t1", "group_id": "g1", "split": "validation", "instruction": "edit note", "input_files": {"note.txt": "original"}, "expected_files": {"note.txt": "edited"}}]}), encoding="utf-8")
            result_path = root / "result.json"
            env = os.environ.copy()
            env.update({"NANORSI_SPLIT": "validation", "NANORSI_RESULT_PATH": str(result_path), "NANORSI_TASK_MANIFEST": str(manifest), "NANORSI_AGENT_CONFIG": json.dumps({"model_command": [sys.executable, str(bridge)], "model": "fixture", "skills": [], "timeout_s": sys.float_info.max}), "NANORSI_REPEAT_ID": "0", "NANORSI_SEED": "0"})
            completed = subprocess.run([sys.executable, str(EVALUATOR)], cwd=root, env=env, capture_output=True, text=True, check=False)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(result_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["case_results"][0]["status"], "runner_error")
            self.assertIn("platform timeout", payload["case_results"][0]["usage"]["errors"][0])

    def test_proposer_platform_max_timeout_keeps_failure_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            harness = root / "harness"
            (harness / "target" / "agent").mkdir(parents=True)
            (harness / "target" / "agent" / "run.py").write_text("print('{}')\n", encoding="utf-8")
            context_path = root / "context.json"
            context_path.write_text(json.dumps({"goal": "improve", "surface": ["target/**"], "agent": {"model": "fixture", "model_command": [sys.executable, "missing.py"], "skills": [], "timeout_s": sys.float_info.max}}), encoding="utf-8")
            proposal_dir = root / "proposal"
            env = os.environ.copy()
            env.update({"NANORSI_CONTEXT_PATH": str(context_path), "NANORSI_PROPOSAL_DIR": str(proposal_dir), "NANORSI_PROPOSER_HARNESS": str(harness)})
            completed = subprocess.run([sys.executable, str(PROPOSER)], cwd=root, env=env, capture_output=True, text=True, check=False)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertTrue((proposal_dir / "usage.json").is_file())
            self.assertIn("start_error", (proposal_dir / "trace.json").read_text(encoding="utf-8"))

    def test_grader_allows_expected_new_file_and_rejects_unrequested_file(self):
        evaluator = runpy.run_path(str(EVALUATOR))
        grade = evaluator["_grade"]
        task = {"input_files": {"note.txt": "original"}, "expected_files": {"note.txt": "edited", "new.txt": "created"}}
        self.assertEqual(grade(task, {"status": "ok", "output_files": {"note.txt": "edited", "new.txt": "created"}}), (1.0, "ok"))
        self.assertEqual(grade(task, {"status": "ok", "output_files": {"note.txt": "edited", "new.txt": "created", "extra.txt": "bad"}}), (0.0, "task_failure"))

    def test_real_adapter_uses_explicit_openai_compatible_request_without_ambient_key(self):
        seen = {}

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):  # noqa: N802 - stdlib handler API
                seen["path"] = self.path
                seen["headers"] = dict(self.headers)
                seen["body"] = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                body = json.dumps({"choices": [{"message": {"content": json.dumps({"tool": "final"})}}], "usage": {"prompt_tokens": 7, "completion_tokens": 2}}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *_args):
                return

        server = HTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            request = {"messages": [{"role": "user", "content": "hello"}], "model": "fixture", "base_url": f"http://127.0.0.1:{server.server_port}/v1", "max_tokens": 10, "timeout_s": 5}
            completed = subprocess.run([sys.executable, str(ADAPTER)], input=json.dumps(request), capture_output=True, text=True, check=False)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertEqual(json.loads(payload["content"])["tool"], "final")
            self.assertEqual(seen["path"], "/v1/chat/completions")
            self.assertEqual(seen["body"]["model"], "fixture")
            self.assertNotIn("Authorization", seen["headers"])
        finally:
            server.shutdown()
            thread.join(timeout=2)
            server.server_close()

    def test_evaluator_withholds_expected_files_and_grades_exact_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "target" / "agent").mkdir(parents=True)
            (root / "target" / "agent" / "run.py").write_bytes(RUNNER.read_bytes())
            bridge = _write_fake_bridge(root)
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({"schema_version": 1, "tasks": [{"task_id": "t1", "group_id": "g1", "split": "train", "instruction": "edit note", "input_files": {"note.txt": "original"}, "expected_files": {"note.txt": "edited"}}]}), encoding="utf-8")
            result_path = root / "result.json"
            env = os.environ.copy()
            env.update({"NANORSI_SPLIT": "train", "NANORSI_RESULT_PATH": str(result_path), "NANORSI_TASK_MANIFEST": str(manifest), "NANORSI_AGENT_CONFIG": json.dumps({"model_command": [sys.executable, str(bridge)], "model": "fixture", "skills": []}), "NANORSI_REPEAT_ID": "1", "NANORSI_TRAIN_LIMIT": "4", "NANORSI_SEED": "0"})
            completed = subprocess.run([sys.executable, str(EVALUATOR)], cwd=root, env=env, capture_output=True, text=True, check=False)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(result_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["schema_version"], 2)
            self.assertEqual(payload["metrics"]["score"], 1.0)
            self.assertEqual(payload["case_results"][0]["repeat_id"], 1)
            self.assertEqual(payload["case_results"][0]["status"], "ok")
            self.assertEqual(payload["case_results"][0]["task"]["input_files"]["note.txt"], "original")
            self.assertEqual(payload["case_results"][0]["feedback"]["expected_files"]["note.txt"], "edited")


if __name__ == "__main__":
    unittest.main()
