# Recursive Self-Improvement (RSI) Research Dossier & Architecture Survey

## 1. Executive Summary

This dossier tracks foundational and frontier research in Recursive Self-Improvement (RSI) for language models and autonomous agents. It establishes the theoretical taxonomy, analyzes leading open-source frameworks, and maps research advancements into the minimal primitives maintained by **nanoRSI**.

nanoRSI structures self-improvement into three orthogonal layers:
1. **Artifact RSI** (Target Assets): Continuous refinement of discrete artifacts (code, prompts, policies, tools) where the agent executes a search over function space.
2. **Harness RSI** (Agent Cognitive Architecture): Self-adaptation of the agent internal scaffolding, tool-dispatch logic, memory reflection, and context engineering.
3. **Model RSI** (Model Weights & Adapters): Closed-loop parameter adaptation, self-distillation, fine-tuning scripts, and LoRA weight evolution under external training contracts.

---

## 2. Research Taxonomy & Paradigm Landscape

| Paradigm | Target Layer | Primary Mechanism | Representative Research / Repos | Key Safety / Soundness Invariant |
| :--- | :--- | :--- | :--- | :--- |
| **Function Search / MAP-Elites** | Artifact | Genetic programming & LLM mutation with quality-diversity archives | FunSearch (DeepMind), OpenEvolve | Island model isolation; evaluator code outside candidate mutation surface |
| **Agentic Context Engineering (ACE)** | Harness | Dynamic playbook evolution, strategy pruning, and context delta accumulation | ACE, Memento-Skills, Hermes Agent | Structured mutation schema; append-only strategy provenance |
| **Darwin Gödel Machine (DGM)** | Harness / Artifact | Self-modification assessed empirically on coding benchmarks | DGM, Gödel Agent | Empirical benchmark evidence; not a formal proof of global improvement |
| **Self-Adapting Language Models (SEAL)**| Model | Execution feedback looped into synthetic dataset curation and targeted parameter update | SEAL, Continual-Intelligence/SEAL | Parameter divergence boundaries; verification on held-out generalist tasks |
| **Principled Evaluation Loop** | Across All | Standardized operator lifecycle: Select -> Mutate -> Evaluate -> Gate -> Lineage | RSIHub (simple-agent-lab), nanoRSI | Evaluator freeze; immutable ground-truth; HMAC audit trails |

---

## 3. Comparative Deep Dive: Canonical Upstreams & nanoRSI Primitives

### 3.1 RSIHub (simple-agent-lab/RSIHub)
- **Core Abstraction**: Recipe-driven pipeline with explicit operator stages (`Select`, `Rollout`, `Analyze`, `Mutate`, `Validate`, `Novelty`, `Gate`, `Record`, `Reflect`).
- **Isolation Strategy**: Generation tags in Git; framework runs operators in subprocesses; sealed split evaluation (`gen/0` anchor) protects against false improvement claims.
- **nanoRSI Mapping**: nanoRSI distills this lifecycle into a single-binary, stdlib-only kernel (`nanorsi.kernel.runner`) operating on dedicated git worktrees. Where RSIHub provides extensible multi-operator plugins, nanoRSI provides the minimal, immutable protocol guarantee: zero unvalidated file mutation, deterministic HMAC lineage, and atomic rollback.

### 3.2 OpenEvolve & FunSearch
- **Core Abstraction**: Evolutionary search in function space utilizing language models as mutation operators. Programs are evaluated on fitness functions, with top-performing programs stored in an elitist archive.
- **nanoRSI Mapping**: Embedded directly in the `artifact` template (`nanorsi.templates.artifact`). The candidate code is isolated in `target/`, while the evaluator and tests remain read-only.

### 3.3 Hermes Agent & Memento-Skills
- **Core Abstraction**: Agent self-improvement through skill library accretion and procedural consolidation. Successful tool use sequences are distilled into modular Python skills.
- **nanoRSI Mapping**: Embedded in the `harness` template (`nanorsi.templates.harness`). Mutability is governed by `mutable_surface` in `nanorsi.toml` (e.g. `target/agent/**`), guaranteeing that agent logic can self-refine while evaluation harnesses remain frozen.

