"""LAB (harvey-labs) access for the harness2-minimal study: tasks, documents, judging.

The benchmark checkout, its Python environment and the judge module all belong
to harvey-labs (MIT) / harness2 (Apache-2.0); this file only reads tasks and
drives their scorer. Paths come from run.py arguments.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

DOC_CAP = 24000

_XLSX_PPTX_SRC = r'''
import sys
from pathlib import Path
name, path = sys.argv[1], Path(sys.argv[2])
out = []
if name.endswith(".xlsx"):
    import openpyxl
    book = openpyxl.load_workbook(path, data_only=True)
    for sheet in book.worksheets:
        out.append(f"## sheet: {sheet.title}")
        for row in sheet.iter_rows(values_only=True):
            cells = ["" if c is None else str(c) for c in row]
            if any(c.strip() for c in cells):
                out.append(" | ".join(cells))
else:
    from pptx import Presentation
    deck = Presentation(str(path))
    for i, slide in enumerate(deck.slides, 1):
        out.append(f"## slide {i}")
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    text = "".join(run.text for run in para.runs)
                    if text.strip():
                        out.append(text)
print("\n".join(out))
'''


def load_task(lab_root, task_name):
    task_dir = Path(lab_root) / "tasks" / task_name
    config = json.loads((task_dir / "task.json").read_text(encoding="utf-8"))
    documents = {}
    docs_dir = task_dir / "documents"
    if docs_dir.is_dir():
        for path in sorted(docs_dir.iterdir()):
            if path.is_file():
                documents[path.name] = path
    deliverables = list(config.get("deliverables", {}))
    return {"name": task_name, "title": config["title"], "instructions": config["instructions"],
            "deliverables": deliverables, "criteria": config["criteria"],
            "documents": documents, "dir": task_dir}


def list_domains(lab_root):
    root = Path(lab_root) / "tasks"
    return sorted(p.name for p in root.iterdir() if p.is_dir())


def list_tasks(lab_root, domain=None):
    root = Path(lab_root) / "tasks"
    areas = [root / domain] if domain else (p for p in sorted(root.iterdir()) if p.is_dir())
    out = []
    for area in areas:
        for task_dir in sorted(area.iterdir()):
            if (task_dir / "task.json").is_file():
                out.append(f"{area.name}/{task_dir.name}")
    return out


def document_reader(lab_root, lab_python):
    """Return convert(name -> text) bound to one task's documents via closure state."""
    holder = {"documents": {}}

    def bind(task):
        holder["documents"] = task["documents"]

    def convert(name):
        path = holder["documents"].get(name)
        if path is None:
            return f"(unknown document {name})"
        suffix = path.suffix.lower()
        try:
            if suffix in {".md", ".txt", ".csv"}:
                text = path.read_text(encoding="utf-8", errors="replace")
            elif suffix == ".docx":
                text = _pandoc(path)
            else:
                text = _lab_python_text(lab_python, name, path)
        except subprocess.SubprocessError as error:
            return f"(conversion failed: {error})"
        if len(text) > DOC_CAP:
            text = text[:DOC_CAP] + f"\n…(truncated at {DOC_CAP} chars)"
        return text

    return bind, convert


def _pandoc(path):
    result = subprocess.run(["pandoc", "-t", "markdown", "--", str(path)],
                            capture_output=True, text=True, timeout=120, check=True)
    return result.stdout


def _lab_python_text(lab_python, name, path):
    result = subprocess.run([str(lab_python), "-c", _XLSX_PPTX_SRC, name, str(path)],
                            capture_output=True, text=True, timeout=120, check=True)
    return result.stdout


def write_deliverable(run_dir, filename, markdown):
    """Write the markdown source and convert it to the expected .docx via pandoc."""
    run_dir = Path(run_dir)
    (run_dir / "sources").mkdir(parents=True, exist_ok=True)
    (run_dir / "output").mkdir(parents=True, exist_ok=True)
    stem = filename.rsplit(".", 1)[0]
    source = run_dir / "sources" / (stem + ".md")
    source.write_text(markdown, encoding="utf-8")
    target = run_dir / "output" / filename
    subprocess.run(["pandoc", str(source), "-o", str(target)],
                   capture_output=True, text=True, timeout=120, check=True)
    return target


def judge(lab_root, lab_python, run_dir, task_name, judge_model, api_key, base_url):
    """Run harvey-labs' own run_eval scorer; return scores.json fields or None."""
    run_dir = Path(run_dir).resolve()
    scores = run_dir / "scores.json"
    if not scores.is_file():
        env = dict(os.environ)
        env["OPENAI_BASE_URL"] = base_url
        env["OPENAI_API_KEY"] = api_key
        result = subprocess.run(
            [str(lab_python), "-u", "-m", "evaluation.run_eval",
             "--run-id", str(run_dir), "--task", task_name, "--judge-model", judge_model],
            cwd=str(lab_root), env=env, capture_output=True, text=True, timeout=3600)
        (run_dir / "judge.log").write_text(
            result.stdout[-8000:] + "\n--stderr--\n" + result.stderr[-4000:], encoding="utf-8")
        if result.returncode != 0 and not scores.is_file():
            raise RuntimeError(f"judge failed ({result.returncode}); see {run_dir / 'judge.log'}")
    data = json.loads(scores.read_text(encoding="utf-8"))
    return {"n_passed": data.get("n_passed"), "n_criteria": data.get("n_criteria"),
            "all_pass": data.get("all_pass")}


def deliverable_text(run_dir):
    """The extracted text of everything in output/, for improver/contrast context."""
    run_dir = Path(run_dir)
    parts = []
    for path in sorted((run_dir / "output").glob("*.docx")) if (run_dir / "output").is_dir() else []:
        try:
            parts.append(f"----- FILE: {path.name} -----\n{_pandoc(path)}")
        except subprocess.SubprocessError as error:
            parts.append(f"----- FILE: {path.name} -----\n(conversion failed: {error})")
    return "\n\n".join(parts)
