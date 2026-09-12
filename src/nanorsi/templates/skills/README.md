# Skills experiment

This workspace evolves persistent Markdown skills with a fixed model. Per-task file edits are episode outputs; only `target/agent/skills/**` changes across proposals. Model weights are not trained. The manifest has 90 local text-edit protocol fixtures, not a public benchmark.

## Configure and run

Use the [first-run tutorial](https://github.com/xxwtiancai/nanoRSI/blob/main/docs/QUICKSTART.md) ([中文](https://github.com/xxwtiancai/nanoRSI/blob/main/docs/QUICKSTART.zh-CN.md)) for installation, provider endpoints, key creation and troubleshooting. The smaller `coding` template is preferable for a first hosted run. To use this workspace, replace `YOUR_MODEL_ID` with an exact API model ID available to your account, obtain a key from the [OpenAI console](https://platform.openai.com/api-keys), then run from here:

```bash
nanorsi configure --workspace . \
  --model YOUR_MODEL_ID --base-url https://api.openai.com/v1 \
  --prompt-key --token-parameter max_completion_tokens \
  --max-steps 1 --max-episodes 100
nanorsi doctor --workspace . --check-model
nanorsi baseline --workspace .
nanorsi run --workspace .
nanorsi freeze --workspace . --repeats 1
nanorsi final-test --workspace .
nanorsi report --workspace . --format html
nanorsi verify --workspace .
```

`configure` is offline. Hidden `--prompt-key` input creates a unique external key file; TOML stores only its absolute path. Choose exactly one of `--prompt-key`, `--api-key-file /absolute/external/path` for an existing file, or `--no-api-key` for an unauthenticated local endpoint. Browser login, exported `OPENAI_API_KEY`, and `.env` files do not configure the bridge. There is no raw `--api-key` flag. Never store credentials inside this workspace.

The bridge uses OpenAI-compatible `/chat/completions`; give a base URL without that suffix. Native Anthropic Messages or OpenAI Responses need another adapter. Choose the supported token parameter (`max_tokens` or `max_completion_tokens`). Preserve generated model/proposer/evaluator commands, which pin the creating Python interpreter. Model settings become fixed once the experiment journal starts; changed settings then require a fresh workspace.

Plain `doctor` validates configuration/key files offline. `--check-model` sends exactly one bounded request requiring `{"tool":"final"}`, without baseline or lineage mutation. Hosted probes may cost money outside experiment accounting. This checks connectivity and formatting, not skill improvement.

## Budget and interpretation

This one-attempt example can use 94 search episodes: 30 baseline + 4 training + 30 parent validation + 30 candidate validation. The one-repeat, three-condition final panel adds 90 outside the search cap. Each task permits up to eight model calls; proposal calls and probes are additional. The untouched defaults allow five attempts, a 400-episode cap, up to 350 search episodes and 270 final episodes at three repeats. Episode limits are not a dollar cap; unknown provider cost is not zero.

Open `reports/report.html` to compare initial skills, no skills and selected skills. Training feedback informs patches; validation chooses candidates; final testing never promotes a candidate. Rejected, unchanged and failed attempts still consume attempt budget and remain in the evidence. `verify` reports `lineage: ok` when integrity checks pass, regardless of whether skills gained performance.

The default `frozen` arm always proposes through initial skills. In a separate matched workspace, set `experiment.arm = "self-use"` before baseline so accepted skills help generate later proposals. Both modify the current parent. Freeze all arms before examining final results and repeat independent experiments before claiming recursive benefit.

The runner loads Markdown skills and exposes list/read/write/final operations in fresh task directories. Replace `agent.model_command` before baseline only when deliberately supplying a custom JSON bridge; see `adapters/model.py` for request/response conventions. Local execution does not hide filesystem data from arbitrary Python; use external isolation for untrusted executable candidates.
