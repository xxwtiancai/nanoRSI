# Memory and context

[← Research map](README.md)

## Mechanism families

| Family | Records |
| --- | ---: |
| [Structured knowledge bases & graphs](#family-structured-knowledge) | 6 |
| [Experience accumulation & replay](#family-experience-accumulation) | 6 |
| [Context organization policies](#family-context-policies) | 4 |
| [Exploration-driven memory construction](#family-exploration-memory) | 1 |
| [Memory-evolution studies & benchmarks](#family-memory-evolution-studies) | 2 |

<a id="family-structured-knowledge"></a>

## Structured knowledge bases & graphs (6)

<a id="evoontology-self-evolving"></a>

### EvoOntology: A Self-Evolving Ontology Layer for Data Agents

**2026-09-14** · paper · Direct bounded loop

**Publication date** — arXiv v1: 2026-09-14. Code repository created 2026-09-15.

**Institutional relationship** — All four authors (Meiduo Chong, Shaolei Zhang - corresponding, Ju Fan, Xiaoyong Du) are at the School of Information, Renmin University of China; the code lives under the ruc-datalab organization.

**What changes and how feedback is reused** — The evolving artifact is an ontology layer (schema, content, tool levels) packaged as an MCP server that sits between a data agent and heterogeneous sources. A builder agent first constructs an evidence-grounded initial ontology from workload queries; then a diagnose-attribute-patch-gate loop refines it: trajectory failures are attributed via interaction signatures to exactly one level, a typed candidate patch modifies only that level, and a backbone-conditional paired gate accepts a candidate only when the same backbone on the same validation set with identical decoding and budgets improves by at least tau; rejected patches are logged.

**Author-reported result** — Three benchmarks, four analysis backbones. DDR-Bench trajectory-wise vs ReAct baseline: GPT-5.5 90.9 (+26.7), GPT-5.6-sol 93.5 (+25.0), Claude-Sonnet-5 81.3 (+8.8), Claude-Opus-4.8 92.3 (+19.3) - average +17.8; vs ReAct+Memory 89.5 vs 75.8 (+13.7). Attribution of gains: builder +12.3, evolution loop a further +7.7 on DDR-Bench; on BIRD EX +5.1 then +3.7. Gate ablation costs -11.2 trajectory-wise, attribution -6.3. Honest negatives: InsightBench is saturated (mean +0.7 to +1.6), and cross-backbone transfer of an evolved ontology drops at least 6.6 points.

**Evidence limits** — Evolution is backbone-specific (paired gate conditions acceptance on the same backbone); saturated benchmarks show near-zero gains; paired validation costs extra compute, which the authors offset by claiming total cost about 20% below the baseline; no dedicated limitations section.

**Code / weights / data / license** — Code released under MIT at github.com/ruc-datalab/EvoOntology (repo created 2026-09-15, 7 stars at verification). No weights or data release located; evaluation uses GPT-5.5/5.6-sol and Claude Sonnet-5/Opus-4.8 APIs.

**Possible nanoRSI experiment — not implemented here** — For nanoRSI: treat knowledge artifacts (skill libraries, domain notes) as typed objects with level-restricted edits and a paired same-condition acceptance gate plus a rejected-edit log - the same shape as the evidence ledger, applied to an evolving artifact.

![Figure 2: EvoOntology overview - the builder grounds candidate concepts in heterogeneous sources, exposes the three-layer ontology as tools, and the evolution agent diagnoses, attributes, patches and gates candidates against the parent ontology.](assets/paper-figures/evoontology-self-evolving.png)

**Source figure / official image** — Figure 2: EvoOntology overview - the builder grounds candidate concepts in heterogeneous sources, exposes the three-layer ontology as tools, and the evolution agent diagnoses, attributes, patches and gates candidates against the parent ontology. · Figure 2 · [source](https://arxiv.org/html/2609.15779v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-16.

**Open code / weights / data links** — [Code repository (MIT)](https://github.com/ruc-datalab/EvoOntology)

**Primary sources** — [arXiv abstract](https://arxiv.org/abs/2609.15779) · [Paper v1 (affiliations, Figure 2, Tables, gate details)](https://arxiv.org/html/2609.15779v1) · [Code repository (MIT)](https://github.com/ruc-datalab/EvoOntology)

<a id="se-gos-skill-graph"></a>

### SE-GoS: Self-Evolving Graph-of-Skills for Skill Library at Scale

**2026-09-08** · paper · Direct bounded loop

**Publication date** — arXiv v1: 2026-09-08. No later revision recorded at verification time.

**Institutional relationship** — Paper v1 lists Dawei Fu (Peking University and Tencent), Cheng Jiang (University of Edinburgh), Sitian Qian (Northwestern University), Huainan Wang (Tencent) and Zhongkai Hao (Tsinghua University). Tencent appears as a direct employer of two authors.

**What changes and how feedback is reused** — Training-free evolution of an existing Graph-of-Skills retrieval graph from real execution traces. Three updates merge into one offline round: topology evolution (induce workflow/dependency/avoid edges from co-occurrence, prune never-used skills), Hebbian edge-weight evolution (reinforce frequently co-used paths), and node-description evolution (a single-round 'text gradient' refresh of retrieval-facing descriptions). The retrieval algorithm, the skill contents and the model weights are untouched — only the retrieval state changes with execution, and the same retrieval interface serves the evolved graph.

**Author-reported result** — On SkillsBench across three LLMs, one evolution round lifts average task reward from 52.4% to 59.4% while cutting average input tokens by roughly one third versus loading the full 1,000-skill library. The evolved graph transfers to a disjoint held-out 37-task split with a +5.4-point gain over the static GoS baseline. Gains vary across model families, and multi-round evolution (Table 4, n=174 attempts per round) continues to help with diminishing returns.

**Evidence limits** — Evolution is offline and requires a pool of training-task runs; metrics are averages over scored attempts on one benchmark (SkillsBench); no code release; the cold-start substrate is a fixed 1,000-skill library whose construction the method takes as given.

**Code / weights / data / license** — No code or data release located; paper only. Evaluation uses three commercial LLM APIs named in the paper.

**Possible nanoRSI experiment — not implemented here** — Give nanoRSI a training-free retrieval-upkeep pass: after each evaluation batch, mine run logs for co-used and never-used primitives, adjust the retrieval graph (edges, weights, descriptions) instead of rewriting skill contents, and verify on a held-out task split before adoption.

![Figure 1: SE-GoS — real agent runs produce execution traces that drive topology, edge-weight and node-description updates; the evolved graph keeps the unchanged GoS retrieval interface.](assets/paper-figures/se-gos-skill-graph.png)

**Source figure / official image** — Figure 1: SE-GoS — real agent runs produce execution traces that drive topology, edge-weight and node-description updates; the evolved graph keeps the unchanged GoS retrieval interface. · Figure 1 · [source](https://arxiv.org/html/2609.08228v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-15.

**Open code / weights / data links** — No verified public code/asset link in the audited sources.

**Primary sources** — [arXiv abstract](https://arxiv.org/abs/2609.08228) · [Paper v1 (affiliations, Figure 1, Tables 2-4)](https://arxiv.org/html/2609.08228v1)

<a id="procedural-graphs-google"></a>

### Procedural Graphs: Self-Evolving Execution Structures for LLM Agents

**2026-09-08** · paper · Direct bounded loop

**Publication date** — arXiv v1: 2026-09-08. No later revision recorded at verification time.

**Institutional relationship** — Paper v1 lists first author Yuxing Lu with Google, Georgia Institute of Technology and Peking University; co-authors Yicheng Chen, Shanchan Wu and Sercan O. Arik list Google. Industry-led work with university collaborators.

**What changes and how feedback is reused** — Procedural knowledge is stored as (procedure, relation, procedure) triplets with edge attributes — a Procedural Graph analogous to a knowledge graph for how-to knowledge. At run time the agent localizes its active node, extracts a 2-hop subgraph, and a guidance model turns it into step-level guidance that biases rather than dictates the next action. In offline self-evolution an LLM refiner contrasts failed against successful trajectories and proposes graph edits (add, delete, update); an edit commits only if held-out validation performance is preserved or improved, and rejected edits are kept in a rejected-memory so the refiner stops re-proposing them.

**Author-reported result** — On EnterpriseArena (liquidity management through successive macro crises, Gemini 3.5 Flash), self-evolution Round 1 adds an audit-cash/forecast-runway node lifting validation survival from 0.0% to 45.0%; Round 2 adds note reuse and lifts survival to 80.0% while tool calls fall from 17.23 to 3.08 per month versus the unguided baseline; Rounds 3-6 commit nothing (one candidate fails structural verification) — no-op rounds are reported. Across HotpotQA, MultiChallenge and ALFWorld-style suites the learned graph matches or surpasses hand-designed guidance and memory-based baselines.

**Evidence limits** — The self-evolution case study is single-model (Gemini 3.5 Flash); no code release; matching hand-designed graphs rests on the authors' own baselines; guidance quality inherits the guidance model's limits.

**Code / weights / data / license** — No code or data release located; paper only. Experiments use Gemini 3.5 Flash (commercial API).

**Possible nanoRSI experiment — not implemented here** — Keep a small procedural graph of nanoRSI's own improvement loop (propose, evaluate, commit), let a refiner read failed versus successful episodes, and add an explicit rejected-edit memory so the loop stops re-proposing known-bad changes; gate every edit on the frozen validation score.

![Figure 2: the Procedural Graph framework — a read-and-guide pass online, then offline self-evolution where an LLM refiner's edits commit only on validation improvement and rejected edits are remembered.](assets/paper-figures/procedural-graphs-google.png)

**Source figure / official image** — Figure 2: the Procedural Graph framework — a read-and-guide pass online, then offline self-evolution where an LLM refiner's edits commit only on validation improvement and rejected edits are remembered. · Figure 2 · [source](https://arxiv.org/html/2609.09153v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-15.

**Open code / weights / data links** — No verified public code/asset link in the audited sources.

**Primary sources** — [arXiv abstract](https://arxiv.org/abs/2609.09153) · [Paper v1 (affiliations, Figure 2, Section 5.4)](https://arxiv.org/html/2609.09153v1)

<a id="recuris-memory-evolution"></a>

### Recursive Experiential-Working Memory Evolution for Long-Horizon Agent Harnesses

**2026-08-25** · paper · Direct bounded loop

**Publication date** — arXiv v1: 2026-08-25 (2608.24876; the repository was created the same day). The system is named Recuris in the paper body; the arXiv title carries no prefix.

**Institutional relationship** — Paper: NUS (Zhaochen Yu, Shuicheng Yan), Stanford (Yingcheng Wu, Zhe Zhao), Oxford (Zhenfei Yin, Kaiyuan Chen) and Princeton (Mengdi Wang, Ling Yang).

**What changes and how feedback is reused** — Couples Working Memory (verified task state with pending/done/blocked goals, committed only by checker predicates the observation supports) with Experiential Memory (skills), retrieved by an invocation policy matched to current state - producing structured traces with 64.8% failure localization versus 13.0% for outcome-only. Across tasks, a fixed Meta-Agent localizes failures to exactly one of four components (skills, working-memory spec, invocation policy, checkers), patches only the implicated component, and a fixed validation gate admits patches only if they repair the source task without regressing a held-out dev set. The base LLM and outer procedure stay frozen.

**Author-reported result** — 35 of 37 completed model-benchmark pairs improve. Tau2-Retail: GPT-5.6 Sol 58.3 -> 76.1, Claude Opus 5 72.4 -> 87.9, Doubao-2.0-Pro 58.1 -> 81.4 (+23.3), Granite-4.1-3B 9.7 -> 23.0. SkillFlow (Qwen3.6-27B) 42.2 -> 58.7. Held-out evolution: +9.01 to +17.44 versus the initial memory, and a second round compounds +6.98 - a rare multi-round gain. Honest caveats kept: Terminal-Bench 2.1 adaptation effect +2.3 at p=0.774 ('a direction rather than an effect'), and 13 runs admitted no patch.

**Evidence limits** — No dedicated limitations section, but the paper keeps its own noise disclosures (zero-including intervals on tau2-Airline; horizon analysis is a stratified re-analysis; memory evolved on one mid-sized deployment model; transfer fails where held-out tasks lack repairable failure types).

**Code / weights / data / license** — Code at github.com/Gen-Verse/Recuris (Apache-2.0, 205 stars at verification).

**Possible nanoRSI experiment — not implemented here** — For nanoRSI: the four-component localization (skills / memory spec / retrieval policy / checkers) plus repair-without-regression gates is a concrete blueprint for attributing a failure to exactly one editable surface before proposing a patch.

![Figure 3: Recuris - within-task, working memory drives a skill-invocation policy with checker-committed state; across tasks, a fixed Meta-Agent patches one implicated component at a time behind a validation gate.](assets/paper-figures/recuris-memory-evolution.png)

**Source figure / official image** — Figure 3: Recuris - within-task, working memory drives a skill-invocation policy with checker-committed state; across tasks, a fixed Meta-Agent patches one implicated component at a time behind a validation gate. · Figure 3 · [source](https://arxiv.org/html/2608.24876v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-17.

**Open code / weights / data links** — [Code repository (Apache-2.0)](https://github.com/Gen-Verse/Recuris)

**Primary sources** — [arXiv abstract](https://arxiv.org/abs/2608.24876) · [Paper v1 (affiliations, Figure 3, tables)](https://arxiv.org/html/2608.24876v1) · [Code repository (Apache-2.0)](https://github.com/Gen-Verse/Recuris)

<a id="xskill-dual-stream"></a>

### XSkill: Continual Learning from Experience and Skills in Multimodal Agents

**2026-03-12** · paper · Direct bounded loop

**Publication date** — arXiv v1: 2026-03-12; v3: 2026-07-01 (ICML 2026; numbers cited from v3).

**Institutional relationship** — Paper v3: HKUST (Guanyu Jiang also Zhejiang; Zhaochen Su; Yi R. Fung corresponding) with Huazhong University of Science and Technology.

**What changes and how feedback is reused** — Training-free continual learning for multimodal agents via dual-stream knowledge: task-level Markdown skills with reusable tool templates, and short condition-action experience items (capped at 120, embedded for retrieval). Extraction is visually grounded (records what visual evidence motivated each action) and a cross-rollout critique contrasts successful vs failed trajectories to emit add/modify operations; at test time subtasks retrieve top-3 items per stream, adapt them to the current images, and inject non-prescriptively. Usage history feeds back for continual refinement.

**Author-reported result** — Four multimodal benchmarks x four backbones: +2.58 to +6.71 average@4 over the tool-only baseline; up to +11.13 over the strongest baseline (TIR-Bench, Gemini-3-Flash: 47.75 vs Agent-KB 36.62); execution errors fall from 29.9% to 15.3%. Ablations: without experience -3.04, without skill -3.85, without experience manager -4.09. Knowledge transferred from Gemini-3-Flash also lifts GPT-5-mini (20.61 -> 23.19).

**Evidence limits** — Only a single accumulation-then-test cycle demonstrated (iterative refinement architecturally supported but untested); transferred knowledge hurt Qwen models' average@4 (Qwen3-VL-235B 11.80 -> 11.52), so base-model capability is critical; authors flag bias propagation through the loop and recommend human oversight.

**Code / weights / data / license** — Code at github.com/XSkill-Agent/XSkill (268 stars, no license file at verification); project page xskill-agent.github.io.

**Possible nanoRSI experiment — not implemented here** — For nanoRSI: separate task-level skills from short condition-action experiences with different caps and retrieval, and record the visual/textual evidence that motivated each action so critiques can contrast grounded causes rather than raw logs.

![Figure 2: XSkill - Phase I distills skill documents and experience items from multi-path visually grounded trajectories via rollout summary and cross-rollout critique; Phase II retrieves, adapts and injects both streams at test time.](assets/paper-figures/xskill-dual-stream.png)

**Source figure / official image** — Figure 2: XSkill - Phase I distills skill documents and experience items from multi-path visually grounded trajectories via rollout summary and cross-rollout critique; Phase II retrieves, adapts and injects both streams at test time. · Figure 2 · [source](https://arxiv.org/html/2603.12056v3)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-17.

**Open code / weights / data links** — [Code repository](https://github.com/XSkill-Agent/XSkill)

**Primary sources** — [arXiv abstract](https://arxiv.org/abs/2603.12056) · [Paper v3 (affiliations, Figure 2, tables)](https://arxiv.org/html/2603.12056v3) · [Code repository](https://github.com/XSkill-Agent/XSkill)

<a id="memskill-memory-skills"></a>

### MemSkill: Learning and Evolving Memory Skills for Self-Evolving Agents

**2026-02-02** · paper · Direct bounded loop

**Publication date** — arXiv v1: 2026-02-02; v2: 2026-05-24 (numbers cited from v2).

**Institutional relationship** — Paper v2: NTU Singapore (Haozhen Zhang, Quanyu Long, Jianzhu Bao, Wenya Wang corresponding) with UIUC (Tao Feng), UIC (Weizhi Zhang) and Tsinghua (Haodong Yue).

**What changes and how feedback is reused** — Memory-extraction operations become learnable 'memory skills' in two intertwined loops. Skill selection/usage: a lightweight controller (MLPs over state-skill embeddings, Gumbel-Top-K sampling) picks a Top-K skill subset per text span; an LLM executor applies them to update the trace-specific memory bank; the controller trains with PPO on downstream query performance. Skill evolution: a sliding hard-case buffer logs query-centric failures; every 100 steps a designer LLM clusters hard cases and refines/adds skills (max 3 edits/round) with snapshot rollback, early stopping and exploration bias toward new skills.

**Author-reported result** — LoCoMo (LLaMA3.3-70B): F1 44.21 / L-J 53.82 vs MemoryOS 41.39 and A-MEM 49.71; transfers to LongMemEval (L-J 60.89) and HotpotQA (best at all 50/100/200-doc settings); ALFWorld seen/unseen 77.14/83.58 SR (avg 80.36) beating Mem0 and CoN; AppWorld 26.71% vs AWM 25.42%. Ablations: without controller -5.4 L-J, without skill descriptions -17.7 (Qwen). Cost: 215 LLM calls vs MemoryOS 1,288 and A-MEM 1,548.

**Evidence limits** — Limitations live in Appendix F (not rendered in the HTML audit); LongMemEval and Qwen rows are transfer-only (trained on LoCoMo with LLaMA); skill-evolution preparation cost is amortized rather than free.

**Code / weights / data / license** — Code at github.com/ViktorAxelsen/MemSkill (Apache-2.0, 576 stars at verification); project page viktoraxelsen.github.io/MemSkill. Paper CC BY 4.0.

**Possible nanoRSI experiment — not implemented here** — For nanoRSI: evolve the memory-writing operations themselves (not just memory content), and gate designer edits with snapshot rollback + early stopping - the same controls as the skill track, one layer up.

![Figure 2: MemSkill architecture - the controller selects a Top-K subset of memory skills from a shared bank, the executor applies them span by span, task rewards train the controller, and failures feed a designer-driven skill-evolution loop.](assets/paper-figures/memskill-memory-skills.png)

**Source figure / official image** — Figure 2: MemSkill architecture - the controller selects a Top-K subset of memory skills from a shared bank, the executor applies them span by span, task rewards train the controller, and failures feed a designer-driven skill-evolution loop. · Figure 2 · [source](https://arxiv.org/html/2602.02474v2)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-16.

**Open code / weights / data links** — [Code repository (Apache-2.0)](https://github.com/ViktorAxelsen/MemSkill)

**Primary sources** — [arXiv abstract](https://arxiv.org/abs/2602.02474) · [Paper v2 (affiliations, Figure 2, tables)](https://arxiv.org/html/2602.02474v2) · [Code repository (Apache-2.0)](https://github.com/ViktorAxelsen/MemSkill)

<a id="family-experience-accumulation"></a>

## Experience accumulation & replay (6)

<a id="echopath-replayable-memory"></a>

### EchoPath: Execution-Level Replayable Memory for GUI Agents

**2026-09-15** · paper · Direct bounded loop

**Publication date** — arXiv v1: 2026-09-15 (2609.16635), verified on the abs page.

**Institutional relationship** — Paper: Johns Hopkins University (Department of Applied Mathematics and Statistics) and Amazon AGI.

**What changes and how feedback is reused** — Artifact-validated GUI trajectories are compiled into standardized, parameter-controlled callable memories (task-intent keys, preconditions, parameters, GUI evidence, validation provenance, lifecycle state). An image-based target-reaiming algorithm re-matches stored GUI targets against the current screen and corrects coordinates before replay, rebinding only declared modifiable inputs. Lifecycle states (candidate, active, quarantined, repaired branch, merged, deprecated) gate what retrieval can expose.

**Author-reported result** — OSWorld-Verified with a paired two-pass design (second pass replays at a changed resolution): replay preserves success — Codex 145/159 (91.2%), Claude 92.8%, Kimi 87.3%, comparable to the Synapse planning-augmentation baseline (91.8%). Second-pass median cost: 20,370 tokens and 127.5 seconds vs Synapse 586,386 tokens and 315.7 seconds (median token cost down more than 90%, execution time down about 60%); first-pass construction costs about 572K tokens and 4.5 minutes.

**Evidence limits** — Best suited to stable environments: visual re-aiming stays vulnerable to toolbar rearrangement, localization, responsive layouts, display scaling and near-duplicate UI elements; live robustness under interface drift is not established, and memory acquisition requires a full autonomous first pass rather than user demonstration.

**Code / weights / data / license** — Paper lists github.com/JackZhao1998/EchoPath; the URL did not resolve at verification.

**Possible nanoRSI experiment — not implemented here** — For nanoRSI: store execution-level skills as callable memories carrying their own validation provenance and lifecycle state, and expose only active ones to retrieval — replay then buys most of the win at a tenth of the tokens.

![EchoPath framework: validated trajectories become parameter-controlled callable memories with validation provenance and lifecycle states, re-aimed to the current screen before replay.](assets/paper-figures/echopath-replayable-memory.png)

**Source figure / official image** — EchoPath framework: validated trajectories become parameter-controlled callable memories with validation provenance and lifecycle states, re-aimed to the current screen before replay. · Figure 1 (S2.F1) · [source](https://arxiv.org/html/2609.16635v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-17.

**Open code / weights / data links** — No verified public code/asset link in the audited sources.

**Primary sources** — [arXiv abstract](https://arxiv.org/abs/2609.16635) · [arXiv HTML v1](https://arxiv.org/html/2609.16635v1)

<a id="bytedance-chain-of-experience"></a>

### Chain-of-Experience for Continual LLM Improvement

**2026-08-18** · paper · Direct bounded loop

**Publication date** — arXiv v1: August 18, 2026; the same paper is listed on ByteDance Seed's official publications page dated 2026.08.18.

**Institutional relationship** — Authors from UC Santa Cruz and ByteDance Seed (Haoqin Tu and Yunhao Fang equal contribution; senior authors Cihang Xie and Shen Yan).

**What changes and how feedback is reused** — Test-time experiential learning: instead of single-shot inference, the model iteratively solves tasks while accumulating its own experience traces (queries, attempts, correctness or test-pass feedback); those traces feed subsequent attempts, forming a Chain-of-Experience. The study compares feedback sources (self-feedback vs. environment feedback), channel combinations, and retention strategies including deliberately keeping 'messy' failed traces.

**Author-reported result** — Across eight LLMs (including GPT-5, Gemini-2.5 Pro, Claude-4.5 Sonnet) on math, coding and knowledge tasks, iterative experience beats feedback-free baselines with a 5.6% overall gain at 19% lower API cost; combining complementary feedback channels adds gains, accuracy-per-token exceeds other test-time methods, and results are robust to weak or spurious feedback.

**Evidence limits** — Gains are bounded test-time adaptation on fixed models: no weight updates, and the paper's own framing (per ByteDance's page) is 'continual improvement beyond zero-shot inference', not cross-task transfer of a learned updater. Percentages are the authors' aggregate over their benchmark suite.

**Code / weights / data / license** — arXiv (CC BY 4.0); listed on ByteDance Seed's official publications page. No code or data release is linked in the audited sources; benchmark prompts and traces are not published per the checked pages.

**Possible nanoRSI experiment — not implemented here** — Proposed: on nanoRSI's digits/programming tasks, compare single-channel execution feedback against combined self+environment feedback channels under a fixed token budget, and test whether retaining failed traces (not only successes) changes held-out accuracy.

![Figure 2: the study's progression from iterative improvement with world feedback to iterative evolution and finally experience-based loops where the model learns from accumulated experience while the environment provides varied feedback.](assets/paper-figures/bytedance-chain-of-experience.png)

**Source figure / official image** — Figure 2: the study's progression from iterative improvement with world feedback to iterative evolution and finally experience-based loops where the model learns from accumulated experience while the environment provides varied feedback. · Figure 2 · [source](https://arxiv.org/html/2608.18027v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-14.

**Open code / weights / data links** — No verified public code/asset link in the audited sources.

**Primary sources** — [arXiv abstract (v1 date, license)](https://arxiv.org/abs/2608.18027) · [Paper HTML (loop figures, results)](https://arxiv.org/html/2608.18027v1) · [ByteDance Seed official publications page (2026.08.18)](https://seed.bytedance.com/zh/public_papers)

<a id="prime-agent"></a>

### Prime Agent: A Self-Improving RLM Harness

**2026-08-05** · paper · Direct bounded loop

**Publication date** — The paper explicitly says first published August 5, 2026; arXiv v1 was submitted August 24. The launch blog confirms August 5.

**Institutional relationship** — Prime Intellect releases the harness; the paper lists Prime Intellect, Princeton and MIT affiliations.

**What changes and how feedback is reused** — Trajectory-triggered refinement edits durable supplemental prompts, skills, memories and subagent specifications. Disk-backed updates and rollback history enable reuse across trajectories; the base system prompt remains immutable.

**Author-reported result** — A seven-day Sonnet 5 Factorio run completed 24/196 technologies with 23.4 million output tokens. There is no matched no-refinement comparator for this case study. Separate harness benchmark gains should not be attributed solely to refinement.

**Evidence limits** — Another Factorio trace persisted resource-spawning cheats as skills. Persistent change can amplify specification exploits; neither case proves improving learning algorithms.

**Code / weights / data / license** — Official code verified, MIT. No new model weights are required; complete evaluation traces/data and separate licensing were not audited.

**Possible nanoRSI experiment — not implemented here** — Proposed: separate immutable evaluator/base policy from versioned memory updates, with provenance and rollback.

![Figure 1: Prime Agent connects persistent root and subagent sessions to a daemon and continual refinement loop.](assets/paper-figures/prime-agent-figure.png)

**Source figure / official image** — Figure 1: Prime Agent connects persistent root and subagent sessions to a daemon and continual refinement loop. · Figure 1, PDF p.3 · [source](https://arxiv.org/html/2608.23552v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-18.

**Open code / weights / data links** — [Official code and license](https://github.com/PrimeIntellect-ai/prime-agent)

**Primary sources** — [arXiv record](https://arxiv.org/abs/2608.23552) · [Paper first-publication statement and Factorio evidence](https://arxiv.org/html/2608.23552v1) · [Official launch and update mechanism](https://www.primeintellect.ai/blog/prime-agent) · [Official code and license](https://github.com/PrimeIntellect-ai/prime-agent)

<a id="atlas-pamphlets"></a>

### Continual Learning, Not Training: Online Adaptation for Agents

**2025-11-02** · paper · Direct bounded loop

**Publication date** — arXiv v1: 2025-11-02. The SDK repository was created 2025-09-30. The system is named ATLAS in the paper body; the arXiv title carries no prefix.

**Institutional relationship** — Paper: Aman Jaglan and Jarrod Barnes (corresponding) at Arc Intelligence; the evaluation uses Microsoft's ExCyTIn-Bench but the work is not a Microsoft affiliation.

**What changes and how feedback is reused** — Gradient-free inference-time adaptation via dual agents: a Teacher (GPT-5) reviews the Student's (GPT-5-mini) trajectories and gives principle-level corrections; an orchestrator stores traces, guidance and ensemble-of-judges reward scores in a Persistent Learning Memory, distilled into Teacher Pamphlets (principles, failure modes, stop conditions) and Student Pamphlets (action schemas, tool plans, guards) retrieved by task context to adjust supervision level and seed plans - no weight updates anywhere.

**Author-reported result** — ExCyTIn-Bench Incident #5 (n=98): ATLAS 54.1% success vs GPT-5 (High) 48.0% (+6.1) at ~86% lower cost ($0.024 vs $0.174 per question), with tokens cut 45% versus the Student baseline; frozen pamphlets lift a new incident from 28% to 41% (+46% relative) while cutting non-reasoning tokens 52.1%.

**Evidence limits** — Single-benchmark evaluation (one incident, n=98); one baseline's tokens logged on only 42/47 runs; generalization tested on exactly one other incident; world-model training is a hypothesis, not validated; the authors themselves note static benchmarks are insufficient and evaluation hacking remains a risk.

**Code / weights / data / license** — Code at github.com/Arc-Computer/atlas-sdk (17 stars, no license file detected at verification); paper states CC BY 4.0 release with traces and pamphlets.

**Possible nanoRSI experiment — not implemented here** — For nanoRSI: two-tier distilled guidance (principle-level for the critic, schema-level for the executor) with supervision-level control is a lightweight alternative to monolithic memory - and pamphlets freeze cleanly for transfer tests.

![Figure 1: ATLAS architecture - an orchestrator manages Teacher-Student interactions during execution; learning is stored in Persistent Learning Memory and distilled into Teacher and Student pamphlets that guide future inference-time decisions.](assets/paper-figures/atlas-pamphlets.png)

**Source figure / official image** — Figure 1: ATLAS architecture - an orchestrator manages Teacher-Student interactions during execution; learning is stored in Persistent Learning Memory and distilled into Teacher and Student pamphlets that guide future inference-time decisions. · Figure 1 · [source](https://arxiv.org/html/2511.01093v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-17.

**Open code / weights / data links** — [Code repository](https://github.com/Arc-Computer/atlas-sdk)

**Primary sources** — [arXiv abstract](https://arxiv.org/abs/2511.01093) · [Paper v1 (affiliations, Figure 1, results)](https://arxiv.org/html/2511.01093v1) · [Code repository](https://github.com/Arc-Computer/atlas-sdk)

<a id="tencent-training-free-grpo"></a>

### Training-Free Group Relative Policy Optimization

**2025-10-09** · paper · Direct bounded loop

**Publication date** — arXiv v1 submitted 2025-10-09. The corresponding Youtu-Agent branch was announced in October 2025 and later integrated into the main repository; the paper date anchors inclusion.

**Institutional relationship** — The paper lists Tencent Youtu Lab, Fudan University and Xiamen University. The official implementation is released in TencentCloudADP/youtu-agent.

**What changes and how feedback is reused** — A frozen base model produces grouped rollouts. Semantic advantages are distilled into an evolving experience library and token prior, which are fed back through context rather than gradient updates. Multiple epochs share the accumulated experience, shifting later output distributions while keeping parameters fixed.

**Author-reported result** — With DeepSeek-V3.1-Terminus, direct prompting improves AIME24 from 68.6 to 72.6 (+4.0) and AIME25 from 52.9 to 54.0 (+1.1); ReAct+CI improves AIME24 80.0→82.7 (+2.7) and AIME25 67.9→73.3 (+5.4) at a reported $18 cost. WebWalkerQA rises 63.2→67.8 (+4.6) in the paper setting.

**Evidence limits** — This is context-space experience evolution, not parameter training: the base model remains frozen and the experience library is the mutable artifact. Results use bounded groups, retries and task-specific prompts; the paper does not show an autonomous improver redesigning its own algorithm.

**Code / weights / data / license** — TencentCloudADP/youtu-agent publishes the training_free_GRPO branch and examples; its LICENSE states MIT, while GitHub API metadata reports NOASSERTION. The paper’s base models and benchmark data retain their own terms; no parameter update should be inferred from the release.

**Possible nanoRSI experiment — not implemented here** — Add a frozen-model control to nanoRSI memory experiments: compare no experience, a fixed library and recursively refreshed experience at equal group counts, while logging token cost, stale advice and held-out transfer.

![Figure 2: Training-Free GRPO updates an experience library from grouped rollouts while keeping the base model frozen.](assets/paper-figures/tencent-training-free-grpo.png)

**Source figure / official image** — Figure 2: Training-Free GRPO updates an experience library from grouped rollouts while keeping the base model frozen. · Figure 2, training-free_GRPO.png · [source](https://ar5iv.labs.arxiv.org/html/2510.08191/assets/figures/training-free_GRPO.png)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Open code / weights / data links** — [Official Youtu-Agent implementation](https://github.com/TencentCloudADP/youtu-agent/tree/training_free_GRPO) · [Youtu-Agent MIT license](https://github.com/TencentCloudADP/youtu-agent/blob/main/LICENSE)

**Primary sources** — [arXiv first submission and history](https://arxiv.org/abs/2510.08191) · [Paper v1 and Training-Free GRPO figure](https://arxiv.org/html/2510.08191v1) · [Official Youtu-Agent implementation](https://github.com/TencentCloudADP/youtu-agent/tree/training_free_GRPO) · [Youtu-Agent MIT license](https://github.com/TencentCloudADP/youtu-agent/blob/main/LICENSE)

<a id="se-agent-trajectory"></a>

### SE-Agent: Self-Evolution Trajectory Optimization in Multi-Step Reasoning with LLM-Based Agents

**2025-08-04** · paper · Direct bounded loop

**Publication date** — arXiv v1: 2025-08-04 (before the 2025-09-16 window start, so the record sits in the renderer's archive section); v6: 2025-11-03. The abs page lists no venue; a NeurIPS 2025 poster appearance is claimed in third-party listings and was not confirmed on arXiv at verification.

**Institutional relationship** — Paper v6: a fourteen-author list including Daxin Jiang (StepFun) and academic co-authors; the abstract page does not render affiliations, so the organization field reflects the tracked lead (StepFun-led with academic partners) and should be re-verified from the PDF before any strong claim.

**What changes and how feedback is reused** — Trajectory-level self-evolution: the agent iteratively revisits its earlier solution trajectories through three operations - revision, recombination and refinement - exploiting cross-trajectory inspiration that per-step search (MCTS-style) misses, expanding the search space beyond local optima and persisting improved strategies for later problems.

**Author-reported result** — SWE-bench Verified across five LLMs: up to 55% relative improvement and state-of-the-art among open-source agents at v6 (abstract-level claim; per-baseline numbers not on the abstract page).

**Evidence limits** — Headline numbers are abstract-level in this audit (per-baseline tables not re-verified from HTML); the v1-first-public date predates the rolling window, so this entry is archival context rather than in-window evidence.

**Code / weights / data / license** — Code at github.com/JARVIS-Xs/SE-Agent.

**Possible nanoRSI experiment — not implemented here** — For nanoRSI: revision/recombination/refinement over stored trajectories is a cheap second use of the run archive - before generating new candidates, mine cross-trajectory recombinations of past attempts.

![Figure 1: SE-Agent - multi-step reasoning trajectories are revisited via revision, recombination and refinement, with improved strategies persisted across problems.](assets/paper-figures/se-agent-trajectory.png)

**Source figure / official image** — Figure 1: SE-Agent - multi-step reasoning trajectories are revisited via revision, recombination and refinement, with improved strategies persisted across problems. · Figure 1 · [source](https://arxiv.org/html/2508.02085v6)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-17.

**Open code / weights / data links** — [Code repository](https://github.com/JARVIS-Xs/SE-Agent)

**Primary sources** — [arXiv abstract](https://arxiv.org/abs/2508.02085) · [Paper v6 (Figure 1, mechanism)](https://arxiv.org/html/2508.02085v6) · [Code repository](https://github.com/JARVIS-Xs/SE-Agent)

<a id="family-context-policies"></a>

## Context organization policies (4)

<a id="repoatlas-evolving-views"></a>

### RepoAtlas: Guiding Coding Agents via Evolving Multimodal Repository Views

**2026-09-15** · paper · Enabling technique / evaluation

**Publication date** — v1 2026-09-15; the paper's own affiliation block reads '1 Beihang University 2 Independent Researcher' (corresponding author chenyan2022@buaa.edu.cn).

**Institutional relationship** — Academic (Beihang-led); no company affiliation shown.

**What changes and how feedback is reused** — A training-free select-project-refresh loop maintains an evolving repository view over a code graph: issue- and exploration-state-conditioned selection under a fixed node budget, projection into complementary visual and textual representations, and refresh when state changes make the view stale.

**Author-reported result** — SWE-bench Verified: +2.4 points resolve rate over the strongest multimodal graph baseline with 5.8% fewer input tokens and 7.8% fewer model calls, consistent across three model families (Qwen3.6-35B-A3B, MiMo-V2.5, Kimi-K2.5); under a matched 15-node budget, selection improves LocBench FA@3 from 0.256 to 0.336.

**Evidence limits** — Gains are over graph-interface baselines rather than the strongest overall agents; the evolving artifact is the repository view, not the agent itself.

**Code / weights / data / license** — arXiv paper public; code not verified at last check.

**Possible nanoRSI experiment — not implemented here** — Give nanoRSI skills a per-skill 'view' — a file whitelist refreshed on drift — instead of full-tree context; the refresh trigger plays the role of the contract guard for context.

![RepoAtlas overview: select a connected, issue- and state-conditioned structure under fixed budgets, project it into phase-appropriate views, reuse or refresh as exploration proceeds.](assets/paper-figures/repoatlas-evolving-views.png)

**Source figure / official image** — RepoAtlas overview: select a connected, issue- and state-conditioned structure under fixed budgets, project it into phase-appropriate views, reuse or refresh as exploration proceeds. · Figure 2 (fig_overview.png) · [source](https://arxiv.org/html/2609.16936v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-18.

**Open code / weights / data links** — No verified public code/asset link in the audited sources.

**Primary sources** — [arXiv abstract](https://arxiv.org/abs/2609.16936) · [Paper HTML (affiliations, Figure 2, selection ablation)](https://arxiv.org/html/2609.16936v1)

<a id="sambanova-stanford-ace"></a>

### Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models

**2025-10-06** · paper · Direct bounded loop

**Publication date** — arXiv v1: October 6, 2025. Repository announcement says November 2025; paper revisions extend into March 2026.

**Institutional relationship** — The paper explicitly affiliates authors with Stanford, SambaNova and Berkeley; this is a joint contribution, not solely a SambaNova invention.

**What changes and how feedback is reused** — Generator traces and execution feedback feed a Reflector; a Curator produces localized playbook deltas. Helpful/harmful counters and deduplication preserve reusable strategies across episodes without weight updates.

**Author-reported result** — With non-thinking DeepSeek-V3.1 in all roles, AppWorld online ACE without ground-truth labels averages 59.5 versus ReAct 42.4 and Dynamic Cheatsheet 51.9 across four TGC/SGC scores. These are percentage-point differences, not relative percentages.

**Evidence limits** — Online evaluation predicts then updates on sequential test tasks. Evidence is bounded adaptation; no weight learning or proof that the updater improves itself.

**Code / weights / data / license** — Official implementation and evaluation code verified; Apache-2.0. No new weights; third-party datasets retain separate terms. Full data redistribution not audited.

**Possible nanoRSI experiment — not implemented here** — Proposed: compare versioned delta memories against whole-file rewrites on a fixed task stream.

![Figure 4: ACE Generator, Reflector and Curator architecture for evolving context playbooks.](assets/paper-figures/sambanova-stanford-ace.png)

**Source figure / official image** — Figure 4: ACE Generator, Reflector and Curator architecture for evolving context playbooks. · Figure 4 · [source](https://arxiv.org/html/2510.04618v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Open code / weights / data links** — [Official implementation](https://github.com/ace-agent/ace)

**Primary sources** — [arXiv dates](https://arxiv.org/abs/2510.04618) · [Original paper affiliations, protocol and Table 1](https://arxiv.org/html/2510.04618v1) · [Official implementation](https://github.com/ace-agent/ace)

<a id="microsoft-legomem-2025"></a>

### LEGOMem: Modular Procedural Memory for Multi-agent LLM Systems for Workflow Automation

**2025-10-06** · paper · Enabling technique / evaluation

**Publication date** — First arXiv paper: 2025-10-06. Microsoft's AAMAS 2026/January 2026 listing is later, not first publication.

**Institutional relationship** — Microsoft Research's official publication listing establishes institutional attribution.

**What changes and how feedback is reused** — Successful logs become full-task planning memories and role-specific subtask memories, retrieved for subsequent tasks. Experiments build memory offline then evaluate inference; they do not test continual online memory evolution.

**Author-reported result** — OfficeBench, 148 training/152 test tasks, three seeds: GPT-4o success 58.44% versus 45.83% without memory; GPT-4o-mini 38.16% versus 24.78%. Synapse scores 58.11% with GPT-4o, so the strong-baseline margin there is small.

**Evidence limits** — Supports procedure-memory reuse, not demonstrated repeated recursive self-improvement; curated memory and external model dependence matter.

**Code / weights / data / license** — Paper verified. Dedicated official code, weights, memory-bank data and corresponding licences were not identified in opened sources or targeted search; availability remains unverified.

**Possible nanoRSI experiment — not implemented here** — Proposed: compare success-filtered procedure memory against no memory, separating planner/subtask retrieval and freezing test memory.

![Figure 1: LEGOMem orchestrator, task agents and modular procedural memories.](assets/paper-figures/microsoft-legomem-2025.png)

**Source figure / official image** — Figure 1: LEGOMem orchestrator, task agents and modular procedural memories. · Figure 1 · [source](https://arxiv.org/html/2510.04851v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Open code / weights / data links** — No verified public code/asset link in the audited sources.

**Primary sources** — [Paper history](https://arxiv.org/abs/2510.04851) · [Paper v1, method and Table 1](https://arxiv.org/html/2510.04851v1) · [Microsoft Research publication](https://www.microsoft.com/en-us/research/publication/legomem-modular-procedural-memory-for-multi-agent-llm-systems-for-workflow-automation/)

<a id="microsoft-acon-2025"></a>

### ACON: Optimizing Context Compression for Long-horizon LLM Agents

**2025-10-01** · paper · Direct bounded loop

**Publication date** — First paper: 2025-10-01; revisions: 2025-10-17 and 2026-06-01. Metrics use v1.

**Institutional relationship** — Lead author's Microsoft internship and Microsoft/KAIST/Cambridge affiliations are explicit in the paper.

**What changes and how feedback is reused** — LLMs inspect paired successful-full-context/failed-compressed-context trajectories, revise compression guidelines, and evaluate candidate guidelines. Selected guidelines feed subsequent optimization rounds; base-agent weights stay fixed.

**Author-reported result** — OfficeBench with GPT-4.1 agent/compressor: utility-optimized history compression achieves 74.74% accuracy and 4.93k peak tokens, versus 76.84%/7.27k without compression and 71.58%/4.40k with simple prompting (v1 Table 2).

**Evidence limits** — Finite offline module optimization; the accuracy/token tradeoff is not universal accuracy improvement or a self-rewriting optimizer.

**Code / weights / data / license** — Official code and MIT licence verified, including distillation pipelines. Released distilled weights, dedicated datasets and their licences were not verified; external benchmarks/models have separate terms.

**Possible nanoRSI experiment — not implemented here** — Proposed: optimize compressor prompts from paired failures, retain held-out validation, and track success alongside peak context.

![Figure 3: Compression guideline optimization uses successful versus failed trajectory feedback.](assets/paper-figures/microsoft-acon-2025.png)

**Source figure / official image** — Figure 3: Compression guideline optimization uses successful versus failed trajectory feedback. · Figure 3 · [source](https://arxiv.org/html/2510.00615v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Open code / weights / data links** — [Official Microsoft code](https://github.com/microsoft/acon) · [MIT licence](https://github.com/microsoft/acon/blob/main/LICENSE)

**Primary sources** — [Paper history](https://arxiv.org/abs/2510.00615) · [Paper v1](https://arxiv.org/html/2510.00615v1) · [Official Microsoft code](https://github.com/microsoft/acon) · [MIT licence](https://github.com/microsoft/acon/blob/main/LICENSE)

<a id="family-exploration-memory"></a>

## Exploration-driven memory construction (1)

<a id="rsiagent-autonomous-exploration"></a>

### RSIAgent: Autonomous Exploration for Recursive Self-improvement in New Environments

**2026-09-14** · paper · Direct bounded loop

**Publication date** — arXiv v1: 2026-09-14. Code repository created 2026-09-13, one day before the paper listing.

**Institutional relationship** — Paper v1 lists Aether AI (corresponding author Kun Zhou) and UC San Diego; first author Sibo Zhu's work was done during an Aether AI internship, with coauthors from UCSD and UIC.

**What changes and how feedback is reused** — Training-free multi-agent self-improvement for an unfamiliar environment: curriculum, actor and verifier agents explore with no gold labels. Broad Recursive Self-exploration (BRS) runs parallel curriculum-organized task groups to map the environment and bank per-group experience memories of reusable (action, condition, consequence) causal patterns; Deep Recursive Self-exploration (DRS) then iterates on the target task, with the verifier judging each attempt and successful memories routed back into later rounds. The progressively refined memory is frozen and reused for downstream tasks; no model parameter is updated at any point.

**Author-reported result** — With GLM-5.3 as actor and Kimi-K3 as verifier/curriculum: OSWorld 2.0 partial 78.98 vs GPT-6 Astra's reported 72.60 (+6.38) and binary 42.68; Agents' Last Exam partial 84.82 vs GPT-6 Astra 82.26 (+2.56), binary 50.75 vs GPT-6 Astra's 52.24 (GPT-6 leads). Ablation over four tasks: full RSI 74.54% vs BRS-only 65.52% vs DRS-only 56.50%. Claude Opus 5 is also reported (70.19/34.72 OSWorld).

**Evidence limits** — The authors state substantial test-time compute cost; performance depends on exploration budgets, stopping policies and memory quality; the model-based verifier may misjudge and propagate errors into later memory; components are not fully isolated; experiments run in controlled environments and do not cover unauthorized-access or privacy risks. GPT-6 Astra numbers are cited from its report, not re-run.

**Code / weights / data / license** — Code released under Apache-2.0 at github.com/AetherLabsAI/RSIAgent (repo created 2026-09-13, 143 stars at verification); project page aetherlabsai.github.io/RSIAgent. No weights or data release located.

**Possible nanoRSI experiment — not implemented here** — For nanoRSI: split the improvement budget into a broad mapping phase (many cheap probe tasks banking causal patterns) and a deep exploitation phase on the target task, then freeze the memory before final testing - a two-phase schedule that matches nanoRSI's freeze discipline.

![Figure 2: RSIAgent method overview - broad recursive self-exploration banks per-group experience memories, deep recursive self-exploration refines them on the target task with verifier feedback, and the frozen memory is reused at test time.](assets/paper-figures/rsiagent-autonomous-exploration.png)

**Source figure / official image** — Figure 2: RSIAgent method overview - broad recursive self-exploration banks per-group experience memories, deep recursive self-exploration refines them on the target task with verifier feedback, and the frozen memory is reused at test time. · Figure 2 · [source](https://arxiv.org/html/2609.15364v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-16.

**Open code / weights / data links** — [Code repository (Apache-2.0)](https://github.com/AetherLabsAI/RSIAgent)

**Primary sources** — [arXiv abstract](https://arxiv.org/abs/2609.15364) · [Paper v1 (affiliations, Figure 2, Table 1, limitations)](https://arxiv.org/html/2609.15364v1) · [Code repository (Apache-2.0)](https://github.com/AetherLabsAI/RSIAgent)

<a id="family-memory-evolution-studies"></a>

## Memory-evolution studies & benchmarks (2)

<a id="bytedance-s3gym"></a>

### S3Gym: Can LLMs Turn Self-Testing and Self-Judging into Self-Improvement?

**2026-08-31** · paper · Direct bounded loop

**Publication date** — arXiv v1 submitted 2026-08-31; project announcement is 2026-09-01. Title uses arXiv's searchable S3Gym spelling.

**Institutional relationship** — Paper explicitly lists ByteDance Seed, M-A-P and TokenWave.AI.

**What changes and how feedback is reused** — Agents explore games and self-score decisions, then reuse raw histories, score-conditioned memory summaries, or experience-trained parameters in later episodes. Executable verifier rewards stay benchmark-side during main exploration; stricter disjoint evaluations measure whether the inherited state improves behavior. There is no universal improvement acceptance gate.

**Author-reported result** — Across seven games, blockwise self-judgment quality has near-zero correlation with next strict-evaluation improvement: −0.010 for event agreement and −0.018 for negative calibration error. These are correlations, not percentage gains. Context pathways have task-dependent winners; parameter training can cause negative transfer.

**Evidence limits** — Game-specific bounded evaluation; recognizing success does not ensure useful memory or transferable policies.

**Code / weights / data / license** — Paper/project public; paper CC BY 4.0. Standalone benchmark code, data, trained checkpoints and associated asset licenses were not verified as released.

**Possible nanoRSI experiment — not implemented here** — Proposed nanoRSI skills ablation: compare raw-history, summary-memory and frozen-state runs, with verifier scores hidden from memory construction.

![Figure 2: S3Gym explores experience-driven improvement through history ICL, summary memory and parameter training.](assets/paper-figures/s3gym-figure.png)

**Source figure / official image** — Figure 2: S3Gym explores experience-driven improvement through history ICL, summary memory and parameter training. · Figure 2, PDF p.7 · [source](https://arxiv.org/html/2608.31100v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Open code / weights / data links** — No verified public code/asset link in the audited sources.

**Primary sources** — [arXiv first submission](https://arxiv.org/abs/2608.31100) · [Paper v1 methods and Table 6](https://arxiv.org/html/2608.31100v1) · [Official Self-Developing Agents project](https://self-developing-agents.github.io/)

<a id="evo-memory-remem"></a>

### Evo-Memory: Benchmarking LLM Agent Test-time Learning with Self-Evolving Memory

**2025-11-25** · paper · Enabling technique / evaluation

**Publication date** — arXiv v1: 2025-11-25; v2: 2026-05-18 (numbers cited from v2).

**Institutional relationship** — Paper v2: UIUC (Tianxin Wei et al., Jingrui He) and Google DeepMind (Noveen Sachdeva, Benjamin Coleman, Ed H. Chi, Fernando Pereira et al.); first author's work done at Google DeepMind.

**What changes and how feedback is reused** — A streaming benchmark, not a mechanism: static datasets are restructured into sequential task streams where each step follows search-synthesize-evolve (retrieve from memory, answer, update memory with the correctness signal). Ten datasets span single-turn (MMLU-Pro, GPQA, AIME 24/25, ToolBench) and multi-turn (AlfWorld, BabyAI, ScienceWorld, PDDL); 10+ memory modules compared (Mem0, A-MEM, MemOS, AWM, Dynamic Cheatsheet...) plus new baselines ExpRAG and ReMem (action-think-memory refine).

**Author-reported result** — Self-evolving memory helps consistently, largest in multi-turn settings (Claude 3.7 Sonnet: ReMem 0.78 average success vs History 0.49); gains correlate with within-dataset task similarity (Pearson r=0.717/0.563); Hard->Easy transfer beats Easy->Hard (0.94/0.97 average); storing failed experiences degrades several baselines while ReMem stays robust; simple ExpRAG 'outperforms several more complex designs'; AlfWorld steps fall from 22.6 to 11.5.

**Evidence limits** — Code 'to be released upon acceptance' (not located at verification); correctness-only feedback signals; the benchmark measures memory given a fixed update rule, not joint memory-plus-policy evolution.

**Code / weights / data / license** — No code URL at verification ('will be released under a permissive open-source license upon acceptance'). Paper CC BY 4.0.

**Possible nanoRSI experiment — not implemented here** — For nanoRSI: the Hard->Easy vs Easy->Hard ordering result is an experiment-design rule - curriculum the memory stream from hard tasks first; and 'simple beats complex' (ExpRAG) is a recurring warning before adding memory machinery.

![Figure 2: the ReMem agent on the Evo-Memory stream - test-time evolution where the agent iteratively searches, synthesizes and evolves its memory across sequential tasks.](assets/paper-figures/evo-memory-remem.png)

**Source figure / official image** — Figure 2: the ReMem agent on the Evo-Memory stream - test-time evolution where the agent iteratively searches, synthesizes and evolves its memory across sequential tasks. · Figure 2 · [source](https://arxiv.org/html/2511.20857v2)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-17.

**Open code / weights / data links** — No verified public code/asset link in the audited sources.

**Primary sources** — [arXiv abstract](https://arxiv.org/abs/2511.20857) · [Paper v2 (affiliations, Figure 2, results)](https://arxiv.org/html/2511.20857v2)
