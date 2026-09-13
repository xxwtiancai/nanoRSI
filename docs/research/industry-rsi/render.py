"""Validate the research catalogue and regenerate its bilingual Markdown pages.

Run from any directory. --check is offline and fails on stale generated pages.
This tool checks structure and rendering, not whether a research claim is true.
"""

import argparse
import calendar
from collections import Counter
from datetime import date
from html import escape
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


def wrap(text, width, limit):
    """Wrap deterministic card copy without adding a text-layout dependency."""
    words = text.split() or [text]
    lines, current = [], ""
    for word in words:
        while len(word) > width:
            if current:
                lines.append(current)
                current = ""
            lines.append(word[:width])
            word = word[width:]
        candidate = f"{current} {word}".strip()
        if current and len(candidate) > width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    if len(lines) > limit:
        lines = lines[:limit]
        lines[-1] = lines[-1].rstrip(" .,;，。；") + "…"
    return lines


def svg_lines(lines, x, y, size, fill="#e8eef8", line_height=1.25, weight="400"):
    spans = []
    for index, line in enumerate(lines):
        dy = "0" if index == 0 else f"{size * line_height:g}"
        spans.append(f'<tspan x="{x}" dy="{dy}">{escape(line)}</tspan>')
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}px" font-weight="{weight}">' + "".join(spans) + "</text>"


def visual_asset(row, lang):
    """Create one source-linked, exact-text summary card for a catalogue record."""
    accent = {
        "parameter-learning": "#9ef01a",
        "agent-code": "#6ee7f9",
        "memory-context": "#c4b5fd",
        "research-workflows": "#fbbf24",
    }[row["category"]]
    category = CATEGORIES[row["category"]][lang == "zh"]
    relation = RELATIONS[row["relationship"]][lang == "zh"]
    title_lines = wrap(row["title"], 38, 3)
    org_lines = wrap(" · ".join(row["organizations"]), 52, 2)
    result_lines = wrap(row["result"][lang], 64, 4)
    limit_lines = wrap(row["limits"][lang], 64, 3)
    availability_lines = wrap(row["availability"][lang], 64, 3)
    source = next((s["url"] for s in row["sources"] if s["kind"] in {"paper", "official-report"}), row["sources"][0]["url"])
    title = svg_lines(title_lines, 70, 150, 34, "#f8fafc", 1.16, "700")
    orgs = svg_lines(org_lines, 70, 285, 16, "#b6c2d9", 1.3)
    result = svg_lines(result_lines, 70, 400, 17, "#edf2f7", 1.35)
    limits = svg_lines(limit_lines, 675, 400, 17, "#edf2f7", 1.35)
    availability = svg_lines(availability_lines, 675, 555, 15, "#cbd5e1", 1.35)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675" viewBox="0 0 1200 675" role="img" aria-labelledby="title desc">
