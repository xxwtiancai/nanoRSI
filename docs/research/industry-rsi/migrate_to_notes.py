"""Rebuild docs/research/RSI_NOTES.md from the frozen catalogue, or verify sync.

The living research notes live in docs/research/RSI_NOTES.md, organized on the
two axes of the 1,250-paper RSI survey (arXiv 2607.07663). catalog.json is the
frozen 2026-10-24 archive this file was first built from; `--check` verifies
that every archived record remains present while allowing newer, manually
verified notes to be added to the living document.
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOTES = ROOT.parent / "RSI_NOTES.md"

SECTIONS = [
    ("deployment", "1. 部署时自进化 / Deployment-time self-evolution"),
    ("training", "2. 训练时自迭代 / Training-time self-iteration"),
    ("selfeval", "3. 自评估 / Self-evaluation"),
    ("autoresearch", "4. 自动研究 / Auto Research"),
]
# Entries whose mutated artifact is the verifier itself; otherwise the section
# rule below is category+family deterministic.
OVERRIDES = {
    "whoverifies-coevolving-graders": "selfeval",
    "ucoe-verifier-harness-coevolution": "selfeval",
    "tesearch-test-suite-signals": "selfeval",
}
CLOSURE = {"direct-loop": "闭环", "assisted-rd": "人在环上", "enabling": "支撑·无闭环"}
FAMILY_ZH = {
    "self-play-curriculum": "自博弈与课程任务生成",
    "verifier-reward": "验证器与奖励进化",
    "skill-weight-coevolution": "技能-权重共进化",
    "experience-distillation": "经验蒸馏与测试时适应",
    "autonomous-training": "自主训练智能体与数据管线",
    "enabling-adaptation": "支撑性适应机制",
    "skill-file-optimization": "技能文件优化与技能库",
    "harness-search": "Harness 搜索与进化",
    "self-modifying-meta-agents": "自改写元智能体与谱系",
    "program-evolution": "程序进化与进化搜索",
    "feedback-orchestration": "反馈审查与编排",
    "safety-governance": "安全与治理",
    "experience-accumulation": "经验积累与回放",
    "structured-knowledge": "结构化知识库与图",
    "context-policies": "上下文组织策略",
    "exploration-memory": "探索式记忆构建",
    "memory-evolution-studies": "记忆进化评测研究",
    "ai-scientists": "AI 科学家系统",
    "autonomous-post-training": "自主后训练及其评测",
    "company-telemetry": "公司研发遥测",
    "alignment-automation": "对齐自动化",
    "analyses-audits": "分析与审计",
    "positions-labs": "立场、路线图与实验室",
}


def section_of(row):
    if row["id"] in OVERRIDES:
        return OVERRIDES[row["id"]]
    if row["category"] == "parameter-learning":
        return "selfeval" if row["family"] == "verifier-reward" else "training"
    if row["category"] in {"agent-code", "memory-context"}:
        return "deployment"
    return "autoresearch"


def sentences(text, count):
    parts = [p for p in re.split(r"(?<=[。；])", text) if p.strip()]
    return "".join(parts[:count]).strip()


def clip(text, limit=260):
    text = text.strip()
    return text if len(text) <= limit else text[:limit].rstrip() + "……"


def paper_url(row):
    for source in row["sources"]:
        if "arxiv.org/abs" in source["url"]:
            return source["url"]
    return row["sources"][0]["url"]


def note_lines(row):
    orgs = " / ".join(row["organizations"][:4])
    if len(row["organizations"]) > 4:
        orgs += " 等"
    repo = next((s for s in row["sources"] if s["kind"] == "repository"), None)
    figure = f'[原文图](industry-rsi/{row["visual"]["asset"]})'
    links = figure + (f' · [仓库]({repo["url"]})' if repo else "")
    return [
        f'- **[{row["title"]}]({paper_url(row)})**（{orgs}，{row["published"]}，{CLOSURE[row["relationship"]]}）',
        f'  - 核心：{clip(sentences(row["mechanism"]["zh"], 2))}',
        f'  - 数字：{clip(sentences(row["result"]["zh"], 1))}',
        f'  - 代码：{clip(sentences(row["availability"]["zh"], 1))}',
        f'  - 点评：{clip(sentences(row["application"]["zh"], 1))} · {links}',
    ]


def build(data):
    rows = sorted(data["records"], key=lambda r: (r["published"], r["id"]), reverse=True)
    lines = [
        "# RSI 研究笔记（活文档）",
        "",
        "> 分类法来自 1250 篇 RSI 综述（arXiv 2607.07663）的两轴：**改进对象**（下面四个章节）×"
        "**闭环程度**（每条末尾标注：闭环 / 人在环上 / 支撑·无闭环，映射自旧三值证据类 direct-loop / assisted-rd / enabling）。"
        "标题与机构保留原文；正文中文。本文件由每日零点自动化更新；完整字段、事件史与逐条配图清单仍在已冻结的"
        " [industry-rsi 归档](industry-rsi/README.md)（catalog.json，2026-10-24 起不再更新）。",
        "",
        "## 最近更新",
        "",
        f"- 2026-10-24 · 体系切换：按综述两轴把存量 {len(rows)} 条整理论文笔记，此后每日收录直接写入本文件；"
        "industry-rsi 旧体系（catalog/render/分类页/RADAR）冻结归档。",
        "",
    ]
    for key, heading in SECTIONS:
        members = [r for r in rows if section_of(r) == key]
        lines.extend([f"## {heading}（{len(members)} 条）", ""])
        families = {}
        for row in members:
            families.setdefault(row["family"], []).append(row)
        for fam in sorted(families, key=lambda f: (-len(families[f]), f)):
            lines.extend([f"### {FAMILY_ZH.get(fam, fam)}（{len(families[fam])}）", ""])
            for row in families[fam]:
                lines.extend(note_lines(row))
                lines.append("")
        lines.append("")
    lines.extend([
        "## 附录：迁移映射",
        "",
        "- agent-code、memory-context 全部族 → 部署时自进化；parameter-learning 除 verifier-reward 外 → 训练时自迭代；"
        "verifier-reward → 自评估；research-workflows 全部族 → 自动研究。",
        "- 覆写（变异对象是验证器本身的三条）：whoverifies-coevolving-graders、ucoe-verifier-harness-coevolution、"
        "tesearch-test-suite-signals → 自评估。",
        "- 迁移脚本：`industry-rsi/migrate_to_notes.py`（`--check` 校验本文件与冻结 catalog 一致）。",
        "",
    ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    content = build(data)
    if args.check:
        current = NOTES.read_text(encoding="utf-8") if NOTES.exists() else ""
        missing = [row["title"] for row in data["records"] if row["title"] not in current]
        missing_assets = [row["visual"]["asset"] for row in data["records"] if row["visual"]["asset"] not in current]
        if missing or missing_assets:
            details = []
            if missing:
                details.append(f"missing titles: {', '.join(missing[:3])}")
            if missing_assets:
                details.append(f"missing visual references: {', '.join(missing_assets[:3])}")
            raise SystemExit("RSI_NOTES.md is missing frozen catalogue content; rerun the migration: " + "; ".join(details))
        print(f"notes retain frozen catalogue: {len(data['records'])} records; living additions allowed")
    else:
        NOTES.write_text(content, encoding="utf-8")
        print(f"wrote {NOTES} with {len(data['records'])} records")


if __name__ == "__main__":
    main()
