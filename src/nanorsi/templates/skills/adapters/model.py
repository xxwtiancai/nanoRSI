"""OpenAI-compatible chat-completions bridge for the skills template.

The endpoint and credentials are explicit request fields. No credential is
read from an ambient environment variable.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


MAX_RESPONSE_BYTES = 1_000_000


def _endpoint(base_url: str) -> str:
    base_url = base_url.rstrip("/")
    if base_url.endswith("/chat/completions"):
        return base_url
    return base_url + "/chat/completions"


def call(request: dict) -> dict:
    model = request.get("model")
    base_url = request.get("base_url")
    key_file = request.get("api_key_file")
    if not isinstance(model, str) or not model:
        raise ValueError("model is required")
    if not isinstance(base_url, str) or not base_url:
        raise ValueError("base_url is required")
    headers = {"Content-Type": "application/json"}
    if key_file is not None:
        if not isinstance(key_file, str) or not key_file:
            raise ValueError("api_key_file must be a non-empty path when supplied")
        api_key = Path(key_file).read_text(encoding="utf-8").strip()
        if not api_key:
            raise ValueError("api_key_file is empty")
        headers["Authorization"] = "Bearer " + api_key
    payload = {"model": model, "messages": request.get("messages", [])}
    if request.get("max_tokens") is not None:
        payload["max_tokens"] = request["max_tokens"]
    timeout = request.get("timeout_s", 60)
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
        raise ValueError("timeout_s must be a finite positive number")
    try:
        timeout_value = float(timeout)
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError("timeout_s must be a finite positive number") from error
    if not math.isfinite(timeout_value) or timeout_value <= 0:
        raise ValueError("timeout_s must be a finite positive number")
    response_request = Request(_endpoint(base_url), data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    with urlopen(response_request, timeout=timeout_value) as response:
        body = response.read(MAX_RESPONSE_BYTES + 1)
        if len(body) > MAX_RESPONSE_BYTES:
            raise ValueError("response exceeded output limit")
        response_payload = json.loads(body.decode("utf-8"))
    choices = response_payload.get("choices") if isinstance(response_payload, dict) else None
    if not isinstance(choices, list) or not choices or not isinstance(choices[0], dict):
        raise ValueError("response has no choices")
    message = choices[0].get("message")
    if not isinstance(message, dict) or not isinstance(message.get("content"), str):
        raise ValueError("response choice has no message content")
    upstream_usage = response_payload.get("usage", {})
    if not isinstance(upstream_usage, dict):
        upstream_usage = {}
    return {"content": message["content"], "usage": {"model_calls": 1, "input_tokens": upstream_usage.get("prompt_tokens"), "output_tokens": upstream_usage.get("completion_tokens"), "cost_usd": upstream_usage.get("cost_usd")}}


def main() -> None:
    try:
        request = json.load(sys.stdin)
        result = call(request)
    except (OSError, ValueError, TypeError, KeyError, HTTPError, URLError, json.JSONDecodeError) as error:
        result = {"error": str(error)[:200]}
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
