from __future__ import annotations

import shutil
import json
from importlib.resources import files
from pathlib import Path


class TemplateError(ValueError):
    pass


def _copy(source, destination: Path) -> None:
    if source.is_dir():
        if source.name in {"__pycache__", ".ipynb_checkpoints"}:
            return
        destination.mkdir(parents=True, exist_ok=True)
        for child in source.iterdir():
            _copy(child, destination / child.name)
    elif source.is_file():
        if source.suffix in {".pyc", ".pyo"}:
            return
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def render_template(name: str, destination: Path, *, goal: str) -> list[str]:
    if name not in {"artifact", "harness", "model", "skills", "coding"}:
        raise TemplateError(f"unknown template: {name}")
    root = files("nanorsi").joinpath("templates", name)
    if destination.exists():
        raise TemplateError(f"destination already exists: {destination}")
    destination.mkdir(parents=True)
    if name == "coding":
        _copy(files("nanorsi").joinpath("templates", "skills"), destination)
        shutil.copyfile(destination / "evaluator/evaluate.py", destination / "evaluator/_skills.py")
    _copy(root, destination)
    config_path = destination / "nanorsi.toml"
    config = config_path.read_text(encoding="utf-8").replace('"{{GOAL}}"', json.dumps(goal, ensure_ascii=False))
    config_path.write_text(config, encoding="utf-8")
    return sorted(path.relative_to(destination).as_posix() for path in destination.rglob("*") if path.is_file())
