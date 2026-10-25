"""Task manifest: the frozen set of work items a harness is improved on."""
from __future__ import annotations

import json
from pathlib import Path


class TaskError(ValueError):
    pass


def load_tasks(root: Path, manifest: str) -> list[dict]:
    path = Path(root) / manifest
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise TaskError(f"cannot read task manifest {path}: {error}") from error
    if not isinstance(data, dict) or data.get("schema_version") != 1 or not isinstance(data.get("tasks"), list):
        raise TaskError("manifest must have schema_version 1 and a tasks list")
    tasks, seen = [], set()
    for row in data["tasks"]:
        if not isinstance(row, dict):
            raise TaskError("every task must be an object")
        task_id = row.get("task_id")
        if not isinstance(task_id, str) or not task_id or task_id in seen:
            raise TaskError(f"task_id missing or duplicated: {task_id!r}")
        seen.add(task_id)
        if not isinstance(row.get("instruction"), str) or not row["instruction"].strip():
            raise TaskError(f"{task_id}: instruction required")
        docs = row.get("documents", {})
        if not isinstance(docs, dict) or any(not isinstance(v, str) for v in docs.values()):
            raise TaskError(f"{task_id}: documents must map name -> relative path")
        deliverables = row.get("deliverables", [])
        if not isinstance(deliverables, list) or not deliverables or any(not isinstance(d, str) for d in deliverables):
            raise TaskError(f"{task_id}: deliverables must be a non-empty list of file names")
        for rel in docs.values():
            if rel.startswith("/") or ".." in Path(rel).parts:
                raise TaskError(f"{task_id}: document path must stay inside the workspace: {rel}")
        tasks.append({"task_id": task_id, "domain": str(row.get("domain", "")), "instruction": row["instruction"],
                      "documents": docs, "deliverables": deliverables, "extra": row.get("extra", {})})
    if not tasks:
        raise TaskError("manifest has no tasks")
    return tasks


def select_tasks(tasks: list[dict], only: list[str] | None, max_tasks: int) -> list[dict]:
    chosen = [t for t in tasks if not only or t["task_id"] in only or t["domain"] in only]
    if only and not chosen:
        raise TaskError("no task matches " + ", ".join(only))
    return chosen[:max_tasks] if max_tasks else chosen
