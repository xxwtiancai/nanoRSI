"""Validate the research catalogue and regenerate its bilingual Markdown pages.

Run from any directory. --check is offline and fails on stale generated pages.
This tool checks structure and rendering, not whether a research claim is true.
"""

import argparse
import calendar
from collections import Counter
from datetime import date
import json
from pathlib import Path
import re
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parent
CATEGORIES = {
    "parameter-learning": ("Parameters and training data", "参数与训练数据"),
    "agent-code": ("Agents and code", "Agent 与代码"),
    "memory-context": ("Memory and context", "记忆与上下文"),
    "research-workflows": ("Automated research and evaluation", "自动化研发与评测"),
}
RELATIONS = {
    "direct-loop": ("Direct bounded loop", "直接有界闭环"),
    "enabling": ("Enabling technique / evaluation", "支撑技术／评测"),
    "assisted-rd": ("Automated / assisted R&D", "自动化／辅助研发"),
}
FIELDS = {
    "date_note": ("Publication date", "日期说明"),
    "affiliation": ("Institutional relationship", "机构关系"),
    "mechanism": ("What changes and how feedback is reused", "改变对象与反馈复用"),
    "result": ("Author-reported result", "作者报告结果"),
    "limits": ("Evidence limits", "证据边界"),
    "availability": ("Code / weights / data / license", "代码／权重／数据／许可"),
    "application": ("Possible nanoRSI experiment — not implemented here", "可用于 nanoRSI 的实验方向——本次未实现"),
}


def bounds(value):
    """Preserve month-only precision without inventing a publication day."""
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}(-\d{2})?", value):
        raise ValueError(f"Invalid date: {value!r}")
    if len(value) == 10:
        exact = date.fromisoformat(value)
        return exact, exact
    year, month = map(int, value.split("-"))
    return date(year, month, 1), date(year, month, calendar.monthrange(year, month)[1])


def validate(data):
    if data["schema_version"] != 1:
        raise ValueError("Unsupported schema_version")
    start = date.fromisoformat(data["window_start"])
    end = date.fromisoformat(data["as_of"])
    if start > end:
        raise ValueError("Reversed research window")
    seen = set()
    for row in data["records"]:
        identity = row["id"]
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", identity) or identity in seen:
            raise ValueError(f"Invalid or duplicate id: {identity}")
        seen.add(identity)
        if row["category"] not in CATEGORIES or row["relationship"] not in RELATIONS:
            raise ValueError(f"Unknown classification: {identity}")
        if row["kind"] not in {"paper", "report", "release"}:
            raise ValueError(f"Unknown publication kind: {identity}")
        if not row["title"] or not row["organizations"] or not all(row["organizations"]):
            raise ValueError(f"Missing title or organizations: {identity}")
        low, high = bounds(row["published"])
        if high > end or low < start <= high:
            raise ValueError(f"Future or boundary-ambiguous date: {identity}")
        verified = date.fromisoformat(row["last_verified"])
        if not low <= verified <= end:
            raise ValueError(f"Invalid verification date: {identity}")
        for event in row.get("additional_events", []):
            event_low, event_high = bounds(event["date"])
            if event_low < low or event_high > verified or not event["label"]:
                raise ValueError(f"Invalid subsequent event: {identity}")
            if event["kind"] not in {"paper", "report", "release"}:
                raise ValueError(f"Unknown subsequent event type: {identity}")
        visual = row.get("visual")
        if not isinstance(visual, dict) or visual.get("kind") not in {"paper-figure", "paper-figure-crop", "official-report-figure", "official-project-figure", "official-report-image", "official-report-screenshot", "official-report-screenshot-crop"}:
            raise ValueError(f"Missing visual provenance: {identity}")
        asset = visual.get("asset", "")
        if not re.fullmatch(r"assets/[a-z0-9._/-]+\.(?:png|jpe?g|svg|webp)", asset) or ".." in asset:
            raise ValueError(f"Invalid visual asset path: {identity}")
        if not isinstance(visual.get("source_url"), str) or urlsplit(visual["source_url"]).scheme != "https":
            raise ValueError(f"Invalid visual source: {identity}")
        if not isinstance(visual.get("locator"), str) or not visual["locator"].strip():
            raise ValueError(f"Missing visual locator: {identity}")
        if not all(isinstance(visual.get("caption", {}).get(lang), str) and visual["caption"][lang].strip() for lang in ("en", "zh")):
            raise ValueError(f"Missing bilingual visual caption: {identity}")
        for key in FIELDS:
            if not all(isinstance(row[key][lang], str) and row[key][lang].strip() for lang in ("en", "zh")):
                raise ValueError(f"Missing bilingual {key}: {identity}")
        if row["local_reproduction"] not in {"not-run", "partial", "reproduced"}:
            raise ValueError(f"Invalid reproduction status: {identity}")
        if row["local_reproduction"] != "not-run" and not row.get("reproduction_evidence"):
            raise ValueError(f"Reproduction requires evidence: {identity}")
        if not row["sources"]:
            raise ValueError(f"No sources: {identity}")
        for source in row["sources"]:
            parsed = urlsplit(source["url"])
            if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
                raise ValueError(f"Invalid primary source URL: {identity}")
            if not source["label"] or source["kind"] not in {"paper", "official-report", "repository", "license", "project-page"}:
                raise ValueError(f"Invalid source type: {identity}")
    return start, end


