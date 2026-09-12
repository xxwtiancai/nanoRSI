from __future__ import annotations

import hmac
import json
import os
import secrets
import tempfile
from hashlib import sha256
from pathlib import Path

from .hashing import canonical_hash
from .paths import contained_path


def artifact(root: Path, path: Path) -> dict:
    relative = path.resolve().relative_to(root.resolve()).as_posix()
    return {"path": relative, "sha256": sha256(path.read_bytes()).hexdigest()}


def write_json(path: Path, payload: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, sort_keys=True, indent=2, allow_nan=False), encoding="utf-8")
    temporary.replace(path)


class LineageError(RuntimeError):
    pass


class LineageStore:
    def __init__(self, path: Path, key_path: Path):
        self.path = path
        self.key_path = key_path

    @classmethod
    def initialize(cls, root: Path) -> "LineageStore":
        control = root / ".nanorsi"
        control.mkdir(parents=True, exist_ok=True)
        path = root / "lineage.jsonl"
        key_path = control / "lineage.key"
        if not key_path.exists():
            descriptor, temporary = tempfile.mkstemp(prefix=".lineage-key-", dir=control)
            try:
                with os.fdopen(descriptor, "wb") as handle:
                    handle.write(secrets.token_bytes(32))
                    handle.flush()
                    os.fsync(handle.fileno())
                try:
                    os.link(temporary, key_path)
                except FileExistsError:
                    pass
            finally:
                Path(temporary).unlink(missing_ok=True)
        if len(key_path.read_bytes()) != 32:
            raise LineageError("lineage signing key must contain exactly 32 bytes")
        path.touch(exist_ok=True)
        return cls(path, key_path)

    def _key(self) -> bytes:
        return self.key_path.read_bytes()

    def _receipt(self, event: dict) -> str:
        payload = canonical_hash({key: value for key, value in event.items() if key != "receipt"})
        return hmac.new(self._key(), payload.encode("ascii"), sha256).hexdigest()

    def append(self, event: dict) -> dict:
        current = self.events()
        record = {key: value for key, value in event.items() if key not in {"seq", "receipt"}}
        record["seq"] = len(current) + 1
        record["receipt"] = self._receipt(record)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
        return record

    def events(self) -> list[dict]:
        if not self.path.exists():
            return []
        events = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                events.append(json.loads(line))
        return events

    def latest_accepted(self) -> dict:
        accepted = [
            event for event in self.events()
            if event.get("decision") in {"accepted", "baseline"} and "generation" in event
        ]
        if not accepted:
            raise LineageError("lineage has no accepted generation")
        return accepted[-1]

    def verify(self) -> list[dict]:
        events = self.events()
        current_parent = None
        for expected, event in enumerate(events, 1):
            if event.get("seq") != expected or event.get("receipt") != self._receipt(event):
                raise LineageError(f"invalid lineage event {expected}")
            if expected == 1 and event.get("decision") != "baseline":
                raise LineageError("first lineage event must be the baseline")
            if event.get("decision") == "baseline":
                current_parent = event.get("generation", current_parent)
            if event.get("decision") == "accepted":
                if current_parent is None or event.get("parent_generation") != current_parent:
                    raise LineageError(f"generation {event.get('generation')} has an invalid parent")
                current_parent = event["generation"]
            for ref in event.get("artifacts", {}).values():
                try:
                    path = contained_path(self.path.parent, ref["path"])
                    if sha256(path.read_bytes()).hexdigest() != ref["sha256"]:
                        raise ValueError("hash mismatch")
                except (OSError, KeyError, ValueError) as error:
                    raise LineageError(f"invalid artifact in event {expected}: {error}") from error
        return events

    def recover_attempts(self) -> None:
        events = self.verify()
        done = {e.get("attempt_id") for e in events if e.get("event_type") in {"generation", "attempt_failed", "candidate_evaluated"}}
        for event in events:
            if event.get("event_type") == "attempt_started" and event["attempt_id"] not in done:
                artifacts = {}
                if event.get("candidate_id") and event.get("run_dir"):
                    directory = contained_path(self.path.parent, event["run_dir"])
                    artifacts = {p.relative_to(directory).as_posix(): artifact(self.path.parent, p)
                                 for p in directory.rglob("*") if p.is_file() and not p.is_symlink()}
                self.append({"event_type": "attempt_failed", "attempt_id": event["attempt_id"],
                             "candidate_id": event.get("candidate_id"), "artifacts": artifacts,
                             "decision": "interrupted", "reason": "previous process stopped before completion"})


Lineage = LineageStore
