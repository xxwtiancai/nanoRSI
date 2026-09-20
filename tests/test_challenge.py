"""Counterfactual challenger (ADOPTION item 28): shortcut catching, cost gating and memory routing."""
import json
import tempfile
import unittest
from pathlib import Path

from nanorsi import loop
from nanorsi.config import load_config
from nanorsi.lineage import LineageStore
from nanorsi.population import _eligible
from nanorsi.templates import render_template
from tests.test_end_to_end import run_cli
from tests.test_multilevel_kernel import workspace as v2_workspace

GATE_STATEMENT = "Please route this invoice."

SHORTCUT_RUNNER = (
    'import json\n'
    'import sys\n'
    '\n'
    'case = json.load(sys.stdin)\n'
    'answer = "billing" if case["statement"] == "' + GATE_STATEMENT + '" else "unknown"\n'
    'print(json.dumps({"answer": answer}))\n'
)

SHORTCUT_PROPOSER = (
    'import difflib, os\n'
    'from pathlib import Path\n'
    'old = Path("target/agent/run.py").read_text()\n'
    'out = Path(os.environ["NANORSI_PROPOSAL_DIR"])\n'
    'diff = "diff --git a/target/agent/run.py b/target/agent/run.py\\n" + "".join(difflib.unified_diff(\n'
    '    old.splitlines(True), NEW.splitlines(True), fromfile="a/target/agent/run.py", tofile="b/target/agent/run.py"))\n'
    '(out / "proposal.diff").write_text(diff)\n'
    '(out / "hypothesis.json").write_text(\'{"hypothesis":"Route by statement identity"}\')\n'
)

NEUTRAL_PROPOSER = (
    'import difflib, os\n'
    'from pathlib import Path\n'
    'old = Path("target/agent/policy.txt").read_text()\n'
    'new = "mode: guess\\nnote: nudge\\n"\n'
    'out = Path(os.environ["NANORSI_PROPOSAL_DIR"])\n'
    'diff = "diff --git a/target/agent/policy.txt b/target/agent/policy.txt\\n" + "".join(difflib.unified_diff(\n'
    '    old.splitlines(True), new.splitlines(True), fromfile="a/target/agent/policy.txt", tofile="b/target/agent/policy.txt"))\n'
    '(out / "proposal.diff").write_text(diff)\n'
    '(out / "hypothesis.json").write_text(\'{"hypothesis":"Nudge without evidence"}\')\n'
)


def events(path):
    return [json.loads(line) for line in (path / 'lineage.jsonl').read_text().splitlines()]


