"""Judging happens only after freeze and only on frozen outputs: the base rollout and
the chosen final of every task. Scores never reach the improver. The judge is a
workspace command (protocol: NANORSI_JUDGE_REQUEST json -> NANORSI_JUDGE_RESULT json
{n_passed, n_criteria, all_pass}); a failed judgement is recorded as ungraded, never
as zero."""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


class JudgeError(RuntimeError):
    pass


def _parse_score(data: object) -> dict | None:
    if not isinstance(data, dict):
        return None
    passed = data.get("n_passed")
    criteria = data.get("n_criteria")
    if (isinstance(passed, bool) or not isinstance(passed, int)
            or isinstance(criteria, bool) or not isinstance(criteria, int)
            or criteria <= 0 or passed < 0 or passed > criteria):
        return None
    all_pass = data.get("all_pass", passed == criteria)
    if not isinstance(all_pass, bool):
        return None
    return {"n_passed": passed, "n_criteria": criteria, "all_pass": all_pass}


def frozen_choices(ledger) -> dict[str, str]:
    """task_id -> chosen final label, as recorded at freeze time."""
    for row in reversed(ledger.events()):
        if row.get("event") == "freeze":
            return dict(row["choices"])
    raise JudgeError("freeze before judging: `nanorsi freeze`")


def _request(config, workspace, task, label, run_dir, result_path) -> dict | None:
    request = run_dir / "judge-request.json"
    request.write_text(json.dumps({"task": task, "label": label, "run_dir": str(run_dir),
                                   "deliverables_dir": str(run_dir / "deliverables"),
                                   "judge_model": config.judge_model}, ensure_ascii=False, indent=1), encoding="utf-8")
    env = {**os.environ, "NANORSI_JUDGE_REQUEST": str(request), "NANORSI_JUDGE_RESULT": str(result_path)}
    try:
        proc = subprocess.run(config.judge_command, cwd=str(workspace), env=env, capture_output=True, text=True, timeout=3600)
        (run_dir / "judge.log").write_text(proc.stdout[-20000:] + "\n--stderr--\n" + proc.stderr[-20000:], encoding="utf-8")
        if not result_path.is_file():
            return None
        return _parse_score(json.loads(result_path.read_text(encoding="utf-8")))
    except (subprocess.TimeoutExpired, OSError, ValueError):
        return None


def judge(config, workspace: Path, tasks: list[dict], ledger, *, bases: bool = True) -> list[dict]:
    if not config.judge_command:
        raise JudgeError("[judge] command is not configured in nanorsi.toml")
    choices = frozen_choices(ledger)
    rows = []
    for task in tasks:
        if task["task_id"] not in choices:
            continue
        run_root = Path(workspace) / ".nanorsi" / "runs" / task["task_id"].replace("/", "__")
        labels = (["base1"] if bases else []) + [choices[task["task_id"]]]
        for label in labels:
            run_dir = run_root / label
            result_path = run_dir / "judge-result.json"
            if result_path.is_file():
                try:
                    score = _parse_score(json.loads(result_path.read_text(encoding="utf-8")))
                except (OSError, ValueError):
                    score = None
            else:
                score = _request(config, workspace, task, label, run_dir, result_path)
            row = {"task": task["task_id"], "label": label, "role": "base" if label == "base1" else "final",
                   "score": score, "graded": score is not None}
            ledger.append("judged", **row)
            rows.append(row)
    return rows
