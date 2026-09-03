import os
from pathlib import Path


output = Path(os.environ["NANORSI_PROPOSAL_DIR"])
(output / "proposal.diff").write_text("", encoding="utf-8")
(output / "hypothesis.json").write_text(
    '{"hypothesis":"External training contract only","expected_metrics":{},"risks":[]}',
    encoding="utf-8",
)
