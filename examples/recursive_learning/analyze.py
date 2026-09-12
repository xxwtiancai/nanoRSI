"""Recompute measured outcomes from verified journals and compare paired seeds."""
from __future__ import annotations
from collections import Counter, defaultdict
import json
import math
from pathlib import Path
import random
import re
import statistics
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / 'src') not in sys.path:
    sys.path.insert(0, str(ROOT / 'src'))
from nanorsi.hashing import canonical_hash
from nanorsi.lineage import LineageStore
from nanorsi.report import _final_comparison


def git(lab, *args):
    return subprocess.check_output(['git', '-C', str(lab), *args])


def verified_events(lab):
    return LineageStore(lab / 'lineage.jsonl', lab / '.nanorsi/lineage.key').verify()


def design_hash(lab, commit):
    config = tomllib.loads(git(lab, 'show', commit + ':nanorsi.toml').decode())
    for key in ['id', 'arm']:
        config['experiment'].pop(key, None)
    recipe = json.loads(git(lab, 'show', commit + ':target/recipe.json'))
    recipe.pop('policy')  # This is the explicit extra-control treatment.
    names = git(lab, 'ls-tree', '-r', '--name-only', commit, '--', 'trainer', 'evaluator', 'proposer', 'adapters').decode().splitlines()
    fixed = {name: git(lab, 'rev-parse', commit + ':' + name).decode().strip() for name in names}
    return canonical_hash({'config': config, 'recipe_without_policy': recipe, 'fixed_blobs': fixed,
                           'initial_checkpoint': git(lab, 'rev-parse', commit + ':target/model.json').decode().strip(),
                           'manifest': git(lab, 'rev-parse', commit + ':tasks/manifest.json').decode().strip()})


def primary_inference(methods):
    """The primary family is fixed before test outcomes exist."""
    return {'methods': sorted(methods), 'contrast': 'self-use minus frozen',
            'family_size': len(methods), 'familywise_alpha': .05,
            'adjustment': 'Bonferroni', 'minimum_gain_pp': 5,
            'requires_complete_matched_budget_panel': True}


WORK_FIELDS = [('actual_update_steps', 'planned_update_steps'),
               ('examples_seen', 'planned_examples_seen'),
               ('training_scored_examples', 'planned_training_scored_examples'),
               ('proposer_scored_examples', 'planned_proposer_scored_examples'),
               ('evaluation_scored_examples', 'planned_evaluation_scored_examples')]


def matched_budget(row):
    return (row.get('protocol_status') == 'completed' and row.get('budget_complete') is True
            and all(row.get(field, 0) == 0 for field in ['failed_attempts', 'missing_attempts', 'unaccounted_attempts'])
            and row.get('started_attempts') == row.get('planned_attempts')
            and all(type(row.get(actual)) is int and type(row.get(planned)) is int
                    and row[actual] == row[planned] for actual, planned in WORK_FIELDS))


def artifact_json(lab, ref):
    # Failed external programs can leave truncated JSON that is still faithfully
    # hashed in the journal. Those bytes prove neither zero work nor completion.
    try:
        return json.loads((lab / ref['path']).read_text()) if ref else None
    except (OSError, ValueError):
        return None


