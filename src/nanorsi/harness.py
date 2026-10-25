"""The editable harness surface: a small tree of text components around a frozen model.

Six of the paper's eight components are kept — four always-on text files, on-demand
skills and deterministic helper scripts; subagents and plugins need a host runtime
nano does not ship. A harness is a plain dict {relative path: text}."""
from __future__ import annotations

import re
from pathlib import Path

ALWAYS_ON = ("systemprompt.md", "guardrails.md", "memory.md", "tool_guidance.md")
SKILL_DIR = "skills"
SCRIPT_DIR = "scripts"
ALWAYS_ON_MAX_CHARS = 24_000
_NAME = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
_COMPONENT = re.compile(r"^(systemprompt|guardrails|memory|tool_guidance)\.md$|^skills/[a-z0-9][a-z0-9_-]*/SKILL\.md$|^scripts/[a-z0-9][a-z0-9_-]*\.py$")


class HarnessError(ValueError):
    pass


def read_tree(root: Path) -> dict[str, str]:
    root = Path(root)
    tree = {}
    for path in sorted(root.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            tree[path.relative_to(root).as_posix()] = path.read_text(encoding="utf-8", errors="replace")
    return tree


def write_tree(tree: dict[str, str], root: Path) -> Path:
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    for stale in sorted((p for p in root.rglob("*") if p.is_file()), reverse=True):
        stale.unlink()
    for rel, body in tree.items():
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
    return root


def validate(tree: dict[str, str]) -> None:
    """Reject paths off the surface, empty always-on sets and over-long context."""
    if not any(name in tree and tree[name].strip() for name in ALWAYS_ON):
        raise HarnessError("harness needs at least one non-empty always-on component")
    for rel in tree:
        if not _COMPONENT.match(rel):
            raise HarnessError(f"not an editable component: {rel}")
    total = sum(len(tree.get(name, "")) for name in ALWAYS_ON)
    if total > ALWAYS_ON_MAX_CHARS:
        raise HarnessError(f"always-on text {total} chars exceeds {ALWAYS_ON_MAX_CHARS}")
    for rel, body in tree.items():
        if rel.startswith(SKILL_DIR + "/") and not body.strip().startswith("---") and "\n" not in body.strip():
            raise HarnessError(f"skill {rel} needs a description line")


def diff_summary(before: dict[str, str], after: dict[str, str]) -> dict[str, list[str]]:
    return {
        "added": sorted(set(after) - set(before)),
        "removed": sorted(set(before) - set(after)),
        "modified": sorted(k for k in set(before) & set(after) if before[k] != after[k]),
    }


def changed(before: dict[str, str], after: dict[str, str]) -> bool:
    summary = diff_summary(before, after)
    return any(summary.values())


def skill_index(tree: dict[str, str]) -> list[tuple[str, str]]:
    """(name, first non-empty description line) for every skill."""
    index = []
    for rel, body in sorted(tree.items()):
        if rel.startswith(SKILL_DIR + "/") and rel.endswith("/SKILL.md"):
            name = rel.split("/")[1]
            lines = [line.strip().lstrip("#-* ") for line in body.splitlines() if line.strip() and not line.strip().startswith("---")]
            desc = next((line.split(":", 1)[1].strip() for line in lines if line.lower().startswith("description:")), lines[0] if lines else "")
            index.append((name, desc[:160]))
    return index


def render_always_on(tree: dict[str, str]) -> str:
    """The text a task executor sees before the task: always-on files plus a skill
    index and the helper-script roster. Skills themselves load on demand."""
    parts = [tree[name].strip() for name in ALWAYS_ON if tree.get(name, "").strip()]
    skills = skill_index(tree)
    if skills:
        parts.append("# AVAILABLE SKILLS\nRead `skills/<name>/SKILL.md` when the situation matches:\n"
                     + "\n".join(f"- `{name}`: {desc}" for name, desc in skills))
    scripts = sorted(rel.split("/")[-1] for rel in tree if rel.startswith(SCRIPT_DIR + "/"))
    if scripts:
        parts.append("# HELPER SCRIPTS\nAvailable under `scripts/`, run with `python3 scripts/<name>`: "
                     + ", ".join(scripts))
    return "\n\n---\n\n".join(parts)


def apply_edit(tree: dict[str, str], component: str, body: str | None) -> dict[str, str]:
    """Return a new tree with one component written (body None removes it)."""
    if not _COMPONENT.match(component):
        raise HarnessError(f"not an editable component: {component}")
    updated = dict(tree)
    if body is None:
        updated.pop(component, None)
    else:
        updated[component] = body if body.endswith("\n") else body + "\n"
    validate(updated)
    return updated


def describe(tree: dict[str, str]) -> str:
    """Full harness listing for the improver's context window."""
    return "\n\n".join(f"=== {rel} ===\n{body.rstrip()}" for rel, body in sorted(tree.items()))
