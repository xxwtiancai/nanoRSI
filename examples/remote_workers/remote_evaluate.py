"""Optional HTTP transport for the installed program evaluator (stdlib only).

Copy this file into adapters/remote_evaluate.py. Workers execute trusted local
candidate code; transport authentication does not create a code sandbox.
"""
from __future__ import annotations

import argparse
import hashlib
import http.client
from importlib.resources import files
import ipaddress
import json
import math
import os
from pathlib import Path
import re
import runpy
import socket
import sys
import threading
from urllib.parse import urlsplit

from nanorsi.evaluator import parse_evaluation

MAX_SOURCE_BYTES = 128_000
MAX_BODY_BYTES = 1_000_000
MAX_RESULT_BYTES = 1_000_000
MAX_MANIFEST_BYTES = 4_000_000
IDENTITY_FIELDS = ("request_id", "source_sha256", "manifest_sha256", "evaluator_sha256",
                   "split", "seed", "repeat_id", "train_limit")
REQUEST_FIELDS = frozenset(("source", *IDENTITY_FIELDS))


def bounded_read(path: Path, limit: int) -> bytes:
    with path.open("rb") as stream:
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise ValueError("file exceeds size limit")
    return data


def read_token(path: Path) -> str:
    token = bounded_read(path, 4096).decode("ascii").strip()
    if not re.fullmatch(r"[A-Za-z0-9_-]{32,512}", token):
        raise ValueError("token file must contain 32–512 ASCII letters, digits, underscores or hyphens")
    return token


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def evaluator_sha256() -> str:
    """Fingerprint the installed grading code and its process/template helpers."""
    digest = hashlib.sha256()
    root = files("nanorsi")
    for name in ("templates/program/evaluator/evaluate.py",
                 "templates/skills/evaluator/evaluate.py", "process.py",
                 "evaluator.py", "templates.py"):
        data = root.joinpath(name).read_bytes()
        digest.update(name.encode() + b"\x00" + str(len(data)).encode() + b"\x00" + data)
    return digest.hexdigest()


def fixed_helpers() -> dict:
    # Reuse the evaluator's exact manifest parser and seeded selection policy.
    return runpy.run_path(str(files("nanorsi").joinpath("templates/skills/evaluator/evaluate.py")))


def expected_tasks(manifest: Path, request: dict) -> list[dict]:
    bounded_read(manifest, MAX_MANIFEST_BYTES)
    helpers = fixed_helpers()
    return helpers["_select"](helpers["_manifest"](manifest), request["split"],
                              request["train_limit"], request["seed"])


