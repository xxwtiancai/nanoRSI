"""Append-only, hash-chained run ledger: every rollout, proposal, contrast,
composition, selection and judgement is an event; nothing is ever rewritten."""
from __future__ import annotations

import json
import time
from hashlib import sha256
from pathlib import Path


class LedgerError(RuntimeError):
    pass


def _digest(previous: str, payload: dict) -> str:
    body = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return sha256((previous + body).encode("utf-8")).hexdigest()


class Ledger:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def events(self) -> list[dict]:
        if not self.path.is_file():
            return []
        rows = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
        return rows

    def append(self, event: str, **fields) -> dict:
        rows = self.events()
        previous = rows[-1]["digest"] if rows else ""
        payload = {"seq": len(rows), "ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "event": event, **fields}
        record = {**payload, "digest": _digest(previous, payload)}
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")
        return record

    def verify(self) -> int:
        previous = ""
        for index, row in enumerate(self.events()):
            digest = row.pop("digest", None)
            if row.get("seq") != index or digest != _digest(previous, row):
                raise LedgerError(f"ledger broken at seq {index}")
            previous = digest
        return index + 1 if self.path.is_file() and self.events() else 0

    def count(self, event: str, **match) -> int:
        return sum(1 for row in self.events() if row.get("event") == event
                   and all(row.get(key) == value for key, value in match.items()))

    def usage(self) -> dict:
        """Counts are by *initiation* (reserved events), so concurrent charges cannot both pass a limit."""
        totals = {"proposer_calls": 0, "rollouts": 0, "input_tokens": 0, "output_tokens": 0}
        for row in self.events():
            use = row.get("usage") or {}
            totals["input_tokens"] += int(use.get("input_tokens") or 0)
            totals["output_tokens"] += int(use.get("output_tokens") or 0)
            if row.get("event") == "reserved":
                if row.get("kind") == "rollout":
                    totals["rollouts"] += 1
                else:
                    totals["proposer_calls"] += 1
        return totals

    def frozen(self) -> bool:
        return self.count("freeze") > 0
