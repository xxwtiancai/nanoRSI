from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path


class LockBusy(RuntimeError):
    pass


@contextmanager
def Lock(root: Path):  # noqa: N801 - public context-manager API
    control = root / ".nanorsi"
    control.mkdir(parents=True, exist_ok=True)
    lock = control / "lock"
    try:
        descriptor = os.open(lock, os.O_RDWR | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as error:
        raise LockBusy("another nanoRSI operation owns this experiment") from error
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        handle.write(str(os.getpid()))
    try:
        yield lock
    finally:
        try:
            lock.unlink()
        except FileNotFoundError:
            pass
