"""Minimal stdlib GLM client and tool-loop executor for the harness2-minimal study.

The reply grammar keeps file payloads out of JSON strings (GLM systematically
breaks escaping when whole files ride inside JSON): every reply is one JSON
header line, and any payload body follows as a fenced block.
"""
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field


class ModelError(RuntimeError):
    pass


@dataclass
class AgentConfig:
    model: str = "glm-5.3"
    base_url: str = "https://api.z.ai/api/coding/paas/v4"
    api_key_file: str = "~/.nanorsi/keys/glm-coding-plan.key"
    max_tokens: int = 8192
    timeout_s: float = 600.0
    retries: int = 1

    def endpoint(self):
        return self.base_url.rstrip("/") + "/chat/completions"


def load_api_key(config):
    path = config.api_key_file
    try:
        from pathlib import Path
        text = Path(path).expanduser().read_text(encoding="utf-8").strip()
    except OSError as error:
        raise ModelError(f"api key file unreadable: {path}") from error
    if not text or any(c.isspace() for c in text):
        raise ModelError("api key file must contain one bare key")
    return text


def chat(config, messages, api_key=None, max_tokens=None):
    """One chat-completions call with a bounded retry on transport errors."""
    payload = {"model": config.model, "messages": messages,
               "thinking": {"type": "disabled"}, "max_tokens": max_tokens or config.max_tokens}
    body = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer " + (api_key or load_api_key(config))}
    last = None
    for attempt in range(config.retries + 1):
        request = urllib.request.Request(config.endpoint(), data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=config.timeout_s) as response:
                data = json.loads(response.read().decode("utf-8"))
            message = data["choices"][0]["message"]
            content = message.get("content") or ""
            if not content.strip():
                raise ModelError("empty content (thinking budget?)")
            usage = data.get("usage") or {}
            return content, {"input_tokens": usage.get("prompt_tokens"),
                             "output_tokens": usage.get("completion_tokens")}
        except ModelError as error:
            last = error
        except (urllib.error.URLError, OSError, ValueError, KeyError, IndexError) as error:
            detail = getattr(error, "code", "")
            last = ModelError(f"{type(error).__name__}{':' + str(detail) if detail else ''} {error}")
        if attempt < config.retries:
            time.sleep(5 * (attempt + 1))
    raise last


_FENCE = re.compile(r"```[a-zA-Z0-9_-]*\n(.*?)```", re.S)
_HEAD = re.compile(r"^\s*(\{.*\})\s*$")


def parse_reply(text):
    """Split a reply into (header dict, fenced body or ''). Raises ModelError."""
    lines = text.strip().splitlines()
    head = None
    for line in lines[:3]:
        match = _HEAD.match(line.strip())
        if match:
            try:
                head = json.loads(match.group(1))
            except ValueError as error:
                raise ModelError(f"bad JSON header: {error}") from error
            break
    if not isinstance(head, dict):
        stripped = text.strip()
        if stripped.startswith("{") and stripped.endswith("}"):
            try:
                head = json.loads(stripped)
            except ValueError as error:
                raise ModelError(f"bad JSON header: {error}") from error
        else:
            raise ModelError("no JSON header line in reply")
    body = _FENCE.search(text)
    return head, (body.group(1) if body else "")


@dataclass
class Execution:
    ok: bool
    turns: int
    trajectory: str
    deliverables: dict = field(default_factory=dict)
    usage: dict = field(default_factory=dict)
    error: str = ""


TOOL_PROMPT = """You act through one JSON action per turn. The first line of every reply MUST be exactly one JSON object:

{"action": "list_documents"}
{"action": "read_document", "name": "<file name>"}
{"action": "write_deliverable", "filename": "<expected deliverable name>"}
{"action": "done", "summary": "<one line>"}

For write_deliverable only, put the COMPLETE document as markdown inside one fenced block after the JSON line:

```markdown
<the full document content>
```

Never put the document itself inside the JSON. Documents are read one at a time; finish only when every expected deliverable file is written."""


