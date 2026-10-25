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
        data = json.loads(result_path.read_text(encoding="utf-8"))
        if not isinstance(data.get("n_criteria"), int) or not isinstance(data.get("n_passed"), int) or data["n_criteria"] <= 0:
            return None
        return {"n_passed": data["n_passed"], "n_criteria": data["n_criteria"],
                "all_pass": bool(data.get("all_pass", data["n_passed"] == data["n_criteria"]))}
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
                score = json.loads(result_path.read_text(encoding="utf-8"))
                score = score if isinstance(score.get("n_criteria"), int) else None
            else:
                score = _request(config, workspace, task, label, run_dir, result_path)
            row = {"task": task["task_id"], "label": label, "role": "base" if label == "base1" else "final",
                   "score": score, "graded": score is not None}
            ledger.append("judged", **row)
            rows.append(row)
    return rows
