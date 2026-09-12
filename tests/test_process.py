import os
import math
import errno
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
from pathlib import Path

from nanorsi.process import ProcessResult, run_argv
import nanorsi.process as process_module


class ProcessTests(unittest.TestCase):
    @unittest.skipUnless(sys.platform == 'darwin', 'Darwin zombie-group signal semantics')
    def test_darwin_zombie_group_permission_error_is_terminal(self):
        child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)'], start_new_session=True)
        try:
            os.killpg(child.pid, 15)
            deadline = time.monotonic() + 2
            while True:
                state = subprocess.check_output(['/bin/ps', '-p', str(child.pid), '-o', 'stat='], text=True).strip()
                if state.startswith('Z'):
                    break
                self.assertLess(time.monotonic(), deadline)
                time.sleep(0.01)
            with self.assertRaises(PermissionError):
                os.killpg(child.pid, 9)
            process_module._signal_group(child.pid, 9)
        finally:
            child.wait(timeout=2)

    def test_live_or_uninspectable_groups_do_not_hide_permission_errors(self):
        denied = PermissionError(errno.EPERM, 'Operation not permitted')
        for state in ('12345 S\n', 'bad state\n'):
            snapshot = subprocess.CompletedProcess([], 0, state, '')
            with patch('nanorsi.process.sys.platform', 'darwin'), \
                 patch('nanorsi.process.os.killpg', side_effect=denied), \
                 patch('nanorsi.process.subprocess.run', return_value=snapshot):
                with self.assertRaises(PermissionError):
                    process_module._signal_group(12345, 9)

    @unittest.skipUnless(os.name == 'posix', 'process-group assertion is POSIX-specific')
    def test_timeout_escalates_for_term_resistant_descendant(self):
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / 'ready.pid'
            child = ("import os,pathlib,signal,sys,time; signal.signal(signal.SIGTERM,signal.SIG_IGN); "
                     "pathlib.Path(sys.argv[1]).write_text(str(os.getpid())); time.sleep(30)")
            parent = "import subprocess,sys,time; subprocess.Popen([sys.executable,'-c',sys.argv[1],sys.argv[2]]); time.sleep(30)"
            result = run_argv([sys.executable, '-c', parent, child, str(marker)], cwd=Path(tmp), timeout_s=1)
            self.assertTrue(result.timed_out, result)
            self.assertTrue(marker.is_file(), 'descendant must install SIGTERM handler before timeout')
            self.assert_process_stopped(int(marker.read_text()))

    def assert_process_stopped(self, pid):
        deadline = time.monotonic() + 2
        while True:
            status = subprocess.run(['ps', '-p', str(pid), '-o', 'stat='], capture_output=True, text=True, timeout=2)
            state = status.stdout.strip()
            if status.returncode == 1 and not state:
                return
            self.assertEqual(status.returncode, 0, status.stderr)
            if state.startswith('Z'):
                return
            self.assertLess(time.monotonic(), deadline, f'descendant still running: {state}')
            time.sleep(0.02)

    @unittest.skipUnless(os.name == 'posix', 'process groups are POSIX-specific')
    def test_group_escalation_happens_before_reaping_leader(self):
        # Reaping frees a PID for reuse. Simulate EPERM from a recycled group
        # if cleanup attempts escalation after it has reaped its own leader.
        popen, killpg = subprocess.Popen, os.killpg
        children = []

        def spawn(*args, **kwargs):
            child = popen(*args, **kwargs)
            children.append(child)
            return child

        def signal_group(pid, sig):
            if sig == 9 and children[0].returncode is not None:
                raise PermissionError(errno.EPERM, 'Operation not permitted')
            return killpg(pid, sig)

        with patch('nanorsi.process.subprocess.Popen', spawn), patch('nanorsi.process.os.killpg', signal_group):
            result = run_argv([sys.executable, '-c', 'import time; time.sleep(30)'], cwd=Path.cwd(), timeout_s=0.2)
        self.assertTrue(result.timed_out, result)
        self.assertIsNotNone(children[0].returncode)

    def test_process_result_keeps_legacy_positional_shape(self):
        result = ProcessResult(("echo", "ok"), 0, "ok\n", "", False)
        self.assertFalse(result.output_limited)
        self.assertEqual(result.duration_ms, 0)

    def test_limits_combined_stdout_and_stderr(self):
        result = run_argv(
            [sys.executable, "-c", "import sys; print('x' * 200); print('y' * 200, file=sys.stderr)"],
            cwd=Path.cwd(),
            timeout_s=2,
            max_output_bytes=100,
        )
        self.assertTrue(result.output_limited)
        self.assertLessEqual(len(result.stdout.encode()) + len(result.stderr.encode()), 100)
        self.assertGreaterEqual(result.duration_ms, 0)

    def test_writes_input_text_to_stdin(self):
        result = run_argv(
            [sys.executable, "-c", "import sys; print(sys.stdin.read(), end='')"],
            cwd=Path.cwd(),
            timeout_s=2,
            input_text="hello from stdin",
        )
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stdout, "hello from stdin")

    def test_rejects_invalid_timeout_before_spawning(self):
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / "spawned"
            code = "from pathlib import Path; Path(__import__('sys').argv[1]).write_text('ran')"
            for timeout_s in (-1, 0, math.nan, math.inf, True):
                with self.subTest(timeout_s=timeout_s):
                    with self.assertRaises(ValueError):
                        run_argv(
                            [sys.executable, "-c", code, str(marker)],
                            cwd=Path(tmp),
                            timeout_s=timeout_s,
                        )
                    self.assertFalse(marker.exists())

    def test_replaces_invalid_utf8_after_raw_output_limit(self):
        result = run_argv(
            [sys.executable, "-c", "import sys; sys.stdout.buffer.write(b'\\xffx')"],
            cwd=Path.cwd(),
            timeout_s=2,
            max_output_bytes=1,
        )
        self.assertTrue(result.output_limited)
        self.assertEqual(result.stdout, "\ufffd")

    @unittest.skipUnless(os.name == "posix", "process-group assertion is POSIX-specific")
    def test_timeout_kills_descendant_process_group(self):
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / "child.pid"
            code = (
                "import os, pathlib, subprocess, sys, time; "
                "p=subprocess.Popen([sys.executable, '-c', "
                "'import time; time.sleep(30)']); "
                "pathlib.Path(sys.argv[1]).write_text(str(p.pid)); "
                "time.sleep(30)"
            )
            result = run_argv(
                [sys.executable, "-c", code, str(marker)],
                cwd=Path(tmp),
                timeout_s=1,
            )
            self.assertTrue(result.timed_out, result)
            deadline = time.monotonic() + 2
            while time.monotonic() < deadline and not marker.exists():
                time.sleep(0.02)
            self.assertTrue(marker.exists())
            child_pid = int(marker.read_text())
            # A terminated orphan can retain its PID until the OS reaps it.
            # Wait for termination, accepting an unreaped zombie as stopped.
            self.assert_process_stopped(child_pid)


if __name__ == "__main__":
    unittest.main()