def validate_request(request: object) -> None:
    if not isinstance(request, dict) or set(request) != REQUEST_FIELDS:
        raise ValueError("request fields do not match the fixed program protocol")
    source = request["source"]
    if not isinstance(source, str) or not source or len(source.encode("utf-8")) > MAX_SOURCE_BYTES:
        raise ValueError("candidate source exceeds size limit or is empty")
    if not isinstance(request["request_id"], str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", request["request_id"]):
        raise ValueError("invalid request_id")
    for key in ("source_sha256", "manifest_sha256", "evaluator_sha256"):
        if not isinstance(request[key], str) or not re.fullmatch(r"[0-9a-f]{64}", request[key]):
            raise ValueError(f"invalid {key}")
    if request["split"] not in ("train", "validation", "test"):
        raise ValueError("invalid split")
    for key, minimum, maximum in (("seed", 0, 2**63 - 1), ("repeat_id", 0, 1_000_000),
                                   ("train_limit", 1, 10_000)):
        value = request[key]
        if isinstance(value, bool) or not isinstance(value, int) or not minimum <= value <= maximum:
            raise ValueError(f"invalid {key}")


def make_request(source: str, manifest: Path, *, split: str, seed: int,
                 repeat_id: int, train_limit: int, request_id: str) -> dict:
    request = {"source": source, "source_sha256": sha256(source.encode("utf-8")),
               "manifest_sha256": sha256(bounded_read(manifest, MAX_MANIFEST_BYTES)),
               "evaluator_sha256": evaluator_sha256(), "split": split,
               "seed": seed, "repeat_id": repeat_id, "train_limit": train_limit,
               "request_id": request_id}
    validate_request(request)
    return request


def validate_response(response: object, request: dict, manifest: Path) -> dict:
    if not isinstance(response, dict) or response.get("schema_version") != 1:
        raise ValueError("invalid worker response schema")
    for key in IDENTITY_FIELDS:
        if response.get(key) != request[key] or type(response.get(key)) is not type(request[key]):
            raise ValueError(f"worker response {key} mismatch")
    if sha256(bounded_read(manifest, MAX_MANIFEST_BYTES)) != request["manifest_sha256"]:
        raise ValueError("local manifest changed during the request")
    worker_id, pid = response.get("worker_id"), response.get("worker_pid")
    if not isinstance(worker_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", worker_id):
        raise ValueError("invalid worker identity")
    if isinstance(pid, bool) or not isinstance(pid, int) or pid <= 0:
        raise ValueError("invalid worker process identity")
    payload = response.get("evaluation")
    if not isinstance(payload, dict) or payload.get("schema_version") != 2:
        raise ValueError("worker must return schema_version 2 evaluation")
    result = parse_evaluation(payload)
    if "score" not in result.metrics or result.usage.get("model_calls") != 0:
        raise ValueError("invalid fixed program evaluation metrics or usage")
    expected = {(task["task_id"], task["group_id"], request["repeat_id"])
                for task in expected_tasks(manifest, request)}
    actual = {(case["task_id"], case["group_id"], case["repeat_id"])
              for case in result.case_results}
    if actual != expected:
        raise ValueError("worker response task identity mismatch")
    for case in result.case_results:
        loaded = {"event": "program_loaded", "path": "target/program.py",
                  "sha256": request["source_sha256"]}
        if not case["trace"] or case["trace"][0] != loaded:
            raise ValueError("worker response candidate trace mismatch")
        if request["split"] != "train" and any(key in case for key in ("task", "feedback")):
            raise ValueError("worker response exposes held-out task details")
    return response


def validate_url(url: str):
    parsed = urlsplit(url)
    if (parsed.scheme not in {"http", "https"} or not parsed.hostname
            or parsed.username is not None or parsed.password is not None
            or parsed.query or parsed.fragment or parsed.path not in {"", "/"}
            or any(character.isspace() for character in url)):
        raise ValueError("worker URL must be an HTTP loopback or HTTPS origin without credentials")
    if parsed.scheme == "http":
        try:
            loopback = ipaddress.ip_address(parsed.hostname).is_loopback
        except ValueError:
            loopback = False
        if not loopback:
            raise ValueError("plaintext HTTP worker URLs require a loopback IP literal")
    if parsed.port is not None and not 1 <= parsed.port <= 65535:
        raise ValueError("invalid worker port")
    return parsed


def _strict_json(data: bytes):
    def reject_constant(_value):
        raise ValueError("non-finite JSON number")

    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON key")
            result[key] = value
        return result

    return json.loads(data, parse_constant=reject_constant, object_pairs_hook=unique_object)


def request_evaluation(url: str, token_file: Path, request: dict, manifest: Path,
                       *, timeout: float = 35, max_result_bytes: int = MAX_RESULT_BYTES) -> dict:
    parsed = validate_url(url)
    if isinstance(timeout, bool) or not math.isfinite(timeout) or not 0 < timeout <= 3600:
        raise ValueError("request timeout must be finite and between 0 and 3600 seconds")
    if isinstance(max_result_bytes, bool) or not isinstance(max_result_bytes, int) or not 0 < max_result_bytes <= MAX_RESULT_BYTES:
        raise ValueError("invalid response size limit")
    body = json.dumps(request, ensure_ascii=False, allow_nan=False).encode("utf-8")
    if len(body) > MAX_BODY_BYTES:
        raise ValueError("request exceeds body limit")
    connection_class = http.client.HTTPSConnection if parsed.scheme == "https" else http.client.HTTPConnection
    connection = connection_class(parsed.hostname, parsed.port, timeout=timeout)
    wire_socket = None

    def abort_connection():
        # HTTP/1.0 detaches the socket from HTTPConnection into HTTPResponse.
        # Retain its identity so the total deadline also interrupts a slow body.
        active_socket = connection.sock or wire_socket
        if active_socket is not None:
            try:
                active_socket.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
        connection.close()

    timer = threading.Timer(timeout, abort_connection)
    timer.daemon = True
    timer.start()
    try:
        connection.request("POST", "/evaluate", body,
                           {"Authorization": "Bearer " + read_token(token_file),
                            "Content-Type": "application/json", "Connection": "close"})
        wire_socket = connection.sock
        response = connection.getresponse()
        if response.status != 200:
            # Do not reflect remote text, which could contain credentials or labels.
            raise ValueError(f"worker HTTP status {response.status}")
        if response.getheader("Content-Type", "").split(";")[0] != "application/json":
            raise ValueError("worker response is not JSON")
        length = response.getheader("Content-Length")
        if length is None or not length.isdecimal() or int(length) > max_result_bytes:
            raise ValueError("worker response exceeds size limit or has no length")
        data = response.read(max_result_bytes + 1)
        if len(data) > max_result_bytes or len(data) != int(length):
            raise ValueError("worker response exceeds size limit or is incomplete")
        return validate_response(_strict_json(data), request, manifest)
    except (OSError, http.client.HTTPException) as error:
        raise ValueError("worker connection failed or exceeded timeout") from error
    finally:
        timer.cancel()
        connection.close()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--urls", nargs="+", required=True)
    parser.add_argument("--token-file", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=35)
    args = parser.parse_args(argv)
    try:
        result_path = Path(os.environ["NANORSI_RESULT_PATH"])
        manifest = Path(os.environ["NANORSI_TASK_MANIFEST"])
        source = bounded_read(Path("target/program.py"), MAX_SOURCE_BYTES).decode("utf-8")
        request_id = sha256(str(result_path.resolve()).encode())
        request = make_request(source, manifest, split=os.environ["NANORSI_SPLIT"],
                               seed=int(os.environ.get("NANORSI_SEED", "0")),
                               repeat_id=int(os.environ.get("NANORSI_REPEAT_ID", "0")),
                               train_limit=int(os.environ.get("NANORSI_TRAIN_LIMIT", "4")),
                               request_id=request_id)
        for url in args.urls:
            validate_url(url)
        url = args.urls[int(request_id, 16) % len(args.urls)]
        response = request_evaluation(url, args.token_file, request, manifest, timeout=args.timeout)
        payload = response["evaluation"]
        payload["remote_worker"] = {key: value for key, value in response.items() if key != "evaluation"}
        result_path.parent.mkdir(parents=True, exist_ok=True)
        result_path.write_text(json.dumps(payload, ensure_ascii=False, allow_nan=False), encoding="utf-8")
        return 0
    except (OSError, ValueError, KeyError, RecursionError):
        print("remote evaluation failed; verify worker availability, identities and limits", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
