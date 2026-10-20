"""Build the deterministic ALFWorld agent-task pack (benchmark track, phase 2).

ADOPTION item 37 phase 2: real agent tasks. Games come from the ALFWorld text
environment (MIT; games generated with alfworld-download from ALFRED data, see
NOTICE). Each task is one TextWorld-PDDL game played by the nanoRSI skills
agent; success is the engine's own ``won`` flag. The mutable surface is the
skills directory (guidance evolves across episodes); the game runner, evaluator
and adapters are authored here and frozen at baseline. Game selection is
deterministic (sorted game paths, strided subsample); the manifest is always
regenerated and must never be hand-edited.

Requirements: ALFWorld data at ~/.cache/alfworld/json_2.1.1 (alfworld-download)
and a Python 3.12 interpreter with alfworld installed (textworld textgen breaks
on Python 3.13 under PEP 667). The runner re-execs itself under NANORSI_ALF_PYTHON.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

CACHE = Path.home() / ".cache/alfworld/json_2.1.1"
TRAIN_COUNT, VALIDATION_COUNT, TEST_PER_SPLIT = 4, 6, 6
GAME_STEPS = 24
ALF_PYTHON = "/opt/miniconda3/envs/alf312/bin/python"

RUNNER = r'''# ALFWorld task pack for nanoRSI (benchmark track, phase 2).
# Games: ALFWorld/TextWorld engine (MIT, Copyright the ALFWorld authors); see NOTICE.
# Runner authored by nanoRSI. It re-execs under the ALFWorld interpreter, loads the
# configured skills, plays the game with the workspace model bridge and reports won.
import json
import os
import sys

_ALF_PYTHON = os.environ.get("NANORSI_ALF_PYTHON", "__ALF_PYTHON__")
if (sys.version_info[:2] != (3, 12) and os.environ.get("NANORSI_ALF_REEXEC") != "1"
        and os.path.isfile(_ALF_PYTHON)):
    # Re-exec only when the ALFWorld interpreter exists; propose mode runs fine
    # without it, and a missing interpreter surfaces as a task-mode import error.
    os.environ["NANORSI_ALF_REEXEC"] = "1"
    os.execv(_ALF_PYTHON, [_ALF_PYTHON, sys.argv[0]] + sys.argv[1:])

import hashlib
import fnmatch
import difflib
import signal
import subprocess
import time
from pathlib import Path

MAX_STEPS = __GAME_STEPS__
WALL_LIMIT_S = 880.0
MAX_BRIDGE_OUTPUT_BYTES = 1_000_000


class RunnerError(Exception):
    pass


class _Usage:
    def __init__(self):
        self.calls, self.errors = 0, []
        self.values = {"input_tokens": 0, "output_tokens": 0}

    def record_call(self, usage, error=None):
        self.calls += 1
        if isinstance(usage, dict):
            for key in self.values:
                value = usage.get(key)
                if isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0:
                    self.values[key] += value
        if error:
            self.errors.append(error)

    def as_dict(self):
        return {"model_calls": self.calls, "input_tokens": self.values["input_tokens"] or None,
                "output_tokens": self.values["output_tokens"] or None, "cost_usd": None,
                "errors": list(self.errors)}


def _safe_environment():
    keep = {k: v for k, v in os.environ.items() if not k.startswith("NANORSI_")}
    keep["NANORSI_ALF_REEXEC"] = "1"
    return keep


def _call_bridge(agent, payload, timeout_value, usage):
    for attempt in (1, 2):
        envelope, error = _bridge_once(agent, payload, timeout_value, usage)
        if error is not None:
            return None, error
        content = envelope["content"]
        usage.record_call(envelope.get("usage"))
        stripped = content.strip()
        if stripped.startswith("```") and stripped.endswith("```") and stripped.count("```") == 2:
            first_newline = stripped.find("\n")
            if first_newline != -1:
                stripped = stripped[first_newline + 1:-3].strip("\n")
        try:
            action = json.loads(stripped)
            if len(content.encode("utf-8")) > 20000:
                raise ValueError
            return action, None
        except (TypeError, ValueError, json.JSONDecodeError):
            if attempt == 2:
                usage.errors.append("invalid_action")
                return None, "model returned invalid action JSON"
            usage.errors.append("invalid_action_retry")


def _bridge_once(agent, payload, timeout_value, usage):
    command = agent["model_command"]
    cwd = Path(__file__).resolve().parents[2]
    try:
        process = subprocess.Popen(command, cwd=cwd, env=_safe_environment(),
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, start_new_session=(os.name == "posix"))
    except OSError:
        usage.record_call(None, "model_start_error")
        return None, "model bridge could not start"
    try:
        stdout, _ = process.communicate(json.dumps(payload).encode("utf-8"), timeout=timeout_value)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except (OSError, ProcessLookupError):
            pass
        process.wait()
        usage.record_call(None, "model_timeout")
        return None, "model bridge timed out"
    if process.returncode != 0 or len(stdout) > MAX_BRIDGE_OUTPUT_BYTES:
        usage.record_call(None, "model_exit_error")
        return None, "model bridge failed"
    try:
        envelope = json.loads(stdout.decode("utf-8"))
    except (TypeError, UnicodeError, json.JSONDecodeError):
        usage.record_call(None, "model_invalid_json")
        return None, "model bridge returned invalid JSON"
    if not isinstance(envelope, dict) or not isinstance(envelope.get("content"), str):
        usage.record_call(envelope if isinstance(envelope, dict) else None, "model_missing_content")
        return None, "model bridge response has no content"
    if isinstance(envelope.get("error_code"), str):
        usage.record_call(envelope.get("usage"), "model_" + envelope["error_code"])
        return None, "model_" + envelope["error_code"]
    return envelope, None


def _load_skills(names):
    hashes, fragments = {}, []
    skill_root = Path(__file__).resolve().parent / "skills"
    for name in names or []:
        if not isinstance(name, str) or "/" in name or name in {".", ".."}:
            raise RunnerError("invalid skill name")
        path = skill_root / name / "SKILL.md"
        if not path.is_file() or path.is_symlink() or (skill_root / name).is_symlink():
            raise RunnerError("skill not found: " + name)
        data = path.read_bytes()
        hashes[name] = hashlib.sha256(data).hexdigest()
        fragments.append("\n--- skill:" + name + " sha256:" + hashes[name] + " ---\n"
                         + data.decode("utf-8"))
    return hashes, "\n".join(fragments)


SYSTEM_PROMPT = (
    "You are an agent in a household simulator. You act strictly one step at a time.\n"
    "Reply with a single JSON object: {\"action\": \"<one command>\"} or "
    "{\"think\": \"<one short sentence>\"} before an action.\n"
    "The observation lists admissible commands; pick from them when possible.\n"
    "Common verbs: go to X, look, examine X, take X from Y, put X in/on Y, open X, "
    "close X, heat X, cool X, clean X, use X.\n"
    "Complete the task stated in the observation, then reply {\"action\": \"stop\"}."
)


def _run_task(request, agent, hashes, skill_text):
    import textworld.gym
    from alfworld.agents.environment.alfred_tw_env import AlfredDemangler, AlfredInfos

    usage = _Usage()
    trace = [{"event": "runner_loaded", "path": "target/agent/run.py",
              "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}]
    task = request["task"]
    game = json.loads(task["input_files"]["game.json"])
    won, steps, transcript = False, 0, []
    env_id = textworld.gym.register_games(
        [game["game_file"]],
        textworld.EnvInfos(won=True, admissible_commands=True),
        batch_size=1, asynchronous=True, max_episode_steps=MAX_STEPS + 1,
        wrappers=[AlfredDemangler(), AlfredInfos])
    env = textworld.gym.make(env_id)
    started = time.monotonic()
    try:
        observation, infos = env.reset()
        observation = observation[0] if isinstance(observation, (list, tuple)) else observation
        messages = [{"role": "system", "content": SYSTEM_PROMPT + skill_text}]
        content = ""
        for step in range(MAX_STEPS):
            commands = sorted(infos.get("admissible_commands", [[]])[0])
            numbered = "\n".join(str(i + 1) + ". " + c for i, c in enumerate(commands[:60]))
            messages.append({"role": "user", "content":
                "Observation:\n" + observation[-1600:] + "\n\nAdmissible commands:\n"
                + numbered + "\n\nReply with one JSON object."})
            payload = {"messages": messages, "model": agent.get("model"),
                       "max_tokens": agent.get("max_tokens")}
            for key in ("base_url", "api_key_file", "timeout_s", "token_parameter", "thinking"):
                if key in agent:
                    payload[key] = agent[key]
            envelope, error = _call_bridge(agent, payload, float(agent.get("timeout_s", 60)), usage)
            if error is not None:
                trace.append({"event": "model_error", "code": error, "step": step})
                break
            action = envelope
            try:
                if not isinstance(action, dict) or not isinstance(action.get("action"), str):
                    raise ValueError
                command = action["action"].strip()
            except (TypeError, ValueError, json.JSONDecodeError):
                trace.append({"event": "invalid_action", "step": step})
                messages.append({"role": "assistant", "content": json.dumps(action)[:400]})
                messages.append({"role": "user", "content":
                    "Invalid reply. Respond with one JSON object like {\"action\": \"go to shelf 1\"}."})
                continue
            trace.append({"event": "action", "step": step, "command": command[:120]})
            transcript.append(command)
            messages.append({"role": "assistant", "content": json.dumps(action)})
            if command == "stop":
                break
            observation, _scores, _dones, infos = env.step([command])
            observation = observation[0] if isinstance(observation, (list, tuple)) else observation
            steps = step + 1
            won = bool(infos.get("won", [False])[0])
            if won:
                break
            if time.monotonic() - started > WALL_LIMIT_S:
                trace.append({"event": "wall_limit", "step": step})
                break
    finally:
        env.close()
    trace.append({"event": "episode_end", "won": won, "steps": steps})
    report = json.dumps({"won": won, "steps": steps, "goal": game.get("goal", ""),
                         "actions": transcript[:MAX_STEPS]})
    return {"status": "ok", "won": won, "steps": steps,
            "output_files": {"game-report.json": report},
            "trace": trace[:60], "skill_hashes": hashes, "usage": usage.as_dict(),
            "duration_ms": max(0, int((time.monotonic() - started) * 1000))}


PROPOSAL_PROMPT = (
    "You are a bounded proposal agent for an ALFWorld skill-evolution experiment. "
    "Return exactly one JSON object with no markdown. Prefer "
    '{"files":{"target/agent/skills/<name>/SKILL.md":"complete new file text"},'
    '"hypothesis":{"reason":"why this guidance should improve unseen episodes"}}. '
    "Include only changed or new files with complete content; the driver computes the "
    'git diff. Alternatively return {"diff":"valid git unified diff","hypothesis":{...}}. '
    "Do not return both. Modify only the allowed skill files. Use the episode feedback "
    "(failed goals, wasted actions, model errors) to write general reusable guidance; "
    "do not embed game paths, task IDs or data-specific shortcuts. "
    'If no justified improvement remains, return {"files":{},"hypothesis":{"reason":"..."}}.\n'
)


def _replacement_diff(files, context):
    if not isinstance(files, dict) or len(files) > 64:
        raise RunnerError("proposal files must be an object with at most 64 paths")
    parents = context.get("parent_files", {})
    if not isinstance(parents, dict):
        raise RunnerError("proposal parent_files must be an object")
    surface = context.get("surface")
    allow = surface.get("allow", []) if isinstance(surface, dict) else ["target/agent/skills/**"]
    deny = surface.get("deny", []) if isinstance(surface, dict) else []
    output = []
    for path, source in sorted(files.items()):
        if not isinstance(path, str) or not path.startswith("target/") or "\\" in path:
            raise RunnerError("invalid proposal file path")
        if any(part in {"", ".", ".."} for part in path.split("/")):
            raise RunnerError("invalid proposal file path")
        if any(not isinstance(pattern, str) or not fnmatch.fnmatch(path, pattern) for pattern in allow) \
                or any(isinstance(pattern, str) and fnmatch.fnmatch(path, pattern) for pattern in deny):
            raise RunnerError("proposal file outside mutable surface")
        if not isinstance(source, str) or "\x00" in source:
            raise RunnerError("proposal file contents must be text")
        old = parents.get(path, "")
        if not isinstance(old, str):
            raise RunnerError("proposal parent file contents must be text")
        if path in parents and old == source:
            continue
        left, right = "a/" + path, "b/" + path
        output.append("diff --git " + left + " " + right + "\n")
        if path not in parents:
            output.append("new file mode 100644\n")
            if not source:
                output.append("index 0000000..0000000\n")
                continue
        lines = difflib.unified_diff(old.splitlines(keepends=True),
                                     source.splitlines(keepends=True),
                                     fromfile="/dev/null" if path not in parents else left,
                                     tofile=right)
        for line in lines:
            output.append(line if line.endswith("\n") else line + "\n\\ No newline at end of file\n")
    return "".join(output)


def _run_propose(request, agent, hashes, skill_text, trace, usage):
    context = request.get("context")
    if not isinstance(context, dict):
        raise RunnerError("invalid proposal context")
    visible = {key: context.get(key) for key in
               ("goal", "parent_files", "train_results", "surface", "rejected_recent")}
    messages = [{"role": "system", "content": PROPOSAL_PROMPT + skill_text},
                {"role": "user", "content": json.dumps(visible, ensure_ascii=False)}]
    payload = {"messages": messages, "model": agent.get("model"), "max_tokens": agent.get("max_tokens")}
    for key in ("base_url", "api_key_file", "timeout_s", "token_parameter", "thinking"):
        if key in agent:
            payload[key] = agent[key]
    result, error = _call_bridge(agent, payload, float(agent.get("timeout_s", 60)), usage)
    trace.append({"event": "model_call", "turn": 1, "ok": error is None})
    if error is not None:
        return {"status": "error", "trace": trace[:60], "skill_hashes": hashes,
                "usage": usage.as_dict()}
    if not isinstance(result, dict) or not isinstance(result.get("hypothesis"), dict) \
            or ("files" in result) == ("diff" in result):
        trace.append({"event": "error", "code": "invalid_proposal"})
        return {"status": "error", "trace": trace[:60], "skill_hashes": hashes,
                "usage": usage.as_dict()}
    if "files" in result:
        result["diff"] = _replacement_diff(result["files"], context)
    elif not isinstance(result["diff"], str):
        raise RunnerError("proposal diff must be text")
    trace.append({"event": "proposal"})
    return {"status": "ok", "diff": result["diff"], "hypothesis": result["hypothesis"],
            "trace": trace[:60], "skill_hashes": hashes, "usage": usage.as_dict()}


def main():
    started = time.monotonic()
    hashes = {}
    result = {"status": "error", "trace": [], "skill_hashes": {},
              "usage": _Usage().as_dict()}
    try:
        request = json.loads(sys.stdin.read())
        mode = request.get("mode")
        if mode not in {"task", "propose"}:
            raise RunnerError("mode must be task or propose")
        agent = request.get("agent", {})
        hashes, skill_text = _load_skills(agent.get("skills"))
        trace = [{"event": "runner_loaded", "path": "target/agent/run.py",
                  "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}]
        if mode == "task":
            result = _run_task(request, agent, hashes, skill_text)
        else:
            result = _run_propose(request, agent, hashes, skill_text, trace, _Usage())
    except (OSError, UnicodeError, RunnerError, json.JSONDecodeError, KeyError,
            TypeError, ValueError) as error:
        result["trace"] = list(result.get("trace", [])) + [{"event": "error",
                                                            "code": str(error)[:120]}]
    result["duration_ms"] = max(0, int((time.monotonic() - started) * 1000))
    print(json.dumps(result))


if __name__ == "__main__":
    main()
'''

EVALUATOR_GRADE = '''def _grade(task, runner_result):
    if runner_result.get("status") != "ok":
        codes = {str(item.get("code", "")) for item in runner_result.get("trace", [])
                 if isinstance(item, dict)}
        if any("timeout" in code for code in codes):
            return 0.0, "timeout"
        return 0.0, "runner_error"
    return (1.0, "ok") if runner_result.get("won") else (0.0, "task_failure")


def _training_feedback(task, runner_result):
    report = runner_result.get("output_files", {}).get("game-report.json")
    try:
        parsed = json.loads(report) if isinstance(report, str) else {}
    except ValueError:
        parsed = {}
    return {"won": bool(runner_result.get("won")), "steps": runner_result.get("steps"),
            "goal": parsed.get("goal", ""), "actions": parsed.get("actions", [])[:24],
            "model_errors": (runner_result.get("usage") or {}).get("errors", [])[:6]}
'''

INITIAL_SKILL = '''# ALFWorld operating skill (initial version)

You are completing household tasks in a text simulator. Reusable guidance may
be added to this file; it is loaded before every episode.

Current guidance (v0):

- Read the task sentence in the observation first; it names the object and the
  destination (for example a ladle on a countertop).
- Explore receptacles one at a time with go to and examine until you find the
  named object.
- Manipulation verbs have fixed effects: take moves an object into your
  inventory; put places it; heat needs the microwave; cool needs the fridge;
  clean needs the sinkbasin; use turns a lamp on while holding nothing else.
- The observation lists admissible commands; prefer exact strings from it.
- When the stated task is complete, reply {"action": "stop"}.
'''


def _sample(games: list[Path], count: int, residue: int) -> list[Path]:
    stride = max(2, len(games) // max(1, count))
    picked = [game for index, game in enumerate(games) if index % stride == residue]
    return picked[:count]


def _games(split: str) -> list[Path]:
    directory = CACHE / split
    games = sorted(path for path in directory.rglob("game.tw-pddl")
                   if "movable" not in str(path) and "Sliced" not in str(path))
    if not games:
        raise SystemExit(f"no games found under {directory}; run alfworld-download first")
    return games


def _game_task(game: Path, split: str, index: int, group: str) -> dict:
    record = json.dumps({"game_file": str(game), "goal": game.parent.parent.name,
                         "max_steps": GAME_STEPS}, ensure_ascii=False)
    return {"task_id": f"{split}-{index:03d}", "group_id": group, "split": split,
            "instruction": "Play the game described in game.json to completion.",
            "input_files": {"game.json": record},
            "expected_files": {"game-report.json": ""}}


def _validation_tasks(count: int, test_per_split: int) -> list[dict]:
    """Validation drawn from the SAME distribution as the frozen test panels.

    The 2026-10-20 gate-ability diagnostic showed train-split validation games
    can carry no signal for edits whose value lives on seen/unseen layouts, so
    validation now samples the valid_seen / valid_unseen pools (evenly split,
    never overlapping the test picks) while train keeps the train split.
    """
    half = (count + 1) // 2
    tasks, index = [], 0
    for split, group, size in (("valid_seen", "validation-seen", half),
                               ("valid_unseen", "validation-unseen", count - half)):
        games = _games(split)
        test_set = set(_sample(games, test_per_split, 0))
        remaining = [game for game in games if game not in test_set]
        stride = max(1, len(remaining) // max(1, size))
        for game in remaining[::stride][:size]:
            tasks.append(_game_task(game, "validation", index, group))
            index += 1
    return tasks


def build_manifest(train_count: int = TRAIN_COUNT, validation_count: int = VALIDATION_COUNT,
                   test_per_split: int = TEST_PER_SPLIT) -> dict:
    """Deterministic game selection; defaults are pinned by tests and studies.

    The test split selection depends only on test_per_split (stride over the
    sorted valid_seen / valid_seen games), so validation-size changes keep
    the frozen test panels comparable across studies.
    """
    train_games = _games("train")
    tasks = ([_game_task(game, "train", i, "train-games")
              for i, game in enumerate(_sample(train_games, train_count, 0))]
             + _validation_tasks(validation_count, test_per_split)
             + [_game_task(game, "test", i, "test-seen")
                for i, game in enumerate(_sample(_games("valid_seen"), test_per_split, 0))]
             + [_game_task(game, "test", test_per_split + i, "test-unseen")
                for i, game in enumerate(_sample(_games("valid_unseen"), test_per_split, 0))])
    return {"schema_version": 1, "tasks": tasks}


def write_pack(output: Path, with_manifest: bool = True, train_count: int = TRAIN_COUNT,
               validation_count: int = VALIDATION_COUNT,
               test_per_split: int = TEST_PER_SPLIT) -> list[Path]:
    directory = output / "alfworld"
    (directory / "target" / "agent" / "skills" / "alfworld").mkdir(parents=True, exist_ok=True)
    paths = []
    if with_manifest:
        manifest_path = directory / "manifest.json"
        manifest_path.write_text(json.dumps(
            build_manifest(train_count, validation_count, test_per_split),
            indent=1, ensure_ascii=False) + "\n")
        paths.append(manifest_path)
    runner_path = directory / "target" / "agent" / "run.py"
    runner_path.write_text(RUNNER.replace("__ALF_PYTHON__", ALF_PYTHON)
                           .replace("__GAME_STEPS__", str(GAME_STEPS)))
    skill_path = directory / "target" / "agent" / "skills" / "alfworld" / "SKILL.md"
    skill_path.write_text(INITIAL_SKILL)
    template = (Path(__file__).resolve().parents[2]
                / "src/nanorsi/templates/skills/evaluator/evaluate.py").read_text()
    evaluator = template[:template.index("def _grade(")] + EVALUATOR_GRADE + template[template.index("def evaluate("):]
    evaluator_path = directory / "evaluator" / "evaluate.py"
    evaluator_path.parent.mkdir(parents=True, exist_ok=True)
    evaluator_path.write_text(evaluator)
    return paths + [runner_path, skill_path, evaluator_path]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write the deterministic ALFWorld task pack.")
    parser.add_argument("output", nargs="?", default=Path(__file__).with_name("out"))
    parser.add_argument("--train", type=int, default=TRAIN_COUNT,
                        help="train games (default 4; record non-default values in the study)")
    parser.add_argument("--validation", type=int, default=VALIDATION_COUNT,
                        help="validation games (default 6)")
    parser.add_argument("--test-per-split", type=int, default=TEST_PER_SPLIT,
                        help="test games per seen/unseen split (default 6)")
    args = parser.parse_args(argv)
    for path in write_pack(Path(args.output), train_count=args.train,
                           validation_count=args.validation, test_per_split=args.test_per_split):
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
