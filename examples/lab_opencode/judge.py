"""nanoRSI judge protocol -> LAB's own rubric judge (evaluation.run_eval).

Reads NANORSI_JUDGE_REQUEST, points run_eval at the rollout's <run_dir>/output
(binary deliverables kept by runner.py) with the configured judge model through
the local custom/ provider, and writes NANORSI_JUDGE_RESULT {n_passed, n_criteria,
all_pass}. A failed judgement writes nothing, which the core records as ungraded."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from runner import lab_env, settings  # same directory


def main() -> int:
    request = json.loads(Path(os.environ["NANORSI_JUDGE_REQUEST"]).read_text(encoding="utf-8"))
    cfg = settings(Path.cwd())
    run_dir = Path(request["run_dir"]).resolve()
    if not (run_dir / "output").is_dir():
        return 1
    env = lab_env(cfg)
    env["OPENAI_BASE_URL"] = cfg["judge_base_url"]
    env["OPENAI_API_KEY"] = Path(cfg["api_key_file"]).expanduser().read_text(encoding="utf-8").strip()
    scores = run_dir / "scores.json"
    if not scores.is_file():
        proc = subprocess.run([cfg["lab_python"], "-u", "-m", "evaluation.run_eval", "--run-id", str(run_dir),
                               "--task", request["task"]["task_id"], "--judge-model", cfg["judge_model"],
                               "--parallel", "3"],
                              cwd=cfg["lab_root"], env=env, capture_output=True, text=True, timeout=3600)
        (run_dir / "judge.log").write_text(proc.stdout[-20000:] + "\n--stderr--\n" + proc.stderr[-10000:], encoding="utf-8")
    if not scores.is_file():
        return 1
    data = json.loads(scores.read_text(encoding="utf-8"))
    result = {"n_passed": int(data["n_passed"]), "n_criteria": int(data["n_criteria"]), "all_pass": bool(data.get("all_pass"))}
    Path(os.environ["NANORSI_JUDGE_RESULT"]).write_text(json.dumps(result), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
