"""Build a nanoRSI workspace that runs LAB tasks through OpenCode via runner.py/judge.py.

Usage (paths default to the harness2 checkout layout used in this repo's studies):
  python examples/lab_opencode/prepare.py ./lab-ws \
      --tasks employment-labor/identify-issues-in-counterparty-motion-brief,... \
      --harness2-root .omx/harness2 --model zai/glm-5.3 --judge-model custom/glm-5.3 \
      --api-key-file ~/.nanorsi/keys/glm-coding-plan.key

The base harness is LAB's own system prompt with the other always-on files empty —
the same starting point the harness2 code uses — so base rollouts are comparable."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

TOML = """[experiment]
id = "lab-opencode"
goal = "Improve the agent harness for professional legal document work on LAB"
mode = "{mode}"
k = {k}
seed = 0

[model]
model = "{chat_model}"
base_url = "{base_url}"
api_key_file = "{api_key_file}"
max_tokens = 8192
timeout_s = 900
thinking = "disabled"

[runner]
kind = "command"
command = [{python}, {runner}]
timeout_s = {runner_timeout}

[harness]
root = "harness"

[tasks]
manifest = "tasks/manifest.json"

[judge]
command = [{python}, {judge}]
model = "{judge_model}"

[budget]
max_proposer_calls = {max_calls}
max_rollouts = {max_rollouts}
max_output_bytes = 4000000
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--tasks", required=True, help="comma list of LAB task ids (practice-area/slug)")
    parser.add_argument("--harness2-root", type=Path, default=Path(".omx/harness2"))
    parser.add_argument("--xdg-config", type=Path, default=Path(".omx/xdg-config"))
    parser.add_argument("--shim-bin", type=Path, default=Path(".omx/bin"))
    parser.add_argument("--model", default="zai/glm-5.3", help="OpenCode provider/model for the executor")
    parser.add_argument("--chat-model", default="glm-5.3", help="bare model id for the improver (chat completions)")
    parser.add_argument("--base-url", default="https://api.z.ai/api/coding/paas/v4")
    parser.add_argument("--judge-model", default="custom/glm-5.3")
    parser.add_argument("--api-key-file", default="~/.nanorsi/keys/glm-coding-plan.key")
    parser.add_argument("--mode", choices=["agg", "seq"], default="agg")
    parser.add_argument("--k", type=int, default=1)
    parser.add_argument("--max-rollouts", type=int, default=40)
    parser.add_argument("--max-calls", type=int, default=80)
    args = parser.parse_args()
    dest = args.destination
    if dest.exists():
        sys.exit(f"destination exists: {dest}")
    h2 = args.harness2_root.resolve()
    lab_root = h2 / "dependencies" / "harvey-labs"
    base_prompt = lab_root / "harness" / "system_prompt.md"
    if not base_prompt.is_file():
        sys.exit(f"LAB checkout not found at {lab_root}; run harness2-setup lab first")
    tasks = []
    for task_id in [t.strip() for t in args.tasks.split(",") if t.strip()]:
        cfg = json.loads((lab_root / "tasks" / task_id / "task.json").read_text(encoding="utf-8"))
        tasks.append({"task_id": task_id, "domain": task_id.split("/")[0], "instruction": cfg["instructions"],
                      "documents": {}, "deliverables": list(cfg.get("deliverables", {})) or ["response.md"],
                      "extra": {"title": cfg["title"], "n_criteria": len(cfg["criteria"])}})
    (dest / "tasks").mkdir(parents=True)
    (dest / "tasks" / "manifest.json").write_text(json.dumps({"schema_version": 1, "tasks": tasks}, ensure_ascii=False, indent=1), encoding="utf-8")
    harness = dest / "harness"
    harness.mkdir()
    shutil.copyfile(base_prompt, harness / "systemprompt.md")
    for name in ("guardrails.md", "memory.md", "tool_guidance.md"):
        (harness / name).write_text("", encoding="utf-8")
    settings = {"lab_root": str(lab_root), "lab_python": str(lab_root / ".venv" / "bin" / "python"),
                "bun": str(h2 / "dependencies" / "tools" / "node_modules" / ".bin" / "bun"),
                "opencode_dir": str(h2 / "dependencies" / "opencode"), "xdg_config_home": str(args.xdg_config.resolve()),
                "shim_bin": str(args.shim_bin.resolve()), "model": args.model, "judge_model": args.judge_model,
                "judge_base_url": args.base_url, "api_key_file": args.api_key_file, "rollout_timeout_s": 3600}
    (dest / "lab_opencode.json").write_text(json.dumps(settings, indent=1), encoding="utf-8")
    (dest / "nanorsi.toml").write_text(TOML.format(
        mode=args.mode, k=args.k, chat_model=args.chat_model, base_url=args.base_url,
        api_key_file=str(Path(args.api_key_file).expanduser()), python=json.dumps(sys.executable),
        runner=json.dumps(str(HERE / "runner.py")), judge=json.dumps(str(HERE / "judge.py")),
        judge_model=args.judge_model, runner_timeout=4500, max_calls=args.max_calls, max_rollouts=args.max_rollouts),
        encoding="utf-8")
    print(f"workspace {dest}: {len(tasks)} LAB tasks, base harness = LAB system prompt + empty guardrails/memory/tool_guidance")
    return 0


if __name__ == "__main__":
    sys.exit(main())
