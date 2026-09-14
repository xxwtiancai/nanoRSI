# RSI radar — daily research log

The radar log is the daily heartbeat of nanoRSI's research track: one dated entry per day, newest first, recording newly verified RSI results, catalogue updates, engineering signals and coverage gaps. The structured data lives in [catalog.json](catalog.json); this log indexes it by day. A day with no qualified findings is still logged, with the searched scope and remaining gaps stated explicitly.

Entry format rules live in [FORMAT.md](FORMAT.md). The research map itself is [README.md](README.md) · [中文](README.zh-CN.md).

---

## 2026-09-15

**New entries**
- [persistent-skills-osworld](agent-code.zh-CN.md#persistent-skills-osworld) — UESTC × Zhejiang (arXiv 2609.04869) evolves a persistent, versioned GUI skill library from interaction traces under a frozen-snapshot discipline, beating a configuration-matched empty-library control by +5.7 to +18.6 points across four OSWorld domains while honestly recording "revision churn".
- [skillglow-procedural-families](agent-code.zh-CN.md#skillglow-procedural-families) — NUS × IAIC Singapore (arXiv 2609.02217) clusters per-task skill cards into procedural families, compresses them into de-instantiated priors, and admits a prior only through a verifier-grounded commit gate: +17.2 points over no-skill in 12/12 runs and 73.9%→83.9% on unseen ALFWorld.
- [procedural-graphs-google](memory-context.zh-CN.md#procedural-graphs-google) — Google × Georgia Tech × PKU (arXiv 2609.09153) stores procedural knowledge as a graph whose edits commit only on held-out validation improvement with a rejected-edit memory; on EnterpriseArena self-evolution lifts validation survival 0.0%→80.0% in two rounds and reports its no-op rounds.
- [se-gos-skill-graph](memory-context.zh-CN.md#se-gos-skill-graph) — PKU × Tencent × Edinburgh × Northwestern × Tsinghua (arXiv 2609.08228) evolves only the retrieval graph of a 1,000-skill library from execution traces — topology, Hebbian edge weights, one-round description refresh — lifting SkillsBench reward 52.4%→59.4% at one-third the input tokens.
- [skillevolver-meta-skill](agent-code.zh-CN.md#skillevolver-meta-skill) — Tsinghua × BJTU (arXiv 2605.10500, May 11; surfaced via a media lead, verified today against the original) packages skill self-evolution as a portable meta-skill with a fresh-session overfit audit that catches leakage and silent-bypass skills: 56.8% avg@5 vs 43.6% human-curated on SkillsBench; MIT code.
- [simskill-traffic](agent-code.zh-CN.md#simskill-traffic) — Jilin × Tongji (arXiv 2609.03753) runs a gap-driven Propose→Act→Evaluate→Distill loop over the SUMO traffic simulator into episodic/procedural/semantic memory, up to +25 points verified success with a stated caveat that memory does not help every backbone; Apache-2.0 code.

**Updated entries**
- [salesforce-beagle-darwinx](agent-code.zh-CN.md#salesforce-beagle-darwinx) — added after verifying the Apache-2.0 Beagle repository, DarwinX v1 paper and official architecture figure; the 2026-09-02 release is recorded separately from the 2026-07-31 paper date.

The rolling window advanced to 2025-09-15 → 2026-09-15 with all 46 records retained — tencent-moe-cl (2025-09-14) moved into the renderer's archive section.

**Signals for engineering**
- ByteDance "Seed-Evolving" re-check: seed.bytedance.com/zh/public_papers still ends at Chain-of-Experience (2026.08.18); no official page or paper for the self-evolving model reported by Tencent News on Sept 11 — still a media lead only; re-check next run.
- Four of today's six entries converge on the same control: changes commit only after an independent check (SkillGLoW's verifier-grounded gate, Procedural Graphs' held-out validation, SkillEvolver's fresh-session auditor, SimSkill's action–critic loop) — tracked as ADOPTION items 14–15. Beagle/DarwinX adds a population-level preserve-and-extend selection boundary — tracked as ADOPTION item 18.
- prime-rl shipped v0.9.0 (Aug 25): adaptive concurrency sized from live vLLM pressure plus soft/hard KV-cache caps — an infrastructure signal for running self-improvement populations cheaply, not a new mechanism (supersedes the stale v0.6.0 note).
- hermes-agent v0.21.3 (Sept 14) rolls up ~338 PRs, mostly remote-gateway session reliability — same infrastructure-reliability category as v0.21.0–2.
- EmbodiSkill (NJU × Microsoft × Tsinghua AIR, per a May media story alongside SkillEvolver) targets embodied skill-aware reflection; not yet verified against its original paper — candidate for the next sweep.

**Coverage & gaps**
- Searched: arXiv via WebSearch plus direct abs/html opens of seven September skill/self-evolution preprints (the export API was not retried after its Sept 14 rate-limiting; same-day listings may have been missed); ByteDance Seed official publications page; Anthropic research index (Sept 4 Fermat formalization is an autonomous-research capability result, not a self-improvement mechanism; Sept 9–10 items are cybersecurity/eval work); OpenAI news sweep (Sept 10 items are product launches; the Sept 3 GPT-6 Astra rollout is a model release, no RSI mechanism); DeepMind site (WeatherNext 3 and science posts, no RSI); Microsoft/Sakana/domestic-vendor sweeps in English and Chinese (no new RSI announcements); GitHub tracked repos including prime-rl and hermes-agent release notes; Chinese-language media keyword sweeps (no new traceable RSI leads beyond those logged).
- Not covered: dedicated per-lab homepage visits (institutions were reached through paper affiliation pages today: UESTC, ZJU, NUS, IAIC, PKU, Tsinghua, BJTU, Edinburgh, Northwestern, Georgia Tech, Tongji, Jilin); OpenReview/NeurIPS 2026 listings; Nature / Nature Machine Intelligence; Qwen3.8-Max open-weights follow-through; OpenAI pacing-model post deep-read; EmbodiSkill original-paper verification.
- Process note: arXiv HTML figure assets mix PNG and SVG; qlmanage renders SVG for eyeballing but its thumbnail aspect can drift — the catalog keeps the original SVG (skillglow-procedural-families) per established practice.

---

## 2026-09-14

**New entries**
- [genuine-rsi-roadmap-2026](research-workflows.zh-CN.md#genuine-rsi-roadmap-2026) — SJTU/Theseus Labs/Tsinghua-led 37-author roadmap (arXiv 2609.11873) with an HCI headroom diagnostic and an L1–L5 RSI autonomy ladder used to survey industry systems.
- [tokenrhythm-neohorse-1](parameter-learning.zh-CN.md#tokenrhythm-neohorse-1) — NeoHorse-1 (arXiv 2609.08183) turns routing-harness records into a three-stage curriculum, on-policy distillation and capability-guided data allocation, lifting 4B/9B macro-averages 58.94→64.87 / 65.60→69.04; authors flag it as a single pass of the loop.
- [openai-research-acceleration-2026](research-workflows.zh-CN.md#openai-research-acceleration-2026) — OpenAI's official post (Sept 6) declares the fall-2025 "automated research intern" goal met, reports 3.1 agent-workdays per human workday, targets an automated AI researcher by March 2028, and documents an RL-training pause after the Hugging Face incident.
- [bytedance-chain-of-experience](memory-context.zh-CN.md#bytedance-chain-of-experience) — ByteDance Seed × UCSC (arXiv 2608.18027) shows test-time experience accumulation across 8 LLMs gives +5.6% over feedback-free baselines at 19% lower API cost.
- [qwen38-max-self-evolving-harness](agent-code.zh-CN.md#qwen38-max-self-evolving-harness) — Qwen's official Aug 3 blog documents a 10+ day autonomous build of a self-evolving harness (265 commits/127 PRs over ~16 days) and a self-improving research loop that beat a reproduced paper's method by +2.7 AIME24.
- [salesforce-toward-self-improving-agents](research-workflows.zh-CN.md#salesforce-toward-self-improving-agents) — Salesforce AI Labs' position story (July 23) frames the owned improvement loop as the compounding asset and prescribes governed autonomy (simulation proof, regression suites, human gates) against a DGM reward-hacking case.
- [microsoft-skillopt](agent-code.zh-CN.md#microsoft-skillopt) — MSR's SkillOpt (blog June 30, MIT code) treats skill files as trainable text parameters with a strict held-out acceptance gate, +23.5 points average with GPT-5.5 and +59.7 cross-harness transfer.

**Updated entries**
- None; the rolling window advanced to 2025-09-14 → 2026-09-14 with all 39 records retained.

**Signals for engineering**
- ByteDance "Seed-Evolving" (自进化模型，"一次接入，永远最新") was reported by Tencent News on 2026-09-11, but no official Seed page or paper exists yet (seed.bytedance.com/zh/public_papers ends at 2026.08.18) — media lead only until ByteDance publishes; re-check tomorrow.
- hermes-agent shipped v0.21.0→v0.21.2 (Aug 31–Sept 11): 947 commits mostly hardening the session store's state.db — an infrastructure-reliability signal for anyone running persistent self-improving agents, not a new mechanism.
- Two more academic surveys surfaced as leads (not catalogued today to avoid flooding the window): "Self-Improvements in Modern Agentic Systems" (arXiv 2607.13104) and "Recursive Self-Improvement in AI: From Bounded Self-Refinement to Autonomous Research Loops" (arXiv 2607.07663, a 1,250-paper survey); compare their taxonomies against the new genuine-rsi-roadmap-2026 ladder before adopting one.
- Qwen's earlier "Agent Frontier" blog (qwen.ai/blog?id=qwen3.7, rule self-evolution: 13 new heuristic rules, 1,618 flagged hacking cases) was not opened/audited in this run; verify before any catalog use.

**Coverage & gaps**
- Searched: arXiv (WebSearch plus direct abs/html opens; the export API stayed rate-limited at 429 — keyword sweeps may have missed same-day listings); OpenAI news/blog (opened via in-app browser after bot-blocking), Microsoft Research blog, Salesforce News, qwen.ai blog (browser), ByteDance Seed official publications page, Anthropic research index (Sep 9 post is cybersecurity alignment, not RSI), Sakana AI news, Prime Intellect / Nous Research / Cognition sweeps, 机器之心/量子位 September sweeps (no RSI hits), GitHub API checks on all tracked repos (ShinkaEvolve, OpenEvolve, SEAL, DGM, ACE, hermes-agent, OpenRSI) plus the three new repos.
- Not covered: per-lab homepages (Tsinghua NLP, PKU, SJTU, Zhejiang, USTC, Fudan, HKUST, MIT, Stanford, CMU, Berkeley, Oxford, Cambridge, ETH, MPI — institutions were covered only via paper affiliation pages); OpenReview/NeurIPS 2026 listings (decisions not yet public); Nature / Nature Machine Intelligence; DeepSeek, Moonshot, Zhipu, MiniMax, Tencent had no new RSI hits this run (Tencent remains deeply covered; MiniMax's M2.7 entry unchanged); prime-rl 0.6.0 release notes unread.
- Process note: qwen.ai and theseus-labs-rsi.github.io are JS-rendered SPAs — plain HTTP readers see an empty shell; open them in a real browser when auditing.

---

## 2026-09-13

**Radar initialized.** The catalogue holds 32 verified entries across parameter learning, agent/code evolution, memory/context updates and automated research workflows. Starting 2026-09-14, a daily midnight sweep covers arXiv (cs.AI/cs.LG/cs.CL/cs.MA), company research pages, domestic and international university labs, conference and journal outputs, high-star GitHub RSI projects, and authoritative media leads traced back to original sources.

**Coverage & gaps**
- Baseline: 32 entries; deepest current coverage is Tencent, ByteDance Seed, Anthropic Fellows, Google DeepMind and Sakana AI.
- First sweeps should prioritize: recent arXiv self-improvement preprints not yet tied to an organization page; OpenReview revisions for NeurIPS/ICLR; high-star GitHub RSI projects outside the tracked list.
