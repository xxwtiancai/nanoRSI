"""Blind terminal selection (k >= 2): the selector sees anonymised deliverables only,
never scores or labels, and must name exactly one. Falls back to the first
delivered final if it cannot."""
from __future__ import annotations

import hashlib
import random

from .model import ModelError, ask
from .propose import clip

SELECT_SYSTEM = (
    "You are choosing the best final deliverable for a professional task from anonymised candidates. Read every "
    "candidate completely; judge correctness, completeness and fitness for the stated task, not length or polish. "
    'Reply with exactly one JSON line: {"choice": "<candidate id>", "why": "<two sentences>"}'
)


def _ids(labels: list[str], *, task_id: str, seed: int) -> dict[str, str]:
    order = sorted(labels)
    random.Random(int(hashlib.sha1(f"{seed}|{task_id}".encode()).hexdigest()[:12], 16)).shuffle(order)
    return {chr(ord("A") + i): label for i, label in enumerate(order)}


def blind(model, task: dict, finals: list, *, seed: int = 0) -> dict:
    id_map = _ids([f.label for f in finals], task_id=task["task_id"], seed=seed)
    by_label = {f.label: f for f in finals}
    sections = []
    for anon, label in id_map.items():
        body = "\n\n".join(f"----- {name} -----\n{clip(text, 8000)}" for name, text in by_label[label].deliverables.items()) or "(no deliverable)"
        sections.append(f"# CANDIDATE {anon}\n{body}")
    user = f"# TASK\n{task['instruction']}\n\n" + "\n\n".join(sections) + f"\n\nChoose exactly one of: {', '.join(id_map)}."
    try:
        header, _bodies, usage = ask(model, SELECT_SYSTEM, user, max_tokens=1024)
        anon = str(header.get("choice", "")).strip()
        if anon not in id_map:
            raise ModelError(f"choice {anon!r} is not one of {sorted(id_map)}")
        return {"chosen": id_map[anon], "why": str(header.get("why", ""))[:400], "id_map": id_map, "usage": usage, "fallback": False}
    except ModelError as error:
        chosen = next((f.label for f in finals if f.delivered), finals[0].label)
        return {"chosen": chosen, "why": f"selector failed ({error}); first delivered final kept", "id_map": id_map,
                "usage": {}, "fallback": True}
