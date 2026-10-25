#!/usr/bin/env python3
"""One-command offline smoke test: the smallest end-to-end nanoRSI experiment.

Builds a CPU fixture workspace (model mode: a real checkpoint is trained, no API),
runs baseline -> search -> freeze -> final-test -> report -> audit, and narrates
what an RSI loop actually does. Read docs/RSI_MINIMAL.md for the mechanism map.

Usage: python examples/smoke/run_smoke.py [--keep]
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EVALUATOR = '''import json,os
from pathlib import Path
rows=json.loads(Path(os.environ['NANORSI_TASK_MANIFEST']).read_text())['tasks']
rows=[r for r in rows if r['split']==os.environ['NANORSI_SPLIT']]
score=json.loads(Path('target/model.json').read_text())['weight']/4
usage={'model_calls':0,'input_tokens':0,'output_tokens':0,'cost_usd':0}
cases=[{'task_id':r['task_id'],'group_id':r['group_id'],'repeat_id':int(os.environ['NANORSI_REPEAT_ID']),'score':score,'status':'ok','trace':[],'skill_hashes':{},'usage':usage,'duration_ms':0} for r in rows]
Path(os.environ['NANORSI_RESULT_PATH']).write_text(json.dumps({'schema_version':2,'status':'ok','metrics':{'score':score},'constraints':{'tests_passed':True},'case_results':cases,'usage':usage,'cost_usd':0,'duration_ms':0}))
'''
TRAINER = '''import hashlib,json,os
from pathlib import Path
p=Path(os.environ['NANORSI_CHECKPOINT_PATH'])
d=Path(os.environ['NANORSI_TRAINING_DATA_PATH'])
initial=hashlib.sha256(p.read_bytes()).hexdigest()
rows=json.loads(d.read_text())['tasks']
assert all(r['split']=='train' for r in rows)
p.write_text(json.dumps({'weight':json.loads(p.read_text())['weight']+1}))
result={'schema_version':1,'status':'completed','checkpoint_path':str(p),'checkpoint_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'method':'smoke-fixture','steps':1,'duration_ms':0,'data_sha256':hashlib.sha256(d.read_bytes()).hexdigest(),'initial_checkpoint_sha256':initial}
Path(os.environ['NANORSI_TRAINING_RESULT_PATH']).write_text(json.dumps(result))
'''
PROPOSER = '''import json,os
from pathlib import Path
out=Path(os.environ['NANORSI_PROPOSAL_DIR'])
(out/'proposal.diff').write_text('')
(out/'hypothesis.json').write_text(json.dumps({'hypothesis':'training updates the checkpoint; no source change proposed'}))
'''
CONFIG = '''[experiment]
schema_version = 2
id = "smoke"
goal = "Offline smoke fixture"
mode = "model"
seed = 0
arm = "frozen"
final_conditions = ["baseline", "candidate"]

[surface]
allow = ["target/**"]

[proposer]
command = ["python3", "proposer/propose.py"]

[evaluator]
command = ["python3", "evaluator/evaluate.py"]
primary_metric = "score"

[gate]
minimum_improvement = 0.1

[budget]
max_steps = 3
max_episodes = 40

[data]
manifest = "tasks/manifest.json"

[training]
command = ["python3", "trainer/train.py"]
compute_budget_s = 5
checkpoint = "target/model.json"
max_checkpoint_bytes = 1024
'''


def find_cli() -> str:
    cli = shutil.which("nanorsi") or shutil.which("nanorsi.exe")
    if not cli:
        print("nanorsi CLI not found on PATH. Install this repository first:\n"
              "  python -m pip install -e .")
        raise SystemExit(2)
    return cli


def build(root: Path) -> None:
    for name in ["target", "trainer", "evaluator", "proposer", "tasks", "adapters"]:
        (root / name).mkdir(parents=True)
    (root / "nanorsi.toml").write_text(CONFIG)
    (root / "target/model.json").write_text('{"weight": 0}')
    (root / "trainer/train.py").write_text(TRAINER)
    (root / "evaluator/evaluate.py").write_text(EVALUATOR)
    (root / "proposer/propose.py").write_text(PROPOSER)
    (root / "adapters/.keep").write_text("")
    rows = [{"task_id": s, "group_id": s, "split": s, "instruction": "predict",
             "input_files": {"x": "1"}, "expected_files": {"y": "1"}} for s in ["train", "validation", "test"]]
    (root / "tasks/manifest.json").write_text(json.dumps({"schema_version": 1, "tasks": rows}))
    (root / ".gitignore").write_text(".nanorsi/\nlineage.jsonl\nreports/\n__pycache__/\n")
    subprocess.run(["git", "init", "-q", str(root)], check=True)


def run(cli: str, *args: str) -> str:
    result = subprocess.run([cli, *args], capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(f"command failed: {' '.join(args)}")
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keep", action="store_true", help="keep the fixture workspace instead of deleting it")
    options = parser.parse_args()
    cli = find_cli()
    workspace = Path(tempfile.mkdtemp(prefix="nanorsi-smoke-")) / "lab"
    print("nanoRSI smoke — the smallest end-to-end RSI experiment (offline, no API)")
    print(f"1/7 building fixture workspace ... {workspace}")
    build(workspace)
    run(cli, "baseline", "--workspace", str(workspace))
    events = [json.loads(line) for line in (workspace / "lineage.jsonl").read_text().splitlines()]
    baseline = next(e for e in events if e.get("event_type") == "generation")
    print(f"2/7 baseline ... validation score {baseline['gate_metrics']['score']} (the starting system)")
    print("3/7 search: training proposes checkpoint updates; the gate keeps only strict validation gains")
    run(cli, "run", "--workspace", str(workspace))
    events = [json.loads(line) for line in (workspace / "lineage.jsonl").read_text().splitlines()]
    for e in events:
        if e.get("event_type") == "generation" and e.get("attempt_id"):
            print(f"      attempt {e['attempt_id']}: {e['decision']}"
                  f" ({e['parent_gate_metrics']['score']} -> {e['gate_metrics']['score']})")
    print("4/7 freeze ... choices locked; the test split stays unseen until now")
    run(cli, "freeze", "--workspace", str(workspace), "--repeats", "1")
    run(cli, "final-test", "--workspace", str(workspace))
    final = json.loads((workspace / "reports/final.json").read_text())
    print("5/7 final test on the held-out split:")
    for r in final["results"]:
        mean = sum(c["score"] for c in r["case_results"]) / max(1, len(r["case_results"]))
        print(f"      {r['condition']:9s} mean {mean}")
    audit = json.loads(run(cli, "audit", "--workspace", str(workspace)))
    print(f"6/7 audit ... leakage={len(audit['leakage'])}, silent bypass={len(audit['uninvoked_scripts'])}"
          f" (no skills surface in model mode)")
    revisions = [json.loads(line) for line in (workspace / "reports/evidence.jsonl").read_text().splitlines()]
    print(f"7/7 evidence ledger ... {len(revisions)} revisions recorded (diagnosis, diff, decision, integrity)")
    print("\nWhat just happened: a protected trainer updated real parameters, every candidate was")
    print("compared with its parent on validation, only strict improvements were kept, and the frozen")
    print("final test confirmed the gain on unseen tasks. That is the bounded core of RSI — nothing here")
    print("claims general recursive self-improvement.")
    if options.keep:
        print(f"\nWorkspace kept at {workspace} — open {workspace}/reports/report.md")
    else:
        shutil.rmtree(workspace.parent, ignore_errors=True)
        print("\nWorkspace cleaned up; re-run with --keep to inspect reports.")
    print("Next: docs/RSI_MINIMAL.md maps every mechanism to this repository's code.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
