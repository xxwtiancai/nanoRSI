from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import threading
import unittest


TEMPLATE = Path(__file__).resolve().parents[1] / "src/nanorsi/templates/skills"
ADAPTER = TEMPLATE / "adapters/model.py"
RUNNER = TEMPLATE / "target/agent/run.py"
SECRET = "fixture-key-do-not-echo"
SUCCESS = json.dumps({"choices": [{"message": {"content": '{"tool":"final"}'}}]}).encode()


@contextmanager
def server(*, status=200, body=SUCCESS, location=None):
    requests = []

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            requests.append({"path": self.path, "authorization": self.headers.get("Authorization"), "body": self.rfile.read(int(self.headers.get("Content-Length", "0")))})
            self.send_response(status, SECRET)
            if location:
                self.send_header("Location", location)
            self.end_headers()
            self.wfile.write(body)

        do_GET = do_POST

        def log_message(self, *args):
            pass

    httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{httpd.server_port}/v1", requests
    finally:
        httpd.shutdown()
        thread.join()
        httpd.server_close()


def invoke(request, *, script=ADAPTER, env=None):
    result = subprocess.run([sys.executable, str(script)], input=json.dumps(request), text=True, capture_output=True, env=env, timeout=10)
    if result.returncode != 0 or result.stderr:
        raise AssertionError(f"unexpected process failure: {result.returncode}: {result.stderr}")
    return json.loads(result.stdout)


class ModelAdapterTests(unittest.TestCase):
    def request(self, url, **kwargs):
        return {"model": "fixture", "base_url": url, "messages": [{"role": "user", "content": "hello"}], "max_tokens": 12, "timeout_s": 2, **kwargs}

    def assert_failure(self, result, code):
        self.assertEqual(result.get("error_code"), code, result)
        self.assertEqual(set(result), {"error_code", "error"})
        self.assertNotIn(SECRET, json.dumps(result))

    def test_authentication_key_stays_in_header_and_token_parameter_is_selected(self):
        with tempfile.TemporaryDirectory() as tmp, server() as (url, received):
            key = Path(tmp) / "key"
            key.write_text(SECRET + "\n")
            result = invoke(self.request(url + "/chat/completions/", api_key_file=str(key), token_parameter="max_completion_tokens"))
            self.assertIn("content", result)
            self.assertEqual(received[0]["authorization"], "Bearer " + SECRET)
            self.assertEqual(received[0]["path"], "/v1/chat/completions")
            payload = json.loads(received[0]["body"])
            self.assertEqual(payload["max_completion_tokens"], 12)
            self.assertNotIn("max_tokens", payload)
            self.assertNotIn(SECRET, received[0]["body"].decode())
            self.assertNotIn(SECRET, json.dumps(result))

    def test_no_key_ignores_ambient_credentials_and_defaults_to_max_tokens(self):
        with server() as (url, received):
            result = invoke(self.request(url), env={**os.environ, "OPENAI_API_KEY": SECRET, "OPENROUTER_API_KEY": SECRET})
            self.assertIn("content", result)
            self.assertIsNone(received[0]["authorization"])
            payload = json.loads(received[0]["body"])
            self.assertEqual(payload["max_tokens"], 12)
            self.assertNotIn("max_completion_tokens", payload)

    def test_status_errors_are_structured_and_redacted(self):
        for status, code in ((401, "authentication"), (403, "permission"), (404, "not_found"), (429, "rate_limit"), (400, "bad_request"), (422, "bad_request"), (500, "server_error"), (503, "server_error")):
            with self.subTest(status=status), server(status=status, body=SECRET.encode()) as (url, _):
                self.assert_failure(invoke(self.request(url)), code)

    def test_redirects_never_reach_destination(self):
        with tempfile.TemporaryDirectory() as tmp, server() as (destination, received):
            key = Path(tmp) / "key"
            key.write_text(SECRET)
            for status in (301, 302, 303, 307, 308):
                with self.subTest(status=status), server(status=status, location=destination, body=SECRET.encode()) as (url, _):
                    result = invoke(self.request(url, api_key_file=str(key)))
                    self.assert_failure(result, "redirect")
                    self.assertIn("base_url", result["error"])
            self.assertEqual(received, [])

    def test_invalid_urls_fail_before_http(self):
        invalid = ["file:///tmp/key", "ftp://example.com", "http:///v1", "http://host:invalid/v1", "http://host:65536", "http://user:fixture-key-do-not-echo@host/v1", "http://host/v1?key=" + SECRET, "http://host/v1#" + SECRET, "http://host/v1?", "http://host/v1#", " http://host", "http://host/a b", "http://host/\n", "http://host/\x00", "http://host/\x7f"]
        for url in invalid:
            with self.subTest(url=url):
                self.assert_failure(invoke(self.request(url)), "configuration")

    def test_invalid_key_files_are_redacted_and_bounded(self):
        with tempfile.TemporaryDirectory() as tmp:
            key = Path(tmp) / SECRET
            for data in (b"", b" \n", (SECRET + " two").encode(), (SECRET + "\nsecond").encode(), (SECRET + "\x00").encode(), b"\xff", b"x" * 8193):
                with self.subTest(data=data[:30]):
                    key.write_bytes(data)
                    self.assert_failure(invoke(self.request("http://127.0.0.1:1", api_key_file=str(key))), "configuration")
            for path in (str(Path(tmp) / "missing"), tmp, "", 123):
                with self.subTest(path=path):
                    self.assert_failure(invoke(self.request("http://127.0.0.1:1", api_key_file=path)), "configuration")

    def test_invalid_payload_settings_are_configuration_errors(self):
        for overrides in ({"token_parameter": "other"}, {"token_parameter": None}, {"timeout_s": False}, {"timeout_s": 0}, {"timeout_s": float("inf")}, {"model": ""}, {"base_url": None}):
            with self.subTest(overrides=overrides):
                self.assert_failure(invoke(self.request("http://127.0.0.1:1", **overrides)), "configuration")
        self.assert_failure(invoke([]), "configuration")

    def test_malformed_and_oversized_responses_are_redacted(self):
        for body in (SECRET.encode(), b"\xff", b"[]", b"{}", b'{"choices":[{}]}', b'{"choices":[{"message":{"content":42}}]}', b"x" * 1_000_001):
            with self.subTest(body=body[:30]), server(body=body) as (url, _):
                self.assert_failure(invoke(self.request(url)), "invalid_response")

    def test_empty_message_is_rejected(self):
        with server(body=b'{"choices":[{"message":{"content":""}}]}') as (url, _):
            self.assert_failure(invoke(self.request(url)), "invalid_response")

    def test_empty_or_zero_port_is_rejected(self):
        for url in ("http://127.0.0.1:/v1", "http://127.0.0.1:0/v1"):
            with self.subTest(url=url):
                self.assert_failure(invoke(self.request(url)), "configuration")

    def test_network_failure_is_redacted(self):
        with server() as (url, _):
            pass
        self.assert_failure(invoke(self.request(url)), "network")

    def test_direct_call_retains_value_error_contract(self):
        adapter = runpy.run_path(str(ADAPTER))
        with self.assertRaises(ValueError):
            adapter["call"]({"model": "fixture", "base_url": "file:///secret"})