### 3.4 SEAL (Self-Adapting Language Models)
- **Core Abstraction**: Closed-loop parameter adjustment through synthetic data generation from problem-solving traces, followed by localized parameter tuning (LoRA/fine-tuning).
- **nanoRSI Mapping**: Formalized as an external training contract (`nanorsi.templates.model`). The kernel handles evaluation, git checkpoints, and score gates, delegating GPU compute to external training scripts with deterministic resource budgets.

---

## 4. Key Invariants for Trustworthy RSI

All self-improvement implementations in nanoRSI must preserve three core security and correctness invariants:

1. **Frozen Evaluator Invariant**:
   The code measuring performance, the test suites, and the scoring logic must never reside in the candidate mutation surface. All metrics must be mechanism-owned.
2. **Atomic Rollback & Lineage Guarantee**:
   Every mutation step must be tagged, hashed, and verifiable. If a candidate degrades performance or violates constraints, the environment must cleanly revert to the verified baseline commit.
3. **Budget & Subprocess Sandboxing**:
   Every candidate generation and evaluation run must be strictly bounded in wall-clock time, memory, and subprocess access to prevent runaway recursion or resource exhaustion.

---

## 5. Continuous Research Radar (Updated Daily)

- **2026-09-13 Tracking (candidate integrations and state preservation)**:
  - **Evidence scope**: rechecked two default-branch commits, the latest release entry, and the three most recently updated open issues/PRs for each of the six reference repositories. All six heads and latest release entries match the September 12 snapshot. The items below are open proposals, not merged capabilities or independently reproduced results.
  - **RSIHub — draft DeepSeek Harness integration**: [PR #79](https://github.com/simple-agent-lab/RSIHub/pull/79), updated September 12, adds a candidate recipe and session-log usage extraction. Inspected `seeds/dsh/dsh_trajectory.py`: recognized token fields are recorded when present; absent metering remains null. The proposal still lists end-to-end validation as outstanding. **Decision:** retain explicit unknown usage in nanoRSI reports; do not import the Node/SDK integration without a concrete benchmark and a validated transport. Session-log accounting alone is not independent attestation of candidate resource consumption.
  - **Anton — memory round-trip preservation**: open [PR #472](https://github.com/mindsdb/anton/pull/472), updated September 12, addresses rules lost during read/modify/write when entries precede a heading or use an unfamiliar section. The inspected diff shares section names and supplies fallback handling plus regression cases. nanoRSI's bundled skills proposer emits a unified diff rather than using Anton's rules parser. **Decision:** no direct port; require preservation tests before introducing a structured memory compactor. Upstream test outcomes were not reproduced here.
  - **ACE — atomic adapter proposal**: [issue #42](https://github.com/ace-agent/ace/issues/42), updated September 12, proposes Generator–Reflector–Curator callables with versioned deltas, stale-write rejection and replay-safe application. Its body explicitly leaves upstream runner wiring unfinished; this is an issue describing a prototype, not an integrated implementation. **Decision:** keep nanoRSI's existing experiment lock and Git-backed candidate lifecycle; reconsider an adapter only with executable integration evidence.
  - **SEAL, DGM, OpenEvolve**: sampled activity supplies no newer merged mechanism. Retain external parameter training, bounded empirical evaluation, and structured verdict parsing respectively; OpenEvolve [PR #486](https://github.com/algorithmicsuperintelligence/openevolve/pull/486) remains open.
  - **Outcome:** research-only update. These proposals identify integration checks worth retaining but do not establish a missing nanoRSI runtime feature or new capability gain.

- **2026-09-12 Tracking (releases and open proposals beyond default-branch heads)**:
  - **Evidence scope**: all six default-branch heads match the September 11 snapshot below. Also checked the latest release and the two most recently updated open pull requests per repository; this is a bounded activity sample, not a comprehensive review of all branches.
  - **Anton — prerelease and unmerged reliability work**: [v2.26.9.11.1rc4](https://github.com/mindsdb/anton/releases/tag/v2.26.9.11.1rc4), published September 11 and marked prerelease, lists a cloud-conversation timestamp correction. Separately, open [PR #471](https://github.com/mindsdb/anton/pull/471) describes preventing empty tool-call IDs from poisoning replayed conversation history. Its reported test results are author claims, not independently reproduced here. nanoRSI's bundled adapter consumes textual message content and the skills runner parses JSON actions; it does not implement this provider-native tool-call replay path. **Decision:** no direct port; validate replay identifiers if such a transport is introduced later.
  - **OpenEvolve — unmerged novelty parser fix**: inspected the diff and regression cases in open [PR #486](https://github.com/algorithmicsuperintelligence/openevolve/pull/486), updated September 10. It normalizes `NOT_NOVEL` to `NOT NOVEL` before substring classification, with cases for plain, explained, and Markdown-wrapped responses. This remains a proposal, not a released fix. nanoRSI has no corresponding free-text novelty judge; its evaluation result is parsed as JSON and schema-validated. **Decision:** retain structured decision contracts; if a novelty judge is added, test negative labels and ambiguous responses before using it as a gate.
  - **RSIHub, SEAL, DGM, ACE**: no release entries were returned, and the sampled open proposals were last updated before September 11. Retain the prior isolation, external-training, empirical-evaluation, and merged-candidate validation decisions. No runtime change is supported by this check.

- **2026-09-11 Tracking (comparison with September 10)**:
  - **Evidence scope**: rechecked the two latest default-branch commits for all six reference repositories. Heads remain [RSIHub `bb8f4dd`](https://github.com/simple-agent-lab/RSIHub/commit/bb8f4ddde8f6c301bbf0a976af01747d11b8dab1), [Anton `22f7414`](https://github.com/mindsdb/anton/commit/22f74142ad5dffc81b1f85232b0b7ce5a3df451d), [SEAL `6d9c9f9`](https://github.com/Continual-Intelligence/SEAL/commit/6d9c9f9ee392c6cc618e771f399d436d190f6ca4), [DGM `a565fd2`](https://github.com/jennyzzt/dgm/commit/a565fd2d1dca504ef5104a7cc0f3bdc4ab9b4fd2), [OpenEvolve `411fb59`](https://github.com/algorithmicsuperintelligence/openevolve/commit/411fb59c886c18704caaffb611e17cf9e7d824d2), and [ACE `82709de`](https://github.com/ace-agent/ace/commit/82709de050e1db6e6ef2f07bcb0393560b94992a). This comparison covers merged default-branch activity, not unpublished experiments or other branches.
  - **Decision**: no newly merged mechanism warrants a runtime port. Retain the September 9–10 adoption decisions: separate search from final evaluation, keep model training external, reject boolean fitness values, and require evidence on the merged candidate before adopting multi-proposal orchestration. Repeated checks are not additional evidence of capability gains.

- **2026-09-10 Tracking (default-branch comparison with September 9)**:
  - **Anton — documentation-only change**: [September 9, `22f7414`](https://github.com/mindsdb/anton/commit/22f74142ad5dffc81b1f85232b0b7ce5a3df451d) updates Docusaurus packages to 3.10.2 in `docs/package.json` and its lockfile. The inspected diff changes no agent learning mechanism; no nanoRSI runtime port is warranted.
  - **Unchanged reference heads**: [RSIHub `bb8f4dd`](https://github.com/simple-agent-lab/RSIHub/commit/bb8f4ddde8f6c301bbf0a976af01747d11b8dab1), [SEAL `6d9c9f9`](https://github.com/Continual-Intelligence/SEAL/commit/6d9c9f9ee392c6cc618e771f399d436d190f6ca4), [DGM `a565fd2`](https://github.com/jennyzzt/dgm/commit/a565fd2d1dca504ef5104a7cc0f3bdc4ab9b4fd2), [OpenEvolve `411fb59`](https://github.com/algorithmicsuperintelligence/openevolve/commit/411fb59c886c18704caaffb611e17cf9e7d824d2), and [ACE `82709de`](https://github.com/ace-agent/ace/commit/82709de050e1db6e6ef2f07bcb0393560b94992a). OpenEvolve's current canonical repository is `algorithmicsuperintelligence/openevolve`; the former `codelion` URL redirects there. Unchanged heads do not establish that no work exists on other branches or in papers.
  - **Applicability to nanoRSI v0.2**: the independent final-test boundary discussed on September 9 now has a concrete local counterpart: `run` uses training/validation, `freeze` closes search, and `final-test` compares initial skills, no skills, and the selected candidate. `tests/test_v2_lifecycle.py` checks that no test split is evaluated during search, final testing requires freezing, and steps are blocked afterward. These deterministic fixtures verify the protocol, not real-model improvement or a hostile-process security boundary.
  - **Decision**: retain the existing evaluation controls and defer ACE-style parallel proposal/reducer orchestration until a measured experiment justifies it. SEAL remains an external model-training reference; DGM remains an empirical self-modification reference. No new mechanism in the inspected changes supports a runtime modification today.

- **2026-09-09 Tracking (primary-source check)**:
  - **RSIHub — new since the previous check**: [September 8 merge `bb8f4dd`](https://github.com/simple-agent-lab/RSIHub/commit/bb8f4ddde8f6c301bbf0a976af01747d11b8dab1) introduces continuous research isolation. The [lifecycle change](https://github.com/simple-agent-lab/RSIHub/commit/5dbf7a7d36483f576126336d37aa216022a7650d) unifies research into a continuous session that can publish candidates before finishing; sealed evaluation follows explicit completion. The framework retains control of guardrail and evaluation phases. **Implication:** future long-running nanoRSI experiments should separate development feedback from final held-out acceptance; this does not justify adding a controller to the minimal kernel now.
  - **Anton — new repository activity, no RSI mechanism change identified in the inspected commits**: [September 8 docs dependency fix](https://github.com/mindsdb/anton/commit/d63624618d8897f50b578dec1969870917465b88) raises the declared React minimum while retaining the already-resolved version. This is documentation dependency maintenance, not evidence of improved agent learning, and does not apply to nanoRSI's stdlib runtime.
  - **SEAL — baseline rechecked, not a new release**: the inspected default-branch head remains [August 1, 2025, `6d9c9f9`](https://github.com/Continual-Intelligence/SEAL/commit/6d9c9f9ee392c6cc618e771f399d436d190f6ca4). [Self-Adapting Language Models](https://arxiv.org/abs/2506.10943) uses reinforcement learning to generate self-edits comprising training data and update directives. Keep parameter adaptation behind the external training contract; similarly named SEAL papers are distinct projects.
  - **DGM — baseline rechecked, terminology clarified**: the inspected head remains [August 13, 2025, `a565fd2`](https://github.com/jennyzzt/dgm/commit/a565fd2d1dca504ef5104a7cc0f3bdc4ab9b4fd2). Its [reference implementation](https://github.com/jennyzzt/dgm) describes empirical coding-benchmark validation of self-modifications, not formal proof of global improvement. nanoRSI's acceptance gate likewise supplies bounded empirical evidence.
  - **OpenEvolve — older fix newly assessed for applicability**: [July 18, `411fb59`](https://github.com/codelion/openevolve/commit/411fb59c886c18704caaffb611e17cf9e7d824d2) excludes boolean flags from fitness aggregation, preventing a timeout flag from inflating a failed candidate's score. nanoRSI already rejects boolean metric values in `parse_evaluation`; boolean constraint flags remain separate. No runtime port is needed.
  - **ACE — older advancement newly assessed**: [August 24, `82709de`](https://github.com/ace-agent/ace/commit/82709de050e1db6e6ef2f07bcb0393560b94992a) adds parallel ComBEE proposals with an LLM reducer. The [reference project](https://github.com/ace-agent/ace) preserves context through incremental playbook updates. **Implication:** any future multi-proposal harness experiment must evaluate the merged candidate; individual proposal quality does not establish merged quality. Defer integration until a concrete benchmark warrants the added orchestration.
  - **Decision:** update the research record and correct DGM terminology. No new runtime dependency or behavior change is supported by this check. Dates above are upstream commit dates, not claims that every item is a newly published advancement.

- **2026-09-08 Tracking**:
  - *TokenRhythm/NeoHorse-1*: Towards Recursive Self-Improvement via Agentic Post-Training with Routing Harness (4B/9B based on Qwen3.5). Implements a closed-loop evaluation-selection-update cycle where execution trajectories in tool-use and coding environments yield training signals via routing-guided curriculum SFT and on-policy distillation. The routing harness dynamically monitors capability demands and feeds back into the training mixture. Emphasizes that execution safety, data decontamination, and harness-driven task dispatch are essential prerequisites for long-horizon RSI loops.
  - *Liuziyu77/Awesome-RSI* (Systematic RSI Taxonomy & Corpus): Classifies self-improvement into a clean tripartite hierarchy: Experience Accumulation (prompts, context, skills, memory), System Modification (harnesses, tools, code mutation, meta-agents like DGM, SICA, MGM, Metaⁿ), and Model Parameters (weight updates, RL, distillation like SafeEvolve, APEx, SPADE). Validates nanoRSI's architectural positioning as a lean, robust System Modification harness with immutable evaluator boundaries and verifiable HMAC lineage.
  - *KaiWU5/Awesome-AI4AI* (Can AI Reliably Improve AI?): Extensive weekly-updated 223-paper index tracking long-horizon autonomous research, automated harness synthesis, and recursive improvement benchmarks. Reinforces strict empirical controls against "phantom gains" and variance across task order in self-evolving agents.

- **2026-09-07 Tracking**:
  - *ahmd-mohsin/KernelAscent*: GPU kernel capability-stratified causal loop benchmark. Identifies that capability floors strictly govern RSI outcomes: frontier models show statistically significant causal self-use gains (F_selfuse > 0), whereas sub-threshold models experience negative returns from self-revision. Crucially demonstrates harness robustness requirements—native compiler crashes (SIGABRT) bypass Python-level signal timeouts, necessitating dedicated isolated per-task subprocesses and resilient process-group cleanup (mirroring nanoRSI subprocess boundaries).
  - *asimfish/awesome_rsi*: Synthesizes empirical evidence across 67 RSI papers. Highlights key empirical laws: evaluator discipline (anchoring outside the loop to prevent reward overoptimization/evaluator collapse), realized meta-depth constraints (~2.5 layers in practice), and the imperative for versioning, audit trails, deterministic forecasting, and atomic rollback in production RSI loops. Validates nanoRSI's core architecture of frozen evaluators, HMAC-signed lineage, and detached worktree isolation.
  - *SystemOriginArchive/creator-theory-operational-canon*: Formalizes recursive self-improvement safety criteria including successor alignment, automated auditing, criterion/evaluator drift mitigation, anti-capture, and provenance continuity. Strongly aligns with nanoRSI lineage verification and explicit gating mechanisms.

- **2026-09-06 Tracking**:
  - *mindsdb/anton*: Analyzed dual verification & session reflection logic (verifier-eval workflow). Reinforces that runtime task verification must rely on decoupled test suites and structured verdict gates.
  - *simple-agent-lab/RSIHub*: Standardized 6-stage operator loop (`Select -> Mutate -> Evaluate -> Gate -> Lineage -> Reflect`) with frozen evaluator boundaries.
  - *exoharness/exo & OpenEvolve*: Highlighted sandbox requirements for patch mutation isolation and empirical regression prevention.
  - *DGM & Agentic Context Engineering (ACE)*: Emphasized structured invariant checks and append-only strategy provenance to avert cognitive degradation under context evolution.

- **2026-09-04 / 2026-09-05 Tracking**:
  - *simple-agent-lab/RSIHub*: Restructured loop phases (`Select` through `Reflect`) and bilingual specification. Evaluator remains strictly out-of-process.
  - *mindsdb/anton*: Self-improving coworker agent integrating Hermes-style skill accretion and runtime state logging.
  - *Continual-Intelligence/SEAL*: Parameterized continual adaptation benchmarks for long-horizon task learning.
