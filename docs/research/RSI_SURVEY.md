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
| **Darwin Gödel Machine (DGM)** | Harness / Artifact | Meta-learning with empirical verification proof steps before adopting changes | DGM, Gödel Agent | Strict formal verification or empirical test pass gate before self-rewrite |
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

- **2026-09-04 / 2026-09-05 Tracking**:
  - *simple-agent-lab/RSIHub*: Restructured loop phases (`Select` through `Reflect`) and bilingual specification. Evaluator remains strictly out-of-process.
  - *mindsdb/anton*: Self-improving coworker agent integrating Hermes-style skill accretion and runtime state logging.
  - *Continual-Intelligence/SEAL*: Parameterized continual adaptation benchmarks for long-horizon task learning.
