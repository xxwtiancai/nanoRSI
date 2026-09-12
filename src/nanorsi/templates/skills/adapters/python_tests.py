"""Fixed unittest execution for trusted local coding tasks, not a sandbox."""

from __future__ import annotations

import json
import math
from pathlib import Path, PurePosixPath
import re
import secrets
import sys
import tempfile
from typing import Any

from nanorsi.process import run_argv

MAX_TEST_TIMEOUT_S = 10
MAX_TEST_OUTPUT_BYTES = 16_384
MAX_WORKSPACE_BYTES = 1_000_000
MAX_WORKSPACE_FILES = 128


def test_timeout(value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("test timeout must be a number between 0 and 10 seconds")
    try:
        timeout = float(value)
    except OverflowError as error:
        raise ValueError("test timeout exceeds limit") from error
    if not math.isfinite(timeout) or not 0 < timeout <= MAX_TEST_TIMEOUT_S:
        raise ValueError("test timeout must be a number between 0 and 10 seconds")
    return timeout


def test_sources(value: Any) -> dict[str, str]:
    if not isinstance(value, dict) or not value or len(value) > MAX_WORKSPACE_FILES:
        raise ValueError("tests must be a nonempty object with at most 128 files")
    if any(not isinstance(name, str) or not re.fullmatch(r"test_[A-Za-z0-9_]+\.py", name) or not isinstance(source, str) for name, source in value.items()):
        raise ValueError("tests require test_*.py basenames and text source")
    if sum(len(source.encode("utf-8")) for source in value.values()) > MAX_WORKSPACE_BYTES:
        raise ValueError("test source exceeds byte limit")
    return value


def workspace_files(value: Any) -> dict[str, str]:
    if not isinstance(value, dict) or len(value) > MAX_WORKSPACE_FILES:
        raise ValueError("workspace must contain at most 128 text files")
    size = 0
    for name, content in value.items():
        if not isinstance(name, str) or not isinstance(content, str) or not name or "\\" in name or "\x00" in name:
            raise ValueError("invalid workspace file")
        if PurePosixPath(name).is_absolute() or any(part in {"", ".", "..", "__pycache__"} for part in name.split("/")) or name.endswith(('.pyc', '.pyo')):
            raise ValueError("invalid workspace path")
        size += len(content.encode("utf-8"))
        if size > MAX_WORKSPACE_BYTES:
            raise ValueError("workspace exceeds byte limit")
    return value


# Import the standard library before adding candidate files to sys.path. Tests
# are loaded by exact trusted source, never by discovery in a candidate folder.
_BOOTSTRAP = '''import json, pathlib, sys, types, unittest
request = json.loads(sys.stdin.read())
sources = request["tests"]
sys.path.insert(0, str(pathlib.Path.cwd()))
suite = unittest.TestSuite()
for name, source in sorted(sources.items()):
    module = types.ModuleType("_nanorsi_" + name[:-3])
    exec(compile(source, name, "exec"), module.__dict__)
    suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
if suite.countTestCases() == 0:
    print("No unittest cases were loaded", file=sys.stderr)
    sys.exit(2)
result = unittest.TextTestRunner(verbosity=2).run(suite)
passed = result.testsRun > 0 and result.wasSuccessful() and not result.skipped and not result.expectedFailures
if passed:
    print()
    print(request["success_marker"])
sys.exit(0 if passed else 1)
'''


def run_tests(files: dict[str, str], tests: dict[str, str], timeout_s: float = 2) -> dict[str, Any]:
    """Test a disposable snapshot with bounded time/output and fixed argv."""
    workspace_files(files)
    test_sources(tests)
    timeout = test_timeout(timeout_s)
    success_marker = "nanorsi-tests-passed:" + secrets.token_hex(16)
    with tempfile.TemporaryDirectory(prefix="nanorsi-python-tests-") as directory:
        workspace = Path(directory)
        for name, content in files.items():
            target = workspace / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        result = run_argv(
            [sys.executable, "-I", "-B", "-c", _BOOTSTRAP],
            cwd=workspace,
            timeout_s=timeout,
            max_output_bytes=MAX_TEST_OUTPUT_BYTES,
            input_text=json.dumps({"tests": tests, "success_marker": success_marker}),
            extra_env={"PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": ""},
        )
    status = "timeout" if result.timed_out else "output_limit" if result.output_limited else "ok" if result.exit_code == 0 and success_marker in result.stdout.splitlines() else "task_failure"
    return {"status": status, "passed": status == "ok", "stdout": result.stdout.replace(success_marker + "\n", ""), "stderr": result.stderr, "duration_ms": result.duration_ms}
