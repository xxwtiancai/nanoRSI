from __future__ import annotations

from pathlib import Path, PurePosixPath


def normalize_relative_path(raw: str) -> str:
    path = PurePosixPath(raw)
    if path.is_absolute() or not raw or raw == ".":
        message = "path is outside the workspace" if path.is_absolute() else "path must be relative and non-empty"
        raise ValueError(f"{message}: {raw!r}")
    parts = [part for part in path.parts if part not in {"", "."}]
    if any(part == ".." for part in parts):
        raise ValueError(f"path is outside the workspace: {raw!r}")
    normalized = PurePosixPath(*parts)
    if str(normalized) == ".":
        raise ValueError(f"path must name a file or directory: {raw!r}")
    return str(normalized)


def contained_path(root: Path, relative: str) -> Path:
    normalized = normalize_relative_path(relative)
    candidate = (root / normalized).resolve()
    root_resolved = root.resolve()
    if candidate != root_resolved and root_resolved not in candidate.parents:
        raise ValueError(f"path escapes the workspace: {relative!r}")
    return candidate


def display_relative(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()
