"""Harnessing-level recursion: after a task adopts a harness, distil one lesson that the
probe contrasts actually support and keep it in the workspace library. Later tasks
read the library before proposing; a lesson is never written without evidence."""
from __future__ import annotations

import json
from pathlib import Path

from . import harness
from .model import ModelError, ask

LIBRARY = ".nanorsi/library.jsonl"

EXPERIENCE_SYSTEM = (
    "A harness edit was adopted after probe contrasts. Extract ONE reusable lesson that the contrasts support — "
    "not a restatement of the edit. Reply with exactly one JSON line: "
    '{"cue": "<when this applies>", "lesson": "<what to do>", "evidence": "<the contrast observation that '
    'supports it>", "confidence": "high|medium|low"} or {"lesson": null} if nothing is supported.'
)


def load_lessons(workspace: Path) -> list[str]:
    path = Path(workspace) / LIBRARY
    if not path.is_file():
        return []
    lessons = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            lessons.append(f"[{row.get('cue', '')}] {row.get('lesson', '')} (evidence: {row.get('evidence', '')[:120]})")
    return lessons


def extract(model, task: dict, base: dict, adopted: dict, decisions: list, workspace: Path) -> dict | None:
    changes = harness.diff_summary(base, adopted)
    user = "\n\n".join([
        f"# TASK\n{task['instruction']}",
        "# ADOPTED CHANGES\n" + json.dumps(changes),
        "# DECISIONS AND OBSERVATIONS\n" + "\n".join(f"- {d.get('decision')}: {d.get('observation', '')}" for d in decisions),
        "# ADOPTED COMPONENTS\n" + "\n\n".join(f"=== {rel} ===\n{adopted[rel][:2500]}" for rel in changes["added"] + changes["modified"]),
    ])
    try:
        header, _bodies, usage = ask(model, EXPERIENCE_SYSTEM, user, max_tokens=1024)
    except ModelError as error:
        return {"lesson": None, "error": str(error), "usage": {}}
    if not header.get("lesson"):
        return {"lesson": None, "usage": usage}
    row = {"task": task["task_id"], "cue": str(header.get("cue", ""))[:300], "lesson": str(header["lesson"])[:500],
           "evidence": str(header.get("evidence", ""))[:400], "confidence": str(header.get("confidence", "medium")),
           "changes": changes}
    path = Path(workspace) / LIBRARY
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(row, ensure_ascii=False) + "\n")
    return {**row, "usage": usage}
