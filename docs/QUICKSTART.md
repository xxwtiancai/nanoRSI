# Your first nanoRSI model experiment

[简体中文](QUICKSTART.zh-CN.md) · [Coding task format](CODING_LAB.md)

This tutorial runs one small Python repair experiment, from API-key setup to a final report. The fixed model edits task code, then proposes changes to reusable Markdown skills. nanoRSI compares those skills on separate tasks; it does not train model weights or guarantee a gain.

## 1. Install

You need **Python 3.11 or newer**, **Git**, and a terminal. These commands use a macOS/Linux shell; replace `python3.11` with your installed Python 3.11+ executable if needed.

```bash
git clone https://github.com/xxwtiancai/nanoRSI.git
cd nanoRSI
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
nanorsi --help
```

Keep the virtual environment active and run the following commands from this repository directory. `nanorsi new` creates a separate experiment workspace and its Git repository; it does not start model calls.

```bash
nanorsi new coding ./coding-lab --goal "Improve reliable Python repair through reusable skills"
```

Expected: a creation message and `coding-lab/nanorsi.toml`, task data, a model adapter, and `target/agent/skills/`.

Generated model/proposer/evaluator commands pin the Python interpreter that creates the workspace. Preserve them when editing TOML. If you move or delete that virtual environment, create a fresh workspace with the intended interpreter (or correct the commands before baseline); `configure` does not rewrite those commands.

## 2. Get API access and choose an endpoint

A browser login to ChatGPT, Claude, or another chat app does **not** configure API credentials for nanoRSI. For a hosted provider, create an API key in that provider's official console, enable API access/billing as required, and choose a model ID available to that account. Keep the key private. For a local server, start a compatible model server separately and use its exact served model ID.

The bundled bridge sends **OpenAI-compatible `/chat/completions` requests**. Set the base URL below, without appending `/chat/completions`. Native Anthropic Messages and OpenAI Responses protocols need a different adapter; changing the URL alone is insufficient.

