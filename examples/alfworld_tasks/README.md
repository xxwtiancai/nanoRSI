# ALFWorld agent-task pack (benchmark track, phase 2)

[ADOPTION item 37](../../docs/research/industry-rsi/ADOPTION.md), phase 2: **real agent
tasks** — the self-improving-agent literature's canonical benchmark (Reflexion, ExpeL,
SPEAR, RetireOPD, SkillWeaver all evaluate on it). Each task is one complete ALFWorld
text game ([MIT](NOTICE); games generated locally by `alfworld-download`, not
redistributed): the agent observes a room, explores, and manipulates objects
(take/heat/cool/clean/place/use) to complete a household goal. Success is the game
engine's own `won` flag — no custom scoring.

## What makes it a real RSI setup

- The **mutable surface is the skill file** `target/agent/skills/alfworld/SKILL.md`;
  the game runner, evaluator and adapters are authored by the generator and frozen at
  baseline. Evolution = the proposer rewrites the operating guidance from episode
  feedback (failed goals, wasted steps), and the strict-improvement gate accepts it
  only if the validation panel of held-out games improves. This mirrors the
  experience-to-guidance loops in the literature, inside nanoRSI's frozen contract.
- The frozen final panel reports the literature's split convention separately:
  **seen** layouts (valid_seen) and **unseen** layouts (valid_unseen).
- Deterministic pack: games are selected from the local ALFWorld cache by sorted path
  and stride (4 train / 6 validation from the train split; 6 seen + 6 unseen test).
  `prepare.py` is the sole generator; never hand-edit the manifest.

## Requirements and run

```bash
# once per machine: Python 3.12 + alfworld (textworld breaks on 3.13 / PEP 667)
conda create -y -n alf312 python=3.12 && conda run -n alf312 pip install alfworld pyyaml
SDKROOT=$(ls /Library/Developer/CommandLineTools/SDKs/MacOSX1*.sdk | tail -1) \
  conda run -n alf312 pip install jericho   # if the wheel build fails on a new SDK
alfworld-download                              # ~/.cache/alfworld/json_2.1.1

python examples/alfworld_tasks/prepare.py /tmp/alf-out
nanorsi new skills ./alf-lab --goal "Improve the ALFWorld operating skill in target/agent/skills/alfworld/SKILL.md from episode feedback. Propose unified diffs to that file only."
cp /tmp/alf-out/alfworld/manifest.json            ./alf-lab/tasks/manifest.json
cp /tmp/alf-out/alfworld/target/agent/run.py      ./alf-lab/target/agent/run.py
cp -r /tmp/alf-out/alfworld/target/agent/skills/alfworld ./alf-lab/target/agent/skills/
cp /tmp/alf-out/alfworld/evaluator/evaluate.py    ./alf-lab/evaluator/evaluate.py
cd alf-lab
# raise [agent] timeout_s to 120 and [evaluator] timeout_s to 5400 in nanorsi.toml
git add -A && git commit -m "ALFWorld pack"
nanorsi configure --workspace . --model YOUR_MODEL --base-url YOUR_URL \
  --api-key-file /absolute/external/path --max-steps 3 --max-episodes 60
nanorsi doctor --workspace . --check-model
nanorsi baseline --workspace .   # ~10 real episodes (offline engine, live agent)
nanorsi run --workspace .        # gated skill evolution
nanorsi freeze --workspace . --repeats 1
nanorsi final-test --workspace . # 12 frozen games: 6 seen + 6 unseen layouts
nanorsi report --workspace . && nanorsi verify --workspace . && nanorsi audit --workspace .
```

Each episode is up to 24 agent turns (WALL limit 880 s); expect roughly one model call
per turn and a few minutes per episode. The runner re-execs itself under
`NANORSI_ALF_PYTHON` (default `/opt/miniconda3/envs/alf312/bin/python`); the bridge
and evaluator stay on the workspace interpreter.

## Honesty boundaries

Skill evolution here improves *guidance loaded into context*, not the model or the
runner; the runner and evaluator are frozen after baseline, audited by the standard
machinery, and `won` comes from the game engine. Games are not redistributed; packs
regenerate from the local ALFWorld cache, so results depend on the upstream
`json_2.1.1` data snapshot. Author-reported ALFWorld numbers (ReAct, Reflexion, ExpeL
and others use different splits, models and step budgets) are **not** reproduced;
these are independent nanoRSI runs on a small deterministic subset. The known
workspace trust boundary applies: a workspace-local proposer can read
`tasks/manifest.json` (game paths, not answers — the winning action sequence is only
knowable by playing).

The 2026-10-11 live study: [results/alfworld-phase2](../results/alfworld-phase2/README.md).
