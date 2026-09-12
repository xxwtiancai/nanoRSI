# A small lab for coding-agent improvement

The coding starter asks a concrete question: can a fixed model solve more Python repair tasks after its reusable skills evolve? Each episode edits a fresh `solution.py`; the cross-episode search changes only Markdown skills. It does not train model weights or accumulate solved task source as a skill library.

## Start with a verified task pack

The twelve independently authored tasks cover stable deduplication, chunking, recursive configuration merge, boolean parsing, interval merging, retry delays, nested lookup, numeric versions, CSV parsing, rolling means, dependency ordering and header redaction. Each task has a specification, broken starter, public tests, private edge cases and a reference implementation. Four distinct task families belong to each split; families do not cross splits.

```bash
python examples/coding_tasks/prepare.py --check
python examples/coding_tasks/prepare.py /tmp/coding-manifest.json
```

The offline check executes all starters and references. It should report 0/12 starters passing and 12/12 references passing. These numbers validate the authored suite; they are not model performance or evidence of self-improvement. Twelve tasks are too small to establish broad generalization.

## Run with your model

For Python/Git installation, provider consoles, API-key creation, endpoint selection and troubleshooting, follow the [complete first-run tutorial](QUICKSTART.md). A browser login and exported environment key do not configure nanoRSI. After installation, replace `YOUR_MODEL_ID` with an exact model ID available to your API account:

```bash
nanorsi new coding ./coding-lab --goal "Improve reliable Python repair through reusable skills"
nanorsi configure --workspace ./coding-lab \
  --model YOUR_MODEL_ID --base-url https://api.openai.com/v1 \
  --prompt-key --token-parameter max_completion_tokens \
  --max-steps 1 --max-episodes 40
nanorsi doctor --workspace ./coding-lab --check-model
nanorsi baseline --workspace ./coding-lab
nanorsi run --workspace ./coding-lab
nanorsi freeze --workspace ./coding-lab --repeats 1
nanorsi final-test --workspace ./coding-lab
nanorsi report --workspace ./coding-lab --format html
nanorsi verify --workspace ./coding-lab
```

`configure` works offline. Hidden key input writes a unique external file, and only its path enters TOML. An existing absolute external `--api-key-file` or a local server's `--no-api-key` are alternatives. Use the [provider table](QUICKSTART.md#2-get-api-access-and-choose-an-endpoint) to change endpoint and token parameter. Keep the generated model/proposer/evaluator commands: they pin the Python interpreter that created the workspace. Complete configuration before the experiment journal starts; subsequent changes require a new workspace.

Plain `doctor` checks files offline. `doctor --check-model` sends one bounded request and requires `{"tool":"final"}` without starting a baseline or changing lineage; a hosted probe can cost money outside experiment accounting. The authenticated local HTTP tests do not establish paid-provider compatibility.

Open `coding-lab/reports/report.html`. Markdown and report data are generated alongside it. Use `python examples/compare.py ./coding-lab/reports/final.json` for a comparison summary. A successful `verify` reports `lineage: ok`; it checks evidence integrity, not whether skills improved.

The one-attempt preset above uses at most 16 search episodes: 4 baseline + 4 training + 4 parent validation + 4 candidate validation. The one-repeat final panel adds 12 outside the search cap, for up to 28 task episodes. At eight calls per episode, that is up to 224 episode calls plus one proposal and separate connectivity probes. The untouched template permits three attempts and a 100-episode cap; its full search can use 40 episodes, with final testing additional. Failed, rejected and unchanged attempts consume the attempt budget. These are execution limits, not a dollar cap; unknown cost is not zero.

## Follow a skill through the RSI loop

`baseline` measures the initial skills on validation tasks. `run` executes training tasks, provides their feedback to the proposer, and requests a patch to `target/agent/skills/**`. The fixed gate compares parent and candidate on validation. An accepted candidate gets a recorded commit and `nanorsi/gen-N` tag; rejected, no-op and failed attempts remain visible in the report and `.nanorsi/runs/`.

