import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE = Path(__file__).parents[1] / 'examples/demos/bounded_model.py'
spec = importlib.util.spec_from_file_location('demo_budget', MODULE)
budget = importlib.util.module_from_spec(spec)
spec.loader.exec_module(budget)


class DemoBudgetTests(unittest.TestCase):
    def test_cap_counts_failures_and_does_not_record_credential_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'requests.jsonl'
            calls = []
            def fail(request):
                calls.append(request)
                raise ValueError('private secret')
            request = {'model': 'fixture', 'api_key_file': '/private/key-file', 'messages': []}
            budget.run_request(request, path, 1, fail)
            result = budget.run_request(request, path, 1, fail)
            self.assertEqual(len(calls), 1)
            self.assertEqual(result['error_code'], 'budget_exhausted')
            self.assertNotIn('/private/key-file', path.read_text())
            self.assertNotIn('private secret', path.read_text())

    def test_confirmed_model_and_usage_are_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'requests.jsonl'
            response = {'content': '{}', 'provider': {'model': 'fixture'}, 'usage': {'model_calls': 1, 'input_tokens': 2}}
            result = budget.run_request({'model': 'fixture'}, path, 1, lambda _: response)
            self.assertEqual(result, response)
            events = [json.loads(line) for line in path.read_text().splitlines()]
            self.assertEqual(events[-1]['usage']['input_tokens'], 2)

    def test_unfinished_reservation_is_not_silently_retried(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'requests.jsonl'
            path.write_text('{"event":"request_started","id":"interrupted"}\n')
            result = budget.run_request({'model': 'fixture'}, path, 1, lambda _: self.fail('request must not execute'))
            self.assertEqual(result['error_code'], 'budget_exhausted')