def harness_system_prompt(harness_files, task):
    parts = []
    for name in ("systemprompt.md", "tool_guidance.md", "LongTermMEMORY.md"):
        body = harness_files.get(name, "").strip()
        if body:
            parts.append(f"# {name}\n{body}")
    skills = sorted(k for k in harness_files if k.startswith("skills/"))
    if skills:
        index = "\n".join(f"- {k}: {harness_files[k].splitlines()[0].lstrip('# ')}"
                          for k in skills if harness_files[k].strip())
        parts.append("# AVAILABLE SKILLS\nLoad when the situation matches:\n" + index)
    parts.append(TOOL_PROMPT)
    expected = ", ".join(f"`{name}`" for name in task["deliverables"])
    parts.append(f"# EXPECTED DELIVERABLES\nWrite exactly these files: {expected}.")
    return "\n\n---\n\n".join(parts)


def _tool_result(action, body, task, convert, deliverables, trajectory):
    name = action.get("action")
    if name == "list_documents":
        listing = "\n".join(sorted(task["documents"]))
        return "DOCUMENTS\n" + listing
    if name == "read_document":
        key = str(action.get("name", ""))
        if key not in task["documents"]:
            return f"ERROR: unknown document {key!r}; use list_documents"
        trajectory.append(f"[READ] {key}")
        return convert(key) or "(empty document)"
    if name == "write_deliverable":
        filename = str(action.get("filename", ""))
        if filename not in task["deliverables"]:
            expected = ", ".join(task["deliverables"])
            return f"ERROR: {filename!r} is not an expected deliverable; expected: {expected}"
        if not body.strip():
            return "ERROR: write_deliverable needs the document in a fenced ```markdown block"
        deliverables[filename] = body
        trajectory.append(f"[WRITE] {filename} ({len(body)} chars)")
        return f"wrote {filename}"
    if name == "done":
        return None
    return f"ERROR: unknown action {name!r}"


def execute_task(config, task, harness_files, *, convert, chat_fn=None, api_key=None, max_turns=16):
    """Run one task under one harness. convert(name) -> extracted document text."""
    caller = chat_fn or (lambda messages, max_tokens=None: chat(config, messages, api_key, max_tokens))
    messages = [{"role": "system", "content": harness_system_prompt(harness_files, task)},
                {"role": "user", "content": task["instructions"]}]
    trajectory, deliverables = [], {}
    usage = {"input_tokens": 0, "output_tokens": 0, "model_calls": 0}
    for turn in range(1, max_turns + 1):
        error_note = ""
        for _attempt in range(2):
            content, spent = caller(messages)
            usage["input_tokens"] += spent["input_tokens"] or 0
            usage["output_tokens"] += spent["output_tokens"] or 0
            usage["model_calls"] += 1
            try:
                head, body = parse_reply(content)
                break
            except ModelError as error:
                error_note = str(error)
                head = None
                messages.extend([{"role": "assistant", "content": content},
                                 {"role": "user", "content":
                                  f"INVALID REPLY ({error_note}). Reply again: one JSON action line"
                                  " first, fenced markdown only for write_deliverable."}])
        if head is None:
            return Execution(False, turn, "\n".join(trajectory), deliverables, usage,
                             f"unparseable actions on turn {turn}")
        action_name = head.get("action", "")
        trajectory.append(f"[ASSISTANT] {json.dumps(head, ensure_ascii=False)[:300]}")
        result = _tool_result(head, body, task, convert, deliverables, trajectory)
        if result is None:
            missing = [f for f in task["deliverables"] if f not in deliverables]
            return Execution(not missing, turn, "\n".join(trajectory), deliverables, usage,
                             f"done; missing deliverables: {missing}" if missing else "")
        trajectory.append(f"[OBSERVATION] {result[:400]}")
        messages.append({"role": "assistant", "content": content})
        messages.append({"role": "user", "content": result})
    missing = [f for f in task["deliverables"] if f not in deliverables]
    return Execution(False, max_turns, "\n".join(trajectory), deliverables, usage,
                     f"turn budget exhausted; missing: {missing}")
