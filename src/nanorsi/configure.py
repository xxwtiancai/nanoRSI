"""Explicit model configuration without putting credentials in experiments."""
from __future__ import annotations

import getpass
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import warnings

from .config import _read, credential_path, load_config, validate_endpoint
from .locking import Lock


def read_key(path: Path) -> str:
    try:
        if not path.is_file():
            raise OSError('not a regular file')
        with path.open('rb') as stream:
            raw = stream.read(8193)
        key = raw.decode('utf-8').strip()
    except (OSError, UnicodeError) as error:
        raise ValueError('API key file is missing, unreadable or not UTF-8; check api_key_file') from error
    if len(raw) > 8192 or not key or any(c.isspace() or ord(c) < 33 or ord(c) > 126 for c in key):
        raise ValueError('API key file must contain one nonempty token of at most 8192 bytes')
    return key


def _prompt_key(root: Path) -> Path:
    if not sys.stdin.isatty():
        raise ValueError('--prompt-key requires an interactive terminal; use --api-key-file for automation')
    with warnings.catch_warnings():
        warnings.simplefilter('error', getpass.GetPassWarning)
        try:
            key = getpass.getpass('API key (hidden; saved outside the workspace): ').strip()
        except (getpass.GetPassWarning, EOFError) as error:
            raise ValueError('cannot safely read a hidden key; use --api-key-file') from error
    if not key or len(key.encode()) > 8192 or any(c.isspace() or ord(c) < 33 or ord(c) > 126 for c in key):
        raise ValueError('API key must be one nonempty token')
    directory = (Path.home() / '.config/nanorsi/keys').resolve()
    if directory.is_relative_to(root.resolve()):
        raise ValueError('credential directory must be outside the experiment workspace')
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    descriptor, name = tempfile.mkstemp(prefix='model-', suffix='.key', dir=directory)
    try:
        with os.fdopen(descriptor, 'w', encoding='utf-8') as stream:
            stream.write(key + '\n')
    except BaseException:
        Path(name).unlink(missing_ok=True)
        raise
    return Path(name)


def _section(text: str, section: str, updates: dict) -> str:
    lines = text.splitlines(keepends=True)
    start = next((i for i, line in enumerate(lines) if re.fullmatch(r'\s*\[' + section + r'\]\s*(?:#.*)?', line.rstrip('\n'))), None)
    if start is None:
        raise ValueError(f'configure requires a standard [{section}] table; edit this TOML layout manually')
    end = next((i for i in range(start + 1, len(lines)) if re.match(r'\s*\[', lines[i])), len(lines))
    block, remaining = [], dict(updates)
    for line in lines[start + 1:end]:
        match = re.match(r'\s*([A-Za-z_][A-Za-z0-9_]*)\s*=', line)
        key = match.group(1) if match else None
        if key in updates:
            if updates[key] is not None:
                block.append(f'{key} = {json.dumps(updates[key], ensure_ascii=False)}\n')
            remaining.pop(key, None)
        else:
            block.append(line if line.endswith('\n') else line + '\n')
    block.extend(f'{key} = {json.dumps(value, ensure_ascii=False)}\n' for key, value in remaining.items() if value is not None)
    return ''.join(lines[:start + 1] + block + lines[end:])


def _replace_config(path: Path, text: str, expected: dict) -> None:
    descriptor, name = tempfile.mkstemp(prefix='.nanorsi-config-', suffix='.toml', dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, 'w', encoding='utf-8') as stream:
            stream.write(text)
        if _read(temporary) != expected:
            raise ValueError('unsupported TOML layout; edit model settings manually to preserve unrelated values')
        load_config(temporary)
        temporary.chmod(path.stat().st_mode & 0o777)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def configure(root: Path, *, model: str, base_url: str, api_key_file: Path | None = None,
              prompt_key: bool = False, no_api_key: bool = False, max_steps: int | None = None,
              max_episodes: int | None = None, token_parameter: str | None = None) -> str:
    root = root.resolve()
    if sum([api_key_file is not None, prompt_key, no_api_key]) != 1:
        raise ValueError('choose exactly one of --prompt-key, --api-key-file or --no-api-key')
    if not isinstance(model, str) or not model.strip() or any(c.isspace() for c in model) or model == 'configure-your-model':
        raise ValueError('model must be the exact nonempty model ID from your provider')
    updates = {'model': model, 'base_url': validate_endpoint(base_url)}
    if token_parameter is not None:
        if token_parameter not in {'max_tokens', 'max_completion_tokens'}:
            raise ValueError('token_parameter must be max_tokens or max_completion_tokens')
        updates['token_parameter'] = token_parameter
    budget = {key: value for key, value in [('max_steps', max_steps), ('max_episodes', max_episodes)] if value is not None}
    if any(type(value) is not int or value <= 0 for value in budget.values()):
        raise ValueError('attempt and episode budgets must be positive integers')
    with Lock(root):
        return _configure_locked(root, updates, budget, api_key_file, prompt_key)


def _configure_locked(root: Path, updates: dict, budget: dict, api_key_file: Path | None, prompt_key: bool) -> str:
    path, journal = root / 'nanorsi.toml', root / 'lineage.jsonl'
    if path.is_symlink():
        raise ValueError('configuration file must not be a symlink')
    if journal.exists() and journal.stat().st_size:
        raise ValueError('experiment has started; create a new workspace to change frozen model settings')
    expected = _read(path)
    experiment = expected.get('experiment')
    if not isinstance(experiment, dict) or experiment.get('schema_version') != 2:
        raise ValueError('configure requires a coding or skills schema-v2 workspace')
    text, created = path.read_text(encoding='utf-8'), None
    if api_key_file is not None:
        key = credential_path(root, str(api_key_file.expanduser().absolute()))
        read_key(key)
        updates['api_key_file'] = str(key)
    elif prompt_key:
        created = _prompt_key(root)
        updates['api_key_file'] = str(created)
    else:
        updates['api_key_file'] = None
    try:
        text = _section(text, 'agent', updates)
        if budget:
            text = _section(text, 'budget', budget)
        for section, changes in [('agent', updates), ('budget', budget)]:
            for key, value in changes.items():
                if value is None:
                    expected[section].pop(key, None)
                else:
                    expected[section][key] = value
        _replace_config(path, text, expected)
    except BaseException:
        if created:
            created.unlink(missing_ok=True)
        raise
    auth = f"external key file: {updates['api_key_file']}" if updates['api_key_file'] else 'no API key (anonymous endpoint)'
    return f'Configured model: {updates["model"]}\nAuthentication: {auth}\nNext: nanorsi doctor --workspace {root} --check-model\n'
