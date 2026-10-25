"""Reports are derived views over the ledger: per-task decisions, contrasts, judged
scores, budget. They select nothing and are regenerated from scratch each time."""
from __future__ import annotations

import json
from pathlib import Path


def _partial(score) -> float | None:
    if not score or not score.get("n_criteria"):
        return None
    return score["n_passed"] / score["n_criteria"]


def summarize(ledger) -> dict:
    events = ledger.events()
    tasks: dict[str, dict] = {}
    for row in events:
        task = row.get("task")
        if not task:
            continue
        entry = tasks.setdefault(task, {"proposals": 0, "contrasts": {"mitigates": 0, "neutral": 0, "regresses": 0},
                                        "decisions": [], "chosen": "", "lesson": None, "scores": {}})
        kind = row["event"]
        if kind == "proposal":
            entry["proposals"] += 1
        elif kind == "contrast":
            entry["contrasts"][row.get("contrast", "neutral")] = entry["contrasts"].get(row.get("contrast", "neutral"), 0) + 1
        elif kind == "compose":
            entry["decisions"].append({"decision": row.get("decision"), "observation": row.get("observation", "")[:240], "files": row.get("files", [])})
        elif kind == "task_done":
            entry["chosen"] = row.get("chosen", "")
        elif kind == "experience":
            entry["lesson"] = (row.get("lesson") or {}).get("lesson")
        elif kind == "judged" and row.get("graded"):
            entry["scores"][row["role"]] = {**row["score"], "partial": _partial(row["score"])}
    graded = [t for t in tasks.values() if "base" in t["scores"] and "final" in t["scores"]]
    means = {}
    if graded:
        means = {"base": sum(t["scores"]["base"]["partial"] for t in graded) / len(graded),
                 "final": sum(t["scores"]["final"]["partial"] for t in graded) / len(graded), "n": len(graded)}
        means["delta_pp"] = (means["final"] - means["base"]) * 100
        means["wins"] = sum(t["scores"]["final"]["partial"] > t["scores"]["base"]["partial"] for t in graded)
        means["ties"] = sum(t["scores"]["final"]["partial"] == t["scores"]["base"]["partial"] for t in graded)
        means["losses"] = len(graded) - means["wins"] - means["ties"]
    return {"tasks": tasks, "means": means, "usage": ledger.usage(), "frozen": ledger.frozen(), "events": len(events)}


def render(summary: dict, config) -> str:
    lines = [f"# nanoRSI report — {config.experiment_id}", "",
             f"mode `{config.mode}` · k={config.k} · model `{config.model.model}` · runner `{config.runner.kind}` · "
             f"{'frozen' if summary['frozen'] else 'not frozen'} · {summary['events']} ledger events", ""]
    means = summary["means"]
    if means:
        lines += [f"**Judged (n={means['n']}): base {means['base']:.3f} → final {means['final']:.3f} partial, "
                  f"{means['delta_pp']:+.1f} pp, {means['wins']}W/{means['ties']}T/{means['losses']}L**", ""]
    lines += ["| task | proposals | mitigates / neutral / regresses | decisions | chosen | base | final |",
              "| --- | ---: | --- | --- | --- | ---: | ---: |"]
    for task_id, entry in summary["tasks"].items():
        c = entry["contrasts"]
        base = entry["scores"].get("base", {}).get("partial")
        final = entry["scores"].get("final", {}).get("partial")
        fmt = lambda v: "—" if v is None else f"{v:.3f}"
        lines.append(f"| {task_id} | {entry['proposals']} | {c.get('mitigates', 0)} / {c.get('neutral', 0)} / {c.get('regresses', 0)} | "
                     f"{', '.join(d['decision'] for d in entry['decisions']) or '—'} | {entry['chosen'] or '—'} | {fmt(base)} | {fmt(final)} |")
    use = summary["usage"]
    lines += ["", f"Budget used: {use['rollouts']} rollouts · {use['proposer_calls']} improver calls · "
              f"{use['input_tokens']:,} input / {use['output_tokens']:,} output tokens", ""]
    lessons = [(t, e["lesson"]) for t, e in summary["tasks"].items() if e.get("lesson")]
    if lessons:
        lines += ["## Lessons in the library", ""] + [f"- **{t}**: {lesson}" for t, lesson in lessons] + [""]
    return "\n".join(lines)


def write(workspace: Path, ledger, config) -> Path:
    summary = summarize(ledger)
    out = Path(workspace) / "reports"
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    path = out / "report.md"
    path.write_text(render(summary, config), encoding="utf-8")
    return path
