from __future__ import annotations

import hmac
import json
import secrets
from hashlib import sha256
from pathlib import Path

from .hashing import canonical_hash


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
            key_path.write_bytes(secrets.token_bytes(32))
            key_path.chmod(0o600)
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

    def verify(self) -> list[str]:
        events = self.events()
        current_parent = None
        for expected, event in enumerate(events, 1):
            if event.get("seq") != expected or event.get("receipt") != self._receipt(event):
                raise LineageError(f"invalid lineage event {expected}")
            if expected == 1 and event.get("decision") != "baseline":
                raise LineageError("first lineage event must be the baseline")
            if event.get("decision") == "baseline":
                current_parent = event["generation"]
            if event.get("decision") == "accepted":
                if current_parent is None or event.get("parent_generation") != current_parent:
                    raise LineageError(f"generation {event.get('generation')} has an invalid parent")
                current_parent = event["generation"]
        return events


Lineage = LineageStore
