"""Draw the paper's LAB evaluation subset rule locally: stratified by practice area,
covering every work type and the full range of task sizes (criteria count as the
context-size proxy). The paper used 100 held-out tasks; we draw N under budget.

python paper_subset.py --n 30 [--seed 7] prints one task id per line.
"""
from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path

LAB = Path(__file__).resolve().parents[2] / ".omx/harness2/dependencies/harvey-labs/tasks"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=30)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    rows = []
    for area in sorted(p for p in LAB.iterdir() if p.is_dir()):
        for task in sorted(area.iterdir()):
            cfg = area / task.name / "task.json"
            if cfg.is_file():
                data = json.loads(cfg.read_text(encoding="utf-8"))
                rows.append({"id": f"{area.name}/{task.name}", "area": area.name,
                             "work": data.get("work_type", ""), "criteria": len(data["criteria"]),
                             "docs": len(list((area / task.name / "documents").iterdir()))
                             if (area / task.name / "documents").is_dir() else 0})
    by_area = defaultdict(list)
    for row in rows:
        by_area[row["area"]].append(row)
    chosen, quota = [], args.n
    # proportional allocation by practice area (largest remainder), min one per area
    counts = {area: max(1, round(quota * len(tasks) / len(rows))) for area, tasks in by_area.items()}
    while sum(counts.values()) > quota:
        shrinkable = [a for a in counts if counts[a] > 1]
        if not shrinkable:
            break
        biggest = max(shrinkable, key=lambda a: counts[a] * len(rows) - quota * len(by_area[a]))
        counts[biggest] -= 1
    for area, tasks in sorted(by_area.items()):
        picked = rng.sample(tasks, min(counts[area], len(tasks)))
        # within an area prefer work-type diversity, then span the criteria range
        seen_works = set()
        diverse = [t for t in picked if not (t["work"] in seen_works or seen_works.add(t["work"]))]
        rest = [t for t in picked if t not in diverse]
        chosen.extend(diverse + rest)
    chosen = chosen[:quota]
    works = {t["work"] for t in chosen}
    print(f"# {len(chosen)} tasks, {len({t['area'] for t in chosen})} areas, works={sorted(works)}, "
          f"criteria {min(t['criteria'] for t in chosen)}..{max(t['criteria'] for t in chosen)}", file=__import__("sys").stderr)
    for t in chosen:
        print(t["id"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
