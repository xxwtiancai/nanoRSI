"""First selector-study dry-run: noise-band arm vs strict gate on an offline fixture.

This exercises the full [selector-study protocol](../../docs/SELECTOR_STUDY_PROTOCOL.md)
toolchain end to end at zero API cost: a deterministic program-mode fixture (a scripted
proposer always proposes the same one-line fix; the stock program evaluator exact-matches)
runs through the multi-seed orchestrator under two arms — control (strict gate) and a
noise-band arm — and every arm workspace is double-scored against the control gate.
The aggregate report carries the protocol's required fields; on this deterministic
fixture all seeds agree by construction, so the dry-run validates machinery and
accounting, not effect sizes. A live study at 3 seeds x 3 budget points is the next step.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import statistics
import subprocess
import sys
import tempfile

REPO = Path(__file__).resolve().parents[2]
MULTISEED = REPO / "examples" / "multiseed" / "run.py"
DOUBLE = REPO / "examples" / "double_scoring" / "run.py"

BROKEN = '''"""Echo task: read records.json, print summary.json with value + 1."""
import json
import sys


def main():
    payload = json.load(sys.stdin)
    print(json.dumps({"answer": payload["value"]}))


if __name__ == "__main__":
    main()
'''

FIXED_LINE = '    print(json.dumps({"answer": payload["value"] + 1}))'
BROKEN_LINE = '    print(json.dumps({"answer": payload["value"]}))'

PROPOSER = '''import json
import os
from pathlib import Path

out = Path(os.environ["NANORSI_PROPOSAL_DIR"])
old = '    print(json.dumps({"answer": payload["value"]}))'
new = '    print(json.dumps({"answer": payload["value"] + 1}))'
diff = ("diff --git a/target/program.py b/target/program.py\\n"
        "--- a/target/program.py\\n"
        "+++ b/target/program.py\\n"
        "@@ -6,3 +6,3 @@\\n"
        " def main():\\n"
        "     payload = json.load(sys.stdin)\\n"
        "-" + old + "\\n"
        "+" + new + "\\n")
(out / "proposal.diff").write_text(diff)
(out / "hypothesis.json").write_text(json.dumps({"hypothesis": "apply the off-by-one fix"}))
'''


def _task(split: str, index: int) -> dict:
    value = index + 1
    record = json.dumps({"value": value}, ensure_ascii=False)
    expected = json.dumps({"answer": value + 1}, ensure_ascii=False)
    return {"task_id": f"{split}-{index:03d}", "group_id": f"{split}-echo", "split": split,
            "instruction": "Emit the value plus one.",
            "input_files": {"records.json": record},
            "expected_files": {"summary.json": expected}}


def build_template(directory: Path, band: float) -> Path:
    from nanorsi.gitops import Git
    from nanorsi.templates import render_template
    render_template("program", directory, goal="Fix the off-by-one echo")
    (directory / "target" / "program.py").write_text(BROKEN)
    tasks = [_task(split, index) for split, count in (("train", 2), ("validation", 3), ("test", 4))
             for index in range(count)]
    (directory / "tasks" / "manifest.json").write_text(
        json.dumps({"schema_version": 1, "tasks": tasks}, indent=1) + "\n")
    (directory / "proposer").mkdir(exist_ok=True)
    (directory / "proposer" / "propose.py").write_text(PROPOSER)
    toml = directory / "nanorsi.toml"
    text = toml.read_text()
    if band:
        text = text.replace("[gate]", f"[gate]\nnoise_band = {band}")
    text = text.replace("max_steps = 5", "max_steps = 3")
    toml.write_text(text)
    git = Git(directory)
    git.init()
    git._run("add", "-A")
    git._run("commit", "-m", "selector dry-run template", identity=True)
    return directory


def _module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_arm(out: Path, band: float, seeds: list[int], repeats: int) -> dict:
    label = "noise-band" if band else "strict"
    with tempfile.TemporaryDirectory() as tmp:
        template = build_template(Path(tmp) / "template", band)
        result = subprocess.run(
            [sys.executable, str(MULTISEED), str(template), str(out / label),
             "--seeds", ",".join(str(seed) for seed in seeds), "--repeats", str(repeats)],
            capture_output=True, text=True, timeout=1800,
            env={"PATH": __import__("os").environ["PATH"], "PYTHONPATH": str(REPO / "src")})
        if result.returncode != 0:
            raise RuntimeError(result.stderr[-600:])
    harness = _module("double_scoring_run", DOUBLE)
    per_seed = []
    for seed in seeds:
        workspace = out / label / f"seed-{seed}"
        scoring = harness.recompute(workspace, 0.0)
        events = [json.loads(line) for line in (workspace / "lineage.jsonl").read_text().splitlines()]
        generations = [e for e in events if e.get("event_type") == "generation" and e.get("attempt_id")]
        per_seed.append({"seed": seed,
                         "decisions": [e.get("decision") for e in generations],
                         "accepted": sum(e.get("decision") == "accepted" for e in generations),
                         "false_blocks": scoring["counts"]["false_block"],
                         "false_admits": scoring["counts"]["false_admit"]})
    return {"arm": label, "noise_band": band, "per_seed": per_seed}


def aggregate(report: dict) -> dict:
    rows = []
    for arm in report["arms"]:
        for seed_row in arm["per_seed"]:
            final = json.loads((report["out"] / arm["arm"] / f"seed-{seed_row['seed']}" / "reports" / "final.json").read_text())
            for entry in final.get("results", []):
                score = (entry.get("metrics") or {}).get("score")
                if isinstance(score, (int, float)):
                    rows.append({"arm": arm["arm"], "seed": seed_row["seed"],
                                 "condition": entry.get("condition"), "score": float(score)})
    conditions: dict[str, dict] = {}
    for row in rows:
        conditions.setdefault(f"{row['arm']}/{row['condition']}", []).append(row["score"])
    return {name: {"mean": statistics.fmean(values), "n": len(values)}
            for name, values in sorted(conditions.items())}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the offline selector-study dry-run.")
    parser.add_argument("out")
    parser.add_argument("--seeds", default="0,1,2")
    parser.add_argument("--band", type=float, default=1.5)
    parser.add_argument("--repeats", type=int, default=2)
    args = parser.parse_args(argv)
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    seeds = [int(value) for value in args.seeds.split(",") if value.strip()]
    report = {"schema_version": 1, "out": out, "arms": [
        run_arm(out, 0.0, seeds, args.repeats),
        run_arm(out, args.band, seeds, args.repeats)]}
    report["conditions"] = aggregate(report)
    report["verdict"] = ("dry-run on a deterministic offline fixture: machinery and "
                         "false-block accounting validated; effect sizes require the live "
                         "three-seed x three-budget study per the selector protocol")
    report.pop("out")
    (out / "summary.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report["conditions"], indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