| Provider | API-key console | `--base-url` | What to use for `--model` |
| --- | --- | --- | --- |
| OpenAI | [API keys](https://platform.openai.com/api-keys) | `https://api.openai.com/v1` | Exact API model ID enabled for your account; use `--token-parameter max_completion_tokens` for models that require it ([API reference](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create)) |
| OpenRouter | [Keys](https://openrouter.ai/settings/keys) | `https://openrouter.ai/api/v1` | Full provider/model slug from its catalog ([quickstart](https://openrouter.ai/docs/quickstart)) |
| DeepSeek | [Platform](https://platform.deepseek.com/) | `https://api.deepseek.com` | A currently available model ID from the [official API guide](https://api-docs.deepseek.com/) |
| Z.AI / GLM | [API keys](https://z.ai/manage-apikey/apikey-list) | `https://api.z.ai/api/paas/v4` (general API), or `https://api.z.ai/api/coding/paas/v4` for an eligible Coding Plan integration | Exact enabled model ID; the published demo used `glm-5.3-flash` with `--thinking disabled`. See [endpoint and integration eligibility](https://docs.z.ai/devpack/tool/others) and [general API](https://docs.z.ai/api-reference/introduction). |
| Local compatible server | No key if your server allows unauthenticated requests | `http://localhost:8000/v1` | The exact model ID served by your running server |

Provider catalogs change. **Replace `YOUR_MODEL_ID` in every command before running it**; it is a placeholder, not an available model. Prefer a fixed snapshot when available. Compatible HTTP syntax alone does not establish that a model follows nanoRSI's JSON action protocol. Automated integration tests use authenticated local HTTP fixtures; they do not establish paid-provider compatibility or model gains.

The [separate live GLM study](../examples/results/v0.4.0/README.md) records the exact requested/returned model and measured outcomes. Endpoint compatibility and subscription eligibility are separate; use the endpoint authorized for your account and integration. nanoRSI does not switch billing endpoints automatically.

## 3. Configure the model and API key

For OpenAI, use this small first-run preset after replacing `YOUR_MODEL_ID`:

```bash
nanorsi configure --workspace ./coding-lab \
  --model YOUR_MODEL_ID --base-url https://api.openai.com/v1 \
  --prompt-key --token-parameter max_completion_tokens \
  --max-steps 1 --max-episodes 40
```

Enter the API key at the hidden terminal prompt. `configure` runs offline. It stores the secret in a unique `~/.config/nanorsi/keys/model-*.key` file **outside the experiment workspace** and writes only its absolute path into `coding-lab/nanorsi.toml`. It also writes model, endpoint, token parameter and budget settings. POSIX permissions restrict the key to its owner. Do not paste a secret into a command, TOML, a skill, an issue, or a Git commit.

For OpenRouter or DeepSeek, substitute the endpoint and exact model ID from the table, and choose the token parameter supported by that model. `max_tokens` is the bridge default; `max_completion_tokens` is available explicitly. The configured token limit defaults to 2048; advanced settings such as `agent.max_tokens`, `max_turns`, and `timeout_s` are editable in the existing TOML before baseline.

Choose **exactly one** authentication option on every `configure` command:

| Option | Behavior |
| --- | --- |
| `--prompt-key` | Hidden interactive input; creates a unique external key file |
| `--api-key-file /absolute/external/path` | Uses an existing key file; does not create or overwrite it |
| `--no-api-key` | Explicitly configures an unauthenticated endpoint, typically local |

For an existing external file (replace both placeholders):

```bash
nanorsi configure --workspace ./coding-lab \
  --model YOUR_MODEL_ID --base-url https://api.openai.com/v1 \
  --api-key-file /absolute/external/path/model.key \
  --token-parameter max_completion_tokens --max-steps 1 --max-episodes 40
```

For a local server:

```bash
nanorsi configure --workspace ./coding-lab \
  --model YOUR_MODEL_ID --base-url http://localhost:8000/v1 \
  --no-api-key --max-steps 1 --max-episodes 40
```

**There is no raw `--api-key` flag. `export OPENAI_API_KEY=...` alone does not configure nanoRSI.** The bundled bridge does not automatically load environment API keys or `.env` files; it reads the explicitly configured external file. This also applies to keys exported for other providers.

<details>
<summary>Manually create a key file with hidden input</summary>

Prefer `--prompt-key`. If you need to prepare a file separately, this Python command reads through `getpass`, creates a unique file outside the workspace, and prints only its path. The secret is never a shell-command literal.

```bash
python - <<'PY'
import getpass
import os
import tempfile
import warnings
from pathlib import Path

with warnings.catch_warnings():
    warnings.simplefilter("error", getpass.GetPassWarning)
    key = getpass.getpass("Model API key: ").strip()
if not key:
    raise SystemExit("API key must not be empty")
directory = Path.home() / ".config" / "nanorsi" / "keys"
directory.mkdir(parents=True, exist_ok=True)
os.chmod(directory, 0o700)
fd, path = tempfile.mkstemp(prefix="model-", suffix=".key", dir=directory)
with os.fdopen(fd, "w", encoding="utf-8") as output:
    output.write(key + "\n")
os.chmod(path, 0o600)
print(path)
PY
```

Pass the printed absolute path to `--api-key-file`. On POSIX, directories use `700` and files `600`. `chmod` does not provide equivalent Windows ACL protection; use your platform's owner-only file permissions. Always keep the key outside the workspace, including when choosing a custom workspace location.

</details>

## 4. Check the connection before starting the experiment

```bash
nanorsi doctor --workspace ./coding-lab
nanorsi doctor --workspace ./coding-lab --check-model
```

Plain `doctor` is offline: it checks local configuration and the configured key file, not provider acceptance. `--check-model` sends exactly one bounded request through your configured model bridge and requires the response content to be the JSON action `{"tool":"final"}`. It does not start a baseline or mutate the experiment lineage. A hosted probe can cost money **outside experiment accounting**. A successful probe proves basic connectivity and action formatting; it does not prove coding ability or that a long run will fit your provider quota.

Resolve any failure before baseline using the table below. You can re-run `configure` while the workspace has not started an experiment. Once its journal has started, configuration is frozen: create a fresh workspace to change the model, endpoint, key path, task data, or budget. An interrupted baseline still counts as started.

## 5. Run the actual improvement loop

```bash
nanorsi baseline --workspace ./coding-lab
nanorsi run --workspace ./coding-lab
nanorsi freeze --workspace ./coding-lab --repeats 1
nanorsi final-test --workspace ./coding-lab
nanorsi report --workspace ./coding-lab --format html
nanorsi verify --workspace ./coding-lab
```

| Stage | What happens / expected evidence |
| --- | --- |
| `baseline` | Runs the initial skills on four validation tasks and records generation 0 |
| `run` | Executes training tasks, asks for a skill patch, compares parent/candidate on validation, records an accepted, rejected, unchanged or failed attempt |
| `freeze --repeats 1` | Fixes the selected version and final comparison panel; search cannot continue |
| `final-test` | Evaluates initial skills, no skills and selected skills on the four unseen tasks, once per condition |
| `report --format html` | Writes `coding-lab/reports/report.html` and supporting report data |
| `verify` | Checks lineage integrity; successful output includes `lineage: ok` |

Open `coding-lab/reports/report.html` in your browser. A rejected patch or a lower final score is a valid experimental result, not proof that the installation failed. Check the report for failed episodes and missing costs before interpreting scores.

### What improves, and what is recursive?

Within each episode the model repairs a fresh task's `solution.py` using `list`, `read`, `write`, `test`, and `final`. Those task-code edits are episode outputs. Across attempts, the proposer edits **persistent procedural Markdown files under `target/agent/skills/**`**. A patch might teach the agent to inspect edge cases before editing and verify behavior afterward. The model weights, evaluator, tasks and model configuration stay fixed.

Training feedback informs proposals. Validation controls acceptance. Final-test feedback does not select candidates. A candidate must satisfy the configured gate; an attempt can fail or make no change. Inspect recorded candidate commits and patches to see what changed—do not infer evolution merely because `run` finished.

The default `experiment.arm = "frozen"` uses the initial skills to propose every patch. For recursive reuse, create another fresh workspace and set `experiment.arm = "self-use"` in its TOML **before baseline**: its latest accepted skills help propose the next patch. Both arms modify the current parent. Match model, task data, inference settings and budgets; freeze both before viewing final results. Repeat independent evolution runs before claiming a recursive benefit. No weight training occurs in either arm.

## Choose a budget before running

An **episode** is one execution of one task in a fresh directory, potentially using several model calls. A **proposal attempt** is one try at changing reusable skills.

The commands above set **one proposal attempt** and a **40-episode search cap**. For this 12-task coding pack, a completed attempt uses at most **16 search episodes**: 4 baseline + 4 training + 4 parent validation + 4 candidate validation. The one-repeat final panel adds **12 episodes outside the search cap**, giving up to **28 task episodes**. At eight model calls per episode that is up to 224 episode calls, plus one proposal call and any separate doctor probes. Failed or no-op proposals can use fewer episodes, but still consume the attempt.

The unmodified coding template permits three attempts and a 100-episode cap; a full search uses up to 40 episodes and the same final panel adds 12. The `skills` text-edit template is larger: 30 tasks per split, five attempts, a 400-episode cap, up to 350 search episodes, and 270 final episodes at three repeats. For a first hosted run, use the coding preset above.

Episode and token limits are **not a dollar spending cap**. Final tests and connectivity probes are additional; proposal calls are recorded separately. Unknown cost means unknown, not zero. Review provider pricing and quota before running. Configure budgets before baseline; changing a started experiment requires a fresh workspace.

## Troubleshooting

| Symptom | Next action |
| --- | --- |
| `nanorsi: command not found` | Activate `.venv` and repeat `python -m pip install -e .` from the repository |
| Missing key / unreadable file | Use `--prompt-key`, or check the existing absolute external file path and owner permissions |
| HTTP 401 | Check that the API key is valid for this endpoint; browser login is not an API key |
| HTTP 403 | Check account/project/model access and provider policy |
| HTTP 404 | Check base URL and exact model ID; omit `/chat/completions` from `--base-url` |
| HTTP 429 | Check quota/billing and rate limits; reduce workload or retry manually later |
| HTTP 400 / 422 | Check provider request requirements, model ID and `--token-parameter max_tokens` versus `max_completion_tokens` |
| HTTP 5xx | Check provider status and retry manually later |
| Network, DNS or TLS error | Check connectivity, certificates and endpoint; do not disable TLS verification |
| Redirect rejected | Verify the final trusted provider URL and reconfigure with that URL before baseline |
| Invalid JSON / action response | The model must emit the required JSON action; check model suitability and token limit, or supply a compatible adapter before baseline |
| Configuration frozen / journal started | Create a new workspace and configure it; do not edit recorded experiment settings |

For an interrupted run, `nanorsi recover --workspace ./coding-lab` reconciles stale local attempt/worktree state. It does not unfreeze settings or guarantee that a failed final panel can be retried. Completed final panels are idempotent; incomplete panels remain explicit failures.

## Inspect and reuse the evidence

| Location | Contents |
| --- | --- |
| `reports/report.html` / `reports/report.md` | Human-readable comparisons, decisions and cost coverage |
| `reports/report.json` | Search journal export |
| `reports/final.json` | Frozen conditions, scores and search/test cost evidence |
| `lineage.jsonl` | Sequenced receipts and parent/candidate identities |
| `.nanorsi/runs/` | Per-attempt context, proposals, traces and evaluations |

From the repository, run `python examples/compare.py ./coding-lab/reports/final.json` for the comparison summary. Accepted skills are identified by their recorded candidate commit and `nanorsi/gen-N` tag; the report lets you inspect the version actually evaluated.

No API access yet? `python examples/coding_tasks/prepare.py --check` validates the broken starters and reference solutions offline. The `artifact` and `harness` templates are scripted offline demos; their scores demonstrate protocol behavior, not learned gains. Their historical heldout split participates in selection; v2 workspaces have a separate final-test phase.

Default execution is trusted local subprocess execution. Worktrees and receipts do not hide labels or keys from arbitrary same-user code. Use an external container/VM/service for untrusted programs and private-label evaluation; see [SECURITY.md](../SECURITY.md).
