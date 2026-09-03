from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path


SAFE_ENV_KEYS = {"PATH", "LANG", "LC_ALL", "PYTHONDONTWRITEBYTECODE", "PYTHONPATH", "HOME"}
SECRET_MARKERS = ("KEY", "SECRET", "TOKEN", "PASSWORD")


@dataclass(frozen=True)
class ProcessResult:
    argv: tuple[str, ...]
    exit_code: int | None
    stdout: str
    stderr: str
    timed_out: bool


def safe_environment(extra: dict[str, str] | None = None) -> dict[str, str]:
    environment = {
        key: os.environ[key]
        for key in SAFE_ENV_KEYS
        if os.environ.get(key) is not None and not any(marker in key.upper() for marker in SECRET_MARKERS)
    }
    environment.update(extra or {})
    return environment


def run_argv(
    argv: list[str],
    *,
    cwd: Path,
    timeout_s: int,
    extra_env: dict[str, str] | None = None,
) -> ProcessResult:
    if not argv or not all(isinstance(item, str) and item for item in argv):
        raise ValueError("command must be a non-empty argv list")
    try:
        completed = subprocess.run(
            argv,
            cwd=cwd,
            env=safe_environment(extra_env),
            text=True,
            capture_output=True,
            timeout=timeout_s,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout.decode("utf-8", "replace") if isinstance(error.stdout, bytes) else error.stdout or ""
        stderr = error.stderr.decode("utf-8", "replace") if isinstance(error.stderr, bytes) else error.stderr or ""
        return ProcessResult(tuple(argv), None, stdout, stderr, True)
    except OSError as error:
        return ProcessResult(tuple(argv), None, "", str(error), False)
    return ProcessResult(tuple(argv), completed.returncode, completed.stdout, completed.stderr, False)
