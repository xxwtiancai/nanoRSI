#!/usr/bin/env python3
"""Render docs/assets/readme/real-tasks-results.svg (paired horizontal bars).

Regenerate:  python3 docs/assets/readme/render-real-tasks.py   (stdlib only)
Data comes from the published studies in examples/results/ (see each summary.json).
Style guidance: the lieflat-charts skill's grouped-bar patterns (Basics C2 paired
rungs / Glance G3 chunky bars) with the wire preset (grayscale + one orange focal
value), adapted to a static SVG for the GitHub README (no scripts run there).
Solid bars, not rung ladders or beads: scores are continuous, and bar length maps
directly to value so the before/after gap reads at a glance. No skill code is
redistributed; this generator is original.
"""
from pathlib import Path

BG, TXT = "#F0F0EE", "#1F1E1C"
INK, GRAY, MUT, LIGHT = "#22211F", "#8F8E86", "#B0AFA9", "#C6C5BF"
TRACK = "rgba(31,30,28,.14)"
HERO = "#F5572F"

ROWS = [
    ("01  FUNCTION MINIMIZATION", "OPENEVOLVE · APACHE-2.0 · GLM-5.3-FLASH · 5 CALLS", 0.9418, 0.9960),
    ("02  SINE APPROXIMATION", "SHINKAEVOLVE · APACHE-2.0 · GLM-5.3 · 5 CALLS", 0.1049, 0.999963),
    ("03  K-MODULE CONFIGURATION", "OPENEVOLVE · APACHE-2.0 · GLM-5.3 · 8 CALLS", 0.0, 1.0),
    ("04  SKILL EVOLUTION · TWO ARMS", "AUTHORED TASKS · GLM-5.3-FLASH · 190 CALLS", 0.0, 2 / 3),
]
HERO_ROW = 1

W, H = 760, 424
X0, X1 = 250.0, 640.0
TOP, GAP = 120.0, 66.0


def x(v: float) -> float:
    return X0 + max(0.0, min(1.0, v)) * (X1 - X0)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;")


def bar(cx: float, width: float, height: float, fill: str) -> str:
    if width < 1:
        return ""
    return (f'<rect x="{X0:.1f}" y="{cx - height / 2:.1f}" width="{width:.1f}" '
            f'height="{height}" rx="{height / 2}" fill="{fill}"/>')


parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Inter,Helvetica,Arial,sans-serif">',
    f'<rect width="{W}" height="{H}" rx="24" fill="{BG}"/>',
    f'<text x="36" y="52" font-size="19" font-weight="700" fill="{TXT}">Every ported task improved under the gate</text>',
    f'<text x="36" y="74" font-size="11" fill="{MUT}">Frozen final-test score · initial program vs evolved candidate · '
    f'nanoRSI end-to-end with GLM · 2026-09</text>',
    f'<line x1="{X0 - 10}" y1="94" x2="712" y2="94" stroke="{TRACK}" stroke-width="1"/>',
    f'<text x="{X0}" y="88" font-size="8" font-weight="600" fill="{GRAY}" text-anchor="middle">0</text>',
    f'<text x="{X1}" y="88" font-size="8" font-weight="600" fill="{GRAY}" text-anchor="middle">1.0</text>',
    f'<text x="712" y="88" font-size="8" font-weight="600" fill="{GRAY}" text-anchor="end" letter-spacing=".08em">GAIN</text>',
]
for i, (name, meta, before, after) in enumerate(ROWS):
    y = TOP + i * GAP
    hero = i == HERO_ROW
    color = HERO if hero else INK
    parts.append(f'<text x="236" y="{y}" font-size="10.5" font-weight="700" fill="{TXT}" text-anchor="end" '
                 f'letter-spacing=".05em">{esc(name)}</text>')
    parts.append(f'<text x="236" y="{y + 13}" font-size="8" fill="{MUT}" text-anchor="end" letter-spacing=".03em">{esc(meta)}</text>')
    delta = f"+{after - before:+.3f}".replace("++", "+")
    parts.append(f'<text x="712" y="{y}" font-size="10" font-weight="700" fill="{HERO if hero else MUT}" '
                 f'text-anchor="end">{delta}</text>')
    for center, height, fill, score, value, size, weight, vfill in (
        (y + 25.5, 7, LIGHT, before, f"{before:.3f}", 9, 600, GRAY),
        (y + 42, 10, color, after, ("1.000" if after >= 0.9995 else f"{after:.3f}"), 11, 800, color),
    ):
        width = max(0.0, min(1.0, score)) * (X1 - X0)
        parts.append(f'<line x1="{X0}" y1="{center}" x2="{X1}" y2="{center}" stroke="{TRACK}" stroke-width="0.7"/>')
        parts.append(bar(center, width, height, fill))
        parts.append(f'<text x="{X0 + width + 8:.1f}" y="{center + 3.5:.1f}" font-size="{size}" '
                     f'font-weight="{weight}" fill="{vfill}">{value}</text>')
parts.append(f'<text x="36" y="{H - 46}" font-size="8.5" font-weight="600" fill="{GRAY}" letter-spacing=".10em">'
             f'LIGHT BAR = INITIAL PROGRAM · SOLID BAR = EVOLVED CANDIDATE · ORANGE = LARGEST GAIN · BAR LENGTH = SCORE</text>')
parts.append(f'<text x="36" y="{H - 28}" font-size="8" fill="{MUT}">Honest notes: the two skill-evolution arms tied each other; '
             f'the rejected-memory A/B was a clean null; failures and rejections are retained in the published evidence.</text>')
parts.append(f'<text x="36" y="{H - 14}" font-size="7.5" font-weight="600" fill="{MUT}" letter-spacing=".12em">'
             f'SOURCE: EXAMPLES/RESULTS · TASKS FROM OPENEVOLVE &amp; SHINKAEVOLVE (APACHE-2.0) · INDEPENDENT NANORSI RUNS</text>')
parts.append("</svg>")

OUT = Path(__file__).resolve().parent / "real-tasks-results.svg"
OUT.write_text("\n".join(parts), encoding="utf-8")
print(f"wrote {OUT}")