def search_accounting(lab, events, recipe, config, manifest):
    """Use only already verified journal/ref bytes; unknown work stays null."""
    rounds = config['budget']['max_steps']
    counts = Counter(t['split'] for t in manifest['tasks'])
    train_count = counts['train']
    grouped = defaultdict(list)
    for event in events:
        if event.get('attempt_id', 0):
            grouped[event['attempt_id']].append(event)
    expected = set(range(1, rounds + 1))
    records, curricula = [], []
    for attempt in sorted(expected | grouped.keys()):
        entries = grouped[attempt]
        started = any(e.get('event_type') == 'attempt_started' for e in entries)
        terminals = [e for e in entries if e.get('event_type') in {'generation', 'attempt_failed', 'candidate_evaluated'}]
        failed = any(e.get('event_type') == 'attempt_failed' for e in terminals)
        inline = [e['training'] for e in entries if isinstance(e.get('training'), dict)]
        evidence, traces = [], []
        for event in entries:
            for name, ref in event.get('artifacts', {}).items():
                if name == 'training/evidence.json':
                    evidence.append(artifact_json(lab, ref))
                elif name == 'proposal/trace.json':
                    value = artifact_json(lab, ref)
                    traces.append(value[0] if isinstance(value, list) and value and isinstance(value[0], dict) else None)
        training = evidence[0] if evidence else inline[0] if inline else None
        if not isinstance(training, dict) or any(value != training for value in [*evidence, *inline]):
            training = None
        if traces and (traces[0] is None or any(trace != traces[0] for trace in traces)):
            traces = []
        completed = training is not None and training.get('status') == 'completed'
        measured = training.get('result', {}) if completed else {}
        if not isinstance(measured, dict):
            measured, completed = {}, False
        # An unstarted planned attempt spent no work; a started attempt without
        # completed evidence may have spent work and cannot be assigned zero.
        zero = 0 if not entries else None
        record = {'attempt_id': attempt, 'started': started,
                  'status': 'missing' if not entries else 'failed' if failed else 'completed' if terminals and completed else 'unaccounted',
                  'training_status': training.get('status') if training else 'unaccounted' if entries else 'not_started',
                  'training_source': 'verified_artifact' if evidence else 'signed_inline' if inline else None,
                  'update_steps': training.get('steps') if completed else zero,
                  'examples_seen': measured.get('examples_seen', zero),
                  'training_scored_examples': measured.get('training_scoring_examples', zero),
                  'proposer_scored_examples': traces[0].get('scored_examples') if traces else
                  (None if any(e.get('event_type') == 'proposal_started' for e in entries) else 0)}
        if traces:
            trace = traces[0]
            # Loss order is descriptive. Sampling depends on membership/weights.
            curricula.append(trace.get('sampling_sha256') or tuple(sorted(set(trace['focus_task_ids']))))
        for field in ['update_steps', 'examples_seen', 'training_scored_examples', 'proposer_scored_examples']:
            if record[field] is not None and (type(record[field]) is not int or record[field] < 0):
                raise ValueError('invalid measured training/scoring work')
        records.append(record)
    totals = {}
    for field in ['update_steps', 'examples_seen', 'training_scored_examples', 'proposer_scored_examples']:
        values = [r[field] for r in records]
        totals['known_' + field] = sum(v for v in values if v is not None)
        totals['actual_update_steps' if field == 'update_steps' else field] = sum(values) if all(v is not None for v in values) else None
    finishes = {e.get('invocation_id'): e for e in events if e.get('event_type') == 'evaluation_finished'}
    evaluated = []
    for start in events:
        if start.get('event_type') != 'evaluation_started' or start.get('phase') != 'search':
            continue
        end = finishes.get(start['invocation_id'], {})
        ref = end.get('artifacts', {}).get('result')
        value = artifact_json(lab, ref)
        cases = value.get('case_results') if isinstance(value, dict) else None
        evaluated.append(len(cases) if isinstance(cases, list) else None)
    totals['known_evaluation_scored_examples'] = sum(v for v in evaluated if v is not None)
    totals['evaluation_scored_examples'] = sum(evaluated) if all(v is not None for v in evaluated) else None
    totals['planned_evaluation_scored_examples'] = counts['validation'] + rounds * (train_count + 2 * counts['validation'])
    totals.update(planned_update_steps=rounds * recipe['steps'], planned_examples_seen=rounds * recipe['steps'] * recipe['batch_size'],
                  planned_training_scored_examples=rounds * 2 * train_count, planned_proposer_scored_examples=rounds * train_count)
    failed = sum(r['status'] == 'failed' for r in records)
    missing = sum(r['status'] == 'missing' for r in records)
    unaccounted = sum(any(r[k] is None for k in ['update_steps', 'examples_seen', 'training_scored_examples', 'proposer_scored_examples']) for r in records)
    complete = (set(grouped) == expected and all(r['started'] and r['status'] == 'completed' for r in records)
                and all(totals[actual] == totals[planned] for actual, planned in WORK_FIELDS)
                and all(r['update_steps'] == recipe['steps'] and r['examples_seen'] == recipe['steps'] * recipe['batch_size']
                        and r['training_scored_examples'] == 2 * train_count and r['proposer_scored_examples'] == train_count for r in records))
    protocol = 'completed' if complete else 'failed' if failed else 'incomplete'
    return {**totals, 'status': protocol, 'protocol_status': protocol, 'budget_complete': complete,
            'planned_attempts': rounds, 'started_attempts': sum(r['started'] for r in records),
            'failed_attempts': failed, 'missing_attempts': missing, 'unaccounted_attempts': unaccounted,
            'attempts': records, 'training_rounds': sum(r['training_status'] == 'completed' for r in records),
            'attempted_update_steps': totals['actual_update_steps'],
            'focus_changes': sum(a != b for a, b in zip(curricula, curricula[1:]))}


