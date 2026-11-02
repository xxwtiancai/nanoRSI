"""Generate the per-paper research notes under docs/research/notes/ from the frozen
catalogue, or verify sync. One Markdown file per paper — full-depth fields from
catalog.json (mechanism / results / limits / nanoRSI input, the paper's own figure
embedded), organised into the four improvement-target sections of the 1,250-paper
RSI survey (arXiv 2607.07663). Papers added after the catalogue froze are hand-written
in the same template and are NOT touched by this generator."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOTES = ROOT.parent / "notes"

SECTIONS = {
    "deployment": "部署时自进化 / Deployment-time self-evolution",
    "training": "训练时自迭代 / Training-time self-iteration",
    "selfeval": "自评估 / Self-evaluation",
    "autoresearch": "自动研究 / Auto Research",
}
CLOSURE = {"direct-loop": "闭环", "assisted-rd": "人在环上", "enabling": "支撑·无闭环"}
OVERRIDES = {
    "whoverifies-coevolving-graders": "selfeval",
    "ucoe-verifier-harness-coevolution": "selfeval",
    "tesearch-test-suite-signals": "selfeval",
}
FAMILY_ZH = {
    "self-play-curriculum": "自博弈与课程任务生成", "verifier-reward": "验证器与奖励进化",
    "skill-weight-coevolution": "技能-权重共进化", "experience-distillation": "经验蒸馏与测试时适应",
    "autonomous-training": "自主训练智能体与数据管线", "enabling-adaptation": "支撑性适应机制",
    "skill-file-optimization": "技能文件优化与技能库", "harness-search": "Harness 搜索与进化",
    "self-modifying-meta-agents": "自改写元智能体与谱系", "program-evolution": "程序进化与进化搜索",
    "feedback-orchestration": "反馈审查与编排", "safety-governance": "安全与治理",
    "experience-accumulation": "经验积累与回放", "structured-knowledge": "结构化知识库与图",
    "context-policies": "上下文组织策略", "exploration-memory": "探索式记忆构建",
    "memory-evolution-studies": "记忆进化评测研究", "ai-scientists": "AI 科学家系统",
    "autonomous-post-training": "自主后训练及其评测", "company-telemetry": "公司研发遥测",
    "alignment-automation": "对齐自动化", "analyses-audits": "分析与审计",
    "positions-labs": "立场、路线图与实验室",
}


def section_of(row: dict) -> str:
    if row["id"] in OVERRIDES:
        return OVERRIDES[row["id"]]
    if row["category"] == "parameter-learning":
        return "selfeval" if row["family"] == "verifier-reward" else "training"
    if row["category"] in {"agent-code", "memory-context"}:
        return "deployment"
    return "autoresearch"


def slug(row: dict) -> str:
    return row["id"]


def paper_url(row: dict) -> str:
    for source in row["sources"]:
        if "arxiv.org/abs" in source["url"]:
            return source["url"]
    return row["sources"][0]["url"]


def repo_of(row: dict):
    return next((s for s in row["sources"] if s["kind"] == "repository"), None)


def sentence(text: str, count: int) -> str:
    parts = [p for p in re.split(r"(?<=[。；])", text) if p.strip()]
    return "".join(parts[:count]).strip()


def figure_md(row: dict) -> tuple[str, str]:
    """Migration papers keep their figures where the frozen archive stored them
    (../../industry-rsi/assets/… from any section dir); hand-written notes use
    notes/assets/."""
    visual = row.get("visual", {})
    asset = visual.get("asset", "")
    return (f"![{visual.get('caption', {}).get('zh', '')}](../../industry-rsi/{asset})\n"
            if asset else ""), visual.get("locator", "")


def paper_md(row: dict) -> str:
    zh = {k: row[k]["zh"] for k in ("mechanism", "result", "limits", "application")}
    orgs = " / ".join(row["organizations"][:5]) + (" 等" if len(row["organizations"]) > 5 else "")
    repo = repo_of(row)
    figure, locator = figure_md(row)
    lines = [
        f"# {row['title']}",
        "",
        f"> {orgs} · {row['published']} · {row['kind']} · **{CLOSURE[row['relationship']]}** · "
        f"[论文]({paper_url(row)})" + (f" · [仓库]({repo['url']})" if repo else ""),
        f"> 机制族：{FAMILY_ZH.get(row['family'], row['family'])} · "
        f"来源核验 {row['last_verified']} · 复现状态 {row['local_reproduction']}",
        "",
        "## Pipeline",
        "",
        figure,
        zh["mechanism"].strip(),
        "",
        f"*图源：{locator}*" if locator else "",
        "## 结果（作者报告，非本地复现）",
        "",
        zh["result"].strip(),
        "",
        "## 证据边界",
        "",
        zh["limits"].strip(),
        "",
        "## 对 nanoRSI 的输入",
        "",
        zh["application"].strip(),
        "",
        "## 来源",
        "",
        " · ".join(f"[{s['label']}]({s['url']})" for s in row["sources"]),
        "",
    ]
    return "\n".join(lines)


def build(catalog: dict) -> dict[str, str]:
    files = {}
    rows = sorted(catalog["records"], key=lambda r: (r["published"], r["id"]), reverse=True)
    counts = {key: 0 for key in SECTIONS}
    for row in rows:
        key = section_of(row)
        counts[key] += 1
        files[f"{key}/{slug(row)}.md"] = paper_md(row)
    return files


def hand_written(generated: dict) -> list[tuple[str, str]]:
    """Papers added after the catalogue froze: title line + path, for the index."""
    found = []
    if NOTES.is_dir():
        for path in sorted(NOTES.glob("*/*.md")):
            rel = path.relative_to(NOTES).as_posix()
            if rel in generated:
                continue
            title = next((l[2:] for l in path.read_text(encoding="utf-8").splitlines() if l.startswith("# ")), rel)
            found.append((rel, title))
    return found


def recent_updates(keep: int = 8) -> tuple[list, list]:
    """Newest daily log lines from updates/<month>.md (the hand-written source of
    truth), plus the month files - so the generated README never blocks daily runs."""
    lines, months = [], []
    if (NOTES / "updates").is_dir():
        for path in sorted((NOTES / "updates").glob("*.md"), reverse=True):
            months.append(path.name)
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.startswith("- ") and re.match(r"- \d{4}-\d{2}-\d{2} . ", line):
                    lines.append(line)
    lines.sort(key=lambda l: l[2:12], reverse=True)
    return lines[:keep], months


def index_md(catalog: dict, rows: list, counts: dict, extra: list) -> str:
    lines = [
        "# RSI 研究笔记",
        "",
        "> 每篇论文一个文件，按 1250 篇 RSI 综述（arXiv 2607.07663）的**改进对象**轴分为四类目录，"
        "**闭环程度**（闭环 / 人在环上 / 支撑·无闭环）标注在每篇元信息行。模板：元信息 → Pipeline（论文主图 + 机制叙述）"
        " → 结果（作者数字）→ 证据边界 → 对 nanoRSI 的输入 → 来源。作者结果 ≠ 本地复现；负结果与边界照录。",
        "",
        f"> 冻结目录（[industry-rsi/](../industry-rsi/)，2026-10-24 起不再更新）迁移生成 {sum(counts.values())} 篇；"
        "此后新增为手写深记。每日更新流水见下。",
        "",
        "## 最近更新",
        "",
]
    updates, months = recent_updates()
    if updates:
        lines += updates
        lines += ["", "全部流水：" + " · ".join(f"[updates/{m}](updates/{m})" for m in months) + "。", ""]
    else:
        lines += ["- （流水见 [updates/](updates/)）", ""]
    lines += [
        "## 分类",
        "",
        "| 分类 | 篇数 | 目录 |",
        "| --- | ---: | --- |",
    ]
    for key, label in SECTIONS.items():
        lines.append(f"| {label} | {counts[key]} | [{key}/]({key}/) |")
    if extra:
        lines += ["", "## 冻结后手写深记", ""]
        lines += [f"- [{title}]({rel})" for rel, title in extra]
    lines += ["", "---", "", "旧流水（拆分前）：见 [updates/2026-10.md](updates/2026-10.md)。", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    files = build(catalog)
    rows = sorted(catalog["records"], key=lambda r: (r["published"], r["id"]), reverse=True)
    counts = {key: 0 for key in SECTIONS}
    for row in catalog["records"]:
        counts[section_of(row)] += 1
    extra = hand_written(files)
    files["README.md"] = index_md(catalog, rows, counts, extra)
    stale = []
    for rel, content in files.items():
        path = NOTES / rel
        if args.check:
            if not path.is_file() or path.read_text(encoding="utf-8") != content:
                stale.append(rel)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if args.check:
        if stale:
            raise SystemExit("generated notes out of sync: " + ", ".join(stale))
        print(f"notes in sync: {len(files) - 1} papers + index")
    else:
        print(f"wrote {len(files) - 1} papers + index under {NOTES}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
