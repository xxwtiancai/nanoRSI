"""Content identities for fixed experiment machinery and comparable panels."""
from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
from pathlib import Path
import shlex

from .hashing import canonical_hash, tree_hash
from .paths import contained_path


CACHE_PATTERNS = ["__pycache__", "__pycache__/**", "**/__pycache__/**"]


def source_hash(path):
    if path.is_dir():
        return tree_hash(path, exclude=CACHE_PATTERNS)
    return sha256(path.read_bytes()).hexdigest() if path.exists() else None


def comparison_hash(root, config):
    """Arm/seed and credential locations vary; evaluation machinery must not."""
    from .loop import tasks
    agent = {key: value for key, value in config.agent.items()
             if key not in {"api_key_file", "api_key", "apikey", "authorization"}}
    evaluator = asdict(config.evaluator)
    if evaluator["train_limit"] == 4:  # Preserve historical default comparison hashes.
        evaluator.pop("train_limit")
    return canonical_hash({
        "contract_version": 2,
        "mode": config.experiment.mode,
        "conditions": config.experiment.final_conditions,
        "tasks": tasks(root, config),
        "fixed": {name: source_hash(contained_path(root, name))
                  for name in ["evaluator", "proposer", "adapters", "trainer"]},
        "initial_target": source_hash(root / "target"),
        "initial_checkpoint": source_hash(contained_path(root, config.training["checkpoint"])) if config.training else None,
        "agent": agent, "training": config.training,
        "surface": asdict(config.surface), "proposer": asdict(config.proposer),
        "evaluator": evaluator, "gate": asdict(config.gate),
        "budget": asdict(config.budget), "safety": config.safety,
    })


def _env_command(root, arguments):
    arguments = list(arguments)
    while arguments:
        option = arguments.pop(0)
        if option == "--":
            break
        if option in {"-u", "--unset"}:
            arguments.pop(0)
        elif option in {"-C", "--chdir"}:
            root = root / arguments.pop(0)
        elif option.startswith("--chdir="):
            root = root / option.split("=", 1)[1]
        elif option in {"-S", "--split-string"}:
            arguments = shlex.split(arguments.pop(0)) + arguments
        elif option.startswith("--split-string="):
            arguments = shlex.split(option.split("=", 1)[1]) + arguments
        elif option in {"-", "-i", "--ignore-environment"} or "=" in option:
            continue
        elif option.startswith("-"):
            raise ValueError("unsupported env option in training.command")
        else:
            arguments.insert(0, option)
            break
    return root, arguments


def _script_entrypoints(root, arguments, python):
    arguments = iter(arguments)
    for option in arguments:
        if option == "--":
            return [root / next(arguments, "")]
        if python and option == "--check-hash-based-pycs":
            next(arguments, None)
            continue
        if option.startswith("--"):
            if not python:
                raise ValueError("unsupported shell launcher option; use a protected wrapper under trainer/")
            continue
        if option.startswith("-") and option != "-":
            if python:
                marker = next(((i, c) for i, c in enumerate(option[1:]) if c in "cmWX"), None)
                if marker:
                    index, kind = marker
                    value = option[index + 2:] or next(arguments, "")
                    if kind == "c":
                        return []
                    if kind == "m":
                        module = value.replace(".", "/")
                        return [root / (module + ".py"), root / module / "__main__.py"]
            elif "c" in option[1:] or "s" in option[1:]:
                return []
            elif option in {"-o", "-O"}:
                next(arguments, None)
            continue
        return [] if option == "-" else [root / option]
    return []


def training_entrypoints(root, command):
    """Potential direct entrypoints, not the trainer's imported architecture."""
    sources, command = [], list(command)
    while command:
        name = Path(command[0]).name
        executable = root / command[0]
        if "/" in command[0] or executable.is_file():
            sources.append(executable)
        if name == "env":
            root, command = _env_command(root, command[1:])
            continue
        python = name.startswith(("python", "pypy"))
        if python or name in {"sh", "bash", "zsh", "dash", "ksh"}:
            sources.extend(_script_entrypoints(root, command[1:], python))
        break
    return sources
