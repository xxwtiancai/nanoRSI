"""Probe: rerun a candidate under matched configuration and classify the behavioral
contrast against the reference — mitigates / neutral / regresses — with no ground
truth. This is the gate: only `mitigates` edits may be adopted."""
from __future__ import annotations

from .model import ModelError, ask
from .propose import clip

VERDICTS = ("mitigates", "neutral", "regresses")

CONTRAST_SYSTEM = (
    "You compare two executions of the same task by the same model under matched configuration; only the "
    "harness differs. Classify the CANDIDATE relative to the REFERENCE: mitigates (clearly reduces an execution "
    "problem or deliverable defect visible in the reference), neutral (no meaningful difference), regresses "
    "(clearly worse, including a missing or broken deliverable). Ignore length and styling alone. Reply with "
    'exactly one JSON line: {"contrast": "mitigates|neutral|regresses", "observation": "<the concrete '
    'observation that decides it>"}'
)


def _view(rollout, limit=4000) -> str:
    deliverables = "\n\n".join(f"----- {name} -----\n{clip(text, limit)}" for name, text in rollout.deliverables.items()) or "(no deliverable)"
    status = "" if rollout.ok else f" (status: {rollout.error or 'incomplete'})"
    return f"## trajectory{status}\n{clip(rollout.trajectory, limit)}\n\n## deliverables\n{deliverables}"


def contrast(model, task: dict, reference, probe, candidate) -> dict:
    """Return {contrast, observation, usage}. A failed call reads as neutral and says so."""
    if not probe.delivered and reference.delivered:
        return {"contrast": "regresses", "observation": f"candidate produced no deliverable ({probe.error or 'none'}); reference did", "usage": {}}
    user = "\n\n".join([
        f"# TASK\n{task['instruction']}",
        f"# CANDIDATE EDIT ({candidate.dim}, {candidate.component})\n{candidate.note}",
        "# REFERENCE EXECUTION\n" + _view(reference),
        "# CANDIDATE EXECUTION\n" + _view(probe),
    ])
    try:
        header, _bodies, usage = ask(model, CONTRAST_SYSTEM, user, max_tokens=1024)
        verdict = str(header.get("contrast", ""))
        if verdict not in VERDICTS:
            raise ModelError(f"unknown contrast verdict {verdict!r}")
        return {"contrast": verdict, "observation": str(header.get("observation", ""))[:500], "usage": usage}
    except ModelError as error:
        return {"contrast": "neutral", "observation": f"contrast call failed: {error}", "usage": {}, "error": str(error)}
