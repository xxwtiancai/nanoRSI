# Skills experiment

Configure `nanorsi.toml` before baseline: model identity, compatible base URL and optional absolute external API-key file. Replace `agent.model_command` to use your own bridge. The model command consumes a JSON request and emits JSON `content` plus nullable `usage`; see `adapters/model.py`.

Run `nanorsi doctor`, `nanorsi baseline`, `nanorsi run`, `nanorsi report`, then `nanorsi freeze --repeats 3`, `nanorsi final-test` and `nanorsi verify` from this workspace.

The task manifest contains local protocol fixtures, not a public benchmark. Default training feedback covers four tasks per attempt; the validation panel chooses candidates. Final testing is separately budgeted and never promotes candidates. Freeze all comparison arms before examining final results.

Change `experiment.arm` to `self-use` in a separate workspace before baseline to use the accepted Harness for later proposals. `frozen` always proposes through the initial Harness. Both modify the current parent. Only skill files are mutable by default.

The default runner loads Markdown skills and offers list/read/write/final operations. Unknown provider cost is null. Local execution does not hide filesystem data from arbitrary Python; use external isolation for untrusted executable candidates. Do not store key files inside this workspace.
