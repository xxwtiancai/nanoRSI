"""Serializable, credential-free request receipts for bounded live demos.

Copied next to the normal model.py bridge. POSIX flock releases on crashes;
an unfinished request reservation still consumes the request cap.
"""
import argparse
from datetime import datetime, timezone
import fcntl
from hashlib import sha256
import importlib.util
import json
import os
from pathlib import Path
import sys
import time
import uuid


def append(stream, event):
    stream.seek(0, 2)
    stream.write(json.dumps(event, sort_keys=True) + '\n')
    stream.flush()
    os.fsync(stream.fileno())


def run_request(request, ledger, limit, call):
    if type(limit) is not int or not 1 <= limit <= 1000:
        raise ValueError('request limit must be between 1 and 1000')
    ledger = Path(ledger)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open('a+', encoding='utf-8') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        stream.seek(0)
        events = [json.loads(line) for line in stream if line.strip()]
        spent = sum(e.get('event') == 'request_started' for e in events)
        if spent >= limit:
            return {'error_code': 'budget_exhausted', 'error': 'Live demo request cap reached', 'usage': {'model_calls': 0}}
        identity = uuid.uuid4().hex
        public = {k: v for k, v in request.items() if k != 'api_key_file'}
        started = time.monotonic()
        append(stream, {'event': 'request_started', 'id': identity, 'request_number': spent + 1,
                        'model': request.get('model'), 'request_sha256': sha256(json.dumps(public, sort_keys=True).encode()).hexdigest(),
                        'recorded_at': datetime.now(timezone.utc).isoformat()})
        try:
            result = call(request)
        except Exception as error:
            code = getattr(error, 'code', 'bridge_error')
            code = code if code in {'authentication', 'permission', 'not_found', 'rate_limit', 'bad_request', 'server_error', 'redirect', 'network', 'configuration', 'invalid_response'} else 'bridge_error'
            result = {'error_code': code, 'error': 'Model request failed; see provider error category'}
        provider = result.get('provider', {})
        if not result.get('error_code') and provider.get('model') != request.get('model'):
            result = {'error_code': 'model_identity_mismatch', 'error': 'Provider did not confirm the requested model identity', 'provider': provider}
        append(stream, {'event': 'request_finished', 'id': identity,
                        'status': result.get('error_code', 'ok'), 'provider': provider,
                        'usage': result.get('usage', {}), 'duration_ms': round((time.monotonic() - started) * 1000)})
        return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ledger', type=Path, required=True)
    parser.add_argument('--max-requests', type=int, required=True)
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location('demo_provider_bridge', Path(__file__).with_name('model.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        response = run_request(json.load(sys.stdin), args.ledger, args.max_requests, module.call)
    except Exception:
        response = {'error_code': 'bridge_error', 'error': 'Invalid request or unavailable request ledger'}
    print(json.dumps(response, allow_nan=False))


if __name__ == '__main__':
    main()