def name(base, lang):
    return f"{base}{'.zh-CN' if lang == 'zh' else ''}.md"


def tr(pair, lang):
    return pair[lang == "zh"]


def cell(text):
    return text.replace("|", "\\|").replace("\n", " ")


def row_link(row, lang):
    return f"[{cell(row['title'])}]({name(row['category'], lang)}#{row['id']})"


def asset_link(row, lang):
    return row["visual"]["asset"]


def table(rows, lang):
    heading = tr(("Date | Work | Organizations | Evidence class", "日期 | 工作 | 机构 | 证据类别"), lang)
    lines = [f"| {heading} |", "| --- | --- | --- | --- |"]
    for row in rows:
        orgs = cell(" / ".join(row["organizations"]))
        relation = tr(RELATIONS[row["relationship"]], lang)
        lines.append(f"| {row['published']} | {row_link(row, lang)} | {orgs} | {relation} |")
    return "\n".join(lines)


def materials(rows, lang):
    title = tr(("Open materials index", "开放材料索引"), lang)
    intro = tr((
        "This table answers a practical question before a reader opens a paper: is there a public implementation, checkpoint or dataset to inspect? Repository and license links are copied from the record's audited sources. A missing link means not verified in this audit, not that an artifact cannot exist.",
        "这张表先回答一个实际问题：打开论文前，是否有可检查的公开实现、检查点或数据集？仓库和许可链接来自条目已核验的一手来源。没有链接表示本轮未核实，不表示资产一定不存在。",
    ), lang)
    links = tr(("[← Research map](README.md) · [Quickstart](QUICKSTART.md) · [Landscape](LANDSCAPE.md) · [Format](FORMAT.md)",
                "[← 研究地图](README.zh-CN.md) · [快速开始](QUICKSTART.zh-CN.md) · [研究全景](LANDSCAPE.zh-CN.md) · [记录格式](FORMAT.md)"), lang)
    heading = tr(("Date | Work | Verified code / weights / data | License and evidence note", "日期 | 工作 | 已核验代码／权重／数据 | 许可与证据说明"), lang)
    lines = [f"# {title}", "", links, "", intro, "", f"| {heading} |", "| --- | --- | --- | --- |"]
    for row in rows:
        releases = [source for source in row["sources"] if source["kind"] in {"repository", "license"}]
        if releases:
            asset_links = " · ".join(f"[{source['label']}]({source['url']})" for source in releases)
        else:
            asset_links = tr(("No verified public asset link", "未核验到公开资产链接"), lang)
        note = cell(row["availability"][lang])
        lines.append(f"| {row['published']} | {row_link(row, lang)} | {asset_links} | {note} |")
    lines.extend(["", tr((
        "Read the category pages for mechanism and result details. Do not infer that an open repository provides released weights or redistributable data; the fields are intentionally separated.",
        "机制与结果详情请看四个分类页面。不要因为仓库公开就推断权重或数据也能再分发；资料库刻意把几类资产分开记录。",
    ), lang), ""])
    return "\n".join(lines)