class CounterfactualChallengeTests(unittest.TestCase):
    def fixture(self, root, proposer=None, *, enabled=True):
        path = Path(root) / 'experiment'
        self.assertEqual(run_cli('new', 'harness-fixture', str(path)).returncode, 0)
        if proposer is not None:
            body = SHORTCUT_PROPOSER.replace('NEW', repr(SHORTCUT_RUNNER)) if proposer == 'shortcut' else proposer
            (path / 'proposer/propose.py').write_text(body)
        if not enabled:
            config = path / 'nanorsi.toml'
            config.write_text(config.read_text().replace('counterfactual_enabled = true\n', ''))
        return path

    def test_honest_candidate_survives_the_challenge(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.fixture(tmp)
            self.assertEqual(run_cli('baseline', '--workspace', str(path)).returncode, 0)
            result = run_cli('step', '--workspace', str(path))
            self.assertEqual(result.returncode, 0, result.stderr)
            generation = [e for e in events(path) if e.get('event_type') == 'generation' and e.get('attempt_id')][0]
            self.assertEqual(generation['decision'], 'accepted')
            self.assertEqual(generation['generation'], 1)
            self.assertEqual(generation['counterfactual_metrics'], {'score': 1.0})
            self.assertEqual(generation['counterfactual_parent_metrics'], {'score': 0.0})

    def test_shortcut_candidate_is_caught_and_routed_to_rejected_memory(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.fixture(tmp, proposer='shortcut')
            self.assertEqual(run_cli('baseline', '--workspace', str(path)).returncode, 0)
            result = run_cli('step', '--workspace', str(path))
            self.assertEqual(result.returncode, 0, result.stderr)
            generation = [e for e in events(path) if e.get('event_type') == 'generation' and e.get('attempt_id')][0]
            self.assertEqual(generation['decision'], 'shortcut')
            self.assertIn('counterfactual gain vanished', generation['reason'])
            self.assertEqual(generation['generation'], 0)
            self.assertEqual(generation['counterfactual_metrics'], {'score': 0.0})
            memory = loop.rejected_recent(events(path))
            self.assertIn('shortcut', [entry['decision'] for entry in memory])

    def test_primary_rejection_skips_the_challenge_entirely(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.fixture(tmp, proposer=NEUTRAL_PROPOSER)
            self.assertEqual(run_cli('baseline', '--workspace', str(path)).returncode, 0)
            result = run_cli('step', '--workspace', str(path))
            self.assertEqual(result.returncode, 0, result.stderr)
            generation = [e for e in events(path) if e.get('event_type') == 'generation' and e.get('attempt_id')][0]
            self.assertEqual(generation['decision'], 'rejected')
            self.assertIsNone(generation['counterfactual_metrics'])
            self.assertFalse([e for e in events(path)
                              if e.get('event_type') == 'evaluation_started' and e.get('split') == 'counterfactual'])

    def test_disabled_challenge_runs_no_counterfactual_evaluations(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.fixture(tmp, enabled=False)
            self.assertEqual(run_cli('baseline', '--workspace', str(path)).returncode, 0)
            result = run_cli('step', '--workspace', str(path))
            self.assertEqual(result.returncode, 0, result.stderr)
            generation = [e for e in events(path) if e.get('event_type') == 'generation' and e.get('attempt_id')][0]
            self.assertEqual(generation['decision'], 'accepted')
            self.assertIsNone(generation['counterfactual_metrics'])
            self.assertFalse(list((path / '.nanorsi' / 'runs').rglob('cf-*.json')))

    def test_population_ranking_excludes_shortcut_candidates(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.fixture(tmp)
            config = load_config(path / 'nanorsi.toml')
            caught = {'kernel_decision': 'shortcut', 'gate_metrics': {'score': 1.0},
                      'gate_constraints': {'tests_passed': True}}
            honest = {'kernel_decision': 'accepted', 'gate_metrics': {'score': 1.0},
                      'gate_constraints': {'tests_passed': True}}
            self.assertFalse(_eligible(caught, config))
            self.assertTrue(_eligible(honest, config))


class SchemaTwoManifestTests(unittest.TestCase):
    def manifest_with_counterfactual(self, root, *, group='cfgroup', drop=None):
        manifest = root / 'tasks' / 'manifest.json'
        rows = json.loads(manifest.read_text())['tasks']
        rows = [row for row in rows if row['split'] != drop]
        rows.append({'task_id': 'cf-1', 'group_id': group, 'split': 'counterfactual',
                     'instruction': 'predict', 'input_files': {'x': '1'}, 'expected_files': {'y': '1'}})
        manifest.write_text(json.dumps({'schema_version': 1, 'tasks': rows}))
        return load_config(root / 'nanorsi.toml')

    def test_counterfactual_panel_is_selected_and_budgeted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = v2_workspace(tmp)
            config = self.manifest_with_counterfactual(root)
            store = LineageStore.initialize(root)
            output = root / '.nanorsi' / 'cf.json'
            result = loop.evaluate(root, config, root, 'counterfactual', output, store)
            self.assertEqual([case['task_id'] for case in result.case_results], ['cf-1'])
            self.assertEqual(loop.search_episode_count(store.events()), 1)

    def test_counterfactual_tasks_cannot_share_a_group_with_another_split(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = v2_workspace(tmp)
            config = self.manifest_with_counterfactual(root, group='validation')
            with self.assertRaises(ValueError):
                loop.tasks(root, config)

    def test_counterfactual_does_not_relieve_required_splits(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = v2_workspace(tmp)
            config = self.manifest_with_counterfactual(root, drop='validation')
            with self.assertRaises(ValueError):
                loop.tasks(root, config)


if __name__ == '__main__':
    unittest.main()
