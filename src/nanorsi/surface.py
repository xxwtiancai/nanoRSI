from __future__ import annotations

import fnmatch
import re
import shlex

from .paths import normalize_relative_path


PROTECTED_PATTERNS = [
    "evaluator/**",
    "evaluator",
    "proposer/**",
    "proposer",
    ".nanorsi/**",
    ".nanorsi",
    "lineage.jsonl",
    "nanorsi.toml",
    "reports/**",
    "reports",
    "runs/**",
    "runs",
    "tasks/**",
    "tasks",
    "adapters/**",
    "adapters",
    "trainer/**",
    "trainer",
]


def _matches(path: str, pattern: str) -> bool:
    if fnmatch.fnmatch(path, pattern):
        return True
    return pattern.endswith("/**") and path == pattern[:-3].rstrip("/")


def check_paths(paths: list[str], include: list[str], exclude: list[str] | None = None) -> list[str]:
    excluded = [*(exclude or []), *PROTECTED_PATTERNS]
    violations: list[str] = []
    for path in paths:
        if any(_matches(path, pattern) for pattern in excluded):
            violations.append(path)
        elif not any(_matches(path, pattern) for pattern in include):
            violations.append(path)
    return violations


class SurfacePolicy:
    def __init__(self, include: list[str], exclude: list[str]):
        self.include = include
        self.exclude = exclude

    def validate_paths(self, paths: list[str]) -> list[str]:
        normalized = [normalize_relative_path(path) for path in paths]
        violations = check_paths(normalized, self.include, self.exclude)
        if violations:
            raise ValueError("changed paths outside mutable surface: " + ", ".join(violations))
        return normalized


def changed_paths_from_unified_diff(diff: str) -> list[str]:
    paths: list[str] = []
    for line in diff.splitlines():
        if not line.startswith("diff --git "):
            continue
        tokens = shlex.split(line)
        if len(tokens) != 4:
            raise ValueError(f"malformed diff header: {line}")
        for token in tokens[2:]:
            if token.startswith("a/"):
                paths.append(normalize_relative_path(token[2:]))
    return list(dict.fromkeys(paths))
