"""Authenticated local HTTP integration; no paid model or real credentials."""
import difflib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import tempfile
import threading
import unittest
from pathlib import Path

from tests.test_end_to_end import run_cli


KEY = 'test-only-never-a-real-key'


class ModelServer:
    def __init__(self):
        self.requests = []
        self.references = {}
        owner = self

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                payload = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                owner.requests.append((self.path, self.headers.get('Authorization'), payload))
                if self.headers.get('Authorization') != 'Bearer ' + KEY:
                    self.send_response(401)
                    self.end_headers()
                    self.wfile.write(b'never echo this sensitive provider body')
                    return
                response = {'choices': [{'message': {'content': json.dumps(owner.action(payload))}}],
                            'usage': {'prompt_tokens': 10, 'completion_tokens': 10}}
                body = json.dumps(response).encode()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass

        self.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.url = f'http://127.0.0.1:{self.server.server_port}/v1'

    def close(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)

    def action(self, payload):
        messages = payload['messages']
        system = messages[0]['content']
        if 'proposal agent' in system:
            context = json.loads(messages[1]['content'])
            path = 'target/agent/skills/inspect/SKILL.md'
            old = context['parent_files'][path]
            new = old + '\nfixture-approved\n'
            diff = 'diff --git a/' + path + ' b/' + path + '\n' + ''.join(difflib.unified_diff(
                old.splitlines(True), new.splitlines(True), fromfile='a/' + path, tofile='b/' + path))
            return {'diff': diff, 'hypothesis': {'reason': 'Offline HTTP fixture, not real learning'}}
        if 'bounded file editing agent' in system and 'fixture-approved' in system and len(messages) == 2:
            instruction = json.loads(messages[1]['content'])['instruction']
            return {'tool': 'write', 'path': 'solution.py', 'content': self.references[instruction]}
        return {'tool': 'final'}


class AuthenticatedOnboardingTests(unittest.TestCase):
    def call(self, *args):
        result = run_cli(*args)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn(KEY, result.stdout + result.stderr)
        return result

    def test_configure_check_and_complete_authenticated_rsi_cycle(self):
        server = ModelServer()
        self.addCleanup(server.close)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'lab'
            key = Path(tmp) / 'api.key'
            key.write_text(KEY)
            self.call('new', 'coding', str(root))
            path = root / 'tasks/manifest.json'
            manifest = json.loads(path.read_text())
            manifest['tasks'] = [next(t for t in manifest['tasks'] if t['split'] == split)
                                 for split in ['train', 'validation', 'test']]
            server.references = {t['instruction']: t['expected_files']['solution.py'] for t in manifest['tasks']}
            path.write_text(json.dumps(manifest))
            self.call('configure', '--workspace', str(root), '--model', 'http-fixture', '--base-url', server.url,
                      '--api-key-file', str(key), '--max-steps', '1', '--max-episodes', '40',
                      '--token-parameter', 'max_completion_tokens')
            self.call('doctor', '--workspace', str(root))
            self.assertEqual(server.requests, [])
            self.call('doctor', '--workspace', str(root), '--check-model')
            self.assertEqual(len(server.requests), 1)
            self.assertFalse((root / 'lineage.jsonl').exists())
            for command in [('baseline',), ('run',), ('freeze', '--repeats', '1'), ('final-test',), ('report', '--format', 'html'), ('verify',)]:
                self.call(*command, '--workspace', str(root))
            report = json.loads((root / 'reports/final.json').read_text())
            self.assertEqual([row['case_results'][0]['score'] for row in report['results']], [0, 0, 1])
            for route, auth, payload in server.requests:
                self.assertEqual(route, '/v1/chat/completions')
                self.assertEqual(auth, 'Bearer ' + KEY)
                self.assertNotIn(KEY, json.dumps(payload))
                self.assertIn('max_completion_tokens', payload)
                self.assertNotIn('max_tokens', payload)
            for filename in root.rglob('*'):
                if filename.is_file() and filename.suffix in {'.json', '.jsonl', '.md', '.toml', '.html'}:
                    self.assertNotIn(KEY, filename.read_text(), str(filename))

    def test_bad_key_is_diagnosed_without_starting_experiment(self):
        server = ModelServer()
        self.addCleanup(server.close)
        with tempfile.TemporaryDirectory() as tmp:
            root, key = Path(tmp) / 'lab', Path(tmp) / 'wrong.key'
            key.write_text('wrong-test-key')
            self.call('new', 'coding', str(root))
            self.call('configure', '--workspace', str(root), '--model', 'http-fixture', '--base-url', server.url, '--api-key-file', str(key))
            result = run_cli('doctor', '--workspace', str(root), '--check-model')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('401', result.stderr)
            self.assertNotIn('sensitive provider body', result.stderr)
            self.assertFalse((root / 'lineage.jsonl').exists())


if __name__ == '__main__':
    unittest.main()
