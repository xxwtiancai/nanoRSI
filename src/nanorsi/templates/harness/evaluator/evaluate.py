import json
import os
import subprocess
import sys
from pathlib import Path


private_cases = {
    "gate": [{"statement": "Please route this invoice.", "answer": "billing"}],
    "train": [{"statement": "Invoice #4 needs review.", "answer": "billing"}],
    "heldout": [{"statement": "We need a refund for order 8.", "answer": "support"}],
}


def invoke(case):
    runner = Path.cwd() / "target" / "agent" / "run.py"
    completed = subprocess.run(
        [sys.executable, str(runner)],
        input=json.dumps({"statement": case["statement"]}),
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(completed.stdout)["answer"]


cases = private_cases[os.environ["NANORSI_SPLIT"]]
case_results = []
for index, case in enumerate(cases):
    answer = invoke(case)
    score = float(answer == case["answer"])
    case_results.append({"id": str(index), "score": score})
result = {
    "schema_version": 1,
    "status": "ok",
    "metrics": {"score": sum(item["score"] for item in case_results) / len(case_results)},
    "constraints": {"tests_passed": True},
    "case_results": case_results,
    "cost_usd": None,
    "duration_ms": 1,
}
Path(os.environ["NANORSI_RESULT_PATH"]).write_text(json.dumps(result), encoding="utf-8")