Within a task the model edits a fresh `solution.py`; this repair is task output. Across attempts, the durable change is a procedural Markdown skill, such as a better inspection or verification procedure. The model weights stay fixed. `freeze` fixes the selected version; `final-test` compares initial skills, no skills and selected skills on unseen tasks. The final score never promotes a candidate, and improvement is not guaranteed.

For a recursive comparison, use separate identically configured workspaces. Before baseline, set `experiment.arm` to `"frozen"` in one and `"self-use"` in the other. Frozen always proposes using initial skills; self-use uses the latest accepted skills to propose the next patch. Both modify the current parent. Match tasks, model settings and budgets, freeze both before examining either final panel, and repeat independent evolution runs before claiming a repeatable benefit.

## What the agent can do

The agent returns one JSON action at a time: `list`, `read`, `write`, `test`, or `final`. The fixed `test` action runs only the supplied public unittest suite against a disposable snapshot. A typical episode is test → inspect failure → edit → test → final. There is no arbitrary shell-command action. The text-edit `skills` starter retains its original four tools.

Public test source and bounded diagnostics are available for learning. Private tests and reference solutions are excluded from model requests and training feedback. The evaluator checks candidate behavior using public and private suites, so an alternative correct implementation passes. Reference source is used to validate the task pack, not as an exact-match grading oracle. Output file names must match the task's input/reference file contract.

This is **trusted local code execution**. Generated Python can exercise host privileges; timeout/output limits and temporary directories are not an OS sandbox. Use an external container, VM or evaluation service for untrusted programs and genuinely confidential test labels. See [SECURITY.md](../SECURITY.md).

## Add your own task

Keep `schema_version: 1` at the manifest root. Each task contains:

```json
{
  "task_id": "my-utility-01",
  "group_id": "my-utility-family",
  "split": "train",
  "instruction": "Describe the full function behavior and edge cases.",
  "input_files": {"solution.py": "...broken Python source..."},
  "expected_files": {"solution.py": "...reference Python source..."},
  "grading": {
    "kind": "python-unittest",
    "public_tests": {"test_public.py": "...unittest source importing solution..."},
    "private_tests": {"test_private.py": "...separate edge-case tests..."},
    "timeout_s": 2
  }
}
```

Write actual Python source in place of the illustrative strings. Both suites must load at least one unittest. Test names are flat `test_*.py` names; traversal and absolute paths are rejected. Keep source groups within one split. All three splits must be nonempty. Test execution permits at most 128 text files, 1 MB per source mapping, 16 KiB captured output and a timeout greater than zero and at most ten seconds. Changing tests, model settings or the task manifest after baseline requires a new workspace.

## What we learned from OpenRSI

[OpenRSI](https://github.com/FrontisAI/OpenRSI) combines executable task environments, improvement operators and reproducible results. The relevant concrete references are its [task evaluator](https://github.com/FrontisAI/OpenRSI/blob/bf2b2ee19a260cb4dba0da1a20fb2212727b6ea4/OpenMLE-Gym/openmle_gym/local_evaluator.py) and [validation-based final selection test](https://github.com/FrontisAI/OpenRSI/blob/bf2b2ee19a260cb4dba0da1a20fb2212727b6ea4/OpenMLE-Evo/third_party/aira-evo/tests/test_final_node_selection.py). nanoRSI applies these ideas to a small fixed-model skills experiment with an independent final split.

This implementation and task pack are independently written. No OpenRSI code, prompts, datasets or model weights are included. Its [non-commercial license](https://github.com/FrontisAI/OpenRSI/blob/bf2b2ee19a260cb4dba0da1a20fb2212727b6ea4/LICENSE) is distinct from nanoRSI's Apache-2.0 license. nanoRSI does not reproduce or claim OpenRSI's reported benchmark results, training system or population search.
