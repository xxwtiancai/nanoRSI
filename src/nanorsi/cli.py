"""Command line: new → configure → evolve → freeze → judge → report / verify / doctor."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from . import harness, judge, recursion, report, tasks, templates
from .config import ConfigError, load_config
from .ledger import Ledger, LedgerError
from .model import Model, ModelError


def _workspace(args) -> Path:
    root = Path(args.workspace).resolve()
    if not (root / "nanorsi.toml").is_file():
        raise ConfigError(f"no nanorsi.toml in {root}")
    return root


def _set_key(text: str, section: str, key: str, value) -> str:
    rendered = json.dumps(value)  # JSON scalars and string arrays are valid TOML values
    pattern = re.compile(rf"(?ms)^\[{re.escape(section)}\]\n(.*?)(?=^\[|\Z)")
    match = pattern.search(text)
    if not match:
        return text.rstrip("\n") + f"\n\n[{section}]\n{key} = {rendered}\n"
    body = match.group(1)
    line = re.compile(rf"(?m)^{re.escape(key)}\s*=.*$")
    body = line.sub(f"{key} = {rendered}", body) if line.search(body) else body.rstrip("\n") + f"\n{key} = {rendered}\n"
    return text[:match.start(1)] + body + text[match.end(1):]


def cmd_configure(args) -> str:
    root = _workspace(args)
    path = root / "nanorsi.toml"
    if Ledger(root / ".nanorsi" / "ledger.jsonl").events():
        raise ConfigError("the ledger has started; model settings are frozen for this workspace")
    key_file = Path(args.api_key_file).expanduser()
    if not key_file.is_file():
        raise ConfigError(f"api key file not found: {key_file}")
    text = path.read_text(encoding="utf-8")
    for key, value in (("model", args.model), ("base_url", args.base_url), ("api_key_file", str(key_file)),
                       ("thinking", args.thinking), ("max_tokens", args.max_tokens)):
        if value is not None:
            text = _set_key(text, "model", key, value)
    path.write_text(text, encoding="utf-8")
    return f"configured model {args.model} at {args.base_url}"


def _open(args):
    root = _workspace(args)
    config = load_config(root / "nanorsi.toml")
    return root, config, Ledger(root / ".nanorsi" / "ledger.jsonl")


def _model(config) -> Model:
    return Model(config.model)


def cmd_evolve(args) -> dict:
    root, config, ledger = _open(args)
    if ledger.frozen():
        raise LedgerError("workspace is frozen; create a new workspace to evolve further")
    ledger.verify()
    all_tasks = tasks.load_tasks(root, config.tasks_manifest)
    chosen_tasks = tasks.select_tasks(all_tasks, args.tasks.split(",") if args.tasks else None, args.max_tasks)
    done = {row["task"] for row in ledger.events() if row.get("event") == "task_done"}
    base = harness.read_tree(root / config.harness_root)
    harness.validate(base)
    model = _model(config)
    session = recursion.Session(config, model, root, ledger)
    if not ledger.events():
        ledger.append("configured", experiment=config.experiment_id, mode=config.mode, k=config.k, seed=config.seed,
                      model=config.model.model, runner=config.runner.kind, harness=sorted(base), tasks=[t["task_id"] for t in all_tasks])
    outcomes = []
    for task in chosen_tasks:
        if task["task_id"] in done:
            outcomes.append({"task": task["task_id"], "status": "already done"})
            continue
        try:
            result = session.evolve_task({**task, "goal": config.goal}, base)
            outcomes.append({"task": task["task_id"], "chosen": result.chosen, "decisions": [d["decision"] for d in result.decisions]})
            print(f"[{task['task_id']}] done -> {result.chosen} ({', '.join(d['decision'] for d in result.decisions)})", flush=True)
        except recursion.BudgetExhausted as error:
            outcomes.append({"task": task["task_id"], "status": f"stopped: {error}"})
            print(f"[{task['task_id']}] {error}", flush=True)
            break
    report.write(root, ledger, config)
    return {"tasks": outcomes, "usage": ledger.usage()}


def cmd_freeze(args) -> dict:
    root, config, ledger = _open(args)
    ledger.verify()
    if ledger.frozen():
        return {"frozen": True, "note": "already frozen"}
    choices = {row["task"]: row["chosen"] for row in ledger.events() if row.get("event") == "task_done"}
    if not choices:
        raise LedgerError("nothing to freeze: run `nanorsi evolve` first")
    ledger.append("freeze", choices=choices, judge_model=config.judge_model)
    return {"frozen": True, "choices": choices}


def cmd_judge(args) -> dict:
    root, config, ledger = _open(args)
    ledger.verify()
    rows = judge.judge(config, root, tasks.load_tasks(root, config.tasks_manifest), ledger, bases=not args.no_bases)
    report.write(root, ledger, config)
    return {"graded": sum(r["graded"] for r in rows), "ungraded": sum(not r["graded"] for r in rows), "rows": rows}


def cmd_doctor(args) -> str:
    root, config, _ledger = _open(args)
    tree = harness.read_tree(root / config.harness_root)
    harness.validate(tree)
    task_list = tasks.load_tasks(root, config.tasks_manifest)
    lines = [f"harness: {len(tree)} components ok", f"tasks: {len(task_list)} ok", f"runner: {config.runner.kind}",
             f"judge: {'configured' if config.judge_command else 'not configured'}"]
    if args.check_model:
        text, usage = _model(config).call([{"role": "user", "content": "Reply with the single word OK."}], max_tokens=8)
        lines.append(f"model: replied {text!r} ({usage})")
    return "\n".join(lines)


def _parser():
    parser = argparse.ArgumentParser(prog="nanorsi", description="A minimal recursive harness-improvement loop.")
    sub = parser.add_subparsers(dest="command", required=True)
    new = sub.add_parser("new", help="create a workspace from the default template")
    new.add_argument("destination", type=Path)
    new.add_argument("--goal", default="Improve the harness for the task set")
    for name in ("configure", "evolve", "freeze", "judge", "report", "verify", "doctor"):
        command = sub.add_parser(name)
        command.add_argument("--workspace", type=Path, default=Path.cwd())
        if name == "configure":
            command.add_argument("--model", required=True)
            command.add_argument("--base-url", required=True)
            command.add_argument("--api-key-file", required=True)
            command.add_argument("--thinking", choices=["enabled", "disabled"])
            command.add_argument("--max-tokens", type=int)
        if name == "evolve":
            command.add_argument("--tasks", default="", help="comma list of task ids or domains")
            command.add_argument("--max-tasks", type=int, default=0)
        if name == "judge":
            command.add_argument("--no-bases", action="store_true")
        if name == "doctor":
            command.add_argument("--check-model", action="store_true")
    return parser


def main(argv=None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "new":
            files = templates.render(args.destination, goal=args.goal)
            print(f"created workspace with {len(files)} files; next: nanorsi configure --workspace {args.destination}")
            return 0
        if args.command == "verify":
            root, _config, ledger = _open(args)
            print(f"ledger: {ledger.verify()} events ok")
            return 0
        if args.command == "report":
            root, config, ledger = _open(args)
            print(report.write(root, ledger, config))
            return 0
        result = {"configure": cmd_configure, "evolve": cmd_evolve, "freeze": cmd_freeze,
                  "judge": cmd_judge, "doctor": cmd_doctor}[args.command](args)
        print(json.dumps(result, ensure_ascii=False, indent=1) if isinstance(result, dict) else result)
        return 0
    except (ConfigError, LedgerError, ModelError, harness.HarnessError, tasks.TaskError,
            judge.JudgeError, templates.TemplateError, recursion.BudgetExhausted) as error:
        print(f"nanorsi: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
