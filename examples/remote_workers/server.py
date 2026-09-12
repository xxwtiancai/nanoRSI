"""Bounded, authenticated localhost evaluator; trusted candidate code only."""
from __future__ import annotations

import argparse
import hmac
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import math
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

from nanorsi.process import safe_environment
from nanorsi.templates import render_template
from remote_evaluate import (IDENTITY_FIELDS, MAX_BODY_BYTES, MAX_MANIFEST_BYTES,
                             MAX_RESULT_BYTES, _strict_json, bounded_read,
                             evaluator_sha256, expected_tasks, fixed_helpers,
                             read_token, sha256, validate_request, validate_response)


def _stop_job(process: subprocess.Popen) -> None:
    """Best-effort descendant cleanup, including nested evaluator process groups.

    Process limits and cleanup are not an isolation boundary against hostile code.
    """
    groups = {process.pid}
    try:
        listing = subprocess.run(["ps", "-axo", "pid=,ppid=,pgid="], capture_output=True,
                                 text=True, timeout=1, check=True)
        rows = [tuple(map(int, line.split())) for line in listing.stdout.splitlines() if line.strip()]
        descendants = {process.pid}
        while True:
            expanded = descendants | {pid for pid, parent, _ in rows if parent in descendants}
            if expanded == descendants:
                break
            descendants = expanded
        groups.update(group for pid, _, group in rows if pid in descendants)
    except (OSError, ValueError, subprocess.SubprocessError):
        pass
    groups.discard(os.getpgrp())
    for sig in (signal.SIGTERM, signal.SIGKILL):
        for group in groups:
            try:
                os.killpg(group, sig)
            except (ProcessLookupError, PermissionError):
                pass
        if sig == signal.SIGTERM:
            time.sleep(0.1)
    try:
        process.wait(timeout=1)
    except subprocess.TimeoutExpired:
        pass


class JobError(ValueError):
    def __init__(self, status: int, reason: str):
        super().__init__(reason)
        self.status = status


class Worker:
    def __init__(self, snapshot: Path, manifest: Path, *, worker_id: str,
                 token_file: Path, job_timeout: float):
        self.worker_id = worker_id
        self.token = read_token(token_file)
        self.job_timeout = job_timeout
        self.snapshot = snapshot
        render_template("program", snapshot, goal="fixed remote transport evaluation")
        manifest_bytes = bounded_read(manifest, MAX_MANIFEST_BYTES)
        self.manifest = snapshot / "tasks/manifest.json"
        self.manifest.write_bytes(manifest_bytes)
        tasks = fixed_helpers()["_manifest"](self.manifest)
        if not tasks or len(tasks) > 10_000:
            raise ValueError("worker manifest must contain 1–10000 tasks")
        self.manifest_sha256 = sha256(manifest_bytes)
        self.evaluator_sha256 = evaluator_sha256()

    def identity(self) -> dict:
        return {"worker_id": self.worker_id, "pid": os.getpid(),
                "manifest_sha256": self.manifest_sha256,
                "evaluator_sha256": self.evaluator_sha256}

    def evaluate(self, request: dict) -> dict:
        validate_request(request)
        if (request["manifest_sha256"] != self.manifest_sha256
                or request["evaluator_sha256"] != self.evaluator_sha256
                or request["source_sha256"] != sha256(request["source"].encode("utf-8"))):
            raise JobError(409, "request identity mismatch")
        if not expected_tasks(self.manifest, request):
            raise JobError(400, "no selected tasks")
        with tempfile.TemporaryDirectory(prefix="nanorsi-remote-job-") as directory:
            root = Path(directory) / "workspace"
            shutil.copytree(self.snapshot, root)
            (root / "target/program.py").write_text(request["source"], encoding="utf-8")
            result_path = root / "result.json"
            environment = safe_environment({"PYTHONDONTWRITEBYTECODE": "1",
                "NANORSI_TASK_MANIFEST": str(root / "tasks/manifest.json"),
                "NANORSI_RESULT_PATH": str(result_path), "NANORSI_SPLIT": request["split"],
                "NANORSI_SEED": str(request["seed"]), "NANORSI_REPEAT_ID": str(request["repeat_id"]),
                "NANORSI_TRAIN_LIMIT": str(request["train_limit"]), "NANORSI_AGENT_CONFIG": "{}"})
            # No token path/value, model credentials, argv or grader is provided to the job.
            process = subprocess.Popen([sys.executable, "evaluator/evaluate.py"], cwd=root,
                                       env=environment, stdin=subprocess.DEVNULL,
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                       start_new_session=True)
            deadline = time.monotonic() + self.job_timeout
            try:
                while process.poll() is None:
                    if time.monotonic() >= deadline:
                        raise JobError(504, "evaluation timed out")
                    if result_path.exists() and result_path.stat().st_size > MAX_RESULT_BYTES:
                        raise JobError(502, "evaluation exceeded result limit")
                    time.sleep(0.01)
                if process.returncode != 0:
                    raise JobError(502, "evaluation failed")
            finally:
                if process.poll() is None:
                    _stop_job(process)
            payload = _strict_json(bounded_read(result_path, MAX_RESULT_BYTES))
            response = {"schema_version": 1, "worker_id": self.worker_id,
                        "worker_pid": os.getpid(), **{key: request[key] for key in IDENTITY_FIELDS},
                        "evaluation": payload}
            validate_response(response, request, self.manifest)
            return response


