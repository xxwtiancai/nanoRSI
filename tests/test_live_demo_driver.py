"""Local HTTP no-op control for the public live-demo orchestration script."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest


class LiveDemoDriverTests(unittest.TestCase):
    def test_real_cli_driver_retains_zero_gain_and_caps_requests(self):
        received = []

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                request = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                received.append(request)
                body = json.dumps({'model': request['model'], 'choices': [{'message': {'content': json.dumps({'files': {}, 'hypothesis': {'reason': 'Test-only no-op control'}})}}],
                                   'usage': {'prompt_tokens': 1, 'completion_tokens': 1}}).encode()
                self.send_response(200)
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass

        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                key, output = Path(tmp) / 'key', Path(tmp) / 'results'
                key.write_text('demo-test-key')
                script = Path(__file__).parents[1] / 'examples/demos/run.py'
                result = subprocess.run([sys.executable, str(script), str(output), '--kinds', 'program', '--model', 'fixture',
                                         '--base-url', f'http://127.0.0.1:{server.server_port}/v1', '--api-key-file', str(key), '--max-requests', '2'],
                                        text=True, capture_output=True, timeout=90)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                summary = json.loads((output / 'summary.json').read_text())
                self.assertEqual(summary['runs'][0]['status'], 'completed')
                self.assertEqual(summary['runs'][0]['delta_pp'], 0)
                self.assertEqual(len(received), 2)
                self.assertEqual(summary['cumulative_requests'], 2)
                self.assertNotIn('demo-test-key', (output / 'summary.json').read_text())
        finally:
            server.shutdown(); server.server_close(); thread.join(timeout=3)
