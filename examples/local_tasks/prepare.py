"""Build the deterministic local text-edit protocol fixture manifest.

These tasks exercise file inspection and constrained editing.  They are
fixtures for checking the harness protocol, not benchmark results.  Ten
counterfactual variants (one per task family: renamed symbols, reordered
lines, reworded instructions, same underlying rule) arm the acceptance
gate's challenger without changing what the rule-following policy must do.
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

# Counterfactual variants: same rule per family, different surface (renamed
# files, fields and labels, reordered lines, reworded instructions).  Guidance
# that memorized the original surface fails here; rule-level guidance passes.


def _cf_replace_task(group_id: str, task_id: str) -> tuple[str, dict[str, str], dict[str, str]]:
    path = f"fixtures/{task_id}/condition.txt"
    original = "\n".join((
        "Status: draft",
        "Owner: crew-lead",
        f"Workspace: archive/{group_id}",
        f"Reference: {task_id}",
    )) + "\n"
    expected = original.replace("Status: draft", "Status: ready")
    instruction = (f"The record {task_id} lives in {path}. Flip the Status value from draft "
                   "to ready and leave the other lines and their order untouched.")
    return instruction, {path: original}, {path: expected}


def _cf_append_task(group_id: str, task_id: str) -> tuple[str, dict[str, str], dict[str, str]]:
    path = f"fixtures/{task_id}/logbook.md"
    original = "\n".join((
        f"# Entry {task_id}",
        f"Team: {group_id}",
        "Outcome: open",
    )) + "\n"
    expected = original + "Evidence checked: yes\n"
    instruction = (f"Read {path}, check that the Team line names {group_id}, then close the entry "
                   "by appending exactly `Evidence checked: yes` as the last line without touching "
                   "the lines above it.")
    return instruction, {path: original}, {path: expected}


def _cf_remove_task(group_id: str, task_id: str) -> tuple[str, dict[str, str], dict[str, str]]:
    path = f"fixtures/{task_id}/pending.txt"
    original = "\n".join((
        f"squad={group_id}",
        "keep: header verified",
        f"drop: scratch note {task_id}",
        "keep: trailer preserved",
    )) + "\n"
    expected = original.replace(f"drop: scratch note {task_id}\n", "")
    instruction = (f"In {path}, delete the single drop line that carries the scratch note for "
                   f"{task_id}. Both keep lines stay in place and keep their order.")
    return instruction, {path: original}, {path: expected}


def _cf_insert_task(group_id: str, task_id: str) -> tuple[str, dict[str, str], dict[str, str]]:
    path = f"fixtures/{task_id}/ledger.txt"
    original = "\n".join((
        f"Entry: {task_id}",
        "Anchor: checked",
        f"Squad: {group_id}",
        "Closed: true",
    )) + "\n"
    expected = original.replace(f"Squad: {group_id}\n", f"Reference: {task_id}\nSquad: {group_id}\n")
    instruction = (f"Open {path} and insert `Reference: {task_id}` directly above the Squad line "
                   f"({group_id}). Treat the Anchor line as the justification and keep every other "
                   "line as it stands.")
    return instruction, {path: original}, {path: expected}


def _cf_field_task(group_id: str, task_id: str) -> tuple[str, dict[str, str], dict[str, str]]:
    path = f"fixtures/{task_id}/options.ini"
    original = "\n".join((
        "[job]",
        f"ref={task_id}",
        f"squad={group_id}",
        "urgency=normal",
        "phase=audit",
    )) + "\n"
    expected = original.replace("urgency=normal", "urgency=high")
    instruction = (f"For {path}, confirm that ref is {task_id} and phase is audit, then raise "
                   "urgency from normal to high while keeping the INI layout.")
    return instruction, {path: original}, {path: expected}


def _cf_move_task(group_id: str, task_id: str) -> tuple[str, dict[str, str], dict[str, str]]:
    path = f"fixtures/{task_id}/pipeline.txt"
    original = "\n".join((
        f"begin: {task_id}",
        "step: draft",
        "step: ship",
        f"squad: {group_id}",
    )) + "\n"
    expected = original.replace("step: ship\n", "").replace("step: draft\n", "step: ship\nstep: draft\n")
    instruction = (f"In {path}, identified by the squad line ({group_id}), reorder the two step "
                   "entries so ship comes before draft. Leave the begin and squad lines alone.")
    return instruction, {path: original}, {path: expected}


def _cf_sync_task(group_id: str, task_id: str) -> tuple[str, dict[str, str], dict[str, str]]:
    source, index = f"fixtures/{task_id}/data.txt", f"fixtures/{task_id}/registry.txt"
    original = {
        source: f"item={task_id}\ntag=stale\nsquad={group_id}\n",
        index: f"match={task_id}\ntag=stale\n",
    }
    expected = {
        source: original[source].replace("tag=stale", "tag=ready"),
        index: original[index].replace("tag=stale", "tag=ready"),
    }
    instruction = (f"Check {source} and {index}; both describe {task_id}. Switch the tag field "
                   "from stale to ready in each file and leave the squad data intact.")
    return instruction, original, expected


def _cf_yaml_task(group_id: str, task_id: str) -> tuple[str, dict[str, str], dict[str, str]]:
    path = f"fixtures/{task_id}/record.yaml"
    original = "\n".join((
        f"ref: {task_id}",
        f"squad: {group_id}",
        "flags:",
        "  stage: queued",
        "  cleared: false",
    )) + "\n"
    expected = original.replace("  cleared: false", "  cleared: true")
    instruction = (f"Audit {path} for ref {task_id}: flip flags.cleared from false to true only, "
                   "preserving the YAML indentation and the queued stage.")
    return instruction, {path: original}, {path: expected}


def _cf_markdown_task(group_id: str, task_id: str) -> tuple[str, dict[str, str], dict[str, str]]:
    path = f"fixtures/{task_id}/briefing.md"
    original = "\n".join((
        f"# {task_id}",
        f"Squad: {group_id}",
        "## Status",
        "Awaiting clearance.",
    )) + "\n"
    expected = original.replace("Awaiting clearance.", "Ready for review.")
    instruction = (f"Open {path}, verify the top heading is {task_id}, and replace the sentence "
                   "under Status with `Ready for review.` without editing the headings or the "
                   "squad line.")
    return instruction, {path: original}, {path: expected}


def _cf_table_task(group_id: str, task_id: str) -> tuple[str, dict[str, str], dict[str, str]]:
    path = f"fixtures/{task_id}/grid.txt"
    original = "\n".join((
        f"ref | {task_id}",
        f"squad | {group_id}",
        "stage | draft",
        "assignee | crew-lead",
    )) + "\n"
    expected = original.replace("stage | draft", "stage | ready")
    instruction = (f"Using the ref row for {task_id} in {path}, change the stage cell from draft "
                   "to ready. Keep the pipe layout and every other row identical.")
    return instruction, {path: original}, {path: expected}


_CF_BUILDERS: tuple[Callable[[str, str], tuple[str, dict[str, str], dict[str, str]]], ...] = (
    _cf_replace_task,
    _cf_append_task,
    _cf_remove_task,
    _cf_insert_task,
    _cf_field_task,
    _cf_move_task,
    _cf_sync_task,
    _cf_yaml_task,
    _cf_markdown_task,
    _cf_table_task,
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
    for group_number, builder in enumerate(_CF_BUILDERS):
        group_id = f"cf-source-{group_number:02d}"
        task_id = f"cf-{group_number + 1:03d}"
        instruction, input_files, expected_files = builder(group_id, task_id)
        tasks.append({"task_id": task_id, "group_id": group_id, "split": "counterfactual",
                      "instruction": instruction, "input_files": input_files,
                      "expected_files": expected_files})
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
