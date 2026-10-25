# LAB + OpenCode adapter for nanoRSI

Runs the Harness² paper's LAB benchmark (harveyai/harvey-labs, MIT) through the
paper's executor substrate (OpenCode) from the nanoRSI v0.5 loop, using nothing but
the core's two command protocols:

- `runner.py` — `NANORSI_REQUEST` → stages the nano harness in the layout LAB's own
  `opencode/run_opencode.py --harness-dir` expects (the entry point the harness2 code
  itself calls), runs one OpenCode rollout, renders the session stream into a
  trajectory, text-extracts deliverables for the contrast step and keeps the binary
  deliverables under `<run_dir>/output` → `NANORSI_RESULT`.
- `judge.py` — `NANORSI_JUDGE_REQUEST` → LAB's `evaluation.run_eval` per-criterion
  rubric judge on `<run_dir>/output` → `NANORSI_JUDGE_RESULT`.
- `prepare.py` — writes a workspace: `nanorsi.toml` (command runner + judge, model,
  budget), `lab_opencode.json` (checkout paths, executor model, judge model, isolated
  OpenCode config dir, GNU-timeout shim), `tasks/manifest.json` from LAB `task.json`
  files, and the base harness = LAB's own system prompt with empty guardrails /
  memory / tool guidance — the same starting point the harness2 code uses.

Prerequisites are the ones recorded for the faithful harness2 run: a harness2 checkout
with `harness2-setup lab` done (OpenCode source + bun + harvey-labs venv), the OpenCode
provider file in an isolated `XDG_CONFIG_HOME`, the `custom/` judge provider patch,
`coreutils` (`gtimeout` as `timeout` on PATH), and the API key file outside the
workspace. See `examples/results/harness2-lab-opencode/setup/`.

```bash
python examples/lab_opencode/prepare.py ./lab-ws --tasks <id>,<id>,...
nanorsi doctor --workspace ./lab-ws --check-model
nanorsi evolve --workspace ./lab-ws
nanorsi freeze --workspace ./lab-ws && nanorsi judge --workspace ./lab-ws
nanorsi report --workspace ./lab-ws
```
