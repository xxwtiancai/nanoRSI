import os
from pathlib import Path


output = Path(os.environ["NANORSI_PROPOSAL_DIR"])
diff = "\n".join(
    [
        "diff --git a/target/search.py b/target/search.py",
        "--- a/target/search.py",
        "+++ b/target/search.py",
        "@@ -1,3 +1,3 @@",
        " def best(values):",
        '     """Return the best value; the seed intentionally loses the maximum."""',
        "-    return 0",
        "+    return max(values) if values else 0",
        "",
    ]
)
(output / "proposal.diff").write_text(diff, encoding="utf-8")
(output / "hypothesis.json").write_text(
    '{"hypothesis":"Select the maximum value","expected_metrics":{"score":1.0},"risks":[]}',
    encoding="utf-8",
)
