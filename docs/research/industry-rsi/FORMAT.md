# Catalogue format / 记录格式

[Research map](README.md) · [中文入口](README.zh-CN.md)

`catalog.json` is the canonical data. `render.py` generates the two indexes and eight category pages using only Python's standard library. Each record's `visual` points to a checked-in paper figure, official research-page image, or source-page screenshot. Edit the JSON, regenerate, then run `--check`; do not edit generated Markdown directly. `COVERAGE.md` and `ADOPTION.md` are maintained prose.

`catalog.json` 是唯一数据源。`render.py` 仅使用 Python 标准库，生成中英文索引及八个分类页面。每条记录的 `visual` 指向已核验并纳入仓库的论文图、官方研究页图片或原文页截图。修改 JSON 后重新生成并运行 `--check`，不要直接修改生成的 Markdown。`COVERAGE.md` 与 `ADOPTION.md` 单独维护。

| Field | Meaning / 含义 |
| --- | --- |
| `schema_version` | Currently `1` / 当前为 `1` |
| `as_of`, `window_start` | Explicit inclusive rolling window; advance deliberately, retaining existing records / 明确的闭区间滚动窗口；更新时保留已有记录 |
| `id` | Stable lowercase kebab-case identifier and detail anchor / 稳定的小写连字符标识，也是详情锚点 |
| `title`, `organizations` | Cited title and actual author institutions; using a company's model does not imply affiliation / 来源标题与真实作者机构；使用某公司模型不代表隶属该公司 |
| `published`, `kind` | First cited work/event date and `paper`, `report` or `release`; `YYYY-MM` permitted when only a month is verified / 所引工作或事件的首次公开日期及类型；只能核实月份时允许 `YYYY-MM` |
| `date_note` | Explain announcement/paper/revision differences; do not substitute conference year for first publication / 解释公告、论文与修订日期差异，不用会议年份替代首发日期 |
| `additional_events` | Optional later substantive paper/release events, each with `date`, `kind`, `label`; sources must be in the record / 后续实质论文或发布事件；来源必须包含在条目中 |
| `category` | `parameter-learning`, `agent-code`, `memory-context`, `research-workflows`; choose the primary surface and explain secondary ones in prose / 选择主要改变对象，次要机制在正文说明 |
| `relationship` | `direct-loop`, `enabling`, `assisted-rd`; catalogue interpretation, not an author endorsement / 资料库的机制解读，不代表作者认可该标签 |
| `affiliation`, `mechanism` | Institutional relationship and mutation → feedback → reuse mechanism / 机构关系，以及修改 → 反馈 → 复用机制 |
| `result`, `limits` | Author result with comparator, unit and conditions; negative findings and confounders belong here too / 作者结果、对照、单位及条件；保留负结果与混杂因素 |
| `availability` | Separately address code, weights, data and licenses; “not verified” is not “does not exist” / 分开说明代码、权重、数据和许可；未核验不等于不存在 |
| `application` | A concrete proposed nanoRSI experiment, not a promise or an implemented capability / 具体拟议实验，不是已实现能力或交付承诺 |
| `sources` | Opened primary URLs with `label`, `url`, `kind`; kinds: `paper`, `official-report`, `repository`, `license`, `project-page` / 已实际打开的一手来源 |
| `visual` | `{kind, asset, source_url, locator, caption:{en,zh}}`; `kind` identifies an original paper figure, official report/project image, or source-page screenshot. The file must explain the cited research, not be an unrelated concept illustration / `{kind, asset, source_url, locator, caption:{en,zh}}`；`kind` 说明论文原图、官方报告/项目图片或原文页截图。图片必须解释所引研究，不能使用无关概念插画 |
| `last_verified` | Date these claims and release states were checked / 最近核验日期 |
| `local_reproduction` | `not-run`, `partial`, `reproduced`; the latter two require `reproduction_evidence` / 后两种必须提供本地复现依据链接 |

All prose fields from `date_note` through `application` use an object with `en` and `zh` strings. Keep both languages consistent. Cite the paper version that supplies the metric, not merely the latest abstract. Do not copy entire abstracts or proprietary source material into the catalogue.

上述说明字段均使用包含 `en`、`zh` 的对象，两个语言版本应一致。指标应引用实际提供该结果的论文版本，而非只链接最新摘要；不要复制整段摘要或专有材料。

`--check` validates dates, required bilingual content, stable IDs, classifications, source URL shape, visual provenance and generated-page consistency. It checks that every visual asset exists and is non-empty, but makes no network calls and cannot establish scientific validity, source reachability, copyright permission or licensing completeness. Source reading and image review remain necessary. Month-only dates crossing a window boundary must be clarified before inclusion.

`--check` 检查日期、必需双语字段、稳定 ID、分类、来源 URL 形式、视觉来源和生成页面一致性，并确认每条记录的图片存在且非空。它不联网，不能证明科学有效性、来源可访问性、版权授权或许可完整性，仍需阅读来源并检查图片。月份精度跨越窗口边界时，应先澄清日期。

```bash
python docs/research/industry-rsi/render.py
python docs/research/industry-rsi/render.py --check
```
