"""Render the published descriptive results; matplotlib is optional tooling only."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def render(root):
    live = json.loads((root / "live/summary.json").read_text())
    learning = json.loads((root / "parameter-learning/summary.json").read_text())
    kinds = ["program", "agent", "recursive", "skills", "population", "remote"]
    rows = {row["kind"]: row for row in live["runs"]}
    groups = {(row["method"], row["arm"]): row for row in learning["groups"]}
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})
    fig, axes = plt.subplots(2, 1, figsize=(11, 10), gridspec_kw={"height_ratios": [1.05, 1]})
    fig.patch.set_facecolor("#fbfaf6")
    colors = ["#8a969c", "#e76736", "#286961"]
    for ax in axes:
        ax.set_facecolor("#fbfaf6")
        ax.set_xlim(0, 115)
        ax.set_xticks([0, 25, 50, 75, 100], ["0%", "25%", "50%", "75%", "100%"])
        ax.grid(axis="x", color="#e1e0da", linewidth=0.7)
        ax.set_axisbelow(True)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.spines["bottom"].set_color("#b0b0aa")
        ax.tick_params(axis="y", length=0)
    ax = axes[0]
    for i, kind in enumerate(kinds):
        for offset, condition, color in [(-.17, "baseline", colors[0]), (.17, "candidate", colors[1])]:
            value = 100 * rows[kind]["scores"][condition]
            ax.barh(i + offset, value, height=.29, color=color,
                    label=condition.capitalize() if i == 0 else None)
            ax.text(value + 1, i + offset, f"{value:.0f}%", va="center", fontsize=10)
    ax.set_yticks(range(6), ["Program", "Agent planner", "Recursive reuse", "Executable skill*", "Population", "HTTP workers**"])
    ax.invert_yaxis()
    ax.set_title("Live GLM proposals · six separate teaching demos", loc="left", fontweight="bold", pad=18)
    ax.legend(loc="lower left", bbox_to_anchor=(0, -.27), ncol=2, frameon=False, fontsize=10)
    ax.set_xlabel("Frozen test pass rate · 4 cases each, except *1 six-file task / 4-action budget")
    ax = axes[1]
    for i, (method, label) in enumerate([("sft", "SFT / cross-entropy"), ("rl", "REINFORCE"), ("lora", "LoRA")]):
        values = [groups[(method, "frozen")]["mean_baseline_accuracy"],
                  groups[(method, "frozen")]["mean_candidate_accuracy"],
                  groups[(method, "self-use")]["mean_candidate_accuracy"]]
        for j, (value, name, color) in enumerate(zip(values, ["Initial", "Frozen proposer", "Self-use proposer"], colors)):
            ax.barh(i + (j - 1) * .23, 100 * value, height=.2, color=color, label=name if i == 0 else None)
            ax.text(100 * value + 1, i + (j - 1) * .23, f"{100 * value:.2f}%", va="center", fontsize=10)
    ax.set_yticks(range(3), ["SFT / cross-entropy", "REINFORCE", "LoRA"])
    ax.invert_yaxis()
    ax.set_title("Real CPU parameter updates · tiny softmax classifier", loc="left", fontweight="bold", pad=18)
    ax.legend(loc="lower left", bbox_to_anchor=(0, -.31), ncol=3, frameon=False, fontsize=10)
    ax.set_xlabel("Mean test accuracy · 3 seeds × 120 test cases per seed · 18 runs / 54 training rounds")
    fig.suptitle("nanoRSI 0.4.0 · measured outcomes", x=.06, y=.98, ha="left", fontsize=22, fontweight="bold", color="#202c30")
    fig.text(.06, .934, "43 GLM-5.3-Flash study requests · 87,812 tokens · all rejected and no-op attempts retained", fontsize=11)
    fig.text(.06, .035, "Small authored tasks, one frozen pass per live demo. **Two localhost HTTP processes; no multi-host test.\n"
             "The remote candidate has a documented parser counterexample. CPU training is not pretrained LLM fine-tuning.\n"
             "Recursive controls are tied or mixed; these results do not establish a sustained recursive advantage.", fontsize=10, color="#4b5659", linespacing=1.6)
    fig.subplots_adjust(left=.23, right=.98, top=.87, bottom=.20, hspace=.55)
    fig.savefig(root / "overview.png", dpi=170, facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path)
    render(parser.parse_args().results)