def read_run(lab):
    events = verified_events(lab)
    comparison = _final_comparison(events)
    frozen = next((e for e in events if e.get('event_type') == 'freeze'), None)
    if frozen is None:
        raise ValueError('workspace has no frozen final plan')
    match = re.fullmatch(r'digits-(sft|rl|lora)-(\d+)-(frozen|self-use|uniform|random)', frozen['experiment_id'])
    if not match:
        raise ValueError('unrecognized signed study identity')
    method, seed, policy = match.groups()
    seed = int(seed)
    if frozen['seed'] != seed or frozen['arm'] != ('frozen' if policy == 'frozen' else 'self-use'):
        raise ValueError('signed study identity differs from declared factors')
    recipe = json.loads(git(lab, 'show', frozen['baseline_commit'] + ':target/recipe.json'))
    expected_policy = 'prioritized' if policy in {'frozen', 'self-use'} else policy
    if recipe['method'] != method or recipe['seed'] != seed or recipe['policy'] != expected_policy:
        raise ValueError('baseline recipe differs from signed study identity')
    if any(e.get('seq', 0) <= frozen['seq'] for e in events if e.get('split') == 'test' or e.get('event_type') == 'final_result'):
        raise ValueError('test preceded freeze')
    finals = {e['result']['condition']: e['result'] for e in events if e.get('event_type') == 'final_result'}
    if frozen['repeats'] != 1 or not set(finals) <= {'baseline', 'candidate'}:
        raise ValueError('digits study requires one repeat and two final conditions')
    from hashlib import sha256
    for condition, result in finals.items():
        saved = sha256(git(lab, 'show', frozen[condition + '_commit'] + ':target/model.json')).hexdigest()
        if result['checkpoint']['sha256'] != saved:
            raise ValueError('frozen checkpoint differs from actual Git bytes')
        scores = result['case_results']
        for metric, key in [('accuracy', 'score'), ('loss', 'loss')]:
            if not math.isclose(result['metrics'][metric], statistics.fmean(c[key] for c in scores), abs_tol=1e-12):
                raise ValueError('metric differs from actual case outcomes')
    config = tomllib.loads(git(lab, 'show', frozen['baseline_commit'] + ':nanorsi.toml').decode())
    manifest = json.loads(git(lab, 'show', frozen['baseline_commit'] + ':tasks/manifest.json'))
    accounting = search_accounting(lab, events, recipe, config, manifest)
    attempts = [e for e in events if e.get('event_type') in {'generation', 'attempt_failed'} and e.get('attempt_id', 0)]
    candidate = json.loads(git(lab, 'show', frozen['candidate_commit'] + ':target/model.json'))
    result = {'method': method, 'seed': seed, 'policy': policy, **accounting,
              'final_status': 'completed' if comparison else 'incomplete',
              'status': accounting['status'] if comparison else 'incomplete',
              'comparison_hash': frozen['comparison_hash'], 'design_hash': design_hash(lab, frozen['baseline_commit']),
              'manifest_hash': frozen['manifest_hash'], 'baseline_commit': frozen['baseline_commit'],
              'candidate_commit': frozen['candidate_commit'], 'settings': recipe,
              'decisions': dict(Counter(e['decision'] for e in attempts)),
              'retained_update_steps': candidate['metadata']['training_steps'], 'test_cases': comparison['tasks'] if comparison else None,
              'artifact_references': sum(len(e.get('artifacts', {})) for e in events),
              'event_count': len(events), 'locally_verified': True}
    for condition in finals:
        for metric in ['accuracy', 'loss']:
            result[condition + '_' + metric] = finals[condition]['metrics'][metric]
        result[condition + '_checkpoint'] = finals[condition]['checkpoint']
    return result


def interval(values, draws=10000, confidence=.95):
    rng = random.Random(20260912)
    samples = sorted(statistics.fmean(rng.choices(values, k=len(values))) for _ in range(draws))
    tail = (1 - confidence) / 2
    return [samples[int(tail * (draws - 1))], samples[int((1 - tail) * (draws - 1))]]


def paired_statistics(pairs):
    deltas = [pair['delta_pp'] for pair in pairs]
    return {'pairs_count': len(pairs), 'mean_delta_pp': statistics.fmean(deltas) if deltas else None,
            'bootstrap_95_ci_pp': interval(deltas) if deltas else [None, None],
            'positive_seeds': sum(x > 0 for x in deltas), 'negative_seeds': sum(x < 0 for x in deltas),
            'tied_seeds': sum(x == 0 for x in deltas), 'pairs': pairs}


def has_outcome(row):
    return (row is not None and row.get('final_status', row.get('status')) == 'completed'
            and all(isinstance(row.get(key), (int, float)) and math.isfinite(row[key])
                    for key in ['candidate_accuracy', 'candidate_loss']))


