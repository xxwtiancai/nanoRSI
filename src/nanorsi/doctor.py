from __future__ import annotations

import shutil
import json
from pathlib import Path

from .config import Config, load_config
from .gitops import Git
from .configure import read_key
from .config import credential_path
from .process import run_argv


MODEL_ERRORS = {
    'authentication': 'API key rejected (401); check the external key file and provider account.',
    'permission': 'Access denied (403); check model/project permissions.',
    'not_found': 'Endpoint or model not found (404); check base_url and exact model ID.',
    'rate_limit': 'Rate limit or quota exceeded (429); check provider limits before retrying.',
    'bad_request': 'Request rejected; check model compatibility and token_parameter.',
    'server_error': 'Provider server error; retry the check later.',
    'redirect': 'Redirect refused; configure the trusted final endpoint directly.',
    'network': 'Network/TLS connection failed; check endpoint, connection and certificates.',
    'configuration': 'Bridge configuration invalid; check endpoint, key file and token_parameter.',
    'invalid_response': 'Response must contain valid message content; check model/API compatibility.',
}


def _model_status(root: Path, config: Config) -> tuple[bool, list[str]]:
    agent = config.agent
    ready = agent['model'] not in {'configure-your-model', 'your-model-id', 'YOUR_MODEL_ID'}
    command_ok = _command_status(root, agent['model_command']) == 'ok'
    lines = [f"model: {agent['model']} ({'configured' if ready else 'run nanorsi configure first'})",
             f"model command: {'ok' if command_ok else 'missing'}"]
    ready = ready and command_ok
    if agent.get('base_url'):
        lines.append(f"endpoint: {agent['base_url']}")
    elif 'adapters/model.py' in agent['model_command']:
        lines.append('endpoint: missing; configure agent.base_url')
        ready = False
    if 'api_key_file' in agent:
        try:
            read_key(credential_path(root, agent['api_key_file']))
            lines.append('authentication: external key file readable (key not displayed)')
        except ValueError as error:
            lines.append(f'authentication: {error}')
            ready = False
    else:
        lines.append('authentication: no key; endpoint must accept anonymous requests')
    return ready, lines


def _check_model(root: Path, config: Config) -> tuple[bool, str]:
    request = {key: config.agent[key] for key in ['model', 'base_url', 'api_key_file', 'max_tokens', 'token_parameter', 'timeout_s'] if key in config.agent}
    request['messages'] = [{'role': 'system', 'content': 'Return exactly one JSON object: {"tool":"final"}. No Markdown or explanation.'},
                           {'role': 'user', 'content': 'Check the JSON action protocol.'}]
    result = run_argv(config.agent['model_command'], cwd=root, timeout_s=min(config.agent['timeout_s'], 60),
                      max_output_bytes=1_000_000, input_text=json.dumps(request))
    if result.timed_out:
        return False, 'model check: timed out; check endpoint availability and model latency'
    if result.output_limited or result.exit_code != 0:
        return False, 'model check: bridge failed or exceeded output limit; check model_command'
    try:
        envelope = json.loads(result.stdout)
        if not isinstance(envelope, dict):
            raise ValueError
        if 'error' in envelope or 'error_code' in envelope:
            detail = MODEL_ERRORS.get(envelope.get('error_code'), 'Bridge reported an error; check configuration and provider status.')
            return False, 'model check: ' + detail
        action = json.loads(envelope['content'])
        if not isinstance(action, dict) or action.get('tool') != 'final':
            raise ValueError
    except (ValueError, TypeError, KeyError):
        return False, 'model check: invalid JSON action; model must return {"tool":"final"}. Check token limit/model compatibility.'
    return True, 'model check: ok (one request; JSON action valid; no experiment started)'


def _command_status(root: Path, command: list[str]) -> str:
    if not command:
        return "missing"
    first = command[0]
    if len(command) > 1 and Path(first).name.startswith(('python', 'pypy')) and command[1].endswith('.py'):
        if not (root / command[1]).is_file():
            return 'missing'
    if "/" in first:
        return "ok" if (root / first).exists() else "missing"
    return "ok" if shutil.which(first) else "missing"


def doctor(root: Path, *, check_model: bool = False) -> tuple[bool, str]:
    try:
        config = load_config(root / "nanorsi.toml")
    except Exception as error:
        return False, f"config: invalid ({error})\n"
    lines = [
        f"config: ok ({config.experiment.mode})",
        f"git: {'ok' if _git_ok(root) else 'missing'}",
        f"proposer command: {' '.join(config.proposer.command)} ({_command_status(root, config.proposer.command)})",
        f"evaluator command: {' '.join(config.evaluator.command)} ({_command_status(root, config.evaluator.command)})",
        f"execution: local subprocess; sandbox is caller responsibility",
    ]
    if config.experiment.mode == "model":
        lines.extend(
            [
                "model: external training contract",
                f"training command: {' '.join(config.training['command'])}",
                f"compute budget: {config.training.get('compute_budget_s', 'unbounded')} seconds",
            ]
        )
    ready = _git_ok(root) and all(_command_status(root, command) == "ok" for command in [config.proposer.command, config.evaluator.command])
    if config.experiment.schema_version == 2:
        from .loop import tasks
        try:
            rows = tasks(root, config)
            lines.append(f"task manifest: ok ({len(rows)} tasks; disjoint source groups)")
        except (OSError, ValueError, KeyError) as error:
            lines.append(f"task manifest: invalid ({error})")
            ready = False
        model_ready, model_lines = _model_status(root, config)
        lines.extend(model_lines + [f"proposer harness: {config.experiment.arm}",
                      "budget: attempts/episodes/time/output bounded; dollar usage reported, not a hard cap"])
        ready = ready and model_ready
    if check_model:
        if config.experiment.schema_version != 2:
            return False, '\n'.join(lines + ['model check requires a coding or skills schema-v2 workspace']) + '\n'
        if ready:
            ready, result = _check_model(root, config)
            lines.append(result)
        else:
            lines.append('model check: skipped; fix offline checks first')
    elif config.experiment.schema_version == 2:
        lines.append('model connection: not checked; use --check-model (one request, may incur API cost)')
    return ready, "\n".join(lines) + "\n"


def _git_ok(root: Path) -> bool:
    try:
        Git(root).ensure_repository()
        return True
    except Exception:
        return False
