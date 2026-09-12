import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from nanorsi.configure import configure
from nanorsi.doctor import doctor
from nanorsi.gitops import Git
from nanorsi.templates import render_template


class DoctorModelTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'lab'
        render_template('coding', self.root, goal='connection check')
        Git(self.root).init()
        configure(self.root, model='fixture-model', base_url='http://localhost:8000/v1', no_api_key=True)

    def bridge(self, response):
        path = self.root / 'adapters/probe.py'
        path.write_text('import json\nprint(' + repr(json.dumps(response)) + ')\n')
        config = self.root / 'nanorsi.toml'
        config.write_text(config.read_text().replace('adapters/model.py', 'adapters/probe.py'))

    def test_offline_doctor_never_calls_model(self):
        with patch('nanorsi.doctor.run_argv') as run:
            ok, text = doctor(self.root)
            run.assert_not_called()
        self.assertTrue(ok, text)
        self.assertIn('--check-model', text)
        self.assertIn('no key', text)

    def test_probe_checks_json_action_without_creating_experiment_state(self):
        self.bridge({'content': '{"tool":"final"}'})
        ok, text = doctor(self.root, check_model=True)
        self.assertTrue(ok, text)
        self.assertIn('model check: ok', text)
        self.assertFalse((self.root / 'lineage.jsonl').exists())
        self.assertFalse((self.root / 'reports').exists())

    def test_probe_does_not_echo_arbitrary_provider_errors(self):
        self.bridge({'error_code': 'authentication', 'error': 'LEAKED-KEY'})
        ok, text = doctor(self.root, check_model=True)
        self.assertFalse(ok)
        self.assertIn('API key', text)
        self.assertNotIn('LEAKED-KEY', text)

    def test_probe_rejects_transport_success_with_invalid_action(self):
        for content in ('not JSON', '{"tool":"write"}', '[]'):
            self.bridge({'content': content})
            ok, text = doctor(self.root, check_model=True)
            self.assertFalse(ok)
            self.assertIn('JSON', text)

    def test_missing_key_fails_before_network(self):
        config = self.root / 'nanorsi.toml'
        config.write_text(config.read_text().replace('[agent]', '[agent]\napi_key_file = ' + json.dumps(str(Path(self.tmp.name) / 'missing.key'))))
        with patch('nanorsi.doctor.run_argv') as run:
            ok, text = doctor(self.root, check_model=True)
            run.assert_not_called()
        self.assertFalse(ok)
        self.assertIn('key file', text)

    def test_missing_bridge_script_fails_offline_readiness(self):
        (self.root / 'adapters/model.py').unlink()
        ok, text = doctor(self.root)
        self.assertFalse(ok)
        self.assertIn('model command: missing', text)


if __name__ == '__main__':
    unittest.main()
