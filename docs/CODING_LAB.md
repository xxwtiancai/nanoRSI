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

Install nanoRSI from the repository, then create a fresh workspace:

```bash
nanorsi new coding ./coding-lab --goal "Improve reliable Python repair through reusable skills"
```

Before baseline, edit the existing `[agent]` section in `coding-lab/nanorsi.toml`. Keep the other fields unless you intentionally change the experiment:

```toml
[agent]
model_command = ["python3", "adapters/model.py"]
model = "your-model-id"
base_url = "http://localhost:8000/v1"
max_turns = 8
max_tokens = 2048
timeout_s = 60
skills = ["inspect", "edit", "verify"]
```

For an authenticated compatible endpoint, set `api_key_file` to an absolute path outside the workspace. Do not commit credentials. A local compatible server can omit the key. Use a fixed model snapshot when available. [Model configuration and execution limits](QUICKSTART.md#choose-a-budget-before-running) apply to both coding and text-edit experiments.

```bash
nanorsi doctor --workspace ./coding-lab
nanorsi run --workspace ./coding-lab
nanorsi freeze --workspace ./coding-lab --repeats 1
nanorsi final-test --workspace ./coding-lab
nanorsi report --workspace ./coding-lab --format html
nanorsi verify --workspace ./coding-lab
```

Open `coding-lab/reports/report.html`. Markdown and raw lineage are generated alongside it. Use `python examples/compare.py ./coding-lab/reports/final.json` for a machine-readable comparison. To compare frozen and self-use proposers, use separate identically configured workspaces, change only `experiment.arm` before baseline, and freeze both before examining either final panel. Repeat with independent seeds before interpreting a result as repeatable.

The coding defaults allow three proposal attempts and at most 100 search episodes. A full three-attempt run can use 40 task episodes (4 baseline, plus 3 × [4 training + 4 parent validation + 4 candidate validation]); a one-repeat final panel adds 12. Each task has up to eight model calls, and each proposal has an additional call. Incomplete, rejected and unchanged attempts count against the attempt budget. Final episodes are recorded separately from the search cap. Hosted calls may incur costs; unknown cost is not zero.

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