def summarize(rows, plan=None):
    grouped = defaultdict(dict)
    for row in rows:
        factors = (row['method'], row['seed'])
        if row['policy'] in grouped[factors]:
            raise ValueError('duplicate study factors')
        grouped[factors][row['policy']] = row
    if plan is not None:
        assigned = {(r['method'], r['seed'], r['policy']) for r in plan['runs']}
        if any((*factors, policy) not in assigned for factors, arms in grouped.items() for policy in arms):
            raise ValueError('unassigned study factors')
        for expected in plan['runs']:
            factors, policy = (expected['method'], expected['seed']), expected['policy']
            grouped[factors].setdefault(policy, {**expected, 'status': 'missing', 'final_status': 'missing',
                                                'protocol_status': 'incomplete', 'budget_complete': False})
        rows = [grouped[(r['method'], r['seed'])][r['policy']] for r in plan['runs']]
    methods = sorted({method for method, _ in grouped})
    rule = primary_inference(methods)
    if plan is not None and plan.get('primary_inference') != rule:
        raise ValueError('summary primary family differs from frozen plan')
    confidence = 1 - .05 / len(methods) if methods else .95
    comparisons, groups = [], []
    for method in ['sft', 'rl', 'lora']:
        seeds = sorted(seed for m, seed in grouped if m == method)
        if not seeds:
            continue
        for policy in ['frozen', 'self-use', 'uniform', 'random']:
            selected = [grouped[(method, seed)].get(policy) for seed in seeds]
            measured = [row for row in selected if has_outcome(row)]
            complete = [row for row in measured if row.get('protocol_status', row.get('status')) == 'completed']
            groups.append({'method': method, 'policy': policy, 'completed_runs': len(complete),
                           'measured_runs': len(measured), 'missing_or_failed_runs': len(seeds) - len(complete),
                           'mean_accuracy': statistics.fmean(r['candidate_accuracy'] for r in measured) if measured else None,
                           'mean_loss': statistics.fmean(r['candidate_loss'] for r in measured) if measured else None,
                           'mean_basis': 'all measured outcomes, including failed/incomplete search protocols'})
        for reference in ['frozen', 'uniform', 'random']:
            measured, complete, budget_pairs = [], [], []
            for seed in seeds:
                arms = grouped[(method, seed)]
                a, b = arms.get('self-use'), arms.get(reference)
                if not has_outcome(a) or not has_outcome(b):
                    continue
                if reference == 'frozen' and a['comparison_hash'] != b['comparison_hash']:
                    raise ValueError('paired comparison hashes differ')
                if a['design_hash'] != b['design_hash']:
                    raise ValueError('control design hashes differ beyond declared policy')
                pair = {'seed': seed, 'delta_pp': 100 * (a['candidate_accuracy'] - b['candidate_accuracy'])}
                measured.append(pair)
                if all(r.get('protocol_status', r.get('status')) == 'completed' for r in [a, b]):
                    complete.append(pair)
                if (matched_budget(a) and matched_budget(b)
                        and all(a[actual] == b[actual] for actual, _ in WORK_FIELDS)):
                    budget_pairs.append(pair)
            all_stats, complete_stats = paired_statistics(measured), paired_statistics(complete)
            primary = reference == 'frozen'
            deltas = [pair['delta_pp'] for pair in measured]
            adjusted = interval(deltas, confidence=confidence) if primary and deltas else [None, None] if primary else None
            full_budget = len(budget_pairs) == len(seeds)
            comparisons.append({'method': method, 'reference': reference, 'primary': primary,
                                'complete_pairs': len(complete), 'incomplete_pairs': len(seeds) - len(complete),
                                **{k: v for k, v in all_stats.items() if k != 'pairs_count'},
                                'reported_effect_basis': 'all measured outcomes',
                                'all_measured_outcomes': all_stats, 'complete_case': complete_stats,
                                'matched_budget_pairs': len(budget_pairs), 'complete_matched_budget_panel': full_budget,
                                'bootstrap_family_adjusted_ci_pp': adjusted,
                                'family_adjusted_confidence': confidence if primary else None,
                                'clear_gain_target_met': bool(primary and deltas and full_budget
                                                              and all_stats['mean_delta_pp'] >= 5 and adjusted[0] > 0)})
    return {'schema_version': 2, 'runs': rows, 'groups': groups, 'comparisons': comparisons,
            'primary_inference': rule,
            'uncertainty_scope': 'Paired percentile bootstrap describes training-seed variation on one fixed dataset split; it does not cover dataset, writer, or task-population generalization.',
            'limitations': ['A real handwritten-digit subset with a custom row split, not the original UCI benchmark or pretrained LLM fine-tuning.',
                            'Planned, actually measured, and retained updates are distinct; failed/unaccounted work prevents a matched-budget primary claim.',
                            'Descriptive paired 95% intervals accompany Bonferroni-adjusted primary-family intervals; uniform/random comparisons are descriptive only.',
                            'Final data remain separate from validation-only model selection; all assigned runs, including missing and failed runs, remain present.']}