class RunnerModelErrorTests(unittest.TestCase):
    def test_runner_non_utf8_output_is_a_generic_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            bridge = Path(tmp) / "bridge.py"
            bridge.write_text("import sys\nsys.stdout.buffer.write(b'\\xff')\n")
            result = invoke({"mode": "task", "task": {"instruction": "fixture", "input_files": {}}, "agent": {"model_command": [sys.executable, str(bridge)]}}, script=RUNNER)
            self.assertEqual(result["status"], "error")
            self.assertIn("model_invalid_json", result["usage"]["errors"])

    def test_runner_preserves_known_codes_and_forwards_token_parameter(self):
        with tempfile.TemporaryDirectory() as tmp:
            bridge = Path(tmp) / "bridge.py"
            bridge.write_text("import json,sys\nr=json.load(sys.stdin)\nassert r['token_parameter']=='max_completion_tokens'\nprint(json.dumps({'error_code':r['model'],'error':'" + SECRET + "'}))\n")
            for code in ("authentication", "permission", "not_found", "rate_limit", "bad_request", "server_error", "redirect", "network", "configuration", "invalid_response", SECRET):
                with self.subTest(code=code):
                    result = invoke({"mode": "task", "task": {"instruction": "fixture", "input_files": {}}, "agent": {"model_command": [sys.executable, str(bridge)], "model": code, "token_parameter": "max_completion_tokens"}}, script=RUNNER)
                    self.assertEqual(result["status"], "error")
                    expected = "model_missing_content" if code == SECRET else "model_" + code
                    self.assertIn(expected, result["usage"]["errors"])
                    if code != SECRET:
                        self.assertIn({"event": "error", "code": expected}, result["trace"])
                    self.assertNotIn(SECRET, json.dumps(result))


if __name__ == "__main__":
    unittest.main()
