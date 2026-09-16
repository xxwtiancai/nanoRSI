"""Basic invariants: surface policy, gate decisions, budget arithmetic, no-change identity.

Idea-level borrowings from other open RSI projects (no code copied): RSI-Harness's
identity invariant ("no Genome => behaves exactly like the upstream agent") and its
coverage invariant ("every upstream settings key must be routed") become, here,
"an empty proposal changes nothing except the attempt record" and "every protected
path is enforced even when re-included in the allow list".
"""
import json
import random
import tempfile
import unittest

from nanorsi import loop
from nanorsi.gate import GateConfig, decide
from nanorsi.surface import PROTECTED_PATTERNS, SurfacePolicy, check_paths
from tests.test_end_to_end import run_cli
from tests.test_v2_lifecycle import make_v2

EMPTY_PROPOSAL_FIXTURE = '''import json,sys
r=json.load(sys.stdin)
system=r['messages'][0]['content']
request=json.loads(r['messages'][1]['content'])
if 'proposal agent' in system:
    action={'diff': '','hypothesis':{'hypothesis':'no justified improvement remains'}}
else:
    action={'tool':'final'}
print(json.dumps({'content':json.dumps(action),'usage':{'model_calls':1,'input_tokens':10,'output_tokens':10,'cost_usd':None}}))
'''


class SurfacePolicyInvariants(unittest.TestCase):
    def test_protected_paths_are_enforced_even_when_reincluded_in_allow(self):
        for pattern in PROTECTED_PATTERNS:
            exemplar = pattern if not pattern.endswith("/**") else pattern[:-3] + "/file"
            with self.subTest(pattern=pattern):
                self.assertEqual(check_paths([exemplar], ["**"]), [exemplar])

    def test_allowlist_membership_is_exactly_the_allowed_paths(self):
        policy = SurfacePolicy(["target/**"], [])
        self.assertEqual(policy.validate_paths(["target/a.py", "target/sub/b.py"]),
                         ["target/a.py", "target/sub/b.py"])
        for path in ["targetx/a.py", "evaluator/run.py", "proposer", "a/target/b"]:
            with self.subTest(path=path):
                with self.assertRaises(ValueError):
                    policy.validate_paths([path])

    def test_denying_can_only_shrink_the_allowed_set(self):
        universe = ["target/a.py", "target/skills/b.md", "docs/c.md", "src/d.py"]
        base = set(p for p in universe if not check_paths([p], ["target/**", "docs/**"]))
        narrowed = set(p for p in universe if not check_paths([p], ["target/**", "docs/**"], ["**/b.md"]))
        self.assertTrue(base >= narrowed)


class GateDecisionInvariants(unittest.TestCase):
    def random_case(self, rng):
        parent = rng.uniform(-2, 2)
        child = parent + rng.uniform(-1, 3)
        return parent, child

    def test_ties_are_never_accepted(self):
        rng = random.Random(11)
        for _ in range(200):
            parent, _ = self.random_case(rng)
            for minimum in [0.0, 0.1, 1.0]:
                decision = decide(GateConfig(minimum_improvement=minimum), parent={"score": parent}, child={"score": parent},
                           parent_heldout=None, child_heldout=None)
                self.assertEqual(decision.decision, "rejected")

    def test_acceptance_is_monotone_in_the_child_score(self):
        rng = random.Random(12)
        for _ in range(200):
            parent, child = self.random_case(rng)
            grown = child + rng.uniform(0.01, 2)
            base = decide(GateConfig(), parent={"score": parent}, child={"score": child}, parent_heldout=None, child_heldout=None).decision
            lifted = decide(GateConfig(), parent={"score": parent}, child={"score": grown}, parent_heldout=None, child_heldout=None).decision
            self.assertFalse(base == "accepted" and lifted != "accepted")

    def test_minimum_improvement_boundary_is_exact(self):
        parent = {"score": 1.0}
        exactly = decide(GateConfig(minimum_improvement=0.5), parent=parent, child={"score": 1.5}, parent_heldout=None, child_heldout=None)
        below = decide(GateConfig(minimum_improvement=0.5), parent=parent, child={"score": 1.4999}, parent_heldout=None, child_heldout=None)
        self.assertEqual(exactly.decision, "accepted")
        self.assertEqual(below.decision, "rejected")

    def test_minimize_direction_mirrors_maximize_with_swapped_roles(self):
        down = decide(GateConfig(), parent={"loss": 2.0}, child={"loss": 1.5}, parent_heldout=None, child_heldout=None,
                      metric="loss", direction="minimize")
        self.assertEqual(down.decision, "accepted")
        rng = random.Random(13)
        for _ in range(200):
            parent_value = rng.uniform(-2, 2)
            child_value = rng.uniform(-2, 4)
            minimize = decide(GateConfig(), parent={"m": parent_value}, child={"m": child_value}, parent_heldout=None,
                              child_heldout=None, metric="m", direction="minimize")
            maximize = decide(GateConfig(), parent={"m": child_value}, child={"m": parent_value}, parent_heldout=None,
                              child_heldout=None, metric="m", direction="maximize")
            self.assertEqual(minimize.decision, maximize.decision)

    def test_failed_constraints_are_inconclusive_and_heldout_regressions_reject(self):
        missing = decide(GateConfig(required_constraints=["tests_passed"]), parent={"score": 0.0},
                         child={"score": 1.0, "constraints": {"tests_passed": False}}, parent_heldout=None, child_heldout=None)
        regression = decide(GateConfig(max_heldout_regression=0.0), parent={"score": 0.0}, child={"score": 1.0},
                            parent_heldout={"score": 1.0}, child_heldout={"score": 0.5})
        self.assertEqual(missing.decision, "inconclusive")
        self.assertEqual(regression.decision, "rejected")


