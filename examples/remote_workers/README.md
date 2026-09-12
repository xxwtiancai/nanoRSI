# Optional HTTP evaluation workers

This is a **localhost transport demonstration**, using two independent worker
processes and the installed `program` template evaluator. It demonstrates
authenticated remote evaluation plumbing and kernel-compatible results. It does
not demonstrate a multi-host cluster, distributed training, or a hardened sandbox.
Candidates are trusted code running with the worker owner's filesystem/network
access. Localhost processes share the host filesystem; this is not private-label
isolation against candidate code.

Use Python 3.11 or newer with nanoRSI installed, then run from the repository:

```sh
python examples/remote_workers/demo.py --output /tmp/nanorsi-http-proof
```

The output directory must be new. The driver renders the ordinary initial program
template, independently starts two workers on `127.0.0.1` with ephemeral ports,
and evaluates that same source on each worker's training panel. It writes
`transport-proof.json` containing distinct process IDs and source, request,
manifest, and evaluator hashes. All workers stop and the temporary authentication
file is deleted on exit. No model call or winning source patch is used. To exercise
an existing program workspace without changing it:

```sh
python examples/remote_workers/demo.py --output /tmp/existing-http-proof --workspace /path/to/program-lab
```

The probe is transport evidence, not an improvement score or a held-out selection
procedure. The request hash and the standard evaluator's source trace bind each
result to the requested source. Worker IDs/PIDs identify the responding process;
they are not cryptographic attestation.

## Kernel integration

Copy `remote_evaluate.py` to the lab's `adapters/remote_evaluate.py`, then configure
the evaluator command before its baseline commit:

```toml
[evaluator]
command = ["/absolute/path/to/python", "adapters/remote_evaluate.py", "--urls", "http://127.0.0.1:PORT1", "http://127.0.0.1:PORT2", "--token-file", "/private/path/worker.token"]
timeout_s = 45
primary_metric = "score"
direction = "maximize"
heldout_enabled = false
```

Keep the token file outside the lab and its version control. The file contains
32–512 ASCII letters, digits, underscores or hyphens (for example,
`secrets.token_hex(32)`), with owner-only permissions. The adapter uses the
standard `NANORSI_SPLIT`, `NANORSI_TASK_MANIFEST`, `NANORSI_SEED`,
`NANORSI_REPEAT_ID`, `NANORSI_TRAIN_LIMIT`, and `NANORSI_RESULT_PATH` environment
variables and reads only `target/program.py` as candidate source. A result-path
hash chooses the endpoint deterministically. It writes the ordinary schema-2
evaluation plus a `remote_worker` receipt. Ordinary baseline/run/freeze/final/verify
commands therefore keep the kernel's selection and final-evaluation protocol.

The example's Python API starts workers for a calling driver:

```python
from demo import local_workers, probe_workers

with local_workers(manifest, token_file, count=2,
                   job_timeout=30, max_requests=128) as workers:
    receipts = probe_workers(workers, token_file, manifest, initial_source)
    # Configure the adapter from worker["url"], then run the normal kernel CLI.
```

Import `demo` from this directory. Each worker entry contains `url`, `worker_id`,
`pid`, `manifest_sha256`, and `evaluator_sha256`. `local_workers` resolves the
already imported nanoRSI package for its subprocesses. The copied adapter still
requires nanoRSI installed or an absolute `PYTHONPATH` in the CLI environment.
Stop the context after all kernel commands finish; the endpoints are temporary.
`examples/demos/run.py --kinds remote` integrates the optional transport into the
live proposal workflow using the model configuration and request budget supplied
to that driver.

For manual startup, invoke `server.py` twice with distinct ready files and worker
IDs. Both workers must independently receive the same initial manifest file and
the same installed nanoRSI version:

```sh
python examples/remote_workers/server.py --manifest /path/to/manifest.json --token-file /private/path/worker.token --ready-file /tmp/worker-1.json --worker-id worker-1 --job-timeout 30 --max-requests 128
```

The ready file supplies the bound URL and process identity. SIGTERM stops the
worker and attempts to stop an active evaluator and its descendant process groups.
The server always binds to `127.0.0.1`; it does not accept a public bind option.

## Fixed wire protocol

`POST /evaluate` requires `Authorization: Bearer <token>`,
`Content-Type: application/json`, and a single `Content-Length`. The token is
compared with `hmac.compare_digest`. Chunked request bodies are rejected. The
request has exactly these fields:

| Field | Meaning |
| --- | --- |
| `source` | UTF-8 contents of `target/program.py` only |
| `source_sha256` | SHA-256 of the source bytes |
| `manifest_sha256` | SHA-256 of the complete initial manifest file bytes |
| `evaluator_sha256` | Framed SHA-256 over installed program/skills evaluator code and process, parser, and template helpers |
| `request_id` | 1–128 ASCII letters, digits, underscores or hyphens |
| `split` | `train`, `validation`, or `test` |
| `seed` | Integer from 0 through 2^63−1 |
| `repeat_id` | Integer from 0 through 1,000,000 |
| `train_limit` | Integer from 1 through 10,000; applies only to training |

There are no client-provided task labels, grader, test source, arbitrary paths,
model settings or argv. At startup the worker reads its manifest and snapshots the
installed program template. Each job gets a fresh temporary copy, the submitted
program, and a fixed evaluator command. JSON/schema/task selection is validated
with nanoRSI's existing evaluator helpers; this example introduces no new grader.

Success returns a schema-1 transport envelope containing the request metadata,
`worker_id`, `worker_pid`, and an `evaluation` holding the standard schema-2 result.
The adapter validates all request/source/data/evaluator identities, exact selected
task/group/repeat identities, program source traces, finite metrics, and absence of
task/feedback fields on validation/test cases. It does not follow HTTP redirects.
Failure statuses include 400 (protocol/result), 401 (authentication), 409 (identity),
413 (body limit), 502 (job/response), and 504 (job timeout). Failure responses do
not echo submitted source, labels, tokens, or evaluator stderr.

Default bounds are 128 KB source, 1 MB request/response, 4 MB manifest, 10,000
manifest tasks, one connection/job per worker, 128 accepted connections per
worker lifetime, a five-second socket inactivity timeout, a 30-second job timeout,
and a 35-second client timeout. Evaluator stdout/stderr are discarded; the fixed
program evaluator additionally bounds each candidate invocation to two seconds
and 1 MB output. Result-file size is monitored during execution and checked again
before parsing. These controls bound normal work; they cannot contain malicious
code that changes files, creates persistent processes, or escapes cleanup.

For an owner-managed private network, keep the worker bound to loopback behind a
TLS reverse proxy and supply an `https://` origin to the adapter. HTTPS uses the
platform certificate trust store. Plain HTTP is accepted only for loopback IP
literals; URL credentials, queries, fragments, and non-root paths are rejected.
Network ACLs, TLS service configuration, account separation and an actual code
isolation boundary are the operator's responsibility. This repository's demo and
tests exercise localhost only; multi-host behavior and that deployment boundary
are unverified.

From a source checkout, run the integration checks with an absolute `PYTHONPATH`:

```sh
PYTHONPATH="$PWD/src" python -m unittest discover -s tests -p test_remote_workers.py -v
```
