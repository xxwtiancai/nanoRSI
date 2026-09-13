"""Evidence-ledger tests use the offline v2 fixture workspace, not live models."""
import json
import tempfile
import unittest

from nanorsi.evidence import revisions, write_ledger
from tests.test_end_to_end import run_cli
from tests.test_v2_lifecycle import make_v2


class EvidenceLedgerTests(unittest.TestCase):
    def call(self, root, *args):
        result = run_cli(*args, '--workspace', str(root))
        self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def test_ledger_records_each_revision_with_diff_and_redacted_cases(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_v2(tmp)
            self.call(root, 'run')
            records = revisions(root)
            self.assertEqual([record['decision'] for record in records], ['accepted', 'no-op', 'no-op'])
            accepted = records[0]
            self.assertEqual(accepted['attempt_id'], 1)
            self.assertEqual(accepted['generation'], 1)
            self.assertEqual(accepted['metric']['name'], 'score')
            self.assertIsInstance(accepted['metric']['delta'], (int, float))
            self.assertEqual(accepted['surface'], ['target/agent/skills/inspect/SKILL.md'])
            self.assertIn('diff --git', accepted['diff']['text'])
            self.assertEqual(accepted['diff']['integrity'], 'ok')
            skill = 'target/agent/skills/inspect/SKILL.md'
            self.assertGreaterEqual(accepted['diff']['stats'][skill][0], 1)
            for cases in (accepted['evaluator']['parent_cases'], accepted['evaluator']['candidate_cases']):
                self.assertTrue(cases)
                for case in cases:
                    self.assertEqual(sorted(case), ['group_id', 'repeat_id', 'score', 'status', 'task_id'])
            self.assertEqual(accepted['diagnosis'], {'hypothesis': 'CI protocol fixture only'})

    def test_ledger_written_by_report_and_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_v2(tmp)
            self.call(root, 'run')
            self.call(root, 'report')
            jsonl = root / 'reports/evidence.jsonl'
            markdown = root / 'reports/evidence.md'
            self.assertTrue(jsonl.is_file() and markdown.is_file())
            first = jsonl.read_bytes()
            self.call(root, 'report')
            self.assertEqual(jsonl.read_bytes(), first)
            self.assertEqual(len(first.decode().splitlines()), 3)
            text = markdown.read_text()
            self.assertIn('# nanoRSI evidence ledger', text)
            self.assertIn('| 1 | 1 | accepted', text)
            self.assertIn('integrity ok', text)

    def test_failed_attempt_lands_in_ledger(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_v2(tmp)
            fixture = root / 'adapters/fixture.py'
            fixture.write_text(fixture.read_text().replace(
                "p='target/agent/skills/inspect/SKILL.md'", "p='evaluator/evil.txt'"))
            self.call(root, 'baseline')
            self.assertNotEqual(run_cli('step', '--workspace', str(root)).returncode, 0)
            records = revisions(root)
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]['decision'], 'failed')
            self.assertTrue(records[0]['reason'])
            self.assertIsNone(records[0]['diff'])

    def test_tampered_artifact_is_flagged_not_hidden(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_v2(tmp)
            self.call(root, 'run')
            diff = next(p for p in (root / '.nanorsi/runs').glob('*/proposal/proposal.diff')
                        if b'fixture-approved' in p.read_bytes())
            original = diff.read_bytes()
            diff.write_bytes(original + b'\n# tampered\n')
            self.assertEqual(revisions(root)[0]['diff']['integrity'], 'mismatch')
            diff.write_bytes(original)
            self.assertEqual(revisions(root)[0]['diff']['integrity'], 'ok')
            self.call(root, 'verify')
            self.assertEqual(write_ledger(root)['revisions'], 3)


if __name__ == '__main__':
    unittest.main()
