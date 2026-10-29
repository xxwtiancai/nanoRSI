"""Run a workspace template across multiple seeds through the ordinary CLI lifecycle.

This is the multi-seed orchestration named as a prerequisite in
docs/v0.4/SELECTOR_STUDY_PROTOCOL.md: every seed is a fresh, independently
baselined workspace (the frozen protocol is immutable per workspace, so
repeats or seeds cannot be raised after the fact). The template must be a
fully assembled but NOT yet baselined workspace - task pack swapped in,
model configured, budgets set. For each seed this script copies the
template, patches ``[experiment] seed``, and runs baseline -> run ->
freeze --repeats R -> final-test -> report -> verify, then aggregates the
per-seed outcomes and cross-seed condition statistics into summary.json.

The script is model-agnostic: it drives the installed ``nanorsi`` CLI with
whatever the template is configured for (offline fixture or live model).
It never modifies the template itself, and every seed directory retains its
full journal for the evidence ledger.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import statistics
import subprocess
import sys


def _nanorsi() -> list[str]:
    return [sys.executable, "-m", "nanorsi.cli"]


def _run(command: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    completed = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(f"command failed ({completed.returncode}): {' '.join(command)}\n{completed.stderr[-400:]}")
    return completed


def _patch_seed(toml: Path, seed: int) -> None:
    text = toml.read_text()
    lines = [f"seed = {seed}\n" if line.strip().startswith("seed = ") and not line.startswith("#") else line
             for line in text.splitlines(keepends=True)]
    if not any(line.startswith("seed = ") for line in lines):
        raise ValueError("template nanorsi.toml has no [experiment] seed line to patch")
    toml.write_text("".join(lines))


def run_seed(template: Path, out: Path, seed: int, repeats: int) -> dict:
    workspace = out / f"seed-{seed}"
    if workspace.exists():
        raise RuntimeError(f"refusing to overwrite existing seed workspace: {workspace}")
    shutil.copytree(template, workspace, ignore=shutil.ignore_patterns("__pycache__", ".nanorsi"))
    toml = workspace / "nanorsi.toml"
    original = toml.read_bytes()
    _patch_seed(toml, seed)
    if toml.read_bytes() != original:  # seed != template default leaves the tree dirty
        from nanorsi.gitops import Git
        git = Git(workspace)
        git._run("add", "-A")  # a committed template stages only the toml; an
        git._run("commit", "-m", f"set experiment seed to {seed}", identity=True)  # uncommitted template gets its initial commit
    cli = _nanorsi()
    for step in (["baseline"], ["run"], ["freeze", "--repeats", str(repeats)], ["final-test"], ["report"], ["verify"]):
        _run(cli + step + ["--workspace", str(workspace)])
    final = json.loads((workspace / "reports" / "final.json").read_text())
    events = [json.loads(line) for line in (workspace / "lineage.jsonl").read_text().splitlines()]
    generations = [e for e in events if e.get("event_type") == "generation" and e.get("attempt_id")]
    return {"seed": seed,
            "workspace": str(workspace),
            "decisions": {str(e.get("attempt_id")): e.get("decision") for e in generations},
            "accepted": sum(e.get("decision") == "accepted" for e in generations),
            "final": final,
            "model_calls": sum(e["usage"].get("model_calls") or 0 for e in final.get("results", [])
                               if isinstance(e.get("usage"), dict))}


def aggregate(runs: list[dict]) -> dict:
    conditions: dict[str, list[float]] = {}
    for run in runs:
        for entry in run["final"].get("results", []):
            score = (entry.get("metrics") or {}).get("score")
            if isinstance(score, (int, float)):
                conditions.setdefault(str(entry.get("condition")), []).append(float(score))
    summary = {condition: {"scores": sorted(values), "n": len(values),
                           "mean": statistics.fmean(values) if values else None,
                           "spread": max(values) - min(values) if values else None}
               for condition, values in sorted(conditions.items())}
    return {"schema_version": 1, "seeds": [run["seed"] for run in runs],
            "accepted_per_seed": {str(run["seed"]): run["accepted"] for run in runs},
            "total_model_calls": sum(run["model_calls"] for run in runs),
            "conditions": summary,
            "note": "every seed is an independent frozen workspace; per-seed journals live in seed-N/"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a workspace template across seeds through the full lifecycle.")
    parser.add_argument("template", help="assembled, not-yet-baselined workspace directory")
    parser.add_argument("out", help="output directory receiving seed-N/ workspaces and summary.json")
    parser.add_argument("--seeds", default="0,1,2", help="comma-separated seed list (default 0,1,2)")
    parser.add_argument("--repeats", type=int, default=3)
    args = parser.parse_args(argv)
    template, out = Path(args.template).resolve(), Path(args.out).resolve()
    if not (template / "nanorsi.toml").is_file():
        raise SystemExit("template must contain nanorsi.toml (assemble and configure it first, before baseline)")
    if (template / "lineage.jsonl").is_file():
        raise SystemExit("template already has an experiment journal; provide a fresh unbaselined copy")
    out.mkdir(parents=True, exist_ok=True)
    seeds = [int(value) for value in args.seeds.split(",") if value.strip() != ""]
    runs = []
    for seed in seeds:
        print(f"== seed {seed}", flush=True)
        runs.append(run_seed(template, out, seed, args.repeats))
        print(json.dumps({"seed": seed, "accepted": runs[-1]["accepted"],
                          "final_scores": {str(e.get("condition")): e["metrics"].get("score")
                                           for e in runs[-1]["final"].get("results", [])}}), flush=True)
    payload = aggregate(runs)
    (out / "summary.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload["conditions"], indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
