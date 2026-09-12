from __future__ import annotations

import os
import subprocess
from contextlib import contextmanager
from pathlib import Path
from threading import RLock
from typing import Iterator


# Git add/remove/prune inspect shared worktree administration files. Population
# threads use distinct Git instances; only these short metadata operations lock.
# The CLI's experiment lock separately coordinates supported process entry points.
_WORKTREE_ADMIN_LOCK = RLock()


class GitError(RuntimeError):
    pass


class Git:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def _run(
        self,
        *args: str,
        input_bytes: bytes | None = None,
        check: bool = True,
        identity: bool = False,
    ) -> subprocess.CompletedProcess[bytes]:
        prefix = ["git"]
        if identity:
            prefix += ["-c", "user.name=nanoRSI", "-c", "user.email=nanorsi@local"]
        command = [*prefix, "-C", str(self.root), *args]
        result = subprocess.run(
            command,
            input=input_bytes,
            capture_output=True,
            check=False,
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
        )
        if check and result.returncode:
            message = result.stderr.decode("utf-8", "replace").strip()
            raise GitError(message or f"git failed: {' '.join(args)}")
        return result

    def init(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        self._run("init", "-b", "main")

    def ensure_repository(self) -> None:
        result = self._run("rev-parse", "--git-dir", check=False)
        if result.returncode:
            raise GitError(f"not a Git repository: {self.root}")

    def is_clean(self) -> bool:
        return not self._run("status", "--porcelain").stdout.strip()

    def commit_all(self, message: str) -> str:
        self._run("add", "-A")
        result = self._run("commit", "-m", message, identity=True, check=False)
        if result.returncode and b"nothing to commit" not in result.stderr:
            raise GitError(result.stderr.decode("utf-8", "replace"))
        return self.resolve_ref("HEAD")

    def commit_paths(self, checkout: Path, paths: list[str], message: str) -> str:
        git = Git(checkout)
        if paths:
            git._run("add", "--", *paths)
        result = git._run("commit", "-m", message, identity=True, check=False)
        if result.returncode:
            raise GitError(result.stderr.decode("utf-8", "replace"))
        return git.resolve_ref("HEAD")

    def resolve_ref(self, ref: str) -> str:
        return self._run("rev-parse", ref).stdout.decode().strip()

    def tree_hash(self, ref: str) -> str:
        return self._run("rev-parse", f"{ref}^{{tree}}").stdout.decode().strip()

    def ref_exists(self, ref: str) -> bool:
        return not self._run("rev-parse", "--verify", ref, check=False).returncode

    def tag(self, ref: str, name: str) -> None:
        if self.ref_exists(name):
            raise GitError(f"ref already exists: {name}")
        self._run("tag", name, ref)

    def apply_diff(self, checkout: Path, diff: str) -> None:
        git = Git(checkout)
        payload = diff.encode("utf-8")
        check = git._run("apply", "--check", "--whitespace=nowarn", "-", input_bytes=payload, check=False)
        if check.returncode:
            raise GitError(check.stderr.decode("utf-8", "replace"))
        git._run("apply", "--whitespace=nowarn", "-", input_bytes=payload)

    def changed_paths(self, checkout: Path, parent_ref: str) -> list[str]:
        git = Git(checkout)
        tracked = git._run("diff", "--name-only", "-z", parent_ref).stdout.decode("utf-8")
        untracked = git._run("ls-files", "--others", "--exclude-standard", "-z").stdout.decode("utf-8")
        paths = [path for path in tracked.split("\0") + untracked.split("\0") if path]
        return list(dict.fromkeys(paths))

    @contextmanager
    def worktree(self, ref: str, destination: Path) -> Iterator[Path]:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with _WORKTREE_ADMIN_LOCK:
            self._run("worktree", "add", "--detach", str(destination), ref)
        try:
            yield destination.resolve()
        finally:
            with _WORKTREE_ADMIN_LOCK:
                self._run("worktree", "remove", "--force", str(destination), check=False)

    def prune_worktrees(self) -> None:
        with _WORKTREE_ADMIN_LOCK:
            self._run("worktree", "prune")
