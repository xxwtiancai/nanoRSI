"""Propose and Compose: the improver edits the harness from execution evidence.

Two candidate dimensions per round, as in the paper — INV targets a cross-domain
agentic deficiency, DOM a domain-specific one — each edit touches exactly one
component. Compose reconciles probed candidates into the next harness and must
tie every decision to a concrete observation."""
from __future__ import annotations

from dataclasses import dataclass, field

from . import harness
from .model import ModelError, ask

EXCERPT = 6000
DIMS = ("INV", "DOM")


def clip(text: str, limit: int = EXCERPT) -> str:
    text = text or ""
    return text if len(text) <= limit else text[:limit] + f"\n…(truncated {len(text) - limit} chars)"


@dataclass
class Candidate:
    dim: str
    component: str
    note: str
    tree: dict
    usage: dict = field(default_factory=dict)
    error: str = ""

    def record(self) -> dict:
        return {"dim": self.dim, "component": self.component, "note": self.note, "usage": self.usage, "error": self.error}


PROPOSE_SYSTEM = (
    "You improve an agent harness by editing exactly ONE component. Reply with one JSON header line "
    '{"component": "<path>", "note": "<one-line hypothesis tied to an observation in the evidence>"} '
    "followed by ONE fenced block holding the COMPLETE new content of that component. Editable components: "
    "systemprompt.md, guardrails.md, memory.md, tool_guidance.md, skills/<slug>/SKILL.md (first line: "
    "description), scripts/<slug>.py. Write reusable guidance; never embed answers, names or figures copied "
    "from the task documents. Keep the component under 120 lines."
)
GUIDANCE = {
    "INV": "Fix ONE cross-domain agentic deficiency visible in the reference execution (planning, tool "
           "discipline, verification, output hygiene). Nothing domain-specific.",
    "DOM": "Fix ONE domain-specific weakness of the deliverable for this kind of professional work "
           "(structure, sourcing, precision the domain expects).",
}


def _rollout_view(rollout) -> str:
    deliverables = "\n\n".join(f"----- {name} -----\n{clip(text, 3000)}" for name, text in rollout.deliverables.items()) or "(no deliverable)"
    status = "" if rollout.ok else f"\n(status: {rollout.error or 'incomplete'})"
    return f"## trajectory{status}\n{clip(rollout.trajectory)}\n\n## deliverables\n{deliverables}"


def _context(task, tree, reference, rejected, lessons) -> str:
    parts = [f"# GOAL\n{task.get('goal', '')}".rstrip(), f"# TASK\n{task['instruction']}",
             "# CURRENT HARNESS\n" + harness.describe(tree), "# REFERENCE EXECUTION\n" + _rollout_view(reference)]
    if lessons:
        parts.append("# LESSONS FROM EARLIER TASKS\n" + "\n".join(f"- {line}" for line in lessons[-8:]))
    if rejected:
        parts.append("# RECENTLY REJECTED EDITS (do not repeat)\n" + "\n".join(f"- {line}" for line in rejected[-5:]))
    return "\n\n".join(parts)


def propose(model, dim: str, task: dict, tree: dict, reference, *, rejected=(), lessons=()) -> Candidate:
    user = _context(task, tree, reference, list(rejected), list(lessons)) + f"\n\n# YOUR JOB ({dim})\n{GUIDANCE[dim]}"
    usage_total = {"calls": 0, "input_tokens": 0, "output_tokens": 0}
    error = ""
    for attempt in range(2):
        try:
            header, bodies, usage = ask(model, PROPOSE_SYSTEM, user + (f"\n\n# PREVIOUS ATTEMPT REJECTED\n{error}" if error else ""))
            for key in usage_total:
                usage_total[key] += usage.get(key, 0)
            component = str(header.get("component", ""))
            if not bodies or not bodies[0].strip():
                raise harness.HarnessError("no fenced component body in reply")
            new_tree = harness.apply_edit(tree, component, bodies[0])
            if not harness.changed(tree, new_tree):
                raise harness.HarnessError("edit left the harness unchanged")
            return Candidate(dim, component, str(header.get("note", ""))[:300], new_tree, usage_total)
        except (ModelError, harness.HarnessError) as failure:
            error = str(failure)
    return Candidate(dim, "", "", dict(tree), usage_total, error=f"proposal failed: {error}")


COMPOSE_SYSTEM = (
    "You compose the next harness from probe evidence. Reply with one JSON header line "
    '{"decision": "adopt_inv|adopt_dom|merge|keep", "observation": "<decision tied to the contrasts>", '
    '"files": ["<component>", ...]} and then, for EVERY listed file in order, one fenced block with its COMPLETE '
    "content. For adopt_inv / adopt_dom the chosen candidate's edit is applied for you — list files only for "
    "additional changes (e.g. memory.md recording a lesson the contrasts support). For merge, list and supply "
    "every merged component. Rules: adopt only edits whose contrast is mitigates; keep beats adopting neutral "
    "or regressing edits; merge only when both candidates mitigate and touch different components."
)


def compose(model, task: dict, base: dict, candidates: list, contrasts: dict, reference) -> tuple[dict, dict]:
    """Return (decision record, new tree). A failed call keeps the base harness."""
    lines = [f"# TASK\n{task['instruction']}", "# BASE HARNESS\n" + harness.describe(base)]
    for cand in candidates:
        verdict = contrasts.get(cand.dim, {})
        lines.append(f"# CANDIDATE {cand.dim} ({cand.component})\nnote: {cand.note}\ncontrast: {verdict.get('contrast', 'unavailable')}\n"
                     f"observation: {verdict.get('observation', '')}\nnew content:\n{clip(cand.tree.get(cand.component, ''), 3000)}")
    lines.append("# REFERENCE TRAJECTORY\n" + clip(reference.trajectory, 3000))
    usage_total = {"calls": 0, "input_tokens": 0, "output_tokens": 0}
    error = ""
    for attempt in range(2):
        try:
            header, bodies, usage = ask(model, COMPOSE_SYSTEM, "\n\n".join(lines) + (f"\n\n# PREVIOUS ATTEMPT REJECTED\n{error}" if error else ""))
            for key in usage_total:
                usage_total[key] += usage.get(key, 0)
            decision = str(header.get("decision", ""))
            if decision not in {"adopt_inv", "adopt_dom", "merge", "keep"}:
                raise harness.HarnessError(f"unknown decision {decision!r}")
            files = header.get("files") if isinstance(header.get("files"), list) else []
            by_dim = {cand.dim: cand for cand in candidates}
            if decision in {"adopt_inv", "adopt_dom"}:
                # Adopting a candidate means taking its probed tree; bodies are optional
                # overrides (e.g. a memory.md lesson) and must never be required.
                chosen = by_dim.get(decision[-3:].upper())
                if chosen is None or chosen.error:
                    raise harness.HarnessError(f"{decision} names a candidate that does not exist or failed")
                tree = dict(chosen.tree)
            else:
                if decision == "merge" and (not files or len(bodies) < len(files)):
                    raise harness.HarnessError(f"merge lists {len(files)} files but {len(bodies)} bodies arrived")
                tree = dict(base)
            for name, body in zip(files, bodies):
                tree = harness.apply_edit(tree, str(name), body)
            record = {"decision": decision, "observation": str(header.get("observation", ""))[:600],
                      "files": [str(f) for f in files], "usage": usage_total}
            return record, (base if decision == "keep" else tree)
        except (ModelError, harness.HarnessError) as failure:
            error = str(failure)
    return {"decision": "keep", "observation": f"compose failed: {error}", "files": [], "usage": usage_total, "error": error}, dict(base)
