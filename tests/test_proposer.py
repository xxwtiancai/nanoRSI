import tempfile
import unittest
from pathlib import Path

from nanorsi.proposer import ProposalError, load_proposal


class ProposerTests(unittest.TestCase):
    def test_loads_diff_and_hypothesis_and_rejects_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "proposal.diff").write_text(
                "diff --git a/target/a.py b/target/a.py\n--- a/target/a.py\n+++ b/target/a.py\n",
                encoding="utf-8",
            )
            (root / "hypothesis.json").write_text(
                '{"hypothesis":"change output","expected_metrics":{"score":0.8},"risks":[]}',
                encoding="utf-8",
            )
            proposal = load_proposal(root)
            self.assertEqual(proposal.changed_paths, ["target/a.py"])
            escape = root / "proposal.diff"
            escape.write_text(
                "diff --git a/../escape.py b/../escape.py\n--- a/../escape.py\n+++ b/../escape.py\n",
                encoding="utf-8",
            )
            with self.assertRaises(ProposalError):
                load_proposal(root)


if __name__ == "__main__":
    unittest.main()
