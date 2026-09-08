from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .config import Config
from .process import run_argv
from .surface import SurfacePolicy, changed_paths_from_unified_diff


class ProposalError(ValueError):
    pass


@dataclass(frozen=True)
class Proposal:
    hypothesis: dict
    diff: str
    changed_paths: list[str]


def load_proposal(directory: Path, include: list[str] | None = None, deny: list[str] | None = None, *, allow_noop=False) -> Proposal:
    diff_path = directory / "proposal.diff"
    hypothesis_path = directory / "hypothesis.json"
    try:
        diff = diff_path.read_text(encoding="utf-8")
        hypothesis = json.loads(hypothesis_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ProposalError(f"invalid proposal files: {error}") from error
    if not isinstance(hypothesis, dict) or (not diff.strip() and not allow_noop):
        raise ProposalError("proposal requires hypothesis.json and a non-empty diff")
    if not diff.strip():
        return Proposal(hypothesis, diff, [])
    try:
        paths = changed_paths_from_unified_diff(diff)
        if include is not None:
            paths = SurfacePolicy(include, deny or []).validate_paths(paths)
    except ValueError as error:
        raise ProposalError(str(error)) from error
    if not paths:
        raise ProposalError("proposal diff changes no files")
    return Proposal(hypothesis, diff, paths)


def run_proposer(config: Config, parent: Path, output: Path, context: dict, *, extra_env=None) -> Proposal:
    output.mkdir(parents=True, exist_ok=True)
    context_path = output / "context.json"
    context_path.write_text(json.dumps(context, sort_keys=True, indent=2), encoding="utf-8")
    result = run_argv(
        config.proposer.command,
        cwd=parent,
        timeout_s=config.proposer.timeout_s,
        extra_env={"NANORSI_PROPOSAL_DIR": str(output), "NANORSI_CONTEXT_PATH": str(context_path),
                   "PYTHONDONTWRITEBYTECODE": "1", **(extra_env or {})},
        max_output_bytes=config.budget.max_output_bytes,
    )
    if result.timed_out or result.output_limited or result.exit_code != 0:
        raise ProposalError(result.stderr.strip() or result.stdout.strip() or "proposer failed")
    if any(p.stat().st_size > config.budget.max_output_bytes for p in output.iterdir() if p.is_file()):
        raise ProposalError("proposal output exceeds byte limit")
    if (output / "usage.json").is_file():
        from .evaluator import _validate_usage
        _validate_usage(json.loads((output / "usage.json").read_text()), "proposal usage")
    return load_proposal(output, config.surface.allow, config.surface.deny, allow_noop=config.experiment.schema_version == 2)
