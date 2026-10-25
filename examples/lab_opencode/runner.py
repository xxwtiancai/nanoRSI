"""nanoRSI runner protocol -> LAB's own OpenCode runner (harveyai/harvey-labs, MIT).

Reads NANORSI_REQUEST, maps the nano harness layout onto the layout LAB's
`opencode/run_opencode.py --harness-dir` expects (the same entry point the
harness2 code uses), runs one OpenCode rollout, and writes NANORSI_RESULT with
the rendered trajectory, text-extracted deliverables and token usage. Binary
deliverables are kept under <run_dir>/output for the judge.

Settings come from lab_opencode.json next to nanorsi.toml (written by prepare.py)."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LAYOUT = {  # nano component -> harness2/LAB tree path
    "systemprompt.md": "systemprompt.md",
    "guardrails.md": "guardrails.md",
    "memory.md": "LongTermMEMORY.md",
    "tool_guidance.md": "tool_descriptions/tool_guidance.md",
}
STUBS = {
    "scripts/README.md": "<!-- c7: deterministic helpers, run as `python3 scripts/<name>.py`. -->\n",
    "sub_agents/README.md": "<!-- c5: delegated subagents (unused by nanoRSI). -->\n",
    "plugin/README.md": "<!-- c8: OpenCode plugins (unused by nanoRSI). -->\n",
    "skills/README.md": "<!-- c6: reusable workflows loaded on demand. -->\n",
}


def settings(workspace: Path) -> dict:
    return json.loads((workspace / "lab_opencode.json").read_text(encoding="utf-8"))


def lab_env(cfg: dict) -> dict:
    env = dict(os.environ)
    lab_python = Path(cfg["lab_python"])
    env["PYTHONPATH"] = cfg["lab_root"]
    env["PATH"] = f"{lab_python.parent}:{Path(cfg['bun']).parent}:{cfg.get('shim_bin', '')}:" + env.get("PATH", "")
    env["XDG_CONFIG_HOME"] = cfg["xdg_config_home"]
    return env


def stage_harness(nano_dir: Path, staged: Path) -> None:
    """Write the nano harness as the tree LAB's renderer reads."""
    staged.mkdir(parents=True, exist_ok=True)
    for name, target in LAYOUT.items():
        src = nano_dir / name
        out = staged / target
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(src.read_text(encoding="utf-8") if src.is_file() else "", encoding="utf-8")
    for sub in ("skills", "scripts"):
        if (nano_dir / sub).is_dir():
            shutil.copytree(nano_dir / sub, staged / sub, dirs_exist_ok=True)
    for rel, body in STUBS.items():
        path = staged / rel
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")


def render_trajectory(stream: Path, limit: int = 60000) -> str:
    lines = []
    for raw in stream.read_text(encoding="utf-8", errors="replace").splitlines() if stream.is_file() else []:
        raw = raw.strip()
        if not raw.startswith("{"):
            continue
        try:
            event = json.loads(raw)
        except ValueError:
            continue
        part = event.get("part") if isinstance(event.get("part"), dict) else event
        kind = part.get("type", event.get("type"))
        if kind == "text" and part.get("text", "").strip():
            lines.append("[ASSISTANT] " + part["text"][:1500])
        elif kind in ("tool", "tool_use", "tool_call", "tool-invocation"):
            state = part.get("state") if isinstance(part.get("state"), dict) else part
            name = part.get("tool") or event.get("tool") or part.get("name") or "tool"
            args = json.dumps(state.get("input") or part.get("input") or {}, ensure_ascii=False)[:300]
            lines.append(f"[ACTION] {name}({args})")
            out = state.get("output") or state.get("error")
            if out:
                lines.append("[OBSERVATION] " + str(out)[:600])
        elif isinstance(event.get("error"), dict):
            lines.append("[ERROR] " + json.dumps(event["error"])[:300])
    text = "\n".join(lines)
    return text if len(text) <= limit else text[:limit] + f"\n…(truncated {len(text) - limit} chars)"


def usage_from_stream(stream: Path) -> dict:
    calls = tokens_in = tokens_out = 0
    for raw in stream.read_text(encoding="utf-8", errors="replace").splitlines() if stream.is_file() else []:
        if '"step_finish"' not in raw and '"step-finish"' not in raw:
            continue
        try:
            tokens = json.loads(raw).get("part", {}).get("tokens", {})
        except ValueError:
            continue
        calls += 1
        tokens_in += int(tokens.get("input") or 0) + int((tokens.get("cache") or {}).get("read") or 0)
        tokens_out += int(tokens.get("output") or 0) + int(tokens.get("reasoning") or 0)
    return {"calls": calls, "input_tokens": tokens_in, "output_tokens": tokens_out}


def extract_text(path: Path) -> str:
    if path.suffix.lower() in {".docx", ".pptx", ".xlsx", ".pdf"}:
        try:
            return subprocess.run(["pandoc", "-t", "markdown", "--wrap=none", str(path)], capture_output=True,
                                  text=True, timeout=120, check=True).stdout
        except (subprocess.SubprocessError, OSError) as error:
            return f"(could not extract {path.name}: {error})"
    return path.read_text(encoding="utf-8", errors="replace")


def main() -> int:
    request = json.loads(Path(os.environ["NANORSI_REQUEST"]).read_text(encoding="utf-8"))
    workspace = Path.cwd()
    cfg = settings(workspace)
    run_dir = Path(request["output_dir"])
    task_id = request["task"]["task_id"]
    staged = Path(tempfile.mkdtemp(prefix="nanorsi-harness-"))
    stage_harness(Path(request["harness_dir"]), staged)
    results_root = run_dir / "lab"
    run_id = f"nanorsi/{request['label']}"
    cmd = [cfg["lab_python"], "-u", str(Path(cfg["lab_root"]) / "opencode" / "run_opencode.py"),
           "--task", task_id, "--run-id", run_id, "--results-root", str(results_root), "--model", cfg["model"],
           "--tool-mode", "base", "--reasoning-effort", "high", "--skill-mode", "native",
           "--timeout", str(cfg.get("rollout_timeout_s", 3600)), "--opencode-dir", cfg["opencode_dir"],
           "--bun", cfg["bun"], "--harness-dir", str(staged)]
    proc = subprocess.run(cmd, cwd=cfg["lab_root"], env=lab_env(cfg), capture_output=True, text=True,
                          timeout=int(cfg.get("rollout_timeout_s", 3600)) + 900)
    (run_dir / "run_opencode.log").write_text(proc.stdout[-30000:] + "\n--stderr--\n" + proc.stderr[-10000:], encoding="utf-8")
    lab_run = results_root / run_id
    stream = lab_run / "opencode_session.jsonl"
    output = lab_run / "workspace" / "output"
    deliverables = {}
    if output.is_dir():
        kept = run_dir / "output"
        shutil.copytree(output, kept, dirs_exist_ok=True)
        for path in sorted(p for p in output.rglob("*") if p.is_file()):
            deliverables[path.relative_to(output).as_posix()] = extract_text(path)
    shutil.rmtree(staged, ignore_errors=True)
    result = {"ok": proc.returncode == 0 and bool(deliverables), "delivered": bool(deliverables),
              "trajectory": render_trajectory(stream), "deliverables": deliverables,
              "usage": usage_from_stream(stream),
              "error": "" if deliverables else f"run_opencode exit {proc.returncode}, no deliverable"}
    Path(os.environ["NANORSI_RESULT"]).write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
