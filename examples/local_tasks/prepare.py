"""Build the deterministic local text-edit protocol fixture manifest.

These tasks exercise file inspection and constrained editing.  They are
fixtures for checking the harness protocol, not benchmark results.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable


SPLITS = ("train", "validation", "test")
TASKS_PER_SPLIT = 30
GROUPS_PER_SPLIT = 10
TASKS_PER_GROUP = 3


def _paths(task_id: str, *names: str) -> list[str]:
    return [f"fixtures/{task_id}/{name}" for name in names]


def _replace_task(split: str, group_id: str, task_id: str) -> tuple[str, dict[str, str], dict[str, str]]:
    path = _paths(task_id, "status.txt")[0]
    original = "\n".join((
        f"Workspace: {split}/{group_id}",
        f"Evidence: {task_id}",
        "Status: draft",
        "Owner: local-runner",
    )) + "\n"
    expected = original.replace("Status: draft", "Status: ready")
    instruction = (f"Open {path} and use the Evidence line for {task_id}. "
                   "Change only the value on the Status line from draft to ready; "
                   "preserve every other line.")
    return instruction, {path: original}, {path: expected}


def _append_task(split: str, group_id: str, task_id: str) -> tuple[str, dict[str, str], dict[str, str]]:
    path = _paths(task_id, "notes.md")[0]
    original = "\n".join((
        f"# Review {task_id}",
        f"Source group: {group_id}",
        "Decision: pending",
    )) + "\n"
    expected = original + "Evidence checked: yes\n"
    instruction = (f"Inspect {path}, confirm the Source group identifies {group_id}, "
                   "then append exactly `Evidence checked: yes` as the final line. "
                   "Do not alter the existing lines.")
    return instruction, {path: original}, {path: expected}


def _remove_task(split: str, group_id: str, task_id: str) -> tuple[str, dict[str, str], dict[str, str]]:
    path = _paths(task_id, "checklist.txt")[0]
    original = "\n".join((
        f"group={group_id}",
        "keep: source inspected",
        f"remove: temporary note for {task_id}",
        "keep: final line retained",
    )) + "\n"
    expected = original.replace(f"remove: temporary note for {task_id}\n", "")
    instruction = (f"In {path}, locate the line containing the task evidence "
                   f"`{task_id}` and remove that one temporary note. Keep both keep lines "
                   "and their order unchanged.")
    return instruction, {path: original}, {path: expected}


def _insert_task(split: str, group_id: str, task_id: str) -> tuple[str, dict[str, str], dict[str, str]]:
    path = _paths(task_id, "record.txt")[0]
    original = "\n".join((
        f"Record: {task_id}",
        "Anchor: verified",
        f"Group: {group_id}",
        "End: true",
    )) + "\n"
    expected = original.replace(f"Group: {group_id}\n", f"Evidence: {task_id}\nGroup: {group_id}\n")
    instruction = (f"Read {path} and insert `Evidence: {task_id}` immediately before its "
                   f"Group line ({group_id}). Use the Anchor line as evidence and leave all "
                   "other text untouched.")
    return instruction, {path: original}, {path: expected}


def _field_task(split: str, group_id: str, task_id: str) -> tuple[str, dict[str, str], dict[str, str]]:
    path = _paths(task_id, "settings.ini")[0]
    original = "\n".join((
        "[task]",
        f"id={task_id}",
        f"group={group_id}",
        "priority=normal",
        "mode=review",
    )) + "\n"
    expected = original.replace("priority=normal", "priority=high")
    instruction = (f"In {path}, verify the id is {task_id} and the mode is review. "
                   "Change only priority from normal to high, retaining the INI layout.")
    return instruction, {path: original}, {path: expected}


def _move_task(split: str, group_id: str, task_id: str) -> tuple[str, dict[str, str], dict[str, str]]:
    path = _paths(task_id, "sequence.txt")[0]
    original = "\n".join((
        f"start: {task_id}",
        "step: prepare",
        "step: publish",
        f"group: {group_id}",
    )) + "\n"
    expected = original.replace("step: publish\n", "").replace("step: prepare\n", "step: publish\nstep: prepare\n")
    instruction = (f"In {path}, use the group line ({group_id}) to identify the record and "
                   "swap the two step lines so publish precedes prepare. Preserve start and group.")
    return instruction, {path: original}, {path: expected}


def _sync_task(split: str, group_id: str, task_id: str) -> tuple[str, dict[str, str], dict[str, str]]:
    source, index = _paths(task_id, "source.txt", "index.txt")
    original = {
        source: f"entry={task_id}\nlabel=old\ngroup={group_id}\n",
        index: f"lookup={task_id}\nlabel=old\n",
    }
    expected = {
        source: original[source].replace("label=old", "label=ready"),
        index: original[index].replace("label=old", "label=ready"),
    }
    instruction = (f"Inspect {source} and {index}; their shared lookup is {task_id}. "
                   "Update the label field from old to ready in both files and leave group data intact.")
    return instruction, original, expected


def _yaml_task(split: str, group_id: str, task_id: str) -> tuple[str, dict[str, str], dict[str, str]]:
    path = _paths(task_id, "metadata.yaml")[0]
    original = "\n".join((
        f"task: {task_id}",
        f"group: {group_id}",
        "labels:",
        "  state: pending",
        "  reviewed: false",
    )) + "\n"
    expected = original.replace("  reviewed: false", "  reviewed: true")
    instruction = (f"Review {path} using task {task_id} and change only labels.reviewed from "
                   "false to true. Keep the YAML indentation and pending state unchanged.")
    return instruction, {path: original}, {path: expected}


def _markdown_task(split: str, group_id: str, task_id: str) -> tuple[str, dict[str, str], dict[str, str]]:
    path = _paths(task_id, "summary.md")[0]
    original = "\n".join((
        f"# {task_id}",
        f"Group: {group_id}",
        "## Finding",
        "Needs review.",
    )) + "\n"
    expected = original.replace("Needs review.", "Ready for review.")
    instruction = (f"Open {path}; confirm the heading names {task_id}, then replace the sentence "
                   "under Finding with `Ready for review.`. Keep headings and group text unchanged.")
    return instruction, {path: original}, {path: expected}


def _table_task(split: str, group_id: str, task_id: str) -> tuple[str, dict[str, str], dict[str, str]]:
    path = _paths(task_id, "table.txt")[0]
    original = "\n".join((
        f"task | {task_id}",
        f"group | {group_id}",
        "state | draft",
        "owner | local-runner",
    )) + "\n"
    expected = original.replace("state | draft", "state | ready")
    instruction = (f"In {path}, use the task row for {task_id} and change the state cell from "
                   "draft to ready. Keep pipe separators, spacing, and all other rows unchanged.")
    return instruction, {path: original}, {path: expected}


_BUILDERS: tuple[Callable[[str, str, str], tuple[str, dict[str, str], dict[str, str]]], ...] = (
    _replace_task,
    _append_task,
    _remove_task,
    _insert_task,
    _field_task,
    _move_task,
    _sync_task,
    _yaml_task,
    _markdown_task,
    _table_task,
)


def _make_task(split: str, group_number: int, variant: int, ordinal: int) -> dict[str, object]:
    task_id = f"{split}-{ordinal:03d}"
    group_id = f"{split}-source-{group_number:02d}"
    builder = _BUILDERS[group_number]
    instruction, input_files, expected_files = builder(split, group_id, task_id)
    return {
        "task_id": task_id,
        "group_id": group_id,
        "split": split,
        "instruction": instruction,
        "input_files": input_files,
        "expected_files": expected_files,
    }


def build_manifest() -> dict[str, object]:
    tasks = []
    ordinal = 1
    for split in SPLITS:
        for group_number in range(GROUPS_PER_SPLIT):
            for variant in range(TASKS_PER_GROUP):
                tasks.append(_make_task(split, group_number, variant, ordinal))
                ordinal += 1
    return {"schema_version": 1, "tasks": tasks}


def write_manifest(output: str | Path) -> Path:
    target = Path(output)
    if target.suffix.lower() != ".json":
        target = target / "manifest.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(build_manifest(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write deterministic local task protocol fixtures.")
    parser.add_argument("output", nargs="?", default=Path(__file__).with_name("manifest.json"),
                        help="manifest JSON path (or directory, which receives manifest.json)")
    args = parser.parse_args(argv)
    print(write_manifest(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
