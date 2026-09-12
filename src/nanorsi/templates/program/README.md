# Program improvement lab

This lab asks a configured model to improve `target/program.py`, a JSON batch
record summarizer. The initial implementation handles ordinary numeric amounts;
the full contract includes currency formatting, accounting negatives, normalized
status values, and missing categories. It already passes the basic cases.

Configure the model bridge in `nanorsi.toml` before running proposals. No provider
or model is selected automatically. For a GLM experiment, configure your actual
OpenAI-compatible endpoint, model identifier, and explicit credential file.
Only proposals call the model; program evaluation is deterministic local Python.

The fixed evaluator executes the current program source with JSON stdin and
grades JSON stdout. Four training tasks expose their inputs and expected/current
outputs to the proposer. Four validation and four test tasks use separate data
and groups; their labels are excluded from proposal feedback. Program source
hashes are recorded in episode traces, and proposal usage records model calls.

Only `target/program.py` is mutable. The evaluator, manifest, adapter, and proposal
driver remain fixed. A proposal must be a model-generated unified diff based on
the current source and training feedback; there is no built-in winning patch.

This small capability demonstration is not a broad coding benchmark. The task
process has a two-second limit and capped output. Candidate code is trusted local
code, and those resource limits are not a security sandbox.
