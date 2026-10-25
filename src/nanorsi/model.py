"""Chat-completions client (standard library only) and the one reply grammar
every improver call uses: a single JSON header line, then optional fenced bodies.

File payloads never ride inside JSON strings — GLM-class models break escaping
on whole files — so bodies travel as ```fences after the header."""
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path


class ModelError(RuntimeError):
    pass


def load_api_key(path: str) -> str:
    if not path:
        raise ModelError("model.api_key_file is not configured; run `nanorsi configure`")
    try:
        text = Path(path).expanduser().read_text(encoding="utf-8").strip()
    except OSError as error:
        raise ModelError(f"api key file unreadable: {path}") from error
    if not text or any(c.isspace() for c in text):
        raise ModelError("api key file must contain exactly one key")
    return text


class Model:
    """One configured endpoint. `call(messages)` returns (text, usage)."""

    def __init__(self, config, *, api_key: str | None = None, transport=None):
        self.config = config
        self._key = api_key
        self._transport = transport  # test seam: fn(payload) -> response dict

    def key(self) -> str:
        if self._key is None:
            self._key = load_api_key(self.config.api_key_file)
        return self._key

    def _send(self, payload: dict) -> dict:
        if self._transport is not None:
            return self._transport(payload)
        url = self.config.base_url.rstrip("/") + "/chat/completions"
        request = urllib.request.Request(
            url, data=json.dumps(payload).encode("utf-8"), method="POST",
            headers={"Content-Type": "application/json", "Authorization": "Bearer " + self.key()})
        with urllib.request.urlopen(request, timeout=self.config.timeout_s) as response:
            return json.loads(response.read().decode("utf-8"))

    def call(self, messages: list[dict], *, max_tokens: int | None = None, retries: int = 3) -> tuple[str, dict]:
        payload = {"model": self.config.model, "messages": messages,
                   "thinking": {"type": self.config.thinking},
                   "max_tokens": max_tokens or self.config.max_tokens}
        last = None
        for attempt in range(retries + 1):
            try:
                data = self._send(payload)
                content = (data["choices"][0]["message"].get("content") or "").strip()
                if not content:
                    raise ModelError("empty content in model reply")
                usage = data.get("usage") or {}
                return content, {"calls": 1, "input_tokens": usage.get("prompt_tokens") or 0,
                                 "output_tokens": usage.get("completion_tokens") or 0}
            except urllib.error.HTTPError as error:
                last = ModelError(f"HTTP {error.code}")
                if error.code not in (429, 500, 502, 503, 504):
                    raise last from error
            except (urllib.error.URLError, OSError, ValueError, KeyError, IndexError) as error:
                last = ModelError(f"{type(error).__name__}: {error}")
            except ModelError as error:
                last = error
            if attempt < retries:
                time.sleep(min(60, 4 * 2 ** attempt))
        raise last


_HEADER = re.compile(r"^\s*(\{.*\})\s*$")
_FENCE = re.compile(r"```[a-zA-Z0-9_.-]*\n(.*?)```", re.S)


def parse_reply(text: str) -> tuple[dict, list[str]]:
    """Return (header dict, fenced bodies in order). Raises ModelError."""
    lines = text.strip().splitlines()
    header = None
    for line in lines[:4]:
        match = _HEADER.match(line)
        if match:
            try:
                header = json.loads(match.group(1))
            except ValueError as error:
                raise ModelError(f"bad JSON header: {error}") from error
            break
    if not isinstance(header, dict):
        stripped = text.strip()
        if stripped.startswith("{") and stripped.endswith("}"):
            try:
                header = json.loads(stripped)
            except ValueError as error:
                raise ModelError(f"bad JSON header: {error}") from error
        else:
            raise ModelError("reply has no JSON header line")
    return header, [body for body in _FENCE.findall(text)]


def ask(model: Model, system: str, user: str, *, max_tokens: int | None = None) -> tuple[dict, list[str], dict]:
    """One improver call with a single structured retry on an unparseable reply."""
    messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    text, usage = model.call(messages, max_tokens=max_tokens)
    try:
        header, bodies = parse_reply(text)
    except ModelError as error:
        messages += [{"role": "assistant", "content": text},
                     {"role": "user", "content": f"INVALID REPLY ({error}). Answer again: exactly one JSON "
                                                 "header line first, then any fenced bodies."}]
        text, more = model.call(messages, max_tokens=max_tokens)
        usage = {k: usage.get(k, 0) + more.get(k, 0) for k in ("calls", "input_tokens", "output_tokens")}
        header, bodies = parse_reply(text)
    return header, bodies, usage
