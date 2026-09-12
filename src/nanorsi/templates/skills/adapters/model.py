"""OpenAI-compatible chat-completions bridge for the skills template.

The endpoint and credentials are explicit request fields. No credential is
read from an ambient environment variable.
"""

from __future__ import annotations

import json
import math
from http.client import HTTPException
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


MAX_RESPONSE_BYTES = 1_000_000
MAX_KEY_BYTES = 8192
ERROR_MESSAGES = {
    "authentication": "Authentication failed; check api_key_file and the provider account.",
    "permission": "Access denied; check the key permissions and model access.",
    "not_found": "Endpoint or model not found; check base_url and model.",
    "rate_limit": "Provider rate or quota limit reached; check account limits and retry later.",
    "bad_request": "Provider rejected the request; check model and token_parameter settings.",
    "server_error": "Provider server failed; retry later.",
    "redirect": "Redirect refused; set base_url to the provider's final API endpoint.",
    "network": "Could not reach the provider; check connectivity, base_url and timeout_s.",
    "configuration": "Invalid model configuration; check base_url, model, api_key_file and token settings.",
    "invalid_response": "Provider returned an invalid or oversized chat-completions response.",
}


class AdapterError(ValueError):
    """A stable failure whose message contains no request or provider data."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(ERROR_MESSAGES[code])


class _NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _http_error(status: int) -> AdapterError:
    if 300 <= status < 400:
        code = "redirect"
    elif status >= 500:
        code = "server_error"
    else:
        code = {401: "authentication", 403: "permission", 404: "not_found", 429: "rate_limit", 400: "bad_request", 422: "bad_request"}.get(status, "invalid_response")
    return AdapterError(code)


def _endpoint(base_url: str) -> str:
    if not isinstance(base_url, str) or not base_url or any(char.isspace() or ord(char) < 32 or 127 <= ord(char) <= 159 for char in base_url) or "?" in base_url or "#" in base_url:
        raise AdapterError("configuration")
    try:
        parsed = urlsplit(base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username is not None or parsed.password is not None:
            raise ValueError("invalid endpoint")
        if parsed.netloc.endswith(":") or (parsed.port is not None and parsed.port <= 0):
            raise ValueError("invalid port")
    except ValueError:
        raise AdapterError("configuration") from None
    base_url = base_url.rstrip("/")
    if base_url.endswith("/chat/completions"):
        return base_url
    return base_url + "/chat/completions"


def _provider_identity(payload: dict, secret: str | None) -> dict:
    result = {}
    for key, source in [('model', 'model'), ('request_id', 'id')]:
        value = payload.get(source)
        if isinstance(value, str) and len(value) <= 200 and not any(c.isspace() or ord(c) < 32 for c in value):
            if not secret or secret not in value:
                result[key] = value
    return result


def call(request: dict) -> dict:
    if not isinstance(request, dict):
        raise AdapterError("configuration")
    model = request.get("model")
    base_url = request.get("base_url")
    key_file = request.get("api_key_file")
    if not isinstance(model, str) or not model:
        raise AdapterError("configuration")
    endpoint = _endpoint(base_url)
    headers = {"Content-Type": "application/json"}
    if key_file is not None:
        if not isinstance(key_file, str) or not key_file:
            raise AdapterError("configuration")
        try:
            path = Path(key_file)
            if not path.is_file():
                raise AdapterError("configuration")
            with path.open("rb") as stream:
                data = stream.read(MAX_KEY_BYTES + 1)
            if len(data) > MAX_KEY_BYTES:
                raise AdapterError("configuration")
            api_key = data.decode("utf-8").strip()
        except (OSError, UnicodeError, ValueError):
            raise AdapterError("configuration") from None
        if not api_key or any(not 33 <= ord(char) <= 126 for char in api_key):
            raise AdapterError("configuration")
        headers["Authorization"] = "Bearer " + api_key
    payload = {"model": model, "messages": request.get("messages", [])}
    if 'thinking' in request:
        if request['thinking'] not in ('enabled', 'disabled'):
            raise AdapterError('configuration')
        payload['thinking'] = {'type': request['thinking']}
    token_parameter = request.get("token_parameter", "max_tokens")
    if token_parameter not in ("max_tokens", "max_completion_tokens"):
        raise AdapterError("configuration")
    if request.get("max_tokens") is not None:
        payload[token_parameter] = request["max_tokens"]
    timeout = request.get("timeout_s", 60)
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
        raise AdapterError("configuration")
    try:
        timeout_value = float(timeout)
    except (TypeError, ValueError, OverflowError):
        raise AdapterError("configuration") from None
    if not math.isfinite(timeout_value) or timeout_value <= 0:
        raise AdapterError("configuration")
    try:
        response_request = Request(endpoint, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        with build_opener(_NoRedirects()).open(response_request, timeout=timeout_value) as response:
            if not 200 <= response.status < 300:
                raise _http_error(response.status)
            body = response.read(MAX_RESPONSE_BYTES + 1)
    except HTTPError as error:
        error.close()
        raise _http_error(error.code) from None
    except (OSError, URLError, HTTPException):
        raise AdapterError("network") from None
    except (TypeError, UnicodeError, ValueError, OverflowError) as error:
        if isinstance(error, AdapterError):
            raise
        raise AdapterError("configuration") from None
    if len(body) > MAX_RESPONSE_BYTES:
        raise AdapterError("invalid_response")
    try:
        response_payload = json.loads(body.decode("utf-8"))
    except (UnicodeError, ValueError, RecursionError):
        raise AdapterError("invalid_response") from None
    choices = response_payload.get("choices") if isinstance(response_payload, dict) else None
    if not isinstance(choices, list) or not choices or not isinstance(choices[0], dict):
        raise AdapterError("invalid_response")
    message = choices[0].get("message")
    if not isinstance(message, dict) or not isinstance(message.get("content"), str) or not message["content"]:
        raise AdapterError("invalid_response")
    upstream_usage = response_payload.get("usage", {})
    if not isinstance(upstream_usage, dict):
        upstream_usage = {}
    provider = _provider_identity(response_payload, headers.get('Authorization', '').removeprefix('Bearer ') or None)
    return {"content": message["content"], "provider": provider, "usage": {"model_calls": 1, "input_tokens": upstream_usage.get("prompt_tokens"), "output_tokens": upstream_usage.get("completion_tokens"), "cost_usd": upstream_usage.get("cost_usd")}}


def main() -> None:
    try:
        request = json.load(sys.stdin)
        result = call(request)
    except AdapterError as error:
        result = {"error_code": error.code, "error": str(error)}
    except (OSError, ValueError, TypeError, KeyError, RecursionError):
        result = {"error_code": "configuration", "error": ERROR_MESSAGES["configuration"]}
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
