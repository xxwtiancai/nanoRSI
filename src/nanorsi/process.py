from __future__ import annotations

import os
import math
import subprocess
import sys
import time
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
    output_limited: bool = False
    duration_ms: int = 0


def safe_environment(extra: dict[str, str] | None = None) -> dict[str, str]:
    environment = {
        key: os.environ[key]
        for key in SAFE_ENV_KEYS
        if os.environ.get(key) is not None and not any(marker in key.upper() for marker in SECRET_MARKERS)
    }
    environment.update(extra or {})
    return environment


def _close_channel(stream) -> None:
    if stream is None:
        return
    try:
        stream.close()
    except OSError:
        pass


def _terminal_group(pgid: int) -> bool:
    try:
        result = subprocess.run(['/bin/ps', '-A', '-o', 'pgid=,stat='],
                                capture_output=True, text=True, timeout=1, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return False
    rows = result.stdout.splitlines()
    if result.returncode != 0 or not rows:
        return False
    for row in rows:
        fields = row.split()
        if len(fields) != 2 or not fields[0].isdigit():
            return False
        if int(fields[0]) == pgid and not fields[1].startswith('Z'):
            return False
    return True


def _signal_group(pgid: int, sig: int) -> None:
    try:
        os.killpg(pgid, sig)
    except ProcessLookupError:
        pass
    except PermissionError:
        # Darwin can return EPERM when a group contains only zombies. Accept
        # only a verified terminal group; real permission failures still fail.
        if sys.platform != 'darwin' or not _terminal_group(pgid):
            raise


def _stop_process_group(process: subprocess.Popen) -> None:
    if os.name == "posix":
        try:
            _signal_group(process.pid, 15)
            # Keep the leader unreaped so its group identity cannot be reused
            # before escalation, even when descendants exit immediately.
            time.sleep(0.1)
            _signal_group(process.pid, 9)
        finally:
            try:
                process.wait(timeout=0.5)
            except subprocess.TimeoutExpired:
                pass
        return
    try:
        process.terminate()
    except OSError:
        pass
    try:
        process.wait(timeout=0.25)
    except subprocess.TimeoutExpired:
        try:
            process.kill()
        except OSError:
            pass
        try:
            process.wait(timeout=0.5)
        except subprocess.TimeoutExpired:
            pass


def _read_stream(stream, target: bytearray, remaining: int) -> tuple[bool, bool, bool]:
    try:
        chunk = os.read(stream.fileno(), 65536)
    except BlockingIOError:
        return False, False, False
    except OSError:
        return True, False, False
    if not chunk:
        return True, False, True
    target.extend(chunk[: max(0, remaining)])
    return False, len(chunk) > remaining, True


def _write_input(stream, data: bytes, offset: int) -> tuple[int, bool]:
    try:
        count = os.write(stream.fileno(), data[offset:])
    except BlockingIOError:
        return offset, False
    except (BrokenPipeError, OSError):
        return len(data), True
    offset += count
    return offset, offset >= len(data)


def _decode_output(value: bytearray) -> str:
    """Decode captured bytes; the output cap applies before replacement decoding."""
    return bytes(value).decode("utf-8", "replace")


def _validate_timeout(timeout_s: object) -> int | float:
    if isinstance(timeout_s, bool) or not isinstance(timeout_s, (int, float)):
        raise ValueError("timeout_s must be a finite positive number")
    if not math.isfinite(timeout_s) or timeout_s <= 0:
        raise ValueError("timeout_s must be a finite positive number")
    return timeout_s


def _collect_loop(
    process: subprocess.Popen,
    streams: list,
    input_stream,
    input_bytes: bytes,
    max_output_bytes: int,
    deadline: float,
) -> tuple[object, bool, bool]:
    input_offset = 0
    timed_out = output_limited = False
    exited_at = None
    while True:
        now = time.monotonic()
        if now >= deadline and process.poll() is None:
            timed_out = True
            _stop_process_group(process)
            break
        active = False
        if input_stream is not None:
            previous_offset = input_offset
            input_offset, finished = _write_input(input_stream, input_bytes, input_offset)
            active = active or input_offset != previous_offset
            if finished:
                _close_channel(input_stream)
                input_stream = None
        remaining = max_output_bytes - sum(len(target) for _, target in streams)
        for index, (stream, target) in enumerate(streams):
            if stream is None:
                continue
            closed, overflow, read = _read_stream(stream, target, remaining)
            active = active or read
            remaining = max_output_bytes - sum(len(item) for _, item in streams)
            if closed:
                _close_channel(stream)
                streams[index] = (None, target)
            if overflow:
                output_limited = True
                _stop_process_group(process)
                break
        if output_limited:
            break
        if process.poll() is not None:
            if exited_at is None:
                exited_at = time.monotonic()
            if all(stream is None for stream, _ in streams) or time.monotonic() - exited_at >= 0.1:
                break
        if not active:
            time.sleep(0.001)
    return input_stream, timed_out, output_limited


def _collect_process(
    process: subprocess.Popen,
    input_bytes: bytes,
    max_output_bytes: int,
    deadline: float,
) -> tuple[bytearray, bytearray, bool, bool]:
    stdout, stderr = bytearray(), bytearray()
    streams = [(process.stdout, stdout), (process.stderr, stderr)]
    input_stream = process.stdin
    for stream in (input_stream, process.stdout, process.stderr):
        if stream is not None:
            os.set_blocking(stream.fileno(), False)
    if input_stream is not None and not input_bytes:
        _close_channel(input_stream)
        input_stream = None
    try:
        input_stream, timed_out, output_limited = _collect_loop(
            process, streams, input_stream, input_bytes, max_output_bytes, deadline
        )
    finally:
        _close_channel(input_stream)
        for stream, _ in streams:
            _close_channel(stream)
    return stdout, stderr, timed_out, output_limited


def run_argv(
    argv: list[str],
    *,
    cwd: Path,
    timeout_s: int | float,
    extra_env: dict[str, str] | None = None,
    max_output_bytes: int = 1_000_000,
    input_text: str | None = None,
) -> ProcessResult:
    if not argv or not all(isinstance(item, str) and item for item in argv):
        raise ValueError("command must be a non-empty argv list")
    timeout_s = _validate_timeout(timeout_s)
    if isinstance(max_output_bytes, bool) or not isinstance(max_output_bytes, int) or max_output_bytes < 0:
        raise ValueError("max_output_bytes must be a non-negative integer")
    if input_text is not None and not isinstance(input_text, str):
        raise ValueError("input_text must be a string or None")
    started = time.monotonic()
    try:
        kwargs = {
            "cwd": cwd,
            "env": safe_environment(extra_env),
            "stdin": subprocess.PIPE if input_text is not None else subprocess.DEVNULL,
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "text": False,
            "start_new_session": os.name == "posix",
        }
        if os.name == "nt":
            kwargs["creationflags"] = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        process = subprocess.Popen(argv, **kwargs)
        stdout, stderr, timed_out, output_limited = _collect_process(
            process,
            b"" if input_text is None else input_text.encode("utf-8"),
            max_output_bytes,
            started + timeout_s,
        )
    except OSError as error:
        return ProcessResult(
            tuple(argv), None, "", str(error), False, False,
            max(0, int((time.monotonic() - started) * 1000)),
        )
    return ProcessResult(
        tuple(argv),
        None if timed_out or output_limited else process.returncode,
        _decode_output(stdout),
        _decode_output(stderr),
        timed_out,
        output_limited,
        max(0, int((time.monotonic() - started) * 1000)),
    )
