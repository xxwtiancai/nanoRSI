"""Keyword judge for the offline starter: one criterion per expected point.

Protocol: NANORSI_JUDGE_REQUEST (json: task, deliverables_dir, label) ->
NANORSI_JUDGE_RESULT (json: n_passed, n_criteria, all_pass). Real benchmarks
replace this file with their own judge behind the same protocol."""
import json
import os
from pathlib import Path


def main() -> int:
    request = json.loads(Path(os.environ["NANORSI_JUDGE_REQUEST"]).read_text(encoding="utf-8"))
    points = request["task"].get("extra", {}).get("expected_points", [])
    text = ""
    for path in sorted(Path(request["deliverables_dir"]).glob("*")):
        if path.is_file():
            text += path.read_text(encoding="utf-8", errors="replace").lower() + "\n"
    passed = sum(1 for point in points if point.lower() in text)
    result = {"n_passed": passed, "n_criteria": len(points), "all_pass": passed == len(points),
              "missed": [p for p in points if p.lower() not in text]}
    Path(os.environ["NANORSI_JUDGE_RESULT"]).write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
