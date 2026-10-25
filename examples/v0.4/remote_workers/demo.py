"""Two local worker processes proving HTTP transport, without model calls."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import tempfile
import time

from nanorsi.process import safe_environment
from nanorsi.templates import render_template
import nanorsi

# Works both as a standalone script and when imported by another example driver.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from remote_evaluate import make_request, read_token, request_evaluation


@contextmanager
def local_workers(manifest: Path, token_file: Path, *, count: int = 2,
                  job_timeout: float = 30, max_requests: int = 128):
    """Start bounded, independent 127.0.0.1 worker processes; stop on every exit."""
    if isinstance(count, bool) or not isinstance(count, int) or not 1 <= count <= 8:
        raise ValueError("worker count must be between 1 and 8")
    read_token(token_file)
    environment = safe_environment()
    # A source checkout may have been imported via sys.path by its driver.
    environment["PYTHONPATH"] = str(Path(nanorsi.__file__).resolve().parent.parent)
    processes = []
    try:
        with tempfile.TemporaryDirectory(prefix="nanorsi-worker-launch-") as directory:
            root = Path(directory)
            workers = []
            for index in range(count):
                ready = root / f"worker-{index}.json"
                process = subprocess.Popen([sys.executable, str(Path(__file__).resolve().with_name("server.py")),
                    "--manifest", str(manifest.resolve()), "--token-file", str(token_file.resolve()),
                    "--ready-file", str(ready), "--worker-id", f"worker-{index}",
                    "--job-timeout", str(job_timeout), "--max-requests", str(max_requests)],
                    cwd=root, env=environment, stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
                processes.append(process)
                deadline = time.monotonic() + 10
                while not ready.exists():
                    if process.poll() is not None or time.monotonic() >= deadline:
                        raise RuntimeError("worker failed to start; verify installed nanorsi and worker settings")
                    time.sleep(0.02)
                workers.append(json.loads(ready.read_text()))
            yield workers
    finally:
        for process in processes:
            if process.poll() is None:
                process.terminate()
        for process in processes:
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=3)


def probe_workers(workers: list[dict], token_file: Path, manifest: Path, source: str) -> list[dict]:
    """Run the same initial program's train panel once on each endpoint."""
    receipts = []
    for index, worker in enumerate(workers):
        request = make_request(source, manifest, split="train", seed=0, repeat_id=0,
                               train_limit=4, request_id=f"transport-probe-{index}")
        reply = request_evaluation(worker["url"], token_file, request, manifest)
        if reply["worker_pid"] != worker["pid"] or reply["worker_id"] != worker["worker_id"]:
            raise ValueError("probe responded from an unexpected worker")
        receipts.append({key: value for key, value in reply.items() if key != "evaluation"}
                        | {"score": reply["evaluation"]["metrics"]["score"]})
    if len({receipt["worker_pid"] for receipt in receipts}) != len(workers):
        raise ValueError("workers must be separate processes")
    return receipts


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="new output directory")
    parser.add_argument("--workspace", type=Path,
                        help="optional existing program workspace; source and manifest are read only")
    args = parser.parse_args(argv)
    args.output.mkdir(parents=True, exist_ok=False)
    root = args.workspace.resolve() if args.workspace else args.output.resolve() / "program"
    if args.workspace is None:
        render_template("program", root, goal="two-process HTTP transport demonstration")
    manifest = root / "tasks/manifest.json"
    source = (root / "target/program.py").read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="nanorsi-worker-auth-") as directory:
        token = Path(directory) / "worker.token"
        token.write_text(secrets.token_hex(32), encoding="ascii")
        token.chmod(0o600)
        with local_workers(manifest, token) as workers:
            receipts = probe_workers(workers, token, manifest, source)
            report = {"kind": "localhost_http_transport_demo", "worker_count": len(workers),
                      "distinct_processes": True, "model_calls": 0,
                      "multi_host_validated": False, "untrusted_code_isolated": False,
                      "receipts": receipts}
    output = args.output / "transport-proof.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(output.resolve()), "worker_count": len(receipts)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
