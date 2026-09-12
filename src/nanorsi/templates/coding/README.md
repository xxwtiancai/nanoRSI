# Python coding experiment

This workspace compares agent skills on twelve small, independently authored
Python utility bugfix tasks. Each episode starts from a broken `solution.py`.
The agent can inspect files, edit its solution, and run exposed public tests;
the evaluator scores behavior with public and private standard-library
`unittest` suites. It does not compare source text with a reference solution.

The pack has four training, four validation, and four final-test tasks. Each
split uses different utility families, with no group shared across splits.
These are starter tasks for developing and testing an experiment workflow,
not an independent published benchmark or evidence of model improvement.
Their small size, public distribution, and hand-authored tests limit any
performance claims. Use a separate, larger task collection for such claims.

Configure the model identity and compatible base URL in `nanorsi.toml` before
running `nanorsi doctor` and `nanorsi baseline`. The default local endpoint is
a placeholder. Then use `nanorsi run`, `nanorsi report`,
`nanorsi freeze --repeats 3`, `nanorsi final-test`, and `nanorsi verify`.
The default budget allows three proposal steps, 100 episodes, and eight model
turns per episode. Only the Markdown skills are mutable across proposals;
the model, runner, grader, task manifest, and public tests stay fixed.

The default `frozen` arm proposes with its initial skills. To compare `self-use`,
initialize another workspace with the same settings, change `experiment.arm`
before baseline, and compare independently frozen results. Validation chooses
candidates; final-test results cannot promote one. These controls make the
comparison auditable but do not establish a gain without actual model runs.

Public tests provide iterative feedback and private tests cover additional
contract cases. Reference programs validate the task pack and are not supplied
to the episode. The manifest is present on the host, so a local subprocess is
not a security sandbox or a way to conceal benchmark material from arbitrary
code. Use external isolation and trusted datasets for untrusted workloads.