<title id="title">{escape(row["title"])}</title>
<desc id="desc">Industry RSI evidence card for {escape(" / ".join(row["organizations"]))}, {escape(row["published"])}.</desc>
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#0b1020"/><stop offset="1" stop-color="#16213b"/></linearGradient><filter id="shadow" x="-10%" y="-10%" width="120%" height="120%"><feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#000" flood-opacity=".25"/></filter></defs>
<rect width="1200" height="675" rx="28" fill="url(#bg)"/>
<rect x="28" y="28" width="1144" height="619" rx="22" fill="none" stroke="#2b3a58"/>
<circle cx="1085" cy="100" r="56" fill="{accent}" opacity=".13"/><circle cx="1085" cy="100" r="25" fill="{accent}" opacity=".35"/>
<text x="70" y="78" fill="{accent}" font-size="18px" font-weight="700" letter-spacing="2">{escape("NANORSI · 企业 RSI 证据" if lang == "zh" else "NANORSI · INDUSTRY RSI EVIDENCE")}</text>
<rect x="70" y="98" width="300" height="34" rx="17" fill="{accent}" opacity=".18"/><text x="88" y="121" fill="{accent}" font-size="16px" font-weight="700">{escape(category)}</text>
<text x="395" y="121" fill="#a8b5ca" font-size="16px">{escape(relation)} · {escape(row["published"])}</text>
{title}
{orgs}
<line x1="70" y1="330" x2="1130" y2="330" stroke="#2b3a58"/>
<text x="70" y="365" fill="{accent}" font-size="14px" font-weight="700" letter-spacing="1.4">{escape("作者报告结果" if lang == "zh" else "AUTHOR-REPORTED RESULT")}</text>
<text x="675" y="365" fill="{accent}" font-size="14px" font-weight="700" letter-spacing="1.4">{escape("证据边界" if lang == "zh" else "EVIDENCE LIMIT")}</text>
{result}
{limits}
<text x="675" y="530" fill="{accent}" font-size="14px" font-weight="700" letter-spacing="1.4">{escape("开放材料 / 许可" if lang == "zh" else "OPEN MATERIALS / LICENSE")}</text>
{availability}
<text x="70" y="612" fill="#7f8da6" font-size="13px">{escape("来源：" if lang == "zh" else "Source: ")}{escape(source)} · {escape("nanoRSI 本地复现：未运行" if lang == "zh" else "Local nanoRSI reproduction: not run")}</text>
</svg>
'''


def row_link(row, lang):
    return f"[{cell(row['title'])}]({name(row['category'], lang)}#{row['id']})"


def asset_link(row, lang):
    suffix = ".zh-CN" if lang == "zh" else ""
    return f"assets/{row['id']}{suffix}.svg"


def table(rows, lang):
    heading = tr(("Date | Work | Organizations | Evidence class", "日期 | 工作 | 机构 | 证据类别"), lang)
    lines = [f"| {heading} |", "| --- | --- | --- | --- |"]
    for row in rows:
        orgs = cell(" / ".join(row["organizations"]))
        relation = tr(RELATIONS[row["relationship"]], lang)
        lines.append(f"| {row['published']} | {row_link(row, lang)} | {orgs} | {relation} |")
    return "\n".join(lines)


def overview(data, rows, lang):
    start, end = data["window_start"], data["as_of"]
    active = [r for r in rows if r["published"] >= start]
    archived = [r for r in rows if r not in active]
    counts = Counter(r["category"] for r in active)
    title = tr(("Industry RSI research map", "企业 RSI 研究地图"), lang)
    intro = tr((
        "A selective, primary-source catalogue of company and company–university papers, systems and results. Every detail entry includes a local visual evidence card and an explicit list of verified code, weights or data links when available. Classification and proposed nanoRSI applications are our interpretation. All numbers are authors' reports unless an entry links local reproduction evidence. These heterogeneous results are not a leaderboard or proof of general RSI.",
        "按一手来源整理企业及产学合作的论文、系统与公开成果，属于精选资料库，并非穷尽式综述。每条详情都带一张本地可视化证据卡，并在有核验结果时单独列出代码、权重或数据链接。分类与 nanoRSI 应用方向是我们的解读；除非条目链接了本地复现证据，数值均为作者报告。这些异构结果不能合成排行榜，也不能证明通用 RSI 已解决。",
    ), lang)
    terms = tr((
        "**Direct bounded loop**: updated code, memory, data policy, parameters or learning rules affect later iterations; this does not necessarily improve the improvement algorithm itself. **Enabling**: useful adaptation, memory or evaluation without a demonstrated recursive deployment loop. **Automated / assisted R&D**: evidence focuses on a research workflow or a separate target model, with varying human involvement. Labels describe the emphasis of an entry, can overlap, and are not levels of proven RSI.",
        "**直接有界闭环**：更新后的代码、记忆、数据策略、参数或学习规则影响后续迭代，但不一定改进了改进算法自身。**支撑技术／评测**：有用的适配、记忆或评测机制，尚未展示递归部署闭环。**自动化／辅助研发**：证据主要针对研究流程或独立目标模型，人类参与程度各异。这些标签表示条目的侧重点，可以有交集，不是已证明 RSI 的等级。",
    ), lang)
    links = tr(("[Coverage, dates and older foundations](COVERAGE.md) · [Experiments to build next](ADOPTION.md)",
                "[检索覆盖、日期与早期基础](COVERAGE.md) · [下一步可实现的实验](ADOPTION.md)"), lang)
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
        lines.extend([
            f"![{tr(('Visual evidence card', '可视化证据卡'), lang)}]({asset_link(row, lang)})",
            "",
            tr((
                "This local card is a visual summary generated from the audited catalogue text; it is not the paper's original figure. Open the primary-source links below for the original charts, screenshots or demos.",
                "这张本地卡片由已核验的资料库文字生成，是信息摘要，不是论文原图。原始图表、截图或演示请打开下方一手来源。",
            ), lang),
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
        for category in CATEGORIES:
            output[name(category, lang)] = details(category, rows, lang)
    assets = {
        f"assets/{row['id']}{suffix}.svg": visual_asset(row, lang)
        for row in rows
        for lang, suffix in (("en", ""), ("zh", ".zh-CN"))
    }
    stale = []
    if args.check:
        for filename, content in output.items():
            path = ROOT / filename
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(filename)
    else:
        for filename, content in output.items():
            (ROOT / filename).write_text(content, encoding="utf-8")
    asset_dir = ROOT / "assets"
    if args.check:
        expected = set(assets)
        actual = {f"assets/{path.name}" for path in asset_dir.glob("*.svg")} if asset_dir.exists() else set()
        stale.extend(sorted(expected - actual))
        stale.extend(sorted(actual - expected))
        for filename, content in assets.items():
            path = ROOT / filename
            if path.exists() and path.read_text(encoding="utf-8") != content:
                stale.append(filename)
    else:
        asset_dir.mkdir(exist_ok=True)
        for filename, content in assets.items():
            (ROOT / filename).write_text(content, encoding="utf-8")
    if stale:
        raise SystemExit("Stale generated pages: " + ", ".join(stale))
    print(f"Validated {len(rows)} records; {len(output)} pages {'match' if args.check else 'written'}.")


if __name__ == "__main__":
    main()
