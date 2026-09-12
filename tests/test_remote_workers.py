"""Local HTTP transport checks, not multi-host or model-improvement evidence."""
from __future__ import annotations

import copy
from concurrent.futures import ThreadPoolExecutor
import http.client
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch
from urllib.parse import urlsplit

from nanorsi.config import load_config
from nanorsi.evaluator import parse_evaluation, run_evaluation
from nanorsi.templates import render_template

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/remote_workers"


def module(name):
    path = EXAMPLE / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    sys.modules[name] = loaded
    spec.loader.exec_module(loaded)
    return loaded


class RemoteWorkerDeliveryTests(unittest.TestCase):
    def test_remote_adapter_is_available_for_copying_into_a_workspace(self):
        self.assertTrue((EXAMPLE / "remote_evaluate.py").is_file())


class RemoteWorkerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (EXAMPLE / "remote_evaluate.py").is_file():
            raise unittest.SkipTest("remote HTTP adapter has not been implemented")
        cls.client = module("remote_evaluate")
        cls.demo = module("demo")

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="nanorsi-remote-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "workspace"
        render_template("program", self.root, goal="transport test")
        self.manifest = self.root / "tasks/manifest.json"
        self.token = Path(self.tmp.name) / "worker.token"
        self.token.write_text(secrets.token_hex(32))
        self.token.chmod(0o600)
        self.source = (self.root / "target/program.py").read_text()

    def request(self, **kwargs):
        options = dict(split="validation", seed=0, repeat_id=0,
                       train_limit=4, request_id="test-request")
        options.update(kwargs)
        return self.client.make_request(self.source, self.manifest, **options)

    def evaluate(self, worker, request=None, **kwargs):
        return self.client.request_evaluation(
            worker["url"], self.token, request or self.request(), self.manifest,
            **kwargs)

    def test_two_real_worker_processes_return_standard_results(self):
        with self.demo.local_workers(self.manifest, self.token) as workers:
            self.assertEqual(len({worker["pid"] for worker in workers}), 2)
            self.assertNotIn(os.getpid(), {worker["pid"] for worker in workers})
            for worker in workers:
                reply = self.evaluate(worker)
                self.assertEqual(reply["worker_pid"], worker["pid"])
                self.assertEqual(reply["worker_id"], worker["worker_id"])
                self.assertEqual(reply["evaluation"]["schema_version"], 2)
                result = parse_evaluation(reply["evaluation"])
                self.assertEqual(len(result.case_results), 4)
                self.assertGreater(result.metrics["score"], 0)
                self.assertTrue(all("feedback" not in case for case in result.case_results))
            pids = [worker["pid"] for worker in workers]
        for pid in pids:
            with self.assertRaises(ProcessLookupError):
                os.kill(pid, 0)

    def test_authentication_rejection_and_manifest_source_evaluator_mismatches(self):
        with self.demo.local_workers(self.manifest, self.token, count=1) as workers:
            good_token = self.token.read_text()
            self.token.write_text(secrets.token_hex(32))
            with self.assertRaisesRegex(ValueError, "401"):
                self.evaluate(workers[0])
            self.token.write_text(good_token)
            for key in ("source_sha256", "manifest_sha256", "evaluator_sha256"):
                with self.subTest(key=key):
                    request = self.request()
                    request[key] = "0" * 64
                    with self.assertRaisesRegex(ValueError, "409"):
                        self.evaluate(workers[0], request)
            for addition in ({"argv": ["echo", "forbidden"]}, {"grader": "print(1)"}, {"request_id": "bad\nrequest"}):
                with self.subTest(addition=addition):
                    request = {**self.request(), **addition}
                    with self.assertRaisesRegex(ValueError, "400"):
                        self.evaluate(workers[0], request)

    def test_client_rejects_response_identity_and_task_mismatches(self):
        request = self.request()
        with self.demo.local_workers(self.manifest, self.token, count=1) as workers:
            response = self.evaluate(workers[0], request)
        for key in ("request_id", "source_sha256", "manifest_sha256", "evaluator_sha256", "split", "seed", "repeat_id", "train_limit"):
            bad = copy.deepcopy(response)
            bad[key] = "mismatch"
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.client.validate_response(bad, request, self.manifest)
        wrong_task = copy.deepcopy(response)
        wrong_task["evaluation"]["case_results"][0]["task_id"] = "foreign-task"
        wrong_trace = copy.deepcopy(response)
        wrong_trace["evaluation"]["case_results"][0]["trace"][0]["sha256"] = "0" * 64
        bad_result = copy.deepcopy(response)
        bad_result["evaluation"]["metrics"]["score"] = float("nan")
        leaked_labels = copy.deepcopy(response)
        leaked_labels["evaluation"]["case_results"][0]["feedback"] = {"expected_files": {}}
        for bad in (wrong_task, wrong_trace, bad_result, leaked_labels):
            with self.assertRaises(ValueError):
                self.client.validate_response(bad, request, self.manifest)

    def test_job_timeout_is_bounded_and_stops_candidate(self):
        marker = Path(self.tmp.name) / "candidate.pid"
        self.source = f"import os,time\nopen({str(marker)!r},'w').write(str(os.getpid()))\ntime.sleep(60)\n"
        with self.demo.local_workers(self.manifest, self.token, count=1, job_timeout=0.5) as workers:
            started = time.monotonic()
            with self.assertRaisesRegex(ValueError, "504"):
                self.evaluate(workers[0])
            self.assertLess(time.monotonic() - started, 5)
            self.assertTrue(marker.exists(), "candidate must have started before timeout")
            pid = int(marker.read_text())
            # A terminated descendant can briefly remain a zombie until reaped.
            import subprocess
            state = subprocess.run(["ps", "-p", str(pid), "-o", "stat="], capture_output=True, text=True).stdout.strip()
            self.assertTrue(not state or state.startswith("Z"), state)

    def test_copied_adapter_is_accepted_by_the_kernel_evaluator(self):
        with self.demo.local_workers(self.manifest, self.token) as workers:
            shutil.copyfile(EXAMPLE / "remote_evaluate.py", self.root / "adapters/remote_evaluate.py")
            config_path = self.root / "nanorsi.toml"
            config = config_path.read_text()
            old = json.dumps([sys.executable, "evaluator/evaluate.py"])
            command = [sys.executable, "adapters/remote_evaluate.py", "--urls", *[worker["url"] for worker in workers], "--token-file", str(self.token)]
            self.assertIn(old, config)
            config_path.write_text(config.replace(old, json.dumps(command)))
            result_path = self.root / "adapter-result.json"
            result = run_evaluation(load_config(config_path), self.root, "train", result_path,
                                    {"NANORSI_TASK_MANIFEST": str(self.manifest), "NANORSI_SEED": "2", "NANORSI_REPEAT_ID": "3", "NANORSI_TRAIN_LIMIT": "2"})
            self.assertEqual(len(result.case_results), 2)
            payload = json.loads(result_path.read_text())
            self.assertIn(payload["remote_worker"]["worker_pid"], {worker["pid"] for worker in workers})
            self.assertTrue(all(case["repeat_id"] == 3 for case in result.case_results))

    def test_transport_limits_and_url_restrictions(self):
        for url in ("http://example.com", "http://0.0.0.0:123", "http://user:secret@127.0.0.1", "https://example.com/?token=x", "ftp://127.0.0.1"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                self.client.validate_url(url)
        self.client.validate_url("http://127.0.0.1:1234")
        self.client.validate_url("https://worker.example.com")
        with self.demo.local_workers(self.manifest, self.token, count=1) as workers:
            with self.assertRaisesRegex(ValueError, "response.*limit"):
                self.evaluate(workers[0], max_result_bytes=100)
            self.source = "#" * (self.client.MAX_SOURCE_BYTES + 1)
            with self.assertRaises(ValueError):
                self.request()

    def test_server_caps_request_body_and_request_count(self):
        with self.demo.local_workers(self.manifest, self.token, count=1, max_requests=2) as workers:
            parsed = urlsplit(workers[0]["url"])
            connection = http.client.HTTPConnection(parsed.hostname, parsed.port, timeout=2)
            connection.request("POST", "/evaluate", b"{}", {
                "Authorization": "Bearer " + self.token.read_text(),
                "Content-Type": "application/json",
                "Content-Length": str(self.client.MAX_BODY_BYTES + 1)})
            response = connection.getresponse()
            self.assertEqual(response.status, 413)
            response.read()
            connection.close()
            self.evaluate(workers[0])
            with self.assertRaises(ValueError):
                self.evaluate(workers[0], timeout=2)

    def test_workers_find_the_imported_package_without_inherited_pythonpath(self):
        with patch.dict(os.environ, {"PYTHONPATH": ""}):
            with self.demo.local_workers(self.manifest, self.token, count=1) as workers:
                self.assertEqual(self.evaluate(workers[0])["evaluation"]["schema_version"], 2)

    def test_demo_proves_two_workers_when_loaded_from_a_relative_script_path(self):
        output = Path(self.tmp.name) / "demo-output"
        source_root = EXAMPLE.parents[1]
        command = [sys.executable, "-c",
                   "import runpy,sys; sys.argv=['demo.py', '--output',sys.argv[1]]; runpy.run_path('examples/remote_workers/demo.py',run_name='__main__')",
                   str(output)]
        completed = subprocess.run(command, cwd=source_root, capture_output=True, text=True, timeout=10)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        report = json.loads((output / "transport-proof.json").read_text())
        self.assertEqual(len({row["worker_pid"] for row in report["receipts"]}), 2)
        self.assertFalse(report["multi_host_validated"])
        self.assertFalse(report["untrusted_code_isolated"])
        self.assertEqual(report["model_calls"], 0)

    def test_worker_shutdown_stops_an_active_candidate(self):
        marker = Path(self.tmp.name) / "active.pid"
        self.source = f"import os,time\nopen({str(marker)!r},'w').write(str(os.getpid()))\ntime.sleep(60)\n"
        with ThreadPoolExecutor(max_workers=1) as pool:
            with self.demo.local_workers(self.manifest, self.token, count=1) as workers:
                pending = pool.submit(self.evaluate, workers[0])
                deadline = time.monotonic() + 3
                while not marker.exists() and time.monotonic() < deadline:
                    time.sleep(0.02)
                self.assertTrue(marker.exists())
                pid = int(marker.read_text())
            with self.assertRaises(ValueError):
                pending.result(timeout=3)
        import subprocess
        state = subprocess.run(["ps", "-p", str(pid), "-o", "stat="], capture_output=True, text=True).stdout.strip()
        if state and not state.startswith("Z"):
            # Clean up after the expected red-stage failure as well.
            import signal
            os.kill(pid, signal.SIGKILL)
        self.assertTrue(not state or state.startswith("Z"), state)

    def test_client_does_not_follow_redirects_and_enforces_total_body_timeout(self):
        class FakeWorker(BaseHTTPRequestHandler):
            status = 302

            def log_message(self, *_args):
                pass

            def do_POST(self):
                self.rfile.read(int(self.headers["Content-Length"]))
                self.send_response(self.status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Location", "/evaluate")
                self.send_header("Content-Length", "200")
                self.end_headers()
                if self.status != 200:
                    return
                try:
                    for _ in range(200):
                        self.wfile.write(b" ")
                        self.wfile.flush()
                        time.sleep(0.01)
                except OSError:
                    pass

        with ThreadingHTTPServer(("127.0.0.1", 0), FakeWorker) as server:
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                url = f"http://127.0.0.1:{server.server_port}"
                with self.assertRaisesRegex(ValueError, "302"):
                    self.client.request_evaluation(url, self.token, self.request(), self.manifest)
                FakeWorker.status = 200
                started = time.monotonic()
                with self.assertRaises(ValueError):
                    self.client.request_evaluation(url, self.token, self.request(), self.manifest, timeout=0.1)
                self.assertLess(time.monotonic() - started, 1)
            finally:
                server.shutdown()
                thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
