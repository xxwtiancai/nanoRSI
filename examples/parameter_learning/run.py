"""Run real CPU learning trials through nanoRSI's ordinary CLI lifecycle.

The default panel is three algorithms, three seeds, and both frozen/self-use
proposer controls. It retains failures, rejected candidates, and negative test
deltas. It neither substitutes an experiment loop nor chooses winning weights.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import importlib.util
import json
import os
from pathlib import Path
import statistics
import subprocess
import sys


def summarize(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["method"], row["arm"])].append(row)
    groups = []
    for (method, arm), runs in sorted(grouped.items()):
        done = [row for row in runs if row["status"] == "completed"]
        deltas = [row["candidate_accuracy"] - row["baseline_accuracy"] for row in done]
        groups.append({
            "method": method, "arm": arm, "completed_runs": len(done),
            "failed_runs": len(runs) - len(done),
            "accuracy_regressions": sum(value < 0 for value in deltas),
            "mean_baseline_accuracy": statistics.fmean(row["baseline_accuracy"] for row in done) if done else None,
            "mean_candidate_accuracy": statistics.fmean(row["candidate_accuracy"] for row in done) if done else None,
            "mean_accuracy_delta": statistics.fmean(deltas) if done else None,
            "accuracy_delta_stdev": statistics.stdev(deltas) if len(done) > 1 else None,
            "mean_baseline_loss": statistics.fmean(row["baseline_loss"] for row in done) if done else None,
            "mean_candidate_loss": statistics.fmean(row["candidate_loss"] for row in done) if done else None,
        })
    pairs = []
    by_method_seed = defaultdict(dict)
    for row in rows:
        if row["status"] == "completed":
            by_method_seed[(row["method"], row["seed"])][row["arm"]] = row
    for (method, seed), arms in sorted(by_method_seed.items()):
        if {"frozen", "self-use"} <= arms.keys():
            pairs.append({"method": method, "seed": seed,
                          "self_use_minus_frozen_accuracy": arms["self-use"]["candidate_accuracy"] - arms["frozen"]["candidate_accuracy"],
                          "self_use_minus_frozen_loss": arms["self-use"]["candidate_loss"] - arms["frozen"]["candidate_loss"]})
    return {"schema_version": 1, "demo": "tiny-softmax-teaching-demo", "runs": rows,
            "groups": groups, "paired_proposer_controls": pairs,
            "limitations": ["Synthetic overlapping numeric clusters; no LLM fine-tuning claim.",
                            "Repeated rounds are gradient training; frozen versus self-use controls isolate checkpoint-guided curriculum only.",
                            "Small seed panel is descriptive; it does not establish recursive self-improvement.",
                            "CPU wall time is measured; API calls are zero and monetary cost remains unknown."]}


def command(args, *, env, evidence, ordinal):
    completed = subprocess.run([sys.executable, "-m", "nanorsi.cli", *args], env=env,
                               capture_output=True, text=True, timeout=180)
    (evidence / f"{ordinal:02d}-{args[0]}.json").write_text(json.dumps({
        "argv": [sys.executable, "-m", "nanorsi.cli", *args], "returncode": completed.returncode,
        "stdout": completed.stdout, "stderr": completed.stderr,
    }, indent=2) + "\n")
    if completed.returncode:
        raise RuntimeError(f"{' '.join(args)}: {completed.stderr.strip()}")


def run_one(output, *, method, seed, arm, rounds):
    name = f"{method}-seed-{seed}-{arm}"
    workspace, evidence = output / name, output / "commands" / name
    if workspace.exists():
        raise ValueError(f"workspace already exists; retained evidence must not be overwritten: {workspace}")
    evidence.mkdir(parents=True, exist_ok=False)
    # Source checkout support; installed packages continue to work normally.
    src = Path(__file__).resolve().parents[2] / "src"
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    if src.is_dir():
        env["PYTHONPATH"] = str(src) + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    row = {"method": method, "seed": seed, "arm": arm, "workspace": str(workspace), "status": "failed"}
    try:
        command(["new", "learner", str(workspace), "--goal", "Measure real parameter learning on held-out numeric cases"], env=env, evidence=evidence, ordinal=0)
        spec = importlib.util.spec_from_file_location("parameter_prepare", Path(__file__).with_name("prepare.py"))
        prepare = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(prepare)
        prepare.prepare_workspace(workspace, method=method, seed=seed, arm=arm, rounds=rounds)
        for ordinal, args in enumerate((["run"], ["freeze", "--repeats", "1"], ["final-test"], ["verify"]), 1):
            command([*args, "--workspace", str(workspace)], env=env, evidence=evidence, ordinal=ordinal)
        report_path = workspace / "reports/final.json"
        report = json.loads(report_path.read_text())
        results = {record["condition"]: record for record in report["results"]}
        if set(results) != {"baseline", "candidate"}:
            raise ValueError("CPU learner final report must contain baseline and candidate")
        for condition in ("baseline", "candidate"):
            row[f"{condition}_accuracy"] = results[condition]["metrics"]["accuracy"]
            row[f"{condition}_loss"] = results[condition]["metrics"]["loss"]
            row[f"{condition}_checkpoint"] = results[condition]["checkpoint"]
        lineage = workspace / "lineage.jsonl"
        events = [json.loads(line) for line in lineage.read_text().splitlines()]
        row["decisions"] = dict(Counter(event["decision"] for event in events if event.get("event_type") in ("generation", "attempt_failed")))
        row["training_rounds"] = len(list((workspace / ".nanorsi/runs").glob("*/training/evidence.json")))
        row["final_report"] = str(report_path)
        if row["decisions"].get("failed", 0):
            row["error"] = f"{row['decisions']['failed']} search attempts failed; final measurements retained"
        else:
            row["status"] = "completed"
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.TimeoutExpired) as error:
        row["error"] = str(error)
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="new evidence directory; existing runs are never overwritten")
    parser.add_argument("--methods", nargs="+", choices=("sft", "rl", "lora"), default=["sft", "rl", "lora"])
    parser.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2])
    parser.add_argument("--arms", nargs="+", choices=("frozen", "self-use"), default=["frozen", "self-use"])
    parser.add_argument("--rounds", type=int, default=3)
    args = parser.parse_args()
    if args.rounds < 1 or any(seed < 0 for seed in args.seeds):
        parser.error("rounds must be positive and seeds nonnegative")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    rows = []
    for method in args.methods:
        for seed in args.seeds:
            for arm in args.arms:
                row = run_one(output, method=method, seed=seed, arm=arm, rounds=args.rounds)
                rows.append(row)
                (output / "summary.json").write_text(json.dumps(summarize(rows), indent=2, sort_keys=True) + "\n")
                if row["status"] == "completed":
                    print(f"{method} seed={seed} {arm}: test accuracy {row['baseline_accuracy']:.3f} -> {row['candidate_accuracy']:.3f}; loss {row['baseline_loss']:.3f} -> {row['candidate_loss']:.3f}; decisions={row['decisions']}", flush=True)
                else:
                    print(f"{method} seed={seed} {arm}: FAILED; {row['error']}", flush=True)
    print(output / "summary.json")
    return 0 if all(row["status"] == "completed" for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
