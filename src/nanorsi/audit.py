"""Fresh-session skill audit: task-answer leakage and silent-bypass detection."""
from __future__ import annotations

import json
from pathlib import Path

from .config import load_config
from .gitops import Git
from .lineage import LineageStore, write_json
from .locking import Lock
from .loop import tasks

MIN_LEAK_CHARS = 8


def _normalize(text: str) -> str:
    return " ".join(text.split())


def _skill_files(checkout: Path) -> dict[str, str]:
    base = checkout / "target" / "agent" / "skills"
    if not base.is_dir():
        return {}
    return {path.relative_to(base).as_posix(): path.read_text(encoding="utf-8", errors="replace")
            for path in sorted(base.rglob("*")) if path.is_file()}


def _surface_files(checkout: Path, include: list[str], deny: list[str]) -> dict[str, str]:
    """Every mutable-surface text file, not just the skills directory.

    Red-team follow-up (ADOPTION item 31): answers can hide anywhere the surface
    allows, so leakage scanning follows the allow patterns rather than one path."""
    from .surface import check_paths
    candidates = []
    for path in sorted(checkout.rglob("*")):
        relative = path.relative_to(checkout)
        if not path.is_file() or path.is_symlink() or any(part in {".git", "__pycache__", ".nanorsi"} for part in relative.parts):
            continue
        try:
            if path.stat().st_size > 65536:
                continue
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        candidates.append((relative.as_posix(), text))
    blocked = set(check_paths([relative for relative, _ in candidates], include, deny))
    return {relative: text for relative, text in candidates if relative not in blocked}


def _leakage(skill_files: dict[str, str], rows: list[dict]) -> list[dict]:
    leaks: list[dict] = []
    for skill, text in skill_files.items():
        content = _normalize(text)
        for row in rows:
            for name, expected in row.get("expected_files", {}).items():
                needle = _normalize(str(expected))
                if len(needle) >= MIN_LEAK_CHARS and needle in content:
                    leaks.append({"skill": skill, "task_id": row["task_id"],
                                  "expected_file": name, "chars": len(needle)})
    return leaks


def _panel(root: Path, event: dict) -> tuple[list[dict], str]:
    entry = (event.get("artifacts") or {}).get("gate.json")
    if not entry:
        return [], "missing"
    try:
        payload = json.loads((root / entry["path"]).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return [], "unreadable"
    return payload.get("case_results") or [], "ok"


def _invocations(panel_rows: list[dict]) -> dict[str, set[str]]:
    loaded: set[str] = set()
    executed: set[str] = set()
    for case in panel_rows:
        loaded.update((case.get("skill_hashes") or {}).keys())
        for item in case.get("trace") or []:
            if item.get("event") == "skill_script_invoked" and item.get("name"):
                executed.add(item["name"])
    return {"loaded": loaded, "executed": executed}


def _bypass(declared: list[str], skill_files: dict[str, str], observed: dict[str, set[str]], cases: int) -> dict:
    scripts = sorted({path.split("/")[0] for path in skill_files if path.endswith("/run.py")})
    markdown_only = sorted(name for name in declared if name not in scripts)
    if not cases:
        return {"panel_cases": 0, "executable_skills": scripts, "markdown_only_always_in_context": markdown_only,
                "uninvoked_scripts": scripts, "declared_but_unloaded": sorted(set(declared) - observed["loaded"]),
                "note": "no evaluation panel found; script invocation could not be checked"}
    return {"panel_cases": cases, "executable_skills": scripts, "markdown_only_always_in_context": markdown_only,
            "uninvoked_scripts": sorted(set(scripts) - observed["executed"]),
            "declared_but_unloaded": sorted(set(declared) - observed["loaded"])}


def audit(root: Path, generation: int | None = None) -> dict:
    config = load_config(root / "nanorsi.toml")
    events = LineageStore.initialize(root).events()
    generations = [e for e in events if e.get("event_type") == "generation"]
    if not generations:
        raise RuntimeError("no generation to audit; run baseline first")
    if generation is None:
        event = generations[-1]
    else:
        event = next((e for e in generations if e.get("generation") == generation), None)
        if event is None:
            raise RuntimeError(f"generation {generation} not found")
    with Lock(root):
        with Git(root).worktree(event["candidate_commit"], root / ".nanorsi/worktrees/audit") as checkout:
            skill_files = _skill_files(checkout)
            surface_files = _surface_files(checkout, config.surface.allow, config.surface.deny)
    panel_rows, panel_status = _panel(root, event)
    observed = _invocations(panel_rows)
    declared = list(config.agent.get("skills", []))
    report = {"schema_version": 1, "generation": event["generation"], "candidate_commit": event["candidate_commit"],
              "panel_status": panel_status, "declared_skills": declared, "skill_files": sorted(skill_files),
              "surface_files": sorted(surface_files),
              "leakage": _leakage(surface_files, tasks(root, config))}
    report.update(_bypass(declared, skill_files, observed, len(panel_rows)))
    write_json(root / "reports" / "audit.json", report)
    return report
