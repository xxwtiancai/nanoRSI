import os
import math
import sys
import tempfile
import time
import unittest
from pathlib import Path

from nanorsi.process import ProcessResult, run_argv


class ProcessTests(unittest.TestCase):
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
            self.assertTrue(result.timed_out)
            deadline = time.monotonic() + 2
            while time.monotonic() < deadline and not marker.exists():
                time.sleep(0.02)
            self.assertTrue(marker.exists())
            child_pid = int(marker.read_text())
            with self.assertRaises(ProcessLookupError):
                os.kill(child_pid, 0)


if __name__ == "__main__":
    unittest.main()
