#!/usr/bin/env python3
"""Render docs/assets/readme/real-tasks-results.svg (editorial dumbbell chart).

Regenerate:  python3 docs/assets/readme/render-real-tasks.py   (stdlib only)
Data comes from the published studies in examples/results/ (see each summary.json).
Style guidance: the lieflat-charts skill's Basics C8 "dumbbell queue" structure with
the wire preset (grayscale + one orange focal value), adapted to a static SVG for the
GitHub README (no scripts run there). Beads are omitted: scores are continuous, not
countable units. No skill code is redistributed; this generator is original.
"""
from pathlib import Path

BG, TXT = "#F0F0EE", "#1F1E1C"
INK, GRAY, MUT = "#22211F", "#8F8E86", "#B0AFA9"
TRACK = "rgba(31,30,28,.14)"
HERO = "#F5572F"

ROWS = [
    ("01  FUNCTION MINIMIZATION", "OPENEVOLVE · APACHE-2.0 · GLM-5.3-FLASH · 5 CALLS", 0.9418, 0.9960),
    ("02  SINE APPROXIMATION", "SHINKAEVOLVE · APACHE-2.0 · GLM-5.3 · 5 CALLS", 0.1049, 0.999963),
    ("03  K-MODULE CONFIGURATION", "OPENEVOLVE · APACHE-2.0 · GLM-5.3 · 8 CALLS", 0.0, 1.0),
    ("04  SKILL EVOLUTION · TWO ARMS", "AUTHORED TASKS · GLM-5.3-FLASH · 190 CALLS", 0.0, 2 / 3),
]
HERO_ROW = 1

W, H = 760, 420
X0, X1 = 250.0, 640.0
TOP, GAP = 118.0, 62.0


def x(v: float) -> float:
    return X0 + max(0.0, min(1.0, v)) * (X1 - X0)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;")


parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Inter,Helvetica,Arial,sans-serif">',
    f'<rect width="{W}" height="{H}" rx="24" fill="{BG}"/>',
    f'<text x="36" y="52" font-size="19" font-weight="700" fill="{TXT}">Every ported task improved under the gate</text>',
    f'<text x="36" y="74" font-size="11" fill="{MUT}">Frozen final-test score · initial program vs evolved candidate · '
    f'nanoRSI end-to-end with GLM · 2026-09</text>',
    f'<line x1="{X0 - 10}" y1="92" x2="{X1 + 14}" y2="92" stroke="{TRACK}" stroke-width="1"/>',
    f'<text x="{X1 + 14}" y="86" font-size="9" font-weight="600" fill="{GRAY}" text-anchor="end" letter-spacing=".08em">BETTER →</text>',
]
for i, (name, meta, before, after) in enumerate(ROWS):
    y = TOP + i * GAP
    xa, xb = x(before), x(after)
    hero = i == HERO_ROW
    parts.append(f'<text x="236" y="{y - 2}" font-size="10.5" font-weight="700" fill="{TXT}" text-anchor="end" '
                 f'letter-spacing=".05em">{esc(name)}</text>')
    parts.append(f'<text x="236" y="{y + 12}" font-size="8" fill="{MUT}" text-anchor="end" letter-spacing=".03em">{esc(meta)}</text>')
    parts.append(f'<line x1="{X0 - 10}" y1="{y}" x2="{X1 + 14}" y2="{y}" stroke="{TRACK}" stroke-width="1"/>')
    parts.append(f'<circle cx="{xa:.1f}" cy="{y}" r="4.4" fill="{BG}" stroke="{INK}" stroke-width="1.4"/>')
    color = HERO if hero else INK
    parts.append(f'<circle cx="{xb:.1f}" cy="{y}" r="5.0" fill="{color}"/>')
    label, value = f"{before:.3f}", ("1.000" if after >= 0.9995 else f"{after:.3f}")
    if after - before < 0.08:
        parts.append(f'<text x="{xa + 9:.1f}" y="{y + 18}" font-size="9.5" font-weight="600" fill="{GRAY}">{label}</text>')
    else:
        parts.append(f'<text x="{xa + 9:.1f}" y="{y - 9}" font-size="9.5" font-weight="600" fill="{GRAY}">{label}</text>')
    parts.append(f'<text x="{xb + 10:.1f}" y="{y - 9}" font-size="11.5" font-weight="800" fill="{color}">{value}</text>')
    delta = f"+{after - before:+.3f}".replace("++", "+")
    parts.append(f'<text x="712" y="{y + 4}" font-size="10" font-weight="700" fill="{HERO if hero else MUT}" '
                 f'text-anchor="end">{delta}</text>')
parts.append(f'<text x="712" y="{TOP - 26}" font-size="8" font-weight="600" fill="{GRAY}" text-anchor="end" '
             f'letter-spacing=".08em">GAIN</text>')
parts.append(f'<text x="{X1 + 14}" y="{TOP + 4 * GAP - 10}" font-size="8" font-weight="600" fill="{GRAY}" '
             f'text-anchor="end" letter-spacing=".06em">1.0 · SCORE</text>')
parts.append(f'<text x="36" y="{H - 46}" font-size="8.5" font-weight="600" fill="{GRAY}" letter-spacing=".10em">'
             f'HOLLOW = INITIAL PROGRAM · SOLID = EVOLVED CANDIDATE · ORANGE = LARGEST GAIN</text>')
parts.append(f'<text x="36" y="{H - 28}" font-size="8" fill="{MUT}">Honest notes: the two skill-evolution arms tied each other; '
             f'the rejected-memory A/B was a clean null; failures and rejections are retained in the published evidence.</text>')
parts.append(f'<text x="36" y="{H - 14}" font-size="7.5" font-weight="600" fill="{MUT}" letter-spacing=".12em">'
             f'SOURCE: EXAMPLES/RESULTS · TASKS FROM OPENEVOLVE &amp; SHINKAEVOLVE (APACHE-2.0) · INDEPENDENT NANORSI RUNS</text>')
parts.append("</svg>")

OUT = Path(__file__).resolve().parent / "real-tasks-results.svg"
OUT.write_text("\n".join(parts), encoding="utf-8")
print(f"wrote {OUT}")
