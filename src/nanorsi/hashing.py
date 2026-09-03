from __future__ import annotations

import fnmatch
import hashlib
import json
from pathlib import Path
from typing import Any


def canonical_hash(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _excluded(relative: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(relative, pattern) for pattern in patterns)


def tree_hash(root: Path, *, exclude: list[str] | None = None) -> str:
    """Hash deterministic file content, modes, and paths; do not follow symlinks."""
    root = root.resolve()
    digest = hashlib.sha256()
    paths = []
    for path in root.rglob("*"):
        relative = path.relative_to(root).as_posix()
        if _excluded(relative, exclude or []):
            continue
        if path.is_symlink():
            paths.append((relative, "symlink", Path(path.readlink()).as_posix()))
        elif path.is_file():
            mode = "exec" if path.stat().st_mode & 0o111 else "file"
            paths.append((relative, mode, hashlib.sha256(path.read_bytes()).hexdigest()))
        elif path.is_dir():
            paths.append((relative, "dir", ""))
    for relative, kind, payload in sorted(paths):
        digest.update(relative.encode("utf-8") + b"\0")
        digest.update(kind.encode("ascii") + b"\0")
        digest.update(payload.encode("utf-8") + b"\0")
    return digest.hexdigest()