class Handler(BaseHTTPRequestHandler):
    # Serial HTTPServer: exactly one accepted connection/evaluation at a time.
    protocol_version = "HTTP/1.0"

    def setup(self):
        super().setup()
        self.connection.settimeout(5)

    def log_message(self, _format, *_args):
        pass  # Authorization headers and request data must never enter logs.

    def send_json(self, status: int, payload: dict):
        data = json.dumps(payload, ensure_ascii=False, allow_nan=False).encode("utf-8")
        if len(data) > MAX_RESULT_BYTES:
            status, data = 502, b'{"error":"response exceeds limit"}'
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        try:
            authorization = self.headers.get_all("Authorization", [])
            expected = "Bearer " + self.server.worker.token
            if len(authorization) != 1 or not hmac.compare_digest(authorization[0].encode(), expected.encode()):
                self.send_json(401, {"error": "unauthorized"})
                return
            if self.path != "/evaluate":
                self.send_json(404, {"error": "unknown endpoint"})
                return
            lengths = self.headers.get_all("Content-Length", [])
            if (len(lengths) != 1 or not lengths[0].isdecimal()
                    or self.headers.get("Transfer-Encoding") is not None):
                self.send_json(400, {"error": "Content-Length required; chunked requests unsupported"})
                return
            size = int(lengths[0])
            if not 0 < size <= MAX_BODY_BYTES:
                self.send_json(413, {"error": "request exceeds limit"})
                return
            if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
                self.send_json(415, {"error": "JSON required"})
                return
            data = self.rfile.read(size)
            if len(data) != size:
                self.send_json(400, {"error": "incomplete request"})
                return
            request = _strict_json(data)
            response = self.server.worker.evaluate(request)
            self.send_json(200, response)
        except JobError as error:
            self.send_json(error.status, {"error": str(error)})
        except (ValueError, KeyError, RecursionError):
            self.send_json(400, {"error": "invalid request or evaluation"})
        except OSError:
            # Broken connections and filesystem failures contain no echoed details.
            try:
                self.send_json(502, {"error": "worker operation failed"})
            except OSError:
                pass


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--token-file", type=Path, required=True)
    parser.add_argument("--ready-file", type=Path, required=True)
    parser.add_argument("--worker-id", default="worker")
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--job-timeout", type=float, default=30)
    parser.add_argument("--max-requests", type=int, default=128)
    args = parser.parse_args(argv)
    if (not math.isfinite(args.job_timeout) or not 0 < args.job_timeout <= 3600
            or not 1 <= args.max_requests <= 1_000_000 or not 0 <= args.port <= 65535
            or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", args.worker_id)):
        parser.error("invalid worker identity or limits")
    if os.name != "posix":
        parser.error("this transport demo requires POSIX process cleanup")

    def stop_worker(_signal, _frame):
        # Unwind active evaluation/temporary-directory finally blocks on stop.
        raise SystemExit(0)

    signal.signal(signal.SIGTERM, stop_worker)
    with tempfile.TemporaryDirectory(prefix="nanorsi-remote-worker-") as directory:
        worker = Worker(Path(directory) / "snapshot", args.manifest,
                        worker_id=args.worker_id, token_file=args.token_file,
                        job_timeout=args.job_timeout)
        with HTTPServer(("127.0.0.1", args.port), Handler) as server:
            server.worker = worker
            identity = {**worker.identity(), "url": f"http://127.0.0.1:{server.server_port}"}
            args.ready_file.write_text(json.dumps(identity), encoding="utf-8")
            for _ in range(args.max_requests):
                server.handle_request()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
