"""Plot the complete measured panel; optional matplotlib tooling only."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def plot(summary, output):
    if any(row.get('final_status') != 'completed' for row in summary['runs']):
        raise ValueError('plot requires every assigned final outcome; inspect missing results first')
    groups = {(r['method'], r['policy']): r for r in summary['groups']}
    methods = [m for m in ['sft', 'rl', 'lora'] if (m, 'self-use') in groups]
    labels = {'sft': 'SFT', 'rl': 'REINFORCE', 'lora': 'LoRA'}
    policies = ['frozen', 'self-use', 'uniform', 'random']
    colors = {'frozen': '#8a969c', 'self-use': '#ed6734', 'uniform': '#286961', 'random': '#cab46a'}
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11})
    fig, axes = plt.subplots(2, 1, figsize=(11, 10), gridspec_kw={'height_ratios': [1, 1.15]})
    fig.patch.set_facecolor('#fbfaf6')
    for ax in axes:
        ax.set_facecolor('#fbfaf6')
        ax.spines[['top', 'right']].set_visible(False)
        ax.grid(axis='y', color='#dddcd4', linewidth=.7)
        ax.set_axisbelow(True)
        ax.set_xticks(range(len(methods)), [labels[m] for m in methods])
    for offset, policy in enumerate(policies):
        xs = [i + (offset - 1.5) * .2 for i in range(len(methods))]
        values = [100 * groups[(m, policy)]['mean_accuracy'] for m in methods]
        bars = axes[0].bar(xs, values, width=.18, label=policy, color=colors[policy])
        axes[0].bar_label(bars, labels=[f'{value:.1f}' for value in values], padding=4, fontsize=9)
    axes[0].set_ylim(0, 107)
    axes[0].set_ylabel('Mean final test accuracy (%)')
    axes[0].set_title('All four policies · real saved checkpoints', loc='left', fontweight='bold')
    axes[0].legend(ncol=4, frameon=False, loc='upper center', bbox_to_anchor=(.5, 1.16))
    references = ['frozen', 'uniform', 'random']
    for j, reference in enumerate(references):
        for i, method in enumerate(methods):
            row = next(r for r in summary['comparisons'] if r['method'] == method and r['reference'] == reference)
            mean = row['mean_delta_pp']
            interval = row['bootstrap_family_adjusted_ci_pp'] if reference == 'frozen' else row['bootstrap_95_ci_pp']
            x = i + (j - 1) * .22
            axes[1].errorbar(x, mean, yerr=[[mean - interval[0]], [interval[1] - mean]],
                             fmt='o', color=colors['self-use'] if j == 0 else colors[reference], capsize=5,
                             label='self-use minus ' + reference if i == 0 else None)
            axes[1].annotate(f'{mean:+.2f}', (x, mean), xytext=(0, 10), textcoords='offset points', ha='center', fontsize=9)
            if reference == 'frozen':
                n = len(row['pairs'])
                jitter = [(k - (n - 1) / 2) * .007 for k in range(n)]
                axes[1].scatter([x + v for v in jitter], [p['delta_pp'] for p in row['pairs']], s=14, alpha=.22, color='#ed6734')
    axes[1].axhline(0, color='#333d3d', linewidth=1)
    axes[1].axhline(5, color='#777e76', linestyle='--', linewidth=.8)
    axes[1].set_ylabel('Paired extra accuracy (percentage points)')
    axes[1].set_title('Additional benefit · every matched training seed', loc='left', fontweight='bold')
    axes[1].legend(frameon=False, loc='upper left', fontsize=9)
    nseeds = len({r['seed'] for r in summary['runs']})
    cases = {r['test_cases'] for r in summary['runs']}
    fig.suptitle('nanoRSI · recursive checkpoint reuse', x=.08, y=.98, ha='left', fontsize=21, fontweight='bold')
    fig.text(.08, .931, f'{len(summary["runs"])} runs · {nseeds} training seeds · {next(iter(cases))} held-out digit images per condition', fontsize=11)
    confidence = 100 * next(r['family_adjusted_confidence'] for r in summary['comparisons'] if r['primary'])
    fig.text(.08, .035, f'Primary intervals: {confidence:.2f}% family-adjusted bootstrap; other controls: descriptive 95%.\n'
             'Intervals cover training-seed variation on one fixed row split. Same update budgets within each method.\n'
             'This is a small classifier experiment, not pretrained LLM fine-tuning or evidence of general RSI.', fontsize=10, color='#59615f', linespacing=1.7)
    fig.subplots_adjust(left=.1, right=.97, top=.84, bottom=.16, hspace=.36)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=170, facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('summary', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    plot(json.loads(args.summary.read_text()), args.output)