def overview(data, rows, lang):
    start, end = data["window_start"], data["as_of"]
    active = [r for r in rows if r["published"] >= start]
    archived = [r for r in rows if r not in active]
    counts = Counter(r["category"] for r in active)
    title = tr(("Industry RSI research map", "企业 RSI 研究地图"), lang)
    intro = tr((
        "A selective, primary-source catalogue of company and company–university papers, systems and results. Every detail entry includes a locally stored paper figure, official research image or source-page screenshot, with its locator and source URL, plus an explicit list of verified code, weights or data links when available. Classification and proposed nanoRSI applications are our interpretation. All numbers are authors' reports unless an entry links local reproduction evidence. These heterogeneous results are not a leaderboard or proof of general RSI.",
        "按一手来源整理企业及产学合作的论文、系统与公开成果，属于精选资料库，并非穷尽式综述。每条详情都带一张纳入仓库的论文原图、官方研究图片或原文页截图，并注明定位信息和来源链接；有核验结果时还会单独列出代码、权重或数据链接。分类与 nanoRSI 应用方向是我们的解读；除非条目链接了本地复现证据，数值均为作者报告。这些异构结果不能合成排行榜，也不能证明通用 RSI 已解决。",
    ), lang)
    terms = tr((
        "**Direct bounded loop**: updated code, memory, data policy, parameters or learning rules affect later iterations; this does not necessarily improve the improvement algorithm itself. **Enabling**: useful adaptation, memory or evaluation without a demonstrated recursive deployment loop. **Automated / assisted R&D**: evidence focuses on a research workflow or a separate target model, with varying human involvement. Labels describe the emphasis of an entry, can overlap, and are not levels of proven RSI.",
        "**直接有界闭环**：更新后的代码、记忆、数据策略、参数或学习规则影响后续迭代，但不一定改进了改进算法自身。**支撑技术／评测**：有用的适配、记忆或评测机制，尚未展示递归部署闭环。**自动化／辅助研发**：证据主要针对研究流程或独立目标模型，人类参与程度各异。这些标签表示条目的侧重点，可以有交集，不是已证明 RSI 的等级。",
    ), lang)
    links = tr(("[Quickstart](QUICKSTART.md) · [Landscape and taxonomy](LANDSCAPE.md) · [Open materials](OPEN_MATERIALS.md) · [Tencent coverage audit](TENCENT.md) · [Coverage and dates](COVERAGE.md) · [Experiments to build next](ADOPTION.md) · [Source-image manifest](assets/paper-figures/README.md)",
                "[快速开始](QUICKSTART.zh-CN.md) · [研究全景与分类](LANDSCAPE.zh-CN.md) · [开放材料](OPEN_MATERIALS.zh-CN.md) · [Tencent 覆盖审计](TENCENT.zh-CN.md) · [检索覆盖与日期](COVERAGE.md) · [下一步可实现的实验](ADOPTION.md) · [原文图片清单](assets/paper-figures/README.md)"), lang)
    lines = [f"# {title}", "", f"**{start} → {end}** · **{len(active)}** " + tr(("in-window records", "条窗口内记录"), lang), "", intro, "", terms, "", links + " · [catalog.json](catalog.json) · [English](README.md) / [中文](README.zh-CN.md)", "", "## " + tr(("Browse by what changes", "按改变对象浏览"), lang), "", "| " + tr(("Category | Records", "分类 | 条目数"), lang) + " |", "| --- | ---: |"]
    for category, label in CATEGORIES.items():
        lines.append(f"| [{tr(label, lang)}]({name(category, lang)}) | {counts[category]} |")
    lines.extend(["", "## " + tr(("Timeline", "时间索引"), lang), "", table(active, lang)])
    if archived:
        lines.extend(["", "## " + tr(("Archive — outside the current window", "历史归档——已超出当前窗口"), lang), "", table(archived, lang)])
    lines.extend(["", "## " + tr(("Dates, reuse and updates", "日期、复用与更新"), lang), "", tr((
        "Dates refer to the cited first paper or dated substantive report, not crawl time, repository activity or conference year. Month-only dates remain month-only. Entry notes distinguish earlier announcements and later papers. Public code is not automatically permissively licensed; weights and datasets can have different terms. This snapshot does not execute or reproduce upstream systems.",
        "采用所引首版论文或实质成果报告的日期，不采用抓取时间、仓库活跃时间或会议年份。仅能确认月份时保留月份；条目说明区分先行公告与后续论文。代码可见不代表可以不受限复用，权重和数据可能有不同条款。本次整理未执行或复现上游系统。",
    ), lang), "", tr((
        "For updates, edit the canonical JSON and follow [the record format](FORMAT.md). The renderer retains old entries as an archive when the window advances. Check sources again before changing a reported metric or release status.",
        "更新时编辑唯一数据源 JSON，并遵循[记录格式](FORMAT.md)。窗口滚动后，生成器会将旧条目保留在历史归档中。修改指标或发布状态前需重新核对来源。",
    ), lang), "", "```bash", "python docs/research/industry-rsi/render.py", "python docs/research/industry-rsi/render.py --check", "```", ""])
    return "\n".join(lines)


