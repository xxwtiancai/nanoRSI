"""Minimal Harness2 (arXiv 2610.14224) task-level recursion on LAB, GLM-5.3 executor.

Per task, k=1: reference run under the current harness -> propose one INVARIANT
and one DOMAIN candidate edit -> probe both under matched configuration ->
classify each behavioral contrast (mitigates/neutral/regresses, no ground truth)
-> compose (adopt/merge/keep, every decision tied to an observation) -> final
run. Baseline arm runs the unmodified harness. LAB's own rubric judge scores
both arms; the paper's GLM-5/OpenCode LAB-partial gain (+11.8pp) is the
reference magnitude. Mechanism shapes follow the paper; no upstream code.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from agent import AgentConfig, Execution, ModelError, chat, execute_task, parse_reply  # noqa: E402
import lab  # noqa: E402

EDITABLE = ("systemprompt.md", "tool_guidance.md", "LongTermMEMORY.md")
EXCERPT = 6000
JUDGE_MODEL = "custom/glm-5.3"


def clip(text, limit=EXCERPT):
    text = text or ""
    return text if len(text) <= limit else text[:limit] + f"\n…(truncated {len(text) - limit} chars)"


def harness_view(harness_files):
    return "\n\n".join(f"=== {name} ===\n{body}" for name, body in sorted(harness_files.items()))


def one_call(config, api_key, system, user, max_tokens=4096):
    content, usage = chat(config, [{"role": "system", "content": system},
                                   {"role": "user", "content": user}], api_key, max_tokens)
    return content, usage


PROPOSE_SYSTEM = (
    "You improve an agent harness by editing exactly ONE component file. Reply with one JSON "
    'header line {"component": "<file>", "note": "<one-line hypothesis>"} followed by ONE '
    "fenced markdown block containing the COMPLETE new content of that file. Editable "
    "components: systemprompt.md, tool_guidance.md, LongTermMEMORY.md, or a new "
    "skills/<slug>/SKILL.md (first line must be a one-line description). Keep the file under "
    "120 lines. Never embed task-specific expected answers, names or numbers you saw in the "
    "documents; write reusable guidance only."
)


def propose(config, api_key, dim, task, harness_files, reference):
    guidance = {
        "INV": "Propose ONE cross-domain agentic deficiency fix: a weakness any task of this "
               "kind shares (planning, tool discipline, output hygiene). No legal-domain specifics.",
        "DOM": "Propose ONE domain-specific improvement for professional legal document work "
               "(structure, sourcing, precision expected in legal deliverables).",
    }[dim]
    user = "\n\n".join([
        f"# TASK\n{task['title']}\n\n{task['instructions']}",
        "# CURRENT HARNESS\n" + harness_view(harness_files),
        "# REFERENCE EXECUTION (current harness, this task)",
        "## trajectory\n" + clip(reference["trajectory"]),
        "## deliverable\n" + clip(reference["deliverable_text"] or "(none)"),
        f"# YOUR JOB ({dim})\n{guidance}",
    ])
    content, usage = one_call(config, api_key, PROPOSE_SYSTEM, user)
    head, body = parse_reply(content)
    component = head.get("component", "")
    valid = component in EDITABLE or (component.startswith("skills/") and component.endswith("SKILL.md"))
    if not valid or not body.strip():
        raise ModelError(f"invalid proposal header: {head}")
    return {"dim": dim, "component": component, "note": str(head.get("note", ""))[:200],
            "content": body.strip(), "usage": usage}


CONTRAST_SYSTEM = (
    "You compare two executions of the same task by the same agent model under matched "
    "configuration; the only difference is the harness. Classify the behavioral contrast of the "
    "CANDIDATE relative to the REFERENCE: mitigates (clearly reduces an execution problem or "
    "deliverable defect seen in the reference), neutral (no meaningful difference), regresses "
    "(clearly worse). Ignore length and styling alone. Reply exactly one JSON line: "
    '{"contrast": "mitigates|neutral|regresses", "observation": "<concrete observation>"}'
)


def contrast(config, api_key, task, reference, probe, candidate):
    user = "\n\n".join([
        f"# TASK\n{task['title']}\n\n{task['instructions']}",
        f"# CANDIDATE EDIT ({candidate['dim']}, {candidate['component']})\n{candidate['note']}",
        "# REFERENCE EXECUTION\n## trajectory\n" + clip(reference["trajectory"], 4000)
        + "\n## deliverable\n" + clip(reference["deliverable_text"], 4000),
        "# CANDIDATE EXECUTION\n## trajectory\n" + clip(probe["trajectory"], 4000)
        + "\n## deliverable\n" + clip(probe["deliverable_text"], 4000),
    ])
    content, usage = one_call(config, api_key, CONTRAST_SYSTEM, user)
    head, _ = parse_reply(content)
    verdict = head.get("contrast")
    if verdict not in {"mitigates", "neutral", "regresses"}:
        raise ModelError(f"invalid contrast verdict: {head}")
    return {"dim": candidate["dim"], "component": candidate["component"],
            "contrast": verdict, "observation": str(head.get("observation", ""))[:400], "usage": usage}


COMPOSE_SYSTEM = (
    "You compose the final harness from probe evidence. Reply with one JSON header line "
    '{"decision": "adopt_inv|adopt_dom|merge|keep", "observation": "<decision tied to concrete '
    'observations>", "files": ["<component>", ...]} followed, for EVERY file in files, by a line '
    "===FILE <name>=== and one fenced markdown block with that file's COMPLETE content. Rules: "
    "only adopt edits whose contrast is mitigates; keep beats adopting neutral or regressing "
    "edits; merge only when the adopted edits touch different components and both mitigate."
)


def compose(config, api_key, task, harness_files, candidates, contrasts, reference):
    lines = [f"# TASK\n{task['title']}", "# BASE HARNESS\n" + harness_view(harness_files)]
    for cand in candidates:
        c = contrasts[cand["dim"]]
        lines.append(f"# CANDIDATE {cand['dim']} ({cand['component']})\nedit note: {cand['note']}\n"
                     f"contrast: {c['contrast']}\nobservation: {c['observation']}\n"
                     f"new content:\n{clip(cand['content'], 3000)}")
    lines.append("# REFERENCE TRAJECTORY\n" + clip(reference["trajectory"], 3000))
    content, usage = one_call(config, api_key, COMPOSE_SYSTEM, "\n\n".join(lines))
    head, _ = parse_reply(content)
    decision = head.get("decision")
    if decision not in {"adopt_inv", "adopt_dom", "merge", "keep"}:
        raise ModelError(f"invalid compose decision: {head}")
    listed = head.get("files") if isinstance(head.get("files"), list) else []
    marker_block = re.compile(r"===FILE\s+([\w./-]+)===\s*```[a-zA-Z0-9_-]*\n(.*?)```", re.S)
    blocks = {name.strip(): body.strip() for name, body in marker_block.findall(content)}
    missing = [name for name in listed if name not in blocks or not blocks[name]]
    if missing:
        # Tolerant fallback: models often emit the files as plain fenced blocks
        # in the listed order, without the ===FILE name=== markers.
        remainder = marker_block.sub("", content)
        fences = [body.strip() for body in re.findall(r"```[a-zA-Z0-9_-]*\n(.*?)```", remainder, re.S)]
        if len(fences) == len(missing):
            for name, body in zip(missing, fences):
                blocks[name] = body
    files = {}
    for name in listed:
        if name not in blocks or not blocks[name]:
            raise ModelError(f"compose lists {name} but no complete FILE block found")
        files[name] = blocks[name]
    if decision != "keep" and not files:
        raise ModelError(f"decision {decision} without files")
    return {"decision": decision, "observation": str(head.get("observation", ""))[:600],
            "files": files, "usage": usage}


def run_execution(label, config, api_key, task, harness_files, bind_reader, convert, runs_dir, writer):
    run_dir = Path(runs_dir) / label
    run_dir.mkdir(parents=True, exist_ok=True)
    bind_reader(task)
    execution = execute_task(config, task, harness_files, convert=convert, api_key=api_key)
    for filename, markdown in execution.deliverables.items():
        writer(run_dir, filename, markdown)
    (run_dir / "trajectory.md").write_text(execution.trajectory, encoding="utf-8")
    record = {"label": label, "run_dir": str(run_dir), "ok": execution.ok, "turns": execution.turns,
              "usage": execution.usage, "error": execution.error,
              "trajectory": execution.trajectory, "deliverable_text": lab.deliverable_text(run_dir)}
    return record


def partial(score):
    if not score or not score.get("n_criteria"):
        return None
    return score["n_passed"] / score["n_criteria"]


def process_task(args, config, api_key, task_name, ledger):
    events = {"usage": {"input_tokens": 0, "output_tokens": 0, "model_calls": 0}}

    def spend(usage):
        for key in events["usage"]:
            events["usage"][key] += usage.get(key) or 0

    def log(phase, event, **fields):
        row = {"ts": time.strftime("%H:%M:%S"), "task": task_name,
               "phase": phase, "event": event, **fields}
        ledger.write(json.dumps(row, ensure_ascii=False) + "\n")
        ledger.flush()
        print(f"[{task_name}] {phase} {event}", flush=True)

    bind_reader, convert = lab.document_reader(args.lab_root, args.lab_python)
    task = lab.load_task(args.lab_root, task_name)
    writer = lab.write_deliverable
    base_harness = load_base_harness()
    rows = {}

    def execute(label, harness_files):
        record = run_execution(f"{task_name}/{label}", config, api_key, task, harness_files,
                               bind_reader, convert, args.runs_dir, writer)
        spend(record["usage"])
        log(phase="exec", event=label, ok=record["ok"], turns=record["turns"], error=record["error"],
            usage=record["usage"])
        return record

    def judged(record, label):
        score = lab.judge(args.lab_root, args.lab_python, record["run_dir"], task_name,
                          JUDGE_MODEL, api_key, config.base_url)
        log(phase="judge", event=label, score=score)
        return score

    if args.arm in {"baseline", "both"}:
        base = execute("baseline", base_harness)
        rows["baseline"] = {"partial": partial(judged(base, "baseline")), "score_ok": base["ok"],
                            "usage": base["usage"]}
    if args.arm in {"recursion", "both"}:
        reference = execute("reference", base_harness)
        if args.judge_reference:
            rows["reference"] = {"partial": partial(judged(reference, "reference")),
                                 "score_ok": reference["ok"], "usage": reference["usage"]}
        candidates, contrasts = [], {}
        for dim in ("INV", "DOM"):
            try:
                cand = propose(config, api_key, dim, task, base_harness, reference)
                spend(cand["usage"])
                candidates.append(cand)
                log(phase="propose", event=dim, component=cand["component"], note=cand["note"])
            except ModelError as error:
                log(phase="propose", event=dim, error=str(error))
                continue
        for cand in candidates:
            probe_harness = dict(base_harness)
            probe_harness[cand["component"]] = cand["content"]
            probe = execute(f"probe-{cand['dim'].lower()}", probe_harness)
            try:
                contrasts[cand["dim"]] = contrast(config, api_key, task, reference, probe, cand)
                spend(contrasts[cand["dim"]]["usage"])
                log(phase="contrast", event=cand["dim"], **{k: v for k, v in contrasts[cand["dim"]].items() if k != "usage"})
            except ModelError as error:
                contrasts[cand["dim"]] = {"contrast": "neutral", "observation": f"contrast call failed: {error}"}
                log(phase="contrast", event=cand["dim"], error=str(error))
        decision, final_harness, compose_error = None, None, None
        for attempt in range(2):
            try:
                decision = compose(config, api_key, task, base_harness, candidates, contrasts, reference)
                spend(decision["usage"])
                log(phase="compose", event=decision["decision"], observation=decision["observation"])
                final_harness = dict(base_harness)
                final_harness.update(decision["files"]) if decision["decision"] != "keep" else None
                break
            except ModelError as error:
                compose_error = error
        if decision is None:
            log(phase="compose", event="failed", error=str(compose_error))
            decision = {"decision": "keep", "observation": f"compose failed: {compose_error}", "files": {}}
            final_harness = base_harness
        if decision["decision"] == "keep":
            final = reference
            log(phase="exec", event="final(kept reference)")
        else:
            final = execute("final", final_harness)
        rows["recursion"] = {"partial": partial(judged(final, "final")), "score_ok": final["ok"],
                             "decision": decision["decision"], "observation": decision["observation"],
                             "usage": events["usage"]}
    rows["usage"] = events["usage"]
    return rows


def load_base_harness():
    directory = Path(__file__).resolve().parent / "harness"
    files = {}
    for path in sorted(directory.rglob("*")):
        if path.is_file():
            files[path.relative_to(directory).as_posix()] = path.read_text(encoding="utf-8")
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lab-root", default=".omx/harness2/dependencies/harvey-labs")
    parser.add_argument("--lab-python", default=".omx/harness2/dependencies/harvey-labs/.venv/bin/python")
    parser.add_argument("--runs-dir", default=".omx/harness2_minimal_runs")
    parser.add_argument("--tasks", default="", help="comma-separated domain/task names")
    parser.add_argument("--domain", default="", help="pick N tasks from one practice area")
    parser.add_argument("--max-tasks", type=int, default=0)
    parser.add_argument("--arm", choices=["baseline", "recursion", "both"], default="both")
    parser.add_argument("--judge-reference", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--model", default="glm-5.3")
    args = parser.parse_args()
    if args.tasks:
        names = [name.strip() for name in args.tasks.split(",") if name.strip()]
    elif args.domain:
        names = lab.list_tasks(args.lab_root, args.domain)
    else:
        parser.error("pass --tasks or --domain")
    if args.max_tasks:
        names = names[:args.max_tasks]
    args.lab_root = str(Path(args.lab_root).resolve())
    # absolute() on purpose: the LAB venv python is a symlink into uv's managed
    # interpreter, and resolve() would strip it, executing the base interpreter
    # without the venv's site-packages.
    args.lab_python = str(Path(args.lab_python).absolute())
    args.runs_dir = str(Path(args.runs_dir).resolve())
    Path(args.runs_dir).mkdir(parents=True, exist_ok=True)
    config = AgentConfig(model=args.model)
    api_key = __import__("agent").load_api_key(config)
    ledger_path = Path(args.runs_dir) / "ledger.jsonl"
    ledger = ledger_path.open("a", encoding="utf-8")
    summary = {}
    for name in names:
        summary[name] = process_task(args, config, api_key, name, ledger)
        (Path(args.runs_dir) / "summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    ledger.close()


if __name__ == "__main__":
    main()