class BudgetArithmeticInvariants(unittest.TestCase):
    def test_reservation_accounting(self):
        started = [{"event_type": "evaluation_started", "phase": "search", "episodes": 3, "reservation_id": "r1"}]
        settled = [{"event_type": "episode_reservation_settled", "reservation_id": "r1"}]
        self.assertEqual(loop.search_episode_count([]), 0)
        self.assertEqual(loop.search_episode_count(started), 3)
        self.assertEqual(loop.search_episode_count(started + settled), 3)
        partial = started + settled + [{"event_type": "evaluation_started", "phase": "search", "episodes": 2, "reservation_id": "r2"}]
        reserved = [{"event_type": "episode_reservation", "reservation_id": "r2", "episodes": 5}]
        self.assertEqual(loop.search_episode_count(partial + reserved), 3 + 5)

    def test_spent_is_monotone_across_event_prefixes(self):
        events = []
        totals = [0]
        for episodes in [1, 4, 2, 0, 5]:
            events.append({"event_type": "evaluation_started", "phase": "search", "episodes": episodes})
            totals.append(loop.search_episode_count(events))
        self.assertEqual(totals, sorted(totals))


class NoChangeIdentityInvariants(unittest.TestCase):
    def test_empty_proposal_changes_nothing_but_the_attempt_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_v2(tmp)
            (root / 'adapters/fixture.py').write_text(EMPTY_PROPOSAL_FIXTURE)
            self.assertEqual(run_cli('baseline', '--workspace', str(root)).returncode, 0)
            events = [json.loads(line) for line in (root / 'lineage.jsonl').read_text().splitlines()]
            baseline = next(e for e in events if e.get('event_type') == 'generation' and e.get('decision') == 'baseline')
            result = run_cli('step', '--workspace', str(root))
            self.assertEqual(result.returncode, 0, result.stderr)
            events = [json.loads(line) for line in (root / 'lineage.jsonl').read_text().splitlines()]
            latest = next(e for e in reversed(events) if e.get('event_type') == 'generation')
            noop = next(e for e in events if e.get('event_type') == 'attempt_failed')
            self.assertEqual(noop['decision'], 'no-op')
            self.assertEqual(latest['candidate_commit'], baseline['candidate_commit'])
            self.assertEqual(latest['gate_metrics'], baseline['gate_metrics'])
            ledger = [json.loads(line) for line in (root / 'reports/evidence.jsonl').read_text().splitlines()]
            self.assertEqual([record['decision'] for record in ledger], ['no-op'])
            self.assertIsNone(ledger[0]['metric']['delta'])

    def test_repeated_evaluation_of_one_workspace_is_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_v2(tmp)
            for args in (['baseline'], ['run']):
                self.assertEqual(run_cli(*args, '--workspace', str(root)).returncode, 0)
            first = run_cli('evaluate', '--split', 'validation', '--workspace', str(root))
            second = run_cli('evaluate', '--split', 'validation', '--workspace', str(root))
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(first.stdout, second.stdout)


if __name__ == '__main__':
    unittest.main()
