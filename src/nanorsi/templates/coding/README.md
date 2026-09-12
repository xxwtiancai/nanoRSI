# Python coding experiment

This workspace asks whether a fixed model solves more Python repair tasks after reusable Markdown skills evolve. Each episode repairs a fresh `solution.py`; cross-attempt proposals modify only `target/agent/skills/**`. There is no model-weight training. The twelve independently authored tasks have four train, four validation and four final-test tasks, with distinct families across splits. They are a small starter suite, not evidence of broad model gains.

## Configure API access first

From this workspace, replace `YOUR_MODEL_ID` with an exact model ID your API account can use. Create your key in the [OpenAI console](https://platform.openai.com/api-keys), or consult the [full provider/key tutorial](https://github.com/xxwtiancai/nanoRSI/blob/main/docs/QUICKSTART.md) ([中文](https://github.com/xxwtiancai/nanoRSI/blob/main/docs/QUICKSTART.zh-CN.md)) for other compatible providers and local servers.

```bash
nanorsi configure --workspace . \
  --model YOUR_MODEL_ID --base-url https://api.openai.com/v1 \
  --prompt-key --token-parameter max_completion_tokens \
  --max-steps 1 --max-episodes 40
nanorsi doctor --workspace . --check-model
nanorsi baseline --workspace .
nanorsi run --workspace .
nanorsi freeze --workspace . --repeats 1
nanorsi final-test --workspace .
nanorsi report --workspace . --format html
nanorsi verify --workspace .
```

`configure` is offline. `--prompt-key` uses hidden terminal input and creates a unique key file outside this workspace; only its path is stored in TOML. Choose exactly one of `--prompt-key`, `--api-key-file /absolute/external/path` (existing file), or `--no-api-key` (unauthenticated endpoint). A browser login, exported `OPENAI_API_KEY`, or `.env` file does not configure the bundled bridge. There is no raw `--api-key` flag.

The bridge uses OpenAI-compatible `/chat/completions`; use a base URL without that suffix. Native Anthropic Messages and OpenAI Responses need a custom adapter. Select `max_tokens` or `max_completion_tokens` according to the model. Preserve generated model/proposer/evaluator commands, which pin the creating Python interpreter. Configure before the experiment journal starts; after that, use a fresh workspace for changed settings.

Plain `doctor` checks configuration and key files offline. `--check-model` makes one bounded request requiring `{"tool":"final"}`, without baseline or lineage mutation. Hosted probes can cost money outside experiment accounting. A successful probe establishes connectivity and response format, not performance.

## Read the result

Open `reports/report.html`. Baseline measures initial validation performance; run uses training feedback to propose a skill patch and validation to accept or reject it. Freeze fixes the selected version. Final testing compares initial skills, no skills and selected skills on unseen tasks; it cannot promote a candidate. Accepted commits and `nanorsi/gen-N` tags identify the evaluated skills. Rejected, unchanged and failed attempts remain visible. Successful verification prints `lineage: ok`, not a claim of improvement.

The preset above allows one attempt: at most 16 search episodes (4 baseline + 4 training + 4 parent validation + 4 candidate validation), plus 12 final episodes outside the search cap. Each task allows up to eight model calls; one proposal call and connectivity probes are additional. The untouched template permits three attempts and 100 search episodes; a full search uses up to 40 episodes. These limits are not a dollar cap. Unknown cost is not zero.

The default `frozen` arm proposes using initial skills. In a separate matched workspace, set `experiment.arm = "self-use"` before baseline to let accepted skills help write the next patch. Both modify the current parent. Freeze both arms before looking at final results and repeat independent runs before claiming recursive benefit.

The agent can inspect/edit files and run supplied public tests; the evaluator scores behavior with public and private unittest suites. Reference programs validate the task pack and are excluded from model requests. Correct alternative implementations can pass. Generated Python runs with local privileges; this is not a sandbox or a way to hide host files from arbitrary code. Use external isolation for untrusted programs or confidential labels.
