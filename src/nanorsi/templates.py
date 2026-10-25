"""The one starter template: a base harness, an offline task set the loopback runner
can execute, and a keyword judge so the whole loop runs without a benchmark."""
from __future__ import annotations

import json
import shutil
import sys
from importlib.resources import files
from pathlib import Path


class TemplateError(ValueError):
    pass


def _copy(source, destination: Path) -> None:
    if source.is_dir():
        if source.name == "__pycache__":
            return
        destination.mkdir(parents=True, exist_ok=True)
        for child in source.iterdir():
            _copy(child, destination / child.name)
    elif source.is_file() and not source.name.endswith((".pyc", ".pyo")):
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def render(destination: Path, *, goal: str) -> list[str]:
    destination = Path(destination)
    if destination.exists():
        raise TemplateError(f"destination already exists: {destination}")
    _copy(files("nanorsi").joinpath("templates", "default"), destination)
    config_path = destination / "nanorsi.toml"
    text = config_path.read_text(encoding="utf-8").replace('"{{GOAL}}"', json.dumps(goal, ensure_ascii=False))
    text = text.replace('"{{PYTHON}}"', json.dumps(sys.executable))
    config_path.write_text(text, encoding="utf-8")
    return sorted(p.relative_to(destination).as_posix() for p in destination.rglob("*") if p.is_file())
