"""Textual learning rate: per-proposal edit budgets (ADOPTION item 53)."""
from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from nanorsi.contracts import comparison_hash
from nanorsi.proposer import ProposalError, edit_lines, load_proposal
from nanorsi.config import load_config
from tests.test_end_to_end import run_cli
from tests.test_v2_lifecycle import make_v2

DIFF = """diff --git a/target/agent/skills/inspect/SKILL.md b/target/agent/skills/inspect/SKILL.md
--- a/target/agent/skills/inspect/SKILL.md
+++ b/target/agent/skills/inspect/SKILL.md
@@ -1,2 +1,2 @@
-old line one
-old line two
+new line one
+new line two
"""


class EditBudgetTests(unittest.TestCase):

    def test_edit_lines_counts_payload_only(self) -> None:
        self.assertEqual(edit_lines(DIFF), 4)  # two deletions + two additions
        self.assertEqual(edit_lines(""), 0)
        self.assertEqual(edit_lines("--- a/x\n+++ b/x\n@@ -1 +1 @@\n context\n"), 0)

    def test_load_proposal_enforces_the_budget(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / "proposal.diff").write_text(DIFF)
            (directory / "hypothesis.json").write_text(json.dumps({"hypothesis": "test"}))
            self.assertIsNotNone(load_proposal(directory, max_edit_lines=4))
            self.assertIsNotNone(load_proposal(directory, max_edit_lines=0))  # 0 = unbounded
            with self.assertRaises(ProposalError) as blocked:
                load_proposal(directory, max_edit_lines=3)
            self.assertIn("edit budget", str(blocked.exception))
            self.assertIn("4 changed lines > 3", str(blocked.exception))

    def test_budget_failure_lands_in_the_journal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_v2(tmp)
            toml = root / 'nanorsi.toml'
            toml.write_text(toml.read_text().replace('[proposer]', '[proposer]\nmax_edit_lines = 1'))
            for command in ('baseline', 'run'):
                result = run_cli(command, '--workspace', str(root))
                self.assertEqual(result.returncode, 0, result.stderr)
            events = [json.loads(line) for line in (root / 'lineage.jsonl').read_text().splitlines()]
            failures = [e for e in events if e.get('event_type') == 'attempt_failed']
            self.assertTrue(failures)
            self.assertTrue(all('edit budget' in (e.get('reason') or '') for e in failures))
            # the negative feedback surfaces for later turns
            from nanorsi.loop import rejected_recent
            self.assertTrue(rejected_recent(events))

    def test_default_budget_keeps_comparison_hash_neutral(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_v2(tmp)
            config = load_config(root / 'nanorsi.toml')
            self.assertEqual(config.proposer.max_edit_lines, 0)
            hashed = comparison_hash(root, config)
            toml = root / 'nanorsi.toml'
            toml.write_text(toml.read_text().replace('[proposer]', '[proposer]\nmax_edit_lines = 0'))
            self.assertEqual(comparison_hash(root, load_config(toml)), hashed)
            toml.write_text(toml.read_text().replace('max_edit_lines = 0', 'max_edit_lines = 5'))
            self.assertNotEqual(comparison_hash(root, load_config(toml)), hashed)


if __name__ == "__main__":
    unittest.main()
