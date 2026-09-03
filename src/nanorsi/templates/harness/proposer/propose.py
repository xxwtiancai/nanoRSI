import os
from pathlib import Path


output = Path(os.environ["NANORSI_PROPOSAL_DIR"])
diff = """diff --git a/target/agent/policy.txt b/target/agent/policy.txt
--- a/target/agent/policy.txt
+++ b/target/agent/policy.txt
@@ -1 +1 @@
-mode: guess
+mode: evidence
"""
(output / "proposal.diff").write_text(diff, encoding="utf-8")
(output / "hypothesis.json").write_text(
    '{"hypothesis":"Use statement evidence instead of guessing","expected_metrics":{"score":1.0},"risks":[]}',
    encoding="utf-8",
)
