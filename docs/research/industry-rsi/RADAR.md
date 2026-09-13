# RSI radar — daily research log

The radar log is the daily heartbeat of nanoRSI's research track: one dated entry per day, newest first, recording newly verified RSI results, catalogue updates, engineering signals and coverage gaps. The structured data lives in [catalog.json](catalog.json); this log indexes it by day. A day with no qualified findings is still logged, with the searched scope and remaining gaps stated explicitly.

Entry format rules live in [FORMAT.md](FORMAT.md). The research map itself is [README.md](README.md) · [中文](README.zh-CN.md).

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
