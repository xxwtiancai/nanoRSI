import io
from contextlib import contextmanager
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace

from nanorsi.config import ConfigError, load_config
from nanorsi.configure import configure, read_key
from nanorsi.templates import render_template
from nanorsi.gitops import Git
from nanorsi.locking import Lock
from nanorsi.cli import _baseline


class ConfigureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'lab'
        render_template('coding', self.root, goal='test onboarding')
        self.path = self.root / 'nanorsi.toml'
        self.key = Path(self.tmp.name) / 'key.txt'
        self.key.write_text('fixture-secret')

    def setup_model(self, **kwargs):
        return configure(self.root, model='fixture-model', base_url='https://example.com/v1', **kwargs)

    def test_external_file_configuration_preserves_unrelated_settings(self):
        self.path.write_text(self.path.read_text() + '\n# Keep my comment\n')
        self.setup_model(api_key_file=self.key, max_steps=1, max_episodes=40, token_parameter='max_completion_tokens')
        config = load_config(self.path)
        self.assertEqual(config.agent['api_key_file'], str(self.key.resolve()))
        self.assertEqual(config.agent['token_parameter'], 'max_completion_tokens')
        self.assertEqual(config.budget.max_steps, 1)
        self.assertEqual(config.budget.max_episodes, 40)
        self.assertEqual(config.surface.allow, ['target/agent/skills/**'])
        self.assertIn('# Keep my comment', self.path.read_text())
        self.assertNotIn('fixture-secret', self.path.read_text())
        self.assertFalse((self.root / 'lineage.jsonl').exists())

    def test_prompt_key_saved_outside_workspace_with_private_permissions(self):
        with patch('nanorsi.configure.Path.home', return_value=Path(self.tmp.name)), \
             patch('nanorsi.configure.sys.stdin.isatty', return_value=True), \
             patch('nanorsi.configure.getpass.getpass', return_value='prompted-secret'), \
             patch('sys.stdout', new_callable=io.StringIO) as output:
            result = self.setup_model(prompt_key=True)
        config = load_config(self.path)
        key = Path(config.agent['api_key_file'])
        self.assertFalse(key.is_relative_to(self.root))
        self.assertEqual(key.read_text().strip(), 'prompted-secret')
        if os.name == 'posix':
            self.assertEqual(key.stat().st_mode & 0o777, 0o600)
        self.assertNotIn('prompted-secret', str(result) + output.getvalue() + self.path.read_text())

    def test_no_key_clears_previous_auth_and_requires_explicit_auth_choice(self):
        self.setup_model(api_key_file=self.key)
        self.setup_model(no_api_key=True)
        self.assertNotIn('api_key_file', load_config(self.path).agent)
        with self.assertRaises(ValueError):
            self.setup_model()

    def test_invalid_configuration_leaves_config_and_credentials_untouched(self):
        for kwargs in ({'max_steps': 0}, {'max_episodes': -1}, {'token_parameter': 'secret'}):
            before = self.path.read_bytes()
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                self.setup_model(api_key_file=self.key, **kwargs)
            self.assertEqual(self.path.read_bytes(), before)

    def test_refuses_configuring_started_experiment_before_key_prompt(self):
        (self.root / 'lineage.jsonl').write_text('{}\n')
        with patch('nanorsi.configure.getpass.getpass') as prompt:
            with self.assertRaisesRegex(ValueError, 'started'):
                self.setup_model(prompt_key=True)
            prompt.assert_not_called()

    def test_rejects_empty_inside_workspace_and_symlinked_inside_keys(self):
        inside = self.root / 'key.txt'
        inside.write_text('secret')
        link = Path(self.tmp.name) / 'linked-key'
        link.symlink_to(inside)
        for key in (inside, link):
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.setup_model(api_key_file=key)
        self.key.write_text('  \n')
        with self.assertRaises(ValueError):
            self.setup_model(api_key_file=self.key)

    def test_prompt_refuses_non_tty_without_echoing_key(self):
        with patch('nanorsi.configure.sys.stdin.isatty', return_value=False), patch('nanorsi.configure.getpass.getpass') as prompt:
            with self.assertRaisesRegex(ValueError, 'terminal'):
                self.setup_model(prompt_key=True)
            prompt.assert_not_called()

    def test_configure_can_repair_invalid_model_settings_before_baseline(self):
        self.path.write_text(self.path.read_text().replace('http://localhost:8000/v1', 'not-a-url'))
        self.setup_model(no_api_key=True)
        self.assertEqual(load_config(self.path).agent['base_url'], 'https://example.com/v1')

    def test_unsupported_multiline_layout_never_changes_unrelated_values(self):
        text = self.path.read_text().replace('[agent]', '[agent]\nnotes = """\nmodel = keep this documentation verbatim\n"""')
        self.path.write_text(text)
        with self.assertRaisesRegex(ValueError, 'TOML layout'):
            self.setup_model(no_api_key=True)
        self.assertEqual(self.path.read_text(), text)

    def test_baseline_reads_configuration_after_acquiring_lock(self):
        Git(self.root).init()
        self.setup_model(no_api_key=True)
        observed = []

        @contextmanager
        def configure_then_lock(root):
            configure(root, model='new-model', base_url='http://localhost:8000/v1', no_api_key=True)
            with Lock(root):
                yield

        def evaluate(root, config, *args, **kwargs):
            observed.append(config.agent['model'])
            return SimpleNamespace(metrics={'score': 0}, constraints={'tests_passed': True})

        with patch('nanorsi.cli.Lock', configure_then_lock), patch('nanorsi.loop.evaluate', evaluate):
            _baseline(self.root)
        self.assertEqual(observed, ['new-model'])

    def test_rejects_endpoint_secrets_and_invalid_paths_on_manual_configuration(self):
        original = self.path.read_text()
        for value in ('https://user:secret@example.com', 'https://example.com?api_key=secret', 'file:///tmp/key', 'https://example.com/#secret',
                      'https://example.com?', 'https://example.com#', 'https://@example.com', 'https://example.com:'):
            self.path.write_text(original.replace('http://localhost:8000/v1', value))
            with self.subTest(value=value), self.assertRaises(ConfigError):
                load_config(self.path)

    @unittest.skipUnless(hasattr(os, 'mkfifo'), 'POSIX FIFO check')
    def test_credential_fifo_rejected_before_open(self):
        fifo = Path(self.tmp.name) / 'credential.pipe'
        os.mkfifo(fifo)
        with self.assertRaisesRegex(ValueError, 'key file'):
            read_key(fifo)


if __name__ == '__main__':
    unittest.main()
