"""A scripted stand-in for the chat endpoint: it recognises each improver role by its
system prompt and answers in the reply grammar, so the whole loop runs offline."""
from __future__ import annotations

import json


class StubTransport:
    def __init__(self, *, contrast="mitigates", decision="adopt_inv", select_choice="A", fail_compose_once=False,
                 final_contrast=None):
        self.contrast = contrast
        self.final_contrast = final_contrast or contrast
        self.decision = decision
        self.select_choice = select_choice
        self.fail_compose_once = fail_compose_once
        self.calls: list[str] = []

    def __call__(self, payload: dict) -> dict:
        messages = payload["messages"]
        system = messages[0]["content"] if messages and messages[0]["role"] == "system" else ""
        text = self._answer(system, messages)
        return {"choices": [{"message": {"content": text}}], "usage": {"prompt_tokens": 100, "completion_tokens": 20}}

    def _answer(self, system: str, messages: list) -> str:
        if "You act through one JSON action" in system:
            self.calls.append("agent")
            return self._agent(messages, system)
        if "editing exactly ONE component" in system:
            self.calls.append("propose")
            dim = "INV" if "(INV)" in messages[-1]["content"] else "DOM"
            component = "guardrails.md" if dim == "INV" else "skills/domain-check/SKILL.md"
            body = ("- Verify every figure against the source before writing.\n" if dim == "INV"
                    else "description: domain checklist\n\nCheck clause numbers and penalties explicitly.\n")
            return json.dumps({"component": component, "note": f"{dim} edit from stub"}) + f"\n```markdown\n{body}```"
        if "Classify the CANDIDATE relative to the REFERENCE" in system:
            self.calls.append("contrast")
            verdict = self.final_contrast if "(FINAL," in messages[-1]["content"] else self.contrast
            return json.dumps({"contrast": verdict, "observation": "stub observation"})
        if "compose the next harness" in system:
            self.calls.append("compose")
            if self.fail_compose_once:
                self.fail_compose_once = False
                return "I think we should adopt the first one."
            if self.decision == "keep":
                return json.dumps({"decision": "keep", "observation": "nothing mitigated", "files": []})
            return (json.dumps({"decision": self.decision, "observation": "INV mitigated the figure errors",
                                "files": ["guardrails.md"]})
                    + "\n```markdown\n- Verify every figure against the source before writing.\n- Flag unowned items.\n```")
        if "anonymised candidates" in system:
            self.calls.append("select")
            return json.dumps({"choice": self.select_choice, "why": "stub choice"})
        if "Extract ONE reusable lesson" in system:
            self.calls.append("experience")
            return json.dumps({"cue": "figures in documents", "lesson": "verify figures before writing",
                               "evidence": "stub observation", "confidence": "high"})
        if "Reply with the single word OK" in messages[-1]["content"]:
            return "OK"
        raise AssertionError("stub received an unknown prompt: " + system[:80])

    def _agent(self, messages: list, system: str) -> str:
        turn = sum(1 for m in messages if m["role"] == "assistant")
        deliverable = system.split("# EXPECTED DELIVERABLES")[1].strip().strip("`").split("`")[0]
        if turn == 0:
            return json.dumps({"action": "list_documents"})
        if turn == 1:
            docs = messages[-1]["content"].splitlines()[1:]
            return json.dumps({"action": "read_document", "name": docs[0] if docs else "none"})
        if turn == 2:
            body = "# Result\n\nPriya 2026-11-03 vendor contract; no owner for budget freeze; Marcus status page.\n" \
                   "Clause 4.2 fifth business day 1.5%; 7.1 thirty (30) days; 9.3 insurance 2,000,000; penalty unstated.\n"
            return json.dumps({"action": "write_deliverable", "filename": deliverable}) + f"\n```markdown\n{body}```"
        return json.dumps({"action": "done"})