def details(category, rows, lang):
    lines = [f"# {tr(CATEGORIES[category], lang)}", "", f"[← {tr(('Research map', '研究地图'), lang)}]({name('README', lang)})", ""]
    for row in rows:
        if row["category"] != category:
            continue
        lines.extend([f'<a id="{row["id"]}"></a>', "", f"## {row['title']}", "", f"**{row['published']}** · {row['kind']} · {tr(RELATIONS[row['relationship']], lang)}", ""])
        for key, label in FIELDS.items():
            lines.extend([f"**{tr(label, lang)}** — {row[key][lang]}", ""])
        visual = row["visual"]
        lines.extend([
            f"![{cell(visual['caption'][lang])}]({asset_link(row, lang)})",
            "",
            f"**{tr(('Source figure / official image', '原文图／官方图片'), lang)}** — {visual['caption'][lang]} · {visual['locator']} · [source]({visual['source_url']})",
            "",
        ])
        status = row["local_reproduction"]
        evidence = row.get("reproduction_evidence")
        if evidence:
            status += f" · [Evidence]({evidence})"
        lines.extend([f"**{tr(('nanoRSI reproduction', 'nanoRSI 复现状态'), lang)}** — {status}. " + tr(("Last source check: ", "来源最近核验："), lang) + row["last_verified"] + ".", ""])
        sources = " · ".join(f"[{s['label']}]({s['url']})" for s in row["sources"])
        released = [s for s in row["sources"] if s["kind"] in {"repository", "license"}]
        if released:
            open_assets = " · ".join(f"[{s['label']}]({s['url']})" for s in released)
        else:
            open_assets = tr(("No verified public code/asset link in the audited sources.", "核验来源中没有确认的公开代码／资产链接。"), lang)
        lines.extend([
            f"**{tr(('Open code / weights / data links', '开源代码／权重／数据链接'), lang)}** — {open_assets}",
            "",
            f"**{tr(('Primary sources', '一手来源'), lang)}** — {sources}",
            "",
        ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    validate(data)
    rows = sorted(data["records"], key=lambda r: (r["published"], r["id"]), reverse=True)
    output = {}
    for lang in ("en", "zh"):
        output[name("README", lang)] = overview(data, rows, lang)
        output[name("OPEN_MATERIALS", lang)] = materials(rows, lang)
        for category in CATEGORIES:
            output[name(category, lang)] = details(category, rows, lang)
    stale = []
    if args.check:
        for filename, content in output.items():
            path = ROOT / filename
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(filename)
    else:
        for filename, content in output.items():
            (ROOT / filename).write_text(content, encoding="utf-8")
    if args.check:
        for row in rows:
            asset = ROOT / row["visual"]["asset"]
            if not asset.exists() or asset.stat().st_size == 0:
                stale.append(row["visual"]["asset"])
    if stale:
        raise SystemExit("Stale generated pages: " + ", ".join(stale))
    print(f"Validated {len(rows)} records; {len(output)} pages {'match' if args.check else 'written'}.")


if __name__ == "__main__":
    main()
